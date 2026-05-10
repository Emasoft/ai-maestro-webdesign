---
name: TECH-13-rich-inline
category: api
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-13.md, pretext-frontend-motion-main/SKILL.md, pretext-agents-skill-main
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# prepareRichInline() — mixed-font inline flow (chips, mentions, code spans)

**Category:** api
**Status:** stable

## What it does

`prepareRichInline(items)` (from `@chenglou/pretext/rich-inline`) takes an array of `{ text, font, break?, extraWidth? }` items and prepares them for inline flow where different fragments have different fonts. Pair with `walkRichInlineLineRanges()` and `materializeRichInlineLineRange()` to lay out mixed inline text with atomic chips/mentions.

## When to use

- Chat messages with @mentions that must never break
- Pills / chips / badges embedded in running text
- Inline code spans with different monospace font

## How it works

Each item carries its own font shorthand; a `break: 'never'` flag keeps the fragment atomic; `extraWidth` adds the padding/background box width to the layout.

```ts
// Source: pretext-text-measurement/SKILL.md
import { prepareRichInline, walkRichInlineLineRanges, materializeRichInlineLineRange } from '@chenglou/pretext/rich-inline'
const prepared = prepareRichInline([
  { text: 'Ship ', font: '500 17px Inter' },
  { text: '@maya', font: '700 12px Inter', break: 'never', extraWidth: 22 },
  { text: "'s feature", font: '500 17px Inter' },
])
walkRichInlineLineRanges(prepared, 320, range => {
  const line = materializeRichInlineLineRange(prepared, range)
  line.fragments.forEach(f => {
    ctx.font = items[f.itemIndex].font
    ctx.fillText(f.text, x + f.gapBefore, y)
  })
})
```

## Minimal example

```ts
// Source: pretext-text-measurement/SKILL.md
const { lineCount, maxLineWidth } = measureRichInlineStats(prepared, containerWidth)
```

## Gotchas

- Imported from a SUB-PATH: `@chenglou/pretext/rich-inline` (not the main module).
- Without `break: 'never'` chips wrap mid-word.
- `extraWidth` accounts for the visual padding/box of the pill — forgetting it produces overlapping chips.

## Cross-references

- Related: TECH-65-rich-note-atomic-pills
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
