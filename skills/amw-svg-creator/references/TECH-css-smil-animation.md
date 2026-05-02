---
name: TECH-css-smil-animation
category: svg-animation
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The `transform-box` rule](#the-transform-box-rule)
- [Spinner (CSS)](#spinner-css)
- [Line drawing reveal (pathLength + stroke-dasharray)](#line-drawing-reveal-pathlength-stroke-dasharray)
- [Staggered entrance](#staggered-entrance)
- [SMIL animation (works in `<img>` tags)](#smil-animation-works-in-img-tags)
  - [Attribute animation](#attribute-animation)
  - [Transform animation](#transform-animation)
  - [Motion along a path](#motion-along-a-path)
  - [Sequential timing via `begin`](#sequential-timing-via-begin)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# CSS + SMIL animation in SVG

## What it does

Two animation systems usable in SVG:
- **CSS animations** — the familiar keyframes / transition / animation
  stack. Requires SVG to be inline (`<svg>...</svg>` in HTML).
- **SMIL** — native SVG `<animate>`, `<animateTransform>`,
  `<animateMotion>` tags. Works in `<img src="file.svg">` where CSS
  and JS can't reach.

## The `transform-box` rule

ALWAYS pair CSS SVG animations with:

```css
transform-box: fill-box;
transform-origin: center;
```

Without these, rotation and scale animate around the SVG origin
(typically top-left), not the element's center.

## Spinner (CSS)

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<style>
  .spin {
    fill: none; stroke: #3b82f6; stroke-width: 4;
    stroke-linecap: round; stroke-dasharray: 80 120;
    animation: rotate 1s linear infinite;
    transform-box: fill-box; transform-origin: center;
  }
  @keyframes rotate { to { transform: rotate(360deg); } }
</style>
```

## Line drawing reveal (pathLength + stroke-dasharray)

```xml
<style>
  .draw {
    stroke-dasharray: 1; stroke-dashoffset: 1;
    animation: reveal 2s ease forwards;
    transform-box: fill-box;
  }
  @keyframes reveal { to { stroke-dashoffset: 0; } }
</style>
<path pathLength="1" class="draw" d="..." fill="none" stroke="#333" stroke-width="2"/>
```

`pathLength="1"` normalizes the path — now `stroke-dasharray: 1` is
the full length regardless of actual path length.

## Staggered entrance

```css
.item {
  opacity: 0; transform: translateY(10px);
  animation: fadeUp 0.5s ease forwards;
  transform-box: fill-box; transform-origin: center;
}
.item:nth-child(1) { animation-delay: 0s; }
.item:nth-child(2) { animation-delay: 0.15s; }
.item:nth-child(3) { animation-delay: 0.3s; }
@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }
```

## SMIL animation (works in `<img>` tags)

SMIL has 96%+ browser support and is the only animation option when
the SVG is embedded as `<img src>` or CSS `background-image`.

### Attribute animation

```xml
<circle cx="50" cy="50" r="20" fill="#3b82f6">
  <animate attributeName="r" values="20;25;20" dur="2s" repeatCount="indefinite"/>
</circle>
```

### Transform animation

```xml
<rect x="-10" y="-10" width="20" height="20" fill="#ef4444">
  <animateTransform attributeName="transform" type="rotate"
    values="0 50 50;360 50 50" dur="3s" repeatCount="indefinite"/>
</rect>
```

### Motion along a path

```xml
<circle r="5" fill="#3b82f6">
  <animateMotion dur="4s" repeatCount="indefinite" rotate="auto">
    <mpath href="#motion-path"/>
  </animateMotion>
</circle>
<path id="motion-path" d="M50,200 Q200,50 350,200" fill="none"/>
```

### Sequential timing via `begin`

```xml
<circle cx="50" cy="50" r="0" fill="#3b82f6">
  <animate id="grow" attributeName="r" from="0" to="20" dur="0.5s" fill="freeze"/>
</circle>
<circle cx="100" cy="50" r="0" fill="#ef4444">
  <animate attributeName="r" from="0" to="20" dur="0.5s" fill="freeze"
    begin="grow.end+0.2s"/>
</circle>
```

`begin="grow.end+0.2s"` — this animation starts 200ms after
`#grow` finishes.

## Gotchas

- CSS animations don't work when SVG is `<img src>` — switch to SMIL.
- SMIL doesn't work in IE (obsolete) — browsers that matter support it.
- Use `fill="freeze"` on one-shot SMIL animations so they hold their
  end state.
- Animations must respect `prefers-reduced-motion` — see
  [TECH-reduced-motion](TECH-reduced-motion.md).

## Cross-references

- [TECH-reduced-motion](TECH-reduced-motion.md) — mandatory accessibility override.
- [TECH-paint-order-and-spread-method](TECH-paint-order-and-spread-method.md) — `pathLength="1"` is key
  for line-draw.
- [TECH-atmospheric-effects](TECH-atmospheric-effects.md) — stars, rain use these patterns.
- [`../SKILL.md`](../SKILL.md) — parent skill

