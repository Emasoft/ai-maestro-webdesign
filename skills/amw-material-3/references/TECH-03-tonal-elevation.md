<!-- MIT — adapted from material-3-skill (Copyright (c) 2026 CWTI Ltd) -->
<!-- See LICENSE / source: material-3-skill-master/skills/material-3/references/typography-and-shape.md (§ Elevation). -->

# TECH-03 — Tonal elevation

## Table of Contents

- [The 5 elevation levels](#the-5-elevation-levels)
- [The surface-container ladder](#the-surface-container-ladder)
- [Why tonal, not shadow](#why-tonal-not-shadow)
- [When to add shadows on top](#when-to-add-shadows-on-top)
- [Hover and focus elevation increase](#hover-and-focus-elevation-increase)
- [Jetpack Compose](#jetpack-compose)
- [Flutter](#flutter)
- [Surface-tint role](#surface-tint-role)
- [Verification](#verification)

## Overview

In Material Design 3, elevation is communicated primarily through **tonal surface color**, not drop shadows. Higher elevation = a surface tinted with the primary color at a specific opacity. The result is that a "floating" card on a light background looks slightly more saturated/tinted than the page surface — this is the depth cue.

Drop shadows are still available, but they are reserved for the case where an element floats over visually busy content (e.g., a FAB over an image) and tonal-only elevation would be insufficient to separate the element from the background.

This file documents:
- The 5 elevation levels and their canonical dp heights
- The tonal-overlay opacity for each level
- The surface-container ladder that implements tonal elevation on the web
- When (and how) to use shadows in addition
- Compose `tonalElevation` parameter

## The 5 elevation levels

| Level | DP height | Tonal overlay (`primary` at ...) | Typical components at rest |
|-------|-----------|----------------------------------|------------------------------|
| **0** | 0 dp | 0% (no overlay) | App bar (flat), filled / tonal / outlined / text buttons, button groups, filled / outlined cards, carousels, chips, full-screen dialogs, icon buttons, lists, nav rail, segmented buttons, sliders, split buttons, tabs |
| **1** | 1 dp | +5% primary | Banners, modal bottom sheet, elevated button, elevated card, elevated chips, modal nav drawer, modal side sheet |
| **2** | 3 dp | +8% primary | App bar (scrolled), menus, nav bar, rich tooltips, toolbar |
| **3** | 6 dp | +11% primary | Date pickers, modal dialogs, extended FAB, FAB, FAB menu close button, search, time pickers |
| **4** | 8 dp | +12% primary | (hover/focus increase only — no resting component sits at level 4) |
| **5** | 12 dp | +14% primary | (hover/focus increase only) |

The dp values are conceptual depths in 3D z-space — they describe how Compose / Flutter resolve shadow penumbra width. On the web, the dp is informational; the **tonal overlay percentage** is the effective implementation knob.

## The surface-container ladder

On the web, MD3 implements tonal elevation through the 5-step surface-container ladder. Each step in the ladder *already* incorporates the primary-tint overlay at the appropriate opacity:

| Elevation | CSS token to use as background |
|-----------|---------------------------------|
| Level 0 | `var(--md-sys-color-surface)` |
| Level 1 | `var(--md-sys-color-surface-container-low)` |
| Level 2 | `var(--md-sys-color-surface-container)` |
| Level 3 | `var(--md-sys-color-surface-container-high)` |
| Level 4-5 | `var(--md-sys-color-surface-container-highest)` |

This is the canonical way to set elevation on a web component. Do NOT compute the overlay manually:

```css
/* GOOD — uses the pre-computed surface-container ladder */
.elevated-card {
  background: var(--md-sys-color-surface-container-low);
  border-radius: var(--md-sys-shape-corner-medium);
}

/* BAD — manually composites primary over surface, fragile under dynamic color */
.elevated-card-bad {
  background:
    linear-gradient(rgba(103, 80, 164, 0.05), rgba(103, 80, 164, 0.05)),
    #FEF7FF;
}
```

The surface-container tokens already encode the right tonal math for both light and dark schemes. Manual composition breaks under dynamic color (the seed changes, the overlay primary changes, the math you wrote is now wrong).

## Why tonal, not shadow

1. **Dark mode legibility.** Drop shadows on dark surfaces are nearly invisible. Tonal elevation works in both light and dark — higher elevation simply gets *lighter* tonal containers in dark mode (tone 4, 10, 12, 17, 22 across the ladder).
2. **GPU cost.** A `box-shadow` with significant blur is more expensive to composite than a flat background color. Tonal elevation has zero GPU cost.
3. **Accessibility.** Users with low vision read tonal differences more reliably than shadow penumbra. Tonal elevation is also more robust under high-contrast modes.
4. **Tonal coherence.** Every elevation step uses the same primary hue. The result is a more unified visual feel than shadows-on-grayscale, which can look stamped-on.

## When to add shadows on top

Tonal elevation is sufficient for resting components on a plain page surface. Add a drop shadow only when:

- The component floats over **visually busy content** (e.g., a FAB over a hero image, a dialog over a populated list).
- The component must read as **detached from its background** (e.g., a dragged card animating across a list).
- **Platform convention** explicitly expects shadows (some Android system components, certain corporate-brand override skins).

When adding shadows, use the following canonical MD3 shadow values. They are calibrated against the tonal overlay, so they look correct *on top of* the surface-container ladder:

```css
/* Level 1 — applied on top of surface-container-low */
box-shadow:
  0 1px 2px rgba(0, 0, 0, 0.3),
  0 1px 3px 1px rgba(0, 0, 0, 0.15);

/* Level 2 — applied on top of surface-container */
box-shadow:
  0 1px 2px rgba(0, 0, 0, 0.3),
  0 2px 6px 2px rgba(0, 0, 0, 0.15);

/* Level 3 — applied on top of surface-container-high */
box-shadow:
  0 4px 8px 3px rgba(0, 0, 0, 0.15),
  0 1px 3px rgba(0, 0, 0, 0.3);

/* Level 4 — hover/focus increase only */
box-shadow:
  0 6px 10px 4px rgba(0, 0, 0, 0.15),
  0 2px 3px rgba(0, 0, 0, 0.3);

/* Level 5 — hover/focus increase only */
box-shadow:
  0 8px 12px 6px rgba(0, 0, 0, 0.15),
  0 4px 4px rgba(0, 0, 0, 0.3);
```

Notice each shadow has two layers — a tight key-light shadow and a softer ambient fill. This matches the MD3 spec for "lifted" components.

In dark mode, shadows on dark backgrounds are nearly invisible. Most MD3 dark themes rely on tonal elevation alone in dark mode and skip the shadow layer entirely.

## Hover and focus elevation increase

Most interactive elevated components increase by **+1 level** on hover and focus:

| Component | Resting elevation | Hover / focus elevation |
|-----------|-------------------|--------------------------|
| FAB | 3 | 4 |
| Extended FAB | 3 | 4 |
| Elevated button | 1 | 2 |
| Elevated card (interactive) | 1 | 2 |
| Filled tonal button | 0 | 1 |

Implementation: swap the background token AND (if you're using a shadow on top) the shadow value, on `:hover` / `:focus-visible`. The transition uses the standard MD3 motion easing:

```css
.md3-fab {
  background: var(--md-sys-color-primary-container);
  /* Level 3 — when the FAB sits over busy content, add the shadow */
  box-shadow: 0 4px 8px 3px rgba(0, 0, 0, 0.15), 0 1px 3px rgba(0, 0, 0, 0.3);
  transition:
    box-shadow var(--md-sys-motion-duration-short4)
               var(--md-sys-motion-easing-standard);
}
.md3-fab:hover,
.md3-fab:focus-visible {
  /* Level 4 */
  box-shadow: 0 6px 10px 4px rgba(0, 0, 0, 0.15), 0 2px 3px rgba(0, 0, 0, 0.3);
}
```

If the component sits over a plain surface (no busy background), you can skip the shadow entirely and rely on the surface-container swap alone. The tonal hop from `primary-container` (FAB resting) is enough to communicate the level.

## Jetpack Compose

Compose exposes a `tonalElevation` parameter on `Surface`:

```kotlin
Surface(
    tonalElevation = 6.dp,    // level 3
    shadowElevation = 6.dp,   // adds shadow on top when needed
    shape = MaterialTheme.shapes.medium,
) {
    Text("Elevated content")
}
```

`tonalElevation` applies the primary-tint overlay internally. `shadowElevation` is independent — set it to the same dp value to add shadow, or leave it at 0.dp to use tonal-only. M3 components like `FloatingActionButton` and `Card` (Elevated variant) set both by default.

## Flutter

Flutter `Material(elevation: ...)` uses Material 2-style shadow elevation by default. To get MD3 tonal elevation, set `useMaterial3: true` and rely on `surfaceTint` on the `ColorScheme`:

```dart
Material(
  elevation: 6,
  color: Theme.of(context).colorScheme.surface,
  surfaceTintColor: Theme.of(context).colorScheme.surfaceTint,
  child: ...,
)
```

The `surfaceTint` default is the primary color; Flutter composites it at the right opacity for the given elevation value.

## Surface-tint role

`--md-sys-color-surface-tint` is a token that exists specifically to be the source color of the tonal overlay. It defaults to `primary` and rarely needs to be overridden, but in advanced theming you can set it to a custom hue to skew the elevation tint without changing the primary brand color.

```css
:root {
  --md-sys-color-surface-tint: var(--md-sys-color-primary);   /* default */
}
```

On the web, the surface-container ladder is pre-computed against `surface-tint` = `primary`. If you need a non-primary tint, generate a fresh ladder using `@material/material-color-utilities` with the new tint as input.

## Verification

Before delivering MD3 markup with elevation:

1. No `box-shadow` on resting cards / buttons / lists unless they sit over busy content. Use the surface-container ladder instead.
2. Elevation transitions reference `var(--md-sys-motion-duration-*)` and `var(--md-sys-motion-easing-*)`, not hardcoded `0.3s ease`.
3. Hover/focus elevation hops by exactly +1 level (don't jump from 1 to 3).
4. Dark mode shadows are minimal or omitted entirely.
5. `surface-tint` is `primary` unless the brief explicitly overrides it.

<!-- End of TECH-03. MIT, adapted from material-3-skill (CWTI Ltd 2026). -->
