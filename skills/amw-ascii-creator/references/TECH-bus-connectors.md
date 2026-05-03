---
name: TECH-bus-connectors
category: ascii-render
source: perfect-ascii-main/server.py
also-in: box-diagram-master/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-bus-connectors — auto fan-out / fan-in between tiers

## What it does

In `layers` mode, setting `connections: "between_layers"` enables automatic
"bus" connectors between adjacent layers: every box in tier N is connected
to every box in tier N+1, drawn as a shared horizontal bus with vertical
drops. The author never writes the individual edges.

## When to use

Whenever every component in one tier communicates with every component in
the next tier — i.e. classic 3-tier or 4-tier stacks (Presentation /
Services / Data). For selective wiring (only some boxes in N talk to some
in N+1), fall back to `diagram` mode with explicit `connectors`.

## How it works

The renderer calculates the horizontal midpoint between rows, draws a
horizontal bus `──────`, and drops vertical `│` branches from each upper-row
box to the bus and from the bus to each lower-row box. Arrowheads appear at
the entry to each lower-row box.

## Minimal example

```
// Source: perfect-ascii-main/server.py docstring (layers mode example)
+---------+  +--------+  +-----+
| Web App |  | Mobile |  | CLI |
+----+----+  +---+----+  +--+--+
     |           |          |
     +-----------+----------+
                 |
           +-----+-------+
           | API Gateway |
           +------+------+
                  |
        +---------+---------+
        |         |         |
        v         v         v
     +------+ +------+ +------+
     | Auth | | Ord. | | Inv. |
     +---+--+ +---+--+ +---+--+
         ...
```

## Gotchas

- If tier N has more boxes than tier N+1 or vice versa, the bus absorbs the
  width difference by widening/narrowing; layer labels stay on the left
  margin.
- For "not every box in N talks to every box in N+1", this is the wrong
  technique — use `diagram` mode with hand-authored connectors.

## Cross-references

- [TECH-render-mode-layers](./TECH-render-mode-layers.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../../amw-box-diagram/SKILL.md) (manual fan-out/fan-in with `┌┬┐`/`└┴┘`)
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

