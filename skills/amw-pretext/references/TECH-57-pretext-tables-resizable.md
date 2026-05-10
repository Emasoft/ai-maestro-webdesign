---
name: TECH-57-pretext-tables-resizable
category: tables
source: pretext-skills/amw-pretext-tables-main/README.md
also-in: 
---

# Resizable table (column + row resize with scroll anchor)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** tables
**Status:** stable

## What it does

The `ResizableTable` variant from pretext-tables lets users drag column borders to resize, and re-runs `layout()` on all affected rows during the drag — smooth because `layout()` is ~0.09 ms. Adds scroll-anchor logic so the focused row stays visible through the resize.

## When to use

- Spreadsheet-like UIs
- Tables where columns need user control
- Any resizable data grid

## How it works

```ts
// Concept — Source: pretext-tables-main/README.md ResizableTable
// On drag of column divider:
// 1. Update column width state
// 2. For each visible row: heights[i] = layout(preparedRows[i], newColWidth, lh).height
// 3. Scroll anchor: maintain the Y of the currently focused row
```

## Minimal example

See pretext-tables-main `ResizableTable` component.

## Gotchas

- Drag emits many events per second — throttle if performance drops below 60 fps (unlikely with pretext).
- Anchor row tracking must happen BEFORE the height update, not after.
- Pass `prepared` from `useMeasure` to `useResizePreview` — it runs only `layout()` during drag, so the Canvas phase never repeats.
- Use `useResizable` for handle props; `useResizePreview` for the ghost column preview; `useScrollAnchor` for stable viewport scroll during resize — these are three separate hooks that compose.

## Cross-references

- Related: TECH-56-pretext-tables-virtualized, TECH-66-resize-observer-pattern
- API reference: [TECH-03-layout](TECH-03-layout.md)
  > What it does · When to use · How it works · Minimal example · Return value · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
