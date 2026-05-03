---
name: TECH-68-virtualized-list
category: workflow
source: pretext-skills/amw-pretext-integrate/SKILL.md
also-in: SKILL-13, SKILL-16, SKILL-21, use-pretext/SKILL.md Recipe 4, pretext-tables-main
---

# Virtualized list with variable-height text rows

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


**Category:** workflow
**Status:** stable

## What it does

Long list (thousands of items) where each row has different text content. Pre-measure every row's height with `prepare()` + `layout()`, build a cumulative-Y offset array, then render only rows inside the viewport plus overscan. Binary-search the offsets array for the first visible index. No reflow, no height mispredictions, no scroll jitter.

## When to use

- Log viewers / console outputs
- Admin tables / lists with text-heavy rows
- Chat histories
- Any list with 500+ variable-height text items

## How it works

```ts
// Source: use-pretext/SKILL.md — Recipe 4 condensed
function precomputeHeights(containerWidth) {
  const textWidth = containerWidth - 32
  heights = items.map(item => layout(prepare(item.text, font), textWidth, lineHeight).height + rowPadding)
  offsets = [0]
  for (let i = 1; i < heights.length; i++) offsets[i] = offsets[i - 1] + heights[i - 1]
  totalHeight = offsets.at(-1) + heights.at(-1)
}
function findStartIndex(scrollTop) {
  let lo = 0, hi = offsets.length - 1
  while (lo < hi) {
    const mid = (lo + hi) >>> 1
    if (offsets[mid] + heights[mid] < scrollTop) lo = mid + 1
    else hi = mid
  }
  return Math.max(0, lo - overscan)
}
```

## Minimal example

See use-pretext/SKILL.md Recipe 4 for full Svelte implementation.

## Gotchas

- Pretext-agent-skill-main warns: TanStack Virtual + pretext height estimation is **fragile**. For <500 items, render all + CSS transitions. For 1000+, use pretext estimates as seeds but rely on DOM correction. (Source: pretext-skill-main/SKILL.md "When NOT to Use".)
- Do NOT forget to recompute heights on width change.

## Cross-references

- Related: TECH-14-dom-free-height, TECH-56-pretext-tables-virtualized
- API reference: [TECH-03-layout](TECH-03-layout.md)
  > What it does · When to use · How it works · Minimal example · Return value · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
