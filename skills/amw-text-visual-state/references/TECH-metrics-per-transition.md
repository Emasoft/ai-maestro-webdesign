---
name: TECH-metrics-per-transition
category: text-visual-state
source: cc-plugin-text-visualizations-main/skills/tools-visual-state-machines/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-metrics-per-transition — link every edge to a dashboard

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Annotates each transition in a product-lifecycle state machine with the
metric that powers it and a link to the dashboard / query backing that
metric. Every edge becomes instrumentable and auditable — the reader
knows how to verify the system's behavior matches the diagram.

## When to use

- Growth funnels (signup → activation → retention → monetization)
- Retention loops with cohort tracking
- Experiment-progression diagrams where each transition is an event
  recorded in analytics
- Compliance workflows where each transition generates an audit entry

## How it works

Below (or beside) each transition arrow, add a metric reference line:

```
[NEW] --signup_complete--> [ACTIVATED]
        metric: dau_signup (looker://dash/42)

[ACTIVATED] --[sessions>=3] retain--> [RETAINED]
             metric: retention_rate_7d (grafana://dash/retention)
```

Format:

- `metric: <metric_name>` — human-readable metric name
- `(<scheme>://path)` — canonical URL to the dashboard or query that
  returns the metric

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-state-machines/SKILL.md lines 35-36 + adapted
[NEW] --signup_complete / { send_welcome }--> [ACTIVATED]
        metric: dau_signup (looker://dash/42)

[ACTIVATED] --[sessions>=3] retain--> [RETAINED]
             metric: retention_rate_7d (grafana://dash/retention)

[RETAINED] --nps>=8--> [ADVOCATE]
            metric: advocate_ratio (mixpanel://funnel/advocate)
```

## Gotchas

- Make sure the metric URLs actually exist before shipping the diagram.
- If a metric is NOT yet instrumented, tag the transition `(no metric —
  TODO instrument)` so the reader knows it's un-measured.
- Avoid mixing a "link" column with "SQL snippets" on the same
  diagram — pick one level of detail.

## Cross-references

- [TECH-state-guards-and-actions](./TECH-state-guards-and-actions.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-state-machine-legend](./TECH-state-machine-legend.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-metadata-annotation-conventions](../../amw-text-visual-workflows/references/TECH-metadata-annotation-conventions.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
