---
name: TECH-flow-poster-archetype
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/layout-patterns.md
---

# Archetype 2: Flow Poster

## What it does

Central flow diagram (vertical or circular) dominates the canvas,
with supporting data panels above, below, or on sides. Arrows are
the primary visual — fees, rewards, token movement, process steps.

## When to use

- Token economy flows (fees → treasury → buyback → burn)
- How-it-works explainers where the story IS the flow
- Strategy overviews with numbered steps and branches
- Any piece where the core narrative is "A produces B produces C"

Example references: `token_ecosystem_flow.png`,
`double_token_strategy_flywheel_flow.png`.

## The shape

```
┌────────────────────────────────────────┐
│  HEADER + STATS STRIP                  │
├────────────────────────────────────────┤
│                                        │
│  ┌──────┐  →  ┌──────┐  →  ┌──────┐   │
│  │ Node │     │ Node │     │ Node │   │
│  │  A   │     │  B   │     │  C   │   │
│  └──────┘     └──────┘     └──────┘   │
│       ↓              ↓                │
│  ┌──────┐       ┌──────┐              │
│  │ Node │  ←──  │ Node │              │
│  │  D   │       │  E   │              │
│  └──────┘       └──────┘              │
│                                        │
├────────────────────────────────────────┤
│  SUPPORTING DATA TABLE / BULLET PANEL  │
├────────────────────────────────────────┤
│  FOOTER                                │
└────────────────────────────────────────┘
```

## CSS implementation

```css
/* source: image-generation/create-infographics/resources/layout-patterns.md */
.flow-poster-layout {
  display: grid;
  grid-template-rows: auto 1fr auto auto;
  gap: 0;
  min-height: 100%;
}

.flow-canvas {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.flow-row {
  display: flex;
  align-items: center;
  gap: 0;
  width: 100%;
  justify-content: center;
}

.flow-node {
  flex: 1;
  max-width: 160px;
  padding: 12px 14px;
  border: 1.5px solid rgba(var(--primary-rgb), 0.4);
  border-radius: 8px;
  background: rgba(var(--primary-rgb), 0.06);
  font-size: 12px;
}

.flow-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  color: var(--primary);
  font-size: 16px;
  flex-shrink: 0;
}

.flow-connector-down {
  width: 2px;
  height: 24px;
  background: var(--primary);
  margin: 0 auto;
  position: relative;
}

.flow-connector-down::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: -3px;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 6px solid var(--primary);
}
```

## Label rule

Every arrow in a Flow Poster MUST carry a text label — action name,
percentage, token name. Never unlabeled arrows in a flow diagram.

## Gotchas

- The flow dominates — don't add 4 supporting sections, 1-2 is
  enough.
- Use vertical arrows (`↓`) between rows for clarity on portrait
  canvases. Use horizontal arrows (`→`) on landscape.
- Branch/split nodes (diamond where flow diverges) need labels on
  each outgoing arrow.

## Cross-references

- `TECH-arrows-and-connectors.md` — detailed arrow patterns.
- `TECH-flow-with-arrows-component.md` — the flow_with_arrows CSS.
- `TECH-flywheel-loop-component.md` — circular variant.
- `TECH-stacked-reference-archetype.md` — default alternative.
- [`../SKILL.md`](../SKILL.md) — parent skill

