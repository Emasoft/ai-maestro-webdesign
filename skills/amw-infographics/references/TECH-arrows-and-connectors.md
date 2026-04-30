---
name: TECH-arrows-and-connectors
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in:
---

# Arrows & connectors — 71% of pieces

## What it does

Arrows are the signature element — they show how concepts, tokens,
fees, or processes flow between sections. They are NOT optional
decoration. Used in 71% of pieces.

## When arrows are MANDATORY

- **Token / fee flows** — show where money goes
  (fees → treasury → buyback → burn).
- **Process steps** — connect numbered steps with directional arrows.
- **Economy loops** — circular flows (stake → earn → reinvest → stake).
- **Section connections** — when Section A's output feeds Section B.

## Rule

If the infographic explains a process, economy, or flow, arrows are
mandatory. If there are 3+ related sections, at least one connector
arrow should show the relationship.

## Horizontal arrow connector

```css
/* source: image-generation/create-infographics/SKILL.md */
.arrow-right {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  color: var(--primary);
  font-size: 18px;
}
```

Use a Phosphor Icon inside: `<i class="ph-bold ph-arrow-right"></i>`.

## Vertical connector line between sections

```css
.connector-down {
  width: 2px;
  height: 32px;
  margin: 0 auto;
  background: var(--primary);
  position: relative;
}
.connector-down::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: -3px;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 6px solid var(--primary);
}
```

The `::after` pseudo creates the arrowhead as a CSS triangle — no
SVG or icon needed.

## Flow diagram row

```css
.flow-row {
  display: flex;
  align-items: center;
  gap: 0;
}
.flow-node {
  flex: 1;
  padding: 12px 14px;
  border: 1.5px solid rgba(var(--primary-rgb), 0.4);
  border-radius: 8px;
  background: rgba(var(--primary-rgb), 0.06);
}
```

## Phosphor Icons CDN

```html
<!-- source: image-generation/create-infographics/SKILL.md -->
<script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>
```

Usage:
```html
<i class="ph ph-arrow-right"></i>
<i class="ph-bold ph-arrow-right"></i>
<i class="ph-fill ph-arrow-right"></i>
```

## Labels on arrows (for flow diagrams)

Arrows in flow diagrams MUST carry labels. Percentages, action
names, token names:

```html
<div class="flow-arrow">
  <span class="arrow-label">30% fees</span>
  <i class="ph-bold ph-arrow-right"></i>
</div>
```

## Gotchas

- Text-arrow fallbacks (`→`, `⟶`) are banned per `design-principles`'
  ai-slop-avoid rules. Always use Phosphor Icons or CSS triangles.
- Arrows without labels in flow diagrams are the #1 giveaway that
  the piece is AI-generated without editorial discipline.
- Color arrows with `var(--primary)` — a black arrow on dark bg
  disappears.

## Cross-references

- `TECH-flow-with-arrows-component.md` — the full flow component.
- `TECH-flow-poster-archetype.md` — the archetype where arrows
  dominate.
- `TECH-flywheel-loop-component.md` — circular arrow pattern.
- [`../SKILL.md`](../SKILL.md) — parent skill

