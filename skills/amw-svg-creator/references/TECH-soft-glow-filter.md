---
name: TECH-soft-glow-filter
category: svg-lighting
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The basic filter](#the-basic-filter)
- [Colored glow variant](#colored-glow-variant)
- [`stdDeviation` tuning](#stddeviation-tuning)
- [Filter region](#filter-region)
- [When to use](#when-to-use)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Soft glow filter

## What it does

A subtle bloom effect — blurs the source and merges it under the
original. Creates a halo around luminous elements (stars, neon
signs, glowing eyes, fire).

## The basic filter

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"
  color-interpolation-filters="linearRGB">
  <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
```

The blur becomes a colored halo; the original draws on top.

## Colored glow variant

To tint the halo a specific color, add an `feColorMatrix` that
remaps the RGB channels before the merge:

```xml
<filter id="glow-amber" x="-30%" y="-30%" width="160%" height="160%"
  color-interpolation-filters="linearRGB">
  <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur"/>
  <feColorMatrix in="blur" type="matrix" result="tinted"
    values="0 0 0 0 1
            0 0 0 0 0.6
            0 0 0 0 0.1
            0 0 0 1 0"/>
  <feMerge>
    <feMergeNode in="tinted"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
```

Rows 1-3 of the matrix output a fixed RGB (pure amber here). Row 4
preserves alpha.

## `stdDeviation` tuning

- 4 — tight glow (eye highlight)
- 8 — standard (neon sign) (default)
- 15+ — wide ambient glow (full-moon halo)

## Filter region

`x="-30%" y="-30%" width="160%" height="160%"` — must exceed element
bounds by at least `stdDeviation` × 2 in each direction, or the halo
gets clipped.

## When to use

- Stars with twinkle animation.
- Neon signs, UI indicators, LED displays.
- Fire, magic spell effects, glowing eyes.
- Infographic hero numbers (at low intensity — `stdDeviation="4"`).

## Gotchas

- Glow + grain textures compete — pick one or reduce both.
- Browser SVG renderers disagree on blur spread when
  `color-interpolation-filters` isn't set. Always set it.
- Adjacent glowing elements at high intensity create one blended
  halo that erases the individual outlines. Separate them in space
  or reduce `stdDeviation`.

## Cross-references

- [TECH-drop-shadow-filter](TECH-drop-shadow-filter.md) — the negative cousin (shadow instead of glow).
  > What it does · Drop shadow (standard) · Contact shadow (tight, right under object) · Cast shadow (large, soft, far) · Inner shadow (not a drop shadow — opposite direction) · The obligatory `color-interpolation-filters="linearRGB"` · Gotchas · Cross-references
- [TECH-colored-shadows](TECH-colored-shadows.md) — color theory for tinted glows.
  > What it does · The palette · Where the color goes · Drop-shadow filter with colored shadow · Opacity rules · Gotchas · Cross-references
- [TECH-specular-diffuse-lighting](TECH-specular-diffuse-lighting.md) — physics-based alternative.
  > What it does · Specular — shiny surface · Diffuse — matte surface · When to use · When NOT to use · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
