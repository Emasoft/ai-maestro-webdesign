---
name: TECH-landscape-composition
category: svg-lighting
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The layer stack (back to front)](#the-layer-stack-back-to-front)
- [The template](#the-template)
- [The atmospheric perspective rule](#the-atmospheric-perspective-rule)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Landscape scene composition — 7+ layers

> **GATE — OUT OF SCOPE FOR SVG-CREATOR.**
> This skill is GATED to icons / logos / technical SVG / patterns / animations only.
> Scene illustrations — landscapes, interiors, skies, environments — are
> **explicitly forbidden** by `../amw-design-principles/ai-slop-avoid.md` item 3
> and by [SKILL](../SKILL.md) (Scope — what this skill CANNOT produce).
>
> This reference file is retained **for technique reuse only** — the layer-stack
> pattern (back-to-front z-ordering, atmospheric perspective desaturation) applies
> legitimately to technical SVG diagrams with depth layers or gradient backgrounds.
> If the user is requesting a landscape illustration or environmental scene: STOP,
> cite `ai-slop-avoid.md` item 3, and route to placeholder or real assets.

## What it does

A layered back-to-front composition template for landscape
illustrations. Each layer is tuned for its atmospheric perspective:
distant elements are desaturated and light-shifted; near elements
are vivid.

## The layer stack (back to front)

1. **Sky** — multi-stop vertical gradient (6+ stops)
2. **Sun / moon** — circle + soft radial glow halo
3. **Far mountains** — low saturation, high lightness, blue-shifted, opacity 0.3-0.4
4. **Mid mountains** — medium saturation, opacity 0.5-0.7
5. **Near hills** — full saturation, detailed
6. **Foreground details** — trees, rocks, with drop shadows
7. **Atmospheric haze** — semi-transparent bluish rect between layers
8. **Vignette overlay** — radial gradient at 0.3-0.5 black opacity on edges

## The template

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md — truncated -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500"
  role="img" aria-labelledby="t d">
  <title id="t">Landscape Title</title>
  <desc id="d">Description</desc>

  <defs>
    <!-- sky gradient (6+ stops), sun glow radial, shadow filter, haze gradient,
         noise filter, vignette gradient -->
  </defs>

  <!-- L1: Sky -->
  <rect width="800" height="500" fill="url(#sky)"/>

  <!-- L2: Sun with soft glow -->
  <circle cx="600" cy="120" r="40" fill="#fbbf24"/>
  <circle cx="600" cy="120" r="90" fill="url(#sun-glow)" opacity="0.4"/>

  <!-- L3: Far mountains (low saturation, blue-shifted) -->
  <path d="M0,350 Q200,220 400,310 Q550,260 800,320 L800,500 L0,500Z"
    fill="#94a3b8" opacity="0.4"/>

  <!-- L4: Mid mountains (medium saturation) -->
  <path d="M0,380 Q150,290 300,350 Q450,310 600,340 L800,370 L800,500 L0,500Z"
    fill="#64748b" opacity="0.6"/>

  <!-- L5: Near hills (full saturation) -->
  <path d="M0,420 Q200,360 400,400 Q600,375 800,410 L800,500 L0,500Z"
    fill="url(#hill-gradient)"/>

  <!-- L6: Foreground -->
  <g id="trees" filter="url(#drop-shadow)">
    <use href="#tree" x="120" y="370" width="60" height="90"/>
  </g>

  <!-- L7: Atmospheric haze -->
  <rect y="280" width="800" height="220" fill="#bfdbfe" opacity="0.12"/>

  <!-- L8: Vignette -->
  <rect width="800" height="500" fill="url(#vignette-grad)"/>
</svg>
```

## The atmospheric perspective rule

Distance from the viewer = color compression toward the sky color.
Far mountains are nearly sky-colored. Mid ground is somewhat desaturated.
Foreground is full color.

## Gotchas

- Layer ordering in the source = render order. Reversing it produces
  nonsense.
- Don't stack too many atmospheric haze rects — a single `opacity:
  0.12` rect between mid and far layers is enough.
- Vignette should fade to black at corners, not edges — a 60% radius
  inner stop, 100% at outer.

## Cross-references

- [TECH-multi-stop-gradients](TECH-multi-stop-gradients.md) — the sky gradient pattern.
  > What it does · When to use · Sky gradient — 6 stops · Sphere radial — 5 stops with offset focal · The `color-interpolation="linearRGB"` rule · Gotchas · Cross-references
- [TECH-vignette-overlay](TECH-vignette-overlay.md) — the edge-darkening pattern.
  > What it does · The gradient · The parameters · Layer order · Off-center vignettes · When to use · When NOT to use · Gotchas · Cross-references
- [TECH-atmospheric-effects](TECH-atmospheric-effects.md) — fog, rays, rain.
  > Scope note · What it does · Light rays (god rays) · Fog / mist (masked gradient) · Stars with twinkling · Rain · Clouds · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

