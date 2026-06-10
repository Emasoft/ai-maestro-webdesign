<!-- MIT — adapted from material-3-skill (Copyright (c) 2026 CWTI Ltd) -->
<!-- See LICENSE / source: material-3-skill-master/skills/material-3/references/color-system.md. -->

# TECH-01 — HCT tonal palette and role-based color tokens

## Table of Contents

- [HCT color space](#hct-color-space)
- [The 5 tonal palettes](#the-5-tonal-palettes)
- [Role-to-tone mapping](#role-to-tone-mapping)
- [Color pairing rules](#color-pairing-rules)
- [Fixed accent colors (Add-on)](#fixed-accent-colors-add-on)
- [Dynamic color (user-generated)](#dynamic-color-user-generated)
- [Generating a scheme from a seed (JavaScript)](#generating-a-scheme-from-a-seed-javascript)
- [Color harmonization](#color-harmonization)
- [User-controlled contrast (May 2025)](#user-controlled-contrast-may-2025)
- [Baseline static schemes (no dynamic color)](#baseline-static-schemes-no-dynamic-color)
- [Verification](#verification)

## Overview

Material Design 3's color system is built on the HCT color space (Hue / Chroma / Tone) and a role-based token namespace. A single seed color generates 5 tonal palettes; each palette spans 16 tonal stops along 0..100; the 29+ color roles are *mapped* to specific stops in those palettes depending on light vs dark scheme.

This file documents:
- The HCT model
- The 5 tonal palettes generated from a seed
- The 29+ color roles and their pairing rules
- Dynamic color generation (`@material/material-color-utilities`)
- The 3 contrast levels (standard / medium / high, May 2025)
- Baseline static schemes for products not using dynamic color

## HCT color space

HCT is a perceptually uniform color space designed for Material You.

- **Hue (H, 0..360)** — the color "family" (red, orange, blue, ...). Equivalent to HSL hue but corrected for perception.
- **Chroma (C, 0..~150)** — colorfulness. 0 = neutral gray. Higher chroma is more saturated, but the maximum achievable chroma depends on the tone.
- **Tone (T, 0..100)** — perceived lightness, calibrated to CIE L*. Tone 0 is pure black; tone 100 is pure white; tone 50 is mid-gray.

Why HCT vs HSL: in HSL, two colors at the same `L` can look very different in perceived lightness (a yellow at `L=50%` looks brighter than a blue at `L=50%`). HCT corrects for this — two HCT colors at the same tone *do* read as the same lightness. This is critical for role-based theming: when the spec says "primary at tone 40 must pair with on-primary at tone 100", the contrast guarantee holds across hue rotations of the seed.

## The 5 tonal palettes

A seed color (one hex value) generates 5 palettes:

| Palette | Derived from seed by | Used for |
|---------|----------------------|---------|
| Primary | Same hue, max chroma | `primary`, `on-primary`, `primary-container`, `on-primary-container` |
| Secondary | Same hue, lower chroma | `secondary`, `on-secondary`, `secondary-container`, `on-secondary-container` |
| Tertiary | Hue shifted +60deg, moderate chroma | `tertiary`, `on-tertiary`, `tertiary-container`, `on-tertiary-container` |
| Neutral | Same hue, very low chroma (~4) | All `surface`, `surface-container-*`, `on-surface`, `inverse-surface` |
| Neutral-Variant | Same hue, slightly higher chroma (~8) | `outline`, `outline-variant`, `on-surface-variant` |

Each palette has 16 key tonal stops: `0, 10, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 95, 98, 99, 100`. Internally, `@material/material-color-utilities` can interpolate any tone in 0..100.

## Role-to-tone mapping

The 29+ color roles map to specific tonal stops. Light and dark schemes use *different* stops from the *same* palette — this is how MD3 generates a working dark theme from a single seed.

### Light scheme

| Role | Palette | Tone |
|------|---------|------|
| primary | Primary | 40 |
| on-primary | Primary | 100 |
| primary-container | Primary | 90 |
| on-primary-container | Primary | 10 |
| secondary | Secondary | 40 |
| on-secondary | Secondary | 100 |
| secondary-container | Secondary | 90 |
| on-secondary-container | Secondary | 10 |
| tertiary | Tertiary | 40 |
| on-tertiary | Tertiary | 100 |
| tertiary-container | Tertiary | 90 |
| on-tertiary-container | Tertiary | 10 |
| error | Error (fixed palette) | 40 |
| on-error | Error | 100 |
| error-container | Error | 90 |
| on-error-container | Error | 10 |
| surface | Neutral | 98 |
| on-surface | Neutral | 10 |
| on-surface-variant | Neutral-Variant | 30 |
| surface-container-lowest | Neutral | 100 |
| surface-container-low | Neutral | 96 |
| surface-container | Neutral | 94 |
| surface-container-high | Neutral | 92 |
| surface-container-highest | Neutral | 90 |
| surface-dim | Neutral | 87 |
| surface-bright | Neutral | 98 |
| outline | Neutral-Variant | 50 |
| outline-variant | Neutral-Variant | 80 |
| inverse-surface | Neutral | 20 |
| inverse-on-surface | Neutral | 95 |
| inverse-primary | Primary | 80 |

### Dark scheme

| Role | Palette | Tone |
|------|---------|------|
| primary | Primary | 80 |
| on-primary | Primary | 20 |
| primary-container | Primary | 30 |
| on-primary-container | Primary | 90 |
| secondary | Secondary | 80 |
| on-secondary | Secondary | 20 |
| secondary-container | Secondary | 30 |
| on-secondary-container | Secondary | 90 |
| tertiary | Tertiary | 80 |
| on-tertiary | Tertiary | 20 |
| tertiary-container | Tertiary | 30 |
| on-tertiary-container | Tertiary | 90 |
| error | Error | 80 |
| on-error | Error | 20 |
| error-container | Error | 30 |
| on-error-container | Error | 90 |
| surface | Neutral | 6 |
| on-surface | Neutral | 90 |
| on-surface-variant | Neutral-Variant | 80 |
| surface-container-lowest | Neutral | 4 |
| surface-container-low | Neutral | 10 |
| surface-container | Neutral | 12 |
| surface-container-high | Neutral | 17 |
| surface-container-highest | Neutral | 22 |
| surface-dim | Neutral | 6 |
| surface-bright | Neutral | 24 |
| outline | Neutral-Variant | 60 |
| outline-variant | Neutral-Variant | 30 |
| inverse-surface | Neutral | 90 |
| inverse-on-surface | Neutral | 20 |
| inverse-primary | Primary | 40 |

Notice the asymmetry: in the light scheme, `primary` is tone 40 (vivid mid-tone); in dark it's tone 80 (lighter, lower contrast against dark surface). The `on-*` pairs invert tone to maintain contrast on whichever container background they sit on.

## Color pairing rules

Containers must only be paired with their designated `on-*` text/icon colors. Pairing outside this table breaks contrast under dynamic color and the medium/high contrast levels.

| Container / fill | Text / icon |
|------------------|-------------|
| `primary` | `on-primary` |
| `primary-container` | `on-primary-container` |
| `secondary` | `on-secondary` |
| `secondary-container` | `on-secondary-container` |
| `tertiary` | `on-tertiary` |
| `tertiary-container` | `on-tertiary-container` |
| `error` | `on-error` |
| `error-container` | `on-error-container` |
| `surface` | `on-surface` or `on-surface-variant` |
| `surface-container-*` (any of 5) | `on-surface` or `on-surface-variant` |
| `inverse-surface` | `inverse-on-surface` or `inverse-primary` |

**`outline` (3:1 contrast against surface)** is reserved for interactive boundaries — text-field outlines, focus rings. **`outline-variant` (~1.5:1)** is decorative — dividers, card borders. Never swap them.

## Fixed accent colors (Add-on)

These maintain the same color in BOTH light and dark themes (unlike normal container colors which change tone):

| Role |
|------|
| `primary-fixed` |
| `primary-fixed-dim` |
| `on-primary-fixed` |
| `on-primary-fixed-variant` |
| `secondary-fixed` / `secondary-fixed-dim` / `on-secondary-fixed` / `on-secondary-fixed-variant` |
| `tertiary-fixed` / `tertiary-fixed-dim` / `on-tertiary-fixed` / `on-tertiary-fixed-variant` |

Use when an accent must stay visually identical between themes (brand mark, status indicator). Fixed colors do not adapt to theme — verify contrast manually if used on a varying background.

## Dynamic color (user-generated)

On Android 12+ (API 31+), the OS extracts a seed from the user's wallpaper and generates an HCT scheme. The Compose surface is:

```kotlin
val colorScheme = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
    if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
} else {
    if (darkTheme) darkColorScheme(...) else lightColorScheme(...)
}
MaterialTheme(colorScheme = colorScheme) { ... }
```

On the web, there is **no browser wallpaper API**. Dynamic color must come from content the app already controls (album art, uploaded image, brand-color picker). Derive a seed from a Color Thief-style extractor and pipe through `@material/material-color-utilities`.

## Generating a scheme from a seed (JavaScript)

```javascript
import {
  argbFromHex,
  hexFromArgb,
  Hct,
  SchemeContent,
} from '@material/material-color-utilities';

function generateScheme(seedHex, isDark = false, contrast = 0.0) {
  const hct = Hct.fromInt(argbFromHex(seedHex));
  // contrast: 0.0 standard, 0.5 medium, 1.0 high (May 2025)
  const scheme = new SchemeContent(hct, isDark, contrast);

  return {
    '--md-sys-color-primary': hexFromArgb(scheme.primary),
    '--md-sys-color-on-primary': hexFromArgb(scheme.onPrimary),
    '--md-sys-color-primary-container': hexFromArgb(scheme.primaryContainer),
    '--md-sys-color-on-primary-container': hexFromArgb(scheme.onPrimaryContainer),
    '--md-sys-color-secondary': hexFromArgb(scheme.secondary),
    '--md-sys-color-on-secondary': hexFromArgb(scheme.onSecondary),
    '--md-sys-color-secondary-container': hexFromArgb(scheme.secondaryContainer),
    '--md-sys-color-on-secondary-container': hexFromArgb(scheme.onSecondaryContainer),
    '--md-sys-color-tertiary': hexFromArgb(scheme.tertiary),
    '--md-sys-color-on-tertiary': hexFromArgb(scheme.onTertiary),
    '--md-sys-color-tertiary-container': hexFromArgb(scheme.tertiaryContainer),
    '--md-sys-color-on-tertiary-container': hexFromArgb(scheme.onTertiaryContainer),
    '--md-sys-color-error': hexFromArgb(scheme.error),
    '--md-sys-color-on-error': hexFromArgb(scheme.onError),
    '--md-sys-color-error-container': hexFromArgb(scheme.errorContainer),
    '--md-sys-color-on-error-container': hexFromArgb(scheme.onErrorContainer),
    '--md-sys-color-surface': hexFromArgb(scheme.surface),
    '--md-sys-color-on-surface': hexFromArgb(scheme.onSurface),
    '--md-sys-color-on-surface-variant': hexFromArgb(scheme.onSurfaceVariant),
    '--md-sys-color-surface-container': hexFromArgb(scheme.surfaceContainer),
    '--md-sys-color-surface-container-low': hexFromArgb(scheme.surfaceContainerLow),
    '--md-sys-color-surface-container-lowest': hexFromArgb(scheme.surfaceContainerLowest),
    '--md-sys-color-surface-container-high': hexFromArgb(scheme.surfaceContainerHigh),
    '--md-sys-color-surface-container-highest': hexFromArgb(scheme.surfaceContainerHighest),
    '--md-sys-color-outline': hexFromArgb(scheme.outline),
    '--md-sys-color-outline-variant': hexFromArgb(scheme.outlineVariant),
    '--md-sys-color-inverse-surface': hexFromArgb(scheme.inverseSurface),
    '--md-sys-color-inverse-on-surface': hexFromArgb(scheme.inverseOnSurface),
    '--md-sys-color-inverse-primary': hexFromArgb(scheme.inversePrimary),
  };
}

function applyScheme(seedHex, isDark = false, contrast = 0.0) {
  const tokens = generateScheme(seedHex, isDark, contrast);
  for (const [k, v] of Object.entries(tokens)) {
    document.documentElement.style.setProperty(k, v);
  }
}
```

## Color harmonization

When integrating a custom brand color that does NOT come from the seed (e.g., a third-party brand badge), harmonize it toward the scheme's primary so it feels cohesive:

```javascript
import { Blend, argbFromHex, hexFromArgb } from '@material/material-color-utilities';

const harmonizedArgb = Blend.harmonize(
  argbFromHex('#FF6600'),    // custom brand color
  argbFromHex('#6750A4')     // scheme primary
);
const harmonizedHex = hexFromArgb(harmonizedArgb);
```

Harmonization rotates the hue slightly toward the primary's hue, keeping chroma and tone — the color stays recognizably itself but reads as part of the same family.

## User-controlled contrast (May 2025)

MD3 now supports 3 user-selectable contrast levels:

| Level | Contrast value | Behavior |
|-------|----------------|----------|
| Standard | `0.0` | Default tonal distances |
| Medium | `0.5` | Increased tonal distance between paired roles |
| High | `1.0` | Maximum tonal distance for vision accessibility |

The contrast parameter widens the tonal gap between `container` and `on-container` pairs without changing the perceived hue. Generate per-contrast schemes once and switch via a CSS class or media query.

```javascript
const standard = new SchemeContent(hct, isDark, 0.0);
const medium   = new SchemeContent(hct, isDark, 0.5);
const high     = new SchemeContent(hct, isDark, 1.0);
```

## Baseline static schemes (no dynamic color)

For products that do not use dynamic color, MD3 ships baseline light and dark schemes derived from the canonical purple seed `#6750A4`.

### Light

```css
:root {
  --md-sys-color-primary: #6750A4;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #EADDFF;
  --md-sys-color-on-primary-container: #21005D;
  --md-sys-color-secondary: #625B71;
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-secondary-container: #E8DEF8;
  --md-sys-color-on-secondary-container: #1D192B;
  --md-sys-color-tertiary: #7D5260;
  --md-sys-color-on-tertiary: #FFFFFF;
  --md-sys-color-tertiary-container: #FFD8E4;
  --md-sys-color-on-tertiary-container: #31111D;
  --md-sys-color-error: #B3261E;
  --md-sys-color-on-error: #FFFFFF;
  --md-sys-color-error-container: #F9DEDC;
  --md-sys-color-on-error-container: #410E0B;
  --md-sys-color-surface: #FEF7FF;
  --md-sys-color-on-surface: #1D1B20;
  --md-sys-color-on-surface-variant: #49454F;
  --md-sys-color-surface-container-lowest: #FFFFFF;
  --md-sys-color-surface-container-low: #F7F2FA;
  --md-sys-color-surface-container: #F3EDF7;
  --md-sys-color-surface-container-high: #ECE6F0;
  --md-sys-color-surface-container-highest: #E6E0E9;
  --md-sys-color-surface-dim: #DED8E1;
  --md-sys-color-surface-bright: #FEF7FF;
  --md-sys-color-outline: #79747E;
  --md-sys-color-outline-variant: #CAC4D0;
  --md-sys-color-inverse-surface: #322F35;
  --md-sys-color-inverse-on-surface: #F5EFF7;
  --md-sys-color-inverse-primary: #D0BCFF;
}
```

### Dark

```css
@media (prefers-color-scheme: dark) {
  :root {
    --md-sys-color-primary: #D0BCFF;
    --md-sys-color-on-primary: #381E72;
    --md-sys-color-primary-container: #4F378B;
    --md-sys-color-on-primary-container: #EADDFF;
    --md-sys-color-secondary: #CCC2DC;
    --md-sys-color-on-secondary: #332D41;
    --md-sys-color-secondary-container: #4A4458;
    --md-sys-color-on-secondary-container: #E8DEF8;
    --md-sys-color-tertiary: #EFB8C8;
    --md-sys-color-on-tertiary: #492532;
    --md-sys-color-tertiary-container: #633B48;
    --md-sys-color-on-tertiary-container: #FFD8E4;
    --md-sys-color-error: #F2B8B5;
    --md-sys-color-on-error: #601410;
    --md-sys-color-error-container: #8C1D18;
    --md-sys-color-on-error-container: #F9DEDC;
    --md-sys-color-surface: #141218;
    --md-sys-color-on-surface: #E6E0E9;
    --md-sys-color-on-surface-variant: #CAC4D0;
    --md-sys-color-surface-container-lowest: #0F0D13;
    --md-sys-color-surface-container-low: #1D1B20;
    --md-sys-color-surface-container: #211F26;
    --md-sys-color-surface-container-high: #2B2930;
    --md-sys-color-surface-container-highest: #36343B;
    --md-sys-color-surface-dim: #141218;
    --md-sys-color-surface-bright: #3B383E;
    --md-sys-color-outline: #938F99;
    --md-sys-color-outline-variant: #49454F;
    --md-sys-color-inverse-surface: #E6E0E9;
    --md-sys-color-inverse-on-surface: #322F35;
    --md-sys-color-inverse-primary: #6750A4;
  }
}
```

## Verification

Before delivering MD3 markup, scan for:

1. Any raw hex value outside the `:root { ... }` block that defines tokens. `grep -nE '#[0-9a-fA-F]{3,8}' file.css` should only return lines inside the `:root` declarations.
2. Any color pairing outside the table above (e.g., `color: var(--md-sys-color-on-primary)` on a `surface-container` background).
3. Any use of `outline` on a divider, or `outline-variant` on a focus ring.

These checks compose with the MD3 compliance audit pattern in the broader skill.

<!-- End of TECH-01. MIT, adapted from material-3-skill (CWTI Ltd 2026). -->
