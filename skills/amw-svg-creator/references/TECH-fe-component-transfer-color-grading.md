---
name: TECH-fe-component-transfer-color-grading
category: svg-lighting
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---

# `feComponentTransfer` — per-channel color grading

## What it does

SVG filter primitive that remaps each color channel (R, G, B, A)
independently. Enables contrast boosts, warm/cool color shifts,
posterization, duotone, gamma curves — the same tricks real
color-grading software uses.

## Increase contrast

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<filter id="contrast" color-interpolation-filters="linearRGB">
  <feComponentTransfer>
    <feFuncR type="linear" slope="1.5" intercept="-0.15"/>
    <feFuncG type="linear" slope="1.5" intercept="-0.15"/>
    <feFuncB type="linear" slope="1.5" intercept="-0.15"/>
  </feComponentTransfer>
</filter>
```

`slope > 1` steepens the curve (more contrast). `intercept` offsets
the output to keep midtones centered.

## Warm color shift (sunset)

```xml
<feComponentTransfer>
  <feFuncR type="linear" slope="1.1" intercept="0.05"/>
  <feFuncG type="linear" slope="0.95" intercept="0"/>
  <feFuncB type="linear" slope="0.85" intercept="-0.05"/>
</feComponentTransfer>
```

Boost R, reduce B — the opposite of cool shift.

## Cool color shift (moonlit)

```xml
<feComponentTransfer>
  <feFuncR type="linear" slope="0.85" intercept="-0.05"/>
  <feFuncG type="linear" slope="0.9" intercept="0"/>
  <feFuncB type="linear" slope="1.15" intercept="0.05"/>
</feComponentTransfer>
```

## Posterize (reduce color steps)

```xml
<feComponentTransfer>
  <feFuncR type="discrete" tableValues="0 0.25 0.5 0.75 1"/>
  <feFuncG type="discrete" tableValues="0 0.25 0.5 0.75 1"/>
  <feFuncB type="discrete" tableValues="0 0.25 0.5 0.75 1"/>
</feComponentTransfer>
```

Snaps each channel to one of 5 fixed values — retro / poster look.

## Duotone (two-color map)

```xml
<filter id="duotone" color-interpolation-filters="linearRGB">
  <feColorMatrix type="saturate" values="0" result="gray"/>
  <feComponentTransfer in="gray">
    <feFuncR type="table" tableValues="0.1 0.9"/>   <!-- dark-red to light-red -->
    <feFuncG type="table" tableValues="0.0 0.6"/>
    <feFuncB type="table" tableValues="0.3 0.95"/>
  </feComponentTransfer>
</filter>
```

Tone the image to a two-color gradient — from `(0.1, 0, 0.3)` at
black to `(0.9, 0.6, 0.95)` at white.

## Gamma curve (lighten midtones)

```xml
<feComponentTransfer>
  <feFuncR type="gamma" amplitude="1" exponent="0.7" offset="0"/>
  <feFuncG type="gamma" amplitude="1" exponent="0.7" offset="0"/>
  <feFuncB type="gamma" amplitude="1" exponent="0.7" offset="0"/>
</feComponentTransfer>
```

`exponent < 1` lifts midtones; `> 1` darkens them.

## Gotchas

- Channel clipping — slope/intercept combinations that push values
  past `[0, 1]` get clamped, losing information. Test with extreme
  source colors.
- `linearRGB` interpolation is essential — sRGB grading amplifies
  artifacts in shadows.
- Don't apply multiple `feComponentTransfer` primitives in series
  when one matrix call can express the same transform cheaper.

## Cross-references

- `TECH-paper-texture-filter.md` — uses slope+intercept to compress
  noise.
- `TECH-material-simulation.md` — gradient-based material recipes
  (alternative to channel-level grading).
- [`../SKILL.md`](../SKILL.md) — parent skill

