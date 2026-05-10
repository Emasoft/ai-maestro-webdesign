---
name: TECH-render-mode-table
category: ascii-render
source: perfect-ascii-main/server.py
also-in: perfect-ascii-main/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-render-mode-table — data grids with cell-span and wrap

## What it does

Renders tabular data with multi-row headers, per-column alignment, separator
lines, footer rows, and cell spanning. Auto-wraps wide tables at 78 columns by
repeating the first column for continuation.

## When to use

- Quarterly/regional comparison matrices
- API endpoint catalogs (Method / Path / Handler / Auth)
- Struct/packet layouts with spanning fields
- Config option tables, capability grids

## How it works

- `headers`: array of header rows (supports multi-row headers for groupings
  like `Q1 / Rev / Growth`). Blank cells use `""`.
- `align`: per-column alignment — `"left"` / `"right"` / `"center"`.
- `rows`: body rows. A cell can be `"text"` or `{"text": "...", "span": N}` to
  span N columns (packet-header idiom).
- `separator_after`: row indices after which to draw a rule. `-1` means
  "after the headers".
- `footer`: optional summary row.

## Minimal example

```json
// Source: perfect-ascii-main/server.py docstring
{
  "table": {
    "headers": [
      ["Region", "Q1 2025", "", "Q2 2025", "", "Annual"],
      ["", "Rev", "Growth", "Rev", "Growth", "Total"]
    ],
    "align": ["left", "right", "right", "right", "right", "right"],
    "rows": [
      ["North", "$1.2M", "+12%", "$1.4M", "+15%", "$2.6M"],
      ["South", "$890K", "+5%",  "$920K", "+3%",  "$1.8M"]
    ],
    "separator_after": [-1],
    "footer": ["Total", "$2.1M", "", "$2.3M", "", "$4.4M"]
  }
}
```

## Gotchas

- Cell spans are specified on individual cells; a `span: 2` cell replaces
  what would otherwise be two plain string cells in that row's array.
- Wide tables auto-split at 78 chars; the first column is repeated on every
  chunk so each slice is readable in isolation.

## Cross-references

- [TECH-cell-spanning](./TECH-cell-spanning.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-json-render-four-modes](./TECH-json-render-four-modes.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
