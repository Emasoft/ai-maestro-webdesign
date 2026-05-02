---
name: TECH-classic-pipeline-fanout
category: ascii-classic
source: ascii-diagrams-skill-main/references/flowcharts.md
also-in: ascii-diagrams-skill-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-classic-pipeline-fanout — request → parse → split → rejoin

## What it does

Renders a processing pipeline that forks into multiple branches and merges
back. Classic Chromium pattern: a `Parse Headers` box that splits into
`HTTP` / `HTTP2` handlers, then converges into `Route to Handler`.

## When to use

Multi-protocol dispatching (HTTP vs HTTP/2 vs HTTP/3), codec negotiation,
format-specific parsers that converge on a common downstream step.

## How it works

- One input box at the top (or left).
- Split line: `+-----+------+` with `|` going down to each branch.
- Branches render as side-by-side boxes.
- Merge line: `+-----+------+` below the branches with `v` going to the
  shared next step.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/flowcharts.md lines 27-48
  Request
    |
    v
  +-------------------+
  | Parse Headers     |
  +--------+----------+
           |
     +-----+------+
     |            |
     v            v
  +------+    +-------+
  | HTTP |    | HTTP2 |
  +--+---+    +---+---+
     |            |
     +-----+------+
           |
           v
  +--------+----------+
  | Route to Handler  |
  +-------------------+
```

## Gotchas

- Column center of the top box and bottom box must be the same — otherwise
  the `|` entering the merge row drifts visually.
- Two-way splits render cleanly; three-way splits need more horizontal
  space — switch to `TECH-render-mode-layers.md` for auto-centering.

## Cross-references

- [TECH-classic-flowchart-diamond](./TECH-classic-flowchart-diamond.md)
- `../../amw-ascii-creator/references/TECH-render-mode-layers.md`
- [flowcharts](./flowcharts.md) (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

