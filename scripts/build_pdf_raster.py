#!/usr/bin/env python3
"""Render the scalability report HTML to a single-page (non-paginated) PDF
via full-page screenshot + img2pdf.

This is the raster fallback path used by ``build_pdf.py`` when the natural
content height would require a scale factor below the configured threshold
(typography breaks down). It can also be invoked directly for image-only
output.

Approach: full-page Playwright screenshot at 2x device scale + img2pdf
wrapper. Chromium's printToPDF auto-paginates and rotates pages taller than
~14,400 points, so the screenshot path is the only reliable way to get a
true non-paginated PDF when content exceeds that ceiling.

Usable as a module:
    from build_pdf_raster import render_raster_pdf
    render_raster_pdf(html_path, pdf_path)

Or as a script (uses the default paths defined at the bottom).
"""
from __future__ import annotations

import math
import warnings
from pathlib import Path

import img2pdf
from PIL import Image
from playwright.sync_api import sync_playwright

# Silence PIL's "decompression bomb" warning - the screenshot is genuinely
# huge by design and we trust the source.
Image.MAX_IMAGE_PIXELS = None
warnings.filterwarnings("ignore", category=Image.DecompressionBombWarning)

# Render width - matches the design max-width (1080px) plus side padding.
DEFAULT_WIDTH_PX = 1200


def render_raster_pdf(
    html_path: Path,
    pdf_path: Path,
    width_px: int = DEFAULT_WIDTH_PX,
    pt_limit: int = 14_300,
) -> dict:
    """Render ``html_path`` to a single-page raster PDF at ``pdf_path``.

    Returns a dict with ``size_mb``, ``image_w_px``, ``image_h_px`` and
    ``dpi`` for the caller's reporting.
    """
    html_path = Path(html_path)
    pdf_path = Path(pdf_path)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": width_px, "height": 1000},
            device_scale_factor=2,  # high-DPI for crisp text/charts
        )
        page = ctx.new_page()
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle")
        page.add_style_tag(content=".toolbar { display: none !important; }")
        page.emulate_media(media="screen")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(500)

        # Chromium's printToPDF can't emit a single page taller than ~14400 pt
        # (it auto-rotates and paginates instead), so we take a full-page PNG
        # screenshot and wrap it in a PDF. Text is rasterised but stays crisp
        # at 2x device scale.
        screenshot = pdf_path.parent / "_full_page.png"
        page.screenshot(path=str(screenshot), full_page=True, type="png")
        browser.close()

    # Pick a DPI that keeps the resulting PDF page under PDF's 200-inch
    # (14400-pt) hard limit. This is just a unit conversion at encoding
    # time; visible quality is unchanged.
    w_px, h_px = Image.open(screenshot).size
    target_dpi = int(math.ceil(max(72, (h_px * 72.0) / pt_limit)))
    w_pt = w_px * 72.0 / target_dpi
    h_pt = h_px * 72.0 / target_dpi

    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(
            str(screenshot),
            layout_fun=img2pdf.get_layout_fun(pagesize=(w_pt, h_pt)),
        ))
    screenshot.unlink()

    return {
        "size_mb": pdf_path.stat().st_size / 1024 / 1024,
        "image_w_px": w_px,
        "image_h_px": h_px,
        "dpi": target_dpi,
    }


if __name__ == "__main__":
    ROOT = Path(__file__).parent.parent
    HTML = ROOT / "examples" / "starter.html"
    PDF = ROOT / "starter.pdf"
    stats = render_raster_pdf(HTML, PDF)

    import subprocess
    info = subprocess.run(["pdfinfo", str(PDF)], capture_output=True, text=True).stdout
    print(f"Wrote {PDF}")
    print(f"  Size: {stats['size_mb']:.1f} MB")
    print(f"  Image: {stats['image_w_px']} x {stats['image_h_px']} px @ {stats['dpi']} DPI")
    for ln in info.splitlines():
        if "Pages:" in ln or "Page size" in ln:
            print(f"  {ln.strip()}")
