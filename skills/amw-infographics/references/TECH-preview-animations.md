---
name: TECH-preview-animations
category: infographic-builder
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Per-component animation table](#per-component-animation-table)
- [Stat counter — JS](#stat-counter-js)
- [Bar chart — CSS transition](#bar-chart-css-transition)
- [Feature card stagger — CSS](#feature-card-stagger-css)
- [SVG line draw](#svg-line-draw)
- [The export capture](#the-export-capture)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Preview entrance animations — browser only

## What it does

Adds entrance animations to components during browser preview.
Animations run in the browser only — the export script captures the
post-animation final state, so PNG/PDF output is unaffected.

## When to use

- Always during Interactive Builder mode — makes components feel
  polished.
- Entrance animations: count-ups on stats, bar fills, fade-ups on
  cards, line-draw on charts.

## Per-component animation table

| Component type | Animation | Duration / easing |
|----------------|-----------|-------------------|
| Stat numbers | Count up from 0 to final value | 800ms, ease-out |
| Bar charts | Bars animate from 0 to full width | 600ms, ease-out |
| Progress bars | Fill sweeps left-to-right + leading glow | 600ms, ease-out |
| Feature cards | Stagger-fade: opacity 0→1 + translateY 12px→0, 80ms stagger | 300ms per card |
| Line charts | Path draws left-to-right via stroke-dashoffset | 900ms, ease-in-out |
| Flow diagrams | Nodes fade in sequentially, 100ms stagger | 250ms per node |

## Stat counter — JS

```js
// source: image-generation/create-infographics/SKILL.md
function animateCount(el, target, duration) {
  const start = performance.now();
  const update = (now) => {
    const t = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - t, 3); // ease-out cubic
    el.textContent = Math.round(ease * target).toLocaleString();
    if (t < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}
document.querySelectorAll('[data-count]').forEach(el => {
  animateCount(el, parseInt(el.dataset.count), 800);
});
```

Usage: `<span data-count="74">0</span>`

## Bar chart — CSS transition

```html
<style>
.bar { width: 0; transition: width 600ms ease-out; }
</style>
<script>
requestAnimationFrame(() => {
  document.querySelectorAll('.bar').forEach(b => b.style.width = b.dataset.width);
});
</script>
```

Usage: `<div class="bar" data-width="74%"></div>`

## Feature card stagger — CSS

```html
<style>
.card {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 300ms ease, transform 300ms ease;
}
</style>
<script>
document.querySelectorAll('.card').forEach((card, i) => {
  setTimeout(() => {
    card.style.opacity = 1;
    card.style.transform = 'none';
  }, i * 80);
});
</script>
```

## SVG line draw

```html
<style>
.chart-path {
  stroke-dasharray: var(--path-length);
  stroke-dashoffset: var(--path-length);
  animation: drawLine 900ms ease-in-out forwards;
}
@keyframes drawLine { to { stroke-dashoffset: 0; } }
</style>
<script>
document.querySelectorAll('.chart-path').forEach(path => {
  const len = path.getTotalLength();
  path.style.setProperty('--path-length', len);
});
</script>
```

## The export capture

```python
# source: image-generation/create-infographics/scripts/export.py
page.wait_for_timeout(300)  # buffer for CSS animations to end
```

The 300ms buffer after network idle captures the post-animation
state — static final frame.

## Gotchas

- Use `requestAnimationFrame` before setting target values, so the
  transition fires (not instant).
- `.toLocaleString()` formats numbers with thousands separators.
- Don't use these animations in the final assembled HTML if you
  want truly static output — remove the JS before export.

## Cross-references

- [TECH-interactive-builder-mode](TECH-interactive-builder-mode.md) — the mode these are used in.
- [TECH-preview-server](TECH-preview-server.md) — where these animations play.
- [TECH-export-pipeline](TECH-export-pipeline.md) — how the post-animation state is captured.
- [`../SKILL.md`](../SKILL.md) — parent skill

