---
name: TECH-waffle-chart
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [HTML](#html)
- [CSS](#css)
- [JS — add `.filled` + stagger](#js-add-filled-stagger)
- [Legend styling](#legend-styling)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Waffle chart — 10×10 grid for % of total

## What it does

A 10×10 grid of 100 squares. Fill N squares to show N%. More
memorable and honest than a pie chart for single-percentage
stories. Editorial feel — less clinical than pie.

## When to use

- Single-percentage stories where memory matters ("63% of supply
  locked").
- Editorial infographics that prefer grid visuals over circular.
- Alternatives to pie when the percentage IS the story.

## HTML

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<div class="waffle-chart-wrapper">
  <div class="waffle-grid" style="--fill-count: 63;">
    <!-- 100 squares — generate with a loop or paste -->
    <span class="waffle-cell"></span>
    <!-- ... 100 total -->
  </div>
  <div class="waffle-legend">
    <div class="waffle-stat">63%</div>
    <div class="waffle-label">OF SUPPLY LOCKED</div>
    <div class="waffle-detail">630M / 1B tokens</div>
  </div>
</div>
```

## CSS

```css
.waffle-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 3px;
  width: 200px;
  height: 200px;
}

.waffle-cell {
  background: rgba(255,255,255,0.08);
  border-radius: 2px;
  aspect-ratio: 1;
}

.waffle-cell.filled {
  background: var(--primary);
  box-shadow: 0 0 4px rgba(var(--primary-rgb), 0.4);
}

/* Staggered fill-in animation */
.waffle-cell.filled {
  animation: waffleFill 0.4s ease both;
  animation-delay: calc(var(--i) * 8ms);
}
@keyframes waffleFill {
  from { transform: scale(0.2); opacity: 0; background: var(--primary); }
  to   { transform: scale(1); opacity: 1; }
}
```

## JS — add `.filled` + stagger

```js
// source: image-generation/create-infographics/resources/charts.md
document.querySelectorAll('.waffle-grid').forEach(grid => {
  const count = parseInt(getComputedStyle(grid).getPropertyValue('--fill-count')) || 0;
  grid.querySelectorAll('.waffle-cell').forEach((cell, i) => {
    if (i < count) {
      cell.classList.add('filled');
      cell.style.setProperty('--i', i);
    }
  });
});
```

## Legend styling

```css
.waffle-stat {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 6vw, 3.5rem);
  font-weight: 800;
  color: var(--primary);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}
.waffle-label {
  font-size: var(--text-caption);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-secondary);
}
```

## Gotchas

- Always 10×10 = 100 squares. Not 5×5 = 25 (which would need
  different math for percentages).
- `:nth-child` with CSS custom property (`--fill-count`) doesn't
  work — need JS to add the `.filled` class.
- Staggered animation delay (`--i` × 8ms) creates a sweeping fill
  effect — keep the multiplier low so the whole animation
  completes in ~800ms.

## Cross-references

- [TECH-svg-pie-chart](TECH-svg-pie-chart.md) — alternative for the same data shape.
  > What it does · The color rule · Primary shades (preferred) · Brand complementary (max 2-3 hues) · SVG arc math · Segment calculator · Template — 4 segments · Legend — side-by-side · Gotchas · Cross-references
- [TECH-chart-selection-guide](TECH-chart-selection-guide.md) — when to pick which.
  > What it does · The decision table · The rule · Chart.js when yes · Chart.js loading · The canvas size trick · Gotchas · Cross-references
- [TECH-annotation-first](TECH-annotation-first.md) — the accompanying stat/label pattern.
  > What it does · The per-chart-type rule · Legend exception · Callout line technique — highlight outliers · Insight callout box (for major insights) · Threshold / benchmark line · The rule · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
