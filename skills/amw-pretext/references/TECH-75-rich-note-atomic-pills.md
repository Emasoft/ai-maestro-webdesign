---
name: TECH-75-rich-note-atomic-pills
category: motion
source: pretext-skills/amw-pretext-frontend-motion-main/core/bundle/blueprints/rich-text.md
also-in: SKILL-15.md (rich-note.ts), pretext-text-measurement/SKILL.md Use Case 3
---

# Rich note (mixed inline fragments with atomic pills)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


**Category:** motion
**Status:** stable

## What it does

Long-form notes with inline @mentions, hashtag chips, code spans, and emoji that must stay atomic (never break mid-pill). Built on TECH-13 `prepareRichInline()` + `walkRichInlineLineRanges()`. The "Rich Text" demo family in pretext-frontend-motion proves pretext can handle complex mixed inline flow.

## When to use

- Social notes / micro-posts
- Editorial annotations
- Developer notes with code inline

## How it works

```ts
// Source: pretext-text-measurement/SKILL.md — Use Case 3
const prepared = prepareRichInline([
  { text: 'Ship ', font: '500 17px Inter' },
  { text: '@maya', font: '700 12px Inter', break: 'never', extraWidth: 22 },
  { text: "'s feature", font: '500 17px Inter' },
  { text: 'urgent', font: '600 12px Inter', break: 'never', extraWidth: 16 },
])
walkRichInlineLineRanges(prepared, 320, range => {
  const line = materializeRichInlineLineRange(prepared, range)
  line.fragments.forEach(f => {
    const item = items[f.itemIndex]
    ctx.font = item.font
    ctx.fillText(f.text, x + f.gapBefore, y)
  })
})
```

## Minimal example

See SKILL-15 `demos/rich-note.ts` + `rich-note.html` for a runnable demo.

## Gotchas

- `break: 'never'` is mandatory for chips/mentions — missing flag produces mid-pill breaks.
- `extraWidth` must include padding + border of the pill visual, not just content.

## Cross-references

- Related: TECH-13-rich-inline
- API reference: [TECH-13-rich-inline](TECH-13-rich-inline.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
