---
name: TECH-category-sections
category: text-visual-cheatsheet
source: cc-plugin-text-visualizations-main/skills/tools-visual-cheatsheets/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-category-sections — split by workflow stage with section headers

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Splits a large CLI cheat-sheet into small per-category panels, each
preceded by a `### Category name` header. Categories map to workflow
stages (`Setup`, `Daily Workflow`, `Review`, `Deploy`, `Rollback`). Makes
the reader's eye jump to the right table without scanning one giant
30-row block.

## When to use

- Any cheat-sheet covering ≥ 3 workflow stages
- Onboarding docs where a new contributor reads sequentially
- Deploy docs where the deploy → rollback split is life-or-death

## How it works

Each category is a `### Heading` Markdown line followed by its own
small panel:

```
### Setup (one-time)

+------------------+---------------------------+---------------------------+
| Install gh       | brew install gh           | winget install gh         |
| Authenticate     | gh auth login             | gh auth login             |
+------------------+---------------------------+---------------------------+

### Daily Workflow

+------------------+---------------------------+---------------------------+
| Sync main        | git pull --rebase         | git pull --rebase         |
| Create branch    | git checkout -b feat/x    | git checkout -b feat/x    |
+------------------+---------------------------+---------------------------+

### Deploy

+------------------+---------------------------+---------------------------+
| *Deploy prod     | ./deploy.sh --env=prod    | .\deploy.ps1 -Env prod    |
+------------------+---------------------------+---------------------------+
```

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-cheatsheets/SKILL.md lines 73-80
### Setup (one-time)

+------------------+---------------------------+---------------------------+
| Install gh       | brew install gh           | winget install gh         |
| Authenticate     | gh auth login             | gh auth login             |
+------------------+---------------------------+---------------------------+
```

## Gotchas

- Keep categories to ≤ 5 commands each; larger categories need their
  own sub-category splits.
- The category name should map to a user's goal ("Deploy") not a
  command set ("kubectl commands").
- Don't over-split — a cheat-sheet with 10 one-row panels is worse
  than one 10-row panel.

## Cross-references

- [TECH-side-by-side-platforms](./TECH-side-by-side-platforms.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-destructive-command-marker](./TECH-destructive-command-marker.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
