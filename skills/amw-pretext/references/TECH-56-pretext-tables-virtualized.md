---
name: TECH-56-pretext-tables-virtualized
category: tables
source: pretext-skills/amw-pretext-tables-main/README.md
also-in: 
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Available hooks (source: pretext-tables SKILL.md)](#available-hooks-source-pretext-tables-skillmd)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Virtualized table with pretext-measured row heights

**Category:** tables
**Status:** stable

## What it does

React table that pre-measures every row's text content with `prepare()` + `layout()`, then virtualizes the scroll with ACCURATE per-row heights — no guess-and-correct reflows, no scroll jitter from height mispredictions. Resize a column and all row heights recalculate instantly via `layout()` calls (pure arithmetic).

## When to use

- Admin dashboards with thousands of rows
- Log viewers
- Data grids with variable-text cells

## How it works

```ts
// Source: pretext-tables-main/README.md (approach section)
const preparedRows = rows.map(r => prepare(r.text, font))  // once on data load
function rowHeight(i, columnWidth) {
  return layout(preparedRows[i], columnWidth, lineHeight).height + padding
}
// Feed rowHeight to any virtualization library (react-virtual, rvirtual, custom)
```

The pretext-tables skill ships composable React hooks — always start with `useMeasure`:

```ts
// Source: pretext-tables-main/skills/amw-pretext-tables/SKILL.md
const { rowHeights, prepared } = useMeasure(rows, columnWidths, {
  font: '14px "Inter", system-ui, sans-serif',
  lineHeight: 20,
  cellPadding: 16,  // total left + right padding
})
```

## Available hooks (source: pretext-tables SKILL.md)

| Hook | Purpose |
|---|---|
| `useMeasure` | Always required — Canvas measurement phase, memoized |
| `useVirtualization` | Virtualized scroll with accurate per-row heights |
| `useResizable` | Column/row resize, returns handle props + drag state |
| `useResizePreview` | Ghost preview during drag; runs only `layout()` |
| `useScrollAnchor` | Keeps focused row visible during column resize |
| `useShrinkWrap` | Shrink column to widest content; uses `prepared` |
| `useExpandable` | Proportional column scaling on container resize |
| `useDraggable` | Drag-to-reorder rows/columns |
| `useSortable` | Sort state + sorted rows |
| `useColumnControls` | Column visibility toggles + click-to-sort |
| `useEditable` | Inline editing; debounces `prepare()`, runs `layout()` per keystroke |
| `useStickyColumns` | Horizontal scroll with frozen left columns |
| `useInfiniteScroll` | Bottom-of-viewport detection |
| `useCanvasCell` | Custom draw functions per cell |
| `useSearch` | Full-text search with highlight rects per cell |
| `useDynamicFont` | Scales font to fit cell width |
| `useExportCanvas` | Table → Canvas → Blob export to PNG |
| `useCellNotes` | Floating notes overlay per cell |
| `useMediaCells` | Image/video auto-height from aspect ratio |

## Minimal example

See pretext-tables-main components: `BasicTable`, `VirtualizedTable`, `ResizableTable`.

## Gotchas

- Re-measure column width changes with `layout()`, NEVER `prepare()`.
- React memoize the prepared array with `useMemo([rows])`.
- Account for row padding, border, and internal icons in the final height.
- Pass `prepared` from `useMeasure` to downstream hooks — never call `prepareWithSegments` twice for the same data.

## Cross-references

- Related: TECH-14-dom-free-height, TECH-67-virtualized-list
- API reference: [TECH-03-layout](TECH-03-layout.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
