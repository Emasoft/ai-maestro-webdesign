---
name: TECH-edge-budget-rule
category: architecture-graph
source: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/prompts.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/validation.md
---

# TECH-edge-budget-rule

## What it does

Caps the number of edges in an architecture graph at **`floor(n × 0.8)`**
where `n` is the node count. The rule prevents the single most common
failure mode of generated architecture diagrams — drawing *every*
connection, which produces a visual mess.

## When to use

- **LLM generation prompt** — bake the rule into the system prompt so
  the LLM aims low from the start.
- **Stage 1 graph validation** — after the LLM returns, verify and
  enforce the cap by dropping surplus edges.
- **Pruning strategy** — surplus edges are dropped in a specific order
  (see below) to preserve the most informative ones.

## How it works

Formula: `max_edges = floor(node_count × 0.8)`.

| Nodes | Max edges |
|---|---|
| 4 | 3 |
| 6 | 4 |
| 8 | 6 |
| 10 | 8 |
| 12 | 9 |
| 14 | 11 |

If the LLM returns more edges than this cap, the validation step applies
the pruning strategy in order:

1. **Drop cross-layer-skip edges first.** An edge from layer 0 to layer 3
   that bypasses layers 1 and 2 implies an architectural shortcut that
   is rarely the main point. Prefer the top-down cascade.
2. **Drop same-layer edges next.** Two peer services in the same layer
   usually interact through the layer above them — the peer-to-peer
   edge is decoration.
3. **Drop the edge with the longest label.** Labels tend to fall off
   edges whose content is contrived; the LLM padded the graph.
4. **Never touch a labelled edge before an unlabelled one.** A labelled
   edge carries the author's emphasis; unlabelled edges are structural.

## Minimal example

10-node graph, LLM returns 12 edges, cap is 8. Pruning sequence:

```json
// Original edges
[
  { "source": "web_app",     "target": "api_gateway" },      // kept — top of cascade
  { "source": "mobile_app",  "target": "api_gateway" },      // kept
  { "source": "api_gateway", "target": "ingest_svc" },       // kept
  { "source": "api_gateway", "target": "query_svc" },        // kept
  { "source": "ingest_svc",  "target": "s3" },               // kept
  { "source": "ingest_svc",  "target": "clickhouse" },       // kept
  { "source": "query_svc",   "target": "redis" },            // kept
  { "source": "query_svc",   "target": "clickhouse" },       // kept (hit the cap)
  { "source": "web_app",     "target": "s3",          "label": "direct upload backup (rarely)" },
  // ^ DROPPED (rule 1) — cross-layer-skip and longest label
  { "source": "ingest_svc",  "target": "query_svc" }, // DROPPED (rule 2) — same-layer
  { "source": "alerts_svc",  "target": "clickhouse" }, // DROPPED (rule 1) — but also legit, see note
  { "source": "query_svc",   "target": "alerts_svc" }  // DROPPED (rule 2) — same-layer
]
```

Note: the alerts → clickhouse edge is semantically correct but was
dropped because there were higher-priority edges already. This is the
tradeoff — visual clarity over exhaustive completeness.

## Gotchas

- **The cap is a visual-clarity rule, not a correctness rule.** Some
  edges will be dropped that are *technically* correct; this is
  intentional. Exhaustive architecture diagrams become unreadable at
  scale.
- **`floor`, not `ceil`.** A 5-node graph gets 4 edges (`5 × 0.8 = 4.0`),
  not 5.
- **Labelled edges survive priority.** When pruning, preserve the
  labelled ones even if they are structurally less important — the
  label carries the author's intention.
- **If the cap forces dropping the one edge that makes the diagram
  make sense**, the diagram has too many nodes. Go back to node
  reduction before trimming edges further.

## Cross-references

- `prompts.md` — rule is in the LLM system prompt
- `validation.md` — Stage 1 edge-integrity section
- `TECH-graph-json-schema.md` — schema constraint table includes this
- `TECH-stage1-graph-validation.md` — how the rule is enforced
- `../../amw-diagram-editorial/references/TECH-density-4-of-10.md` — the
  editorial analogue (node density cap)
- [`../SKILL.md`](../SKILL.md) — parent skill

