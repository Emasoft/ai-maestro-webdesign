---
name: TECH-chart-variants
category: infographic-template
source: web-content-designer-main/dashboard-structure.md + ux-designer-skill-main/references/18-data-visualization.md + Tufte data-ink (T-145..T-148 synthesis)
also-in:
---

## Table of Contents

- [What this is](#what-this-is)
- [Decision matrix — chart by data shape](#decision-matrix--chart-by-data-shape)
- [Per-type axis, legend, grid conventions](#per-type-axis-legend-grid-conventions)
- [Data-ink maximization (Tufte)](#data-ink-maximization-tufte)
- [Forbidden chart patterns](#forbidden-chart-patterns)
- [Cross-references](#cross-references)

# Chart variants — type catalogue, when to use which, axis conventions

## What this is

Catalogue of chart variants that ship in the consulting-grade output
this plugin produces. Decision matrix selects type from the data
shape; per-type sections give the axis, legend, and grid conventions
that prevent a chart from looking like a default Chart.js example.

This file complements `TECH-chart-selection-guide.md` (which decides
CSS-vs-Chart.js) — that file picks the render method; this file
picks the chart type and tunes its anatomy.

## Decision matrix — chart by data shape

| Data shape | Primary chart | Acceptable alt | Avoid |
|---|---|---|---|
| Single ranked series, ≤ 8 categories | Horizontal bar | Lollipop, dot plot | Pie (low precision) |
| Single ranked series, > 8 categories | Vertical bar (sorted desc) | Dot plot | Word cloud |
| Time series, single line | Line chart | Sparkline (inline) | Bar chart |
| Time series, 2–4 lines, all comparable | Line chart (multi) | Small multiples | Stacked area |
| Time series with composition over time | Stacked area | Stream graph | Pie per period |
| Composition of 100%, 3–5 segments | Donut, waffle | Stacked bar (single) | 3D pie |
| Composition of 100%, 6+ segments | Stacked horizontal bar | Treemap | Donut (too crowded) |
| 2-variable correlation | Scatter plot | Hexbin (large N) | Bar pair |
| 3-variable (X, Y, magnitude) | Bubble chart | Heatmap | 3D anything |
| Geographic distribution | Choropleth | Symbol map | Bubble on world map |
| Hierarchical proportion | Treemap | Sunburst | Nested pie |
| Flow between categories | Sankey | Chord diagram | Multi-line spaghetti |
| Distribution / frequency | Histogram | Box plot, violin | Bar with raw counts |
| Density across 2 dimensions | Heatmap | Hexbin | Scatter (overplotted) |
| Before / after, 2 points only | Slope chart | Dumbbell, paired bar | Animated transition |
| Process / journey stages | Funnel | Stepped horizontal bar | Pyramid |

## Per-type axis, legend, grid conventions

### Bar chart (horizontal or vertical)
- **Axis floor:** zero. Always. No exceptions — non-zero baselines lie.
- **Bar order:** sorted descending by value, unless category has natural order (months, sizes).
- **Bar width vs gap:** bar 4× gap, e.g. 32px bar + 8px gap.
- **Grid lines:** light horizontal only (`rgba(0,0,0,0.04)`). No vertical grid.
- **Labels:** prefer labels-on-bars (right of bar end for horizontal, above for vertical) over a separate legend.
- **No 3D, no shadows, no gradients on bars.**

### Line chart
- **Axis floor:** does NOT have to be zero (lines show change, not magnitude). Tight Y range emphasizes pattern.
- **Line weight:** 2px primary, 1.5px secondary, 1px reference/benchmark.
- **Data points:** dots at each X value only if N ≤ 20; for dense series, line only.
- **Grid lines:** 4–6 horizontal gridlines max, dotted or `rgba(0,0,0,0.04)`. No vertical.
- **Legend:** label-at-end-of-line (right of last point) over a boxed legend.

### Stacked area
- **Reserve for cumulative metrics** where total matters (revenue, market share over time).
- **Order segments by stability** — most stable category at the bottom.
- **Cap segments at 5** — beyond that, switch to small multiples.

### Donut chart
- **Inner radius ≥ 60% of outer.** Anything thinner is harder to compare than a bar.
- **Center label:** use the empty middle for total or KPI.
- **Max 5 segments.** Beyond 5, donut becomes unreadable — switch to stacked horizontal bar.
- **Sort segments largest-to-smallest, clockwise from 12 o'clock.**
- **No legend** — labels on segments (with leader lines if needed).

### Scatter plot
- **Both axes start at zero** unless the relationship is purely about deviation from a center.
- **Dot opacity 0.6** when N > 50 (reveals density without overplotting).
- **Trend line:** include if R² > 0.3, label with the R² value.
- **Quadrant labels** when the chart is conceptual (e.g., effort vs impact matrix).

### Sparkline (inline)
- **Inline `<svg>` 12–14px tall.**
- **No axes, no labels, no grid.** Just the line.
- **End dot in `--primary`** to anchor the last value.
- **Use when:** a row of numeric values would benefit from a tiny trend visual — KPI cards, table rows.

### Small multiples
- **Same scale on every panel** (the whole point — comparison).
- **Same chart type on every panel.**
- **3–12 panels** in a grid. Beyond 12 they shrink past readability.
- **One axis label set total** (left and bottom of the grid), not per panel.

### Heatmap
- **Sequential color scale** — monochromatic gradient of `--primary` (5–7 stops).
- **Diverging only when there is a meaningful zero** (positive vs negative deviation).
- **Square cells** unless the data has natural rectangular grid (calendar = squares; matrix = rect).
- **Cell labels** when N cells ≤ 50; tooltip-only beyond that.

## Data-ink maximization (Tufte)

The chart's job is to show the data. Every pixel of ink that does not represent data is overhead. Cut overhead aggressively:

- **No chart background fill.** White or transparent.
- **No chart border / box around the plot area.**
- **Gridlines dotted or `rgba(0,0,0,0.04)`, never solid or dark.**
- **No axis lines** — let the data and ticks imply the axes.
- **Labels on data, not in a separate legend** when possible (line ends, bar tips, segment centers).
- **No borders on bars / dots / segments.** Fill only.
- **Tick marks: 4–6 max per axis.** Not 10, not "automatic".
- **Muted color palette** — desaturate brand by 20–30% for chart fills so the data reads as analytical, not promotional.
- **Thin-line method:** 1.5–2px for structural lines (data), 0.5px for decorative lines (axes, gridlines).

## Forbidden chart patterns

- **3D anything.** 3D pie, 3D bar, 3D donut — all distort proportion.
- **Pie chart with > 5 segments.**
- **Donut with inner radius < 40%** (becomes a pie).
- **Stacked bar with > 5 segments per bar.**
- **Dual Y-axis on a single line chart** — Tufte calls this lying.
- **Spaghetti line charts** (> 4 overlapping lines).
- **Truncated Y-axis on bar charts.**
- **Rainbow color palettes** on a single-series chart.
- **Bright alarm red on data** — use muted oxblood (`#6b1220`) for downside signals.
- **Border-radius > 2px on bars.**
- **Drop-shadows or glow on chart elements.**
- **Animated chart entrance > 600ms.** Anything longer is a distraction.

## Cross-references

- `TECH-chart-selection-guide.md` — CSS-vs-Chart.js render method
- `TECH-data-viz-templates.md` — reusable data-viz panel templates (this file is per-chart; that one is per-section)
- `TECH-dashboard-archetypes.md` — chart density by dashboard archetype
- `TECH-annotated-bar-chart.md` — annotation idioms
- `skills/amw-design-principles/ai-slop-avoid.md` — VI Color (saturation ceiling, palette discipline)
