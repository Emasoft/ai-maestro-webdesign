---
name: TECH-group-aware-width-detection
category: ascii-validate
source: box-diagram-master/skills/amw-box-diagram/validate.py
also-in: box-diagram-master/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-group-aware-width-detection — per-structure width, not global mode

## What it does

Instead of picking one "expected width" for the entire file (the classic
Perl validator's mode), this technique groups consecutive lines that share
box-char column positions into one structural group, and only flags
intra-group width deviations. A diagram with three independent stacked
structures (a header, a fan-out, a fan-in — each at a different natural
width) passes, whereas the global-mode check would flag every line outside
the most-common width.

## When to use

Multi-structure diagrams: a page with a header band + a flowchart + a
separate legend table. Also any fan-out/fan-in that naturally produces
three widths (parent box, connector row, child boxes). All three are
"valid" but live at different widths; the global-mode check can't tell.

## How it works

```python
# Source: box-diagram-master/skills/amw-box-diagram/validate.py lines 86-113
# Group consecutive lines that share box-char column positions.
# Lines with box chars at different columns are separate structures
# (e.g., box content at [0,15,19,34] vs branch connector at [8,27,46]).
box_lines = []
current_group = []
for i, line in enumerate(lines):
    cols = box_char_cols(line)
    if len(cols) >= 2:
        if current_group:
            prev_cols = box_char_cols(lines[current_group[-1]])
            if cols & prev_cols:         # shared columns → same structure
                current_group.append(i)
            else:                        # different columns → new group
                box_lines.append(current_group)
                current_group = [i]
        else:
            current_group = [i]
    else:
        if current_group:
            box_lines.append(current_group)
            current_group = []
if current_group:
    box_lines.append(current_group)

for group in box_lines:
    group_widths = set(widths[i] for i in group)
    if len(group_widths) > 1:
        issues.append(f"Inconsistent widths in box (lines {group[0]+1}-{group[-1]+1}): ...")
```

## Minimal example

Passes group-aware detection, FAILS global-mode detection:

```
╭─────╮
│ Hdr │                     ← 7 chars — group 1
╰─────╯

    │                       ← blank + 1 pipe — separator, not in any group
    ▾

╭──────────────╮            ← 16 chars — group 2 (different column positions)
│ Body of diag │
╰──────────────╯
```

## Gotchas

- Blank lines end a group; don't sandwich structures across blanks.
- A group needs ≥ 2 lines with ≥ 2 box chars. Single-line structures (a
  standalone `───▶`) are not grouped and skip the width check entirely.

## Cross-references

- [TECH-width-mismatch-rule](./TECH-width-mismatch-rule.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../../amw-box-diagram/SKILL.md)
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
