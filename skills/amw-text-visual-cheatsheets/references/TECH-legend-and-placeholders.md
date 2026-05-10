---
name: TECH-legend-and-placeholders
category: text-visual-cheatsheet
source: cc-plugin-text-visualizations-main/skills/tools-visual-cheatsheets/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-legend-and-placeholders — `<branch>` convention + legend caption

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Uses angle-bracket placeholders (`<branch>`, `<repo>`, `<env>`) for
user-substitutable values in CLI commands, plus a legend caption below
the cheat-sheet that maps each placeholder to a concrete example and a
description. Eliminates the "what is `<branch>`?" moment.

## When to use

Any cheat-sheet where commands accept variable arguments the reader is
expected to substitute. Always, in practice — cheat-sheets are about
repeatable workflows, and repeatable workflows parameterize on inputs.

## How it works

- Use `<placeholder>` in the command body. Do NOT use `$placeholder`
  (shell-variable notation) unless that IS the actual shell syntax.
- Under the table, add a legend:

```
Legend:
  <branch>   feature branch name (e.g. feat/login-redesign)
  <env>      target environment (dev / staging / prod)
  <repo>     GitHub repo slug (e.g. org/repo)
```

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-cheatsheets/SKILL.md lines 39 + adapted
+------------------+--------------------------------+
| Checkout branch  | git checkout <branch>          |
| Deploy env       | ./deploy.sh --env=<env>        |
| Open PR          | gh pr create --base <branch>   |
+------------------+--------------------------------+

Legend:
  <branch>   feature branch name (e.g. feat/login-redesign)
  <env>      target environment (dev / staging / prod)
```

## Gotchas

- The legend is part of the cheat-sheet; without it, `<branch>` is
  ambiguous. Don't skip it to save lines.
- Conflict with real shell syntax: `$VAR` means "expand this variable"
  and should NOT be confused with `<placeholder>` meaning "substitute
  this". If a command uses both, annotate inline.
- Environment-specific commands (`.\deploy.ps1 -Env <env>` vs
  `./deploy.sh --env=<env>`) sometimes use different flag names — don't
  assume parity; document both.

## Cross-references

- [TECH-side-by-side-platforms](./TECH-side-by-side-platforms.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-category-sections](./TECH-category-sections.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
