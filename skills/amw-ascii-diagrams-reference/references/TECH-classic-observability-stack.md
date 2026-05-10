---
name: TECH-classic-observability-stack
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

# TECH-classic-observability-stack — exporters → tsdb → alertmanager → sinks

## What it does

Renders a metrics/alerting pipeline (VictoriaMetrics-style): exporters +
telegraf at the top, fanning into vmagent, feeding a time-series DB, an
alerting engine, and out to multiple notification sinks (GLPI, Telegram,
Discord).

## When to use

- Infrastructure-team runbooks for metrics pipelines
- ADRs for alerting architecture decisions
- Incident post-mortem attachments showing "which part of the stack
  failed"

## How it works

- Top row: 2-3 data sources (exporters, telegraf, collectd) feeding
  right-ward.
- Middle row: ingestion (vmagent) → storage (vmtsdb) → alert rules
  (vmalert) → alertmanager.
- Bottom row: 3+ notification sinks side-by-side, fan-out from
  alertmanager.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/network-topology.md lines 45-63
  +----------+    +----------+    +----------+
  | exporters|--->| vmagent  |--->| vmtsdb   |
  +----------+    +----+-----+    +----+-----+
  | telegraf |-------->|              |
  +----------+         |         +----v-----+
                       |         | vmalert  |
                       |         +----+-----+
                       |              |
                       |         +----v--------+
                       |         |alertmanager |
                       |         +----+--------+
                       |              |
                       |    +---------+---------+
                       |    |         |         |
                       | +--v---+ +--v----+ +--v-----+
                       | |GLPI  | |Telegr.| |Discord |
                       | +------+ +-------+ +--------+
```

## Gotchas

- Long vertical pipes (spanning 4-5 rows) are easy to misalign by one
  column — anchor the top and bottom endpoints first, then fill.
- Notification sinks fan-out beyond 5 gets cramped — group them into
  "critical" vs "informational" sub-fans.

## Cross-references

- [TECH-classic-multi-service-architecture](./TECH-classic-multi-service-architecture.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-namespace-nesting](./TECH-classic-namespace-nesting.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [network-topology](./network-topology.md) (legacy pattern file)
  > Reference
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
