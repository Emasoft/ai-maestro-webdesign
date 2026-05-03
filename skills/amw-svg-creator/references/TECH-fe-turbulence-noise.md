---
name: TECH-fe-turbulence-noise
category: svg-noise
source: image-generation/svg-creator/SKILL.md
also-in: image-generation/svg-creator/references/advanced-techniques.md
---
## Table of Contents

- [What it does](#what-it-does)
- [The basic filter](#the-basic-filter)
- [`baseFrequency` — texture scale](#basefrequency-texture-scale)
- [Directional stretch — two-value baseFrequency](#directional-stretch-two-value-basefrequency)
- [`numOctaves` — complexity](#numoctaves-complexity)
- [`type="fractalNoise"` vs `type="turbulence"`](#typefractalnoise-vs-typeturbulence)
- [`stitchTiles="stitch"`](#stitchtilesstitch)
- [`seed` — reproducibility](#seed-reproducibility)
- [Salt & Pepper texture (advanced)](#salt-pepper-texture-advanced)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# `feTurbulence` — noise texture that breaks digital perfection

## What it does

Adds fractal or turbulence noise as an SVG filter primitive. Applied
at low opacity (5-15%) on surfaces and backgrounds, it breaks the
"too clean" look that vector graphics carry by default — the single
biggest cue that separates "illustrated" from "generated".

## The basic filter

```xml
<!-- source: image-generation/svg-creator/SKILL.md -->
<filter id="grain" color-interpolation-filters="linearRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="3"
    stitchTiles="stitch" result="noise"/>
  <feColorMatrix in="noise" type="saturate" values="0" result="mono"/>
  <feBlend in="SourceGraphic" in2="mono" mode="soft-light"/>
</filter>
```

Apply with `filter="url(#grain)"` at 5-15% opacity on a rect covering
the whole scene.

`feBlend in="SourceGraphic" in2="mono"` — `SourceGraphic` is the base
layer; the desaturated noise (`mono`) is blended on top with `soft-light`.
This keeps the source colors while the noise varies the luminosity.
Explicit `result=` names on each step make the chain debuggable and safe
to extend.

## `baseFrequency` — texture scale

```
0.01–0.05  Large cloud-like patterns, terrain
0.05–0.2   Medium organic textures (water, marble, smoke)
0.2–0.5    Coarse grain (stone, sand)
0.5–0.8    Fine grain (paper, film noise) — most useful for texture overlays
0.8–2.0    Very fine static
```

## Directional stretch — two-value baseFrequency

```
baseFrequency="0.02 0.2"    Horizontal grain (wood)
baseFrequency="0.01 0.5"    Strong horizontal stretch (glitch effect)
baseFrequency="0.5 0.01"    Vertical stretch (rain, banding)
```

## `numOctaves` — complexity

- 1 = rough
- **3 = sweet spot**
- 5+ = diminishing returns

## `type="fractalNoise"` vs `type="turbulence"`

- `fractalNoise` — smoother, better for grain / texture overlays
- `turbulence` — more chaotic, better for clouds / smoke / water

## `stitchTiles="stitch"`

Required for pattern fills — ensures seamless tiling at tile
boundaries. Always set when using as a `<pattern>` fill.

## `seed` — reproducibility

Different integer = different random pattern. Change to get variety
across multiple instances; keep stable for reproducibility.

## Salt & Pepper texture (advanced)

Professional technique — two-layer grain: "pepper" darkens via
multiply blend, "salt" brightens via overlay blend. See
[TECH-salt-pepper-texture](TECH-salt-pepper-texture.md).

## Gotchas

- Browsers handle `feTurbulence` differently — Firefox and Chrome
  produce different noise patterns from the same seed. Not a bug;
  test both.
- Heavy noise (opacity > 20%) turns the image into TV static —
  always stay subtle.
- Noise + a drop shadow on the same element can double-blur — disable
  one or reduce both.

## Cross-references

- [TECH-salt-pepper-texture](TECH-salt-pepper-texture.md) — the advanced two-layer grain filter.
  > What it does · The filter · When to use · Subtler salt — use `soft-light` instead of `overlay` · Usage pattern · Gotchas · Cross-references
- [TECH-paper-texture-filter](TECH-paper-texture-filter.md) — subtle paper for editorial looks.
  > What it does · The filter · Parameter walkthrough · When to use · When NOT to use · Usage · Gotchas · Cross-references
- [TECH-glassmorphism-filter](TECH-glassmorphism-filter.md) — noise + displacement combined.
  > What it does · The filter · How it works · When to use · When NOT to use · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

