---
name: TECH-protocol-label-arrows
category: text-visual-arch
source: cc-plugin-text-visualizations-main/skills/tools-visual-ascii-arch/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-protocol-label-arrows — `HTTP`, `gRPC`, `L1 tx` on edges

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Labels every edge in an architecture diagram with the protocol / call
type: `HTTP`, `gRPC`, `TCP`, `L1 tx` (blockchain), `Kafka event`, etc.
Without this label the reader can't reason about failure modes, retry
semantics, or latency budgets.

## When to use

- Any system diagram that spans multiple protocols (a gateway doing
  HTTP on one side and gRPC on the other)
- Blockchain architecture diagrams (distinguish L1 tx vs L2 bridge vs
  off-chain signal)
- Event-driven systems (distinguish sync REST call vs Kafka publish)

## How it works

Place the protocol label directly above or next to the arrow:

```
+---+   HTTP    +---+
| A | =========>| B |
+---+           +---+

+---+   gRPC    +---+
| C | --------->| D |
+---+           +---+

+---+   Kafka   +---+
| E | ~~~~~~~~~>| F |
+---+           +---+
```

Conventions:

- `HTTP` / `REST` / `gRPC` / `TCP` / `WS` for protocols
- `L1 tx` / `L2 bridge` / `IBC` for blockchain
- `Kafka topic:X` / `RabbitMQ q:Y` / `SNS topic:Z` for messaging
- Keep labels ≤ 15 chars — they eat horizontal space

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-ascii-arch/SKILL.md lines 25-27 + adapted
+--------+   HTTP    +--------+   gRPC    +--------+
|  Web   | =========>|  API   | --------->| Billing|
+--------+           +--------+           +--------+
                         |
                         | Kafka topic:events
                         ~~>
                     +--------+
                     | Worker |
                     +--------+
```

## Gotchas

- Unlabeled arrows in an architecture diagram are silent trust failures
  — the reader assumes a default (usually "sync HTTP") and gets the
  failure modes wrong when the reality is async.
- Multi-protocol edges (a service that speaks HTTP + WS + SSE to the
  same client) need separate arrows per protocol, not one arrow
  multi-labeled.

## Cross-references

- [TECH-c4-zoom-levels](./TECH-c4-zoom-levels.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-arrow-vocabulary](../../amw-diagram-architecture/references/TECH-arrow-vocabulary.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-async-arrow-vocabulary](../../amw-text-visual-workflows/references/TECH-async-arrow-vocabulary.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

