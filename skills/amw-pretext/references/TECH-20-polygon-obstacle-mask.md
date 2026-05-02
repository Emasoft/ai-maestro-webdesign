---
name: TECH-20-polygon-obstacle-mask
category: layout
source: pretext-skills/SKILL-11.md
also-in: pretext-frontend-motion-main, pretext-skill-main/patterns.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Polygon / obstacle mask routing

**Category:** layout
**Status:** stable

## What it does

Text routes around arbitrary convex or concave polygonal obstacles (logos, cutouts, draggable orbs). For each line band, compute the free horizontal interval(s) left by the polygon; feed each free slot width to a `layoutNextLine()` call. The same text stream carries across slots via the `line.end` cursor.

## When to use

- Editorial layouts with illustrations or pull quotes
- Draggable UI obstacles that text must wrap around
- Multi-shape cutouts (multiple floating images)

## How it works

```ts
// Concept — Source: SKILL-11.md (carveTextLineSlots technique)
// 1. For each Y, raycast the polygon to find blocked intervals
// 2. Subtract blocked intervals from the full line width to get free slots
// 3. For each free slot, call layoutNextLine(prepared, cursor, slot.width)
// 4. Render the line at the slot's start X
```

## Minimal example

```ts
// Source: pretext-skill-main/patterns.md (editorial engine)
for (const article of articles) {
  const prepared = prepareWithSegments(article.text, article.font)
  let cursor = { segmentIndex: 0, graphemeIndex: 0 }
  while (cursor) {
    for (let col = 0; col < columns; col++) {
      const colWidth = getColumnWidth(col, y, obstacles)
      const line = layoutNextLine(prepared, cursor, colWidth)
      if (!line) { cursor = null; break }
      renderInColumn(line, col, y)
      cursor = line.end
    }
    y += lineHeight
  }
}
```

## Gotchas

- When an obstacle is mid-line, a SINGLE free slot wastes space — split into left/right and fill both (SKILL-11 calls this `carveTextLineSlots`).
- `MIN_SLOT_WIDTH` (~50 px) prevents unreadable sliver slots.
- Recompute every frame for animated obstacles — `prepare()` is cached so this is cheap.

## Cross-references

- Related: TECH-19-shaped-container, TECH-38-text-around-floated-image, TECH-44-editorial-engine
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
