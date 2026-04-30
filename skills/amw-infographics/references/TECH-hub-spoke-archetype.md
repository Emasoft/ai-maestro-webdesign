---
name: TECH-hub-spoke-archetype
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/layout-patterns.md
---

# Archetype 3: Hub & Spoke

## What it does

Central entity (logo, token, platform) with radiating connections
to surrounding nodes. The hub owns 30-40% of canvas; spokes radiate
to category nodes around it.

## When to use

- Ecosystem maps where one platform sits at the center
- Integration networks — central app with N integrations
- Game economy hubs — token at center, various use cases around

Example reference: `nft_ecosystem_overview.png`.

## The shape

```
┌────────────────────────────────────────┐
│  HEADER                                │
├────────────────────────────────────────┤
│                                        │
│    [Node]    [Node]    [Node]          │
│       ↘        ↓        ↙             │
│    [Node] ←─[HUB]─→ [Node]           │
│       ↗        ↑        ↖             │
│    [Node]    [Node]    [Node]          │
│                                        │
├────────────────────────────────────────┤
│  CATEGORY DETAIL PANELS (2-3 col)      │
├────────────────────────────────────────┤
│  FOOTER                                │
└────────────────────────────────────────┘
```

## CSS implementation

```css
/* source: image-generation/create-infographics/resources/layout-patterns.md */
.hub-spoke-layout {
  display: grid;
  grid-template-rows: auto 1fr auto auto;
  gap: 0;
  min-height: 100%;
}

.spoke-canvas {
  position: relative;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.hub-node {
  position: relative;
  z-index: 2;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 2px solid var(--primary);
  background: rgba(var(--primary-rgb), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 20px rgba(var(--primary-rgb), 0.3);
}

.spoke-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  width: 100%;
}

.spoke-node {
  padding: 10px 12px;
  border: 1px solid rgba(var(--primary-rgb), 0.3);
  border-radius: 6px;
  background: rgba(var(--primary-rgb), 0.04);
  font-size: 11px;
  text-align: center;
}
```

## Connection lines — SVG overlay

For true radial connections (spoke lines from hub to each node),
overlay an SVG:

```html
<svg style="position:absolute;inset:0;pointer-events:none;" viewBox="0 0 800 600">
  <line x1="400" y1="300" x2="150" y2="150" stroke="var(--primary)"
    stroke-width="1.5" opacity="0.4" stroke-dasharray="4 3"/>
  <line x1="400" y1="300" x2="400" y2="100" stroke="var(--primary)"
    stroke-width="1.5" opacity="0.4"/>
  <!-- ... more lines from hub to each spoke node -->
</svg>
```

## Gotchas

- Hub must be visually dominant — make it larger, glowing, central.
- Too many spokes (>8) crowd the diagram — group related spokes
  into 3-4 category clusters.
- Spokes should have some hierarchy — primary spokes at cardinal
  directions (N/S/E/W), secondary at diagonals.

## Cross-references

- `TECH-ecosystem-playbook.md` — when to reach for this archetype.
- `TECH-flow-poster-archetype.md` — if flows dominate more than hub.
- `TECH-flywheel-loop-component.md` — circular variant.
- [`../SKILL.md`](../SKILL.md) — parent skill

