---
name: TECH-css-modern-syntax
category: design-principles-process
source: clean-room synthesis from MDN / CSS Working Drafts (batch9 Wave 2 Round 3, T-175)
license: MIT (plugin-original under the plugin root LICENSE file)
also-in: TECH-css-variable-discipline.md (how tokens layer with these features); TECH-enterprise-system-overrides.md (3-tier tokens benefit from light-dark / oklch); TECH-named-color-shadow-techniques.md (oklch unlocks perceptual-uniform palettes); ai-slop-avoid.md (rejects raw screen primaries — oklch is the alternative)
---

# Modern CSS syntax — color, queries, scoping, transitions

## Table of contents

- [What it does](#what-it-does)
- [When this file fires](#when-this-file-fires)
- [Baseline-availability summary](#baseline-availability-summary)
- [Color features](#color-features)
  - [`oklch()` and `oklab()` — perceptual color spaces](#oklch-and-oklab--perceptual-color-spaces)
  - [`color-mix()` — programmatic tinting / shading](#color-mix--programmatic-tinting--shading)
  - [`light-dark()` — automatic dark-mode pairs](#light-dark--automatic-dark-mode-pairs)
  - [Relative color syntax — derive from a base](#relative-color-syntax--derive-from-a-base)
- [Container queries](#container-queries)
  - [`@container` — query the parent's size](#container--query-the-parents-size)
  - [Container query units (`cqw`, `cqh`, `cqi`, `cqb`)](#container-query-units-cqw-cqh-cqi-cqb)
- [Scoping and cascade control](#scoping-and-cascade-control)
  - [`@layer` — explicit cascade ordering](#layer--explicit-cascade-ordering)
  - [`@scope` — bounded style application](#scope--bounded-style-application)
  - [Native CSS nesting](#native-css-nesting)
- [Selector ergonomics](#selector-ergonomics)
  - [`:has()` — parent / sibling-aware selectors](#has--parent--sibling-aware-selectors)
  - [`:is()` and `:where()`](#is-and-where)
- [Transitions and motion](#transitions-and-motion)
  - [`@starting-style` — first-paint transitions](#starting-style--first-paint-transitions)
  - [View Transitions API](#view-transitions-api)
- [Anchor positioning](#anchor-positioning)
- [Tailwind v4 native-CSS features](#tailwind-v4-native-css-features)
- [Layout & viewport correctness](#layout--viewport-correctness)
  - [Dynamic viewport units — `100dvh`, never `100vh`](#dynamic-viewport-units--100dvh-never-100vh)
  - [CSS Grid for structure — not flexbox percentage math](#css-grid-for-structure--not-flexbox-percentage-math)
- [Fallback strategies](#fallback-strategies)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

Catalogues modern CSS features the plugin treats as **default-on** for any project targeting recent evergreen browsers (Chrome / Edge 120+, Firefox 121+, Safari 17.4+). Each entry includes baseline-availability status, the syntax, what it replaces, and a fallback strategy for older browsers when required.

## When this file fires

Read this file when:
- Writing any CSS that exceeds the basics — anything involving theming, dynamic color, container-sized components, scoped styles, or first-paint animation.
- Reviewing a colleague's CSS that uses old-school workarounds (CSS-in-JS for nesting, MQ-only responsiveness, JS for color tinting) — many of those are now native.
- Specifying a project's "browser support matrix" — most of the features below are baseline-shipping, but a handful still need fallback for Safari < 17.4 or for embedded WebViews.

Do NOT use this file for legacy IE-11 or pre-2023 browser targets — none of these features will work.

## Baseline-availability summary

Status as of late 2025. **Verify with caniuse.com or MDN for the project's specific target matrix before shipping** — this is a snapshot, not a contract.

| Feature | Baseline status | Safe to use unconditionally? |
|---|---|---|
| `oklch()` / `oklab()` | Newly available (≈ 2024) | Yes for modern targets; fallback to `hsl()` for older |
| `color-mix()` | Newly available (≈ 2024) | Yes for modern targets |
| `light-dark()` | Newly available (≈ 2024) | Yes for modern targets |
| Relative color syntax (`oklch(from var(--c) l c h)`) | Limited (Safari shipped 2024; older browsers no) | Provide fallback or progressive enhancement |
| `@container` (size queries) | Widely available (≈ 2023) | Yes |
| Container query units (cqw etc.) | Widely available | Yes |
| `@layer` | Widely available | Yes |
| `@scope` | Newly available (Chrome 2024, Safari 2024, Firefox arrived later) | Yes for evergreen-only; fallback to BEM scoping otherwise |
| Native nesting (`&`) | Widely available | Yes |
| `:has()` | Widely available (Firefox shipped 2024) | Yes |
| `:is()` / `:where()` | Widely available | Yes |
| `@starting-style` | Newly available (2024) | Yes for evergreen-only |
| View Transitions API (same-document) | Newly available (Chrome 2023, Safari 2024, Firefox in progress) | Use with `@supports` for cross-document |
| Anchor positioning (`anchor-name`, `position-anchor`) | Limited (Chrome 2023, others trailing) | Provide fallback with absolute positioning |

"Newly available" in baseline terminology means it shipped in all three engines but is < 30 months mature; "Widely available" means it's been ≥ 30 months since universal shipping. The plugin's default rule: **Newly available is safe for modern projects; the second tier (Limited / specific browsers only) needs an `@supports` query.**

## Color features

### `oklch()` and `oklab()` — perceptual color spaces

`oklch()` is the plugin's preferred color syntax for anything that isn't a fixed brand color. Unlike `hsl()`, `oklch()` is **perceptually uniform** — equal lightness values *look* equally bright across all hues, which `hsl()` does not deliver (HSL yellow at L=50% looks much brighter than HSL blue at L=50%).

```css
/* Old (hsl): equal lightness, unequal perceived brightness */
:root {
  --warn:    hsl(40 100% 50%);   /* looks bright */
  --danger:  hsl(0  100% 50%);   /* looks medium-dark */
}

/* New (oklch): equal lightness, equal perceived brightness */
:root {
  --warn:    oklch(65% 0.20 70);   /* yellow-orange, mid-bright */
  --danger:  oklch(65% 0.20 25);   /* red, same mid-bright */
  --info:    oklch(65% 0.20 230);  /* blue, same mid-bright */
}
```

Use OKLCH for any palette where consistent perceived brightness matters — status colors, chart series, semantic accents. Use OKLab (`oklch()`'s Cartesian sibling) only when you need to interpolate colors linearly; OKLCH is more intuitive for human authoring.

### `color-mix()` — programmatic tinting / shading

`color-mix()` blends two colors in a specified color space. The plugin uses it to generate hover / active / disabled variants without authoring 6 colors per accent.

```css
:root {
  --brand:        oklch(58% 0.18 250);
  --brand-hover:  color-mix(in oklch, var(--brand), black 8%);   /* 8% darker */
  --brand-active: color-mix(in oklch, var(--brand), black 16%);  /* 16% darker */
  --brand-bg:     color-mix(in oklch, var(--brand), white 90%);  /* very light tint */
  --brand-fg:     color-mix(in oklch, var(--brand), black 60%);  /* deep variant for text */
}
```

**Always specify the color space** (`in oklch`, `in oklab`, `in srgb`). Different spaces give different intermediate colors; OKLCH is the plugin's default because it preserves perceived hue while shifting lightness.

`color-mix()` replaces SCSS / Tailwind plugins that pre-generate shade palettes. The result is native, dynamic, and themeable through CSS variables.

### `light-dark()` — automatic dark-mode pairs

`light-dark(<light-value>, <dark-value>)` returns one of its two arguments based on the `color-scheme` property. This collapses dark-mode definitions from a separate `@media (prefers-color-scheme: dark)` block to a single per-token expression.

```css
:root {
  color-scheme: light dark;   /* opt in — required for light-dark() to work */

  --color-bg:    light-dark(#FFFFFF, #0A0A0A);
  --color-text:  light-dark(#0F172A, #F1F5F9);
  --color-line:  light-dark(oklch(90% 0 0), oklch(20% 0 0));
}
```

User-controlled overrides still work via `color-scheme: only light` or `only dark` on a subtree, and the global `prefers-color-scheme` media query still applies.

### Relative color syntax — derive from a base

Relative-color syntax extracts components of one color to produce another. Useful for theming systems where the team specifies a base and derives the rest.

```css
:root {
  --brand: oklch(58% 0.18 250);

  /* derived: same hue, lighter */
  --brand-200: oklch(from var(--brand) calc(l + 0.20) c h);

  /* derived: same hue, less chroma */
  --brand-muted: oklch(from var(--brand) l calc(c * 0.5) h);

  /* derived: same hue, hue-shift 30° */
  --brand-analog: oklch(from var(--brand) l c calc(h + 30));
}
```

This is the closest CSS has to SCSS's `darken($brand, 10%)` — but native, dynamic, and themeable. **Caveat.** Browser support is still settling; provide fallback colors via `@supports` when targeting Safari < 17 or older Firefox.

## Container queries

### `@container` — query the parent's size

`@container` lets a component change layout based on the *containing element's* size, not the viewport. This is the right primitive for component-driven design — a card knows it's in a narrow sidebar vs a wide main column without the parent telling it.

```css
.card-grid {
  container-type: inline-size;
  container-name: cards;
}

.card {
  display: grid;
  grid-template-columns: 1fr;
}

@container cards (min-width: 480px) {
  .card {
    grid-template-columns: 120px 1fr;
  }
}
```

The card switches from stacked to side-by-side at 480 px **of its container**, regardless of viewport width. The same card works in a sidebar and a main column without two separate media queries.

### Container query units (`cqw`, `cqh`, `cqi`, `cqb`)

Sized relative to the container, not the viewport:

| Unit | Meaning |
|---|---|
| `cqw` | 1% of container's width |
| `cqh` | 1% of container's height |
| `cqi` | 1% of container's inline size (writing-mode-aware) |
| `cqb` | 1% of container's block size |

Use `cqi` instead of `cqw` when authoring in a multilingual project — `cqi` adapts to the writing mode automatically (vertical for Japanese / Mongolian; horizontal otherwise).

## Scoping and cascade control

### `@layer` — explicit cascade ordering

`@layer` defines a named cascade layer; later layers win over earlier ones, regardless of selector specificity. Use it to defeat specificity wars and make third-party styles overridable.

```css
@layer reset, base, components, utilities;

@layer reset {
  * { box-sizing: border-box; margin: 0; }
}

@layer components {
  .button { padding: 8px 16px; border-radius: 6px; }
}

@layer utilities {
  .text-center { text-align: center !important; }
}
```

The order `reset, base, components, utilities` (declared once at the top) defines the cascade. `utilities` always wins over `components`, regardless of selector specificity. Tailwind v4 uses this internally; the plugin recommends explicit layering for any project larger than a single file.

### `@scope` — bounded style application

`@scope` restricts a rule's reach to a subtree. The classic use is preventing global styles from bleeding into a component slot.

```css
@scope (.user-content) to (.no-style) {
  /* applies to descendants of .user-content, but stops at .no-style barriers */
  p { margin-block: 1em; }
  a { color: var(--brand); text-decoration: underline; }
}
```

This is the modern alternative to BEM-prefix scoping (`.userContent__paragraph`) and to CSS-in-JS hashed class names. Browser support is still arriving in Firefox; provide BEM fallback for older targets.

### Native CSS nesting

Nesting is now part of CSS itself — no SCSS / PostCSS needed.

```css
.card {
  padding: 16px;
  background: var(--surface);

  & .title {
    font-weight: 600;
  }

  &:hover {
    background: var(--surface-hover);
  }

  @media (min-width: 768px) {
    padding: 24px;
  }
}
```

The `&` is required (unlike SCSS, which makes it optional). The plugin's house style: always use `&` even when SCSS would let you omit it, for clarity.

## Selector ergonomics

### `:has()` — parent / sibling-aware selectors

`:has()` selects elements based on what they *contain* or follow. This is the long-awaited "parent selector" plus much more.

```css
/* style a card differently when it contains a video */
.card:has(video) {
  aspect-ratio: 16 / 9;
}

/* style a form when any required field is empty */
form:has(input:required:placeholder-shown) .submit {
  opacity: 0.5;
}

/* style a list item when its sibling is focused */
li:has(+ li:focus-within) {
  border-bottom: 2px solid var(--brand);
}
```

`:has()` is widely available now (Firefox shipped in early 2024). Use it freely; the only caveat is performance — `:has()` is more expensive than simple selectors. Don't nest it inside heavy selectors that run on every element.

### `:is()` and `:where()`

Both group selectors. The difference: `:is()` takes the **highest specificity** of its arguments; `:where()` has **zero specificity**.

```css
/* :is() — useful for shortening */
:is(h1, h2, h3) {
  margin-block: 0;
}
/* equivalent to: h1, h2, h3 { margin-block: 0; } */

/* :where() — useful for low-specificity defaults */
:where(article p) {
  line-height: 1.6;
}
/* zero specificity — easily overridden by any p { } rule later */
```

Use `:where()` for design-system *defaults* the consumer should override without specificity battles. Use `:is()` for terse selector grouping.

## Transitions and motion

### `@starting-style` — first-paint transitions

`@starting-style` lets you transition from the styles an element has when it first becomes visible. Before this, fade-in-on-mount required JavaScript.

```css
.toast {
  opacity: 1;
  translate: 0;
  transition: opacity 0.2s, translate 0.2s;

  @starting-style {
    opacity: 0;
    translate: 0 -8px;
  }
}
```

The toast fades in and slides down on mount, with zero JS. Newly available; safe for modern targets.

### View Transitions API

Smooth, scripted transitions between page states. Two variants:

**Same-document** (`document.startViewTransition(callback)`) — animates DOM mutations:

```js
document.startViewTransition(() => {
  // Mutate the DOM here
  document.getElementById('view').innerHTML = newView;
});
```

The browser captures before / after snapshots and cross-fades automatically. Elements with `view-transition-name: <name>` get morph-style transitions between matching names on old and new DOM.

**Cross-document** (new in 2024–2025): transitions across navigation. Requires `@view-transition` declaration:

```css
@view-transition {
  navigation: auto;
}
```

Plus `view-transition-name` on shared elements (e.g. a hero image present on both pages). Browser support is rolling out; gate with `@supports (view-transition-name: x)` for now.

## Anchor positioning

`anchor-name` + `position-anchor` lets an element position itself relative to another, declaratively. Replaces a lot of "popper.js" use cases.

```css
.button {
  anchor-name: --button-anchor;
}

.tooltip {
  position: absolute;
  position-anchor: --button-anchor;
  top: anchor(bottom);
  left: anchor(center);
  translate: -50% 8px;
}
```

The tooltip is anchored to the button without JS. Chromium ships it; Firefox / Safari are catching up. Provide JS fallback for non-Chromium until late 2026.

## Tailwind v4 native-CSS features

Tailwind v4 exposes several of the features above directly as utilities:

| Tailwind v4 utility | Native CSS |
|---|---|
| `text-balance` | `text-wrap: balance` — balanced line lengths in headings |
| `text-pretty` | `text-wrap: pretty` — avoid orphans in body text |
| Color utilities | OKLCH-native default palette (instead of v3's HSL) |
| `bg-[color-mix(...)]` arbitrary values | `color-mix()` native |
| `@container` directive support | Native `@container` |
| `dark:` variant | Optionally backed by `light-dark()` instead of class toggle |

When the project uses Tailwind v4, prefer the utility syntax for legibility; reach for raw CSS only when the v4 utility doesn't exist for the feature you need.

```html
<h1 class="text-balance text-4xl font-display">
  Headlines wrap with balanced line lengths automatically
</h1>

<p class="text-pretty leading-relaxed">
  Body copy avoids leaving a single short word on the last line.
</p>
```

`text-balance` is the most impactful per character of code — every heading on a marketing page benefits, costs nothing.

## Layout & viewport correctness

Two construction defaults that prevent a recurring class of layout bugs. Both are "Widely available" — no `@supports` gate needed.

### Dynamic viewport units — `100dvh`, never `100vh`

For full-height heroes and sections, use `min-height: 100dvh`, not `height: 100vh`. On mobile Safari (and Chrome Android) the URL bar collapses and expands as the user scrolls, which changes what `100vh` resolves to *mid-scroll* — the layout jumps and the bottom of a `100vh` hero is clipped behind the address bar on first paint. `dvh` tracks the **dynamic** viewport, so the box stays stable across the bar's collapse/expand. Use `svh` / `lvh` only when you specifically want the small / large extreme locked. Pair with `min-height` (not `height`) so content taller than the viewport can still grow.

```css
.hero { min-height: 100dvh; }   /* stable across the iOS address-bar collapse */
```

This is why every starter-component in `starter-components/` already uses `100dvh`; fresh HTML must match.

### CSS Grid for structure — not flexbox percentage math

Build multi-column page structure with CSS Grid, not flexbox + percentage widths. `calc(33% - 1rem)` column math drifts: the per-item gap subtraction is approximate, the last item wraps or overflows at certain widths, and changing the gap means editing every width. Let the grid own the gaps:

```css
/* Don't: flexbox percentage math */
.features > * { flex: 0 0 calc(33% - 1rem); }

/* Do: grid owns the columns and the gaps */
.features { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
```

Flexbox is the right tool for *one-dimensional* content flow (a toolbar, a tag row, a wrapping button cluster) — not for the page's column skeleton. (The "three equal cards" layout itself is separately constrained by [ai-slop-avoid](../ai-slop-avoid.md) § III — Grid is *how* you build whatever asymmetric layout you choose, not a license for the 3-equal-card cliché.)

## Fallback strategies

For features that haven't reached "Widely available" yet, the plugin's pattern is **progressive enhancement with `@supports`**:

```css
/* Fallback first — works everywhere */
.brand {
  color: #2563EB;
}

/* Enhancement — only applies in browsers that support the syntax */
@supports (color: oklch(58% 0.18 250)) {
  .brand {
    color: oklch(58% 0.18 250);
  }
}
```

The fallback declares the value as a fixed sRGB color; the `@supports` block overrides with OKLCH where available. Older browsers see the fallback; newer browsers get the perceptually-uniform variant.

**Do not** detect features in JS and toggle CSS — `@supports` is faster, more reliable, and doesn't block render.

## Breaks if

- The team uses `oklch()` for fixed brand colors without an `@supports` fallback. Older browsers show the default `currentColor` or the previous declaration, which can be invisible or completely wrong.
- `color-mix()` is used without specifying the color space. The default is `srgb` interpolation, which produces dingy intermediates for highly-saturated brand colors — always specify `in oklch`.
- `@scope` is used as the project's primary scoping mechanism in a codebase that needs Firefox-before-2024 support. The styles silently apply globally in those browsers because the `@scope` rule is unknown and ignored.
- `:has()` is overused on heavy selectors (e.g. `body:has(video.autoplay)`) causing layout / paint performance regressions. The browser re-evaluates `:has()` on every relevant DOM mutation; scope it to the smallest reasonable parent.
- View Transitions are used for cross-document navigation without an `@supports` gate. Browsers that don't ship cross-document VT show no transition (acceptable) but the *declaration* itself may break older Safari parsers (unacceptable).
- The team uses `light-dark()` without setting `color-scheme: light dark` on `:root`. The function returns the *light* value unconditionally because the document's color scheme is unset.

## Cross-references

- [color-system.md](../color-system.md) — plugin default palette tokens, expressed in `oklch()`.
- [TECH-css-variable-discipline.md](TECH-css-variable-discipline.md) — how the 3-tier token system layers with the features above.
- [TECH-enterprise-system-overrides.md](TECH-enterprise-system-overrides.md) — `light-dark()` and `color-mix()` make per-tenant theming easier in multi-tenant SaaS.
- [TECH-named-color-shadow-techniques.md](TECH-named-color-shadow-techniques.md) — perceptually-uniform palettes via `oklch()`.
- [TECH-reduced-motion.md](TECH-reduced-motion.md) — `@starting-style` and View Transitions must respect `prefers-reduced-motion`.
- [TECH-cross-cultural-design.md](TECH-cross-cultural-design.md) — the Wu-Xing OKLCH palette uses the syntax documented here.
- [ai-slop-avoid.md](../ai-slop-avoid.md) — the plugin-wide rules against raw screen primaries; `oklch()` is the recommended alternative.
