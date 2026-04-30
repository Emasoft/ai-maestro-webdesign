---
name: TECH-chart-selection-guide
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---

# Chart selection — decision tree for chart type

## What it does

Matches data shape to the right chart type. Rule: use CSS/SVG for
anything static and allocation-based. Use Chart.js only when the
data is dynamic or the chart genuinely requires it.

## The decision table

| Chart type | Method | When |
|-----------|--------|------|
| **Pie (full)** | Inline SVG | Token allocation, any % breakdown ≤ 8 segments |
| **Horizontal bar** | Pure CSS | Vesting schedule, allocation strips, ranked lists |
| **Vertical bar** | Chart.js | Multi-period comparisons, time-series bars |
| **Line chart** | Chart.js | Price over time, growth curves, trend lines |
| **Radar / Spider** | Chart.js | Game character stats, feature comparisons |
| **Progress bar** | Pure CSS | Unlock progress, single metric completion |
| **Waffle chart** | Pure HTML/CSS | % of total — more memorable than pie |
| **Slope chart** | Inline SVG | Before/after comparison, two-point change |
| **Annotated bar** | Inline SVG | Bar chart with callout on hero + benchmark |
| **Proportional circles** | Inline SVG | 3-6 magnitudes where area = value |
| **Dot plot** | Inline SVG | Distribution, individual data points |

## The rule

> Never add Chart.js just for a bar chart you could build in CSS.

CSS/SVG charts have zero runtime dependencies, work in PNG/PDF
export, and render instantly. Chart.js earns its place for
dynamic/interactive charts (line, vertical bar, radar) or for
animations.

## Chart.js when yes

- Line charts showing time series (price history, growth).
- Vertical bar charts with multiple datasets per bar.
- Radar charts for multi-axis comparisons.
- Animated counters or interactive tooltips.

## Chart.js loading

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

Use `<canvas>` elements — Playwright screenshots canvas correctly.

## The canvas size trick

For Chart.js charts in infographics:

```html
<div class="chart-container" style="position:relative; height:240px;">
  <canvas id="lineChart"></canvas>
</div>
```

Chart.js needs an explicit container height or it'll render at 0px.

## Gotchas

- Don't use Chart.js for static allocations — SVG pie is cleaner,
  faster, better in PDF export.
- Don't add Chart.js just because you want an animated fill —
  CSS animations on SVG bars work fine.
- Chart.js + Playwright export: set `animation: false` in the
  chart options or the screenshot captures mid-animation.

## Cross-references

- `TECH-svg-pie-chart.md` — the most-used SVG chart.
- `TECH-waffle-chart.md` — the single-percentage alternative.
- `TECH-line-chart.md` — when to use Chart.js line.
- `TECH-bar-chart-css.md` — the CSS horizontal bar.
- `TECH-radar-chart.md` — Chart.js radar for game stats.
- [`../SKILL.md`](../SKILL.md) — parent skill

