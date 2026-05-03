---
name: TECH-state-machine-legend
category: text-visual-state
source: cc-plugin-text-visualizations-main/skills/tools-visual-state-machines/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-state-machine-legend — `[STATE]` boxes + `-->` / `..>` arrows

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Defines a lightweight legend for ASCII state machines: states are
`[STATE]` (ALL-CAPS inside square brackets); solid transitions are
`-->`; dotted / optional transitions are `..>`; terminal states are
`((STATE))` or `((end))`. Keeps the vocabulary narrow and predictable.

## When to use

Any state-machine diagram. A legend at the top of the diagram removes
ambiguity even when the reader is unfamiliar with state-machine
notation.

## How it works

| Symbol | Meaning |
|---|---|
| `[STATE]` | Regular state |
| `(start)` or `(*)` | Start state |
| `(end)` or `((STATE))` | Terminal / absorbing state |
| `-->` | Solid (mandatory) transition |
| `..>` | Dotted (optional / conditional) transition |
| `-- trigger -->` | Arrow with label |

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-state-machines/SKILL.md lines 19-31
(start)
  |
  | signup complete
  v
[ACTIVATED] --fails SLA--> [CHURN RISK]
  | retention event
  v
[RETAINED]
```

## Gotchas

- Mixing `[STATE]` and `+---+` box syntax in the same diagram looks
  inconsistent — pick one (bracket style is lighter-weight, box style
  matches other diagram vocabularies).
- Arrow labels should name the TRIGGER, not the source/destination
  (which is obvious from the arrow direction).

## Cross-references

- [TECH-state-guards-and-actions](./TECH-state-guards-and-actions.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-metrics-per-transition](./TECH-metrics-per-transition.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-state-machine-arrows](../../amw-ascii-diagrams-reference/references/TECH-classic-state-machine-arrows.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

