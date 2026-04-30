---
name: TECH-09-layout-next-line-range
category: api
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-13.md
---

# layoutNextLineRange() + materializeLineRange() — variable-width iterator without strings

**Category:** api
**Status:** stable

## What it does

`layoutNextLineRange(prepared, cursor, maxWidth) -> LayoutLineRange | null` advances one line at a time returning `{ width, start, end }` (no string) — faster than `layoutNextLine()` when you need per-line widths but build strings only for the lines you actually render. Pair with `materializeLineRange(prepared, range)` to get the string on demand.

## When to use

- Variable-width iteration where some lines are skipped / clipped
- Obstacle-routed text where the geometry loop does an extra pass before rendering
- Two-pass layouts: collect line ranges, decide, then materialize visible lines

## How it works

```ts
// Source: pretext-text-measurement/SKILL.md
const prepared = prepareWithSegments(article, '16px Inter')
let cursor = { segmentIndex: 0, graphemeIndex: 0 }
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

## Minimal example

```ts
// Source: pretext-text-measurement/SKILL.md
const range = layoutNextLineRange(prepared, cursor, width)
if (range) {
  const line = materializeLineRange(prepared, range)
  // use line.text, line.width
}
```

## Return type (source: pretext-skill-master/SKILL.md)

```ts
type LayoutLineRange = {
  width: number
  start: LayoutCursor  // { segmentIndex: number; graphemeIndex: number }
  end: LayoutCursor    // pass as cursor to the next call
}
```

## Gotchas

- Zero string allocation until you call `materializeLineRange()` — so skip that call for lines you discard.
- Requires `prepareWithSegments`.

## Cross-references

- Related: TECH-05-layout-next-line, TECH-38-text-around-floated-image
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
