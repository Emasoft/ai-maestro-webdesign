---
name: TECH-swim-lane-architecture
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/style-details.md
---

# Swim-lane architecture diagram

## What it does

Two-tier (or multi-tier) horizontal labeled bands showing protocol
layers. Each lane = one architectural layer (e.g., AUCTIONEER
LAYER / STRATEGY LAYER), with flow nodes inside the lane.

## When to use

- Two-tier protocol architectures (Aave-style auctioneer / strategy).
- Multi-layer system designs (frontend / API / database / storage).
- Showing functional separation via horizontal bands.

## CSS

```css
/* source: image-generation/create-infographics/resources/style-details.md */
.swim-diagram {
  border: 1px solid var(--border);
  overflow: hidden;
}

.swim-lane {
  display: grid;
  grid-template-columns: 80px 1fr;
  min-height: 80px;
  border-bottom: 1px solid var(--border);
}

.swim-lane:last-child {
  border-bottom: none;
}

.swim-label {
  background: rgba(var(--primary-rgb), 0.08);
  border-right: 1px solid rgba(var(--primary-rgb), 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  writing-mode: vertical-rl;
  font-size: 8px;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--primary);
}

.swim-content {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
```

## HTML

```html
<div class="swim-diagram">
  <div class="swim-lane">
    <div class="swim-label">AUCTIONEER LAYER</div>
    <div class="swim-content">
      <div class="flow-node"><div class="label">Bid Pool</div></div>
      <div class="flow-arrow"><i class="ph-bold ph-arrow-right"></i></div>
      <div class="flow-node"><div class="label">Match Engine</div></div>
      <div class="flow-arrow"><i class="ph-bold ph-arrow-right"></i></div>
      <div class="flow-node"><div class="label">Settlement</div></div>
    </div>
  </div>
  <div class="swim-lane">
    <div class="swim-label">STRATEGY LAYER</div>
    <div class="swim-content">
      <div class="flow-node"><div class="label">Asset Router</div></div>
      <div class="flow-arrow"><i class="ph-bold ph-arrow-right"></i></div>
      <div class="flow-node"><div class="label">Yield Allocator</div></div>
      <div class="flow-arrow"><i class="ph-bold ph-arrow-right"></i></div>
      <div class="flow-node"><div class="label">Rebalancer</div></div>
    </div>
  </div>
</div>
```

## The vertical label trick

```css
writing-mode: vertical-rl;
```

Rotates the layer label 90° so it reads vertically along the left
edge of the lane. Saves horizontal space — more room for the flow
nodes.

## When NOT to use

- Single-layer systems — swim lanes need 2+ lanes to make sense.
- 4+ lanes — gets cramped on portrait canvases.
- Non-hierarchical systems — swim lanes imply ordered layers.

## Gotchas

- Vertical label text needs generous min-height (80px+) or the label
  wraps weirdly.
- `letter-spacing: 2px` is wide on purpose — matches editorial
  uppercase-label convention.
- `rgba(primary, 0.08)` background on the label is barely visible —
  intentional; the label is informational, not the focus.

## Cross-references

- `TECH-flow-with-arrows-component.md` — the flow-node pattern
  inside the lane.
- `TECH-template-registry.md` — DeFi Protocol template where this
  pattern fits.
- `TECH-hub-spoke-archetype.md` — alternative for hub-centric
  architectures.
- [`../SKILL.md`](../SKILL.md) — parent skill

