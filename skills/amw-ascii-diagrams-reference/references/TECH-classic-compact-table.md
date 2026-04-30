---
name: TECH-classic-compact-table
category: ascii-classic
source: ascii-diagrams-skill-main/references/sequences-tables.md
also-in: ascii-diagrams-skill-main/SKILL.md
---

# TECH-classic-compact-table — pipe-separated table with dash underline

## What it does

Renders a tabular data layout with pipe-separated columns and a single
dashed header-separator row. Lighter-weight than full `+---+---+`
bordered tables; optimal for code comments, API-endpoint references,
and status-code tables where visual ceremony is overhead.

## When to use

- HTTP status-code tables (200 OK, 400 Bad Request, ...)
- API endpoint references (Method + Path + Handler + Auth)
- Configuration-option tables in YAML / INI docs
- Database-column summaries in schema docs

## How it works

- Header row with columns separated by ` | `.
- Separator row of `-` with `|` at column boundaries (all columns share
  their pipe column).
- Body rows with the same ` | ` alignment.
- No outer frame — that's `+---+---+` territory.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/sequences-tables.md lines 29-46
  Method   | Path         | Handler        | Auth
  ---------|--------------|----------------|------
  GET      | /api/users   | list_users     | yes
  POST     | /api/users   | create_user    | yes
  GET      | /api/health  | health_check   | no

  Status | Meaning
  -------|--------------------
  200    | OK
  400    | Bad Request
  401    | Unauthorized
  404    | Not Found
  500    | Internal Server Error
```

## Gotchas

- Column widths must be consistent per column; pad each cell with trailing
  spaces to the column width.
- GitHub Markdown tables require the separator row and render differently
  from plain monospace — this pattern is for the plain monospace form,
  not for `| Col |` Markdown.
- For emphasis, prefer `*` / `**` inside the content rather than changing
  the table syntax.

## Cross-references

- `../../amw-ascii-creator/references/TECH-render-mode-table.md` (JSON-driven,
  supports cell-spans, multi-row headers)
- `./sequences-tables.md` (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

