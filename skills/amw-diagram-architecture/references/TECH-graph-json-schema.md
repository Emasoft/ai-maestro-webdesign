---
name: TECH-graph-json-schema
category: architecture-graph
source: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/formats.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/prompts.md
---

# TECH-graph-json-schema

## What it does

Defines the canonical **layered graph JSON** that all four output formats
(`graph`, `mermaid`, `svg`, `png`) are derived from. The graph is the
single source of truth — generated once per request, validated once, and
then transformed into whichever surface the caller asked for.

## When to use

- **Always**, first step of the pipeline — before any Mermaid, SVG, or
  PNG rendering.
- **When caching** — the graph JSON is cheap to re-transform into other
  formats; the LLM call is expensive, so save the graph, re-render on
  format change.

## How it works

Top-level shape:

```jsonc
{
  "title": "string (3–5 words, title-case)",
  "subtitle": "string (≤12 words, one sentence)",
  "layers": [
    { "id": "snake_case_id",
      "label": "Layer Name (displayed)",
      "color": "#hex",
      "order": 0 }
  ],
  "nodes": [
    { "id": "snake_case_id",
      "label": "Node Name (1–3 words, title-case)",
      "description": "≤8 words plain English",
      "layerId": "must match a layer id" }
  ],
  "edges": [
    { "id": "e1",
      "source": "valid node id",
      "target": "valid node id",
      "label": "" }
  ]
}
```

## Constraints

| Field | Min | Max | Preferred |
|---|---|---|---|
| `layers` | 2 | 6 | 3–5 |
| `nodes` total | 4 | 14 | 8–10 |
| `nodes` per layer | 1 | 5 | 2–4 |
| `edges` total | 0 | `floor(n × 0.8)` | essential paths only |

Layer `order` starts at 0, increments by 1, no gaps. Every node's
`layerId` resolves to a real layer. Every edge's `source` and `target`
resolve to real node IDs. IDs are snake_case and unique within their
collection.

## Minimal example

SaaS analytics platform, 4 layers × 9 nodes × 8 edges:

```json
{
  "title": "SaaS Analytics Platform",
  "subtitle": "Event-driven analytics with real-time querying",
  "layers": [
    { "id": "frontend", "label": "Frontend Layer", "color": "#6366F1", "order": 0 },
    { "id": "gateway",  "label": "Gateway Layer",  "color": "#8B5CF6", "order": 1 },
    { "id": "services", "label": "Service Layer",  "color": "#06B6D4", "order": 2 },
    { "id": "storage",  "label": "Storage Layer",  "color": "#F59E0B", "order": 3 }
  ],
  "nodes": [
    { "id": "web_app",     "label": "Web Dashboard",     "description": "Analytics UI",         "layerId": "frontend" },
    { "id": "mobile_app",  "label": "Mobile App",        "description": "iOS and Android",      "layerId": "frontend" },
    { "id": "api_gateway", "label": "API Gateway",       "description": "Routes and authenticates", "layerId": "gateway" },
    { "id": "ingest_svc",  "label": "Ingestion Service", "description": "Receives events + ETL", "layerId": "services" },
    { "id": "query_svc",   "label": "Query Service",     "description": "Data retrieval",       "layerId": "services" },
    { "id": "alerts_svc",  "label": "Alerts Service",    "description": "Threshold notifications", "layerId": "services" },
    { "id": "clickhouse",  "label": "ClickHouse",        "description": "Columnar warehouse",   "layerId": "storage" },
    { "id": "redis",       "label": "Redis Cache",       "description": "Hot query cache",      "layerId": "storage" },
    { "id": "s3",          "label": "S3 Event Store",    "description": "Raw event zone",       "layerId": "storage" }
  ],
  "edges": [
    { "id": "e1", "source": "web_app",     "target": "api_gateway", "label": "" },
    { "id": "e2", "source": "mobile_app",  "target": "api_gateway", "label": "" },
    { "id": "e3", "source": "api_gateway", "target": "ingest_svc",  "label": "" },
    { "id": "e4", "source": "api_gateway", "target": "query_svc",   "label": "" },
    { "id": "e5", "source": "ingest_svc",  "target": "s3",          "label": "" },
    { "id": "e6", "source": "ingest_svc",  "target": "clickhouse",  "label": "" },
    { "id": "e7", "source": "query_svc",   "target": "redis",       "label": "" },
    { "id": "e8", "source": "query_svc",   "target": "clickhouse",  "label": "" }
  ]
}
```

## Gotchas

- **Layer `color` is a hex string, not a CSS variable.** The schema must
  be renderer-agnostic; the Mermaid transform turns it into a classDef,
  the SVG transform uses it directly.
- **Node `description` fits on one render row (≤8 words).** Longer
  descriptions wrap ugly in the 160×64 node card.
- **Edge `label` is an empty string when unused**, not missing. The
  schema stays consistent so the transforms don't need null-guards.
- **Layer `order` is a compact sequence.** If you drop a layer during
  validation, re-compact — don't leave a gap at `order: 2`.

## Cross-references

- [formats](formats.md) — the four transforms that consume this schema
- [validation](validation.md) — Stage 1 validation rules
- [TECH-layer-palette-5-colors](TECH-layer-palette-5-colors.md) — the fixed palette for layer colors
- [TECH-edge-budget-rule](TECH-edge-budget-rule.md) — `floor(n × 0.8)` cap
- [TECH-stage1-graph-validation](TECH-stage1-graph-validation.md) — validation catalogue
- [`../SKILL.md`](../SKILL.md) — parent skill

