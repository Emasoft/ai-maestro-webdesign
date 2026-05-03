---
name: TECH-06-walk-line-ranges
category: api
source: pretext-skills/amw-pretext-docs/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, SKILL-14.md, SKILL-16.md, pretext-text-measurement/SKILL.md, use-pretext/SKILL.md
---

# walkLineRanges() — geometry-only line iteration (no string allocation)

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

`walkLineRanges(prepared, maxWidth, onLine) -> lineCount` invokes a callback per line with `{ width, start, end }` — no `text` string is built. Fastest way to compute line widths for shrink-wrap, column balancing, hit-testing, and speculative width probes.

## When to use

- Shrink-wrap bubbles / tooltips / labels
- Binary search for optimal width (balanced headlines)
- Column balancing / hit-testing
- Anywhere you want line geometry without paying for string materialization

## How it works

Same internal line-break loop as `layoutWithLines` but skips the string copy per line. Requires `prepareWithSegments`.

```ts
// Source: pretext-text-measurement/SKILL.md
let widest = 0
walkLineRanges(prepared, 320, line => {
  if (line.width > widest) widest = line.width
})
// widest is the tightest width that still fits the text (shrinkwrap)
```

## Minimal example

```ts
// Source: use-pretext/SKILL.md — Recipe 2 shrink-wrap
let maxLineWidth = 0
walkLineRanges(prepared, lo, line => {
  if (line.width > maxLineWidth) maxLineWidth = line.width
})
const tightWidth = Math.ceil(maxLineWidth) + paddingH * 2
```

## Gotchas

- Callback must not allocate per-line strings if performance matters — that defeats the purpose.
- `start` and `end` are `LayoutCursor`s — useful for slicing the text later if needed.

## Cross-references

- Related: TECH-04-layout-with-lines, TECH-40-shrinkwrap-width, TECH-41-balanced-headline
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
