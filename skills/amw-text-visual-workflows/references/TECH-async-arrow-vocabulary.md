---
name: TECH-async-arrow-vocabulary
category: text-visual-workflow
source: cc-plugin-text-visualizations-main/skills/tools-visual-workflows/SKILL.md
also-in: diagram-skill-main/ASCII-STYLES.md
---

# TECH-async-arrow-vocabulary — `-->` / `==>` / `~~>` / `..>` distinctions

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Differentiates sync / emphasized / async / optional transitions in a
workflow flowchart using distinct arrow bodies, not arrowhead changes.
The arrowhead is always `>` or `v`; the body conveys the connection's
kind.

## When to use

- Workflows mixing sync and async steps (a webhook fire-and-forget vs
  the synchronous approval step)
- Primary-path emphasis (`==>` for the main flow, `-->` for fallbacks)
- Optional / conditional branches (`..>` for "fires only if guard passes")

## How it works

| Body | Meaning | Arrowhead |
|---|---|---|
| `-->` | Sync / default | `>` |
| `==>` | Emphasized / primary | `>` |
| `~~>` | Async / fire-and-forget | `>` |
| `..>` | Optional / conditional | `>` |
| `<--` | Return / callback | `<` |
| `<-->` | Bidirectional / handshake | both |

Pick one body style per *kind* of relationship; don't mix `==>` and `-->`
for sync calls within one diagram.

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-workflows/SKILL.md lines 23-25 + adapted
[ API request ] ==> [ validate ] --> { ok? }
                                      |      |
                                      yes    no
                                      |      |
                                      v      v
                      [ enqueue ] ~~> [ worker ]     [ return 400 ]
                                       ^
                                       ..> [ retry ]
```

## Gotchas

- Bodies are 2-3 chars long; they consume horizontal space. Budget
  accordingly when the diagram approaches the 78/100-col ceiling.
- `~~>` looks like prose em-dashes in some renderers — use it sparingly
  and with a legend.
- `..>` is only valid in a diagram with a legend; standalone it reads as
  a typo.

## Cross-references

- [TECH-flowchart-paren-bracket-glyphs](./TECH-flowchart-paren-bracket-glyphs.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-arrow-vocabulary](../../amw-diagram-architecture/references/TECH-arrow-vocabulary.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-arrow-head-variants](../../amw-box-diagram/references/TECH-arrow-head-variants.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

