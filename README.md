# Pigment design system

A portable, reusable visual identity system derived from the **Pigment 2024 Brand Style Guidelines**, intended for use across any HTML/CSS/print artefact that should look and feel "Pigment".

This isn't an official Pigment design-system release - it's a working extract that codifies the brand's editorial / museum-wayfinding sensibility into copy-paste tokens, typography rules, and layout patterns so any new artefact (web pages, slide decks, customer reports, internal tools, prospect collateral) can stay on-brand without re-deriving from the source style guide every time.

## What's in here

| File | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | The canonical reference doc - colours, typography, layout, components, red flags, starter HTML. The whole design system in one self-contained document. |
| [`tokens.css`](tokens.css) | Standalone CSS custom-properties file. Inline it into HTML `<style>` or `@import` it as a stylesheet. The single source of truth for every colour. |
| [`examples/starter.html`](examples/starter.html) | Drop-in standalone single-file HTML that renders on-brand immediately. Useful for prototypes, one-pagers, mockups. |

## Quick start

```bash
git clone https://github.com/damianPiggy/PLEX-pigment-design-system
cd PLEX-pigment-design-system
open examples/starter.html
```

Or for an existing project: copy `tokens.css` into your stylesheet path, import it at the top of your component CSS, and reference the tokens (`var(--ink)`, `var(--paper)`, `var(--emerald-bold)`, etc.) instead of inlining hex codes.

## Brand identity in one paragraph

Pigment's identity is **maturity, elegance, trust** - moving away from startup feel toward enterprise. Visual inspiration: editorial design + museum wayfinding ("timeless professional vibe"). **Carbon dark** (`#020D23`) typography on **Titanium cream** (`#F7F4F3`) paper is the signature pair. Sophisticated Bold accents (Emerald `#1D683F`, Cobalt `#152D80`) carry emphasis. Section sub-headers use **Crimson Pro** serif; display headings use **DM Sans** Semibold ALL CAPS. Numeric data uses **JetBrains Mono** in table cells (only in cells, headers stay DM Sans).

See [`SKILL.md`](SKILL.md) for the full reference - colour palette, typography spec, layout invariants, component recipes, and red flags.

## Usage as a Claude Code skill

[`SKILL.md`](SKILL.md) is structured as a Claude Code skill - it has the frontmatter and tone required for skill activation. To install it into a Claude Code project:

```bash
mkdir -p .claude/skills/pigment-design-system
cp SKILL.md .claude/skills/pigment-design-system/
```

Then Claude Code will activate it whenever you ask to style a Pigment-branded HTML/CSS artefact.

It's also useful as a plain-prose reference for humans - the same content works either way.

## Conventions enforced

- **Single source of truth.** All colours live in `tokens.css`. Never inline a raw hex code in component CSS - reference the token name. Brand refresh = edit one file.
- **Two faces only** for non-numeric typography: DM Sans (sans, primary) and Crimson Pro (serif, accents + headings). JetBrains Mono is the third face but reserved for numeric cells and code refs.
- **Alternative-g glyph** on DM Sans is part of the brand - enable via `font-feature-settings: "ss01" on`.
- **Italic emphasis via `<em>`** inside headings - the CSS rule (`h1 em, h2 em → Crimson Pro italic`) is keyed on `<em>` specifically.
- **No zero-padding side touching a divider** - cells inside divider-bordered grids need internal padding on the divider-facing sides.

## References

- [Pigment Brand Style Guidelines 2024](https://www.pigment.com/) (full 55-page PDF on the press kit)
- [DM Sans on Google Fonts](https://fonts.google.com/specimen/DM+Sans)
- [Crimson Pro on Google Fonts](https://fonts.google.com/specimen/Crimson+Pro)
- [JetBrains Mono on Google Fonts](https://fonts.google.com/specimen/JetBrains+Mono)

## Contributing

This is a working extract maintained as the visual identity evolves. For corrections (wrong hex, outdated type spec, missing pattern), open a PR with a single-file change against `tokens.css` or `SKILL.md` and a short note about the brand-guide page or example that drove the change.

## Status

Working set as of May 2026, tracking the Pigment 2024 Brand Style Guidelines. The colour tokens have been validated against the live `report_charts/templates/_tokens.css` in the [load-tester](https://github.com/damianPiggy/load-tester) repo (private), where they drive the customer-facing scalability reports.
