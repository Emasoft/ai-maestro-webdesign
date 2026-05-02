---
name: TECH-type-er
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-type-er

## What it does

Emits an **entity-relationship diagram** — each entity is a two-part box
(header with entity name + list of field rows), joined by 1px lines whose
endpoint markers encode cardinality (one, many, one-or-many, zero-or-one).
Editorial HTML+SVG, no ER-specific runtime.

## When to use

- The user needs to show a data model: tables/entities, the fields they
  hold, and how they reference each other.
- Foreign keys, join tables, and cardinality matter to the reader.
- ≤6 entities. More than that — the diagram becomes unreadable; split by
  bounded context or zoom into a single aggregate.

Do not use for: logical service topology (architecture), workflow
(flowchart), or pure data-flow between components (architecture with
labelled edges is usually clearer).

## How it works

Entity = two stacked rects: header (`fill="var(--paper-2)"`, bold
`Geist Sans` entity name) + body (`fill="var(--paper)"`, `stroke="var(--ink)"`,
rows of field lines). Each field row is **16px tall** on the 4px baseline
grid. Each field row: `"fieldName"` in `Geist Sans` 11px + type sublabel
in `Geist Mono` muted 10px, right-aligned. The primary-key row gets an
inline `(PK)` annotation in mono muted; foreign keys get `(FK)`.
Default entity width: **200px** (expand in multiples of 20 if a field
name overflows).

Relationship lines: 1px `muted`. Cardinality markers at each end:

| Marker | Glyph | Meaning |
|---|---|---|
| One | Single short tick perpendicular to the line near the endpoint | "exactly one" |
| Many | Three diverging short ticks (crow's foot) | "0..many" or "1..many" |
| Optional | Small open circle just before the tick | "zero-or-..." |

Implement as additional `<line>` or `<circle>` primitives at each endpoint
— no external marker library.

## Minimal example

Two-entity ER (User 1—∞ Order), accent on the focal entity:

```html
<svg width="520" height="300" viewBox="0 0 520 300"
     font-family="Geist, system-ui, sans-serif">
  <rect width="520" height="300" fill="var(--paper)"/>

  <!-- Entity: User (accent header) -->
  <rect x="40" y="60" width="160" height="24"
        fill="var(--accent)"/>
  <text x="120" y="76" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--accent-fg)">User</text>
  <rect x="40" y="84" width="160" height="80"
        fill="var(--paper)" stroke="var(--ink)" stroke-width="1"/>
  <text x="48" y="104" font-size="11" fill="var(--ink)">id</text>
  <text x="152" y="104" font-size="10" font-family="'Geist Mono', monospace"
        fill="var(--muted)">(PK) uuid</text>
  <text x="48" y="124" font-size="11" fill="var(--ink)">email</text>
  <text x="152" y="124" font-size="10" font-family="'Geist Mono', monospace"
        fill="var(--muted)">varchar</text>
  <text x="48" y="144" font-size="11" fill="var(--ink)">created_at</text>
  <text x="152" y="144" font-size="10" font-family="'Geist Mono', monospace"
        fill="var(--muted)">timestamptz</text>

  <!-- Entity: Order -->
  <rect x="320" y="60" width="160" height="24"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="400" y="76" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">Order</text>
  <rect x="320" y="84" width="160" height="80"
        fill="var(--paper)" stroke="var(--ink)" stroke-width="1"/>
  <text x="328" y="104" font-size="11" fill="var(--ink)">id</text>
  <text x="432" y="104" font-size="10" font-family="'Geist Mono', monospace"
        fill="var(--muted)">(PK) uuid</text>
  <text x="328" y="124" font-size="11" fill="var(--ink)">user_id</text>
  <text x="432" y="124" font-size="10" font-family="'Geist Mono', monospace"
        fill="var(--muted)">(FK) uuid</text>
  <text x="328" y="144" font-size="11" fill="var(--ink)">total_cents</text>
  <text x="432" y="144" font-size="10" font-family="'Geist Mono', monospace"
        fill="var(--muted)">integer</text>

  <!-- Relationship: User 1—∞ Order -->
  <line x1="200" y1="112" x2="320" y2="112"
        stroke="var(--muted)" stroke-width="1"/>
  <!-- "one" tick on User side -->
  <line x1="208" y1="108" x2="208" y2="116"
        stroke="var(--muted)" stroke-width="1"/>
  <!-- crow's foot on Order side -->
  <line x1="312" y1="104" x2="320" y2="112"
        stroke="var(--muted)" stroke-width="1"/>
  <line x1="312" y1="112" x2="320" y2="112"
        stroke="var(--muted)" stroke-width="1"/>
  <line x1="312" y1="120" x2="320" y2="112"
        stroke="var(--muted)" stroke-width="1"/>
</svg>
```

## Gotchas

- **Field rows must line up on a 4px baseline grid.** The cumulative
  `y="104, 124, 144"` in the example is 20px row-height — a multiple of 4.
  Deviating from this is the fastest way the ER diagram reads as "AI-
  generated alignment drift".
- **Cardinality markers are small but load-bearing.** Skipping them
  turns the diagram into a schematic without semantic meaning.
- **`(PK)` and `(FK)` in mono, muted**, not in the entity header. Don't
  bold them; they're decoration, not content.
- **Do not inline field comments.** If a field needs explanation, move it
  to a [primitive-annotation](primitive-annotation.md) side callout.

## Cross-references

- `../SKILL.md` — 13-type table
- [primitive-annotation](primitive-annotation.md) — for in-margin field explanations
- [design-system](design-system.md) — row-height / font-size rules
- [TECH-type-architecture](TECH-type-architecture.md) — if the intent is component-level topology
  rather than data schema
