---
name: TECH-render-mode-diagram
category: ascii-render
source: perfect-ascii-main/server.py
also-in: perfect-ascii-main/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-render-mode-diagram — grid-based flowchart/block-diagram renderer

## What it does

Given a flat list of boxes plus a 2D `grid` of box IDs (with `null` for empty
cells) plus a list of `connectors`, the renderer emits a perfectly aligned
ASCII block diagram. Used for flowcharts, ER diagrams, state machines, or any
rectangular node-and-edge graph laid out on a grid.

## When to use

When the structure is "boxes in a grid with arrows between them". Each grid
row is a horizontal layer; columns are vertical stacks. Different-row,
different-column connectors route as L-shaped elbows; same-column as
vertical; same-row as horizontal.

## How it works

- `grid`: 2D array of box IDs or `null` for blank cells. Each row is a band.
- `connectors`: `{from, to, label?}`. Routing is auto (vertical / horizontal /
  L-elbow) based on the relative positions in the grid.
- `body` (optional): list of strings inside a box for multi-line boxes (ER
  attribute lists, state-machine entry/exit actions).
- `lanes` (optional): list of row labels for swimlane-style left-margin
  labeling (git graph tracks, CI pipeline stages).

## Minimal example

```json
// Source: perfect-ascii-main/server.py render_ascii docstring
{
  "diagram": {
    "title": "Login Flow",
    "boxes": [
      {"id": "start", "label": "Start"},
      {"id": "creds", "label": "Enter Credentials"},
      {"id": "valid", "label": "Valid?"},
      {"id": "ok", "label": "Grant Access"},
      {"id": "fail", "label": "Lock Account"}
    ],
    "grid": [
      ["start"],
      ["creds"],
      ["valid"],
      ["ok", null, "fail"]
    ],
    "connectors": [
      {"from": "start", "to": "creds"},
      {"from": "creds", "to": "valid"},
      {"from": "valid", "to": "ok", "label": "yes"},
      {"from": "valid", "to": "fail", "label": "no"}
    ]
  }
}
```

## Gotchas

- Connectors that skip intermediate rows auto-route around boxes, but dense
  graphs can still overflow 78 columns — shorten labels or split into two
  diagrams.
- Grid cells holding `null` reserve horizontal space; useful for visual
  balance but each `null` consumes one column's worth of width.

## Cross-references

- [TECH-json-render-four-modes](./TECH-json-render-four-modes.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-lane-labeled-diagrams](./TECH-lane-labeled-diagrams.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-multi-line-box-body](./TECH-multi-line-box-body.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
