---
name: TECH-03-layout
category: api
source: pretext-skills/amw-pretext-docs/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, SKILL-14.md, SKILL-15.md, SKILL-16.md, SKILL-17.md, SKILL-21.md, SKILL-23.md, pretext-text-measurement/SKILL.md
---

# layout() — fast height + line count

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Return value](#return-value)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** api
**Status:** stable

## What it does

`layout(prepared, maxWidth, lineHeight) -> { height, lineCount }` computes the paragraph's total height and wrapped line count at a given container width. Pure arithmetic (~0.09 ms / text), safe to call in resize handlers and `requestAnimationFrame`.

## When to use

- Virtualized lists, masonry, accordion height
- Any overflow / wrap prediction
- CSS layout prefetch (reserve space before rendering)

## How it works

Line-breaking over cached segment widths from `prepare()`. Zero DOM access.

```ts
// Source: pretext-docs/SKILL.md
import { prepare, layout } from '@chenglou/pretext'
const prepared = prepare(text, '16px Inter')
const { height, lineCount } = layout(prepared, 320, 24)
```

## Minimal example

```ts
// Source: pretext-docs/SKILL.md
function getItemHeight(prepared, containerWidth) {
  return layout(prepared, containerWidth, 24).height
}
```

## Return value

```ts
type LayoutResult = { lineCount: number; height: number }
// height === lineCount * lineHeight (always)
```

## Gotchas

- **`lineHeight` must be ABSOLUTE pixels, not a CSS multiplier.** Passing `1.5` instead of `fontSize*1.5` silently produces heights ~14x too small. This is the #1 integration bug (source: pretext-skill-main/pretext/skills/amw-pretext/SKILL.md).
- `maxWidth` in px matches container width, not full viewport.
- Re-running on resize is cheap — do NOT re-call `prepare()`.

## Cross-references

- Related: TECH-01-prepare-basics, TECH-31-dom-free-height
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
