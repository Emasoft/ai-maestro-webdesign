---
name: TECH-vertical-line-continuity
category: ascii-validate
source: ascii-diagram-validator-main/validate_ascii.pl
also-in: box-diagram-master/skills/amw-box-diagram/validate.py, ascii-diagram-validator-main/README.md
---

# TECH-vertical-line-continuity — `│` / `|` align across consecutive rows

## What it does

Between any two consecutive non-border-only lines, the validator checks that
the set of vertical-pipe columns in line N intersects the set in line N+1.
If two rows have pipes but at totally disjoint columns, the validator flags
`VERTICAL_MISALIGNED` with the exact column list from each row.

## When to use

Any diagram with nested boxes or any multi-row frame. Vertical continuity
is the invariant that keeps the eye anchored as it scans down the diagram —
a one-column drift at a corner is the most common hand-authoring bug.

## How it works

For each line pair (i, i+1):

1. Skip if either line is border-only (`╭───╮` pattern — no pipes at all).
2. Compute `curr_pipes = {col for col, ch in enumerate(lines[i]) if ch in "│|┃║"}`.
3. Compute `next_pipes` the same way for line i+1.
4. If `curr_pipes and next_pipes and not (curr_pipes & next_pipes)`, flag
   the pair as misaligned.

## Minimal example

```python
# Source: box-diagram-master/skills/amw-box-diagram/validate.py lines 125-140
#   for i in range(len(lines) - 1):
#       if is_border_only(lines[i]) or is_border_only(lines[i + 1]):
#           continue
#       curr_pipes = set(find_columns(lines[i], VERT))
#       next_pipes = set(find_columns(lines[i + 1], VERT))
#       if curr_pipes and next_pipes:
#           if not curr_pipes & next_pipes:
#               issues.append(f"Lines {i+1}-{i+2}: vertical connectors misaligned...")
```

Example bad output it would catch:

```
│    A    │          ← pipes at cols [0, 10]
  │    B    │        ← pipes at cols [2, 12]   ← flagged
```

## Gotchas

- Border-only lines (pure `─` with corners, no pipes) are skipped — they are
  transitions between box top/bottom and the content below/above.
- If one row is "all pipes, matching" and the next row has ZERO pipes, the
  check is skipped (no overlap constraint applies when one side is empty).

## Cross-references

- `./TECH-width-mismatch-rule.md`
- `./TECH-box-corner-alignment.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

