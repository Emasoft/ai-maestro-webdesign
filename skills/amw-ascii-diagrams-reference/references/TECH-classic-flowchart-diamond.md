---
name: TECH-classic-flowchart-diamond
category: ascii-classic
source: ascii-diagrams-skill-main/references/flowcharts.md
also-in: ascii-diagrams-skill-main/SKILL.md
---

# TECH-classic-flowchart-diamond — branching decision with `+--+` diamond

## What it does

Renders a control-flow decision point as a centered diamond (top vertex
above, bottom below, yes/no branches left/right). Based on patterns mined
from Linux, Chromium, LLVM, TensorFlow in the CHI'24 paper.

## When to use

Code-comment flowcharts that compile-through-diff (classic ASCII survives
CVS-era blame tools and simple editors). Any decision point in a request-
processing pipeline, validation flow, or early-exit condition.

## How it works

Center the diamond's vertical axis in the containing frame. Label the two
branches (`yes|` / `no|`) just below the split so the reader maps each
outgoing edge to its predicate outcome. Continue with box / arrow nodes
from each branch.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/flowcharts.md lines 6-24
                    +----------+
                    |  Input   |
                    +----+-----+
                         |
                    +----v-----+
                    | Validate |
                    +----+-----+
                         |
                   +-----+------+
                   | Valid?     |
                   +--+------+--+
                      |      |
                   yes|      |no
                      |      |
                 +----v--+ +-v------+
                 | Store | | Reject |
                 +-------+ +--------+
```

## Gotchas

- Center the flow vertically; asymmetric trees drift visually.
- Keep decision branches left/right labeled explicitly (`yes` / `no`, not
  `T` / `F` unless the audience is familiar).
- Use `+` for every corner and junction — this is the anchor for
  `bin/amw-validate-ascii.pl`'s corner-alignment check.

## Cross-references

- `./TECH-classic-pipeline-fanout.md`
- `./TECH-classic-state-machine-arrows.md`
- `./flowcharts.md` (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

