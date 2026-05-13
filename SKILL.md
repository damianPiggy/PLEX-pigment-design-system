---
name: pigment-design-system
description: Use when styling ANY Pigment-branded artefact - web pages, marketing pages, slide decks, internal tools UIs, customer docs, prospect collateral, scalability reports, anything HTML/CSS/print. Covers the canonical Pigment 2024 visual identity (Carbon/Titanium foundation, DM Sans + Crimson Pro + JetBrains Mono typography, divider-grid + editorial layout patterns, callout cards, chart palette) decoupled from any specific deliverable. Self-contained - includes copy-paste CSS tokens, component recipes, and a starter HTML skeleton.
---

# Pigment design system

Portable visual identity reference for any Pigment-branded artefact. Encodes colours, typography, and layout from the Pigment 2024 Brand Style Guidelines as plain CSS + component recipes - reusable across web pages, slide decks, scalability reports, internal tools, prospect collateral, anything that should look "Pigment."

The brand pitch in one paragraph: **maturity, elegance, trust** - editorial design + museum wayfinding sensibility. Carbon dark on Titanium cream is the signature pair. Sophisticated Bold accents (Emerald, Cobalt) carry emphasis. Section sub-headers are Crimson Pro serif (classic / sophisticated); display headings are DM Sans Semibold ALL CAPS (impact).

---

## Section 1 - Colours

### Foundation (Carbon / Titanium)

```css
:root {
  /* Carbon scale - typography + dark surfaces */
  --carbon-100: #020D23;
  --carbon-90:  #061336;
  --carbon-50:  rgba(2, 13, 35, 0.65);
  --carbon-40:  rgba(2, 13, 35, 0.40);
  --carbon-20:  rgba(2, 13, 35, 0.10);
  --carbon-10:  rgba(2, 13, 35, 0.04);

  /* Light surfaces */
  --titanium:   #F7F4F3;   /* the signature cream */
  --paper-deep: #EFEAE5;   /* slightly deeper cream for highlighted rows */
  --white:      #FFFFFF;
}
```

| Token | Hex | Use |
|---|---|---|
| `--carbon-100` | `#020D23` | Body text, primary ink, bold strokes |
| `--carbon-90` | `#061336` | Dark backgrounds (hero sections, exec cards) |
| `--carbon-50` | rgba 65% | Secondary text |
| `--carbon-40` | rgba 40% | Tertiary text, placeholders |
| `--carbon-20` | rgba 10% | Borders, dividers, rules |
| `--carbon-10` | rgba 4% | Subtle surface tints |
| `--titanium` | `#F7F4F3` | Page background (the signature cream) |
| `--paper-deep` | `#EFEAE5` | Highlighted rows, depth surfaces |

### Sophisticated palette - Bold variants (for accents + emphasis)

```css
:root {
  --emerald-bold:   #1D683F;
  --cobalt-bold:    #152D80;
  --turquoise-bold: #1A5B70;
  --ochre-bold:     #E9A800;
  --fuchsia-bold:   #720741;
  --amethyst-bold:  #4C2672;
  --sienna-bold:    #C14812;
}
```

Use sparingly - one or two accents per surface. Bold variants are the body emphasis layer (button states, success/info callouts, chart series, link hovers).

### Soft palette - background tints for callouts + tinted surfaces

```css
:root {
  --emerald-soft:   #E8F5CE;
  --cobalt-soft:    #B4D7FF;
  --ochre-soft:     #FBEBB1;
  --fuchsia-soft:   #FFCCE7;
  --amethyst-soft:  #E9CDFF;
  --sienna-soft:    #FBD9B1;
  --turquoise-soft: #B0F1FF;
}
```

Pair each Soft with its Bold for callout cards (background = soft, accent border or label = bold).

### Vivid palette - accent only, use sparingly

```css
:root {
  --emerald-vivid:   #01A54C;
  --cobalt-vivid:    #0355F3;
  --fuchsia-vivid:   #F34F77;
  --ochre-vivid:     #FFD468;
  --sienna-vivid:    #FFC368;
  --turquoise-vivid: #00BBCC;
  --amethyst-vivid:  #AE89FF;
}
```

For highlights, badges, single-point emphasis. Never use Vivid as a body / surface fill.

### Chart-specific palette (tuned for legibility on Titanium)

```css
:root {
  --chart-primary:       #1f4e79;
  --chart-accent:        #2e75b6;
  --chart-positive:      #2e7d32;
  --chart-positive-soft: #66bb6a;
  --chart-neutral:       #5a5a5a;
  --chart-grid:          #cccccc;
  --chart-warn:          #c62828;
}
```

Slightly brighter than the body Bold variants for data visualisation legibility on a cream canvas.

### Semantic aliases - use these in component CSS

```css
:root {
  --ink:        var(--carbon-100);     /* primary text */
  --ink-soft:   var(--carbon-90);      /* dark surface fill */
  --paper:      var(--titanium);       /* page background */
  --rule:       rgba(2,13,35,0.12);    /* borders + dividers */
  --body:       var(--carbon-100);     /* body text */
  --muted:      var(--carbon-50);      /* secondary text */
  --green:      var(--emerald-bold);   /* positive emphasis */
  --green-soft: var(--emerald-soft);
  --blue:       var(--cobalt-bold);    /* primary accent */
  --blue-tint:  rgba(180,215,255,0.35);
  --gold:       var(--ochre-bold);     /* warn / attention */
  --shadow:     0 1px 2px rgba(2,13,35,.04), 0 8px 24px rgba(2,13,35,.06);
}
```

**Always reference these tokens in component CSS rather than raw hex values.** Brand refresh = edit one tokens file → every consumer updates.

### Dark mode swap

```css
@media (prefers-color-scheme: dark) {
  :root {
    --paper: var(--carbon-90);
    --ink:   var(--titanium);
    --rule:  rgba(247,244,243,0.18);
  }
}
```

---

## Section 2 - Typography

### Font stack

| Face | Role | Notes |
|---|---|---|
| **DM Sans** | Headlines, body, eyebrows, table headers, buttons | Geometric sans. **Always enable Alternative-g** via `font-feature-settings: "ss01" on` - the brand guide flags this as important. |
| **Crimson Pro** | Section sub-headers, `<em>` italic emphasis inside headlines, pull quotes | Transitional serif. Gives the editorial / classic touch. |
| **JetBrains Mono** | Numeric `<td>` cells in tables, code refs, technical data labels | Monospace. Headers stay in DM Sans. |

### Loading the fonts

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300..800&family=Crimson+Pro:ital,wght@0,300..600;1,300..600&family=JetBrains+Mono:wght@400;500;700&display=swap">
```

Web-safe fallbacks: `Arial` (DM Sans), `Georgia` (Crimson Pro), `Menlo` (JetBrains Mono).

### Base CSS

```css
body {
  font-family: 'DM Sans', Arial, sans-serif;
  font-feature-settings: "ss01" on;   /* the alt-g glyph */
  color: var(--ink);
  background: var(--paper);
  line-height: 1.5;
}
```

### Type-style spec (from Pigment Brand Style Guidelines pp.35-36)

| Style | Face | Weight | Letter-spacing | Line-height | Casing | Use |
|---|---|---|---|---|---|---|
| Header XL | DM Sans | 600 | -2% | 110% | UPPER | Marketing hero headlines (where impact > elegance) |
| **Sub Header L** | **Crimson Pro** | **400** | **-3%** | **100%** | **Title** | **Cover h1 for customer-facing reports** |
| Sub Header M | Crimson Pro | 400 | -3% | 100% | Title | Body-section h2 |
| Sub Header S | Crimson Pro | 500 | -2% | 100% | Title | h3 subsections |
| Sub Header XS | DM Sans | 600 | 0% | 110% | Title | h4 / nested |
| Eyebrow | DM Sans | 700 | 7% | 110% | UPPER | Section kickers, meta tags |
| Body | DM Sans | 400 | - | 1.5 | Sentence | Paragraph text |
| Quotes | Crimson Pro | 300 italic | - | 1.4 | Sentence | Pull quotes, ledes |
| Buttons | DM Sans | 500 | - | 1 | Sentence | CTAs |

**Important practice note.** For customer-facing reports (scalability assessments, prospect deliverables, etc.) the **cover h1 uses Sub Header L** (Crimson Pro 400 mixed-case), NOT Header XL (DM Sans uppercase). Header XL is reserved for marketing hero contexts where the brand wants to lean into shouty impact. The Valeo scalability report convention, validated as the canonical pattern, uses Crimson Pro for the cover headline with the `<em>` element picking up emerald-bold italic emphasis. The `examples/starter.html` in this repo demonstrates this verbatim.

CSS recipe - cover h1 (Crimson Pro mixed-case, emerald-italic `<em>`):

```css
.cover h1 {
  font: 400 64px/1.0 'Crimson Pro', Georgia, serif;
  letter-spacing: -0.03em;
  color: var(--ink);
  margin: 0 0 26px;
  max-width: 18ch;
}
.cover h1 em {
  font-style: italic;
  font-weight: 400;
  color: var(--emerald-bold);
}
```

CSS recipe - body-section h2 / h3:

```css
section.body h2 {
  font: 400 32px/1.05 'Crimson Pro', Georgia, serif;
  letter-spacing: -0.03em;
  margin: 36px 0 16px;
}
section.body h2 em {
  font-style: italic;
  color: var(--emerald-bold);
  font-weight: 400;
}
section.body h3 {
  font: 500 22px/1.0 'Crimson Pro', Georgia, serif;
  letter-spacing: -0.02em;
}
```

CSS recipe - eyebrow with the canonical emerald-dash prefix:

```css
.eyebrow {
  font: 700 11px/1.1 'DM Sans', sans-serif;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--emerald-bold);
  display: inline-flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 30px;
}
.eyebrow::before {
  content: "";
  width: 36px;
  height: 1px;
  background: var(--emerald-bold);
}
```

CSS recipe - marketing-hero h1 (Header XL spec, used outside customer reports):

```css
.hero h1 {
  font: 600 56px/1.1 'DM Sans', sans-serif;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  margin: 0;
}
```

### Italic emphasis pattern

Headlines and h2 strings use `<em>` to lift key phrases into Crimson Pro italic, creating typographic contrast against surrounding DM Sans:

```html
<h2>Validated for <em>660-1,000</em> active users</h2>
<h1>Prepare for <em>anything</em></h1>
```

```css
h1 em, h2 em {
  font-family: 'Crimson Pro', Georgia, serif;
  font-style: italic;
  font-weight: 400;
}
/* When the heading itself is Crimson Pro (h2), the em can use DM Sans italic instead for contrast */
h2 em {
  font-family: inherit;  /* stays Crimson Pro italic */
}
```

### Numeric cells in tables

```css
td.num {
  font-family: 'JetBrains Mono', Menlo, monospace;
  text-align: right;
  font-variant-numeric: tabular-nums;
}
th.num {
  text-align: right;   /* DM Sans, NOT monospace */
}
```

This split is deliberate: headers stay typographically consistent with the rest of the table; only data cells get the monospace feel for column alignment.

---

## Section 3 - Layout

### The divider-grid invariant

Any divider-bordered grid (factsheet, KPI strip, pillars, feature grid) needs left-padding on every cell except the first, so content doesn't visually crash into the previous cell's right divider.

```css
.grid > div {
  padding-right: 22px;
  border-right: 1px solid var(--rule);
}
.grid > div:not(:first-child) {
  padding-left: 22px;
}
.grid > div:last-child {
  border-right: none;
  padding-right: 0;
}
```

The `:not(:first-child)` keeps the leading cell flush with surrounding paragraph margin while giving cells 2+ breathing room. Symmetric uniform padding is also acceptable when first-cell flush-alignment isn't a concern - the rule is **"no zero-padding side facing a divider"**, not a specific recipe.

### Section-banner pattern

Eyebrow kicker (DM Sans 700 7%-tracking ALL CAPS) above a Crimson Pro h2:

```html
<div class="section-head">
  <div class="num">03 · Industry context</div>
  <h2>From <em>concurrent</em> users to <em>active</em> users</h2>
</div>
```

```css
.section-head .num {
  font: 700 11px/1.1 'DM Sans', sans-serif;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--ink);
  margin-bottom: 8px;
}
.section-head h2 {
  font: 400 32px/1.0 'Crimson Pro', Georgia, serif;
  letter-spacing: -0.03em;
}
```

### Brand bar (header)

Two-column flex: Pigment wordmark SVG + thin vertical divider + "Platform Excellence" label on the left; right-aligned meta with confidentiality + audience + date + version. Anchored by a Carbon-rule border below.

```html
<header class="brandbar">
  <div class="mark">
    <span class="logo"><!-- Pigment wordmark SVG, height 26px --></span>
    <span class="divider"></span>
    <span class="label">Platform Excellence</span>
  </div>
  <div class="meta">
    Confidential &middot; Prepared for &lt;Audience&gt;<br>
    <strong>13th May 2026</strong> &middot; v1.0
  </div>
</header>
```

```css
.brandbar {
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid var(--rule); padding: 26px 0 22px;
}
.brandbar .mark { display: flex; align-items: center; gap: 18px; }
.brandbar .mark .logo { height: 26px; display: block; }
.brandbar .mark .logo svg { height: 100%; width: auto; display: block; }
.brandbar .mark .divider { width: 1px; height: 22px; background: var(--rule); }
.brandbar .mark .label {
  font: 700 11px/1 'DM Sans', sans-serif;
  letter-spacing: 0.07em; text-transform: uppercase;
  color: var(--carbon-50);
}
.brandbar .meta {
  font: 500 11px/1.6 'DM Sans', sans-serif;
  letter-spacing: 0.07em; text-transform: uppercase;
  color: var(--muted); text-align: right;
}
.brandbar .meta strong { color: var(--ink); font-weight: 700; }
```

### Cover (customer-facing report front-matter)

The canonical cover structure used by the scalability-report pipeline. Emerald-dashed eyebrow, Crimson Pro mixed-case headline with emerald-italic `<em>`, Crimson Pro 300 italic lede, and a 4-cell factsheet grid with the divider-grid padding invariant.

```html
<section class="cover">
  <div class="eyebrow">Customer scalability assessment</div>
  <h1>Validated for <em>660-1,000</em> active users.</h1>
  <p class="lede">Across nine load test runs ... <strong>660-1,000 active user base</strong>.</p>
  <div class="factsheet">
    <div><div class="label">Test journey</div><div class="value">User journey - full month-end</div></div>
    <div><div class="label">Concurrency range</div><div class="value">1 &middot; 10 &middot; ... &middot; 100</div></div>
    <div><div class="label">Driver footprint</div><div class="value">10 GCP zones, EMEA + AMER</div></div>
    <div><div class="label">Reporting date</div><div class="value">10th May 2026</div></div>
  </div>
</section>
```

```css
.cover { padding: 64px 0 56px; border-bottom: 1px solid var(--rule); position: relative; }
.cover .eyebrow {
  font: 700 11px/1.1 'DM Sans', sans-serif;
  letter-spacing: 0.07em; text-transform: uppercase;
  color: var(--emerald-bold); margin-bottom: 30px;
  display: inline-flex; align-items: center; gap: 14px;
}
.cover .eyebrow::before {
  content: ""; width: 36px; height: 1px; background: var(--emerald-bold);
}
.cover h1 {
  font: 400 64px/1.0 'Crimson Pro', Georgia, serif;
  letter-spacing: -0.03em; color: var(--ink);
  margin: 0 0 26px; max-width: 18ch;
}
.cover h1 em { font-style: italic; font-weight: 400; color: var(--emerald-bold); }
.cover .lede {
  font: 300 22px/1.4 'Crimson Pro', Georgia, serif;
  font-style: italic; letter-spacing: -0.01em;
  color: var(--ink-soft); max-width: 60ch; margin: 0 0 36px;
}
.cover .lede strong { font-weight: 600; font-style: italic; color: var(--emerald-bold); }
.cover .factsheet {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 0;
  border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule);
  margin-top: 40px;
}
.cover .factsheet > div { padding: 18px 22px 18px 0; border-right: 1px solid var(--rule); }
.cover .factsheet > div:not(:first-child) { padding-left: 22px; }
.cover .factsheet > div:last-child { border-right: none; padding-right: 0; }
.cover .factsheet .label {
  font: 700 10px/1 'DM Sans', sans-serif;
  letter-spacing: 0.07em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 8px;
}
.cover .factsheet .value {
  font: 500 19px/1.2 'Crimson Pro', Georgia, serif;
  letter-spacing: -0.02em; color: var(--ink);
}
```

### Executive summary (dark card with emerald stripe + KPI strip)

The signature feature block for any report-shaped artefact. Dark Carbon-100 background, 6px emerald accent stripe down the right edge, Crimson Pro h2 in titanium with emerald-soft italic `<em>`, body paragraphs in titanium 78%, pull quote with emerald-bold left-border, and a 5-cell KPI strip across the bottom.

```html
<section class="summary">
  <div class="tag">Executive Summary</div>
  <h2>Linear scaling through <em>100 concurrent users</em> ... zero degradation.</h2>
  <p>Pigment delivers <strong>linear scalability ...</strong></p>
  <p class="pull">Translated to the customer's planning horizon ...</p>
  <div class="kpis">
    <div><div class="num">100<small>&nbsp;users</small></div><div class="lab">Validated concurrent capacity ...</div></div>
    <div><div class="num">110.1<small>&nbsp;iter/hr</small></div><div class="lab">Full month-end iterations per hour ...</div></div>
    <!-- 5 cells total -->
  </div>
</section>
```

```css
.summary {
  margin: 56px 0; padding: 52px 56px; border-radius: 4px;
  background: var(--carbon-100); color: rgba(247,244,243,0.85);
  position: relative; overflow: hidden;
  box-shadow: var(--shadow);
}
.summary::before {
  content: ""; position: absolute; top: 0; right: 0; bottom: 0;
  width: 6px; background: var(--emerald-bold);
}
.summary .tag {
  font: 700 11px/1.1 'DM Sans', sans-serif;
  letter-spacing: 0.07em; text-transform: uppercase;
  color: var(--emerald-soft); margin-bottom: 18px;
}
.summary h2 {
  font: 400 38px/1.05 'Crimson Pro', Georgia, serif;
  letter-spacing: -0.03em; color: var(--titanium);
  margin: 0 0 24px; max-width: 26ch;
}
.summary h2 em { font-style: italic; color: var(--emerald-soft); font-weight: 400; }
.summary p {
  font-size: 15.5px; line-height: 1.6;
  color: rgba(247,244,243,0.78);
  max-width: 60ch; margin: 0 0 14px;
}
.summary p strong, .summary .pull strong { color: var(--titanium); font-weight: 600; }
.summary .pull {
  border-left: 2px solid var(--emerald-bold);
  padding: 8px 0 8px 20px; margin: 28px 0 6px;
  font: 400 italic 21px/1.4 'Crimson Pro', Georgia, serif;
  letter-spacing: -0.015em; color: var(--titanium); max-width: 56ch;
}

/* KPI strip - 5 columns, divider-grid padding applied. */
.kpis {
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 0;
  margin-top: 38px; padding-top: 28px;
  border-top: 1px solid rgba(255,255,255,.18);
}
.kpis > div { padding-right: 16px; border-right: 1px solid rgba(255,255,255,.12); }
.kpis > div:not(:first-child) { padding-left: 16px; }
.kpis > div:last-child { border-right: none; }
.kpis .num {
  font: 500 40px/1 'Crimson Pro', Georgia, serif;
  letter-spacing: -0.03em; color: var(--titanium); margin-bottom: 10px;
}
.kpis .num small {
  font-size: 16px; color: var(--emerald-soft);
  font-weight: 500; letter-spacing: -0.01em;
}
.kpis .lab {
  font-size: 12px; font-weight: 500; line-height: 1.4;
  color: rgba(247,244,243,0.65);
}
```

**Five KPI cells only** - never six. The user explicitly fixed this on the Valeo build; a sixth dilutes the impact and the divider grid stops feeling editorial.

### Page footer (mirror of the brand bar)

```html
<footer>
  <div>
    <div class="brand">
      <span class="logo"><!-- Pigment wordmark SVG, height 18px --></span>
      <span class="label">Platform Excellence</span>
    </div>
    <div class="credit">Prepared by Damian Arnold &middot; Technical Solutions Lead</div>
    <div class="note">Customer-specific footer note here.</div>
  </div>
  <div class="meta">Report v1.0<br>&copy; 2026</div>
</footer>
```

```css
footer {
  padding: 36px 0 56px; border-top: 1px solid var(--rule);
  display: grid; grid-template-columns: 1fr auto; gap: 24px;
  align-items: end; font-size: 12px; color: var(--muted);
}
footer .brand { display: flex; align-items: center; gap: 14px; }
footer .brand .logo { height: 18px; display: block; }
footer .brand .label {
  font: 700 11px/1 'DM Sans', sans-serif;
  letter-spacing: 0.07em; text-transform: uppercase; color: var(--carbon-50);
}
footer .meta {
  font: 500 11px/1.4 'DM Sans', sans-serif;
  letter-spacing: 0.07em; text-transform: uppercase; text-align: right;
}
footer .credit { margin-top: 14px; color: var(--ink); font-weight: 600; font-size: 13px; }
footer .note { margin-top: 6px; color: var(--muted); font-size: 12px; max-width: 60ch; }
```

### Callout cards

Three themes mapped to the soft palette + bold accents:

```css
.callout {
  padding: 18px 22px;
  border-radius: 2px;
  margin: 18px 0;
}
.callout.info {
  background: var(--cobalt-soft);
  border-left: 4px solid var(--cobalt-bold);
}
.callout.positive {
  background: var(--emerald-soft);
  border-left: 4px solid var(--emerald-bold);
}
.callout.warn {
  background: var(--ochre-soft);
  border-left: 4px solid var(--ochre-bold);
}
.callout .label {
  font: 700 11px/1.1 'DM Sans', sans-serif;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--ink);
  margin-bottom: 4px;
}
.callout .body {
  font: 400 15px/1.5 'DM Sans', sans-serif;
  color: var(--body);
}
```

Use sparingly - one or two per page section, never stacked.

### Editorial whitespace

- **Generous outer margins.** Editorial layouts breathe; treat the page edge as a frame, not a constraint.
- **Section padding ~64-96px top/bottom** for primary sections; ~32-48px for nested subsections.
- **Body text max-width 65-72ch** for readability. Don't run paragraphs the full page width.
- **18-22px gap** between cells inside divider grids - matches the padding-left value used in the grid recipe.
- **Asymmetric grids** (1-2 / 2-1 / sidebar-main) feel more editorial than symmetric four-column splits.

### Card / surface shadow

One shadow recipe, applied to elevated surfaces (KPI cards, hero panels, modal sheets):

```css
.card {
  background: var(--paper);
  box-shadow: var(--shadow);
  border-radius: 4px;
  padding: 24px;
}
```

`--shadow` = `0 1px 2px rgba(2,13,35,.04), 0 8px 24px rgba(2,13,35,.06)`. Soft and Carbon-tinted; never use a neutral grey shadow on Titanium paper.

### Tables

```css
table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
}
th {
  text-align: left;
  font-weight: 600;
  color: var(--ink);
  border-bottom: 2px solid var(--ink);
  padding: 12px 14px;
}
td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--rule);
  color: var(--body);
}
tr.highlight td { background: var(--paper-deep); font-weight: 600; }
```

---

## Section 4 - Logos + assets

The Pigment press kit lives at `~/Downloads/Pigment press kit/`. Logo variants: `PigmentLogo_Digital_<Style>_<Form>.{svg,png}`.

| Background | Style | Form | When |
|---|---|---|---|
| Light (Titanium) | `Colors` | `Full` | Standard customer-facing |
| Light (Titanium) | `AllDark` | `Full` | Monochrome dark on light |
| Dark (Carbon 90) | `AllWhite` | `Full` | Hero / cover on dark |
| Dark (Carbon 90) | `WhiteText` | `Full` | Coloured P-mark + white wordmark |
| Header / icon | any | `Icon` | Just the P-mark (115×136 viewBox) |
| Wordmark only | any | `Text` | Where the P-mark would be redundant |

`Full` viewBox: 704×136. `Icon` viewBox: 115×136. For standalone single-file HTML, inline the SVG; for tooling that doesn't accept SVG (python-pptx, some print tools) use the matching PNG.

---

## Section 5 - Starter HTML skeleton

See [`examples/starter.html`](examples/starter.html) - a complete, working single-file artefact demonstrating every canonical pattern in this skill:

- Brand bar header (Pigment wordmark SVG + Platform Excellence label + meta)
- Cover section (emerald-dashed eyebrow + Crimson Pro h1 + italic lede + 4-cell factsheet)
- Executive summary card (dark Carbon-100 surface + emerald stripe + Crimson h2 + pull quote + 5-KPI strip)
- Numbered body section (eyebrow kicker + Crimson h2 + supporting prose)
- Callout cards (info / positive / warn themes)
- Numeric table (DM Sans headers, JetBrains Mono right-aligned cells)
- Page footer (mirror of the brand bar, with credit + version + copyright)

The starter is byte-aligned with the load-tester scalability-report templates (same class names, same CSS values, same wordmark SVG), so anything built from it can be ported into the report pipeline directly.

To use:

```bash
cp examples/starter.html my-new-artefact.html
# edit the cover / summary / body content; CSS tokens at the top of <style>
# stay the same so the brand identity is preserved automatically
```

Drop into any browser as a standalone file - no build step, no preprocessing. Edit, save, refresh.

---

## Section 6 - Implementation patterns

### Single source of truth

Centralise the `:root` token block in one CSS file (e.g. `_tokens.css`). Inline it into the HTML `<style>` for standalone deliverables, or `@import` it for multi-page sites. Never inline a raw hex code in component CSS - reference the token name. Brand refresh = edit one file.

### Brand-refresh workflow

1. Update hex values in the tokens file.
2. Visually verify against a sample artefact.
3. Every consumer of the tokens picks up the change automatically.

If you find yourself doing find-and-replace across multiple files, your tokens aren't actually centralised.

### When to add a new token

Add to the tokens file when:
- A new palette tier is needed (e.g. introducing the Vivid layer).
- A new semantic role emerges (e.g. `--warning-banner-bg` for a recurring component).

Don't add when:
- One component needs a one-off shade. Use rgba() of an existing token instead.
- The value would only be referenced once.

---

## Red flags

| Thought | Reality |
|---|---|
| "I'll inline the hex once, just here" | Reference the token. Every untokenised hex is a future brand-refresh bug. |
| "Pure black or pure dark grey for text" | Pigment uses Carbon 100 (`#020D23`) - it has subtle blue undertone. Pure black breaks the brand feel. |
| "Use Vivid Cobalt for the primary button" | Vivid is accent-only. Use Bold (`#152D80`) for body emphasis; Vivid is for badges / single-point highlights. |
| "Add a 6th colour to the chart series" | Stay within the 7-colour chart palette. More than 5 series on a single chart is usually a comprehension problem, not a colour problem. |
| "Skip the ss01 font-feature-settings, default DM Sans looks fine" | The Alternative-g is part of the brand. The default g looks different and the style guide explicitly flags this. |
| "Use grey shadow on Titanium paper" | Shadow tint should be Carbon-rgba, never neutral grey. The `--shadow` recipe is in the tokens. |
| "Inline the divider line directly between cells" | Cell content will crash into it. Apply the `:not(:first-child) { padding-left: 22px }` recipe. |
| "Headings in Crimson Pro Bold, body in DM Sans Bold" | Crimson Pro is Regular/Medium. DM Sans Semibold is the body-bold weight. Don't use heavy weights of Crimson Pro - it's a transitional serif, not a display face. |
| "Cover h1 in DM Sans Semibold uppercase (Header XL)" | For customer-facing reports the cover h1 is **Crimson Pro 400 mixed-case** (Sub Header L), with the `<em>` element picking up emerald-bold italic. Header XL is reserved for marketing-hero contexts where shouty impact > editorial elegance. The Valeo report's "Validated for *660-1,000* active users." is the canonical reference. |
| "Reuse `.num` class for both section eyebrows AND numeric table cells" | They look similar in markup but the section eyebrow uses display: inline-flex with an emerald ::before dash. If the CSS rule isn't scoped (`section.body > .num`), it cascades into `td.num` cells and breaks the table layout entirely. Use direct-child combinators or rename the eyebrow class. |
| "Stretch paragraphs to the full content width" | Editorial readability tops at ~70ch. Constrain `<p>`. |
| "Italic via `<i>` for SEO neutrality" | Use `<em>` - the CSS rule (`h2 em` → Crimson Pro italic) is keyed on `em`. Semantic stress emphasis matches the typographic intent. |
| "Add a 6th KPI to the executive-summary strip" | Five only. A sixth dilutes the impact and breaks the editorial feel of the divider grid. Move surplus figures into the body narrative or an appendix table. |
