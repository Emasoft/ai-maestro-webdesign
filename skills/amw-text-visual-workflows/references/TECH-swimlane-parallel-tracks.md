---
name: TECH-swimlane-parallel-tracks
category: text-visual-workflow
source: cc-plugin-text-visualizations-main/skills/tools-visual-workflows/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-swimlane-parallel-tracks — per-role lanes across one timeline

## What it does

Renders a swimlane timeline where multiple roles / teams work in parallel
across the same calendar. Each row is one lane; `==` fills the active
window for that lane on that date range. Shared columns anchor the time
axis across all lanes.

## When to use

- Project plans where Dev / QA / Launch work overlapping windows
- Capacity plans showing parallel streams of work
- Service-level ownership diagrams ("Team A owns week 1-2; Team B owns
  week 3-4")
- Incident response showing parallel mitigation + investigation +
  communication tracks

## How it works

- Header row: time markers (Day 0, Day 3, ...) aligned to column
  positions.
- One row per lane, with the lane name on the left.
- `|==...==|` shows the active window for that lane.
- Blank space shows the lane is idle during that interval.

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-workflows/SKILL.md lines 96-105
          Day 0     Day 3     Day 7     Day 14
Dev       |==build==|==test==|
QA                  |==plan==|==run====|
Launch                                 |==go=|
```

## Gotchas

- All lanes share the same column positions for time markers — drift of
  one column in one lane is visible immediately.
- Lane names eat left-margin space; keep them ≤ 10 chars.
- For 5+ lanes, consider splitting into two stacked swimlane diagrams —
  visual density gets high fast.
- `==` fill-chars signal "active"; don't change the fill-char per lane.

## Cross-references

- [TECH-timeline-with-anchors](./TECH-timeline-with-anchors.md)
- `../../amw-ascii-creator/references/TECH-lane-labeled-diagrams.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

