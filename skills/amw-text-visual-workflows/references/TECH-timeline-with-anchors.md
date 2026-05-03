---
name: TECH-timeline-with-anchors
category: text-visual-workflow
source: cc-plugin-text-visualizations-main/skills/tools-visual-workflows/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-timeline-with-anchors — Day/Week markers + labels below

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Renders a linear timeline as a row of anchor markers (`|`) along a
dashed horizontal axis, with time labels above and event/owner labels
below. Used for launch schedules, migration phases, onboarding weeks —
any flow whose calendar position matters more than its branching
structure.

## When to use

- Launch schedules ("Day 0: Plan / Day 3: Build / Day 7: QA / Day 14:
  Launch")
- Onboarding checklists across weeks
- Migration phase plans
- Sprint-level roadmaps

## How it works

- Top row: time markers (`Day 0`, `Day 3`, `Day 7`, `Day 14`, ...).
- Middle row: `|---------|---------|---------|` with bars at each anchor.
- Third row: event / phase labels (`Plan`, `Build`, `QA`, `Launch`).
- Fourth row (optional): owner handles (`@alice`, `@bob`, `@cara`).

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-workflows/SKILL.md lines 38-42
Day 0  Day 3  Day 7
|-----|-----|-----|
Dev   QA    Launch
```

With owners:

```
Day 0     Day 3     Day 7     Day 14
|---------|---------|---------|
Plan      Build     QA        Launch
@alice    @bob      @cara     @dana
```

## Gotchas

- Dashes between markers should be proportional to the TIME gap, not the
  label widths — otherwise the visual pacing is misleading.
- Label text between markers may overflow into the next cell if it's
  longer than the gap — shorten labels or widen the gap.
- Time-unit changes (days → weeks → months) on a single timeline read
  confusingly; break into stacked sub-timelines.

## Cross-references

- [TECH-swimlane-parallel-tracks](./TECH-swimlane-parallel-tracks.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-milestone-timeline](../../amw-text-visual-retro/references/TECH-milestone-timeline.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-timeline-events](../../amw-ascii-diagrams-reference/references/TECH-classic-timeline-events.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

