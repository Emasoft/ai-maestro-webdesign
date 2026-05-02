---
name: TECH-milestone-timeline
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


# TECH-milestone-timeline — weekly timeline + highlights + actions

## What it does

Renders a launch post-mortem or experiment readout as a weekly timeline
(`Week 1 / Week 2 / Week 3 / Week 4`) with bar markers anchoring each
week, phase labels below, a `Highlights:` bullet block, and an
`Actions:` checklist block — all in one visual artifact.

## When to use

- Launch post-mortems
- Quarter-end experiment readouts
- Multi-week retrospectives where the timeline IS the story
- Incident timelines spanning multiple days/weeks

## How it works

Three stacked sections:

1. **Timeline axis** — bar markers at week anchors with phase labels
   and owner handles.
2. **Highlights** — `Highlights:` header followed by bullet lines per
   week (`Week 2 -- migration framework shipped (PR #123)`).
3. **Actions** — `Actions:` header followed by a checklist of follow-ups
   with owners and due dates.

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-retro/SKILL.md line 23-24 + text-visual-retro/SKILL.md lines 62-73
Week 1      Week 2      Week 3      Week 4
|-----------|-----------|-----------|-----------|
Plan        Build       QA          Launch      Post
@alice      @dev-team   @qa-team    @launch     @all

Highlights:
  Week 2 -- migration framework shipped (PR #123)
  Week 3 -- 2 p0 bugs caught (one leaked to prod, see incident #42)
  Week 4 -- soft launch succeeded, +12% DAU

Actions:
  [ ] Fix incident #42 runbook (@oncall, due 04-28)
  [ ] Remove dead migration code (@db-team, due 05-05)
```

## Gotchas

- `Highlights:` lines should reference concrete artifacts (PRs,
  incidents, metrics) — vague bullets erode trust in the retro.
- `Actions:` must have owners and due dates; un-owned actions are
  aspirations, not commitments.
- The timeline axis should render with proportional spacing — uneven
  week-widths look like a bug.

## Cross-references

- [TECH-grid-side-by-side](./TECH-grid-side-by-side.md)
- [TECH-owner-action-items](./TECH-owner-action-items.md)
- `../../amw-text-visual-workflows/references/TECH-timeline-with-anchors.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

