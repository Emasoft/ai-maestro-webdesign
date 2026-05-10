---
name: TECH-classic-before-after-comparison
category: ascii-classic
source: ascii-diagrams-skill-main/references/graphs-annotations.md
also-in: ascii-diagrams-skill-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-classic-before-after-comparison — N-scenario side-by-side ASCII

## What it does

Renders 2-3 related diagrams side-by-side with numbered/labeled headers
("0) Before / 1) After Fusion / 2) Combined") to show refactoring,
migration, or optimization deltas. Derived from TensorFlow's HLO
optimization examples.

## When to use

- Refactoring proposals (old structure vs new)
- Migration plans (current vs target)
- Optimization comparisons (original graph vs fused graph)
- A/B experiment diagrams (variant A vs variant B)

## How it works

- Each scenario is a mini-diagram, vertically aligned with its neighbors.
- Top of each column: numbered / labeled header.
- Diagrams use shared visual vocabulary (same box shape, same arrow style)
  so the reader can compare at a glance.
- Whitespace between columns keeps them visually distinct.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/graphs-annotations.md lines 55-69
  0) Before         1) After Fusion    2) Combined
     p                  p                  p
     |                  |                  |
     v                  v              +---v---+
     A                  A              | A     |
    / \                 |              | / \   |
   |   |           +----+----+        | B   C |
   v   v           | / \     |        | tuple |
   B   C           | B   C   |        +---+---+
    \ /            | tuple   |            |
    v v            +----+----+           / \
   ROOT                 |           gte_b   gte_a
                       / \
                  gte_b   gte_c
```

## Gotchas

- Columns share the 78-col budget — with 3 columns, each gets ~25 cols.
  Pick nodes with very short labels.
- Alignment between columns is visual only (no shared frame); the
  validator doesn't enforce it, so double-check by eye.
- For 4+ scenarios, stack them vertically instead; 3 is the practical
  max for side-by-side in 78 cols.

## Cross-references

- [TECH-grid-side-by-side](../../amw-text-visual-retro/references/TECH-grid-side-by-side.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [graphs-annotations](./graphs-annotations.md) (legacy pattern file)
  > Directed Graphs · Code Annotations · Before/After Comparisons · UI Sketches
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
