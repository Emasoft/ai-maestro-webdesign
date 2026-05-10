---
name: TECH-metadata-annotation-conventions
category: text-visual-workflow
source: cc-plugin-text-visualizations-main/skills/tools-visual-workflows/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-metadata-annotation-conventions — owners, SLAs, tools inline

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Standardizes metadata annotation inside flowchart / timeline nodes so the
reader can parse owner / SLA / tool at a glance. Keeps the annotation in
parentheses after the node, not on a following prose line.

## When to use

- Any workflow diagram where ownership + timing matters
- Team-shared flowcharts where "who does what by when" is the whole
  point
- On-call runbooks with per-step SLAs

## How it works

| Annotation | Form | Placement |
|---|---|---|
| Owner | `@alice` / `@qa-team` | Inside or right after the node |
| Tool / command | `gh pr checks` / `kubectl rollout` | Appended in parens |
| SLA | `<15min` / `<24h` / `<3 days` | Appended in parens |
| Environment tag | `[prod]` / `[staging]` | Prefix the tool/command |

Combine them: `[ Run migrations ] (@db-team, <15min, prod-only)`.

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-workflows/SKILL.md lines 44, 115 + adapted
[ Open PR ]
  |
  v
{ CI passes? }
  |            |
  yes          no
  |            |
  v            v
[ Request review ]    [ Fix and push ]
  (@reviewers, <24h)    (@author, <15min)
```

## Gotchas

- Parenthetical metadata belongs on the same line as the node or on the
  line directly below. Putting it in a separate paragraph breaks the
  eye-tracking from node to annotation.
- `@someone` without a verified mapping to a real handle is fabrication —
  ask the user for owners before filling in.
- SLA notation: prefer unambiguous forms (`<24h` not `fast`). The reader
  doesn't know what "fast" means in this team's culture.

## Cross-references

- [TECH-flowchart-paren-bracket-glyphs](./TECH-flowchart-paren-bracket-glyphs.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-owner-action-items](../../amw-text-visual-retro/references/TECH-owner-action-items.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
