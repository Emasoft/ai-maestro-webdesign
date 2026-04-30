---
name: TECH-multi-stop-gradients
category: svg-gradient
source: image-generation/svg-creator/SKILL.md
also-in: image-generation/svg-creator/references/advanced-techniques.md
---

# Multi-stop gradients (4+ stops with hue shifts)

## What it does

Two-stop gradients look flat and digital. Multi-stop gradients (4–8
stops) with intentional hue shifts between stops create the
painterly, reference-grade depth that single-color blends cannot.

## When to use

- Sky gradients (dark → mid → warm → golden hour at horizon).
- Sphere / orb lighting — use radial with `fx="0.3" fy="0.3"` to
  offset toward light source.
- Any surface that needs perceived depth — 4+ stops minimum.

## Sky gradient — 6 stops

```xml
<!-- source: image-generation/svg-creator/SKILL.md -->
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"
  color-interpolation="linearRGB">
  <stop offset="0%"   stop-color="#0f172a"/>
  <stop offset="25%"  stop-color="#1e3a5f"/>
  <stop offset="50%"  stop-color="#3b82f6"/>
  <stop offset="75%"  stop-color="#93c5fd"/>
  <stop offset="90%"  stop-color="#fde68a"/>
  <stop offset="100%" stop-color="#f97316"/>
</linearGradient>
```

Six stops, transitioning through navy → blue → cyan → pale gold →
orange — a sunset over ocean.

## Sphere radial — 5 stops with offset focal

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<radialGradient id="obj" fx="0.35" fy="0.3" cx="45%" cy="45%" r="55%"
  color-interpolation="linearRGB">
  <stop offset="0%"  stop-color="#fff7ed" stop-opacity="0.8"/>  <!-- specular -->
  <stop offset="15%" stop-color="#fb923c"/>                     <!-- light area -->
  <stop offset="50%" stop-color="#ea580c"/>                     <!-- half-tone -->
  <stop offset="85%" stop-color="#7c2d12"/>                     <!-- form shadow -->
  <stop offset="100%" stop-color="#431407"/>                    <!-- deep shadow -->
</radialGradient>
```

## The `color-interpolation="linearRGB"` rule

Default sRGB gradient blending makes mid-range blends look muddier
than expected (darker, desaturated). `linearRGB` interpolation
produces physically accurate transitions — always set it on
gradients and filters.

## Gotchas

- Stops must be in ascending `offset` order — out-of-order stops
  cause renderer-specific undefined behavior.
- Adjacent stops with the same color create hard lines — sometimes
  desired (horizon, band stripes), sometimes a bug.
- Two-stop gradients still have a place — UI surfaces (buttons,
  cards), simple backgrounds. The multi-stop rule is for
  illustrative elements where depth matters.

## Cross-references

- `TECH-five-zone-lighting.md` — the theory behind the 5-stop shape.
- `TECH-paint-order-and-spread-method.md` — `spreadMethod="reflect"`
  for metallic gradients.
- `TECH-colored-shadows.md` — shadow stops should be dark blue /
  purple / teal, not pure black.
- [`../SKILL.md`](../SKILL.md) — parent skill

