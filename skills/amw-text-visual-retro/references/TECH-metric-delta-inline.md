---
name: TECH-metric-delta-inline
category: text-visual-retro
source: cc-plugin-text-visualizations-main/skills/tools-visual-retro/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-metric-delta-inline — `+12% DAU` / `-180ms p99` signed deltas

## What it does

Embeds quantitative deltas inline in retro bullets using signed percent
or absolute units: `+12% DAU`, `-180ms p99`, `+40% tickets`, `-3
incidents`. The sign communicates "better" or "worse" at a glance
without a separate color or icon.

## When to use

Every retro bullet that cites a metric. If a retro says "DAU went up"
without a number, the reader can't tell if the change is signal or
noise — and can't justify the conclusions to a VP.

## How it works

Format: `<sign><number><unit> <metric_name>`.

- `+12% DAU` — percent change, human-readable metric name
- `-180ms p99` — absolute change, percentile metric
- `+40% tickets` — percent change, operational metric
- `-3 incidents` — absolute change, count metric
- `2→8 NPS` — before→after form for non-delta comparisons

Pair with `metric:` reference lines for dashboard links:

```
+12% DAU post-launch
  metric: dau_daily (looker://dash/42)
```

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-retro/SKILL.md line 28-29 + text-visual-retro/SKILL.md lines 52-53
+12% DAU post-launch             ← positive delta
  metric: dau_daily

Support ticket backlog +40%      ← negative (wanted lower)
  metric: support_queue_size

p99 latency -180ms               ← absolute improvement
  metric: api_p99_latency
```

## Gotchas

- Sign convention: `+` means "more", not "better". `+40% tickets` is
  usually bad news. Context the reader must infer.
- Use consistent time framing — `+12% DAU week-over-week` vs `+12% DAU
  month-over-month` are very different stories.
- Unsourced deltas are suspect; always pair with a metric name or
  dashboard link.

## Cross-references

- [TECH-owner-action-items](./TECH-owner-action-items.md)
- [TECH-milestone-timeline](./TECH-milestone-timeline.md)
- `../../amw-text-visual-state/references/TECH-metrics-per-transition.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

