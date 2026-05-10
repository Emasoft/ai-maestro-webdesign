---
name: TECH-71-auto-height-textarea
category: workflow
source: pretext-skills/SKILL-21.md
also-in: SKILL-23.md (AutoHeightTextarea)
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Auto-height textarea (pre-wrap, no scroll bar)

**Category:** workflow
**Status:** stable

## What it does

A textarea that grows to fit its content with no vertical scrollbar. On every `input` event, re-run `prepare(value, font, { whiteSpace: 'pre-wrap' })` + `layout()` and set `textarea.style.height = result.height + 'px'`. Used in SKILL-23 as a project-wide `AutoHeightTextarea` component replacing all default textareas.

## When to use

- Comment boxes that expand as the user types
- Chat input fields
- Any forms where the user's content length is unpredictable

## How it works

```ts
// Source: SKILL-23 AutoHeightTextarea
const FONT = '16px Inter'
const LINE_HEIGHT = 24
textarea.addEventListener('input', () => {
  const prepared = prepare(textarea.value, FONT, { whiteSpace: 'pre-wrap' })
  const { height } = layout(prepared, textarea.clientWidth, LINE_HEIGHT)
  textarea.style.height = `${height + padding}px`
})
```

## Minimal example

See How-it-works above.

## Gotchas

- Initial mount must also trigger the handler — set an initial height.
- Padding and border must be added to the final height.
- For very long inputs, consider preparing on `blur` only to reduce CPU.

## Cross-references

- Related: TECH-15-textarea-prewrap, TECH-60-svelte-islands-integration
- API reference: [TECH-03-layout](TECH-03-layout.md)
  > What it does · When to use · How it works · Minimal example · Return value · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
