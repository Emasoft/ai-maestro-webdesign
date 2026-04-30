---
name: TECH-annotated-bar-chart
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---

# Annotated bar chart — SVG with callout + benchmark

## What it does

SVG horizontal bar chart with one highlighted hero bar, a callout
annotation line pointing to it, and a benchmark/threshold line
crossing the chart. No Chart.js dependency.

## When to use

- Highlighting a single outlier or hero bar in a ranked dataset.
- Showing "above/below average" stories with a benchmark line.
- Editorial bar charts where annotations live ON the chart, not
  in a separate caption.

## HTML (excerpt — see source for full)

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<svg viewBox="0 0 500 300" class="annotated-bar-svg">
  <text x="120" y="18" class="abar-title">STAKING APY BY PROTOCOL</text>

  <!-- Benchmark line at 45% of 340 = x=273 -->
  <line x1="273" y1="22" x2="273" y2="268" class="benchmark-line"/>
  <text x="276" y="30" class="benchmark-label">AVG 18%</text>

  <!-- Hero bar: Lido 72% → width=245 -->
  <text x="112" y="50" class="abar-label hero-label">LIDO</text>
  <rect x="120" y="38" width="245" height="20" rx="3" class="abar-fill hero-fill"/>
  <text x="370" y="52" class="abar-value hero-value">72%</text>

  <!-- Callout for hero: line + box + text -->
  <line x1="365" y1="48" x2="400" y2="70" class="callout-line"/>
  <rect x="398" y="60" width="90" height="28" rx="4" class="callout-box"/>
  <text x="443" y="71" class="callout-text" text-anchor="middle">TOP APY</text>
  <text x="443" y="82" class="callout-subtext" text-anchor="middle">+4× AVERAGE</text>

  <!-- Regular bars (no callout) -->
  <text x="112" y="90" class="abar-label">ROCKET POOL</text>
  <rect x="120" y="78" width="153" height="20" rx="3" class="abar-fill"/>
  <text x="278" y="92" class="abar-value">45%</text>
  <!-- ... more bars -->
</svg>
```

## CSS

```css
.abar-fill { fill: rgba(255,255,255,0.10); }
.abar-fill.hero-fill {
  fill: var(--primary);
  filter: drop-shadow(0 0 6px rgba(var(--primary-rgb), 0.5));
}

.abar-value { font-family: var(--font-display); font-size: 11px; fill: var(--text-secondary); }
.abar-value.hero-value {
  fill: var(--primary);
  font-weight: 700;
  font-size: 13px;
}

.benchmark-line {
  stroke: rgba(255,255,255,0.2);
  stroke-width: 1;
  stroke-dasharray: 4 3;
}
.benchmark-label {
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  fill: var(--muted);
}

.callout-line { stroke: var(--primary); stroke-width: 1; opacity: 0.5; }
.callout-box {
  fill: rgba(var(--primary-rgb), 0.12);
  stroke: var(--primary);
  stroke-width: 0.75;
  stroke-opacity: 0.4;
}
.callout-text {
  font-family: var(--font-display);
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  fill: var(--primary);
}
```

## The hero bar signature

- Hero bar: `fill: var(--primary)` + drop shadow glow.
- Other bars: `fill: rgba(255,255,255,0.10)` — faded.
- Hero label: `fill: var(--text-primary)` + font-weight 600.
- Hero value: larger font + colored in primary.

## Gotchas

- Benchmark line goes BEHIND bars (lower z). Draw it first in SVG
  source order.
- Callout box + line should point from outside the chart area —
  don't put the callout inside the bars.
- Bars should have `rx="3"` rounded caps — matches the dense-table
  rounded-corner signature.

## Cross-references

- `TECH-svg-pie-chart.md` — alternative chart for proportions.
- `TECH-annotation-first.md` — the "labels on chart" principle this
  implements.
- `TECH-slope-chart.md` — for before/after stories.
- [`../SKILL.md`](../SKILL.md) — parent skill

