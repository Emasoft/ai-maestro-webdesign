---
name: TECH-glassmorphism-filter
category: svg-lighting
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The filter](#the-filter)
- [How it works](#how-it-works)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Glassmorphism filter — frosted glass effect

## What it does

Combines `feTurbulence` + `feDisplacementMap` + `feSpecularLighting`
to simulate a frosted-glass surface. Displaces the source pixels by
a turbulent field (the "frosting") and adds a specular highlight for
the light catching the surface.

## The filter

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<filter id="frosted-glass" x="-20%" y="-20%" width="140%" height="140%"
  color-interpolation-filters="linearRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" result="noise"/>
  <feColorMatrix in="noise" type="matrix" result="soft"
    values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.5 0"/>
  <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blurred"/>
  <feDisplacementMap in="blurred" in2="soft" scale="12"
    xChannelSelector="R" yChannelSelector="G" result="distorted"/>
  <feSpecularLighting in="soft" surfaceScale="2" specularConstant="0.6"
    specularExponent="30" lighting-color="#ffffff" result="shine">
    <fePointLight x="200" y="50" z="200"/>
  </feSpecularLighting>
  <feComposite in="shine" in2="SourceAlpha" operator="in" result="glass-shine"/>
  <feMerge>
    <feMergeNode in="distorted"/>
    <feMergeNode in="glass-shine"/>
  </feMerge>
</filter>
```

## How it works

1. Generate fractal noise → `noise`
2. Tone it down to 50% alpha → `soft`
3. Blur the source → `blurred`
4. Displace `blurred` pixels using `soft` as a displacement map →
   `distorted` (the frosting)
5. Add a specular highlight using `soft` as the surface normals
   source → `shine`
6. Clip the shine to the element shape → `glass-shine`
7. Merge distorted + glass-shine

## When to use

- Frosted-glass UI panels (macOS / Windows 11 glassmorphism).
- Ice, crystal, translucent stones.
- Modern infographic callout panels — combined with content behind.

## When NOT to use

- Without content behind — on a solid background, the effect is
  invisible.
- Performance-critical scenes — 3 filter primitives compound GPU cost.

## Gotchas

- `scale="12"` on the displacement is strong — tune down to `6` for
  subtler frosting.
- Requires something behind the element to distort. Glassmorphism on
  a blank canvas shows nothing.
- Can break Safari in some versions — test the browser matrix before
  shipping.

## Cross-references

- [TECH-fe-turbulence-noise](TECH-fe-turbulence-noise.md) — the noise primitive.
  > What it does · The basic filter · `baseFrequency` — texture scale · Directional stretch — two-value baseFrequency · `numOctaves` — complexity · `type="fractalNoise"` vs `type="turbulence"` · `stitchTiles="stitch"` · `seed` — reproducibility · Salt & Pepper texture (advanced) · Gotchas · Cross-references
- [TECH-specular-diffuse-lighting](TECH-specular-diffuse-lighting.md) — the shine primitive.
  > What it does · Specular — shiny surface · Diffuse — matte surface · When to use · When NOT to use · Gotchas · Cross-references
- [TECH-paper-texture-filter](TECH-paper-texture-filter.md) — contrasting "paper" feel.
  > What it does · The filter · Parameter walkthrough · When to use · When NOT to use · Usage · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

