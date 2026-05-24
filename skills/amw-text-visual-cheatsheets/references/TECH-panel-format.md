---
name: TECH-panel-format
category: text-visual-cheatsheet
---

# TECH-panel-format — Layout, alignment, footer, glyphs

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Standard layout](#standard-layout)
- [Column alignment](#column-alignment)
- [Highlighting critical / destructive commands](#highlighting-critical--destructive-commands)
- [Categorizing into sections](#categorizing-into-sections)
- [Placeholders and context](#placeholders-and-context)
- [Glyph and width standards](#glyph-and-width-standards)
- [Extended connection types](#extended-connection-types)
- [Footer metadata](#footer-metadata)
- [Cross-references](#cross-references)

## What it does

Documents the complete authoring contract for ASCII CLI cheat-sheet panels:
table layout, column alignment rules, destructive-command markers,
section categorization, placeholder conventions, glyph & width standards,
the extended connection-arrow vocabulary, and the mandatory footer
metadata block.

## When to use

Every cheat-sheet panel this skill emits, before running the
`amw-validate-ascii.py` gate. The validator catches alignment & glyph
errors, but the rules below are what produce a panel worth shipping.

## Standard layout

Table with fixed-width columns, one action per row, one platform per column:

```
+------------------+--------------------------------+---------------------------------------+
| Action           | macOS / Linux                  | Windows (PowerShell)                  |
+------------------+--------------------------------+---------------------------------------+
| Clone            | gh repo clone org/repo ~/code  | gh repo clone org/repo $HOME\code     |
| Create PR        | gh pr create --fill            | gh pr create --fill                   |
| *Force push      | git push --force-with-lease    | git push --force-with-lease           |
| Check CI         | gh pr checks --watch           | gh pr checks --watch                  |
+------------------+--------------------------------+---------------------------------------+
```

## Column alignment

- Left-align every column.
- Column widths: longest cell plus 2 spaces of padding. Never wrap a command mid-cell.
- Headers match column widths with `-` fill in the separator row.

## Highlighting critical / destructive commands

- Prefix the action name with `*` — e.g. `*Force push`, `*Drop database`, `*Reset local branch`.
- Add a footnote line below the table per starred action:

```
* Force push: rewrites remote history. Use `--force-with-lease` to avoid
  clobbering teammates' commits. Never on `main` / `master` / `release/*`.
```

- For non-destructive but non-obvious commands, use a `(note)` suffix and expand in the footer.

## Categorizing into sections

If the command set spans multiple workflows (setup vs daily vs deploy), split into **separate small panels** with a header line per section:

```
### Setup (one-time)

+------------------+---------------------------+---------------------------+
| Install gh       | brew install gh           | winget install gh         |
| Authenticate     | gh auth login             | gh auth login             |
+------------------+---------------------------+---------------------------+

### Daily workflow

+------------------+---------------------------+---------------------------+
| Sync main        | git fetch && git pull     | git fetch; git pull       |
| Create branch    | git checkout -b feat/x    | git checkout -b feat/x    |
+------------------+---------------------------+---------------------------+
```

A single monolithic 20-row panel is nearly unreadable. Two five-row panels with clear headers is always better.

## Placeholders and context

- Explicit placeholder syntax: `<branch>`, `<env>`, `<issue-id>`. Consistent `<...>` brackets.
- Legend below the panel listing every placeholder: `<branch> = the feature branch, e.g. feat/order-refactor`.
- Note env vars inline: `GH_TOKEN=$(op read op://...) gh pr create`.

## Glyph and width standards

- **Width ceiling:** 100 columns for GitHub READMEs; 80 for terminal `--help` embedding. Drop to 80 when in doubt.
- **Box corners:** `+`, verticals `|`, horizontals `-`.
- **No tabs.** Spaces only.
- **No variable-width glyphs.** No emoji. Use `*` for "important" and `(note)` for "has a footnote".
- **Consistent quoting.** Use double quotes in shell commands when a variable expands; escape PowerShell variables as `$env:USERPROFILE` not `%USERPROFILE%` unless the target shell is CMD.

## Extended connection types

Cheat sheets are mostly tabular, but occasionally a panel needs an
inline command-flow annotation ("command A pipes to command B", "set-env
then run") or a cross-reference arrow (`see also ---▷ ...`). Use this
vocabulary when the panel needs to show relationships alongside the
command grid. Source: adapted from the diagram-skill-main ASCII-STYLES
reference (subsumed into the current skill).

| Type | Glyph | Meaning |
|---|---|---|
| sync | `-->` | Command A chains into command B (sequential). |
| emphasized | `==>` | Primary / most-used command path; single accented arrow per panel. |
| async | `~~>` | Command fires a background job (non-blocking). |
| optional | `..>` | Optional follow-up (only if previous succeeded). |
| return | `<--` | Reverse command (undo / rollback reference). |
| bidirectional | `<-->` | Two-way sync command (e.g. `git pull <--> git push`). |
| dependency | `---▷` | "See also" cross-reference to another panel / command. |
| association | `───` | Plain grouping / shared context indicator. |

Use sparingly — cheat sheets are read by scanning columns, not by
tracing arrows. When a command flow has more than 2 arrows in it,
promote to `text-visual-workflows` instead.

## Footer metadata

End every panel with:

- A last-tested date: `Last verified: 2026-04-22 on macOS 14 / Windows 11.`
- Link(s) to source docs if applicable: `See: https://cli.github.com/manual/`.
- Owner / reviewer tag if cross-team: `Owner: @platform-team.`

Stale cheat sheets are worse than no cheat sheet. The footer forces accountability.

## Cross-references

- [TECH-side-by-side-platforms](./TECH-side-by-side-platforms.md) — column layout for macOS/Linux vs Windows.
- [TECH-destructive-command-marker](./TECH-destructive-command-marker.md) — `*` prefix + footnote.
- [TECH-category-sections](./TECH-category-sections.md) — splitting by workflow stage.
- [TECH-legend-and-placeholders](./TECH-legend-and-placeholders.md) — `<branch>` convention.
- [SKILL](../SKILL.md) — parent skill.
