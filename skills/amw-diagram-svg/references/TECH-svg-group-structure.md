---
name: TECH-svg-group-structure
category: svg-shape
source: SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md
also-in:
---

# TECH-svg-group-structure

## What it does

Organises diagrams into four **logical SVG `<g>` groups** — background,
nodes, connections, labels — in a fixed order. The order determines the
z-stack: background at the bottom, labels at the top. Any group can be
omitted when empty.

## When to use

- **Every non-trivial mechanical SVG** — more than 3-4 primitives.
- **Whenever downstream tooling** (CSS styling, animation, DOM
  selection) needs to target a specific conceptual layer.
- **When the diagram has overlapping elements** — the group order
  guarantees labels always render on top.

Do not introduce extra groups beyond the four below unless there is a
specific animation target. Over-grouping makes the SVG hard to read.

## How it works

Canonical structure:

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <g id="background">
    <!-- optional backdrop rects, patterns, gradients -->
  </g>

  <g id="connections">
    <!-- edges, arrows, leader lines — drawn BEFORE nodes -->
  </g>

  <g id="nodes">
    <!-- node shapes (rect, circle, polygon, path) -->
  </g>

  <g id="labels">
    <!-- text on top of everything -->
  </g>
</svg>
```

Omitting a group is valid:

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <g id="nodes">
    <circle cx="500" cy="500" r="80" fill="#38bdf8"/>
  </g>
  <g id="labels">
    <text x="500" y="510" text-anchor="middle" font-size="28">Hi</text>
  </g>
</svg>
```

## Why this order

1. **Background** first → sits at the bottom.
2. **Connections** second → edges pass behind nodes, which is the
   standard convention in architecture and flowchart diagrams.
3. **Nodes** third → overlap connection endpoints cleanly.
4. **Labels** last → always visible on top, regardless of what overlaps.

Reversing any pair produces visual bugs:

- Labels before nodes → text hidden behind shapes.
- Nodes before connections → arrows appear to terminate inside nodes
  rather than at their edges.

## Minimal example

Three connected nodes with labels:

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10"
            refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#0f172a"/>
    </marker>
  </defs>

  <g id="background">
    <rect width="1000" height="1000" fill="#f8fafc"/>
  </g>

  <g id="connections">
    <line x1="250" y1="500" x2="450" y2="500"
          stroke="#0f172a" stroke-width="4" marker-end="url(#arrow)"/>
    <line x1="550" y1="500" x2="750" y2="500"
          stroke="#0f172a" stroke-width="4" marker-end="url(#arrow)"/>
  </g>

  <g id="nodes">
    <rect x="150" y="460" width="100" height="80" rx="20"
          fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>
    <rect x="450" y="460" width="100" height="80" rx="20"
          fill="#38bdf8" stroke="#0f172a" stroke-width="4"/>
    <rect x="750" y="460" width="100" height="80" rx="20"
          fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>
  </g>

  <g id="labels">
    <text x="200" y="510" text-anchor="middle" font-size="22"
          fill="#0f172a">In</text>
    <text x="500" y="510" text-anchor="middle" font-size="22"
          fill="#0f172a">Mid</text>
    <text x="800" y="510" text-anchor="middle" font-size="22"
          fill="#0f172a">Out</text>
  </g>
</svg>
```

## Gotchas

- **`<defs>` goes OUTSIDE the four groups**, at the top of the SVG.
  Arrow markers, gradients, filters, clip paths all belong there.
- **Don't nest groups inside groups.** If `#nodes` needs subgroups for
  different node types, use sibling groups (`#rect-nodes`,
  `#circle-nodes`) rather than nesting.
- **Connection endpoints overshoot nodes by a few px** if the marker
  isn't accounted for. Use the marker's `refX` to pull the arrow tip
  back; don't shorten the line coordinates.
- **Labels drawn after nodes** are always on top regardless of z-order
  within `#labels`. If you need label-over-label layering, the order
  inside the group matters.

## Cross-references

- `../SKILL.md` — structure is mentioned in the Canvas section
- `TECH-canvas-1000x1000.md` — the container for this structure
- `TECH-arrow-marker-def.md` — markers that go in `<defs>`
- `TECH-node-shape-vocabulary.md` — the shapes inside `#nodes`
- `TECH-stroke-width-4-palette.md` — style defaults
