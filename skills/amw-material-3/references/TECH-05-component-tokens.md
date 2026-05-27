<!-- MIT — adapted from material-3-skill (Copyright (c) 2026 CWTI Ltd) -->
<!-- See LICENSE / source: material-3-skill-master/skills/material-3/references/component-catalog.md. -->

# TECH-05 — Per-component token mapping

Each MD3 component is defined by a set of **component-level tokens** (`--md-comp-{component}-{property}`) that resolve to system-level tokens (`--md-sys-color-*`, `--md-sys-shape-corner-*`, `--md-sys-typescale-*`). Overriding a component-level token only re-skins that one component without affecting the global theme.

This file documents the canonical token overrides for the most common MD3 web components, the equivalent Compose composables, and the spec-aligned CSS pattern for components without a `@material/web` implementation.

## Token override convention

Every web component exposes its tokens with the prefix `--md-{variant}-{component}-{property}`. Examples:

- `--md-filled-button-container-color`
- `--md-outlined-button-label-text-color`
- `--md-fab-container-shape`
- `--md-outlined-text-field-focus-outline-color`

Set them on the component (or any ancestor) to re-theme one variant locally:

```css
md-filled-button {
  --md-filled-button-container-color: var(--md-sys-color-tertiary);
  --md-filled-button-label-text-color: var(--md-sys-color-on-tertiary);
}
```

## Buttons

### Filled button (`md-filled-button`)

Resting: container `primary`, label `on-primary`, shape `full`, height 40dp.

```css
md-filled-button {
  --md-filled-button-container-color: var(--md-sys-color-primary);
  --md-filled-button-label-text-color: var(--md-sys-color-on-primary);
  --md-filled-button-container-shape: var(--md-sys-shape-corner-full);
  --md-filled-button-container-height: 40px;
  --md-filled-button-label-text-font: var(--md-sys-typescale-label-large-font);
  --md-filled-button-label-text-size: var(--md-sys-typescale-label-large-size);
  --md-filled-button-label-text-weight: var(--md-sys-typescale-label-large-weight);
  --md-filled-button-hover-state-layer-color: var(--md-sys-color-on-primary);
  --md-filled-button-hover-state-layer-opacity: 0.08;
  --md-filled-button-focus-state-layer-opacity: 0.10;
  --md-filled-button-pressed-state-layer-opacity: 0.10;
}
```

### Outlined button (`md-outlined-button`)

Resting: container transparent, label `primary`, border `outline`, shape `full`.

```css
md-outlined-button {
  --md-outlined-button-label-text-color: var(--md-sys-color-primary);
  --md-outlined-button-outline-color: var(--md-sys-color-outline);
  --md-outlined-button-outline-width: 1px;
  --md-outlined-button-container-shape: var(--md-sys-shape-corner-full);
  --md-outlined-button-container-height: 40px;
  --md-outlined-button-hover-state-layer-color: var(--md-sys-color-primary);
}
```

### Text button (`md-text-button`)

Resting: container transparent, label `primary`, shape `full`.

```css
md-text-button {
  --md-text-button-label-text-color: var(--md-sys-color-primary);
  --md-text-button-container-shape: var(--md-sys-shape-corner-full);
  --md-text-button-container-height: 40px;
  --md-text-button-hover-state-layer-color: var(--md-sys-color-primary);
}
```

### Elevated button (`md-elevated-button`)

Resting: container `surface-container-low` (elevation 1), label `primary`, shape `full`.

```css
md-elevated-button {
  --md-elevated-button-container-color: var(--md-sys-color-surface-container-low);
  --md-elevated-button-label-text-color: var(--md-sys-color-primary);
  --md-elevated-button-container-shape: var(--md-sys-shape-corner-full);
  --md-elevated-button-container-height: 40px;
  --md-elevated-button-container-elevation: 1;
}
```

### Filled tonal button (`md-filled-tonal-button`)

Resting: container `secondary-container`, label `on-secondary-container`, shape `full`.

```css
md-filled-tonal-button {
  --md-filled-tonal-button-container-color: var(--md-sys-color-secondary-container);
  --md-filled-tonal-button-label-text-color: var(--md-sys-color-on-secondary-container);
  --md-filled-tonal-button-container-shape: var(--md-sys-shape-corner-full);
  --md-filled-tonal-button-container-height: 40px;
}
```

## FAB and extended FAB

### FAB (`md-fab`)

Resting: container `primary-container`, icon `on-primary-container`, shape `large` (16dp), elevation 3.

| Size | Token override |
|------|----------------|
| Small | `--md-fab-container-height: 40px; --md-fab-container-width: 40px;` |
| Medium (default) | `56px x 56px` |
| Large | `96px x 96px` (use `--md-sys-shape-corner-extra-large` shape) |

```css
md-fab {
  --md-fab-container-color: var(--md-sys-color-primary-container);
  --md-fab-icon-color: var(--md-sys-color-on-primary-container);
  --md-fab-container-shape: var(--md-sys-shape-corner-large);
  --md-fab-container-elevation: 3;
}
```

Color variants: `surface` (uses `surface-container-high`), `primary`, `secondary`, `tertiary`. Set via the `variant` attribute on the element.

### Extended FAB (`md-extended-fab`)

Same colors as FAB, with `Label Large` text + leading icon.

```css
md-extended-fab {
  --md-extended-fab-container-color: var(--md-sys-color-primary-container);
  --md-extended-fab-label-text-color: var(--md-sys-color-on-primary-container);
  --md-extended-fab-container-shape: var(--md-sys-shape-corner-large);
  --md-extended-fab-container-height: 56px;
  --md-extended-fab-label-text-font: var(--md-sys-typescale-label-large-font);
}
```

## Icon button

### Standard icon button (`md-icon-button`)

Container transparent, icon `on-surface-variant`, shape `full`, 40x40dp.

```css
md-icon-button {
  --md-icon-button-icon-color: var(--md-sys-color-on-surface-variant);
  --md-icon-button-state-layer-shape: var(--md-sys-shape-corner-full);
  --md-icon-button-state-layer-height: 40px;
  --md-icon-button-state-layer-width: 40px;
  --md-icon-button-icon-size: 24px;
}
```

Variants: `filled` (uses `primary` container), `filled-tonal` (uses `secondary-container`), `outlined` (transparent container, `outline` border).

## Card

### Outlined card

```css
.md3-card--outlined {
  background: var(--md-sys-color-surface);
  border: 1px solid var(--md-sys-color-outline-variant);
  border-radius: var(--md-sys-shape-corner-medium);
  color: var(--md-sys-color-on-surface);
  padding: 16px;
}
```

### Filled card

```css
.md3-card--filled {
  background: var(--md-sys-color-surface-container-highest);
  border-radius: var(--md-sys-shape-corner-medium);
  color: var(--md-sys-color-on-surface);
  padding: 16px;
}
```

### Elevated card

```css
.md3-card--elevated {
  background: var(--md-sys-color-surface-container-low);   /* tonal elevation level 1 */
  border-radius: var(--md-sys-shape-corner-medium);
  color: var(--md-sys-color-on-surface);
  padding: 16px;
  /* No shadow at rest. Add on :hover only if over busy content. */
}
```

## Text fields

### Outlined text field (`md-outlined-text-field`)

```css
md-outlined-text-field {
  --md-outlined-text-field-container-shape: var(--md-sys-shape-corner-small);
  --md-outlined-text-field-outline-color: var(--md-sys-color-outline);
  --md-outlined-text-field-focus-outline-color: var(--md-sys-color-primary);
  --md-outlined-text-field-focus-outline-width: 2px;
  --md-outlined-text-field-error-outline-color: var(--md-sys-color-error);
  --md-outlined-text-field-input-text-color: var(--md-sys-color-on-surface);
  --md-outlined-text-field-input-text-font: var(--md-sys-typescale-body-large-font);
  --md-outlined-text-field-input-text-size: var(--md-sys-typescale-body-large-size);
  --md-outlined-text-field-label-text-color: var(--md-sys-color-on-surface-variant);
  --md-outlined-text-field-focus-label-text-color: var(--md-sys-color-primary);
}
```

### Filled text field (`md-filled-text-field`)

```css
md-filled-text-field {
  --md-filled-text-field-container-color: var(--md-sys-color-surface-container-highest);
  --md-filled-text-field-container-shape-start-start: var(--md-sys-shape-corner-small);
  --md-filled-text-field-container-shape-start-end: var(--md-sys-shape-corner-small);
  --md-filled-text-field-container-shape-end-end: 0;
  --md-filled-text-field-container-shape-end-start: 0;
  --md-filled-text-field-active-indicator-color: var(--md-sys-color-on-surface-variant);
  --md-filled-text-field-focus-active-indicator-color: var(--md-sys-color-primary);
  --md-filled-text-field-focus-active-indicator-height: 2px;
}
```

Note the asymmetric corner shape: filled text fields have rounded top corners and a flat bottom edge (where the active indicator line sits).

## Top app bar

### Small top app bar

```css
.md3-top-app-bar {
  height: 64px;
  padding: 0 4px 0 16px;
  background: var(--md-sys-color-surface);   /* elevation 0 — flat */
  color: var(--md-sys-color-on-surface);
  display: flex;
  align-items: center;
  gap: 24px;
}
.md3-top-app-bar__title {
  font-family: var(--md-sys-typescale-title-large-font);
  font-size: var(--md-sys-typescale-title-large-size);
  font-weight: var(--md-sys-typescale-title-large-weight);
  line-height: var(--md-sys-typescale-title-large-line-height);
  flex: 1;
}
```

### Scrolled state

When the page scrolls, swap to `surface-container` (elevation 2):

```css
.md3-top-app-bar--scrolled {
  background: var(--md-sys-color-surface-container);
}
```

Variants: Center-Aligned (title centered, 64dp), Medium (112dp tall, large title), Large (152dp tall, hero-style title).

## Navigation

### Navigation bar (bottom, mobile)

```css
.md3-nav-bar {
  height: 80px;
  background: var(--md-sys-color-surface-container);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 12px 0 16px;
}
.md3-nav-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 0 12px;
}
.md3-nav-tab__icon-pill {
  width: 64px;
  height: 32px;
  border-radius: var(--md-sys-shape-corner-large);
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
}
.md3-nav-tab--active .md3-nav-tab__icon-pill {
  background: var(--md-sys-color-secondary-container);
}
.md3-nav-tab__label {
  font: var(--md-sys-typescale-label-medium-weight)
        var(--md-sys-typescale-label-medium-size) /
        var(--md-sys-typescale-label-medium-line-height)
        var(--md-sys-typescale-label-medium-font);
  color: var(--md-sys-color-on-surface-variant);
}
.md3-nav-tab--active .md3-nav-tab__label {
  color: var(--md-sys-color-on-secondary-container);
}
```

### Navigation rail (tablet portrait, foldable)

```css
.md3-nav-rail {
  width: 80px;
  background: var(--md-sys-color-surface);
  border-right: 1px solid var(--md-sys-color-outline-variant);
  padding-top: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}
```

### Navigation drawer (expanded / desktop)

```css
.md3-nav-drawer {
  width: 360px;
  background: var(--md-sys-color-surface-container-low);
  padding: 12px;
  border-radius: 0 var(--md-sys-shape-corner-large) var(--md-sys-shape-corner-large) 0;
}
```

## Dialog

```css
.md3-dialog {
  background: var(--md-sys-color-surface-container-high);   /* elevation 3 */
  border-radius: var(--md-sys-shape-corner-extra-large);
  padding: 24px;
  max-width: 560px;
  min-width: 280px;
  color: var(--md-sys-color-on-surface);
}
.md3-dialog__headline {
  font: var(--md-sys-typescale-headline-small-weight)
        var(--md-sys-typescale-headline-small-size) /
        var(--md-sys-typescale-headline-small-line-height)
        var(--md-sys-typescale-headline-small-font);
  color: var(--md-sys-color-on-surface);
  margin-bottom: 16px;
}
.md3-dialog__body {
  font: var(--md-sys-typescale-body-medium-weight)
        var(--md-sys-typescale-body-medium-size) /
        var(--md-sys-typescale-body-medium-line-height)
        var(--md-sys-typescale-body-medium-font);
  color: var(--md-sys-color-on-surface-variant);
}
.md3-dialog__actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 24px;
}
```

## Snackbar

```css
.md3-snackbar {
  background: var(--md-sys-color-inverse-surface);
  color: var(--md-sys-color-inverse-on-surface);
  border-radius: var(--md-sys-shape-corner-extra-small);
  padding: 14px 16px;
  min-height: 48px;
  max-width: 560px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.md3-snackbar__action {
  color: var(--md-sys-color-inverse-primary);
  font: var(--md-sys-typescale-label-large-weight)
        var(--md-sys-typescale-label-large-size) /
        var(--md-sys-typescale-label-large-line-height)
        var(--md-sys-typescale-label-large-font);
}
```

## Chips

```css
md-assist-chip,
md-filter-chip,
md-input-chip,
md-suggestion-chip {
  --md-chip-container-shape: var(--md-sys-shape-corner-small);
  --md-chip-container-height: 32px;
  --md-chip-label-text-font: var(--md-sys-typescale-label-large-font);
  --md-chip-label-text-size: var(--md-sys-typescale-label-large-size);
  --md-chip-label-text-color: var(--md-sys-color-on-surface);
  --md-chip-outline-color: var(--md-sys-color-outline);
}
md-filter-chip[selected] {
  --md-filter-chip-selected-container-color: var(--md-sys-color-secondary-container);
  --md-filter-chip-selected-label-text-color: var(--md-sys-color-on-secondary-container);
}
```

## Switch and checkbox

### Switch (`md-switch`)

```css
md-switch {
  --md-switch-track-shape: var(--md-sys-shape-corner-full);
  --md-switch-track-height: 32px;
  --md-switch-track-width: 52px;
  --md-switch-track-outline-color: var(--md-sys-color-outline);
  --md-switch-selected-track-color: var(--md-sys-color-primary);
  --md-switch-selected-handle-color: var(--md-sys-color-on-primary);
  --md-switch-handle-color: var(--md-sys-color-outline);
}
```

### Checkbox (`md-checkbox`)

```css
md-checkbox {
  --md-checkbox-selected-container-color: var(--md-sys-color-primary);
  --md-checkbox-selected-icon-color: var(--md-sys-color-on-primary);
  --md-checkbox-outline-color: var(--md-sys-color-on-surface-variant);
  --md-checkbox-container-shape: var(--md-sys-shape-corner-extra-small);
}
```

## Compose component mapping

| Web component | Compose composable | Flutter widget |
|---------------|---------------------|-----------------|
| `md-filled-button` | `Button` | `FilledButton` |
| `md-outlined-button` | `OutlinedButton` | `OutlinedButton` |
| `md-text-button` | `TextButton` | `TextButton` |
| `md-elevated-button` | `ElevatedButton` | `ElevatedButton` |
| `md-filled-tonal-button` | `FilledTonalButton` | `FilledButton.tonal` |
| `md-fab` | `FloatingActionButton` | `FloatingActionButton` |
| `md-extended-fab` | `ExtendedFloatingActionButton` | `FloatingActionButton.extended` |
| `md-icon-button` | `IconButton` | `IconButton` |
| `md-filled-text-field` | `TextField` | `TextField` |
| `md-outlined-text-field` | `OutlinedTextField` | `TextField` (decoration: outlined) |
| `md-dialog` | `AlertDialog` / `Dialog` | `AlertDialog` |
| `md-list` / `md-list-item` | `LazyColumn` + `ListItem` | `ListTile` |
| `md-navigation-bar` | `NavigationBar` | `NavigationBar` |
| `md-tabs` / `md-primary-tab` | `TabRow` + `Tab` | `TabBar` + `Tab` |
| `md-switch` | `Switch` | `Switch` |
| `md-checkbox` | `Checkbox` | `Checkbox` |
| `md-radio` | `RadioButton` | `Radio` |
| `md-slider` | `Slider` | `Slider` |
| `md-menu` | `DropdownMenu` | `PopupMenuButton` |
| `md-linear-progress` | `LinearProgressIndicator` | `LinearProgressIndicator` |
| `md-circular-progress` | `CircularProgressIndicator` | `CircularProgressIndicator` |
| `md-divider` | `HorizontalDivider` / `VerticalDivider` | `Divider` |

## Component import on the web

Always import individual modules. Barrel imports include the entire library and balloon the bundle:

```js
// Good — only the components you need
import '@material/web/button/filled-button.js';
import '@material/web/textfield/outlined-text-field.js';
import '@material/web/icon/icon.js';

// Bad — pulls every component
import '@material/web';
```

## Verification

Before delivering MD3 component markup:

1. Each component's container background, label color, shape, height, and state-layer values resolve to `var(--md-sys-*)` tokens — no raw hex / px.
2. Component variants match the mapping table (button height 40dp, FAB shape `large`, chip shape `small`).
3. Per-component overrides use the canonical `--md-{variant}-{component}-{property}` token names, not invented ones.
4. Web component imports are individual, not barrel.
5. Dark mode is handled by the `:root` token overrides — components themselves do NOT need separate dark variants because they resolve their colors through tokens.

<!-- End of TECH-05. MIT, adapted from material-3-skill (CWTI Ltd 2026). -->
