---
name: TECH-drop-shadow-filter
category: svg-lighting
source: image-generation/svg-creator/references/advanced-techniques.md
also-in: image-generation/svg-creator/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [Drop shadow (standard)](#drop-shadow-standard)
- [Contact shadow (tight, right under object)](#contact-shadow-tight-right-under-object)
- [Cast shadow (large, soft, far)](#cast-shadow-large-soft-far)
- [Inner shadow (not a drop shadow — opposite direction)](#inner-shadow-not-a-drop-shadow-opposite-direction)
- [The obligatory `color-interpolation-filters="linearRGB"`](#the-obligatory-color-interpolation-filterslinearrgb)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Drop shadow, contact shadow, cast shadow (three filter chains)

## What it does

Three shadow-filter recipes, each tuned for a specific shadow type.
All use the same SVG filter primitives — `feGaussianBlur` +
`feOffset` + `feFlood` + `feComposite` + `feMerge` — but with
different blur / offset / opacity parameters.

## Drop shadow (standard)

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<filter id="drop-shadow" x="-20%" y="-20%" width="140%" height="140%"
  color-interpolation-filters="linearRGB">
  <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur"/>
  <feOffset in="blur" dx="3" dy="5" result="offset"/>
  <feFlood flood-color="#1e1b4b" flood-opacity="0.30" result="color"/>
  <feComposite in="color" in2="offset" operator="in" result="shadow"/>
  <feMerge>
    <feMergeNode in="shadow"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
```

- `stdDeviation="4"` — soft blur
- `dy="5"` — shadow falls below the object
- `flood-opacity="0.30"` — visible but not loud

## Contact shadow (tight, right under object)

Same filter, different params:

```
stdDeviation="1.5"
dx="0" dy="1"
flood-opacity="0.40"
```

Reads as "sitting on a surface" — no cast-shadow feel.

## Cast shadow (large, soft, far)

```
stdDeviation="6"
dx="4" dy="8"
flood-opacity="0.20"
```

Reads as sunlight casting a shadow onto the ground. Larger blur,
more offset, lower opacity.

## Inner shadow (not a drop shadow — opposite direction)

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<filter id="inner-shadow" x="-10%" y="-10%" width="120%" height="120%"
  color-interpolation-filters="linearRGB">
  <feComponentTransfer in="SourceAlpha" result="inverse">
    <feFuncA type="table" tableValues="1 0"/>
  </feComponentTransfer>
  <feGaussianBlur in="inverse" stdDeviation="3" result="blur"/>
  <feOffset in="blur" dx="2" dy="3" result="offset"/>
  <feComposite in="offset" in2="SourceAlpha" operator="in" result="inner"/>
  <feFlood flood-color="#1e1b4b" flood-opacity="0.5" result="color"/>
  <feComposite in="color" in2="inner" operator="in" result="shadow"/>
  <feMerge>
    <feMergeNode in="SourceGraphic"/>
    <feMergeNode in="shadow"/>
  </feMerge>
</filter>
```

Use for pressed-button / engraved effects.

## The obligatory `color-interpolation-filters="linearRGB"`

Every shadow filter — always set this on the filter element. Without
it, the shadow color composites in sRGB and looks muddier than
expected.

## Gotchas

- Changing `flood-color` to black makes the shadow look generated —
  always use the colored-shadow palette from TECH-colored-shadows.
- Filter region (`x`, `y`, `width`, `height`) must exceed the
  element bounds by at least the offset + blur — otherwise the
  shadow gets clipped.
- `dy` alone works fine for overhead light. Add `dx` for angled light
  (morning/evening sun, raking light).

## Cross-references

- [TECH-colored-shadows](TECH-colored-shadows.md) — the color palette rule these filters implement.
  > What it does · The palette · Where the color goes · Drop-shadow filter with colored shadow · Opacity rules · Gotchas · Cross-references
- [TECH-soft-glow-filter](TECH-soft-glow-filter.md) — the positive cousin (glow instead of shadow).
  > What it does · The basic filter · Colored glow variant · `stdDeviation` tuning · Filter region · When to use · Gotchas · Cross-references
- [TECH-specular-diffuse-lighting](TECH-specular-diffuse-lighting.md) — physics-based alternative for
  > What it does · Specular — shiny surface · Diffuse — matte surface · When to use · When NOT to use · Gotchas · Cross-references
  surface-realistic shading.
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
