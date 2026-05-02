---
name: TECH-dot-plot
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [HTML](#html)
- [CSS](#css)
- [Y-jitter convention](#y-jitter-convention)
- [Annotations — median line, ranges](#annotations-median-line-ranges)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Dot plot — distribution + individual points

## What it does

Shows individual data points on a linear scale. Less misleading than
bars for distributions. Editorial and clean. Best for 8-40 points.

## When to use

- Validator uptime distributions, response time distributions.
- Any data where seeing individual points matters more than
  aggregates.
- Replacing bar charts that hide variance.

## HTML

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<svg viewBox="0 0 500 200" class="dot-plot-svg">
  <text x="20" y="16" class="dp-title">VALIDATOR UPTIME DISTRIBUTION (%)</text>

  <!-- Axis line + ticks -->
  <line x1="20" y1="160" x2="480" y2="160" class="dp-axis"/>
  <!-- value*4.6+20 = x  (0→20, 100→480) -->
  <line x1="20"  y1="158" x2="20"  y2="164" class="dp-tick"/>
  <text x="20"  y="175" class="dp-tick-label" text-anchor="middle">0%</text>
  <!-- ... more ticks -->

  <!-- Top Validators (y=60) -->
  <text x="15" y="64" class="dp-cat-label" text-anchor="end">TOP TIER</text>
  <circle cx="479" cy="60" r="5" class="dp-dot hero"/>   <!-- 99.8% hero -->
  <circle cx="477" cy="54" r="4" class="dp-dot"/>         <!-- 99.5 -->
  <circle cx="476" cy="66" r="4" class="dp-dot"/>         <!-- 99.1 -->

  <!-- Mid Validators (y=110) with jitter in y -->
  <text x="15" y="114" class="dp-cat-label" text-anchor="end">MID TIER</text>
  <circle cx="400" cy="108" r="4" class="dp-dot mid"/>
  <circle cx="385" cy="114" r="4" class="dp-dot mid"/>
  <!-- ... more dots with y-jitter for natural scatter -->

  <!-- Median annotation -->
  <line x1="365" y1="30" x2="365" y2="150" class="dp-median-line"/>
  <text x="368" y="38" class="dp-annotation">MEDIAN</text>
  <text x="368" y="48" class="dp-annotation-val">75%</text>
</svg>
```

## CSS

```css
.dp-dot {
  fill: rgba(255,255,255,0.25);
  stroke: none;
}
.dp-dot.hero {
  fill: var(--primary);
  filter: drop-shadow(0 0 4px rgba(var(--primary-rgb), 0.6));
  r: 6;
}
.dp-dot.mid { fill: rgba(255,255,255,0.15); }

.dp-median-line {
  stroke: rgba(255,255,255,0.25);
  stroke-width: 1;
  stroke-dasharray: 3 3;
}
```

## Y-jitter convention

When many points share similar x-values (e.g. several validators at
~99%), add small random Y offsets (±5-10px) so they don't stack
into one dot. Keeps individual points readable.

## Annotations — median line, ranges

Overlay reference lines (median, mean, range brackets) as dashed
lines with small text labels. Cue readers to the distribution's
shape without forcing them to read every dot.

## Gotchas

- Too many dots (>40) create noise — filter or aggregate.
- Use `.hero` class sparingly — 1 highlighted dot per category.
- Jitter should be consistent — don't randomize on every render.

## Cross-references

- [TECH-chart-selection-guide](TECH-chart-selection-guide.md) — when to reach for dot plot.
- [TECH-annotated-bar-chart](TECH-annotated-bar-chart.md) — bar alternative.
- [TECH-slope-chart](TECH-slope-chart.md) — 2-point alternative.
- [`../SKILL.md`](../SKILL.md) — parent skill

