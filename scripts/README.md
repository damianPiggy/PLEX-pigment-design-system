# PDF generation scripts

Tooling to render a Pigment-branded HTML artefact (one made from the design system) as a **single-page, text-selectable, pageless PDF** - the same format the Pigment scalability reports ship in.

The "one tall page" approach is deliberate: editorial long-form content reads naturally as a single continuous flow, paginated only by browser scroll. Standard print CSS breaks this by paginating into fixed-height pages, which destroys the editorial rhythm. These scripts produce a single page sized to the actual content height instead.

## Why this is non-trivial

Chromium's `printToPDF` auto-rotates and paginates any single page taller than ~14,400pt. Long-form Pigment reports hit this routinely. The scripts handle it in four stages:

1. **Probe `@page` injection.** Inject a generous `@page` rule (20,000pt tall) so the layout reflows under the same constraints `printToPDF` will use. Measuring before injection gives a stale height because Chromium reflows when print media activates - the post-injection height can be 1.5-2× the pre-injection height for some templates.
2. **Scale calculation.** Compute the `printToPDF` scale needed to land just under 14,300pt (a 100pt safety margin under the 14,400pt ceiling). The required scale is computed against `PT_TARGET - SCALE_BUFFER` (=14,220pt) so rounding can't push scaled content above the boundary.
3. **Final `@page` re-injection.** Re-inject with the correct dimensions and call `page.pdf()`. Page width is held constant across probe + final (scaling width would re-flow content taller).
4. **Raster fallback.** If the required scale would drop below `MIN_SCALE` (0.55), automatically fall back to `build_pdf_raster.py` (full-page screenshot + img2pdf). The raster path has no scale constraint, so very long content stays readable.

This means callers always get a single-page PDF without needing to know which path produced it.

## Dependencies

```bash
pip install playwright img2pdf pillow
playwright install chromium
```

The vector path uses Playwright + headless Chromium. The raster fallback adds `img2pdf` and `pillow` for the screenshot → PDF conversion.

## Usage

### Vector path (default - text-selectable PDF)

```bash
python scripts/build_pdf.py
# renders examples/starter.html → starter.pdf
```

With custom paths:

```bash
python scripts/build_pdf.py --input my-artefact.html --output my-artefact.pdf
```

Auto-falls back to raster if the required scale would drop below 0.55.

### Raster path (forced)

```bash
python scripts/build_pdf_raster.py
# always uses screenshot + img2pdf
```

Use directly when you know you need the raster path (e.g., HTML uses features Chromium's print pipeline doesn't handle cleanly), or for debugging.

## Constants you can tune

In `scripts/build_pdf.py`:

| Constant | Default | Purpose |
|---|---|---|
| `WIDTH_PX` | `1240` | Render viewport width in pixels. Slightly wider than 1080px design max-width so the PDF has visible outer margin. |
| `PT_CEILING` | `14400` | Chromium's hard single-page limit. Don't change. |
| `PT_TARGET` | `14300` | Where we aim to land. 100pt below the ceiling. |
| `SCALE_BUFFER` | `80` | Extra headroom inside PT_TARGET. Without this, rounding can push scaled content over the boundary. Don't reduce below ~60. |
| `MIN_SCALE` | `0.55` | Below this scale, body text becomes uncomfortably small and the raster fallback kicks in. |
| `INNER_PAD_PX` | `53` | `.page` inner padding for consistent visible margin across viewport widths. |

## What NOT to simplify

These exist for specific reasons; removing them has bitten before:

- **Two-stage measurement.** Measuring before the `@page` rule is injected gives a stale height; Chromium reflows content under print constraints. Pre-injection measurement undersizes the final page → pagination.
- **SCALE_BUFFER.** Scale is computed against `PT_TARGET - SCALE_BUFFER`, not `PT_TARGET` directly. Without it, rounding can push scaled content above the 14,400pt ceiling and trigger a second page.
- **Fixed page width.** Width is held constant across probe + final `@page` injections. Scaling the width re-flows content taller and breaks the page count.
- **The raster fallback.** Some content is too tall for the vector path to keep type readable. Auto-fallback means callers never see a "PDF too cramped" failure mode.

The full rationale is in [`build_pdf.py`'s module docstring](build_pdf.py).
