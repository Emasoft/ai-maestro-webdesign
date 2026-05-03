---
name: TECH-owner-action-items
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


# TECH-owner-action-items — `[ ] <action> (@owner, due YYYY-MM-DD)`

## What it does

Standardizes action-item formatting across every retro artifact:
unchecked checkbox + short imperative action + owner handle + due date.
Every bullet is individually trackable and assignable.

## When to use

Any retro, post-mortem, or readout with follow-up commitments. Applies
whether the template is a grid, a timeline, or a heatmap — action items
belong at the bottom of every retro artifact.

## How it works

Format:

```
[ ] <imperative verb + object> (@<owner>, due YYYY-MM-DD)
```

- `[ ]` — unchecked box (will become `[x]` when done).
- `<imperative verb + object>` — "Fix flaky test in auth spec", not
  "Flaky tests".
- `(@<owner>, due YYYY-MM-DD)` — owner handle + ISO date.

When an action is done, update `[ ]` → `[x]` in place.

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-retro/SKILL.md line 41 + text-visual-retro/SKILL.md lines 70-73
Actions:
  [ ] Fix incident #42 runbook (@oncall, due 04-28)
  [ ] Remove dead migration code (@db-team, due 05-05)
  [x] Publish post-mortem doc (@alice, due 04-25)        ← already done
  [ ] Schedule 30-min debrief with SRE team (@manager, due 05-01)
```

## Gotchas

- Actions without owners become team-wide aspirations that never happen.
  If you don't know the owner, ASK — don't guess.
- Due dates in relative form (`next week`, `soon`) are useless — always
  ISO 8601 `YYYY-MM-DD`.
- Actions should be individually completable. If an action is "Improve
  test suite", split it — that's not actionable in one session.

## Cross-references

- [TECH-milestone-timeline](./TECH-milestone-timeline.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-grid-side-by-side](./TECH-grid-side-by-side.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-metadata-annotation-conventions](../../amw-text-visual-workflows/references/TECH-metadata-annotation-conventions.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

