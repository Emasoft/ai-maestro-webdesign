<!-- MIT — adapted from material-3-skill (Copyright (c) 2026 CWTI Ltd) -->
<!-- See LICENSE / source: material-3-skill-master/. State-layer mechanics consolidated from MD3 spec. -->

# TECH-02 — State layers (interaction states)

## Table of Contents

- [The 4 interaction states and their opacities](#the-4-interaction-states-and-their-opacities)
- [State-layer color selection (what color the overlay is)](#state-layer-color-selection-what-color-the-overlay-is)
- [CSS implementation (web, custom)](#css-implementation-web-custom)
- [Outlined / text variant — transparent resting](#outlined-text-variant-transparent-resting)
- [Jetpack Compose](#jetpack-compose)
- [`@material/web` component overrides](#materialweb-component-overrides)
- [Ripple](#ripple)
- [Accessibility gotchas](#accessibility-gotchas)
- [Verification](#verification)

In Material Design 3, every interactive surface — button, FAB, icon button, list item, navigation item, chip, switch, checkbox, radio — communicates its interaction state by overlaying a **translucent state layer** on top of its resting container color. The state layer is NOT a separate color; it is the appropriate "state-layer color" rendered at a specific opacity, composited over the container.

This file documents:
- The 4 interaction states + their canonical opacities
- The state-layer color selection rule per component variant
- Implementation patterns (CSS pseudo-element, Compose, web component overrides)
- Ripple behavior
- Accessibility gotchas

## The 4 interaction states and their opacities

| State | Opacity | When applied |
|-------|---------|--------------|
| Hover | **8%** | Pointer is over the interactive area; not pressed; not focused |
| Focus | **10%** | Element has keyboard / programmatic focus |
| Pressed | **10%** on web (`@material/web`) / **16%** on Android Compose / Flutter | Active during click / touch / Enter+Space |
| Dragged | **16%** | Component is being dragged (sliders, draggable cards) |

Hover + focus may *combine* visually when an element is both hovered and focused; both layers composite. The pressed layer replaces hover (it is "stronger"). Disabled state does NOT use a state layer — it dims the entire component (typically 38% opacity on text/icon, 12% on container).

> Note: the **16% pressed** value originates from Compose / native Android. The web `@material/web` implementation defaults to 10% pressed because the ripple animation supplements the static layer. When implementing pressed in custom web CSS (no ripple), prefer 12% as a balanced value.

## State-layer color selection (what color the overlay is)

The state-layer color depends on the *base variant* of the component. The rule is "use the color of the text/icon that sits on the container."

| Component variant | Resting container | State-layer color |
|-------------------|-------------------|-------------------|
| Filled button (`md-filled-button`) | `primary` | `on-primary` |
| Filled tonal button (`md-filled-tonal-button`) | `secondary-container` | `on-secondary-container` |
| Outlined button (`md-outlined-button`) | transparent (`surface`) | `primary` |
| Text button (`md-text-button`) | transparent (`surface`) | `primary` |
| Elevated button (`md-elevated-button`) | `surface-container-low` | `primary` |
| FAB (`md-fab`) | `primary-container` | `on-primary-container` |
| Filled icon button | `primary` | `on-primary` |
| Filled tonal icon button | `secondary-container` | `on-secondary-container` |
| Outlined icon button | transparent | `on-surface-variant` |
| Standard icon button | transparent | `on-surface-variant` |
| Card (filled) | `surface-container-highest` | `on-surface` |
| Card (elevated) | `surface-container-low` | `on-surface` |
| List item | `surface` | `on-surface` |
| Chip (assist / filter / input / suggestion) | `surface-container-low` / `secondary-container` | matches `on-*` of resting container |
| Navigation bar item (active) | indicator: `secondary-container` | `on-secondary-container` |
| Navigation bar item (inactive) | transparent | `on-surface-variant` |
| Navigation rail / drawer item | matches navigation bar | matches navigation bar |
| Tab (primary) | transparent | `primary` |
| Tab (secondary) | transparent | `on-surface` |
| Top app bar action | transparent | `on-surface` (or `on-primary` if app bar uses `primary` container) |
| Snackbar action | `inverse-surface` | `inverse-primary` |

The pattern: state-layer color is always the foreground text/icon color of the same component. This guarantees the overlay reads correctly against the container in all themes and contrast levels.

## CSS implementation (web, custom)

When you're not using `@material/web` and need to render a state layer manually, the canonical pattern is a `::before` pseudo-element that sits inside the component, sized to fill it, and whose opacity is driven by `:hover` / `:focus-visible` / `:active`:

```css
.md3-button {
  position: relative;
  overflow: hidden;            /* state-layer must clip to component shape */
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border-radius: var(--md-sys-shape-corner-full);
  isolation: isolate;           /* keep state-layer stacking local */
}

.md3-button::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--md-sys-color-on-primary);   /* state-layer color */
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--md-sys-motion-duration-short2)
              var(--md-sys-motion-easing-standard);
  z-index: -1;                  /* sit between background and content */
}

.md3-button:hover::before        { opacity: 0.08; }   /* 8% hover */
.md3-button:focus-visible::before { opacity: 0.10; }  /* 10% focus */
.md3-button:active::before        { opacity: 0.10; }  /* 10% pressed (web) */
```

Important notes:

- Use `:focus-visible`, not `:focus`. Otherwise click also triggers the focus layer and it stacks awkwardly with the press layer.
- `overflow: hidden` is mandatory — the pseudo-element fills the bounding box, so without clipping you'll get rectangular overflow on rounded buttons.
- `pointer-events: none` on the pseudo-element keeps hover/click events on the host element.
- Add `isolation: isolate` to keep the `z-index: -1` scoped to the component (prevents the layer from being hidden by ancestors with their own stacking context).
- Match the state-layer color to the variant — the rule "always use the `on-*` color of the resting container" never breaks.

### Combined hover+focus

When an element is both hovered AND focused, the spec layers them (8% + 10% composited). The easiest CSS approximation is to bump the opacity:

```css
.md3-button:hover:focus-visible::before { opacity: 0.18; }
```

This is the visual approximation; the exact composite would be `1 - (1 - 0.08)(1 - 0.10) = 0.172`. The 0.18 approximation is within visual tolerance.

## Outlined / text variant — transparent resting

For outlined and text buttons, the resting container is transparent (the parent's `surface` shows through). The state layer is still rendered, but its overlay color is `primary` (the same color as the label text). This produces a subtle "primary tint" on hover without filling the button.

```css
.md3-button--outlined {
  background: transparent;
  color: var(--md-sys-color-primary);
  border: 1px solid var(--md-sys-color-outline);
}
.md3-button--outlined::before {
  background: var(--md-sys-color-primary);   /* state-layer is primary, not on-primary */
}
```

## Jetpack Compose

Compose handles state layers automatically through `Modifier.indication(...)` and `LocalRippleConfiguration`. Default M3 components (Button, Card, ListItem, NavigationBarItem, etc.) wire this up; you don't add the layer manually. To customize:

```kotlin
CompositionLocalProvider(
    LocalRippleConfiguration provides RippleConfiguration(
        color = MaterialTheme.colorScheme.onPrimary,
        rippleAlpha = RippleAlpha(
            pressedAlpha = 0.16f,
            focusedAlpha = 0.10f,
            hoveredAlpha = 0.08f,
            draggedAlpha = 0.16f,
        )
    )
) {
    Button(onClick = {}) { Text("MD3") }
}
```

Compose uses `0.16f` for `pressedAlpha` natively. The web's 10% pressed value is a deliberate trade-off because the ripple supplements the static layer on touch devices.

## `@material/web` component overrides

When using web components, the state layer is built in but you can override the opacity tokens per component:

```css
md-filled-button {
  --md-filled-button-hover-state-layer-opacity: 0.08;
  --md-filled-button-focus-state-layer-opacity: 0.10;
  --md-filled-button-pressed-state-layer-opacity: 0.10;
  --md-filled-button-hover-state-layer-color: var(--md-sys-color-on-primary);
  --md-filled-button-pressed-state-layer-color: var(--md-sys-color-on-primary);
}
```

The same pattern repeats for `md-outlined-button`, `md-text-button`, `md-filled-tonal-button`, `md-elevated-button`, `md-icon-button` variants, `md-fab`, etc. — replace the prefix with the component name.

## Ripple

Ripples are a separate animated effect that runs on top of the state layer at the moment of click/touch. On the web (`@material/web`), ripples are part of the built-in `<md-ripple>` element. On Compose, ripples are part of the default `Modifier.indication(...)` configuration.

When implementing custom web CSS without a ripple library, the static pressed layer (opacity ~0.10) is the minimum acceptable approximation. Adding a ripple animation is optional polish — do NOT skip the state layer just because you don't have a ripple.

## Accessibility gotchas

1. **`:focus-visible`, not `:focus`.** Mouse-click on a button focuses it — using `:focus` makes the focus layer stick after every click, which looks broken. `:focus-visible` only fires for keyboard/programmatic focus.
2. **Touch targets >= 48dp / 48px regardless of visual size.** A small visual button can have invisible padding on top to reach the touch target. State layer must still clip to the visible bounds, not the padded touch target — otherwise hover triggers in the padding gap.
3. **Disabled state is NOT a state layer.** Apply opacity to the component itself (text 38%, container 12% or `surface-container-low`). Do NOT render hover/focus/pressed layers on disabled elements; they confuse screen readers and look broken.
4. **Reduced motion.** Honor `@media (prefers-reduced-motion: reduce)` by setting the state-layer `transition-duration` to 0 (the opacity still changes, but instantly — the layer still appears). Do NOT suppress the layer entirely; users with reduced motion still need to see interaction states.
5. **High contrast mode (Windows).** State layers may not render at all in `forced-colors: active` mode. Use the `:hover { outline: 2px solid Highlight }` pattern as a high-contrast fallback so interaction state is still communicated.

```css
@media (prefers-reduced-motion: reduce) {
  .md3-button::before { transition: none; }
}

@media (forced-colors: active) {
  .md3-button::before { display: none; }
  .md3-button:hover { outline: 2px solid Highlight; outline-offset: 2px; }
  .md3-button:focus-visible { outline: 2px solid Highlight; outline-offset: 2px; }
}
```

## Verification

Before delivering MD3 markup with custom state layers:

1. Every interactive component has a state layer wired up. Buttons without `:hover`, `:focus-visible`, `:active` overlays violate the system.
2. Opacities match the table (8 / 10 / 10..16 / 16) within +/-2%.
3. State-layer color matches the `on-*` foreground color of the same component (i.e. uses the same `var(--md-sys-color-*)` token, not a hardcoded value).
4. Disabled elements show no state layer.
5. `:focus-visible` used (not `:focus`).
6. `prefers-reduced-motion` + `forced-colors` fallbacks present.

<!-- End of TECH-02. MIT, adapted from material-3-skill (CWTI Ltd 2026). -->
