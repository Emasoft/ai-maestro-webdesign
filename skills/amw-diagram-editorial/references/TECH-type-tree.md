---
name: TECH-type-tree
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


# TECH-type-tree

## What it does

Emits a **tree diagram** — a root node at top, children arranged below,
connected by hairline edges. Editorial HTML+SVG. Classic structure for
org charts, file trees, taxonomy, decision trees with discrete branches.

## When to use

- Parent-child relationships are explicit and there is a single root.
- The tree is ≤4 levels deep and ≤12 nodes total. Beyond 4 levels,
  switch to nested or layer stack — the tree becomes unreadable.
- Edges between parent and child carry all the meaning (no sibling-
  sibling connections).

Do not use for: containment hierarchy (nested), cycles (that's a graph,
not a tree — use architecture), or lifecycle (state machine).

## How it works

Vertical layout: root centered at top (usually the accent node), children
evenly distributed on the next row, grandchildren on the row below. Edge
paths: 1px `muted` **orthogonal L-shaped polylines** — vertical from the
parent centre, horizontal pivot at the child's y-band, vertical back down
to the child — pattern `M px py V mid H cx V cy`. Never diagonals; two
children may share a horizontal span. Children spread with 32px minimum
horizontal gap.

Row vertical gap: 88px (enough for node + label + edge spacing). Nodes:
standard 140×40 rounded rect. Leaves can be smaller (100×32) if space is
tight, but stay on the 4px grid.

## Minimal example

2-level org tree, accent on the root:

```html
<svg width="640" height="280" viewBox="0 0 640 280"
     font-family="Geist, system-ui, sans-serif">
  <rect width="640" height="280" fill="var(--paper)"/>

  <!-- Root (accent) -->
  <rect x="260" y="40" width="120" height="40" rx="6"
        fill="var(--accent)"/>
  <text x="320" y="64" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--accent-fg)">CEO</text>

  <!-- Edges (T-shape) -->
  <path d="M 320 80 V 112 H 120 V 160" fill="none"
        stroke="var(--muted)" stroke-width="1"/>
  <path d="M 320 80 V 112 H 320 V 160" fill="none"
        stroke="var(--muted)" stroke-width="1"/>
  <path d="M 320 80 V 112 H 520 V 160" fill="none"
        stroke="var(--muted)" stroke-width="1"/>

  <!-- Children row -->
  <rect x="60" y="160" width="120" height="40" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="120" y="184" text-anchor="middle" font-size="12"
        fill="var(--ink)">CTO</text>

  <rect x="260" y="160" width="120" height="40" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="320" y="184" text-anchor="middle" font-size="12"
        fill="var(--ink)">CPO</text>

  <rect x="460" y="160" width="120" height="40" rx="6"
        fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="520" y="184" text-anchor="middle" font-size="12"
        fill="var(--ink)">CFO</text>
</svg>
```

## Gotchas

- **T-shaped edges, not diagonals.** A horizontal pivot line between
  parent and children reads far cleaner than individual diagonal edges —
  especially for 3+ children. Diagonals work only for 2 children.
- **Accent the root, not a leaf.** If the leaf is the point of the
  diagram, you're probably drawing something other than a tree.
- **Label depth consistent per level.** Level 1 nodes should all be
  140×40; don't make some 120 and some 160 just because labels fit.
- **No crossings.** If two edges cross, the tree is wrong — reorder
  siblings or split into two diagrams.

## Cross-references

- `../SKILL.md` — 13-type table
- [TECH-type-nested](TECH-type-nested.md) — for containment hierarchy
- [TECH-type-pyramid](TECH-type-pyramid.md) — if the hierarchy is ranked rather than strictly
  parent-child
- `../../amw-ascii-diagrams-reference/SKILL.md` — ASCII tree cousin for
  terminal documentation
