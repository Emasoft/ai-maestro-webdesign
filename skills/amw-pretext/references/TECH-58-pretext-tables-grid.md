---
name: TECH-58-pretext-tables-grid
category: tables
source: pretext-skills/amw-pretext-tables-main/README.md
also-in: 
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Full table variant summary (source: pretext-tables-main README.md)](#full-table-variant-summary-source-pretext-tables-main-readmemd)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Grid table (CSS Grid layout with sticky headers)

**Category:** tables
**Status:** stable

## What it does

`GridTable` from pretext-tables uses CSS Grid for the structural layout plus pretext for measured cell heights. Sticky headers stay pinned as you scroll; variable-height text cells size correctly via pre-measurement. Demonstrates pretext works with modern CSS Grid, not just absolute positioning.

## When to use

- Modern data tables where CSS Grid is idiomatic
- Designs with complex row/col spanning
- Tables that need to integrate with surrounding page grid

## How it works

```ts
// Concept — Source: pretext-tables-main/README.md GridTable
// 1. Pre-measure each cell: layout(prepared, cellWidth, lineHeight).height
// 2. Track the MAX height per row (cells must align)
// 3. Apply the row max height via CSS Grid row sizing: grid-template-rows: <maxH>px <maxH>px ...
```

## Minimal example

See pretext-tables-main `GridTable`, `SpanningTable`, `ColumnControlsTable`, `DraggableTable`, `ExpandableTable` for full set of variants.

## Full table variant summary (source: pretext-tables-main README.md)

| Component | What it shows |
|---|---|
| `BasicTable` | Static table with pretext-measured row heights |
| `VirtualizedTable` | Virtualized scroll with accurate per-row heights |
| `ResizableTable` | Column and row resize with scroll anchor |
| `ExpandableTable` | Proportional column scaling on container resize |
| `DraggableTable` | Drag-to-reorder rows and columns |
| `ColumnControlsTable` | Column visibility toggles and click-to-sort |
| `SpanningTable` | Multi-row spanning with aligned SVG chart |
| `GridTable` | CSS Grid layout with sticky headers (this file) |

## Gotchas

- Sticky headers clash with `overflow: hidden` — use `position: sticky; top: 0`.
- Row alignment across columns requires the max-height step; single-cell measurement is insufficient.
- Multi-row spanning must use the max height across all spanning cells, not just the first cell's measurement.

## Cross-references

- Related: TECH-56-pretext-tables-virtualized
- API reference: [TECH-03-layout](TECH-03-layout.md)
  > What it does · When to use · How it works · Minimal example · Return value · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
