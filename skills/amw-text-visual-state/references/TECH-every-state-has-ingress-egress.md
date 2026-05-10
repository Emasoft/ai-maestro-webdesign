---
name: TECH-every-state-has-ingress-egress
category: text-visual-state
source: cc-plugin-text-visualizations-main/skills/tools-visual-state-machines/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-every-state-has-ingress-egress — verification rule for correctness

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Enforces a verification rule: every state in a state-machine diagram
must have at least one incoming transition (ingress) and at least one
outgoing transition (egress), EXCEPT declared start / end states.
Unlabeled or orphan states are a modeling bug — the reader can't get
to them or can't leave them.

## When to use

As a pre-emission check on any state-machine diagram. Can be done by
eye on small diagrams (5 states or fewer) or by parsing the diagram
and building an adjacency check on larger ones.

## How it works

For each state `S` in the diagram:

1. If `S` is the declared start state, skip ingress check.
2. If `S` is a terminal/absorbing state, skip egress check.
3. Otherwise, verify at least one transition arrow points INTO `S` and
   at least one points OUT of `S`.
4. Flag any state failing the check: "State `S` has no ingress" / "has
   no egress".

## Minimal example

Bad (orphan `ORPHAN` state):

```
[NEW] --> [ACTIVATED] --> [RETAINED]

[ORPHAN]                          ← no ingress, no egress — flag it
```

Good (every state reachable and leaveable):

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-state-machines/SKILL.md lines 41 + adapted
(start) --> [NEW] --> [ACTIVATED] --> [RETAINED] --> [CHURNED] ((end))

[NEW] --abandon--> [CHURNED]          ← alt egress from NEW
```

## Gotchas

- Terminal states intentionally have no egress — flag them with
  `((STATE))` notation so the check knows to skip the egress rule.
- A start state intentionally has no ingress — flag it with `(start)` or
  `(*)` so the check skips the ingress rule.
- Loops are fine (`[ACTIVATED] --> [ACTIVATED]` self-loops count as
  egress for the source and ingress for the target, which are the same
  state).

## Cross-references

- [TECH-state-machine-legend](./TECH-state-machine-legend.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-state-guards-and-actions](./TECH-state-guards-and-actions.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
