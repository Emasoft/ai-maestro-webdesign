---
name: TECH-04-layout-with-lines
category: api
source: pretext-skills/amw-pretext-docs/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, SKILL-14.md, SKILL-16.md, pretext-text-measurement/SKILL.md, pretext-art/SKILL.md
---

# layoutWithLines() — materialize all lines at a fixed width

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Return types (source: pretext-skill-master/SKILL.md)](#return-types-source-pretext-skill-masterskillmd)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** api
**Status:** stable

## What it does

`layoutWithLines(prepared, maxWidth, lineHeight) -> { lines, height, lineCount }` returns every line as `{ text, width, start, end }`. Use for Canvas/SVG `fillText` rendering and for DOM surfaces where you position each line absolutely.

## When to use

- Canvas / SVG text rendering
- Animated kinetic typography (re-run each frame with a new width)
- Absolutely positioned DOM lines
- Anywhere you want the per-line string plus measured width

## How it works

Materializes each wrapped line from the prepared handle — allocates strings (slightly more costly than `walkLineRanges`). Requires `prepareWithSegments()` input.

```ts
// Source: pretext-art/SKILL.md
const prepared = prepareWithSegments(TEXT, FONT)
const { lines } = layoutWithLines(prepared, maxWidth, LINE_HEIGHT)
lines.forEach((line, i) => ctx.fillText(line.text, 0, i * LINE_HEIGHT))
```

## Minimal example

```ts
// Source: pretext-text-measurement/SKILL.md
const prepared = prepareWithSegments('Hello world, this is Pretext!', '18px "Helvetica Neue"')
const { lines } = layoutWithLines(prepared, 320, 26)
lines.forEach((line, i) => ctx.fillText(line.text, 0, i * 26))
```

## Return types (source: pretext-skill-master/SKILL.md)

```ts
type LayoutLine = {
  text: string
  width: number
  start: LayoutCursor  // { segmentIndex: number; graphemeIndex: number }
  end: LayoutCursor    // exclusive end; pass as cursor to next call
}
type LayoutLinesResult = { lineCount: number; height: number; lines: LayoutLine[] }
```

## Gotchas

- Requires `prepareWithSegments` (not `prepare`) or it crashes at runtime.
- If you don't need the string content, prefer `walkLineRanges()` — it skips string allocation.

## Cross-references

- Related: TECH-02-prepare-with-segments, TECH-06-walk-line-ranges
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
