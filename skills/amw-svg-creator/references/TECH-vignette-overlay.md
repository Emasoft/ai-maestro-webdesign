---
name: TECH-vignette-overlay
category: svg-lighting
source: image-generation/svg-creator/references/advanced-techniques.md
also-in: image-generation/svg-creator/SKILL.md
---

# Vignette overlay — edge darkening

## What it does

A radial gradient from transparent center to darkened corners,
placed over the final scene with `mix-blend-mode: multiply`.
Focuses the viewer's eye toward the center — classic photographic
and cinematic technique.

## The gradient

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<radialGradient id="vignette-grad" cx="50%" cy="50%" r="60%">
  <stop offset="0%"   stop-color="black" stop-opacity="0"/>
  <stop offset="100%" stop-color="black" stop-opacity="0.45"/>
</radialGradient>
<rect width="800" height="600" fill="url(#vignette-grad)"
  style="mix-blend-mode:multiply"/>
```

## The parameters

- `cx="50%" cy="50%"` — centered vignette. Offset to highlight
  something (`cx="30%" cy="40%"`).
- `r="60%"` — inner clear radius. Smaller = tighter focus.
- Outer stop opacity 0.30–0.50 for subtle, 0.50–0.70 for dramatic.

## Layer order

Vignette goes LAST — on top of everything. Over the noise texture,
over the content, over atmospheric effects.

## Off-center vignettes

Move `cx` / `cy` to emphasize a specific area:

```xml
<!-- Vignette centered on top-left — emphasizes that corner -->
<radialGradient id="tl-vignette" cx="25%" cy="25%" r="70%">
  <stop offset="0%"   stop-color="black" stop-opacity="0"/>
  <stop offset="100%" stop-color="black" stop-opacity="0.50"/>
</radialGradient>
```

## When to use

- Every scene-based illustration — landscapes, portraits, product
  shots.
- Hero images for infographics.
- When you want "focus" without physically cropping.

## When NOT to use

- Flat UI / logo design — reads as damage.
- Very short, wide banners — vignettes need square-ish space to work.
- Combined with existing heavy atmospheric haze — redundant.

## Gotchas

- `mix-blend-mode: multiply` interacts with the underlying content —
  pure black underneath goes fully black, white underneath stays
  half-darkened. Tune to your content.
- Without `mix-blend-mode`, the vignette just stacks a black gradient
  on top — technically the same effect, but multiply respects the
  underlying tones better.

## Cross-references

- `TECH-landscape-composition.md` — vignette is layer 8 in the stack.
- `TECH-atmospheric-effects.md` — often combined with fog/mist.
- `TECH-mesh-gradient-workaround.md` — radial gradients from a
  different angle.
- [`../SKILL.md`](../SKILL.md) — parent skill

