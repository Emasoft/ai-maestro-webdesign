---
name: TECH-line-chart
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---

# Line chart — Chart.js with designer theming

## What it does

Chart.js line chart configured to match the dense editorial palette:
dark tooltip background, muted gridlines, Inter-font ticks, primary-
colored line with glow.

## When to use

- Price over time, user growth, revenue trend.
- Any time-series data spanning 3+ points.
- When the trend (direction + shape) is the story.

## HTML

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<div class="chart-container" style="position:relative; height:240px;">
  <canvas id="lineChart"></canvas>
</div>

<script>
const ctx = document.getElementById('lineChart').getContext('2d');
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Q1', 'Q2', 'Q3', 'Q4', "Q1 '26"],
    datasets: [{
      label: 'Price (USD)',
      data: [0.001, 0.0034, 0.0028, 0.0089, 0.012],
      borderColor: '#F5A623',
      backgroundColor: 'rgba(245,166,35,0.08)',
      borderWidth: 2,
      pointBackgroundColor: '#F5A623',
      pointRadius: 4,
      fill: true,
      tension: 0.4,
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#1A1A1A',
        borderColor: 'rgba(255,255,255,0.1)',
        borderWidth: 1,
        titleColor: '#F5A623',
        bodyColor: '#FFFFFF',
      }
    },
    scales: {
      x: {
        grid: { color: 'rgba(255,255,255,0.05)' },
        ticks: { color: '#8B8B8B', font: { family: 'Inter', size: 11 } }
      },
      y: {
        grid: { color: 'rgba(255,255,255,0.05)' },
        ticks: { color: '#8B8B8B', font: { family: 'Inter', size: 11 } }
      }
    }
  }
});
</script>
```

## The signature options

| Option | Value | Why |
|--------|-------|-----|
| `borderColor` | `var(--primary)` (hex) | Brand color for the line |
| `backgroundColor` | `rgba(primary, 0.08)` | Very faint fill under line |
| `borderWidth` | `2` | Visible but not thick |
| `fill: true` | — | Gradient under line |
| `tension: 0.4` | — | Smooth curve, not jagged |
| `legend.display` | `false` | No legend (annotation-first) |
| `grid.color` | `rgba(255,255,255,0.05)` | Almost invisible grid |
| `ticks.color` | `#8B8B8B` | Muted tick labels |

## The container-height trick

```html
<div class="chart-container" style="position:relative; height:240px;">
  <canvas id="lineChart"></canvas>
</div>
```

Chart.js needs an explicit parent height. Without it, the canvas
renders at 0×0 and you get an invisible chart.

## Gotchas

- `maintainAspectRatio: false` is required so the canvas fills the
  container.
- `animation: false` is needed for Playwright screenshot export —
  otherwise the screenshot captures mid-animation.
- Don't use `legend: { display: true }` — use direct labels on the
  chart per the annotation-first principle.

## Cross-references

- `TECH-chart-selection-guide.md` — when to choose line vs other.
- `TECH-radar-chart.md` — other Chart.js type.
- `TECH-annotation-first.md` — why legend is disabled.
- [`../SKILL.md`](../SKILL.md) — parent skill

