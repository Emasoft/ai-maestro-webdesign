---
name: TECH-02-prepare-with-segments
category: api
source: pretext-skills/amw-pretext-docs/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, SKILL-14.md, SKILL-16.md, pretext-text-measurement/SKILL.md, pretext-art/SKILL.md
---

# prepareWithSegments() — richer handle for line-level access

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [TypeScript types (source: pretext-skill-master/SKILL.md)](#typescript-types-source-pretext-skill-masterskillmd)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** api
**Status:** stable

## What it does

`prepareWithSegments(text, font, options?) -> PreparedTextWithSegments` returns a superset of `prepare()`'s handle — it additionally exposes enough segmentation to drive `layoutWithLines()`, `layoutNextLine()`, `walkLineRanges()`, `measureLineStats()`, and `measureNaturalWidth()`. Use this the moment you need per-line text, per-line geometry, or variable-width flow.

## When to use

- Canvas/SVG rendering where you need each `line.text`
- Variable-width flow (shaped containers, obstacle routing)
- Shrink-wrap width search (`walkLineRanges`)
- Any layout where widths/positions matter per line

## How it works

`prepareWithSegments()` performs the same Canvas measurement pass as `prepare()` but retains the segment array in the handle so the richer layout functions can materialize line strings and cursors. Do NOT call both for the same text — pick one.

```ts
// Source: pretext-docs/SKILL.md
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'
const prepared = prepareWithSegments('Hello world', '16px Inter')
const { lines } = layoutWithLines(prepared, 320, 22)
```

## Minimal example

```ts
// Source: pretext-art/SKILL.md
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'
const prepared = prepareWithSegments('Words wave and flow', '18px Georgia')
const { lines } = layoutWithLines(prepared, 400, 28)
lines.forEach((line, i) => ctx.fillText(line.text, 0, i * 28))
```

## TypeScript types (source: pretext-skill-master/SKILL.md)

```ts
type PreparedTextWithSegments = PreparedText & {
  segments: string[]                         // e.g. ['hello', ' ', 'world']
  widths: number[]                           // pixel width per segment
  kinds: SegmentBreakKind[]                  // break behavior per segment
  breakableWidths: (number[] | null)[]       // grapheme widths for overflow-wrap
  discretionaryHyphenWidth: number
}

type SegmentBreakKind =
  | 'text' | 'space' | 'preserved-space' | 'tab'
  | 'glue' | 'zero-width-break' | 'soft-hyphen' | 'hard-break'

type LayoutCursor = { segmentIndex: number; graphemeIndex: number }
```

## Gotchas

- Using `prepare` then `layoutWithLines` CRASHES at runtime (no `.segments`). Always match the prepare variant to the layout function.
- Heavier than `prepare()` — use `prepare()` if only height/count needed.
- Cursor type is `{ segmentIndex, graphemeIndex }`, opaque; only pass it to pretext functions, do not inspect.

## Cross-references

- Related: TECH-01-prepare-basics, TECH-04-layout-with-lines, TECH-05-layout-next-line, TECH-06-walk-line-ranges
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
