---
name: TECH-07-measure-line-stats
category: api
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-13.md
---

# measureLineStats() — aggregate line stats without string alloc

**Category:** api
**Status:** stable

## What it does

`measureLineStats(prepared, maxWidth) -> { lineCount, maxLineWidth }` returns only the counts/widths you usually want for shrink-wrap, no per-line allocations. Thinner than `walkLineRanges()` if you don't need a custom callback.

## When to use

- Shrink-wrap binary searches that only need line count or widest line
- Overflow checks where the exact lines don't matter
- Fast-path summary after `prepareWithSegments`

## How it works

Internally equivalent to walking the line ranges but returns the aggregate directly.

```ts
// Source: pretext-text-measurement/SKILL.md
import { prepareWithSegments, measureLineStats } from '@chenglou/pretext'
const prepared = prepareWithSegments(article, '16px Inter')
const { lineCount, maxLineWidth } = measureLineStats(prepared, 320)
```

## Minimal example

```ts
// Source: pretext-text-measurement/SKILL.md — binary search for balanced width
function findBalancedWidth(text, font, maxWidth) {
  const prepared = prepareWithSegments(text, font)
  const { lineCount: targetLines } = measureLineStats(prepared, maxWidth)
  let lo = 1, hi = maxWidth
  while (hi - lo > 1) {
    const mid = (lo + hi) / 2
    const { lineCount } = measureLineStats(prepared, mid)
    if (lineCount <= targetLines) hi = mid
    else lo = mid
  }
  return hi
}
```

## Gotchas

- Requires `prepareWithSegments`.
- None documented in source.

## Cross-references

- Related: TECH-06-walk-line-ranges, TECH-41-balanced-headline
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
