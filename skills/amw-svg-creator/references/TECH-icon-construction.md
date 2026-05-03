---
name: TECH-icon-construction
category: svg-render-loop
source: image-generation/svg-creator/SKILL.md
also-in: image-generation/svg-creator/references/advanced-techniques.md
---
## Table of Contents

- [What it does](#what-it-does)
- [24×24 UI icons](#2424-ui-icons)
- [64×64+ app icons — depth + shine](#6464-app-icons-depth-shine)
- [Test legibility at small size](#test-legibility-at-small-size)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Icon construction — 24×24 stroke-based + app icons

## What it does

Two icon recipes: small stroke-based 24×24 UI icons, and larger
64×64+ app icons with depth (gradient background, top shine, glyph).

## 24×24 UI icons

Rules:
- Grid-aligned, integer coordinates
- 2px stroke
- `stroke-linecap="round"`
- `stroke-linejoin="round"`
- `fill="none"`
- `stroke="currentColor"` — inherits parent color
- Stay within 2–22 coordinate range (2px inset from edges)
- Usually one-pass works — no need for the full iterative loop

```xml
<!-- 24×24 icon template -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
  fill="none" stroke="currentColor" stroke-width="2"
  stroke-linecap="round" stroke-linejoin="round">
  <!-- Icon paths — stay in [2, 22] bbox -->
  <path d="M3 12h18"/>
  <path d="M12 3v18"/>
</svg>
```

## 64×64+ app icons — depth + shine

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"
      color-interpolation="linearRGB">
      <stop offset="0%"   stop-color="#818cf8"/>
      <stop offset="50%"  stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#4338ca"/>
    </linearGradient>
    <filter id="ico-shadow" x="-20%" y="-20%" width="140%" height="140%"
      color-interpolation-filters="linearRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
      <feOffset dy="2"/>
      <feFlood flood-color="#1e1b4b" flood-opacity="0.25"/>
      <feComposite operator="in" in2="SourceAlpha"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="64" height="64" rx="14" fill="url(#bg)" filter="url(#ico-shadow)"/>
  <!-- Top shine: small rounded rect at top, white, low opacity -->
  <rect x="4" y="4" width="56" height="28" rx="10" fill="white" opacity="0.12"/>
  <!-- Icon glyph centered -->
  <g transform="translate(32,32)" fill="none" stroke="white" stroke-width="2.5"
    stroke-linecap="round" stroke-linejoin="round">
    <!-- Icon paths centered on origin -->
  </g>
</svg>
```

## Test legibility at small size

Render the 24×24 at actual 24px in a browser before shipping — many
icons that look clear at 200px are illegible at 24.

## Gotchas

- Stroke-width less than 2 at 24×24 looks hairline and disappears on
  non-retina displays.
- `currentColor` means the icon inherits the parent's text color —
  always use it on UI icons so they work in light/dark themes.
- App-icon top shines at opacity > 0.15 start to look like glass —
  stay subtle for "shine", go higher for "glass-button".

## Cross-references

- [TECH-paint-order-and-spread-method](TECH-paint-order-and-spread-method.md) — `paint-order="stroke fill"`
  > What it does · `paint-order="stroke fill"` · `spreadMethod` on gradients · Example — brushed metal with `reflect` · `vector-effect="non-scaling-stroke"` · `pathLength="1"` · `gradientTransform` · Gotchas · Cross-references
  for halo-style icons.
- [TECH-multi-stop-gradients](TECH-multi-stop-gradients.md) — the gradient patterns for app icons.
  > What it does · When to use · Sky gradient — 6 stops · Sphere radial — 5 stops with offset focal · The `color-interpolation="linearRGB"` rule · Gotchas · Cross-references
- [TECH-drop-shadow-filter](TECH-drop-shadow-filter.md) — the shadow used under app icons.
  > What it does · Drop shadow (standard) · Contact shadow (tight, right under object) · Cast shadow (large, soft, far) · Inner shadow (not a drop shadow — opposite direction) · The obligatory `color-interpolation-filters="linearRGB"` · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

