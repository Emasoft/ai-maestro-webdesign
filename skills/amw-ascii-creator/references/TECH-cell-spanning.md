---
name: TECH-cell-spanning
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


# TECH-cell-spanning — `{text, span: N}` for multi-column cells

## What it does

In `table` mode, a cell value can be an object `{"text": "...", "span": N}`
rather than a plain string, which spans the cell across `N` columns.
Classic use case: packet-header layouts where one field covers 4 bytes.

## When to use

- IP/TCP/UDP packet header diagrams (version + IHL + TTL + fields that span
  2 or 4 bytes)
- Struct layouts with union fields spanning multiple columns
- Sales matrices where a subtotal row spans multiple quarters
- Merged header rows that label a group of columns

## How it works

In `rows`, replace a plain string cell with `{"text": "value", "span": N}`.
The cell occupies positions `[i, i+1, ..., i+N-1]` in the row. The following
plain-string cells in that same row are shifted right by `N-1` positions —
i.e. a row with one `span: 2` cell contains one fewer entry than a plain row.

## Minimal example

```json
// Source: perfect-ascii-main/server.py docstring (packet header example)
{
  "table": {
    "align": ["center", "center", "center", "center"],
    "rows": [
      ["Version", "IHL", "Type of Svc", "Total Length"],
      [{"text": "Identification", "span": 2}, "Flags", "Frag Offset"],
      ["TTL", "Protocol", {"text": "Header Checksum", "span": 2}],
      [{"text": "Source IP Address",       "span": 4}],
      [{"text": "Destination IP Address",  "span": 4}]
    ],
    "separator_after": [0, 1, 2, 3]
  }
}
```

## Gotchas

- A row with `span: N` cells has `(total_cols - (N-1) * span_count)` entries —
  easy to off-by-one; the renderer errors with a column-count mismatch if the
  row arithmetic doesn't add up.
- `span` only applies horizontally; there is no vertical row-span.

## Cross-references

- [TECH-render-mode-table](./TECH-render-mode-table.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

