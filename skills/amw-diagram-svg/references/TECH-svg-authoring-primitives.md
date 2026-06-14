---
name: TECH-svg-authoring-primitives
category: svg-authoring
source: skills/amw-diagram-svg/SKILL.md
also-in:
---
## Table of Contents

- [Canvas and structure](#canvas-and-structure)
- [Node types and style](#node-types-and-style)
- [Text labels](#text-labels)
- [Connections and arrowheads](#connections-and-arrowheads)
- [Layout shapes](#layout-shapes)
- [Flowchart and architecture rules](#flowchart-and-architecture-rules)
- [Cross-references](#cross-references)

# TECH-svg-authoring-primitives

The full primitive vocabulary for authoring one self-contained SVG inside the
canvas. Produce the SVG, write it to a `.svg` file, and return only the file
path.

> **Token banner.** Every hex shown below is the mechanical slate default —
> always substitute the user's oklch tokens first when supplied.
> `design-principles` prefers oklch; hex values are kept in the examples only
> for human-readable pattern matching.

## Canvas and structure

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
```

Coordinate system `0–1000`; center `(500, 500)`; all elements stay inside.

Organize with logical groups (omit any unused):

```xml
<g id="background"></g>
<g id="nodes"></g>
<g id="connections"></g>
<g id="labels"></g>
```

## Node types and style

| Node type         | Shape                                         |
|-------------------|-----------------------------------------------|
| Process / Service | `<rect>` with rounded corners (`rx=20 ry=20`) |
| Database          | Cylinder — `<ellipse>` + `<rect>` + `<ellipse>` |
| User / Actor      | `<circle>`                                    |
| Decision          | Diamond — `<polygon>`                         |
| Input / Output    | Parallelogram — `<polygon>` (slanted rect)    |
| External system   | `<rect>` with a dashed stroke                 |

- Stroke width `4`, stroke color `#0f172a` (slate-950; oklch ≈ `oklch(20% 0.03 240)`).
- Fill: `#f1f5f9` (slate-100, `oklch(96% 0.01 240)`, light), `#334155` (slate-700, `oklch(37% 0.04 240)`, mid), or `#38bdf8` (sky-400, `oklch(74% 0.15 230)`, accent). Flat colors only.
- Rounded rectangles use `rx="20" ry="20"`.

## Text labels

```xml
<text x="500" y="500" text-anchor="middle" font-size="24" fill="#0f172a">Label</text>
```

- Center text (`text-anchor="middle"`). Font size `18`–`28`.
- Avoid long labels — split into `<tspan>` lines or shorten.

## Connections and arrowheads

Use `<line>` or `<path>`:

```xml
<line x1="200" y1="500" x2="400" y2="500" stroke="#0f172a" stroke-width="4"/>
```

Directional flow uses an arrowhead marker in `<defs>`:

```xml
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 10 3, 0 6" fill="#0f172a"/>
  </marker>
</defs>
```

Apply with `marker-end="url(#arrow)"`.

## Layout shapes

Diagrams are one of three explicit layout shapes — choose ONE before placing
nodes, never mix:

| Layout | When to use | Direction | Minimum spacing |
|---|---|---|---|
| **horizontal-flow** | Linear pipelines, before/after, left-to-right sequences | left → right | `120` units on x, free on y |
| **vertical-flow** | Tiered / layered architecture, top-to-bottom hierarchies | top → bottom | `120` units on y, free on x |
| **grid-layout** | Dense matrices, 3+ parallel branches, quadrant diagrams | both axes | `120` units on both x and y |

Minimum node spacing is `120` units on the active axis of each layout shape
(both axes for grid) — enforced inside the 0-1000 viewBox. No node overlap.
Nodes never touch the canvas edge: reserve ≥ 40 units of margin on all sides.

## Flowchart and architecture rules

**Flowchart rules.**

**Start → Process → Decision → Branch paths → End.** Decisions must use diamond shapes; branch edges must be clearly separated and labelled (`yes` / `no` or domain-specific).

**Architecture diagram rules.**

Typical nodes: API, Service, Database, Queue, Client, External system. Edges represent data flow or communication direction. For tiered/layered architectures, hand off to `../amw-diagram-architecture/`.

## Cross-references

- [SKILL](../SKILL.md) — the orchestration layer that routes here
- [TECH-canvas-1000x1000](TECH-canvas-1000x1000.md) — the 0–1000 viewBox convention
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-svg-group-structure](TECH-svg-group-structure.md) — the four logical groups
  > What it does · When to use · How it works · Why this order · Minimal example · Gotchas · Cross-references
- [TECH-node-shape-vocabulary](TECH-node-shape-vocabulary.md) — shape → node-type mapping
  > What it does · When to use · How it works · Gotchas · Cross-references
- [TECH-stroke-width-4-palette](TECH-stroke-width-4-palette.md) — stroke-4 + slate palette
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-arrow-marker-def](TECH-arrow-marker-def.md) — arrowhead marker definition
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
