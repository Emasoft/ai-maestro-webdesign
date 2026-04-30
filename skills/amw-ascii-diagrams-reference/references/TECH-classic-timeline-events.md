---
name: TECH-classic-timeline-events
category: ascii-classic
source: ascii-diagrams-skill-main/references/sequences-tables.md
also-in: ascii-diagrams-skill-main/SKILL.md
---

# TECH-classic-timeline-events — scaled time axis with event labels

## What it does

Renders a linear timeline with time markers at proportional positions
(`t=0  t=100ms  t=200ms  t=500ms  t=1s`) and event labels anchored to
each marker. Used for performance traces, boot sequences, and
steady-state visualizations.

## When to use

- Boot / init time breakdowns (`boot → ready → first-request → cache-hit
  → steady`)
- Performance annotations in runbooks
- Incident timelines (at-a-glance: what happened when)

## How it works

- Top row: time markers at proportional intervals.
- Bar row: `|---------|---------|` with bars at each marker and dashes
  proportional to the actual time interval (NOT the character count).
- Bottom row: event labels centered under each marker.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/sequences-tables.md lines 19-24
  t=0     t=100ms   t=200ms   t=500ms   t=1s
  |         |         |         |         |
  boot    ready    first-req  cache-hit  steady
```

## Gotchas

- Dashes between markers should be proportional to the TIME gap, not the
  character width of the label — a `t=100ms → t=500ms` gap is 4x wider
  than `t=0 → t=100ms`.
- For very non-linear timelines (ms + seconds + minutes), use a log scale
  or break the timeline into two stacked pieces.
- Events clustered within 10ms of each other don't render cleanly on a
  1-second timeline — consider a secondary zoomed-in timeline below the
  overview.

## Cross-references

- `../../amw-text-visual-workflows/references/TECH-timeline-with-anchors.md`
- `../../amw-text-visual-retro/references/TECH-milestone-timeline.md`
- `./sequences-tables.md` (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

