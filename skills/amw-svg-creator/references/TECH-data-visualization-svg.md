---
name: TECH-data-visualization-svg
category: svg-dataviz
source: image-generation/svg-creator/SKILL.md
also-in: image-generation/svg-creator/references/advanced-techniques.md
---
## Table of Contents

- [What it does](#what-it-does)
- [Bar chart with gradient + drop shadow](#bar-chart-with-gradient-drop-shadow)
- [Donut chart — arc math](#donut-chart-arc-math)
- [Axis lines](#axis-lines)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Data visualization in SVG — bars, donuts, grids

## What it does

Patterns for building data charts directly in SVG — no Chart.js, no
D3. Suitable for static infographics and documentation where
dependencies are unwanted.

## Bar chart with gradient + drop shadow

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<defs>
  <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"
    color-interpolation="linearRGB">
    <stop offset="0%"   stop-color="#93c5fd"/>
    <stop offset="50%"  stop-color="#3b82f6"/>
    <stop offset="100%" stop-color="#1d4ed8"/>
  </linearGradient>
</defs>
<rect x="40" y="80" width="50" height="170" rx="4" fill="url(#bar)"
  filter="url(#drop-shadow)"/>
```

Key moves:
- 3-stop gradient for depth
- `rx="4"` rounded caps
- Drop-shadow filter for lift

## Donut chart — arc math

```xml
<!-- Shadow behind -->
<circle cx="200" cy="205" r="80" fill="none" stroke="#1e1b4b" stroke-width="30"
  opacity="0.1" filter="url(#soft)"/>
<!-- Segment: stroke-dasharray = (percentage × circumference), total circumference -->
<circle cx="200" cy="200" r="80" fill="none" stroke="#3b82f6" stroke-width="30"
  stroke-dasharray="201 503" transform="rotate(-90 200 200)" stroke-linecap="round"/>
```

- Circumference = 2π × r ≈ 503 for r=80
- `stroke-dasharray="201 503"` — 40% of the circle is colored (201/503)
- `rotate(-90)` aligns the start to 12 o'clock
- `stroke-linecap="round"` rounds the segment ends

## Axis lines

- Grid: `#f1f5f9`, stroke-width 0.5
- Axes: `#94a3b8`, stroke-width 1
- Labels: `font-size="11"`, `fill="#64748b"`
- Round caps everywhere

## Gotchas

- Compute segment positions from data — don't hand-count percentages.
- Donut rings look crisp only when `stroke-width` is much less than
  the radius — `r=80, stroke-width=30` is a good ratio; `r=40,
  stroke-width=30` looks chunky.
- Chart.js `<canvas>` elements are not SVG — Playwright screenshots
  them correctly, but they won't scale with SVG transforms.

## Cross-references

- [TECH-svg-pie-chart](../../amw-infographics/references/TECH-svg-pie-chart.md) — full-pie
  > What it does · The color rule · Primary shades (preferred) · Brand complementary (max 2-3 hues) · SVG arc math · Segment calculator · Template — 4 segments · Legend — side-by-side · Gotchas · Cross-references
  alternative for infographics.
- [TECH-multi-stop-gradients](TECH-multi-stop-gradients.md) — gradient patterns for chart fills.
  > What it does · When to use · Sky gradient — 6 stops · Sphere radial — 5 stops with offset focal · The `color-interpolation="linearRGB"` rule · Gotchas · Cross-references
- [TECH-drop-shadow-filter](TECH-drop-shadow-filter.md) — the shadow filter used above.
  > What it does · Drop shadow (standard) · Contact shadow (tight, right under object) · Cast shadow (large, soft, far) · Inner shadow (not a drop shadow — opposite direction) · The obligatory `color-interpolation-filters="linearRGB"` · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

