#!/usr/bin/env python3
"""Render the scalability report HTML to a single-page text-selectable PDF.

Uses Chromium's native printToPDF (via Playwright) so all body text,
tables and labels remain copy/paste-able. ~5x smaller than the raster
fallback for typical report sizes.

PDF gotcha (handled here, do not "simplify" away):

    Chromium's printToPDF auto-rotates and paginates any single page taller
    than ~14,400pt. Scrolling-report HTML hits this ceiling routinely. We
    deal with it in four stages:

      1. Inject a generous probe @page rule (20,000pt tall) so the layout
         reflows under the same constraints printToPDF will use, then
         measure the actual content height. Measuring before the @page
         rule is injected gives a stale height because the layout reflows
         when printToPDF takes over - the @page-aware height can be 1.5-2x
         the pre-injection height for some templates, and a stale
         measurement makes the final page too short, causing pagination.
      2. Compute the printToPDF ``scale`` needed to land just under
         ~14,300pt (a 100pt safety margin under the 14,400pt ceiling).
      3. Re-inject the final @page rule with the correct dimensions.
      4. If the required scale is below ``MIN_SCALE`` (typography becomes
         visibly cramped), bail out to the raster fallback in
         ``build_pdf_raster.render_raster_pdf`` automatically.

    This means callers always get a single-page PDF without needing to
    know which path produced it. Don't replace the scale with a constant;
    don't remove the fallback; don't collapse the two-stage measurement
    back into a single pre-injection measurement - the report's natural
    height shifts every time content is added.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
DEFAULT_HTML = ROOT / "examples" / "starter.html"
DEFAULT_PDF = ROOT / "starter.pdf"

# Render viewport. Slightly wider than the 1080px design max-width so the
# resulting PDF page has visible outer paper margin.
WIDTH_PX = 1240

# Chromium's single-page ceiling, with a safety margin.
PT_CEILING = 14_400
PT_TARGET = 14_300  # leave ~100pt headroom under the ceiling

# Extra headroom INSIDE PT_TARGET. The required scale is computed from
# (PT_TARGET - SCALE_BUFFER), not from PT_TARGET directly, so the
# scaled content lands strictly below the page boundary. Without this
# buffer, rounding can push scaled-content height a fraction-of-a-point
# above the page height and trigger a second page in Chromium.
SCALE_BUFFER = 80

# Below this scale, body text becomes uncomfortably small. Fall back to the
# raster path which has no scale constraint.
MIN_SCALE = 0.55

# Inner .page padding. Tuned so the total visible page margin stays
# consistent across viewport widths.
INNER_PAD_PX = 53


def _natural_height_pt(page) -> float:
    """Return the rendered content height in PDF points."""
    height_px = page.evaluate(
        "Math.max("
        "document.documentElement.scrollHeight,"
        "document.body ? document.body.scrollHeight : 0)"
    )
    return float(height_px) * 0.75  # 1px == 0.75pt at 96 DPI


def _prepare_page(page) -> None:
    """Apply screen-media + cosmetic overrides shared by all PDF paths."""
    page.add_style_tag(content=".toolbar { display: none !important; }")
    # SCREEN media keeps the customer-facing typography (no print-mode
    # font-size shrinks, no @page A4 rules from the source stylesheet).
    page.emulate_media(media="screen")


def build_vector_pdf(html_path: Path, pdf_path: Path) -> dict:
    """Render ``html_path`` to a vector single-page PDF at ``pdf_path``.

    Falls back to the raster path automatically if the required scale would
    drop below ``MIN_SCALE``. Returns a dict with ``path``, ``mode``
    ('vector' or 'raster'), and ``scale`` (None for raster).
    """
    # Two-stage render: open Chromium, measure, decide path, close. If we
    # need the raster fallback, it spins up its own Playwright instance -
    # which only works once this outer one has been torn down.
    needs_fallback = False
    required_scale = 1.0
    natural_h_pt = 0.0

    page_w_pt_initial = round(WIDTH_PX * 0.75)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": WIDTH_PX, "height": 1000},
            device_scale_factor=1,
        )
        page = ctx.new_page()
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle")
        _prepare_page(page)
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(500)

        # STAGE 1: inject a generous probe @page rule so the layout reflows
        # under the same constraints printToPDF will apply. Measuring
        # BEFORE this injection underreports the height on some templates,
        # because Chromium re-paginates content once @page kicks in.
        page.add_style_tag(content=f"""
            @page {{
                size: {page_w_pt_initial}pt 20000pt;
                margin: 0;
            }}
            *, *::before, *::after {{
                break-inside: auto !important;
                page-break-inside: auto !important;
                break-before: auto !important;
                page-break-before: auto !important;
                break-after: auto !important;
                page-break-after: auto !important;
            }}
            html, body {{ height: auto !important; }}
            .page {{ padding: 0 {INNER_PAD_PX}px !important; }}
        """)
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(300)

        # STAGE 2: measure the post-reflow content height.
        natural_h_pt = _natural_height_pt(page)
        # Scale to a slightly-smaller target than PT_TARGET so rounding
        # can't push scaled content above the page boundary.
        safe_target = PT_TARGET - SCALE_BUFFER
        required_scale = min(1.0, safe_target / natural_h_pt) if natural_h_pt > 0 else 1.0

        if required_scale < MIN_SCALE:
            needs_fallback = True
        else:
            # Keep page WIDTH constant (matches the probe-stage width), and
            # let the printToPDF scale parameter shrink content within that
            # fixed page. Changing the page width between probe and final
            # would re-flow content (content gets taller in a narrower
            # page), invalidating the measurement and producing 2 pages.
            page_w_pt = page_w_pt_initial
            # Page height = scaled content + the SCALE_BUFFER headroom we
            # already reserved in the scale calc. Clamped to PT_TARGET.
            page_h_pt = min(PT_TARGET, round(natural_h_pt * required_scale) + SCALE_BUFFER)

            # STAGE 3: re-inject the final @page with the correct height.
            page.add_style_tag(content=f"""
                @page {{
                    size: {page_w_pt}pt {page_h_pt}pt;
                    margin: 0;
                }}
            """)
            page.wait_for_timeout(200)

            width_in = page_w_pt / 72.0
            height_in = page_h_pt / 72.0
            page.pdf(
                path=str(pdf_path),
                width=f"{width_in:.3f}in",
                height=f"{height_in:.3f}in",
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                print_background=True,
                scale=required_scale,
                prefer_css_page_size=True,
            )
        browser.close()

    if needs_fallback:
        print(
            f"[build_pdf] natural height {natural_h_pt:.0f}pt would need "
            f"scale {required_scale:.2f} (< MIN_SCALE {MIN_SCALE}); "
            f"falling back to raster path.",
            file=sys.stderr,
        )
        from build_pdf_raster import render_raster_pdf
        render_raster_pdf(html_path, pdf_path)
        return {"path": pdf_path, "mode": "raster", "scale": None}

    return {"path": pdf_path, "mode": "vector", "scale": required_scale}


def _cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a scalability report HTML to a single-page text-selectable PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Defaults: --input {DEFAULT_HTML.relative_to(ROOT)}  --output {DEFAULT_PDF.relative_to(ROOT)}",
    )
    parser.add_argument(
        "--input", "-i", type=Path, default=DEFAULT_HTML,
        help="HTML file to render (default: %(default)s).",
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=DEFAULT_PDF,
        help="PDF file to write (default: %(default)s).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _cli()
    if not args.input.exists():
        sys.exit(f"error: input HTML not found: {args.input}")
    result = build_vector_pdf(args.input, args.output)
    info = subprocess.run(["pdfinfo", str(args.output)], capture_output=True, text=True).stdout
    print(f"Wrote {args.output}")
    print(f"  Mode: {result['mode']}" +
          (f" (scale={result['scale']:.3f})" if result["scale"] else ""))
    print(f"  Size: {args.output.stat().st_size / 1024 / 1024:.2f} MB")
    for ln in info.splitlines():
        if "Pages:" in ln or "Page size" in ln:
            print(f"  {ln.strip()}")
