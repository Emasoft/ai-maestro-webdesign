---
name: TECH-25-shrinkwrap-width
category: typography
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, SKILL-15.md, SKILL-23.md, use-pretext/SKILL.md, pretext-skill-main/patterns.md
---

# Shrink-wrap container width (tightest multiline width)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


**Category:** typography
**Status:** stable

## What it does

Given some text and a max width, find the smallest container width that still fits the same line count — or walk the lines and take the widest. Chat bubbles / tooltips / badges then size themselves to that value instead of the full container. CSS cannot do this with multiline text.

## When to use

- Chat bubbles (tight to the content)
- Tooltips / labels / badges
- Any multiline container that should be "as narrow as possible"

## How it works

```ts
// Source: pretext-text-measurement/SKILL.md
import { prepareWithSegments, walkLineRanges } from '@chenglou/pretext'
const prepared = prepareWithSegments(text, font)
let widest = 0
walkLineRanges(prepared, 320, line => { if (line.width > widest) widest = line.width })
const bubbleWidth = Math.ceil(widest) + paddingH * 2
```

## Minimal example

```ts
// Source: use-pretext/SKILL.md — Recipe 2
// 1) Get target line count at max width
const initial = layout(prepared, contentMax, lineHeight)
// 2) Binary-search smallest width that preserves that line count
let lo = 1, hi = contentMax
while (lo < hi) {
  const mid = Math.floor((lo + hi) / 2)
  if (layout(prepared, mid, lineHeight).lineCount <= initial.lineCount) hi = mid
  else lo = mid + 1
}
// 3) Walk line widths at the found width to get tightest
```

## Gotchas

- Without preserving line count, shrink-wrap collapses a 2-line bubble to 1 very long line.
- `measureLineStats(prepared, maxWidth).maxLineWidth` is a shorter alternative.
- Account for padding / border when setting the final container width.

## Cross-references

- Related: TECH-06-walk-line-ranges, TECH-07-measure-line-stats, TECH-26-balanced-headline
- API reference: [TECH-06-walk-line-ranges](TECH-06-walk-line-ranges.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
