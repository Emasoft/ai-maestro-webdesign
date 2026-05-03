---
name: TECH-type-nested
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


# TECH-type-nested

## What it does

Emits a **nested diagram** — concentric or enclosed rectangles representing
hierarchy by containment. Outer rect = broader scope; inner rects = things
contained within. Editorial HTML+SVG.

## When to use

- Hierarchy expressed as "X contains Y contains Z" (cloud → region → AZ,
  org → team → squad, monorepo → package → module).
- 2–4 nesting levels. Deeper nests become unreadable; switch to tree
  layout.
- Containment is the point — not connections between siblings.

Do not use for: parent-child with explicit edges (tree), layered abstraction
without containment (layer stack), or overlap (Venn).

## How it works

Outermost rect: full canvas minus 40px padding, 1px `ink` stroke, 10px
border-radius, `paper-2` fill at 30% opacity, title in upper-left in
`Geist Sans` 11px **uppercase letter-spacing `0.05em`** `var(--muted)`.
Each nested level: inset 16px from parent, same rounded-rect pattern,
slightly darker `paper-2` fill per level (or accent for the single focal
nest).

Labels sit in the top-left corner of each rect, NOT centred — centred
labels conflict with inner content. Use a small `text` element offset
`x+12`, `y+22` from the rect's origin.

Innermost nodes (leaves) can be regular 160×48 rounded rects or plain
text labels, depending on whether they represent components or concepts.

## Minimal example

Three-level cloud scope, accent on the innermost:

```html
<svg width="620" height="400" viewBox="0 0 620 400"
     font-family="Geist, system-ui, sans-serif">
  <rect width="620" height="400" fill="var(--paper)"/>

  <!-- Level 1: Cloud (outermost) -->
  <rect x="40" y="40" width="540" height="320" rx="10"
        fill="var(--paper-2)" fill-opacity="0.3"
        stroke="var(--ink)" stroke-width="1"/>
  <text x="52" y="62" font-size="12" font-weight="600"
        fill="var(--ink)">AWS · us-east-1</text>

  <!-- Level 2: VPC -->
  <rect x="80" y="88" width="460" height="240" rx="10"
        fill="var(--paper-2)" fill-opacity="0.6"
        stroke="var(--ink)" stroke-width="1"/>
  <text x="92" y="110" font-size="11" font-weight="600"
        fill="var(--ink)">VPC · 10.0.0.0/16</text>

  <!-- Level 3: Subnet (accent) -->
  <rect x="120" y="136" width="200" height="160" rx="10"
        fill="var(--accent)" fill-opacity="0.12"
        stroke="var(--accent)" stroke-width="1"/>
  <text x="132" y="158" font-size="11" font-weight="600"
        fill="var(--accent)">Private Subnet</text>

  <!-- Level 3: second subnet -->
  <rect x="340" y="136" width="180" height="160" rx="10"
        fill="var(--paper-2)" fill-opacity="0.8"
        stroke="var(--ink)" stroke-width="1"/>
  <text x="352" y="158" font-size="11" font-weight="600"
        fill="var(--ink)">Public Subnet</text>

  <!-- Leaf components inside focal subnet -->
  <rect x="140" y="192" width="160" height="40" rx="6"
        fill="var(--paper)" stroke="var(--ink)" stroke-width="1"/>
  <text x="220" y="216" text-anchor="middle" font-size="11"
        fill="var(--ink)">RDS (Postgres)</text>

  <rect x="140" y="244" width="160" height="40" rx="6"
        fill="var(--paper)" stroke="var(--ink)" stroke-width="1"/>
  <text x="220" y="268" text-anchor="middle" font-size="11"
        fill="var(--ink)">ElastiCache</text>
</svg>
```

## Gotchas

- **Inset by a consistent amount** (24px is the editorial default). If each
  level uses a different inset, the diagram reads as misaligned rather
  than as hierarchy.
- **Label in the corner, not centred.** Centre labels compete with inner
  content; corner labels act as "breadcrumbs".
- **Opacity ramp to encode depth.** Outer 30%, middle 60%, inner
  80–100% — or reverse if the focal is deepest. The ramp must be
  monotonic; don't zigzag.
- **Don't draw edges between siblings inside a nested diagram.** If
  siblings interact, nested isn't the right primitive — switch to
  architecture or flowchart.

## Cross-references

- [SKILL](../SKILL.md) — 13-type table
- [TECH-type-tree](TECH-type-tree.md) — if parent-child relationships have explicit edges
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-type-layers](TECH-type-layers.md) — for stacked abstraction without containment
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [design-system](design-system.md) — opacity ramp, corner-label pattern
  > Grid · Typography · Loading the fonts · Type scale · Colour discipline · Rules · Focal node vs standard node · Connection styling · Density calibration · Coordinate-level checklist
