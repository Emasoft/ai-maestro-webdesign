---
name: TECH-png-export-bridge
category: architecture-graph
source: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/formats.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-png-export-bridge

## What it does

Handles the `png` output format by **returning the same SVG as the `svg`
format plus an appended instructions block** explaining how to convert
it to PNG. The transform does not rasterise inline — PNG conversion
happens outside the skill in whatever environment the caller prefers.

## When to use

- **`output_format: "png"`** — this is the path.
- **When the caller wants a raster image** but does not have a Node
  canvas, sharp, cairosvg, or puppeteer already available.
- **For sharing / social posting / Slack** — PNGs travel better than SVG
  in most non-developer contexts.

Do not use this path when the caller can render SVG directly — the PNG
bridge is for consumers without an SVG-capable renderer.

## How it works

Two-part output:

1. The SVG string produced by the `svg` transform (identical).
2. An appended instructions block listing all the conversion paths
   available:

```
---
To save as PNG:
1. Copy the SVG above into a file named architecture.svg
2. Open it in any browser — it renders immediately
3. Right-click the image → "Save image as…" → choose PNG
   OR use the browser's print dialog → Save as PDF, then convert

For programmatic conversion:
  • Node.js: sharp('architecture.svg').png().toFile('architecture.png')
  • Python:  cairosvg.svg2png(url='architecture.svg', write_to='architecture.png')
  • CLI:     inkscape architecture.svg --export-png=architecture.png
  • Online:  https://svgtopng.com
```

## Minimal example

Caller passes `output_format: "png"`. The skill returns:

```
<svg xmlns="http://www.w3.org/2000/svg" width="820" height="620">
  ... (identical to the svg format output) ...
</svg>

---
To save as PNG:
1. Copy the SVG above into a file named architecture.svg
2. Open it in any browser — it renders immediately
...
```

## Gotchas

- **The instructions block MUST appear AFTER the SVG.** If it appears
  before, most Markdown renderers try to parse the instructions as
  part of the SVG and the diagram fails to render. Stage 2 validation
  catches this; re-ordering is a deterministic fix.
- **No inline rasterisation.** The plugin does not ship a Chrome /
  Chromium / puppeteer dependency just for PNG export — the user's
  browser is the fallback rasteriser. Self-contained SVG renders
  correctly in every modern browser, so this works for 100% of users.
- **Programmatic options are listed, not chosen.** The instructions
  enumerate Node / Python / CLI / online tools because different
  environments have different tooling. Letting the caller pick their
  preferred path is more robust than forcing one.
- **Output size.** PNG at 820px wide ≈ 120-180 KB depending on
  complexity; the source SVG is 8-15 KB. For Slack / GitHub issues,
  the PNG is unavoidable; for READMEs, prefer SVG.
- **The `/amw-init` flow** optionally installs `cairosvg` — if present,
  the plugin's `bin/amw-svg-render.py` can rasterise the SVG automatically
  without the caller lifting a finger. The instructions block above is
  the universal fallback when that isn't installed.

## Cross-references

- [formats](formats.md) — the full transform spec for all 4 formats
  > Format 1: `graph` (default) · Schema · Constraints · Format 2: `mermaid` · Transform Rules · Layer Color Mapping · Mermaid Output Template · Mermaid ID Safety · Format 3: `svg` · Layout Algorithm · SVG Structure · SVG Height Calculation · Format 4: `png`
- [TECH-svg-layered-layout](TECH-svg-layered-layout.md) — the transform that produces the SVG
  > What it does · When to use · How it works · Canvas constants · Algorithm · Height calculation · Node card structure · Layer band structure · Minimal example · Gotchas · Cross-references
- `../../../bin/amw-svg-render.py` — optional local rasteriser (Python +
  cairosvg)
- [validation](validation.md) — Stage 2 PNG checks (instructions after SVG, etc.)
  > Stage 1 — Graph Validation (all formats) · 1 Layer count · 2 Node count · 3 Layer balance · 4 Node label quality · 5 Edge integrity · 6 ID integrity · 7 Layer order sequence · Stage 2 — Format Validation · Format: `graph` · Format: `mermaid` · Format: `svg` · Format: `png` · Validation Summary (quick reference) · **Stage 1 — Graph validation**: structural checks on the graph JSON. · **Stage 2 — Format validation**: surface-level checks on the rendered output.
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

