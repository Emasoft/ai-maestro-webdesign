---
name: TECH-arrow-marker-def
category: svg-arrow-marker
source: SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/formats.md
---

# TECH-arrow-marker-def

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Defines a reusable **SVG arrowhead marker** in `<defs>`, then applies it
to any line or path via `marker-end="url(#arrow)"`. The marker is a
small filled polygon — a clean triangular tip that scales with the
line stroke-width.

## When to use

- **Every directional connection** in a mechanical SVG diagram.
- **Whenever the diagram has flow semantics** — arrows encode direction;
  directional lines without arrows leave the reader guessing.

Do not use arrowheads on non-directional lines (dividers, scaffolding,
legend rules). Leave those as bare `<line>` elements.

## How it works

Define once in `<defs>`, use many times:

```xml
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10"
          refX="8" refY="3" orient="auto">
    <polygon points="0 0, 10 3, 0 6" fill="#0f172a"/>
  </marker>
</defs>

<!-- Apply to any line or path -->
<line x1="200" y1="500" x2="800" y2="500"
      stroke="#0f172a" stroke-width="4"
      marker-end="url(#arrow)"/>
```

### Attribute breakdown

| Attribute | Value | Meaning |
|---|---|---|
| `id` | `"arrow"` | DOM anchor for `url(#arrow)` |
| `markerWidth` | `10` | Width of the marker's viewport |
| `markerHeight` | `10` | Height of the marker's viewport |
| `refX` | `8` | Tip x-coordinate inside the marker (pulls arrow back from line end) |
| `refY` | `3` | Tip y-coordinate — middle of the height |
| `orient` | `"auto"` | Arrow rotates to match the line's direction |

The `<polygon points="0 0, 10 3, 0 6" />` defines a triangle: top-left,
tip (at 10,3), bottom-left — pointing right in the marker's local
coordinate system.

## Minimal example

Two directional edges with arrows:

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10"
            refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#0f172a"/>
    </marker>
  </defs>

  <g id="connections">
    <!-- Straight horizontal arrow -->
    <line x1="200" y1="500" x2="400" y2="500"
          stroke="#0f172a" stroke-width="4"
          marker-end="url(#arrow)"/>
    <!-- Curved path with arrow at end -->
    <path d="M 600 500 C 700 400, 800 400, 900 500"
          stroke="#0f172a" stroke-width="4" fill="none"
          marker-end="url(#arrow)"/>
  </g>
</svg>
```

## Gotchas

- **`orient="auto"` is non-negotiable for line arrows.** Without it the
  marker always points right regardless of the line's angle, producing
  upside-down arrows on vertical lines.
- **`refX="8"` pulls the arrow tip back** so the tip doesn't overshoot
  the line endpoint. Without refX adjustment, the arrow's tip sits AT
  the line endpoint and looks like it's floating past the node.
- **Marker fill matches stroke colour.** Mixing colours between the line
  and its arrowhead reads as a bug.
- **One `<defs>` block per SVG.** Don't duplicate the marker definition
  for every edge — define once, reference many times.
- **`markerUnits="userSpaceOnUse"`** is ALSO a valid option — it fixes
  the marker size to absolute pixels rather than scaling with stroke-
  width. The `architecture-canvas` skill uses this variant for tighter
  control; the baybee default leaves it unset so arrows scale with the
  4px stroke convention.

## Cross-references

- [SKILL](../SKILL.md) — defs and marker section
- [TECH-svg-group-structure](TECH-svg-group-structure.md) — where markers live (always in `<defs>`)
  > What it does · When to use · How it works · Why this order · Minimal example · Gotchas · Cross-references
- [TECH-stroke-width-4-palette](TECH-stroke-width-4-palette.md) — arrow colour and stroke coupling
  > What it does · When to use · How it works · Usage pattern · Minimal example · Gotchas · Cross-references
- [TECH-svg-layered-layout](../../amw-diagram-architecture/references/TECH-svg-layered-layout.md) —
  > What it does · When to use · How it works · Canvas constants · Algorithm · Height calculation · Node card structure · Layer band structure · Minimal example · Gotchas · Cross-references
  sibling arrow convention with `markerUnits="userSpaceOnUse"`
- [TECH-svg-animate-motion](TECH-svg-animate-motion.md) — animating dots along an arrow path
  > What it does · When to use · How it works · Animate a dot along a path (data-in-transit pattern) · Blink a node (alert pattern) · Pulse a ring (activation pattern) · Mandatory attributes · Minimal example · Gotchas · Cross-references
