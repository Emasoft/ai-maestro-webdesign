---
name: TECH-22-text-around-floated-image
category: layout
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, SKILL-14.md, SKILL-15.md, SKILL-16.md, pretext-integrate/SKILL.md, pretext-skill-main/patterns.md
---

# Text flowing around a floated image

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** layout
**Status:** stable

## What it does

Classic editorial pattern: an image floats on one side; the first N lines are narrower (column minus image width), remaining lines are full width. Implement with `layoutNextLine()` + a `getLineWidth()` that returns the narrow width while the line's Y is within the image's vertical range.

## When to use

- Article layouts with an illustration
- Blog posts with pull quotes
- Any single-column text that must respect one floating block

## How it works

```ts
// Source: pretext-integrate/SKILL.md — Path C
let cursor = { segmentIndex: 0, graphemeIndex: 0 }
let lineIndex = 0, line
while ((line = layoutNextLine(prepared, cursor, getLineWidth(lineIndex))) !== null) {
  renderLine(line.text, lineIndex)
  cursor = line.end
  lineIndex++
}
function getLineWidth(i) {
  return i < floatHeightInLines ? containerWidth - floatWidth : containerWidth
}
```

## Minimal example

```ts
// Source: pretext-text-measurement/SKILL.md
while (true) {
  const width = y < image.bottom ? columnWidth - image.width : columnWidth
  const range = layoutNextLineRange(prepared, cursor, width)
  if (range === null) break
  const line = materializeLineRange(prepared, range)
  ctx.fillText(line.text, 0, y)
  cursor = range.end
  y += lineHeight
}
```

## Gotchas

- Image margin / padding must be included in `floatWidth`.
- When the image is on the right, the lines are still `width = columnWidth - image.width` but render at the SAME X.

## Cross-references

- Related: TECH-05-layout-next-line, TECH-20-polygon-obstacle-mask
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
