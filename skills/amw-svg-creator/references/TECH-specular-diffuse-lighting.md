---
name: TECH-specular-diffuse-lighting
category: svg-lighting
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [Specular — shiny surface](#specular-shiny-surface)
- [Diffuse — matte surface](#diffuse-matte-surface)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# `feSpecularLighting` + `feDiffuseLighting` — physics-based shading

## What it does

SVG filter primitives that compute lighting from a virtual light
source — directional, point, or spot — and produce realistic
highlights (`feSpecularLighting`) or diffuse shading
(`feDiffuseLighting`). Optional, but when used they add photorealism
that hand-crafted gradients can't match.

## Specular — shiny surface

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<filter id="specular" x="-10%" y="-10%" width="120%" height="120%"
  color-interpolation-filters="linearRGB">
  <feSpecularLighting in="SourceAlpha" surfaceScale="5" specularConstant="0.75"
    specularExponent="25" lighting-color="#ffffff" result="specular">
    <fePointLight x="250" y="100" z="300"/>
  </feSpecularLighting>
  <feComposite in="specular" in2="SourceAlpha" operator="in" result="lit"/>
  <feMerge>
    <feMergeNode in="SourceGraphic"/>
    <feMergeNode in="lit"/>
  </feMerge>
</filter>
```

- `specularExponent="20–40"` → glossy
- `specularExponent="5–10"` → matte
- Light position `(x, y, z)` in SVG coords — z is height above surface

## Diffuse — matte surface

```xml
<filter id="diffuse" color-interpolation-filters="linearRGB">
  <feDiffuseLighting in="SourceAlpha" surfaceScale="4" diffuseConstant="1"
    lighting-color="#ffe4c4" result="diffuse">
    <feDistantLight azimuth="225" elevation="45"/>
  </feDiffuseLighting>
  <feComposite in="diffuse" in2="SourceGraphic" operator="in" result="lit"/>
  <feBlend in="SourceGraphic" in2="lit" mode="multiply"/>
</filter>
```

`feDistantLight` is a parallel light (like sunlight) — `azimuth` is
horizontal angle (0 = right, 90 = up), `elevation` is height above
horizon.

## When to use

- Orbs, spheres, glass balls — specular shows reflection hotspots.
- Stones, clay, fabric — diffuse looks like real matte materials.
- UI elements with physical-material aesthetic (e.g. glossy buttons).

## When NOT to use

- Flat iconography / flat logos — physics-based lighting adds 3D
  that clashes with flat design.
- Performance-critical SVGs — these filters are expensive.

## Gotchas

- `surfaceScale` is in SVG units, not physical units. Tune by feel.
- `lighting-color` can be tinted (warm sun, cool moon) — don't
  default to pure white.
- `feComposite operator="in"` restricts the lighting to the alpha
  shape — without it, the light spills outside the object.

## Cross-references

- [TECH-soft-glow-filter](TECH-soft-glow-filter.md) — simpler alternative when you just
  want a halo.
- [TECH-glassmorphism-filter](TECH-glassmorphism-filter.md) — specular + displacement for glass.
- [TECH-five-zone-lighting](TECH-five-zone-lighting.md) — the artistic model for when you
  don't want physics.
- [`../SKILL.md`](../SKILL.md) — parent skill

