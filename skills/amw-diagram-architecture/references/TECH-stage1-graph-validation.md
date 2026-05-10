---
name: TECH-stage1-graph-validation
category: architecture-graph
source: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/validation.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-stage1-graph-validation

## What it does

Runs the **Stage 1 validation** catalog against a fresh graph JSON before
any transform. Structural + visual-quality checks — layer count, node
count, balance, label quality, edge integrity, ID integrity, order
sequence. Every failing check has a deterministic fix; some failures
trigger full re-generation instead of in-place patching.

## When to use

- **Every time** the LLM returns a graph — before the format transform
  runs.
- **Every time** the graph is edited (by the user, by a downstream
  tool) — before it is re-rendered.
- **Never skip** — a bad graph produces a bad Mermaid / SVG / PNG and the
  format-level validation can't recover from a structurally broken
  source.

## How it works

Seven check categories, each with a fix strategy:

**1.1 Layer count**

| Check | Condition | Fix |
|---|---|---|
| Too few | `layers.length < 2` | Re-run generation — cannot patch |
| Too many | `layers.length > 6` | Merge the two most similar adjacent layers |
| Prefer | `< 3 or > 5` | Warn internally; acceptable |

**1.2 Node count**

| Check | Condition | Fix |
|---|---|---|
| Too few | `nodes.length < 4` | Re-run generation |
| Too many | `> 14` | Drop nodes with overlapping descriptions; remove their edges |
| Prefer | `< 6 or > 12` | Warn internally |

**1.3 Layer balance** — Empty layer → remove it. Overloaded layer (>5 nodes) → move least-essential node to an adjacent layer.

**1.4 Node label quality**

- Label too long (>4 words): truncate to 3 meaningful words, title-case
- Not title-case: convert using acronym list (API, UI, DB, URL, …)
- Description too long (>8 words): truncate to 7, preserve verb + object
- Description empty: infer 4–6 words from the label

**1.5 Edge integrity**

| Check | Fix |
|---|---|
| Dangling source/target | Remove edge |
| Self-loop | Remove edge |
| Duplicate pair | Remove duplicate, keep first |
| Reverse duplicate (A→B and B→A) | Remove the upward one |
| Edge count > `floor(n × 0.8)` | Apply pruning order: cross-layer-skip → same-layer → longest label |

**1.6 ID integrity** — Duplicate layer ID → append `_2` to second, update references. Duplicate node ID → append `_b` to second, update edges. Node `layerId` not in layers → assign by label similarity.

**1.7 Layer order sequence** — `order` must be `0, 1, 2, …` with no gaps or duplicates. Sort by current order, re-assign to index.

## Minimal example

Input graph with multiple issues:

```json
{
  "layers": [
    { "id": "frontend", "order": 0 },
    { "id": "services", "order": 2 },        // gap at order 1
    { "id": "storage",  "order": 2 }         // duplicate order
  ],
  "nodes": [
    { "id": "web",      "label": "Web",     "layerId": "frontend" },
    { "id": "api",      "label": "API",     "layerId": "services" },
    { "id": "postgres", "label": "postgres database that holds everything",  // label too long
      "layerId": "storage" },
    { "id": "orphan",   "label": "Orphan",  "layerId": "nonexistent" }   // dangling layerId
  ],
  "edges": [
    { "source": "web", "target": "api" },
    { "source": "api", "target": "web" },         // reverse duplicate (upward)
    { "source": "api", "target": "api" },         // self-loop
    { "source": "api", "target": "postgres" }
  ]
}
```

Apply fixes:

- Order: re-assign [0, 1, 2].
- Node label: truncate to "Postgres Database" → "Postgres" (1-3 words).
- Orphan's layerId: assign to `storage` by similarity.
- Edges: drop self-loop, drop upward duplicate `api → web`.

## Gotchas

- **Re-generate is a valid fix.** If `layers.length < 2` or `nodes.length
  < 4`, don't try to patch — just re-call the LLM. Patching a
  structurally-broken graph produces subtle bugs downstream.
- **Acronym preservation.** The fix for "api gateway" is "API Gateway",
  not "Api Gateway". Use the canonical list: API, UI, DB, ID, URL, HTTP,
  SDK, SPA, ETL, ML, AI, S3, CDN, DNS, JWT, SSO, TLS, gRPC, REST.
- **Edge pruning order matters.** Dropping a labelled edge just because
  it exceeds the budget is wrong — labelled edges carry the author's
  emphasis. Respect the pruning rule order.
- **Validate once, transform once.** Don't re-validate after a fix; the
  fixes are deterministic and idempotent within the validation pass.

## Cross-references

- [validation](validation.md) — full spec with both stages
  > Stage 1 — Graph Validation (all formats) · 1 Layer count · 2 Node count · 3 Layer balance · 4 Node label quality · 5 Edge integrity · 6 ID integrity · 7 Layer order sequence · Stage 2 — Format Validation · Format: `graph` · Format: `mermaid` · Format: `svg` · Format: `png` · Validation Summary (quick reference) · **Stage 1 — Graph validation**: structural checks on the graph JSON. · **Stage 2 — Format validation**: surface-level checks on the rendered output.
- [formats](formats.md) — stage 2 runs after the transform
  > Format 1: `graph` (default) · Schema · Constraints · Format 2: `mermaid` · Transform Rules · Layer Color Mapping · Mermaid Output Template · Mermaid ID Safety · Format 3: `svg` · Layout Algorithm · SVG Structure · SVG Height Calculation · Format 4: `png`
- [TECH-edge-budget-rule](TECH-edge-budget-rule.md) — the `floor(n × 0.8)` cap
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-graph-json-schema](TECH-graph-json-schema.md) — the schema being validated
  > What it does · When to use · How it works · Constraints · Minimal example · Gotchas · Cross-references
- [TECH-json-repair-recipe](TECH-json-repair-recipe.md) — upstream repair before validation runs
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
