---
name: TECH-five-zone-lighting
category: svg-lighting
source: image-generation/svg-creator/SKILL.md
also-in: image-generation/svg-creator/references/advanced-techniques.md
---
## Table of Contents

- [What it does](#what-it-does)
- [The five zones](#the-five-zones)
- [Implementation — radial gradient + overlays](#implementation-radial-gradient-overlays)
- [When to use](#when-to-use)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Five-zone lighting model

## What it does

Every non-trivial SVG object gets five shading zones: specular
highlight, light area, half-tone, form shadow (cool-shifted),
reflected light. This is standard digital-illustration practice —
pulls an object out of flat-fill territory into perceived 3D.

## The five zones

| Zone | What it is | Color rule |
|------|------------|------------|
| **Specular highlight** | The tiny brightest point where light reflects straight into the viewer's eye | Brighter than the fill, warm-shifted |
| **Light area** | The side facing the light source | Lighter than the base color |
| **Half-tone** | The terminator / midline — the true base color | The actual "color" of the object |
| **Form shadow** | The darker back half | **Cool-shifted** — blue, purple, teal. NEVER pure black or gray |
| **Reflected light** | Subtle warm glow on the shadow edge (bounced light from surroundings) | Warm, very low opacity 0.10–0.20 |

## Implementation — radial gradient + overlays

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md — Object Study -->
<defs>
  <radialGradient id="obj" fx="0.35" fy="0.3" cx="45%" cy="45%" r="55%"
    color-interpolation="linearRGB">
    <stop offset="0%"  stop-color="#fff7ed" stop-opacity="0.8"/>  <!-- specular area -->
    <stop offset="15%" stop-color="#fb923c"/>                     <!-- light area -->
    <stop offset="50%" stop-color="#ea580c"/>                     <!-- half-tone -->
    <stop offset="85%" stop-color="#7c2d12"/>                     <!-- form shadow -->
    <stop offset="100%" stop-color="#431407"/>                    <!-- deep shadow -->
  </radialGradient>
</defs>

<!-- Main object -->
<circle cx="200" cy="210" r="85" fill="url(#obj)"/>
<!-- Form shadow overlay (cool-shifted) -->
<ellipse cx="225" cy="235" rx="70" ry="75" fill="#3b1764" opacity="0.2"
  style="mix-blend-mode:multiply" clip-path="url(#obj-clip)"/>
<!-- Highlight -->
<ellipse cx="175" cy="180" rx="35" ry="25" fill="#fff7ed" opacity="0.35"/>
<!-- Specular dot -->
<circle cx="170" cy="172" r="7" fill="white" opacity="0.85"/>
<!-- Reflected / bounced light on shadow edge -->
<ellipse cx="230" cy="250" rx="25" ry="35" fill="#fef3c7" opacity="0.12"
  clip-path="url(#obj-clip)"/>
```

## When to use

- Every object that should read as 3D — spheres, bodies, orbs, fruit.
- Not needed for flat-fill UI elements (icons, logos) unless you want
  depth.

## Gotchas

- The cool-shifted form shadow is THE rule that separates amateur
  from pro. Black shadows look digital. Blue/purple/teal shadows
  look like paintings.
- Reflected light opacity must stay under 0.20 — louder than that
  and it looks like a second light source, not bounced light.
- Specular highlight goes LAST (on top) — rendering order matters.

## Cross-references

- [TECH-colored-shadows](TECH-colored-shadows.md) — the shadow-color rule in isolation.
- [TECH-multi-stop-gradients](TECH-multi-stop-gradients.md) — the 5-stop radial maps to the five zones.
- [TECH-character-incremental-construction](TECH-character-incremental-construction.md) — apply lighting per body part.
- [`../SKILL.md`](../SKILL.md) — parent skill

