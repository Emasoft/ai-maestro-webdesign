---
name: TECH-19-shaped-container
category: layout
source: pretext-skills/amw-pretext-art/SKILL.md
also-in: SKILL-11.md, SKILL-14.md, skills/amw-pretext-art/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Shaped container (text inside a circle / polygon / outline)

**Category:** layout
**Status:** stable

## What it does

Fill an arbitrary shape (circle, polygon, silhouette) with flowing text. For each line's Y offset, compute the chord width of the shape and pass it to `layoutNextLine()` as `maxWidth`. The same single text stream wraps to narrower / wider widths as the shape's cross-section changes.

## When to use

- Circular text blocks (posters, stamps)
- Polygonal / custom-outline editorial flows
- Any non-rectangular container where you want tight text flow

## How it works

```ts
// Source: pretext-art/SKILL.md
function circleChord(radius, yOffset) {
  const d = Math.abs(yOffset)
  if (d >= radius) return 0
  return 2 * Math.sqrt(radius * radius - d * d)
}

let cursor = { segmentIndex: 0, graphemeIndex: 0 }
let lineY = cy - radius + LINE_HEIGHT
while (lineY < cy + radius) {
  const line = layoutNextLine(prepared, cursor, circleChord(radius, lineY - cy))
  if (!line) break
  ctx.fillText(line.text, cx, lineY)
  lineY += LINE_HEIGHT
  cursor = line.end
}
```

## Minimal example

```ts
// Source: skills/amw-pretext-art/SKILL.md (plugin)
// Replace circleChord with any shape-width sampler
function polyChord(yOffset, polygon) { /* compute horizontal span of polygon at yOffset */ }
```

## Gotchas

- Scan Y step must equal `LINE_HEIGHT` exactly — mismatches produce gaps or overlap.
- When chord width is narrower than the widest grapheme, `layoutNextLine()` returns a zero-fit line — clamp your chord floor.
- `ctx.textAlign = 'center'` and passing the shape center as X gives proper horizontal centering.

## Cross-references

- Related: TECH-05-layout-next-line, TECH-20-polygon-obstacle-mask, TECH-43-calligram-shapes
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
