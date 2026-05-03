---
name: TECH-eval-rubric-six-axes
category: ascii-render
source: perfect-ascii-main/bench/eval-guide.md
also-in: perfect-ascii-main/bench/scenarios.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-eval-rubric-six-axes — score an ASCII diagram on six 1-5 axes

## What it does

Defines a six-axis scoring rubric an evaluator (human or automated) applies
to a rendered ASCII diagram. Each axis scores 1-5; the subtotal is out of
30 per scenario. Used to measure progress across iterations of a renderer or
hand-authored diagram.

## When to use

- Benchmarking a renderer or a prompt-authoring strategy across scenarios
- QA pass on a diagram that passed the validator — the validator catches
  alignment bugs but not layout quality
- Side-by-side review of two competing diagrams for the same brief

## How it works

Score each axis 1 (fail) to 5 (perfect). Render the diagram as a monospace
image (PNG) and evaluate the image, not the raw text — a text buffer may
look aligned but screenshot-reveal misalignment under a specific font.

| Axis | Question | 5 = | 1 = |
|---|---|---|---|
| box_closure | Every box closed; corners meet edges | All boxes perfect | Multiple broken boxes |
| vertical_alignment | `│` in the same logical column lands on same pixel column | Perfect | Visibly jagged |
| horizontal_alignment | `─` in the same logical row stays on one line | Perfect | Visibly uneven |
| connector_routing | Arrows connect source → dest cleanly | All connect | Multiple disconnected |
| text_centering | Labels sit cleanly inside boxes | Well-centered | Clearly off |
| overall_readability | The diagram reads as what it represents | Immediately clear | Confusing |

## Minimal example

```
// Source: perfect-ascii-main/bench/eval-guide.md lines 45-53 (score recording format)
scenario_1: box=5 vert=5 horiz=4 conn=5 text=4 read=5 subtotal=28/30
scenario_2: box=5 vert=5 horiz=5 conn=5 text=5 read=5 subtotal=30/30
scenario_3: box=4 vert=3 horiz=4 conn=4 text=5 read=4 subtotal=24/30
score=82/90
```

## Gotchas

- Score based on the SCREENSHOT, not the raw text. LLMs and humans both
  misjudge width at a glance.
- Be strict. "Off by one column" is a fail on alignment axes — the whole
  value of perfect-ASCII is pixel-perfect.
- The `overall_readability` axis is subjective; use it sparingly and pair
  it with specific feedback ("I couldn't tell which arrow represents the
  error path").

## Cross-references

- [SKILL](../../amw-ascii-validator/SKILL.md)
- [TECH-78-column-cap](./TECH-78-column-cap.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

