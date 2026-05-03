---
name: TECH-44-outline-calligram
category: art
source: pretext-skills/SKILL-11.md
also-in: 
---

# Outline calligram (text fills the exact contour of a glyph)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


**Category:** art
**Status:** demo-only

## What it does

Unlike SDF (TECH-38) or pixel-mask (TECH-39) calligrams, the **outline** variant fills the ACTUAL Bezier contour of a font glyph extracted via opentype.js. Pretext + `layoutNextLine` flows body text; opentype.js provides the glyph outline as the shape mask at high precision.

## When to use

- Publication-quality calligram pieces
- Vector-exportable poster art
- Brand logo interiors

## How it works

```js
// Concept — Source: SKILL-11 opentype + Pretext
const glyphPath = font.getPath(letter, 0, 0, displaySize)  // opentype.js
const contour = glyphPath.toPathData()
// For each scan Y inside the glyph's bounding box, raycast the contour to find free slot widths
// Feed the slot widths to layoutNextLine(body, cursor, slotWidth)
```

## Minimal example

Not runnable in a few lines — combines two libraries and per-Y raycasting.

## Gotchas

- Opentype.js cannot parse `.woff2` — use `.woff` or `.ttf` only.
- `font.unitsPerEm` must be the scale factor (`fontSize / font.unitsPerEm`).
- For high-precision rendering, pre-sample the contour at small Y intervals.

## Cross-references

- Related: TECH-38-calligram-shape, TECH-39-glyph-mask-calligram, TECH-52-glyph-path-art
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
