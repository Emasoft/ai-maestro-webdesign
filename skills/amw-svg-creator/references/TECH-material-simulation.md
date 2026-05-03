---
name: TECH-material-simulation
category: svg-gradient
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [Metal (steel / chrome)](#metal-steel-chrome)
- [Gold](#gold)
- [Glass / transparent](#glass-transparent)
- [Wood](#wood)
- [Water](#water)
- [Stone / rock](#stone-rock)
- [Fabric / cloth](#fabric-cloth)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Material simulation — metal, gold, glass, wood, water, stone, fabric

## What it does

Recipes for rendering specific physical materials in SVG — combining
the right gradient stops, filter chains, and layer composition.

## Metal (steel / chrome)

High-contrast multi-stop gradient with sharp transitions. Add
`spreadMethod="reflect"` for brushed-metal repeat:

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"
  color-interpolation="linearRGB">
  <stop offset="0%"   stop-color="#e8e8e8"/>
  <stop offset="20%"  stop-color="#6b6b6b"/>
  <stop offset="35%"  stop-color="#d4d4d4"/>
  <stop offset="50%"  stop-color="#888"/>
  <stop offset="65%"  stop-color="#e0e0e0"/>
  <stop offset="80%"  stop-color="#555"/>
  <stop offset="100%" stop-color="#b0b0b0"/>
</linearGradient>
```

Combine with:
- Thin near-white specular lines along edges
- Specular filter (see [TECH-specular-diffuse-lighting](TECH-specular-diffuse-lighting.md))
  > What it does · Specular — shiny surface · Diffuse — matte surface · When to use · When NOT to use · Gotchas · Cross-references
- Reflected environment colors at 15-30% opacity

## Gold

Same structure, warm tones:
- Highlights: `#fff7d1`, `#ffd700`, `#ffec99`
- Base: `#daa520`, `#b8860b`
- Shadows: `#8b6914`, `#6b4c0a`, `#4a3508`

## Glass / transparent

Layer composition, not a single gradient:

```xml
<!-- Base shape with low opacity -->
<rect rx="12" width="200" height="300" fill="#88ccff" opacity="0.12"/>
<!-- Highlight streak (angled linear gradient) -->
<rect rx="8" x="15" y="8" width="50" height="240"
  fill="url(#glass-highlight)" opacity="0.5"/>
<!-- Edge darkening (dark border) -->
<rect rx="12" width="200" height="300" fill="none" stroke="#1e3a5f"
  stroke-width="1" opacity="0.3"/>
<!-- Reflected light on bottom edge -->
<ellipse cx="100" cy="285" rx="70" ry="10" fill="white" opacity="0.1"/>
```

## Wood

Two-value baseFrequency creates directional grain:

```xml
<filter id="wood-grain" color-interpolation-filters="linearRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.02 0.2" numOctaves="5" result="grain"/>
  <feColorMatrix in="grain" type="matrix" result="brown"
    values="0.4 0.3 0.1 0 0.3
            0.3 0.2 0.1 0 0.15
            0.1 0.1 0.05 0 0.05
            0 0 0 1 0"/>
</filter>
```

`baseFrequency="0.02 0.2"` — horizontal stretch makes the grain
directional.

## Water

- Multiple semi-transparent blue layers at opacity 0.2–0.5
- Thin concentric elliptical ripple lines (white, opacity 0.3)
- Vertically flipped desaturated reflections at 30-50% opacity
- `feTurbulence` + `feDisplacementMap` for wavy distortion
- Gradient: dark blue deep → mid cyan → light blue surface with 5+ stops

## Stone / rock

- Base gray-brown gradient
- Heavy noise: `baseFrequency="0.35"`, multiply blend, opacity 0.6
- Irregular polygon shapes
- Thin dark crack lines with slight organic curves

## Fabric / cloth

- Alternating light-dark-light gradient bands simulate folds
- Very fine noise: `baseFrequency="0.8"`, soft-light blend
- Curved shadow shapes following drape direction

## Gotchas

- Materials look stupid at the wrong scale — wood grain on a
  2000×2000px canvas needs different `baseFrequency` than on a
  100×100 tile.
- Glass requires something behind — on solid black it's invisible.
- Don't combine more than 2 material effects on one element — they
  cancel each other out.

## Cross-references

- [TECH-multi-stop-gradients](TECH-multi-stop-gradients.md) — the gradient primitive.
  > What it does · When to use · Sky gradient — 6 stops · Sphere radial — 5 stops with offset focal · The `color-interpolation="linearRGB"` rule · Gotchas · Cross-references
- [TECH-fe-turbulence-noise](TECH-fe-turbulence-noise.md) — the noise primitive.
  > What it does · The basic filter · `baseFrequency` — texture scale · Directional stretch — two-value baseFrequency · `numOctaves` — complexity · `type="fractalNoise"` vs `type="turbulence"` · `stitchTiles="stitch"` · `seed` — reproducibility · Salt & Pepper texture (advanced) · Gotchas · Cross-references
- [TECH-specular-diffuse-lighting](TECH-specular-diffuse-lighting.md) — physics-based light for metals.
  > What it does · Specular — shiny surface · Diffuse — matte surface · When to use · When NOT to use · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

