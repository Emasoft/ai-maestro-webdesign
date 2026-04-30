---
name: TECH-salt-pepper-texture
category: svg-noise
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---

# Salt & pepper texture — two-layer professional grain

## What it does

The pro-grade noise filter: a "pepper" layer darkens via multiply
blend, a "salt" layer brightens via overlay blend. Combined, they add
tactile grain that reads as "material" without obscuring the
underlying art.

## The filter

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<filter id="salt-pepper" x="0" y="0" width="100%" height="100%"
  color-interpolation-filters="linearRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="3"
    stitchTiles="stitch" result="noise"/>
  <feColorMatrix in="noise" type="saturate" values="0" result="mono"/>
  <!-- Pepper (shadow grain) -->
  <feBlend in="SourceGraphic" in2="mono" mode="multiply" result="pepper"/>
  <!-- Salt (highlight grain) -->
  <feBlend in="pepper" in2="mono" mode="overlay" result="salted"/>
  <!-- Control intensity — reduce slope (0.5–0.8) to soften grain -->
  <feComponentTransfer in="salted">
    <feFuncA type="linear" slope="0.7" intercept="0"/>
  </feComponentTransfer>
</filter>
```

`feFuncA slope="0.7"` reduces the overall alpha of the composited result
to 70%, softening the grain. Default `slope="1"` (identity) gives maximum
grain intensity — reduce toward `0.5` for subtle texture, go up toward `1`
for strong grain. Do NOT set `slope` above `1` — it amplifies noise beyond
the source material and causes clipping artifacts.

Apply at element level for selective texturing, or at root for
full-canvas texture.

## When to use

- Photographic / painterly illustrations — adds tactile realism.
- Editorial infographics where the background feels "too digital".
- Album covers, posters, print material — grain is expected.

## Subtler salt — use `soft-light` instead of `overlay`

Change `mode="overlay"` to `mode="soft-light"` on the salt layer for
a less punchy highlight grain — useful on subjects where overlay
brights would burn out.

## Usage pattern

```xml
<circle cx="200" cy="210" r="85" fill="url(#obj)"/>
<!-- Texture on the element -->
<circle cx="200" cy="210" r="85" fill="none" filter="url(#salt-pepper)"
  opacity="0.08"/>
```

Note the `fill="none"` on the texture rect — the filter draws the
grain over the clipped bounds without covering the underlying fill.

## Gotchas

- Salt+pepper is intense — opacities above 0.12 push into "grungy"
  territory. Stay subtle.
- Works best on mid-tone subjects — on pure black or pure white
  surfaces, the grain is invisible.
- The filter's `result` names (`noise`, `mono`, `pepper`, `salted`)
  must match between `feBlend in="..."` references — a typo silently
  breaks the chain.

## Cross-references

- `TECH-fe-turbulence-noise.md` — the simpler single-layer cousin.
- `TECH-paper-texture-filter.md` — warmer grain for editorial looks.
- `TECH-colored-shadows.md` — salt+pepper pairs well with blue shadows.
- [`../SKILL.md`](../SKILL.md) — parent skill

