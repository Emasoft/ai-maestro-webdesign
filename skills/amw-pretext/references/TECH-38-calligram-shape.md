---
name: TECH-38-calligram-shape
category: art
source: pretext-skills/SKILL-11.md
also-in: pretext-ui-claude-skills-main
---

# Calligram (word rendered in the shape of what it describes)

**Category:** art
**Status:** demo-only

## What it does

Render a word (`ocean`) using its OWN letters tiled to fill a target shape (a wave, heart, star, spiral). The calligram effect uses an SDF (signed distance function) shape plus `prepareWithSegments` to measure per-character widths, and fills the interior by layout-sampling along the shape.

## When to use

- Typographic posters with meaning in form
- Brand logo experiments
- Heart-shaped love notes, star-shaped badges

## How it works

```js
// Source: SKILL-11.md — Calligrams block
// 1. Define shape SDF: sdfShape(x, y) returns <=0 if inside
// 2. For each Y in shape.bbox, find horizontal span (x0..x1) where sdf<=0
// 3. Feed (x1 - x0) as maxWidth to layoutNextLine with the repeating text
// 4. Render lines at x0, y
```

## Minimal example

```js
// Concept from SKILL-11 defaults
const shapes = ['heart', 'circle', 'star', 'wave', 'spiral']
// Canvas 200–800 px, char density 6–24 px, 10–14 px fill
```

## Gotchas

- Exact glyph fit requires sub-line tuning; small chars look best.
- Without SDF, you can use a Canvas `getImageData` pixel mask (see TECH-39-glyph-mask-calligram).

## Cross-references

- Related: TECH-19-shaped-container, TECH-39-glyph-mask-calligram
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
