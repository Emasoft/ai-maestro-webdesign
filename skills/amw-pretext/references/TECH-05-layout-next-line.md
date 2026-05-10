---
name: TECH-05-layout-next-line
category: api
source: pretext-skills/amw-pretext-docs/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, SKILL-14.md, SKILL-16.md, pretext-art/SKILL.md, pretext-integrate/SKILL.md
---

# layoutNextLine() — iterator with variable width per line

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** api
**Status:** stable

## What it does

`layoutNextLine(prepared, cursor, maxWidth) -> LayoutLine | null` emits one line at a time, and accepts a DIFFERENT `maxWidth` on every call. This single feature is the key to shaped containers, obstacle routing, multi-column handoff, and non-rectangular flow.

## When to use

- Shaped containers (circle, polygon, silhouette)
- Text around floated images / animated obstacles
- Per-line-width variations (narrower column for the first N lines)
- Multi-column / multi-region handoff using `line.end` as cursor for the next region

## How it works

Each call advances an opaque `LayoutCursor`. `null` signals end-of-text. The caller decides the next `maxWidth` based on geometry at line Y.

```ts
// Source: pretext-art/SKILL.md
let cursor = { segmentIndex: 0, graphemeIndex: 0 }
while ((line = layoutNextLine(prepared, cursor, circleChord(radius, lineY - cy))) !== null) {
  ctx.fillText(line.text, cx, lineY)
  lineY += LINE_HEIGHT
  cursor = line.end
}
```

## Minimal example

```ts
// Source: pretext-integrate/SKILL.md
let cursor = { segmentIndex: 0, graphemeIndex: 0 }
let y = startY, line
while ((line = layoutNextLine(prepared, cursor, maxWidth)) !== null) {
  ctx.fillText(line.text, x, y)
  y += LINE_HEIGHT
  cursor = line.end
}
```

## Gotchas

- Always advance `cursor = line.end` before the next call — otherwise you emit the same line forever.
- Narrow widths (< widest grapheme) return zero-fit lines; clamp `maxWidth` to a sane minimum.
- Requires `prepareWithSegments`.

## Cross-references

- Related: TECH-02-prepare-with-segments, TECH-36-shaped-containers, TECH-39-obstacle-routing-60fps
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
