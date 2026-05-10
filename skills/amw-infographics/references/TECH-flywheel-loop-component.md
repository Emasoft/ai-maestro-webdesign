---
name: TECH-flywheel-loop-component
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [CSS](#css)
- [HTML](#html)
- [Arrow labels (mandatory)](#arrow-labels-mandatory)
- [When to use a horizontal flow instead](#when-to-use-a-horizontal-flow-instead)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# `flywheel_loop` — rectangular nodes → circular back to start

## What it does

The designer's signature economy-loop diagram: rectangular process
nodes connected by directional arrows, forming a closed loop that
returns to the start. Used for token economies, fee loops, incentive
cycles.

## When to use

- Token flywheels (stake → earn → reinvest → stake)
- Fee loops (fees → treasury → buyback → burn → supply reduced)
- Incentive cycles (play → earn → spend → create value → more play)
- Any closed economic loop where A feeds B feeds ... feeds A

## CSS

```css
.flywheel-loop {
  position: relative;
  width: 400px;
  height: 400px;
  margin: 0 auto;
}

/* Nodes positioned at 0°, 90°, 180°, 270° */
.flywheel-node {
  position: absolute;
  width: 120px;
  padding: 12px 16px;
  border: 1.5px solid rgba(var(--primary-rgb), 0.4);
  background: rgba(var(--primary-rgb), 0.08);
  border-radius: 8px;
  text-align: center;
}

.flywheel-node.top    { top: 0;    left: 50%; transform: translateX(-50%); }
.flywheel-node.right  { right: 0;  top: 50%;  transform: translateY(-50%); }
.flywheel-node.bottom { bottom: 0; left: 50%; transform: translateX(-50%); }
.flywheel-node.left   { left: 0;   top: 50%;  transform: translateY(-50%); }

/* Connecting arrows — SVG overlay */
.flywheel-arrows {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.flywheel-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.flywheel-sub {
  font-size: 10px;
  color: var(--muted);
  margin-top: 3px;
}
```

## HTML

```html
<div class="flywheel-loop">
  <div class="flywheel-node top">
    <div class="flywheel-label">STAKE</div>
    <div class="flywheel-sub">Deposit $TKN</div>
  </div>
  <div class="flywheel-node right">
    <div class="flywheel-label">EARN</div>
    <div class="flywheel-sub">8% APY</div>
  </div>
  <div class="flywheel-node bottom">
    <div class="flywheel-label">COMPOUND</div>
    <div class="flywheel-sub">Auto-reinvest</div>
  </div>
  <div class="flywheel-node left">
    <div class="flywheel-label">GROW</div>
    <div class="flywheel-sub">Larger stake</div>
  </div>

  <svg class="flywheel-arrows" viewBox="0 0 400 400">
    <!-- Curved arrows connecting nodes clockwise -->
    <path d="M 250 60 Q 340 60 340 150" stroke="var(--primary)"
      fill="none" stroke-width="2" marker-end="url(#arrow)"/>
    <!-- ... 3 more arrows around the loop -->

    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5"
        markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--primary)"/>
      </marker>
    </defs>
  </svg>
</div>
```

## Arrow labels (mandatory)

Each arrow carries a label — action name, percentage, token name.
Position labels at the midpoint of the arc:

```svg
<text x="340" y="100" font-size="10" fill="var(--primary)"
  text-anchor="middle" text-transform="uppercase" letter-spacing="0.05em">
  REWARDS
</text>
```

## When to use a horizontal flow instead

If the story is linear (3-5 steps, no return), use
`TECH-flow-with-arrows-component` — horizontal flow nodes, no
circularity. Flywheel is specifically for closed loops.

## Gotchas

- 4 nodes is the sweet spot. 3 feels incomplete; 5+ gets crowded.
- Arrows should curve (SVG `<path>`), not be straight lines — the
  curvature communicates "loop" visually.
- SVG `<marker>` for arrowheads avoids the text-arrow anti-pattern
  but requires `viewBox` + `refX`/`refY` to position the arrowhead.

## Cross-references

- [TECH-flow-with-arrows-component](TECH-flow-with-arrows-component.md) — linear alternative.
  > What it does · When to use · Horizontal flow — CSS · Vertical connector — CSS · HTML · Arrow icons — Phosphor only · Label rule — mandatory · Gotchas · Cross-references
- [TECH-token-economics-playbook](TECH-token-economics-playbook.md) — where flywheels appear most.
  > What it does · When to use · Color system · Typography · Standard component prevalence (across 62 pieces) · Visual properties · Signature layout pattern (portrait-tall, 10+ content blocks) · CSS variables · Font pair · Reference template · Density rule · Gotchas · Cross-references
- [TECH-flow-poster-archetype](TECH-flow-poster-archetype.md) — archetype for flywheel-dominant
  > What it does · When to use · The shape · CSS implementation · Label rule · Gotchas · Cross-references
  pieces.
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
