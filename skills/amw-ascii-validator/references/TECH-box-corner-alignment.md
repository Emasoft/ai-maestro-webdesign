---
name: TECH-box-corner-alignment
category: ascii-validate
source: ascii-diagram-validator-main/validate_ascii.pl
also-in: box-diagram-master/skills/amw-box-diagram/validate.py, ascii-diagram-validator-main/README.md
---

# TECH-box-corner-alignment — nested boxes share corner columns

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

The validator checks that between any two corner characters on the same line
(`+ ╭ ╮ ╰ ╯ ┌ ┐ └ ┘`), the characters between are only valid horizontal
fill (`- = ─ ━ ═` or T-junctions `┬ ┴ ├ ┤ ┼` or spaces). A broken border —
e.g. a stray letter between two corners — raises a `BROKEN_BORDER` finding.

## When to use

Any nested frame, especially dashboards with multiple content regions inside
a single outer frame, or editorial layouts with columns and sub-columns.

## How it works

For each line, list the column positions of corner chars. For each pair
`(start, end)`, extract `line[start+1:end]` and verify every char is in the
allowed-fill set (HORIZ + JUNCTIONS + `' '`). Any disallowed char produces
a `FIX:` instruction naming the exact column.

## Minimal example

```python
# Source: box-diagram-master/skills/amw-box-diagram/validate.py lines 142-156
#   corner_positions = [j for j, ch in enumerate(line) if ch in CORNERS]
#   if len(corner_positions) >= 2:
#       for k in range(0, len(corner_positions) - 1, 2):
#           start = corner_positions[k]
#           end = corner_positions[k + 1]
#           between = line[start + 1 : end]
#           allowed_fill = HORIZ | JUNCTIONS | {' '}
#           if between and not all(ch in allowed_fill for ch in between):
#               issues.append(f"Line {i+1}: broken box border ...")
```

Example bug this catches:

```
╭──X──╮   ← flagged: 'X' is not valid fill between corners
```

## Gotchas

- Corner pairs are matched in order (0,1), (2,3), etc. — if a line has an
  odd number of corners, the last one is un-paired and not checked.
- T-junctions (`┬ ┴ ├ ┤ ┼`) are allowed between corners — they're how
  three-way or four-way intersections show up inside a wider frame.

## Cross-references

- [TECH-width-mismatch-rule](./TECH-width-mismatch-rule.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-vertical-line-continuity](./TECH-vertical-line-continuity.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

