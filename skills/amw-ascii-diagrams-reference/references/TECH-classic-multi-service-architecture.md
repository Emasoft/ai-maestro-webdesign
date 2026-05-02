---
name: TECH-classic-multi-service-architecture
category: ascii-classic
source: ascii-diagrams-skill-main/references/network-topology.md
also-in: ascii-diagrams-skill-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-classic-multi-service-architecture — client → gateway → services → DB

## What it does

Renders a multi-tier microservice architecture with a single client →
API gateway → three services → shared DB flow. Auth service breaks out
independently to capture the common "auth sits outside the service-mesh"
pattern.

## When to use

- Architecture overview in a README
- ADR comparing a monolith migration vs microservices
- Runbook context for "what talks to what" troubleshooting

## How it works

- Top row: single client (or 2-3 clients for multi-platform apps).
- Second row: API gateway.
- Third row: 2-3 services side by side (plus the auth service often broken
  out to the right).
- Bottom row: shared DB or data store, with fan-in from the services.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/network-topology.md lines 25-42
  +--------+     +----------+     +---------+
  | client |---->| api-gw   |---->| auth-svc|
  +--------+     +----+-----+     +---------+
                      |
                 +----+-----+
                 |          |
            +----v---+ +---v----+
            |order-  | |product-|
            |svc     | |product |
            +---+----+ +---+----+
                |          |
                +----+-----+
                     |
                +----v----+
                |   DB    |
                +---------+
```

## Gotchas

- Mixing sync (`-->`) and async (`- - >`) arrows in one diagram needs a
  legend box, or the reader can't tell which is which.
- Shared DB boxes imply a single-point-of-failure; if that's the point,
  annotate it; if not, split into per-service DBs.
- Observability components (Prometheus, Grafana) don't fit cleanly — use
  [TECH-classic-observability-stack](./TECH-classic-observability-stack.md) for that topology.

## Cross-references

- [TECH-classic-observability-stack](./TECH-classic-observability-stack.md)
- [TECH-classic-k8s-topology](./TECH-classic-k8s-topology.md)
- [network-topology](./network-topology.md) (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

