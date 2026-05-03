---
name: TECH-grid-side-by-side
category: text-visual-retro
source: cc-plugin-text-visualizations-main/skills/tools-visual-retro/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-grid-side-by-side — `Went Well` / `Needs Attention` 2-column grid

## What it does

Renders a retrospective as a two-column grid: left column for positives
(`Went Well`, `Liked`, `Start`), right column for concerns (`Needs
Attention`, `Lacked`, `Stop`). Bullet rows inside each cell list short
highlights with owners and metric deltas.

## When to use

- End-of-sprint retros
- `start / stop / continue` templates
- `4Ls` (liked / learned / lacked / longed-for)
- `mad / sad / glad` — any 2-3 category emotional-axis retro
- `went well / needs attention` — default generic retro

## How it works

- 2 columns of equal width, outer frame `+---+---+`.
- Header row with category names.
- Body rows with bullet items per cell.
- Owners `(@name)` appended to each action-bearing item.
- Metric deltas (`+12% DAU`, `-180ms p99`) inline.

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-retro/SKILL.md lines 17-24 + text-visual-retro/SKILL.md lines 45-55
+----------------------------+-----------------------------+
| Went Well                  | Needs Attention             |
+----------------------------+-----------------------------+
| Deploy automation shipped  | Flaky tests blocked 3 PRs   |
| @alice, done               | @bob owns fix (due 04-28)   |
|                            |                             |
| +12% DAU post-launch       | Support ticket backlog +40% |
| metric: dau_daily          | @triage-team to prioritize  |
+----------------------------+-----------------------------+
```

## Gotchas

- Column widths must match; pad with trailing spaces inside each cell.
- 3-column grid (`start / stop / continue`) uses the same pattern but
  fits only if the cells are narrow (~25 cols each) — long bullets
  don't fit.
- Action items need owners; bullets without `@someone` are observations,
  not commitments.

## Cross-references

- [TECH-milestone-timeline](./TECH-milestone-timeline.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-heatmap-intensity-markers](./TECH-heatmap-intensity-markers.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-owner-action-items](./TECH-owner-action-items.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-before-after-comparison](../../amw-ascii-diagrams-reference/references/TECH-classic-before-after-comparison.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

