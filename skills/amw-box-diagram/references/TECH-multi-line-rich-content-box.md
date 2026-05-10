---
name: TECH-multi-line-rich-content-box
category: ascii-unicode
source: box-diagram-master/README.md
also-in: box-diagram-master/skills/amw-box-diagram/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-multi-line-rich-content-box — title + separator + body lines

## What it does

Renders a "rich" box containing a title line, a full-width separator
rule (`─` spanning the inner width), and 2-5 body lines. Used for
incident-response steps, runbook stages, and any flow where each node
needs more than a single-label.

## When to use

- Incident-response runbooks (severity + source + on-call channel per
  step)
- Multi-step pipelines where each step has metadata (owner, SLA, gating
  condition)
- Architecture diagrams where each service box needs its tech stack
  (`Python / Postgres / Celery`)

## How it works

Line 1: `│ <title>` padded to inner_width
Line 2: `│ ` + `─` * inner_width + ` │`  (separator rule)
Lines 3+: `│ <body[n]>` padded to inner_width
Last line: `╰──────────╯`

## Minimal example

```
// Source: box-diagram-master/README.md lines 29-36
╭──────────────────────────────────────────╮
│ 1. ALERT TRIGGERED                       │
│ ──────────────────────────────────────── │
│ PagerDuty → #incident-channel            │
│ Severity: P1 (user-facing)               │
│ Source: Grafana alert rule                │
╰──────────────────────────────────────────╯
```

## Gotchas

- Width of every body line MUST match the frame — the validator enforces
  this via `TECH-width-mismatch-rule.md`.
- Blank body lines are allowed and render as `│` + spaces + `│` — useful
  for visual spacing between related groups of lines.
- Title line + body > 7 total lines gets harder to scan at a glance;
  split into two boxes with an arrow between them.

## Cross-references

- [TECH-unicode-rounded-corner-set](./TECH-unicode-rounded-corner-set.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-multi-line-box-body](../../amw-ascii-creator/references/TECH-multi-line-box-body.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- `../../amw-box-diagram/examples/incident-response.txt`
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
