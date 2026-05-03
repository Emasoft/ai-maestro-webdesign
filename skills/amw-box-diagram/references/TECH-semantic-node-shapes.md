---
name: TECH-semantic-node-shapes
category: ascii-unicode
source: diagram-skill-main/ASCII-STYLES.md
also-in: box-diagram-master/skills/amw-box-diagram/SKILL.md, diagram-skill-main/REFERENCE.md
---

# TECH-semantic-node-shapes — DB / queue / external / decision glyphs

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Uses different node shapes to distinguish types of nodes in an
architecture diagram: database as rounded-corner cylinder, queue as
tilde-bordered block, external service as dashed-border block, decision
point as labeled rounded box with a question mark. These are authoring
conventions that accelerate reader comprehension — a DB doesn't look
like an in-process service.

## When to use

- Architecture diagrams with mixed component types (services + DBs +
  queues + external APIs)
- Runbooks distinguishing internal vs external dependencies
- ADRs where the component type is part of the decision ("we chose
  Redis because it's a cache, not a DB")

## How it works

| Node type | Shape | Glyph set |
|---|---|---|
| Actor / user | Simple box, often w/ stick figure label | `╭─╮ │ │ ╰─╯` |
| Component / service | Default rounded box | `╭─╮ │ │ ╰─╯` |
| Service (emphasized) | Double border | `┌═┐ ║ ║ └═┘` |
| Database | Rounded cylinder; same outer corners, top/bottom `─` | `╭─╮ │ │ ╰─╯` |
| Queue / topic / stream | Tilde ribbon top/bottom (`≋`) | `≋≋ │ │ ≋≋` |
| External service | Dashed border (`╌`, `╎`) | `┌╌┐ ╎ ╎ └╌┘` |
| Decision | Labeled rounded box w/ `?` suffix, branch w/ labeled connectors | `╭─╮ │ Valid?│ ╰─╯` |

## Minimal example

```
// Source: diagram-skill-main/ASCII-STYLES.md lines 156-166 + box-diagram-master/SKILL.md lines 98-124
Database:        Queue:          External:
╭──────╮         ≋≋≋≋≋≋≋≋        ┌╌╌╌╌╌╌╌╌┐
│ DB   │         │ Queue │        ╎ Stripe ╎
╰──────╯         ≋≋≋≋≋≋≋≋        └╌╌╌╌╌╌╌╌┘
```

## Gotchas

- `≋` (U+224B) is single-width in monospace but not all fonts include it;
  test before shipping.
- Dashed borders with `╌` and `╎` signal "outside our system"; don't
  overuse (3+ external services per diagram clutters the frame).
- Diamonds (`◇ ╱ ╲`) are notoriously hard to render cleanly in ASCII;
  prefer labeled rounded boxes with a `?` suffix for decisions.

## Cross-references

- [TECH-unicode-rounded-corner-set](./TECH-unicode-rounded-corner-set.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-arrow-vocabulary](../../amw-diagram-architecture/references/TECH-arrow-vocabulary.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../../amw-ascii-creator/SKILL.md) (style presets)
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

