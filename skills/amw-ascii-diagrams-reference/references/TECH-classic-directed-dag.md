---
name: TECH-classic-directed-dag
category: ascii-classic
source: ascii-diagrams-skill-main/references/graphs-annotations.md
also-in: ascii-diagrams-skill-main/SKILL.md
---

# TECH-classic-directed-dag — build-dependency graph with backward edges

## What it does

Renders a directed acyclic graph (DAG) — build dependencies, compilation
pipelines, task graphs — using boxes and directional arrows. Supports
leftward arrows for "depends on" relationships.

## When to use

- Build-system dependency graphs (Bazel, Nx, Turbopack)
- Compilation pipelines (parser → AST → codegen → optimizer)
- Task DAGs in data pipelines (Airflow-style flows when you want ASCII
  instead of Mermaid)

## How it works

- Boxes laid out on a rough grid matching topological order.
- Forward edges (`-->`) for execution / data flow.
- Backward edges (`<--`) for dependency / "uses" relations.
- Cross-edges OK; minimize crossings by reordering on the grid.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/graphs-annotations.md lines 7-16
  +-----+     +------+     +--------+
  | lib |<----| app  |---->| config |
  +--+--+     +--+---+     +--------+
     |           |
     v           v
  +--+--+     +--+----+
  |utils|     | tests |
  +-----+     +-------+
```

## Gotchas

- More than 6-8 nodes becomes unreadable in ASCII; switch to Mermaid /
  Graphviz at that threshold.
- Graph layout is NP-hard; accept sub-optimal for ASCII. If the result
  has too many crossings, reorder nodes by hand — no algorithm is worth
  the complexity in a README.
- Self-loops (`A -> A`) render as a small arc above the box; they often
  need custom hand-drawing.

## Cross-references

- `../../amw-diagram-architecture/SKILL.md` (JSON → Mermaid / SVG path)
- `./graphs-annotations.md` (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

