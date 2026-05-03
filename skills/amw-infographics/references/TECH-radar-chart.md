---
name: TECH-radar-chart
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [HTML](#html)
- [The signature options](#the-signature-options)
- [Multi-character comparison — overlay datasets](#multi-character-comparison-overlay-datasets)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Radar chart — Chart.js for game stats + multi-axis comparison

## What it does

Chart.js radar (spider) chart with designer theming. 4-8 axes
showing multi-dimensional comparisons — game character stats,
feature comparisons, capability assessments.

## When to use

- Game character stats (Attack / Defense / Speed / Magic / Stamina / Luck).
- Feature comparison matrices.
- Personality / capability assessments.
- Multi-axis scoring where a single value per axis matters.

## HTML

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<div class="chart-container"
     style="position:relative; height:280px; max-width: 320px; margin: 0 auto;">
  <canvas id="radarChart"></canvas>
</div>

<script>
new Chart(document.getElementById('radarChart'), {
  type: 'radar',
  data: {
    labels: ['ATTACK', 'DEFENSE', 'SPEED', 'MAGIC', 'STAMINA', 'LUCK'],
    datasets: [{
      data: [85, 72, 91, 60, 78, 55],
      borderColor: '#00E5A0',
      backgroundColor: 'rgba(0,229,160,0.12)',
      borderWidth: 2,
      pointBackgroundColor: '#00E5A0',
      pointRadius: 4,
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      r: {
        min: 0, max: 100,
        grid: { color: 'rgba(255,255,255,0.08)' },
        angleLines: { color: 'rgba(255,255,255,0.08)' },
        pointLabels: {
          color: '#8B8B8B',
          font: { family: 'Inter', size: 10 }
        },
        ticks: { display: false }
      }
    }
  }
});
</script>
```

## The signature options

| Option | Value | Why |
|--------|-------|-----|
| `min / max` | `0 / 100` | Consistent scale across characters |
| `grid.color` | `rgba(255,255,255,0.08)` | Barely visible web lines |
| `angleLines.color` | same | Same subtle feel for spokes |
| `ticks.display` | `false` | No numeric ticks — axis labels suffice |
| `pointLabels` | small muted text | Axis labels (attack, defense) |
| `borderColor` | Brand accent | The polygon outline |
| `backgroundColor` | low-alpha accent | Filled polygon area |

## Multi-character comparison — overlay datasets

```js
datasets: [
  {
    label: 'Character A',
    data: [85, 72, 91, 60, 78, 55],
    borderColor: '#00E5A0',
    backgroundColor: 'rgba(0,229,160,0.12)',
  },
  {
    label: 'Character B',
    data: [45, 95, 50, 85, 70, 80],
    borderColor: '#A764F6',
    backgroundColor: 'rgba(167,100,246,0.12)',
  }
]
```

Two different brand accents — teal and violet — make the comparison
readable.

## Gotchas

- Radar charts mislead if axes are ordered arbitrarily. Group
  related axes next to each other (Attack + Speed together, Defense +
  Stamina together).
- 4-8 axes optimal. Fewer feels incomplete; more gets cramped.
- Zero values on one axis collapse the polygon toward the center —
  can look like a bug. Consider setting `min` above 0 if some data
  would be 0.

## Cross-references

- [TECH-chart-selection-guide](TECH-chart-selection-guide.md) — when radar is the right choice.
  > What it does · The decision table · The rule · Chart.js when yes · Chart.js loading · The canvas size trick · Gotchas · Cross-references
- [TECH-game-overview-playbook](TECH-game-overview-playbook.md) — where radar charts shine.
  > What it does · When to use · Color system · Typography — two sub-variants · Standard game · Pixel / retro game · Standard component prevalence (across 25 pieces) · Visual properties · Signature layout pattern · Character card grid (signature pattern) · Light-mode sub-variant · CSS variables (standard) · CSS variables (pixel) · Reference template · Gotchas · Cross-references
- [TECH-line-chart](TECH-line-chart.md) — the other Chart.js type in the library.
  > What it does · When to use · HTML · The signature options · The container-height trick · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

