---
name: TECH-fan-out-fan-in-junctions
category: ascii-unicode
source: box-diagram-master/skills/amw-box-diagram/SKILL.md
also-in: box-diagram-master/README.md
---

# TECH-fan-out-fan-in-junctions — `┌┬┐` / `└┴┘` to diverge and rejoin

## What it does

Renders a 1-to-N fan-out and N-to-1 fan-in using the T-junction set
(`┬ ┴ ├ ┤ ┼`). Produces clean wye-shapes where a single source splits to
multiple parallel sinks, then those sinks converge back to a single
downstream node (the canonical "build → 3 parallel tests → release"
shape).

## When to use

- CI pipelines with parallel test suites
- Message fan-out to multiple subscribers
- Service fan-in from multiple writers to a shared DB
- Any flow where one node hands off to N downstream nodes then
  reconverges

## How it works

Fan-out (1 source → 3 sinks):

- `┌` at the leftmost sink column.
- `┬` at each inner sink column.
- `┐` at the rightmost sink column.
- `─` between them.
- `│` vertical drop to each sink's top border.

Fan-in (3 sources → 1 sink):

- Mirror of fan-out: `└` / `┴` / `┘` with `─` between, `│` going up to
  each source.

## Minimal example

```
// Source: box-diagram-master/skills/amw-box-diagram/SKILL.md lines 111-127
         │                     (source)
┌────────┼────────┐            fan-out
│        │        │
▾        ▾        ▾

│        │        │
└────────┼────────┘            fan-in
         │                     (destination)
         ▾
```

Full fan-out + fan-in (source: box-diagram-master/README.md lines 16-26):

```
              ┌──────────────────┬──────────────────┐
              │                  │                  │
              ▾                  ▾                  ▾
╭──────────────────╮  ╭──────────────────╮  ╭──────────────────╮
│ Unit Tests       │  │ API Tests        │  │ E2E Tests        │
╰──────────────────╯  ╰──────────────────╯  ╰──────────────────╯
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                                 ▾
```

## Gotchas

- The `┌` / `┬` / `┐` columns MUST align with the center column of each
  child box below. Off-by-one is the most common bug.
- For asymmetric splits (2-of-3 into one, 1-of-3 into another), classic
  wye-shape breaks down — draw each arm as a separate arrow.
- The source-column (where `┼` sits at the top) must align with the
  CENTER of the source-box above — not its left edge.

## Cross-references

- `./TECH-unicode-rounded-corner-set.md`
- `./TECH-python-helper-pattern.md`
- `../../amw-box-diagram/examples/ci-cd-pipeline.txt`
- [`../SKILL.md`](../SKILL.md) — parent skill

