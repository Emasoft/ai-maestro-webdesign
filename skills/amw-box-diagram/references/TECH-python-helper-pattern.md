---
name: TECH-python-helper-pattern
category: ascii-unicode
source: box-diagram-master/skills/amw-box-diagram/SKILL.md
also-in: box-diagram-master/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-python-helper-pattern — `border_top` / `border_bot` / `box_line`

## What it does

Uses small Python helpers to generate box-drawing primitives
programmatically — `border_top(w)`, `border_bot(w)`, `box_line(text, w)` —
rather than hand-counting spaces. Any diagram with 3+ boxes benefits:
hand-counting spaces produces off-by-one bugs that the validator then
catches, costing iteration rounds.

## When to use

Any diagram with 3+ parallel boxes, any diagram with multi-line content,
any diagram where the author will later want to tweak a box width and
re-render (manual editing after a width change is highly bug-prone).

## How it works

Define the primitive constants, then three functions:

- `border_top(inner_width)` → `╭──────────╮` with N `─` fill
- `border_bot(inner_width)` → `╰──────────╯`
- `box_line(text, inner_width)` → `│ text      │` padded to width

The `assert len(text) <= inner_width` in `box_line` catches one-char
overflows BEFORE the renderer produces a misaligned diagram — fail fast.

## Minimal example

```python
# Source: box-diagram-master/skills/amw-box-diagram/SKILL.md lines 86-98
H = '─'      # ─
V = '│'      # │
TL, TR = '╭', '╮'  # ╭ ╮
BL, BR = '╰', '╯'  # ╰ ╯

def box_line(text, w):
    assert len(text) <= w, f"text too wide: {text!r}"
    return V + ' ' + text + ' ' * (w - len(text)) + ' ' + V

def border_top(w):
    return TL + H * (w + 2) + TR

def border_bot(w):
    return BL + H * (w + 2) + BR

print(border_top(10))
print(box_line('hello', 10))
print(border_bot(10))
```

## Gotchas

- `inner_width` is the content width (no border, no padding). Total line
  width = `inner_width + 4` (2 borders + 2 padding spaces).
- For mixed-width rows (fan-out fan-in with narrow-then-wide boxes),
  parameterize each row separately; do NOT try to unify with one width.
- These helpers are single-byte-char-aware only; if labels contain
  non-ASCII wide characters, `len(text)` undercounts — use
  `unicodedata.east_asian_width` to correct.

## Cross-references

- [TECH-unicode-rounded-corner-set](./TECH-unicode-rounded-corner-set.md)
- [TECH-fan-out-fan-in-junctions](./TECH-fan-out-fan-in-junctions.md)
- `../../amw-ascii-validator/references/TECH-wide-character-detection.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

