---
name: TECH-39-glyph-mask-calligram
category: art
source: pretext-skills/SKILL-11.md
also-in: 
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Glyph-mask calligram (big letter filled with small text)

**Category:** art
**Status:** demo-only

## What it does

Render a huge letterform (e.g. "R" in Playfair) as a Canvas pixel mask via `ctx.measureText` + `getImageData`, then for each Y scan line find the pixel extent of the glyph and feed that width to `layoutNextLine()` with body text. The result: a letter shape "filled" with smaller words. No SDF, no opentype.js needed — just Canvas pixel inspection.

## When to use

- Editorial drop-cap pages filled with lorem ipsum
- Poster gallery with big letters and tiny fill text
- Magazine-style opening pages

## How it works

```js
// Concept — Source: SKILL-11 (Pixel-Mask technique)
// 1. Render the big glyph at full canvas size to an offscreen canvas with solid fill
// 2. For each scan line Y, walk ctx.getImageData pixels; find x_left, x_right where alpha > 0
// 3. Feed (x_right - x_left) as maxWidth to layoutNextLine(body, cursor, width)
// 4. Draw body line at (x_left, y)
```

## Minimal example

```js
// Source: SKILL-11 defaults: canvas 500 px, fill font 11 px, fill model 'lorem' or 'self'
```

## Gotchas

- `getImageData` on large canvases is memory-heavy — scale down the mask if only the outline is needed.
- For high-DPI rendering, match mask canvas DPR to viewport or widths drift.
- Case and columns (1–4) of fill text affect readability dramatically.

## Cross-references

- Related: TECH-38-calligram-shape, TECH-40-letterbox-gallery
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
