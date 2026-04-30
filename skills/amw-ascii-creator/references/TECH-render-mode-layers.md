---
name: TECH-render-mode-layers
category: ascii-render
source: perfect-ascii-main/server.py
also-in: perfect-ascii-main/README.md
---

# TECH-render-mode-layers — layered architecture with bus connectors

## What it does

Shortcut for classic 3- to 5-tier architecture diagrams. Each level is a
centered row of boxes with a layer label on the left margin. Connectors
between tiers are auto-generated using bus patterns (fan-out from each box
above to every box below, fan-in in the reverse direction), so the author
never writes the edges by hand.

## When to use

Any "Presentation / API / Services / Data" stack. When every component in
tier N talks to every component in tier N+1, or when the individual edges
are not the point and only the tiering matters.

## How it works

Top-level `layers` key holds `{title?, levels, connections}`:

- `levels`: ordered list of `{label, boxes: [string, ...]}`. The `label` goes
  on the left margin; `boxes` are centered within their row.
- `connections: "between_layers"` enables the bus-connector mode — auto
  fan-out / fan-in between adjacent levels without explicit edges.

## Minimal example

```json
// Source: perfect-ascii-main/server.py docstring
{
  "layers": {
    "title": "System Architecture",
    "levels": [
      {"label": "Presentation", "boxes": ["Web App", "Mobile", "CLI"]},
      {"label": "API",          "boxes": ["API Gateway"]},
      {"label": "Services",     "boxes": ["Auth", "Orders", "Inventory"]},
      {"label": "Data",         "boxes": ["PostgreSQL", "Redis", "S3"]}
    ],
    "connections": "between_layers"
  }
}
```

Rendered output: four centered rows, left-margin labels `Presentation / API /
Services / Data`, bus connectors automatically drawn between each adjacent
pair of rows.

## Gotchas

- Use `layers` mode only when every component in tier N fans out to every
  component in tier N+1. For selective wiring, use `diagram` mode with
  explicit `connectors`.
- Tier labels share a left margin column; keep labels short (≤ 14 chars)
  to stay within the 78-col cap.

## Cross-references

- `./TECH-json-render-four-modes.md`
- `./TECH-bus-connectors.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

