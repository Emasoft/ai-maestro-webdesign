---
name: TECH-background-depth
category: infographic-archetype
source: image-generation/create-infographics/resources/style-details.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [Gradient mesh background](#gradient-mesh-background)
- [SVG noise grain](#svg-noise-grain)
- [Scanline overlay (Cyber aesthetic)](#scanline-overlay-cyber-aesthetic)
- [Paper texture (Editorial aesthetic)](#paper-texture-editorial-aesthetic)
- [Glassmorphism accent panels](#glassmorphism-accent-panels)
- [Background decoration hierarchy](#background-decoration-hierarchy)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Background depth — radial gradient orbs, scanlines, paper texture

## What it does

Adds subtle depth to the flat dark background via three techniques:
radial gradient mesh, SVG noise grain, optional scanline overlay.
Background is NOT flat — it has depth. The decoration is structural
(borders, glows, geometry), not texture-based.

## Gradient mesh background

```css
/* source: image-generation/create-infographics/resources/style-details.md */
.infographic {
  background-color: #0D0D0D;
  background-image:
    radial-gradient(ellipse 80% 60% at 20% 10%,
      rgba(var(--primary-rgb), 0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%,
      rgba(var(--secondary-rgb), 0.08) 0%, transparent 50%),
    radial-gradient(ellipse 100% 80% at 50% 50%,
      rgba(255,255,255,0.02) 0%, transparent 70%);
}
```

**Tuning:**
- 3 layers is the sweet spot. More = muddy.
- Keep opacity low (0.06–0.15). The mesh is felt, not seen.
- Anchor one gradient to where the hero stat lives.

## SVG noise grain

```html
<!-- source: image-generation/create-infographics/resources/style-details.md -->
<svg style="position:absolute;width:0;height:0">
  <defs>
    <filter id="grain">
      <feTurbulence type="fractalNoise" baseFrequency="0.65"
        numOctaves="3" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
      <feBlend in="SourceGraphic" mode="overlay" result="blend"/>
      <feComposite in="blend" in2="SourceGraphic" operator="in"/>
    </filter>
  </defs>
</svg>
```

Apply to container:

```css
.infographic::after {
  content: '';
  position: absolute;
  inset: 0;
  filter: url(#grain);
  opacity: 0.04;       /* 3-6%: subtle. Above 8% becomes noise */
  pointer-events: none;
  border-radius: inherit;
}
```

**When to use:** Editorial, Premium/Luxury, Corporate aesthetics.
**Skip for:** Bold/Cyber — glow already adds depth.

## Scanline overlay (Cyber aesthetic)

```css
.infographic::before {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 0, 0, 0.12) 2px,
    rgba(0, 0, 0, 0.12) 4px
  );
  pointer-events: none;
  z-index: 1;
}
```

**When to use:** Bold/Cyber only. Pair with neon accents + dark
backgrounds.
**Do NOT use:** Editorial or Corporate — reads as distressed/broken.

## Paper texture (Editorial aesthetic)

```html
<svg style="position:absolute;width:0;height:0">
  <defs>
    <filter id="paper">
      <feTurbulence type="turbulence" baseFrequency="0.04"
        numOctaves="5" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="2"
        xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>
</svg>
```

```css
.infographic {
  background-color: #F5F0E8;   /* warm off-white */
  filter: url(#paper);
}
```

**When to use:** Editorial/Clean, Print/Newsletter output. Gives a
handcrafted, trusted feel.

## Glassmorphism accent panels

```css
.glass-panel {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
}

/* Colored glass accent variant */
.glass-accent {
  background: rgba(var(--primary-rgb), 0.08);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(var(--primary-rgb), 0.2);
  border-radius: 12px;
}
```

**Rules:**
- Requires content BEHIND it (gradient mesh, image). On solid black
  it's invisible.
- Max 2 glass panels per infographic.
- Good for: callout boxes, hero stat containers, quote cards.
- Do NOT use for standard data cards or backgrounds.

## Background decoration hierarchy

```
Bold/Cyber:       Gradient mesh + scanlines + glow
Editorial/Clean:  Paper texture, no glow
Premium/Luxury:   Gradient mesh at 0.06 opacity, subtle grain
Corporate:        Solid, subtle drop shadow only
Playful/Loud:     Gradient mesh, saturation OK
```

## Gotchas

- `::before` and `::after` pseudos on body element — they need
  `position: absolute` and the body needs `position: relative`.
- SVG filters can be expensive on mobile — test on lower-end devices.
- Multiple layers compete — pick one primary (gradient mesh) and
  maybe one secondary (grain). Stacking more is muddy.

## Cross-references

- [TECH-glow-system](TECH-glow-system.md) — the complementary element-level glows.
  > What it does · The glow system · Double-layer glow pattern · Top confirmed glow colors · When to use each · Light-mode override · Gotchas · Cross-references
- [TECH-signature-palette](TECH-signature-palette.md) — what `--primary-rgb` resolves to.
  > What it does · Background rules · The default accent hierarchy · Palette temperature · Other most-used accents (in order) · Named palette recipes (top 3) · AMBER DARK (signature, most used) · CYBER TEAL · HOT PINK WEB3 · Rule — brand first, signature second · Gotchas · Cross-references
- [TECH-mesh-gradient-workaround](../../amw-svg-creator/references/TECH-mesh-gradient-workaround.md) —
  > What it does · The technique · Best practices · Gradient parameters that matter · When to use · Gotchas · Cross-references
  the gradient mesh technique in depth.
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

