---
name: TECH-mesh-gradient-workaround
category: svg-gradient
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The technique](#the-technique)
- [Best practices](#best-practices)
- [Gradient parameters that matter](#gradient-parameters-that-matter)
- [When to use](#when-to-use)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Mesh gradient workaround — layered radial gradients

## What it does

SVG doesn't support true mesh gradients (yet). The workaround is to
layer 3–5 overlapping radial gradients at different positions with
offset focal points — the visual result is indistinguishable from a
real mesh.

## The technique

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<defs>
  <radialGradient id="blob1" cx="30%" cy="25%" r="50%" fx="25%" fy="20%"
    color-interpolation="linearRGB">
    <stop offset="0%"  stop-color="#818cf8" stop-opacity="0.6"/>
    <stop offset="100%" stop-color="#818cf8" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="blob2" cx="70%" cy="60%" r="45%"
    color-interpolation="linearRGB">
    <stop offset="0%"  stop-color="#f472b6" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="#f472b6" stop-opacity="0"/>
  </radialGradient>
</defs>

<!-- Base dark background -->
<rect width="800" height="600" fill="#0f172a"/>
<!-- Blob 1 — top-left indigo -->
<rect width="800" height="600" fill="url(#blob1)"/>
<!-- Blob 2 — bottom-right pink -->
<rect width="800" height="600" fill="url(#blob2)"/>
<!-- Optional noise overlay for organic feel -->
<rect width="800" height="600" filter="url(#salt-pepper)" opacity="0.06"/>
```

## Best practices

- **3 layers is the sweet spot** — more becomes muddy.
- **Keep opacity low** (0.06–0.15 for subtle; 0.3–0.6 for vibrant).
- **Anchor one gradient to where content sits** — the gradient
  becomes the content's glow.
- **Pair with noise** — add `feTurbulence` at 6% opacity to break
  the too-smooth blend.

## Gradient parameters that matter

```
cx / cy      Gradient center (% of fill area)
r            Gradient radius
fx / fy      Focal point offset (where the gradient "starts")
spreadMethod pad (default), reflect, repeat
```

Off-center focal points (`fx="0.25" fy="0.20"`) create sphere-like
lighting — the hotspot offset toward a virtual light source.

## When to use

- Modern Web3 / SaaS backgrounds — the "aurora" look.
- Dark-mode hero sections that need life without being busy.
- Paired with `feTurbulence` noise for organic feel.

## Gotchas

- Overlapping radials can produce unexpected colors where they
  intersect — the `mix-blend-mode` of the rect affects it.
- On a pure black background, low-opacity blobs are near-invisible —
  increase opacity or lighten the bg.
- Performance — 5+ gradients on a full-canvas rect stress mobile GPUs.

## Cross-references

- [TECH-multi-stop-gradients](TECH-multi-stop-gradients.md) — individual gradient tuning.
  > What it does · When to use · Sky gradient — 6 stops · Sphere radial — 5 stops with offset focal · The `color-interpolation="linearRGB"` rule · Gotchas · Cross-references
- [TECH-pattern-tiles](TECH-pattern-tiles.md) — regular-tile alternative for backgrounds.
  > What it does · Dots · Diagonal lines · Waves · `patternUnits` — the critical attribute · `patternTransform` — rotate / scale / translate the whole pattern · Gotchas · Cross-references
- [TECH-vignette-overlay](TECH-vignette-overlay.md) — often combined to darken edges.
  > What it does · The gradient · The parameters · Layer order · Off-center vignettes · When to use · When NOT to use · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

