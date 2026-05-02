---
name: TECH-density-4-of-10
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-density-4-of-10

## What it does

Caps editorial-diagram density at roughly **4 out of 10**. Translates to:
5 nodes is usually enough, 8 is getting too many, 12+ nodes means the
diagram is overloaded and should split into two or switch to a nested
layout.

## When to use

- **Every diagram** before emission, as a final smoke-check against
  density.
- **Whenever an input** (architecture description, PRD, feature list)
  suggests more than ~8 primary components — delegate the surplus to a
  nested or layered treatment.
- **Whenever the reader would learn more from a sentence than from a
  diagram** — the "should I even draw this?" question.

## How it works

Rough conversion:

| Node count | Density (10-scale) | Action |
|---|---|---|
| 2–4 | 2/10 | Too sparse — consider whether a sentence would do the job |
| 5–7 | 4/10 | Sweet spot |
| 8–10 | 6/10 | Pruning needed — merge siblings, drop duplicates |
| 11+ | 8/10+ | Split into overview + detail, or switch to nested/layers |

**Pruning strategy** (apply greedily in order until node count ≤8):

1. Drop any node that duplicates a sibling's description.
2. Merge minor infrastructure nodes into the service they accompany
   (e.g. "Redis cache" behind "Query Service" becomes a sublabel).
3. Collapse terminal branches into a single "error → contact support"
   leaf.
4. If still too many, split into two diagrams: the overview shows layer
   clusters, the detail shows one cluster expanded.

## Minimal example

Input (architecture with 14 components):

```
Web, Mobile, Admin Panel, CDN, API Gateway, Ingestion, Query, Alerts,
Webhook Worker, Pipeline Worker, Postgres, ClickHouse, Redis, S3
```

Apply the rules:

- Merge CDN into the frontend tier (it's infrastructure serving
  clients, not a component).
- Merge Admin Panel into Web (they share the same deployment).
- Merge Pipeline Worker into Ingestion (ETL is its job — the
  architecture-canvas example does exactly this).
- Merge Webhook Worker into Alerts (same responsibility).

Pruned list (10 components):

```
Web, Mobile, API Gateway, Ingestion, Query, Alerts, Postgres, ClickHouse,
Redis, S3
```

Still over 8. If the article is about *storage tiering*:

- Split off the storage layer as its own detail diagram with ClickHouse /
  Postgres / Redis / S3 and the data-flow between them.
- Keep the overview diagram at 6 nodes: Web, Mobile, API Gateway,
  Ingestion, Query, Alerts.

## Gotchas

- **The "would a sentence do it?" test is load-bearing.** A 2-node
  diagram ("Frontend → Backend") almost always fails it. A 5-node
  architecture diagram usually passes because the shape carries meaning
  the sentence can't.
- **Splitting is always preferable to shrinking labels.** Don't drop font
  size below 10px just to fit 14 nodes.
- **"Delete nodes until it hurts, then delete one more."** This is the
  editor's reflex — most diagrams ship with at least one node that was
  there because the author couldn't bear to cut it. Cut it.
- **Nested / layered types give the illusion of more content at a lower
  density.** 3 layers × 3 nodes per layer is 9 nodes but reads as ~5/10
  density because the containment structure does compression work.

## Cross-references

- `../SKILL.md` — non-negotiables list
- [TECH-focal-accent-discipline](TECH-focal-accent-discipline.md) — the companion rule on focal
  emphasis (they work together — focal + low density = clear diagram)
- [TECH-type-nested](TECH-type-nested.md) / [TECH-type-layers](TECH-type-layers.md) — the two escape hatches
  for when content genuinely needs hierarchy
- [troubleshooting](troubleshooting.md) — diagnose "too cluttered"
