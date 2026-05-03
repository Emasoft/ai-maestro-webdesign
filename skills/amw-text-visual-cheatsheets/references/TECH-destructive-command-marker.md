---
name: TECH-destructive-command-marker
category: text-visual-cheatsheet
source: cc-plugin-text-visualizations-main/skills/tools-visual-cheatsheets/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-destructive-command-marker — `*` prefix + footnote caveat

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Marks destructive or non-obvious commands in a CLI cheat-sheet with a
leading `*` on the action name, and adds a footnote below the table
explaining the risk and the safety guardrail.

## When to use

- Any cheat-sheet listing `git push --force`, `rm -rf`, `DROP TABLE`,
  or similar irreversible operations
- Deploy scripts with commands that skip CI or bypass approvals
- Rollback commands that overwrite recent state

## How it works

- Prefix the action column value with `*` (e.g. `*Force push`, `*Drop DB`).
- Keep the table row itself unchanged otherwise.
- Below the table, add footnotes:

```
* Force push: rewrites remote history. Use `--force-with-lease` to avoid
  clobbering teammates' commits. Never on `main` / `master` / `release/*`.

* Drop DB: irreversible. Confirm backups exist in the last 24h before
  running. Requires DBA approval in #db-ops.
```

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-cheatsheets/SKILL.md lines 30-32, 58-60 + adapted
+------------------+------------------------------------+--------------------------------------+
| Action           | macOS / Linux                      | Windows                              |
+------------------+------------------------------------+--------------------------------------+
| Clone            | gh repo clone org/repo ~/code      | gh repo clone org/repo $HOME\code    |
| *Force push      | git push --force-with-lease        | git push --force-with-lease          |
| *Drop branch     | git branch -D feature/foo          | git branch -D feature/foo            |
+------------------+------------------------------------+--------------------------------------+

* Force push: rewrites remote history. Use `--force-with-lease` to avoid
  clobbering teammates' commits. Never on `main` / `master` / `release/*`.
* Drop branch: permanent local deletion; verify the branch is merged
  upstream before running.
```

## Gotchas

- The `*` is a visual cue; the footnote explains the danger. Don't
  assume the reader will infer the risk from the star alone.
- Don't mix `*` (destructive) with `(note)` (clarification) — keep one
  convention per cheat-sheet or the reader learns nothing.

## Cross-references

- [TECH-side-by-side-platforms](./TECH-side-by-side-platforms.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-category-sections](./TECH-category-sections.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

