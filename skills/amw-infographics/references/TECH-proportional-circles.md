---
name: TECH-proportional-circles
category: infographic-template
source: image-generation/create-infographics/resources/charts.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [The math](#the-math)
- [HTML](#html)
- [CSS — primary shade coloring](#css-primary-shade-coloring)
- [Positioning](#positioning)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Proportional circles — area = value

## What it does

SVG circles where area (NOT radius) represents the value.
`r = sqrt(value) * k` where k scales to fit canvas. Ensures fair
visual comparison of magnitudes.

## When to use

- Comparing 3-6 magnitudes (market caps, audience sizes, TVL).
- Editorial infographics that avoid bar-bias.
- When proportions matter more than exact values.

## The math

```
maxValue   = largest data point
maxRadius  = 90     (or whatever fits canvas)
r_i        = sqrt(value_i / maxValue) * maxRadius
```

Example: BTC=$800B, ETH=$350B, SOL=$85B:
- `r_btc = sqrt(800/800) * 90 = 90`
- `r_eth = sqrt(350/800) * 90 = 59.5`
- `r_sol = sqrt(85/800)  * 90 = 29.3`

## HTML

```html
<!-- source: image-generation/create-infographics/resources/charts.md -->
<svg viewBox="0 0 520 240" class="prop-circles-svg">
  <text x="260" y="16" class="pcircle-title" text-anchor="middle">MARKET CAP COMPARISON ($B)</text>

  <!-- BTC — r=90, centered at (100, 130) -->
  <circle cx="100" cy="130" r="90" class="pcircle c1"/>
  <text x="100" y="125" class="pcircle-label" text-anchor="middle">BTC</text>
  <text x="100" y="141" class="pcircle-value" text-anchor="middle">$800B</text>

  <!-- ETH — r=60 -->
  <circle cx="229" cy="130" r="60" class="pcircle c2"/>
  <text x="229" y="125" class="pcircle-label" text-anchor="middle">ETH</text>
  <text x="229" y="141" class="pcircle-value" text-anchor="middle">$350B</text>

  <!-- SOL — r=29, bottom-aligned -->
  <circle cx="322" cy="175" r="29" class="pcircle c3"/>
  <text x="322" y="172" class="pcircle-label small" text-anchor="middle">SOL</text>
  <text x="322" y="183" class="pcircle-value small" text-anchor="middle">$85B</text>
</svg>
```

## CSS — primary shade coloring

```css
.pcircle { opacity: 0.9; }
.pcircle.c1 { fill: var(--primary); }
.pcircle.c2 { fill: hsl(from var(--primary) h s calc(l - 12%)); opacity: 0.8; }
.pcircle.c3 { fill: hsl(from var(--primary) h s calc(l - 24%)); opacity: 0.75; }
.pcircle.c4 { fill: hsl(from var(--primary) h s calc(l - 34%)); opacity: 0.7; }
.pcircle.c5 { fill: hsl(from var(--primary) h s calc(l - 42%)); opacity: 0.65; }

/* Fallback if CSS relative color syntax unsupported */
/* .c2 { fill: #C4841A; } .c3 { fill: #9A6614; } etc. */

.pcircle-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  fill: var(--bg-primary);
}
.pcircle-value {
  font-family: var(--font-display);
  font-size: 12px;
  font-weight: 700;
  fill: var(--bg-primary);
  font-variant-numeric: tabular-nums;
}
```

## Positioning

Arrange circles left-to-right, largest to smallest. For small
circles (r<30), use bottom-alignment (higher `cy`) for visual
interest rather than baseline-aligning everything.

## Gotchas

- Label readability — labels inside small circles (r<25) need
  smaller fonts (9px). Consider placing below the circle.
- Labels over circles need to contrast — use `fill: var(--bg-primary)`
  (dark text on the colored fill).
- Don't use this for 2 items — a pie chart is clearer for 2-way
  splits.

## Cross-references

- [TECH-chart-selection-guide](TECH-chart-selection-guide.md) — decision tree for chart type.
- [TECH-svg-pie-chart](TECH-svg-pie-chart.md) — alternative for normalized percentages.
- [`../SKILL.md`](../SKILL.md) — parent skill

