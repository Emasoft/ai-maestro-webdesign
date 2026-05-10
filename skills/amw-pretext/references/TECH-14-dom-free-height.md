---
name: TECH-14-dom-free-height
category: measure
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, SKILL-16.md, SKILL-23.md, use-pretext/SKILL.md, pretext-docs/SKILL.md
---

# DOM-free paragraph height (the core pretext win)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** measure
**Status:** stable

## What it does

Measure a paragraph's total height at a given container width without touching the DOM — no `getBoundingClientRect`, no `offsetHeight`, no hidden probe div, no layout reflow. `prepare()` runs once; `layout()` runs on every resize in constant time. Benchmarked ~300-600x faster than DOM measurement (source: SKILL-16 / pretext-main-2 README).

## When to use

- Virtual lists (10k+ row heights without reflow)
- Reserving exact container height BEFORE content arrives (prevents CLS)
- Responsive layouts where surrounding elements depend on text height
- Any resize-driven height recompute that previously triggered reflow

## How it works

1. Canvas `measureText` measures segment widths once (~19 ms / 500 texts).
2. Pure-arithmetic line breaker computes `{ height, lineCount }` per maxWidth (~0.09 ms).

```ts
// Source: pretext-text-measurement/SKILL.md
const prepared = prepare('AGI 春天到了. بدأت الرحلة 🚀', '16px Inter')
const { height, lineCount } = layout(prepared, containerWidth, 20)
```

## Minimal example

```ts
// Source: use-pretext/SKILL.md — Recipe 6 layout-shift prevention
async function loadAndRender(width) {
  const text = await fetchText()
  const prepared = prepare(text, '16px Inter')
  const { height } = layout(prepared, width, 24)
  container.style.height = `${height}px`  // reserve before inserting
  container.textContent = text
}
```

## Gotchas

- Font must be loaded: `await document.fonts.ready` first for custom fonts.
- `font` and `lineHeight` must match CSS precisely; drift produces wrong heights.
- Does not account for `::first-letter`, `::first-line` styles, or counters.

## Cross-references

- Related: TECH-03-layout, TECH-66-masonry-grid, TECH-67-virtualized-list
- API reference: [TECH-03-layout](TECH-03-layout.md)
  > What it does · When to use · How it works · Minimal example · Return value · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
