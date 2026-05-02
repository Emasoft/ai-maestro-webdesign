---
name: TECH-paint-order-and-spread-method
category: svg-gradient
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [`paint-order="stroke fill"`](#paint-orderstroke-fill)
- [`spreadMethod` on gradients](#spreadmethod-on-gradients)
  - [Example — brushed metal with `reflect`](#example-brushed-metal-with-reflect)
- [`vector-effect="non-scaling-stroke"`](#vector-effectnon-scaling-stroke)
- [`pathLength="1"`](#pathlength1)
- [`gradientTransform`](#gradienttransform)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# `paint-order` and `spreadMethod` — power features

## What it does

Two underused SVG attributes that unlock sophisticated effects:
- **`paint-order`** — controls whether stroke draws before or after
  fill.
- **`spreadMethod`** — controls gradient behavior beyond boundaries.

## `paint-order="stroke fill"`

Default paint order is fill → stroke → markers. Reversing to
`stroke fill` draws the stroke BEHIND the fill — creates outlined
text and halo effects without duplicate elements.

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<text x="50" y="50" font-size="48" fill="white"
  stroke="#000" stroke-width="8" paint-order="stroke fill">
  Hello
</text>
```

Produces white text with a black outline where the outline doesn't
bleed into the characters.

## `spreadMethod` on gradients

Three values, controls what happens beyond the gradient's `0%` /
`100%` stops:

```
spreadMethod="pad"     (default) Extends the last color
spreadMethod="reflect" Mirrors the gradient — great for metallic surfaces
spreadMethod="repeat"  Tiles the gradient — stripe patterns
```

### Example — brushed metal with `reflect`

```xml
<linearGradient id="brush" x1="0" y1="0" x2="0" y2="0.1"
  spreadMethod="reflect">
  <stop offset="0%" stop-color="#6b6b6b"/>
  <stop offset="100%" stop-color="#d4d4d4"/>
</linearGradient>
```

The small gradient `0.1` tall repeats via reflection, producing the
banded "brushed" look.

## `vector-effect="non-scaling-stroke"`

Keeps stroke width constant regardless of element transforms or
zoom. Essential for technical illustrations and icons that render at
multiple scales.

## `pathLength="1"`

Normalizes path length for dash calculations. With this set,
`stroke-dasharray="0.5 0.5"` = 50% dashed regardless of the path's
actual length — simplifies line-drawing animations dramatically.

```xml
<path pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"
  class="draw" d="..." fill="none" stroke="#333" stroke-width="2"/>
```

## `gradientTransform`

Apply transforms to gradient coordinate systems:

```xml
<linearGradient id="angled" gradientTransform="rotate(30)">
```

No need to recalculate `x1`/`y1`/`x2`/`y2` — just rotate the
gradient.

## Gotchas

- `paint-order` isn't universally supported — test Safari and older
  mobile browsers.
- `spreadMethod="reflect"` on a gradient that's the full shape size
  does nothing (no area beyond 100% to reflect into).
- `non-scaling-stroke` interacts weirdly with `vector-effect` chains
  — test at the scales you care about.

## Cross-references

- [TECH-multi-stop-gradients](TECH-multi-stop-gradients.md) — gradients that benefit from
  `spreadMethod`.
- [TECH-material-simulation](TECH-material-simulation.md) — `reflect` is essential for metals.
- [TECH-css-smil-animation](TECH-css-smil-animation.md) — `pathLength="1"` is the keystone
  for line-draw animations.
- [`../SKILL.md`](../SKILL.md) — parent skill

