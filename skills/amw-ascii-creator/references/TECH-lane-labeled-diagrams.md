---
name: TECH-lane-labeled-diagrams
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


# TECH-lane-labeled-diagrams — swimlanes via `lanes[]` in diagram mode

## What it does

`diagram` mode accepts an optional top-level `lanes: ["label1", "label2", ...]`
array that renders a left-margin track label next to each grid row — the same
pattern `layers` mode uses, but with arbitrary track names instead of the
fixed `Presentation / API / Services / Data` shape.

## When to use

- Git-branch graphs (main / feature / hotfix lanes)
- CI-pipeline swimlanes (build / test / deploy)
- Saga choreography (service-A / service-B / service-C tracks)
- Any two-to-three-track flow that would be cramped on a single horizontal
  row

## How it works

The `lanes` array length MUST match the grid's row count. Each row inherits
the `lanes[rowIndex]` label as a left-margin tag. Connectors between lanes
render as L-elbows crossing rows.

## Minimal example

```json
// Source: perfect-ascii-main/server.py docstring (lane-labeled diagrams section)
{
  "diagram": {
    "lanes": ["main", "feature"],
    "boxes": [
      {"id": "m1", "label": "v1.0"},
      {"id": "m2", "label": "v1.1"},
      {"id": "f1", "label": "auth"},
      {"id": "f2", "label": "tests"}
    ],
    "grid": [
      ["m1", null, "m2"],
      [null, "f1", "f2"]
    ],
    "connectors": [
      {"from": "m1", "to": "m2"},
      {"from": "m1", "to": "f1", "label": "branch"},
      {"from": "f1", "to": "f2"},
      {"from": "f2", "to": "m2", "label": "merge"}
    ]
  }
}
```

## Gotchas

- `lanes.length` must equal `grid.length`, or the renderer errors.
- Keep lane labels ≤ 10 chars; they eat left-margin width that other rows
  cannot reclaim.

## Cross-references

- [TECH-render-mode-diagram](./TECH-render-mode-diagram.md)
- [TECH-render-mode-layers](./TECH-render-mode-layers.md)
- [`../SKILL.md`](../SKILL.md) — parent skill

