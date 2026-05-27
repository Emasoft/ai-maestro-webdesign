---
name: TECH-data-viz-templates
category: infographic-template
source: web-content-designer-main/dashboard-example.html + infographic-structure.md + one-page-structure.md + Tufte small-multiples (T-145..T-148 synthesis)
also-in:
---

## Table of Contents

- [What this is](#what-this-is)
- [Template 1 — KPI dashboard header](#template-1--kpi-dashboard-header)
- [Template 2 — Time-series + breakdown](#template-2--time-series--breakdown)
- [Template 3 — Comparison matrix](#template-3--comparison-matrix)
- [Template 4 — Conversion funnel](#template-4--conversion-funnel)
- [Template 5 — Cohort retention](#template-5--cohort-retention)
- [Template 6 — Risk / progress dashboard](#template-6--risk--progress-dashboard)
- [Template 7 — Geographic distribution panel](#template-7--geographic-distribution-panel)
- [Cross-references](#cross-references)

# Data-viz templates — reusable panel layouts for dashboards and infographics

## What this is

Seven reusable templates that compose into a dashboard or infographic. Each is a self-contained HTML+CSS+chart panel. Pick the templates that match your content shape; arrange them in the layout structure that matches the content type (`amw-design-principles/starter-components/` for chrome, `web-content-designer` structures for the overall flow).

Every template uses CSS variables (no Tailwind color utilities), hairline borders over shadows, monochromatic charts, eyebrow labels before headings — the consulting-deck rules from `TECH-chart-variants.md`.

## Template 1 — KPI dashboard header

A 4-card row introducing a report. Each card: eyebrow → number → label.

```html
<div class="kpi-row grid grid-cols-2 lg:grid-cols-4 gap-4">
  <div class="kpi-card">
    <p class="kpi-eyebrow">METRIC 01</p>
    <p class="kpi-number">$29.6B</p>
    <p class="kpi-label">Annual revenue, FY25</p>
  </div>
  <div class="kpi-card">
    <p class="kpi-eyebrow">METRIC 02</p>
    <p class="kpi-number">+145%</p>
    <p class="kpi-label">YoY growth in core segment</p>
  </div>
  <!-- 4 cards total -->
</div>

<style>
.kpi-card {
  padding: 1rem 1.1rem;
  border: 1px solid var(--border);
  border-top: 3px solid var(--primary);
  background: #fff;
}
.kpi-eyebrow {
  font-size: 0.58rem;
  font-weight: 800;
  color: var(--text-light);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.3rem;
}
.kpi-number {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--primary);
  line-height: 1;
  letter-spacing: -0.02em;
}
.kpi-label {
  font-size: 0.68rem;
  color: var(--text-light);
  margin-top: 0.35rem;
  line-height: 1.35;
  font-weight: 600;
}
</style>
```

**Rules:** 4 cards exactly (3 = thin, 5+ = crowded). Number max 6 chars. Label max 8 words on 2 lines. Never icons in this template (icons would compete with the number).

## Template 2 — Time-series + breakdown

A 60/40 split: left = main line chart over time; right = stacked-bar or donut breakdown of the latest period.

```html
<div class="grid grid-cols-1 lg:grid-cols-5 gap-6 my-10">
  <div class="lg:col-span-3 chart-box">
    <p class="card-title">FIGURE 1 — Revenue, FY20 to FY25</p>
    <div class="chart-container"><canvas id="revLine"></canvas></div>
  </div>
  <div class="lg:col-span-2 chart-box">
    <p class="card-title">FY25 BREAKDOWN BY SEGMENT</p>
    <div class="chart-container"><canvas id="segDonut"></canvas></div>
  </div>
</div>
```

**When to use:** narrative report sections where "what is the trend AND what is the current composition" matter together. Avoid stacking the breakdown chart below the line — side-by-side is the consulting-deck idiom.

## Template 3 — Comparison matrix

For "Option A vs Option B (vs Option C)" decisions. A table with row labels in `--primary` weight and rows separated by hairline borders.

```html
<table class="comparison-table">
  <thead>
    <tr>
      <th>Dimension</th>
      <th>Option A — Build</th>
      <th>Option B — Buy</th>
      <th>Option C — Partner</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="row-label">Upfront cost</td>
      <td>$2.5M</td>
      <td>$8.0M</td>
      <td>$0.5M + 8% revshare</td>
    </tr>
    <tr>
      <td class="row-label">Time to market</td>
      <td>12 mo</td>
      <td>3 mo</td>
      <td>6 mo</td>
    </tr>
    <tr>
      <td class="row-label">Strategic control</td>
      <td>High</td>
      <td>Low</td>
      <td>Medium</td>
    </tr>
  </tbody>
</table>
```

**Rules:** 3–5 columns max. 4–8 rows. Best option per row can be bolded — but never colored cells (that's a heatmap, different template). Last row is often the recommendation.

## Template 4 — Conversion funnel

Multi-stage drop-off. Use stepped horizontal bars, NOT the trapezoid "funnel" cliche (which exaggerates proportion).

```html
<div class="funnel">
  <div class="funnel-row">
    <span class="funnel-label">01 · Visitors</span>
    <div class="funnel-bar" style="width: 100%;">12,400</div>
    <span class="funnel-rate">—</span>
  </div>
  <div class="funnel-row">
    <span class="funnel-label">02 · Sign-up start</span>
    <div class="funnel-bar" style="width: 38%;">4,712</div>
    <span class="funnel-rate">38%</span>
  </div>
  <div class="funnel-row">
    <span class="funnel-label">03 · Email verified</span>
    <div class="funnel-bar" style="width: 22%;">2,728</div>
    <span class="funnel-rate">22%</span>
  </div>
  <div class="funnel-row">
    <span class="funnel-label">04 · First action</span>
    <div class="funnel-bar" style="width: 14%;">1,736</div>
    <span class="funnel-rate">14%</span>
  </div>
  <div class="funnel-row">
    <span class="funnel-label">05 · Activated</span>
    <div class="funnel-bar" style="width: 9%;">1,116</div>
    <span class="funnel-rate">9%</span>
  </div>
</div>

<style>
.funnel { display: grid; gap: 0.5rem; }
.funnel-row { display: grid; grid-template-columns: 180px 1fr 60px; gap: 1rem; align-items: center; font-size: 0.78rem; }
.funnel-label { color: var(--text-mid); font-weight: 600; }
.funnel-bar { background: var(--primary); color: #fff; padding: 0.5rem 0.75rem; font-weight: 700; }
.funnel-rate { color: var(--accent); font-weight: 800; text-align: right; }
</style>
```

**Rules:** 4–6 stages. Show absolute number + rate per stage. Highlight the biggest drop-off with a callout. Never use a trapezoid SVG (geometry lies about ratios).

## Template 5 — Cohort retention

Triangular heatmap. Rows = sign-up cohort (week or month); columns = weeks since sign-up; cell shade = retention %.

```html
<div class="cohort-grid">
  <!-- Header row: week offsets -->
  <div></div>
  <div class="cohort-h">W0</div>
  <div class="cohort-h">W1</div>
  <div class="cohort-h">W4</div>
  <div class="cohort-h">W8</div>
  <div class="cohort-h">W12</div>

  <!-- Data rows: one per cohort -->
  <div class="cohort-label">Jan</div>
  <div class="cohort-cell" style="background: rgba(5,28,44,1.0); color: #fff;">100</div>
  <div class="cohort-cell" style="background: rgba(5,28,44,0.6);">58</div>
  <div class="cohort-cell" style="background: rgba(5,28,44,0.35);">31</div>
  <div class="cohort-cell" style="background: rgba(5,28,44,0.22);">22</div>
  <div class="cohort-cell" style="background: rgba(5,28,44,0.18);">18</div>

  <div class="cohort-label">Feb</div>
  <div class="cohort-cell" style="background: rgba(5,28,44,1.0); color: #fff;">100</div>
  <div class="cohort-cell" style="background: rgba(5,28,44,0.62);">62</div>
  <div class="cohort-cell" style="background: rgba(5,28,44,0.38);">36</div>
  <div class="cohort-cell" style="background: rgba(5,28,44,0.26);">25</div>
  <div class="cohort-cell" style="background: rgba(5,28,44,0.0);">—</div>

  <!-- repeat per cohort -->
</div>

<style>
.cohort-grid { display: grid; grid-template-columns: 70px repeat(5, 1fr); gap: 2px; font-size: 0.72rem; }
.cohort-h { padding: 0.4rem; text-align: center; font-weight: 800; color: var(--text-light); text-transform: uppercase; letter-spacing: 0.05em; }
.cohort-label { padding: 0.5rem; font-weight: 700; color: var(--primary); }
.cohort-cell { padding: 0.5rem; text-align: center; font-weight: 700; color: var(--text); }
</style>
```

**Rules:** monochromatic `--primary` tints only (no rainbow). Triangular — cells with no data yet are blank, not zero-colored. Use for retention, churn, engagement-by-cohort.

## Template 6 — Risk / progress dashboard

Stacked horizontal progress bars for risk-meters or completion-meters. Use sparingly — too many bars stacked feels like a settings page.

```html
<div class="risk-stack">
  <div class="risk-item">
    <div class="risk-header">
      <span class="risk-label">Regulatory exposure</span>
      <span class="risk-value">85%</span>
    </div>
    <div class="risk-track">
      <div class="risk-fill" style="width: 85%; background: #6b1220;"></div>
    </div>
  </div>
  <div class="risk-item">
    <div class="risk-header">
      <span class="risk-label">Supply chain stability</span>
      <span class="risk-value">42%</span>
    </div>
    <div class="risk-track">
      <div class="risk-fill" style="width: 42%; background: var(--primary);"></div>
    </div>
  </div>
  <!-- 3–6 items max -->
</div>

<style>
.risk-item { margin-bottom: 1rem; }
.risk-header { display: flex; justify-content: space-between; font-size: 0.75rem; margin-bottom: 0.4rem; }
.risk-label { font-weight: 700; color: var(--text-mid); text-transform: uppercase; letter-spacing: 0.03em; }
.risk-value { font-weight: 800; color: var(--primary); }
.risk-track { height: 4px; background: var(--border); overflow: hidden; }
.risk-fill { height: 100%; }
</style>
```

**Rules:** track height max 4px (thin). Use `#6b1220` muted oxblood for risk/downside, `--primary` for neutral, `--accent` for highlight. Never alarm red. 3–6 bars per panel.

## Template 7 — Geographic distribution panel

When the story is regional, prefer a small symbol map or a ranked horizontal bar over a choropleth. Choropleths exaggerate large rural regions.

```html
<div class="geo-panel grid grid-cols-1 md:grid-cols-2 gap-6">
  <div>
    <p class="card-title">TOP 10 REGIONS BY METRIC</p>
    <!-- Horizontal bar chart, sorted desc -->
    <div class="chart-container"><canvas id="geoBar"></canvas></div>
  </div>
  <div>
    <p class="card-title">REGIONAL HEATMAP</p>
    <!-- SVG choropleth OR symbol map; monochromatic --primary tints only -->
    <div class="map-container"><svg viewBox="0 0 800 400"><!-- map paths --></svg></div>
  </div>
</div>
```

**Rules:** pair the map with a ranked bar — the map gives spatial pattern; the bar gives precise comparison. Map alone is rarely enough.

## Cross-references

- `TECH-chart-variants.md` — choose the chart type before picking a template
- `TECH-dashboard-archetypes.md` — pick the dashboard archetype before composing templates
- `TECH-annotated-bar-chart.md`, `TECH-bar-chart-css.md` — sibling per-chart templates
- `../skills/amw-design-principles/starter-components/` — page chrome that wraps these panels
