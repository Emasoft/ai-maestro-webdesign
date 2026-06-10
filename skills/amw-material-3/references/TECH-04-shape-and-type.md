<!-- MIT — adapted from material-3-skill (Copyright (c) 2026 CWTI Ltd) -->
<!-- See LICENSE / source: material-3-skill-master/skills/material-3/references/typography-and-shape.md. -->

# TECH-04 — Shape scale, type scale, and the 4dp spatial grid

## Table of Contents

- [Shape: corner-radius scale](#shape-corner-radius-scale)
- [Type: the 15-style scale](#type-the-15-style-scale)
- [Spacing: the 4dp grid](#spacing-the-4dp-grid)
- [Verification](#verification)

## Overview

This file covers the three visual axes that anchor Material Design 3 layout:

- **Shape** — the 7-step corner-radius scale (+ `none` + `full`), used for buttons, cards, dialogs, sheets.
- **Type** — the 15-style type scale (5 categories x 3 sizes) and the 15 emphasized variants.
- **Spacing / grid** — the 4dp spatial grid that every component snaps to.

## Shape: corner-radius scale

The MD3 shape scale has 7 prescribed steps plus `none` and `full`. M3 Expressive (May 2025) adds 3 "increased" variants for larger surface treatments. The token name uses the prefix `--md-sys-shape-corner-*`.

| Token | Value (dp / px) | Default components |
|-------|------------------|---------------------|
| `none` | 0 | (custom — explicit flat) |
| `extra-small` | 4 | Snackbar |
| `small` | 8 | Text fields, menus, chips |
| `medium` | 12 | Cards |
| `large` | 16 | FAB, extended FAB, navigation drawer |
| `large-increased` | 20 | (Expressive — large hero cards) |
| `extra-large` | 28 | Dialogs, bottom sheets, side sheets |
| `extra-large-increased` | 32 | (Expressive — hero panels) |
| `extra-extra-large` | 48 | (Expressive — very large surfaces) |
| `full` | 9999px (effectively a pill) | Buttons, badges, sliders, switches, search bars |

### CSS

```css
:root {
  --md-sys-shape-corner-none: 0px;
  --md-sys-shape-corner-extra-small: 4px;
  --md-sys-shape-corner-small: 8px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-large: 16px;
  --md-sys-shape-corner-large-increased: 20px;
  --md-sys-shape-corner-extra-large: 28px;
  --md-sys-shape-corner-extra-large-increased: 32px;
  --md-sys-shape-corner-extra-extra-large: 48px;
  --md-sys-shape-corner-full: 9999px;
}

.md3-card    { border-radius: var(--md-sys-shape-corner-medium); }
.md3-button  { border-radius: var(--md-sys-shape-corner-full); }
.md3-dialog  { border-radius: var(--md-sys-shape-corner-extra-large); }
```

### Component shape mapping

| Component | Default shape token |
|-----------|---------------------|
| Buttons (filled / outlined / text / elevated / tonal) | `full` |
| Icon button | `full` |
| FAB | `large` (16) |
| Extended FAB | `large` (16) |
| Chips (assist / filter / input / suggestion) | `small` (8) |
| Cards (filled / outlined / elevated) | `medium` (12) |
| Dialogs | `extra-large` (28) |
| Text fields | `small` (top corners only — bottom flat for filled) |
| Menus | `small` (8) |
| Navigation drawer | `large` (16, end corners) |
| Bottom sheets | `extra-large` (28, top corners) |
| Side sheets | `extra-large` (28) |
| Snackbar | `extra-small` (4) |
| Badges | `full` |
| Sliders (handle) | `full` |
| Switch (track) | `full` |
| Tabs (indicator) | `full` (top corners) |
| Search bar / search view | `full` |

### Per-corner shape control

For components where only certain corners are rounded (text fields, bottom sheets, top app bar in landscape), use the long-form `border-radius`:

```css
/* Filled text field — top corners rounded, bottom flat */
.md3-text-field--filled {
  border-radius:
    var(--md-sys-shape-corner-small)   /* top-left */
    var(--md-sys-shape-corner-small)   /* top-right */
    0                                   /* bottom-right */
    0;                                  /* bottom-left */
}

/* Modal bottom sheet — top corners rounded */
.md3-bottom-sheet {
  border-radius:
    var(--md-sys-shape-corner-extra-large)
    var(--md-sys-shape-corner-extra-large)
    0
    0;
}
```

### Shape morphing (Expressive, Compose-first)

M3 Expressive introduced animated shape morphing — buttons that change shape on press, selected states that morph. This is **Compose-first** and is **not** implemented in `@material/web`. On the web, a CSS `transition` on `border-radius` provides a degraded approximation:

```css
.md3-button {
  border-radius: var(--md-sys-shape-corner-full);
  transition: border-radius var(--md-sys-motion-duration-short4)
              var(--md-sys-motion-easing-emphasized);
}
.md3-button:active {
  border-radius: var(--md-sys-shape-corner-small);
}
```

This is a compromise, not parity. True shape morphing uses a Bezier interpolation between two parameterized shape definitions, which CSS does not support.

## Type: the 15-style scale

MD3 uses 15 baseline type styles organized in 5 categories (Display / Headline / Title / Body / Label) x 3 sizes (Large / Medium / Small), plus 15 "emphasized" variants with higher weight.

### Baseline (default values, Roboto)

| Style | Font | Weight | Size (sp / rem) | Line height (sp / rem) | Tracking |
|-------|------|--------|-----------------|--------------------------|----------|
| Display Large | Roboto | 400 | 57 / 3.5625 | 64 / 4 | -0.25px |
| Display Medium | Roboto | 400 | 45 / 2.8125 | 52 / 3.25 | 0 |
| Display Small | Roboto | 400 | 36 / 2.25 | 44 / 2.75 | 0 |
| Headline Large | Roboto | 400 | 32 / 2 | 40 / 2.5 | 0 |
| Headline Medium | Roboto | 400 | 28 / 1.75 | 36 / 2.25 | 0 |
| Headline Small | Roboto | 400 | 24 / 1.5 | 32 / 2 | 0 |
| Title Large | Roboto | 400 | 22 / 1.375 | 28 / 1.75 | 0 |
| Title Medium | Roboto | 500 | 16 / 1 | 24 / 1.5 | 0.15px |
| Title Small | Roboto | 500 | 14 / 0.875 | 20 / 1.25 | 0.1px |
| Body Large | Roboto | 400 | 16 / 1 | 24 / 1.5 | 0.5px |
| Body Medium | Roboto | 400 | 14 / 0.875 | 20 / 1.25 | 0.25px |
| Body Small | Roboto | 400 | 12 / 0.75 | 16 / 1 | 0.4px |
| Label Large | Roboto | 500 | 14 / 0.875 | 20 / 1.25 | 0.1px |
| Label Medium | Roboto | 500 | 12 / 0.75 | 16 / 1 | 0.5px |
| Label Small | Roboto | 500 | 11 / 0.6875 | 16 / 1 | 0.5px |

**sp -> rem conversion:** assuming 16px root, `1sp = 1/16 rem`. So 16sp = 1rem, 14sp = 0.875rem, etc.

### Emphasized variants

Each baseline style has a paired emphasized version with **higher weight** (typically 500 -> 600 or 600 -> 700). Use emphasized for:
- Selected / active component states
- Primary action buttons
- Headlines that need extra weight
- Unread / important content

Swap the baseline token for the emphasized version:

```
md.sys.typescale.display-large          ->  md.sys.typescale.emphasized.display-large
md.sys.typescale.title-medium           ->  md.sys.typescale.emphasized.title-medium
md.sys.typescale.label-large            ->  md.sys.typescale.emphasized.label-large
```

### CSS tokens (per-axis)

Each style maps to 5 individual axis tokens:

```css
:root {
  /* Body Large */
  --md-sys-typescale-body-large-font: 'Roboto', 'Roboto Flex', system-ui, sans-serif;
  --md-sys-typescale-body-large-weight: 400;
  --md-sys-typescale-body-large-size: 1rem;
  --md-sys-typescale-body-large-line-height: 1.5rem;
  --md-sys-typescale-body-large-tracking: 0.03125rem;   /* 0.5px / 16 */

  /* Title Medium */
  --md-sys-typescale-title-medium-font: 'Roboto', sans-serif;
  --md-sys-typescale-title-medium-weight: 500;
  --md-sys-typescale-title-medium-size: 1rem;
  --md-sys-typescale-title-medium-line-height: 1.5rem;
  --md-sys-typescale-title-medium-tracking: 0.009375rem;

  /* Label Large (used for buttons) */
  --md-sys-typescale-label-large-font: 'Roboto', sans-serif;
  --md-sys-typescale-label-large-weight: 500;
  --md-sys-typescale-label-large-size: 0.875rem;
  --md-sys-typescale-label-large-line-height: 1.25rem;
  --md-sys-typescale-label-large-tracking: 0.00625rem;
}
```

### Applying a style

```css
.headline {
  font-family: var(--md-sys-typescale-headline-large-font);
  font-weight: var(--md-sys-typescale-headline-large-weight);
  font-size: var(--md-sys-typescale-headline-large-size);
  line-height: var(--md-sys-typescale-headline-large-line-height);
  letter-spacing: var(--md-sys-typescale-headline-large-tracking);
}
```

### Brand vs Plain typeface

MD3 separates type into two typeface roles:

- **Brand** (`--md-ref-typeface-brand`) — used for Display and Headline styles (expression-focused, larger sizes).
- **Plain** (`--md-ref-typeface-plain`) — used for Title, Body, and Label styles (readability-focused, smaller sizes).

Both default to Roboto / Roboto Flex. To customize:

```css
:root {
  --md-ref-typeface-brand: 'Outfit', 'Roboto', sans-serif;
  --md-ref-typeface-plain: 'Inter', 'Roboto', sans-serif;
}
```

The 15 type-scale tokens reference these via `--md-sys-typescale-*-font: var(--md-ref-typeface-brand)` (for Display / Headline) or `var(--md-ref-typeface-plain)` (for Title / Body / Label).

### Roboto Flex (variable font)

For modern MD3 implementations, Roboto Flex is the preferred typeface — a variable font with axes for `wght` (100..1000), `wdth` (25..151), `opsz` (8..144). It enables fine-grained weight modulation without shipping multiple font files.

```css
@font-face {
  font-family: 'Roboto Flex';
  src: url('RobotoFlex-Variable.woff2') format('woff2');
  font-weight: 100 1000;
  font-stretch: 25% 151%;
}
```

### Component type usage

| Component | Type style |
|-----------|------------|
| Button label | Label Large |
| Top app bar title | Title Large |
| Card title | Title Medium |
| Card supporting text | Body Medium |
| Navigation label | Label Medium |
| Dialog headline | Headline Small |
| Dialog body | Body Medium |
| Chip label | Label Large |
| Text field input | Body Large |
| Text field label (resting) | Body Large |
| Text field label (floating) | Body Small |
| List headline | Body Large |
| List supporting text | Body Medium |
| Snackbar text | Body Medium |
| Tooltip text | Body Small |
| Tab label | Title Small |
| Badge count | Label Small |

### Note on the "avoid Roboto" rule

The plugin's general AI-slop guidance (`amw-design-principles/ai-slop-avoid.md`) warns against using Roboto as a default body face. That rule **does NOT apply** when the user explicitly asked for MD3 — in MD3, Roboto / Roboto Flex IS the correct default. Replace only when the user supplies a brand typeface.

## Spacing: the 4dp grid

Every MD3 layout sits on a **4dp grid**. All padding, margin, and gap values are multiples of 4dp. The default step is 8dp (`8dp / 0.5rem` on the web).

### Spacing tokens

```css
:root {
  --md-sys-spacing-0: 0;
  --md-sys-spacing-1: 4px;     /* 0.25rem */
  --md-sys-spacing-2: 8px;     /* 0.5rem  — default step */
  --md-sys-spacing-3: 12px;    /* 0.75rem */
  --md-sys-spacing-4: 16px;    /* 1rem    — standard container padding */
  --md-sys-spacing-5: 20px;
  --md-sys-spacing-6: 24px;    /* 1.5rem */
  --md-sys-spacing-7: 28px;
  --md-sys-spacing-8: 32px;    /* 2rem */
  --md-sys-spacing-10: 40px;
  --md-sys-spacing-12: 48px;   /* 3rem    — minimum touch target */
  --md-sys-spacing-14: 56px;
  --md-sys-spacing-16: 64px;   /* 4rem */
  --md-sys-spacing-20: 80px;
  --md-sys-spacing-24: 96px;
}
```

### Standard component spacing

| Component / context | Padding |
|---------------------|---------|
| Button (filled / outlined / tonal / elevated) | `10px 24px` (vertical / horizontal) |
| Text button | `10px 12px` |
| Icon button | `8px` (square, total 40x40 with 24px icon) |
| FAB | `16px` (square, 56x56) |
| Card | `16px` (content); `8px 16px 16px` (with actions row at bottom) |
| Dialog | `24px` (content); `24px 24px 8px` (with action row spacing) |
| Snackbar | `8px 16px` |
| Top app bar | `0 16px` (horizontal); `64px` height |
| List item (single line) | `16px` horizontal; `48px` minimum height |
| List item (two-line) | `16px` horizontal; `64px` minimum height |
| List item (three-line) | `16px` horizontal; `88px` minimum height |
| Navigation bar item | `12px 0`; `80px` height total |
| Section gap (between cards in a grid) | `16px` |
| Page padding (mobile compact) | `16px` |
| Page padding (medium / expanded) | `24px` or `32px` |

### Window size classes (breakpoints)

MD3 defines 5 window size classes that drive layout adaptation:

| Class | Width range | Typical device |
|-------|-------------|----------------|
| Compact | < 600 dp | Phone portrait |
| Medium | 600 .. 839 dp | Tablet portrait, foldable closed |
| Expanded | 840 .. 1199 dp | Tablet landscape, foldable open, laptop |
| Large | 1200 .. 1599 dp | Desktop, large monitor |
| Extra-Large | >= 1600 dp | Ultra-wide, TV |

On the web, map these to media queries:

```css
@media (min-width: 600px)  { /* medium and up */ }
@media (min-width: 840px)  { /* expanded and up */ }
@media (min-width: 1200px) { /* large and up */ }
@media (min-width: 1600px) { /* extra-large */ }
```

### Maximum content width

On Large (1200dp+) and Extra-Large (1600dp+) windows, constrain text content to **840-1040 dp** (`52.5-65 rem` at 16px root). Endless-width text lines are unreadable. Use a centered container with a `max-width`:

```css
.md3-content {
  max-width: 65rem;   /* 1040dp */
  margin-inline: auto;
  padding-inline: var(--md-sys-spacing-6);   /* 24px */
}
```

## Verification

Before delivering MD3 markup:

1. **Shape via tokens.** No `border-radius: 12px` or `border-radius: 1rem`. Always `border-radius: var(--md-sys-shape-corner-medium)`.
2. **Type via tokens.** No hardcoded `font-size: 16px`. Always `font-size: var(--md-sys-typescale-body-large-size)`.
3. **Spacing on the 4dp grid.** Every padding / margin / gap is a multiple of 4 (or, ideally, of 8). `padding: 13px 17px` is a violation.
4. **Component shape matches the mapping table.** Buttons use `full`, cards use `medium`, dialogs use `extra-large`.
5. **Component type style matches the mapping table.** Button labels use Label Large, card titles use Title Medium, etc.
6. **Page content has a max-width.** On wide viewports, text doesn't stretch edge to edge.

<!-- End of TECH-04. MIT, adapted from material-3-skill (CWTI Ltd 2026). -->
