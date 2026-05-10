---
name: TECH-bar-chart-css
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [HTML](#html)
- [CSS](#css)
- [The 3-column grid layout](#the-3-column-grid-layout)
- [Animation — CSS transition](#animation-css-transition)
- [Progress bars — single metric variant](#progress-bars-single-metric-variant)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# CSS horizontal bar chart — vesting / allocation strips

## What it does

Pure-CSS horizontal bars for vesting schedules, allocation strips,
and ranked lists. Zero dependencies. Renders identically in browser,
PNG export, PDF.

## HTML

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<div class="bar-chart">
  <div class="bar-row">
    <div class="bar-label">COMMUNITY</div>
    <div class="bar-track">
      <div class="bar-fill" style="width: 35%; background: #F5A623;">
        <span class="bar-pct">35%</span>
      </div>
    </div>
    <div class="bar-value">350M</div>
  </div>
  <div class="bar-row">
    <div class="bar-label">ECOSYSTEM</div>
    <div class="bar-track">
      <div class="bar-fill" style="width: 25%; background: #00E5A0;">
        <span class="bar-pct">25%</span>
      </div>
    </div>
    <div class="bar-value">250M</div>
  </div>
</div>
```

## CSS

```css
.bar-chart { display: flex; flex-direction: column; gap: 10px; }

.bar-row {
  display: grid;
  grid-template-columns: 140px 1fr 80px;
  align-items: center;
  gap: 12px;
}

.bar-label {
  font-family: var(--font-body);
  font-size: var(--text-caption);
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  text-align: right;
}

.bar-track {
  height: 10px;
  background: rgba(255,255,255,0.07);
  border-radius: 5px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 4px;
  box-shadow: 0 0 8px rgba(255,255,255,0.15);
  transition: width 0.8s ease;
}

.bar-pct {
  font-size: 9px;
  font-family: var(--font-mono);
  color: rgba(255,255,255,0.7);
  white-space: nowrap;
}

.bar-value {
  font-family: var(--font-body);
  font-size: var(--text-caption);
  color: var(--text);
  text-transform: uppercase;
}
```

## The 3-column grid layout

```
┌─────────────┬────────────────────────┬──────┐
│ LABEL       │ ████████░░░░░░░░  35%  │ 350M │
└─────────────┴────────────────────────┴──────┘
  140px fixed   1fr (flexible)          80px fixed
```

- Left: label (uppercase, right-aligned)
- Middle: track + fill (percentage-based width)
- Right: value (uppercase)

## Animation — CSS transition

```css
.bar-fill {
  transition: width 0.8s ease;
}
```

Set `width: 0` initially, then set to target width via JS:
```js
requestAnimationFrame(() => {
  document.querySelectorAll('.bar-fill').forEach(b =>
    b.style.width = b.dataset.width
  );
});
```

## Progress bars — single metric variant

```css
.progress-bar {
  height: 8px;
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  box-shadow: 0 0 8px rgba(var(--primary-rgb), 0.5);
}
```

## Gotchas

- Rows beyond 8 look cramped — split into two columns.
- `box-shadow: 0 0 8px rgba(255,255,255,0.15)` creates subtle glow
  around the fill — signature neon feel.
- The 3-column grid (140px/1fr/80px) is tuned for typical labels —
  bump left column to 180px for longer labels.

## Cross-references

- [TECH-progress-bar-vesting](TECH-progress-bar-vesting.md) — the vesting-specific progress
  > What it does · When to use · HTML · CSS · The milestone marker trick · Labels row — above and below · Gradient fill · Gotchas · Cross-references
  variant.
- [TECH-svg-pie-chart](TECH-svg-pie-chart.md) — alternative for proportions.
  > What it does · The color rule · Primary shades (preferred) · Brand complementary (max 2-3 hues) · SVG arc math · Segment calculator · Template — 4 segments · Legend — side-by-side · Gotchas · Cross-references
- [TECH-annotated-bar-chart](TECH-annotated-bar-chart.md) — SVG bar with annotations.
  > What it does · When to use · HTML (excerpt — see source for full) · CSS · The hero bar signature · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
