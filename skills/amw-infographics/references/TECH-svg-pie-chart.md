---
name: TECH-svg-pie-chart
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The color rule](#the-color-rule)
  - [1. Primary shades (preferred)](#1-primary-shades-preferred)
  - [2. Brand complementary (max 2-3 hues)](#2-brand-complementary-max-2-3-hues)
- [SVG arc math](#svg-arc-math)
- [Segment calculator](#segment-calculator)
- [Template — 4 segments](#template-4-segments)
- [Legend — side-by-side](#legend-side-by-side)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# SVG pie chart — token allocation (the #1 chart)

## What it does

Full-solid SVG pie chart (no donut hole). Central chart in 35% of
infographics. Built as inline SVG so it works in PNG/PDF with zero
dependencies.

## The color rule

**Never arbitrary rainbow.** Two options, in priority:

### 1. Primary shades (preferred)

Derive all segment colors from HSL shades of the brand primary.
Example for amber `#F5A623` (HSL 37°, 91%, 55%):

```
Shade 1 (lightest): hsl(37, 85%, 70%) → #F7C26B
Shade 2 (primary):  hsl(37, 91%, 55%) → #F5A623 ← fullest
Shade 3:            hsl(37, 76%, 40%) → #C4841A
Shade 4 (darkest):  hsl(37, 75%, 27%) → #7A5211
```

Spread evenly across lightness — ensure adjacent segments contrast.

### 2. Brand complementary (max 2-3 hues)

Only if brand has defined secondary/accent colors. Never invent
colors not in the brand palette. Never exceed 3 distinct hues.

## SVG arc math

Each segment is a filled `<path>` wedge from the center:
```
M cx cy          — move to center
L x1 y1          — line to arc start
A r r 0 [large-arc] 1 x2 y2   — arc to end (clockwise)
Z                — close to center
```

Point on circle at angle θ (0° = right, increases clockwise in SVG):
```
x = cx + r * cos(θ * π/180)
y = cy + r * sin(θ * π/180)
```

Start angle: **−90°** (12 o'clock). Add each segment's degrees to advance.
`large-arc-flag` = 1 if segment > 50%, else 0.

## Segment calculator

```
segment_degrees = percentage / 100 * 360
start_angle     = -90 + (sum of previous segments' degrees)
end_angle       = start_angle + segment_degrees
x1 = 100 + 90 * cos(start_angle * π/180)
y1 = 100 + 90 * sin(start_angle * π/180)
x2 = 100 + 90 * cos(end_angle * π/180)
y2 = 100 + 90 * sin(end_angle * π/180)
large-arc-flag = segment_degrees > 180 ? 1 : 0
```

## Template — 4 segments

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<svg viewBox="0 0 200 200" width="280" height="280">
  <circle cx="100" cy="100" r="90" fill="#0D0D0D"/>
  <!-- Segment 1: 35% → start -90°, end 36° -->
  <path d="M 100 100 L 100 10.0 A 90 90 0 0 1 172.8 152.9 Z"
    fill="#F7C26B" stroke="#0D0D0D" stroke-width="1.5"/>
  <!-- Segment 2: 25% → start 36°, end 126° -->
  <path d="M 100 100 L 172.8 152.9 A 90 90 0 0 1 47.1 172.8 Z"
    fill="#F5A623" stroke="#0D0D0D" stroke-width="1.5"/>
  <!-- Segment 3: 20% → start 126°, end 198° -->
  <path d="M 100 100 L 47.1 172.8 A 90 90 0 0 1 14.4 72.2 Z"
    fill="#C4841A" stroke="#0D0D0D" stroke-width="1.5"/>
  <!-- Segment 4: 20% → start 198°, end 270° -->
  <path d="M 100 100 L 14.4 72.2 A 90 90 0 0 1 100 10.0 Z"
    fill="#7A5211" stroke="#0D0D0D" stroke-width="1.5"/>
</svg>
```

## Legend — side-by-side

```html
<div class="chart-legend">
  <div class="legend-item">
    <span class="legend-dot" style="background:#F7C26B;"></span>
    <span class="legend-label">COMMUNITY / AIRDROP</span>
    <span class="legend-pct">35%</span>
  </div>
  <!-- ... more items -->
</div>
```

## Gotchas

- Segments < 5% look like slivers — merge into "Other" if possible.
- `stroke` between segments (background color) creates a gap —
  essential for adjacent segments to read distinctly.
- Full pie (no donut hole) is the signature — don't add a center
  circle to make a donut unless specifically needed.

## Cross-references

- [TECH-chart-selection-guide](TECH-chart-selection-guide.md) — when to use pie vs other charts.
- [TECH-waffle-chart](TECH-waffle-chart.md) — alternative for single-percentage stories.
- [TECH-annotation-first](TECH-annotation-first.md) — labels go on the chart, not in a
  separate legend when <5 series.
- [`../SKILL.md`](../SKILL.md) — parent skill

