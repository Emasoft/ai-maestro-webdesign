---
name: amw-material-3
description: >-
  Material Design 3 (Material You) token reference: HCT tonal palettes,
  role-based color tokens, state layers, tonal elevation, shape scale, type
  styles, and the 4dp spatial grid. Activates on narrow triggers only:
  "material 3", "material design 3", "M3 tokens", "HCT palette", "tonal
  elevation", "state layer", "md-sys color", "MaterialTheme colors". Does NOT
  activate on generic "material design" or broad design vocabulary - those
  route to amw-design-principles.
author: ai-maestro-webdesign (direct-port from material-3-skill, MIT, CWTI Ltd 2026)
---

<!-- MIT — adapted from material-3-skill (Copyright (c) 2026 CWTI Ltd) -->
<!-- See LICENSE / source: material-3-skill-master (https://github.com/cwti-ltd). Reorganised for the ai-maestro-webdesign plugin. -->

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Activated when the user explicitly names Material 3 / MD3 / Material You as the target design system, or asks for HCT palette / state-layer / tonal-elevation / md-sys-* tokens. The orchestrator routes here; do not re-route generic design intent back to this skill.

## Scope

This skill ships the token-level reference for Material Design 3 (MD3). It covers what the design system *is* — every visual axis (color, type, shape, elevation, motion, spacing) expressed as machine-applicable CSS custom properties (`--md-sys-*`) and the platform mappings to `MaterialTheme.colorScheme` (Jetpack Compose) and `ColorScheme.fromSeed` (Flutter).

It does **not** ship: full component implementations, opinionated layout templates, or the M3 Expressive motion / shape-morph physics (that lives in Compose, not on the web). The companion preset `amw-design-system-presets/references/S-008-material-3.md` is a single self-contained token bundle drawn from this skill; use that preset when only a token block is needed.

## What MD3 brings (vs MD2)

- **HCT tonal palettes** replace fixed shade ramps. A single seed color generates 5 palettes (primary, secondary, tertiary, neutral, neutral-variant), each with 16 tonal stops along 0..100.
- **Role-based color tokens** (29+). `primary`, `on-primary`, `primary-container`, `surface-container-*`, `outline`, `outline-variant`, etc. Every container has a paired `on-*` text/icon color with guaranteed contrast.
- **Tonal surface elevation** replaces drop shadows. Higher elevation = a surface tinted with primary-color overlay (5% L1 -> 14% L5). Shadows only when an element floats over busy content.
- **State layers**: every interactive element overlays a translucent state color on top of its container — `8%` hover, `10%` focus, `12%` pressed (10% on web), `16%` dragged.
- **7-step shape scale** + `full` (pill). Buttons -> `full`; cards -> `medium` (12dp); FAB -> `large` (16dp); dialogs -> `extra-large` (28dp).
- **15 type styles** in 5 categories (Display / Headline / Title / Body / Label) x 3 sizes (L / M / S), plus 15 "emphasized" variants with higher weight.
- **4dp spatial grid** for all spacing tokens. Components snap to 4dp multiples; 8dp is the default margin/padding step.
- **3 contrast levels** (May 2025): standard / medium / high, generated from the same seed.

## Token namespace at a glance

| Axis | CSS prefix | Compose surface | Flutter surface |
|------|------------|-----------------|------------------|
| Color | `--md-sys-color-*` | `MaterialTheme.colorScheme.*` | `Theme.of(context).colorScheme.*` |
| Type | `--md-sys-typescale-*` | `MaterialTheme.typography.*` | `Theme.of(context).textTheme.*` |
| Shape | `--md-sys-shape-corner-*` | `MaterialTheme.shapes.*` | `Theme.of(context).extension<MaterialShapes>()` |
| Motion | `--md-sys-motion-easing-*` / `--md-sys-motion-duration-*` | `MotionScheme.*` | `Theme.of(context).pageTransitionsTheme` |
| State layer | overlay opacity values (not tokens) | `LocalRippleConfiguration` | `Theme.of(context).splashColor` |
| Elevation | tonal overlay percentages on `primary` | `Surface(tonalElevation = ...dp)` | `Material(elevation: ..., color: Theme.of(context).colorScheme.surfaceTint)` |

## Quick-start: baseline light scheme

```css
:root {
  /* Core color roles (baseline purple seed #6750A4) */
  --md-sys-color-primary: #6750A4;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #EADDFF;
  --md-sys-color-on-primary-container: #21005D;
  --md-sys-color-secondary: #625B71;
  --md-sys-color-secondary-container: #E8DEF8;
  --md-sys-color-tertiary: #7D5260;
  --md-sys-color-tertiary-container: #FFD8E4;
  --md-sys-color-error: #B3261E;
  --md-sys-color-on-error: #FFFFFF;
  --md-sys-color-surface: #FEF7FF;
  --md-sys-color-on-surface: #1D1B20;
  --md-sys-color-on-surface-variant: #49454F;
  --md-sys-color-surface-container-lowest: #FFFFFF;
  --md-sys-color-surface-container-low: #F7F2FA;
  --md-sys-color-surface-container: #F3EDF7;
  --md-sys-color-surface-container-high: #ECE6F0;
  --md-sys-color-surface-container-highest: #E6E0E9;
  --md-sys-color-outline: #79747E;
  --md-sys-color-outline-variant: #CAC4D0;

  /* Shape */
  --md-sys-shape-corner-none: 0px;
  --md-sys-shape-corner-extra-small: 4px;
  --md-sys-shape-corner-small: 8px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-large: 16px;
  --md-sys-shape-corner-extra-large: 28px;
  --md-sys-shape-corner-full: 9999px;
}
```

Apply dark theme by overriding the same role tokens under `@media (prefers-color-scheme: dark)` — see [TECH-01-hct-palette](references/TECH-01-hct-palette.md).

## Decision tree

| If the user asks for ... | Read this reference |
|---|---|
| Color tokens / dynamic color / seed -> palette generation | [TECH-01-hct-palette](references/TECH-01-hct-palette.md) |
| Hover / focus / pressed overlay opacity, ripple values | [TECH-02-state-layers](references/TECH-02-state-layers.md) |
| Elevation, surface-tint overlay, when to use shadows | [TECH-03-tonal-elevation](references/TECH-03-tonal-elevation.md) |
| Shape scale, type scale, spacing grid | [TECH-04-shape-and-type](references/TECH-04-shape-and-type.md) |
| Per-component token mapping (button, card, text field, ...) | [TECH-05-component-tokens](references/TECH-05-component-tokens.md) |

## Hard rules MD3 enforces

These are non-negotiable when the user asks for MD3:

1. **No hardcoded colors.** Always reference `var(--md-sys-color-*)`. Hardcoded hex breaks dynamic color, dark mode, and the 3 contrast levels.
2. **Pair every container with its `on-*` partner.** `primary` always pairs with `on-primary`; `surface-container` with `on-surface` or `on-surface-variant`. Never mix arbitrary text colors on surface containers — it breaks contrast in dynamic and high-contrast modes.
3. **`outline` vs `outline-variant`** are not interchangeable. `outline` carries 3:1 contrast for interactive borders (text-field outlines). `outline-variant` is decorative (dividers, card borders).
4. **Elevation is tonal, not shadow.** Use the surface-container ladder. Drop shadows are only for elements that float over busy content (FAB over imagery).
5. **Shape via tokens.** `border-radius` always references `var(--md-sys-shape-corner-*)`, never a raw `px` value. Keeps shape consistent under theme overrides.
6. **State layers are overlays, not new colors.** A hovered button shows its base color + an 8%-opacity overlay of the appropriate state-layer color (`on-primary` for filled primary, `primary` for tonal/outlined/text). Never substitute a new color.
7. **4dp grid.** All spacing is a multiple of 4dp. Default step is 8dp. Components snap to the grid.
8. **No MD2 + MD3 mix.** Never import `@material/mdc-*` alongside `@material/web` or use legacy MD2 token names. APIs and shapes are incompatible.
9. **Roboto / Roboto Flex IS the MD3 typeface.** The plugin's general "avoid Roboto" guidance from `amw-design-principles/ai-slop-avoid.md` does NOT apply when the user explicitly asked for MD3 — Roboto is the correct default. Replace only when the user supplies a brand typeface.

## Anti-patterns

- Importing all of `@material/web` (barrel imports bloat the bundle). Always import one module per component used.
- Using `border-radius: 12px` instead of `var(--md-sys-shape-corner-medium)`.
- Setting `box-shadow: ...` on resting cards. Use `--md-sys-color-surface-container-low` (level 1 tonal elevation) instead.
- Applying `outline` to dividers — that's `outline-variant`.
- Generating multiple color schemes by hand instead of via `@material/material-color-utilities` + `themeFromSourceColor()`.
- Treating M3 Expressive as a web feature. M3 Expressive (spring physics, shape morphing, new button sizes XS..XL) is Compose-first; `@material/web` is in maintenance mode and does NOT implement the Expressive APIs. See the Google announcement for [Material Web maintenance status](https://m3.material.io/develop/web).

## Resources

- [TECH-01-hct-palette](references/TECH-01-hct-palette.md) — HCT model, seed-to-scheme generation, dynamic color, contrast levels, baseline light/dark schemes
> [TECH-01-hct-palette.md] HCT color space · The 5 tonal palettes · Role-to-tone mapping · Color pairing rules · Fixed accent colors (Add-on) · Dynamic color (user-generated) · Generating a scheme from a seed (JavaScript) · Color harmonization · User-controlled contrast (May 2025) · Baseline static schemes (no dynamic color) · Verification
- [TECH-02-state-layers](references/TECH-02-state-layers.md) — Interaction state overlays (hover 8% / focus 10% / pressed 16%), state-layer color selection per component, ripple guidance
> [TECH-02-state-layers.md] The 4 interaction states and their opacities · State-layer color selection (what color the overlay is) · CSS implementation (web, custom) · Outlined / text variant — transparent resting · Jetpack Compose · `@material/web` component overrides · Ripple · Accessibility gotchas · Verification
- [TECH-03-tonal-elevation](references/TECH-03-tonal-elevation.md) — 5 elevation levels mapped to surface-container ladder + tonal-overlay percentages, shadow values when needed
> [TECH-03-tonal-elevation.md] The 5 elevation levels · The surface-container ladder · Why tonal, not shadow · When to add shadows on top · Hover and focus elevation increase · Jetpack Compose · Flutter · Surface-tint role · Verification
- [TECH-04-shape-and-type](references/TECH-04-shape-and-type.md) — 7-step shape scale + `full`, 15 type styles + 15 emphasized, 4dp grid spacing tokens
> [TECH-04-shape-and-type.md] Shape: corner-radius scale · Type: the 15-style scale · Spacing: the 4dp grid · Verification
- [TECH-05-component-tokens](references/TECH-05-component-tokens.md) — Per-component token override patterns (button, FAB, card, text field, app bar, navigation, dialog, snackbar)
> [TECH-05-component-tokens.md] Token override convention · Component token tables — Buttons, FAB and extended FAB, Icon button, Card, Text fields, Top app bar, Navigation, Dialog, Snackbar, Chips, Switch and checkbox · Compose component mapping · Component import on the web · Verification

## Cross-references

- Companion preset (single-file token bundle for a quick apply): [S-008-material-3](../amw-design-system-presets/references/S-008-material-3.md)
> [S-008-material-3.md] Identity · Token block · "Breaks if" invariants · Canonical render-test pointer · Render-test verdict · Cross-references · Attribution
- Tokens companion file format for hand-off: `../amw-design-md/` (DESIGN.md emission with MD3 tokens)
- Orchestrator + AI-slop rules: [SKILL](../amw-design-principles/SKILL.md), [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md)
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)

<!-- End of amw-material-3 SKILL.md. MIT, adapted from material-3-skill (CWTI Ltd 2026). -->
