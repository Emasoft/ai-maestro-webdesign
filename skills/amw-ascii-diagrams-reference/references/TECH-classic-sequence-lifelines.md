---
name: TECH-classic-sequence-lifelines
category: ascii-classic
source: ascii-diagrams-skill-main/references/sequences-tables.md
also-in: ascii-diagrams-skill-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-classic-sequence-lifelines — Client/Server/DB actor columns

## What it does

Renders a sequence diagram using classic ASCII lifeline columns. Actor
names at top, `|` lifelines descending, `-- message -->` arrows between
columns, timing implied by vertical order.

## When to use

- README documentation of request flows (REST, RPC, SQL)
- ADR attachments showing event ordering across services
- Code-comment annotations for complex interaction flows

## How it works

- Top row: actor names, each followed by their lifeline `|`.
- Arrow rows: `|-- request -->|` or `|<-- response -----|`.
- Empty rows: `|       |       |` keep vertical spacing without events.
- Messages read top-to-bottom for chronology.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/sequences-tables.md lines 6-16
  Client          Server          Database
    |                |                |
    |-- GET /user -->|                |
    |                |-- SELECT * --> |
    |                |<-- rows -------|
    |<-- 200 OK -----|                |
    |                |                |
```

## Gotchas

- Align every `|` to the same column per actor — off-by-one drift is the
  most common bug (see
  [TECH-vertical-line-continuity](../../amw-ascii-validator/references/TECH-vertical-line-continuity.md)).
- 4+ actors rarely fit in 78 cols without abbreviating names.
- For complex flows with alt/opt/par fragments, switch to
  `TECH-render-mode-sequence.md` (JSON→ASCII renderer).

## Cross-references

- [TECH-render-mode-sequence](../../amw-ascii-creator/references/TECH-render-mode-sequence.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-timeline-events](./TECH-classic-timeline-events.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [sequences-tables](./sequences-tables.md) (legacy pattern file)
  > Sequence Diagrams · Tables
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

