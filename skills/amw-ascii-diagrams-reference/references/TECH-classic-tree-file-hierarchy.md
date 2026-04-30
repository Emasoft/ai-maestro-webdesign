---
name: TECH-classic-tree-file-hierarchy
category: ascii-classic
source: ascii-diagrams-skill-main/references/trees.md
also-in: ascii-diagrams-skill-main/SKILL.md
---

# TECH-classic-tree-file-hierarchy — `+--` / `|` file-tree rendering

## What it does

Renders any hierarchy — file tree, class hierarchy, org chart, DOM tree —
using the `+--` branch and `|` vertical-continuation idioms. The
last-child line drops the continuing `|` on the parent row, a subtle but
high-value cue the reader's eye uses for depth tracking.

## When to use

- File-system layouts in READMEs (`project/ → src/ → ...`)
- Class hierarchies in LLVM / Chromium / TensorFlow-style codebases
- Organization charts in ADRs
- DOM tree visualizations in bug reports

## How it works

- `+--` introduces each child.
- `|` continues the vertical line for all children except the last.
- Indent consistently — 3 or 4 spaces per level.
- The last child drops the `|` on the parent's line (so the parent's
  vertical rule doesn't extend past where it's needed).

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/trees.md lines 6-24
  project/
  |
  +-- src/
  |   +-- main.py
  |   +-- utils/
  |   |   +-- helpers.py
  |   |   +-- validators.py
  |   +-- models/
  |       +-- user.py
  |       +-- order.py
  |
  +-- tests/
  |   +-- test_main.py
  |   +-- test_utils.py
  |
  +-- README.md
  +-- pyproject.toml
```

## Gotchas

- The "last child drops the `|`" rule matters — if you keep the `|` after
  the last child, the reader sees a phantom sibling.
- Depth of 5+ levels gets hard to scan; at that point, fold subtrees
  (`...`) or split into multiple smaller trees.
- Filenames containing `+`, `-`, or `|` are rare but DO happen — box the
  affected name in backticks in the surrounding prose so the reader knows
  the character is content, not structure.

## Cross-references

- `./trees.md` (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

