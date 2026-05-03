---
name: TECH-atmospheric-effects
category: svg-effects
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [Scope note](#scope-note)
- [What it does](#what-it-does)
- [Light rays (god rays)](#light-rays-god-rays)
- [Fog / mist (masked gradient)](#fog-mist-masked-gradient)
- [Stars with twinkling](#stars-with-twinkling)
- [Rain](#rain)
- [Clouds](#clouds)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Atmospheric effects — light rays, fog, stars, rain, clouds

## Scope note

These effects are **in-scope** for svg-creator when applied as
decorative background elements inside a technical SVG (e.g. a star
field behind a space-themed logo, a fog overlay on a dark diagram
background, a rain-stripe texture). They are **out of scope** if the
goal is building a full landscape scene or character environment —
that territory is forbidden by [SKILL](../SKILL.md) (Scope — what this skill
CANNOT produce).

## What it does

Small pattern library of environmental effects that add mood and
atmosphere to SVG backgrounds and logo compositions. Each is a handful
of elements — light on resources, heavy on impact.

## Light rays (god rays)

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<g opacity="0.12" style="mix-blend-mode:screen">
  <polygon points="500,80 280,500 340,500" fill="#fbbf24"/>
  <polygon points="500,80 400,500 470,500" fill="#fbbf24"/>
  <polygon points="500,80 550,500 640,500" fill="#fbbf24"/>
  <polygon points="500,80 700,500 780,500" fill="#fbbf24"/>
</g>
```

Triangles radiating from a light source, blended with `screen`.

## Fog / mist (masked gradient)

```xml
<defs>
  <mask id="fog-mask">
    <linearGradient id="fog-fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="black"/>
      <stop offset="30%" stop-color="white"/>
      <stop offset="70%" stop-color="white"/>
      <stop offset="100%" stop-color="black"/>
    </linearGradient>
    <rect width="800" height="200" fill="url(#fog-fade)"/>
  </mask>
</defs>
<rect y="300" width="800" height="200" fill="white" opacity="0.25"
  mask="url(#fog-mask)"/>
```

White rectangle, masked to fade at top and bottom edges.

## Stars with twinkling

```xml
<style>
  @keyframes twinkle {
    0%, 100% { opacity: 0.3; }
    50%      { opacity: 1; }
  }
  .star { animation: twinkle 3s ease-in-out infinite; transform-box: fill-box; }
</style>
<g id="stars">
  <circle class="star" cx="50" cy="30" r="1" fill="white" style="animation-delay:0s"/>
  <circle class="star" cx="200" cy="55" r="1.5" fill="white" style="animation-delay:1.2s"/>
  <circle class="star" cx="400" cy="40" r="0.8" fill="white" style="animation-delay:0.5s"/>
  <!-- Vary size 0.5–2, delay 0–4s -->
</g>
```

Stagger delays randomly for natural twinkle.

## Rain

```xml
<g opacity="0.25" stroke="white" stroke-width="1" stroke-linecap="round">
  <line x1="100" y1="0"  x2="88"  y2="60"/>
  <line x1="250" y1="20" x2="238" y2="80"/>
  <!-- Many more, slight angle, varied lengths 40-80 -->
</g>
```

Slight diagonal angle, staggered lengths.

## Clouds

```xml
<g filter="url(#soft)">
  <ellipse cx="200" cy="100" rx="80" ry="35" fill="white" opacity="0.9"/>
  <ellipse cx="155" cy="108" rx="55" ry="30" fill="white" opacity="0.85"/>
  <ellipse cx="245" cy="106" rx="60" ry="28" fill="white" opacity="0.85"/>
  <ellipse cx="200" cy="118" rx="90" ry="25" fill="white" opacity="0.8"/>
</g>
```

Overlapping ellipses with soft blur filter.

## Gotchas

- Light rays at opacity > 0.2 dominate the scene — keep subtle.
- Twinkle animations need `prefers-reduced-motion` override (see
  [TECH-reduced-motion](TECH-reduced-motion.md)).
- Rain angles should match wind direction if the scene implies wind.

## Cross-references

- [TECH-landscape-composition](TECH-landscape-composition.md) — the scene these effects live in.
  > What it does · The layer stack (back to front) · The template · The atmospheric perspective rule · Gotchas · Cross-references
- [TECH-css-smil-animation](TECH-css-smil-animation.md) — CSS + SMIL animation for twinkling /
  > What it does · The `transform-box` rule · Spinner (CSS) · Line drawing reveal (pathLength + stroke-dasharray) · Staggered entrance · SMIL animation (works in `<img>` tags) · Attribute animation · Transform animation · Motion along a path · Sequential timing via `begin` · Gotchas · Cross-references
  moving effects.
- [TECH-reduced-motion](TECH-reduced-motion.md) — accessibility override.
  > What it does · The minimum implementation · Why `0.01ms` instead of `0s` · SMIL equivalent · When it's OK to ignore · When it's partially OK · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

