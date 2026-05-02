---
name: TECH-classic-k8s-topology
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


# TECH-classic-k8s-topology — Ingress → Service → Pods fan-out

## What it does

Renders a Kubernetes service topology as a vertical fan-out: Ingress at top,
ClusterIP Service below, then three (or N) Pods side-by-side as leaves.
Matches the canonical "Ingress → Service → Pods" diagram found in every
K8s intro doc.

## When to use

- Cluster-topology docs in runbooks
- ADRs explaining service-to-pod routing decisions
- Comparison diagrams (old deployment vs canary deployment)

## How it works

- Ingress is a labeled box with its port (`:443/https`).
- Service row has a single labeled box (`ClusterIP`).
- Pod row has three (or N) identical-width boxes with replica numbers and
  version tags inside (`app:v2.1`).
- Vertical connectors use `|` with fan-out lines at the Service → Pods
  level.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/network-topology.md lines 6-22
                        +-- Ingress --+
                        |  :443/https |
                        +------+------+
                               |
                        +------v------+
                        |   Service   |
                        | ClusterIP   |
                        +------+------+
                               |
              +----------------+----------------+
              |                |                |
       +------v------+ +------v------+ +------v------+
       |   Pod (1)   | |   Pod (2)   | |   Pod (3)   |
       | app:v2.1    | | app:v2.1    | | app:v2.1    |
       +-------------+ +-------------+ +-------------+
```

## Gotchas

- Fan-out beyond 5 pods gets cramped in 78 cols — use ellipsis between pods
  (`Pod(1) ... Pod(N)`) or switch to `TECH-render-mode-layers.md`.
- For DaemonSets / StatefulSets / Jobs, the topology shape differs — this
  pattern is specifically for Deployment → Service → Pods.

## Cross-references

- [TECH-classic-multi-service-architecture](./TECH-classic-multi-service-architecture.md)
- [TECH-classic-namespace-nesting](./TECH-classic-namespace-nesting.md)
- [network-topology](./network-topology.md) (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

