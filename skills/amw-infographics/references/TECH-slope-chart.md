---
name: TECH-slope-chart
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Coordinate system](#coordinate-system)
- [HTML](#html)
- [CSS](#css)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Slope chart — before/after comparison

## What it does

Two columns of labeled points connected by lines. Color-codes
positive change (green/accent) vs negative change (red/muted). Best
for 3-8 items showing year-over-year or before/after.

## When to use

- Before/after metric comparisons.
- 2-point trend data (not a full line chart).
- Showing winners and losers across the same period.

## Coordinate system

SVG viewBox `0 0 400 300`. Left column x=80, right column x=320.
Y positions spread evenly between 40 and 260.

## HTML

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<svg viewBox="0 0 400 320" class="slope-svg">
  <!-- Column headers -->
  <text x="80"  y="18" class="slope-col-label" text-anchor="middle">2023</text>
  <text x="320" y="18" class="slope-col-label" text-anchor="middle">2024</text>

  <!-- Column axis lines -->
  <line x1="80"  y1="28" x2="80"  y2="292" class="slope-axis"/>
  <line x1="320" y1="28" x2="320" y2="292" class="slope-axis"/>

  <!-- BTC — up (positive) -->
  <line x1="80" y1="60" x2="320" y2="40" class="slope-line positive"/>
  <circle cx="80"  cy="60" r="5" class="slope-dot positive"/>
  <circle cx="320" cy="40" r="5" class="slope-dot positive"/>
  <text x="72"  y="64" class="slope-label-left">BTC</text>
  <text x="72"  y="56" class="slope-value-left">$42K</text>
  <text x="328" y="44" class="slope-label-right">BTC</text>
  <text x="328" y="36" class="slope-value-right">$98K ↑</text>

  <!-- LUNA — down (negative) -->
  <line x1="80" y1="180" x2="320" y2="240" class="slope-line negative"/>
  <circle cx="80"  cy="180" r="5" class="slope-dot negative"/>
  <circle cx="320" cy="240" r="5" class="slope-dot negative"/>
  <text x="72"  y="184" class="slope-label-left">LUNA</text>
  <text x="72"  y="176" class="slope-value-left">$12</text>
  <text x="328" y="244" class="slope-label-right">LUNA</text>
  <text x="328" y="236" class="slope-value-right">$0.01 ↓</text>
</svg>
```

## CSS

```css
.slope-line {
  stroke-width: 2;
  fill: none;
}
.slope-line.positive { stroke: var(--primary); opacity: 0.8; }
.slope-line.negative { stroke: #ef4444; opacity: 0.7; }

.slope-dot { fill: var(--bg-primary); stroke-width: 2; }
.slope-dot.positive { stroke: var(--primary); }
.slope-dot.negative { stroke: #ef4444; }

.slope-label-left {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  fill: var(--muted);
  text-anchor: end;
}
.slope-value-left {
  font-family: var(--font-display);
  font-size: 11px;
  fill: var(--text-secondary);
  text-anchor: end;
}

.slope-label-right {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  fill: var(--muted);
  text-anchor: start;
}
.slope-value-right {
  font-family: var(--font-display);
  font-size: 11px;
  fill: var(--text-secondary);
  text-anchor: start;
}
.slope-value-right.positive { fill: var(--primary); }
.slope-value-right.negative { fill: #ef4444; }
```

## Gotchas

- Lines crossing each other = visual chaos. If 2+ lines would
  cross, stagger Y positions to avoid crossings.
- `↑` and `↓` glyphs in the value text show direction. Keep them in
  the value, not in a separate element.
- `#ef4444` is a fixed red that works across palettes — don't
  derive it from `var(--primary)`.

## Cross-references

- [TECH-chart-selection-guide](TECH-chart-selection-guide.md) — when to pick slope over line
  > What it does · The decision table · The rule · Chart.js when yes · Chart.js loading · The canvas size trick · Gotchas · Cross-references
  chart.
- [TECH-annotated-bar-chart](TECH-annotated-bar-chart.md) — alternative for single-period
  > What it does · When to use · HTML (excerpt — see source for full) · CSS · The hero bar signature · Gotchas · Cross-references
  comparisons.
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

