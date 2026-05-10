---
name: TECH-08-measure-natural-width
category: api
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-13.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# measureNaturalWidth() — unconstrained text width

**Category:** api
**Status:** stable

## What it does

`measureNaturalWidth(prepared) -> number` returns the width the text would take if it NEVER wrapped. Useful for sizing buttons, chips, pills, or any container that should match the intrinsic width of short label text.

## When to use

- Button / chip / pill auto-sizing
- Badge containers that must fit on a single line
- Single-line label width without instantiating a layout

## How it works

Sums the segment widths without applying any line-break rules. Constant-time relative to the number of segments.

```ts
// Source: pretext-text-measurement/SKILL.md
import { prepareWithSegments, measureNaturalWidth } from '@chenglou/pretext'
const prepared = prepareWithSegments('Short label', '14px Inter')
const naturalWidth = measureNaturalWidth(prepared)
```

## Minimal example

```ts
// Source: pretext-text-measurement/SKILL.md
const prepared = prepareWithSegments('Submit', '14px Inter')
button.style.width = `${measureNaturalWidth(prepared) + 24}px`
```

## Gotchas

- Does NOT consider `\n` or `pre-wrap` — it's the unwrapped, collapsed-whitespace width.
- Returns a number in CSS px, matching Canvas measurement.

## Cross-references

- Related: TECH-02-prepare-with-segments
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
