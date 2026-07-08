---
name: TECH-chart-rendering
category: svg-dataviz
source: amw-asset-generator-agent §9 (chart-rendering routing rows)
also-in: ../docs/components/chart.mdx (shadcn-ui chart wrapper for Recharts), TECH-data-visualization-svg.md (hand-authored SVG bars/donuts)
---

# Chart rendering — library trade-off matrix

## Table of Contents

- [What it does](#what-it-does)
- [Boundary](#boundary)
- [Library matrix](#library-matrix)
- [Decision flow](#decision-flow)
- [Brand-token integration](#brand-token-integration)
- [Accessibility](#accessibility)
- [Output format](#output-format)
- [What the agent must NOT do](#what-the-agent-must-not-do)

## What it does

Decision matrix for picking a chart library or hand-authoring SVG when the
brief asks for line / bar / pie / donut / sparkline / area / scatter /
radar / treemap / gauge charts on a real, data-backed deliverable
(dashboard widget, blog header, marketing-stats hero, infographic).

## Boundary

This TECH file does NOT pick ONE library — it documents trade-offs so the
agent can recommend the best fit per brief. The matrix is the contract.
The skill `amw-svg-creator` always retains the option to hand-author the
SVG (TECH-data-visualization-svg.md) for static, no-runtime cases.

## Library matrix

| Library | Best for | Render output | Bundle weight | Interactivity | A11y story | When to pick |
|---|---|---|---|---|---|---|
| **Hand-authored SVG** (this skill, TECH-data-visualization-svg.md) | static infographic; export to PNG; no runtime | SVG | 0 KB | none (pure declarative SVG) | manual `<title>`/`<desc>` per element | Brief is "render once and ship", no interactivity, ≤ 20 data points, no real-time updates |
| **Chart.js 4.x** | dashboards, marketing pages, simple to moderate interactivity | Canvas | ~70 KB gz (core only); ~10 KB gz per extra plugin | hover tooltips, click events, pan/zoom via plugin | ARIA via `chartjs-plugin-a11y` (community plugin); canvas needs explicit fallback table | Brief needs hover tooltips, simple animations, common chart types (line/bar/pie/donut/scatter/radar) |
| **D3.js 7.x** | bespoke / scientific / publication-quality / unusual chart types | SVG (or Canvas) | ~40 KB gz core; selectively import sub-modules | full custom interactivity (drag, zoom, brush, force) | manual ARIA on every node — no built-in story | Brief is custom: chord diagrams, force-directed graphs, hierarchical treemaps, hexbin, parallel-coords, custom geo |
| **Recharts** (React) | React projects with shadcn-ui — composable React API | SVG | ~110 KB gz | rich React event surface; declarative props | manual but each component allows ARIA pass-through | Brief is React/Next/shadcn stack; common chart types; declarative API matches the React mental model. Note `amw-shadcn-ui/vendor/components/chart.mdx` wraps Recharts. |
| **Observable Plot** | exploratory dataviz, statistical charts, layered grammar | SVG | ~50 KB gz | minimal (hover, no built-in pan/zoom) | manual; low-level | Brief is statistical/scientific (boxplot, violin, density, area-stacked-stream); D3 power without D3 verbosity |
| **ECharts** | enterprise dashboards, geo-maps, large datasets | Canvas (or SVG via setting) | ~330 KB gz full / ~80 KB gz tree-shaken core | extensive (zoom, brush, datazoom, legend toggle) | weak — requires custom narration for screen readers | Brief is data-heavy (>10k points), needs geo-map / candlestick / sunburst, enterprise-style |
| **ApexCharts** | quick-start dashboards with batteries-included theming | SVG | ~150 KB gz | full (annotations, drilldown) | weak (canvas-like) | Brief is rapid prototyping, theme-first; no React peer dep concerns |
| **uPlot** | very large time-series datasets, perf-critical | Canvas | ~40 KB gz | minimal (hover only) | none built-in | Brief is realtime/streaming data, > 100k points, sub-100ms render budget |

## Decision flow

```
Brief signal → Pick
─────────────────────────────────────────────────
"static infographic, 5 bars" ────────→ Hand-authored SVG (TECH-data-visualization-svg)
"dashboard widget, hover tooltip" ────→ Chart.js 4 (or Recharts if React)
"React + shadcn, line chart" ─────────→ Recharts via shadcn-ui chart.mdx
"custom chord / force / treemap" ─────→ D3.js 7
"realtime time-series, 100k points" ──→ uPlot (Canvas)
"geo-map / sunburst / candlestick" ───→ ECharts
"statistical (boxplot/violin)" ───────→ Observable Plot
"rapid theme-first prototype" ────────→ ApexCharts
```

## Brand-token integration

Every chart library's color array is a function of the brand-tokens
bundle. Map by intent rather than position:

| Brand-token role | Chart-color role |
|---|---|
| `colors.primary` | first/dominant series |
| `colors.accent` | comparison / contrast series |
| `colors.muted` | grid lines, axis tick labels |
| `colors.text` | axis labels, legend text |
| `colors.bg` | chart background |
| `colors.danger` | negative values, error states |

Never let the library's default palette through — every visible color
must trace back to a brand token or a derived (lighten/darken/desaturate)
variant of one. The asset-generator agent flags any chart that ships with
library defaults.

## Accessibility

Charts MUST have:
1. A meaningful `<title>` (chart purpose) and `<desc>` (key takeaway) for
   SVG outputs, OR an `aria-labelledby` referencing nearby text
2. A linked HTML data-table fallback (Chart.js convention: render the
   underlying data into a visually-hidden `<table>` adjacent to the
   chart, link with `aria-describedby`)
3. Color is never the sole channel — pair color with shape (line marker
   variants), pattern (stroke-dasharray), or labels
4. Axis labels are real text, not images of text
5. For Canvas-rendered charts (Chart.js, ECharts, uPlot, ApexCharts),
   the data-table fallback is mandatory — Canvas is opaque to screen
   readers

## Output format

Every chart asset gets:
- The source markup (SVG file, or React component, or Chart.js config
  JSON) saved under `design/charts/<purpose>.<ext>`
- A separate data-table fallback HTML file if the render is Canvas-based
- A README note in the report citing which library was picked and why
- An accessibility-attribute audit excerpt (title/desc/aria + table
  fallback presence)

## What the agent must NOT do

- Pick the library based on what's "popular" — pick on the matrix
- Use a library when the brief is "static, render once, no runtime" —
  hand-author per TECH-data-visualization-svg.md
- Skip the data-table fallback for Canvas charts
- Hard-code colors instead of using brand tokens
- Add a chart library to a project that already uses a different one
  (consult `target_stack` and existing dependencies before adding bytes)
