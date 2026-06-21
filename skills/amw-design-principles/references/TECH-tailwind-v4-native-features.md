---
name: TECH-tailwind-v4-native-features
category: design-principles-process
source: Tailwind v4 docs (direct-port with attribution, batch9 Wave 2 Round 4, T-176)
license: MIT (Tailwind v4 is MIT under upstream; plugin re-licenses under its own MIT — see ../../../LICENSE)
also-in: TECH-css-modern-syntax.md (oklch / color-mix / container queries; this file covers the Tailwind v4 surface specifically); TECH-css-variable-discipline.md (how Tailwind v4 @theme integrates with the plugin's 3-tier token system); TECH-enterprise-system-overrides.md (Tailwind v4 in a multi-brand context); ../../amw-tailwind-4/SKILL.md (the executor skill — this reference is the pre-read)
---

<!--
Sources: Tailwind CSS v4 documentation (MIT, https://tailwindcss.com/docs) — direct-port of the v4 native-CSS feature surface, theme-block syntax, color-feature integration, container queries, source directive. The Tailwind project is MIT-licensed; this plugin is also MIT (../../../LICENSE).
Synthesis novel to this plugin: the per-feature browser-support matrix, fallback strategies via @supports, the breaks-if invariants, and the cross-references to the wider amw-design-principles token system.
-->

# Tailwind v4 native-CSS features — what's new, when to use, fallback strategy

## Table of contents

- [What it does](#what-it-does)
- [When this file fires](#when-this-file-fires)
- [The five-line summary](#the-five-line-summary)
- [Browser-support matrix](#browser-support-matrix)
- [The `@theme` block — CSS-native config](#the-theme-block--css-native-config)
- [The `@source` directive — explicit content scanning](#the-source-directive--explicit-content-scanning)
- [`oklch()` colors and `color-mix()` — perceptual palettes](#oklch-colors-and-color-mix--perceptual-palettes)
- [`text-balance` and `text-wrap: pretty` — typesetting](#text-balance-and-text-wrap-pretty--typesetting)
- [Container queries — `@container` and `@xs:`/`@sm:` variants](#container-queries--container-and-xssm-variants)
- [The `--spacing()` function — derived spacing](#the---spacing-function--derived-spacing)
- [Native cascade layers — `@layer` ordering](#native-cascade-layers--layer-ordering)
- [Fallback strategies via `@supports`](#fallback-strategies-via-supports)
- [Worked example — production-ready button using all v4 features](#worked-example--production-ready-button-using-all-v4-features)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

Tailwind v4 is a near-rewrite of v3 that delegates more work to the browser's native CSS engine. The big architectural moves: configuration in CSS (not JavaScript), native CSS variables for every theme value, `oklch()` color by default, container queries as first-class, and a 5–10× faster build via the Rust-based Oxide engine.

This file documents only the features that are *new in v4* or *materially different from v3*. The wider v3-compatible feature set (utility classes, responsive variants, dark-mode prefix) is unchanged and lives in the executor skill `amw-tailwind-4/SKILL.md`.

## When this file fires

- The project uses Tailwind v4 (any `4.x` release) and the team wants to use the new features
- A v3 project is being migrated to v4 and the team needs to know which v4 features to adopt first
- The team is choosing between Tailwind v4 and a pure-CSS approach
- A component needs `oklch()` colors, `text-balance`, container queries, or `@theme`-based tokens

Do NOT read this file for:
- Pure v3 projects without a migration plan (read `amw-tailwind-4/SKILL.md` instead, which still covers v3-compatible utilities)
- Vanilla-CSS projects that don't use Tailwind at all (read `TECH-css-modern-syntax.md` for the underlying CSS features)

## The five-line summary

1. **Configuration moved to CSS.** `tailwind.config.js` is replaced by a `@theme { ... }` block inside your CSS. Every theme token becomes a real CSS variable.
2. **`oklch()` is the default color space.** All shipped palette tokens are `oklch()`; the perceptual-uniform spacing of lightness ramps is more even than the v3 HSL palette.
3. **Container queries are first-class.** `@xs:`, `@sm:`, `@md:` variants apply to the nearest `@container` ancestor, not the viewport.
4. **`@source` controls content scanning.** Replaces v3's `content: [...]` JS array. Explicitly opt-in to which files Tailwind scans for class names.
5. **The build is 5-10× faster.** The Oxide (Rust) engine replaces the v3 JavaScript scanner. Cold builds drop from 800ms to 50-100ms on medium projects.

## Browser-support matrix

| Feature | Chrome | Firefox | Safari | Notes |
|---|---|---|---|---|
| `oklch()` colors | 111+ | 113+ | 15.4+ | Wide support since mid-2023 |
| `color-mix()` | 111+ | 113+ | 16.2+ | Wide support since 2023 |
| `@container` (size queries) | 105+ | 110+ | 16+ | Wide support since 2022 |
| Container query units (`cqi`, `cqb`) | 105+ | 110+ | 16+ | Same support window |
| `text-wrap: balance` | 114+ | 121+ | 17.5+ | Universal since mid-2024 |
| `text-wrap: pretty` | 117+ | 121+ | 17.5+ | Chromium-led, others followed |
| Native CSS nesting | 112+ | 117+ | 16.5+ | Wide support since mid-2023 |
| `@layer` | 99+ | 97+ | 15.4+ | Universal since 2022 |
| `light-dark()` | 123+ | 120+ | 17.5+ | Newer; older browsers need `prefers-color-scheme` |
| `@property` (typed custom properties) | 85+ | 128+ | 16.4+ | Firefox lagged until late 2024 |
| `:has()` selector | 105+ | 121+ | 15.4+ | Universal since end-2023 |

The Tailwind v4 minimum stated targets are Chrome 111, Firefox 128, Safari 16.4 (released March 2025). Anything older than this gets the unprefixed Tailwind v3 build via the explicit migration path.

## The `@theme` block — CSS-native config

In v3, theme tokens lived in `tailwind.config.js`:

```js
// v3
module.exports = {
  theme: {
    colors: {
      brand: { 500: "#3b82f6" },
    },
    spacing: { 18: "4.5rem" },
  },
};
```

In v4, theme tokens live in the CSS itself:

```css
/* v4 */
@import "tailwindcss";

@theme {
  --color-brand-500: oklch(60% 0.18 250);
  --color-brand-600: oklch(55% 0.20 250);
  --color-brand-700: oklch(48% 0.20 250);

  --spacing-18: 4.5rem;

  --font-display: "Inter", system-ui, sans-serif;
}
```

Each `--color-*`, `--spacing-*`, `--font-*` etc. inside `@theme` becomes:
1. A standard CSS variable on `:root` (visible to runtime CSS)
2. A Tailwind utility class (`bg-brand-500`, `text-brand-700`, `space-18`)

This is the single biggest v4 win: no JS context-switch to change a theme value, no rebuild required to inspect a token, and the tokens live where the CSS lives.

### Plugin integration

The plugin's 3-tier token system (described in `TECH-css-variable-discipline.md`) maps directly onto `@theme`:

```css
@theme {
  /* Tier 1 — Primitives (raw values, not exposed as utilities) */
  --color-blue-500: oklch(60% 0.18 250);

  /* Tier 2 — Semantic (component-agnostic intent) */
  --color-brand-default: var(--color-blue-500);
  --color-brand-hover: oklch(55% 0.20 250);

  /* Tier 3 — Component (specific to a component family) */
  --color-button-primary-bg: var(--color-brand-default);
  --color-button-primary-bg-hover: var(--color-brand-hover);
}
```

In v4, all three tiers can live in the same `@theme` block. Tailwind generates utilities for every one (`bg-brand-default`, `bg-button-primary-bg`); use the semantic tier in 90% of cases and reach for primitives only at the token-binding layer.

## The `@source` directive — explicit content scanning

In v3, you told Tailwind which files to scan via the JS `content` array. In v4, you use `@source`:

```css
@import "tailwindcss";

/* Default: Tailwind auto-detects sources in your project root. */

/* If you have files outside the auto-detected paths: */
@source "../legacy-app/src/**/*.html";
@source "../node_modules/our-shared-lib/src/**/*.{ts,tsx}";

/* If you want to EXCLUDE something Tailwind would otherwise scan: */
@source not "./src/legacy/**/*";
```

The auto-detection in v4 is good enough that most projects don't need any `@source` declarations. Reach for it when:
- You import classes from a shared library outside the project root
- You have a legacy bundle Tailwind is mistakenly scanning
- You're integrating Tailwind into a non-standard project structure

## `oklch()` colors and `color-mix()` — perceptual palettes

Tailwind v4's shipped palette is `oklch()` end-to-end. The lightness ramps are perceptually-uniform — a `-500` shade has roughly the same perceived contrast against white in every hue family, which the v3 HSL palette could not guarantee.

For brand colors, define them in `@theme` using `oklch()`:

```css
@theme {
  --color-brand-50:  oklch(98% 0.02 250);
  --color-brand-100: oklch(94% 0.04 250);
  --color-brand-200: oklch(88% 0.08 250);
  --color-brand-300: oklch(80% 0.12 250);
  --color-brand-400: oklch(70% 0.15 250);
  --color-brand-500: oklch(60% 0.18 250);
  --color-brand-600: oklch(52% 0.20 250);
  --color-brand-700: oklch(43% 0.20 250);
  --color-brand-800: oklch(35% 0.18 250);
  --color-brand-900: oklch(28% 0.15 250);
  --color-brand-950: oklch(20% 0.10 250);
}
```

The hue value (`250` in this example, blue) stays constant; lightness and chroma vary. This produces a palette where every shade looks like the same color at different intensities, which the HSL equivalent could not.

### `color-mix()` for derived tints

Use `color-mix()` inside `@theme` to derive tints without manually picking each one:

```css
@theme {
  --color-brand-500: oklch(60% 0.18 250);
  --color-brand-500-alpha-50: color-mix(in oklch, var(--color-brand-500) 50%, transparent);
  --color-brand-500-tint: color-mix(in oklch, var(--color-brand-500) 20%, white);
  --color-brand-500-shade: color-mix(in oklch, var(--color-brand-500) 80%, black);
}
```

The mix happens in `oklch` color space, which preserves perceptual hue. Mixing in `srgb` (the default for older `color-mix` usages) can drift hue, producing muddy mid-tones; `in oklch` keeps the hue clean.

## `text-balance` and `text-wrap: pretty` — typesetting

Tailwind v4 ships utilities for both:

```html
<h1 class="text-balance">Long headline that should balance across two lines</h1>
<p class="text-pretty">Body copy that should avoid orphans at the end of paragraphs.</p>
```

Maps to:

```css
.text-balance { text-wrap: balance; }
.text-pretty { text-wrap: pretty; }
```

**When to use `text-balance`.** Headlines, hero titles, card titles, anything 2-3 lines where line breaks landing on awkward boundaries (a single dangling word on the second line) looks broken. The browser balances by adjusting line breaks across all lines so the line lengths are similar.

**When to use `text-pretty`.** Body paragraphs of 4+ lines. The browser tries to avoid orphans (a single short word on the last line) and hyphenation in early lines. The cost is small (~30ms on a 50-line page) and the typography improvement is visible.

**Concrete example.**

```html
<article>
  <h1 class="text-2xl font-semibold text-balance">
    Why every team needs a 5-line manifesto on their landing page
  </h1>
  <p class="mt-3 text-pretty text-gray-600 leading-relaxed">
    Long body paragraph that explains the topic. Without text-pretty,
    the last line might end with just the word "the." which looks
    abandoned. With text-pretty, the browser rebalances the last few
    lines so the orphan disappears.
  </p>
</article>
```

## Container queries — `@container` and `@xs:`/`@sm:` variants

In v3, container queries required the `@tailwindcss/container-queries` plugin. In v4, they're native:

```html
<div class="@container">
  <div class="grid grid-cols-1 @md:grid-cols-2 @lg:grid-cols-3 gap-4">
    <!-- cards -->
  </div>
</div>
```

The `@container` class on the parent declares it as a container. The `@md:grid-cols-2` utility on the child applies when the *container* is `>=` 28rem (the `@md` breakpoint), not when the viewport is. This decouples component layout from viewport size — the same card grid renders 1-col in a sidebar, 2-col in a main column, 3-col in a wide hero, without any media queries.

### v4 container-query breakpoints (in container units, not viewport)

| Variant | Min container width |
|---|---|
| `@xs:` | 20rem (320px) |
| `@sm:` | 24rem (384px) |
| `@md:` | 28rem (448px) |
| `@lg:` | 32rem (512px) |
| `@xl:` | 36rem (576px) |
| `@2xl:` | 42rem (672px) |
| `@3xl:` | 48rem (768px) |
| `@4xl:` | 56rem (896px) |
| `@5xl:` | 64rem (1024px) |
| `@6xl:` | 72rem (1152px) |
| `@7xl:` | 80rem (1280px) |

Note these are *container* breakpoints. The viewport-relative breakpoints (`sm:`, `md:`, `lg:`) keep their v3 meaning.

## The `--spacing()` function — derived spacing

Tailwind v4 introduces a CSS function for spacing arithmetic:

```css
.my-card {
  /* Equivalent to: padding: 1rem 2rem (with v4's spacing scale, where 4 = 1rem) */
  padding: --spacing(4) --spacing(8);

  /* Negative values: */
  margin-top: --spacing(-2);   /* -0.5rem */

  /* Half-steps: */
  padding-block: --spacing(2.5);   /* 0.625rem */
}
```

The function reads the `--spacing-*` tokens from `@theme`. Useful inside hand-written CSS that should share the same scale as the utility classes:

```css
@theme {
  --spacing-base: 0.25rem;  /* 4px */
}

.special-spacing {
  /* Use the same scale as p-4, m-8, etc. */
  gap: --spacing(6);  /* 1.5rem */
}
```

## Native cascade layers — `@layer` ordering

Tailwind v4 emits its CSS into named `@layer` blocks, so you can place your overrides cleanly:

```css
@import "tailwindcss";

/* Tailwind emits 3 layers in this order: theme < base < components < utilities */

@layer base {
  /* Your global resets / base styles — apply BEFORE Tailwind utilities */
  html { line-height: 1.6; }
}

@layer components {
  /* Your component classes — apply BEFORE utilities so utilities can override */
  .card {
    border-radius: 0.75rem;
    background: var(--color-bg-surface);
  }
}

@layer utilities {
  /* Your custom utilities — apply AT THE SAME LEVEL as Tailwind's */
  .scroll-snap-x { scroll-snap-type: x mandatory; }
}
```

Without `@layer`, your `.card` class would have the same specificity as a utility but parse later (winning). With `@layer components`, you guarantee Tailwind's `bg-red-500` utility beats your `.card { background }` — which is what you want, because the user wrote the utility on purpose.

## Fallback strategies via `@supports`

For the small minority of users on browsers older than v4's target window (Chrome 111 / FF 128 / Safari 16.4), wrap new features in `@supports`:

```css
.button {
  background: #3b82f6;  /* v3-style fallback for old browsers */
}

@supports (color: oklch(0 0 0)) {
  .button {
    background: oklch(60% 0.18 250);  /* v4-native */
  }
}
```

```css
.card-grid {
  display: grid;
  grid-template-columns: 1fr;
}

@supports (container-type: inline-size) {
  .card-grid-container {
    container-type: inline-size;
  }
  @container (min-width: 28rem) {
    .card-grid {
      grid-template-columns: 1fr 1fr;
    }
  }
}
```

For most teams, the v4-supported browser window is wide enough (Chrome / FF / Safari from 2023+) that explicit fallbacks aren't needed. Use `@supports` when:
- The product serves enterprise customers on managed older browsers
- The team committed to support browsers older than the v4 minimum
- A new feature (e.g. `text-wrap: pretty`) ships in only one engine and degradation is unacceptable

## Worked example — production-ready button using all v4 features

```html
<button class="
  inline-flex items-center gap-2
  px-4 py-2
  bg-brand-500 hover:bg-brand-600
  text-white text-sm font-medium
  rounded-lg
  shadow-sm hover:shadow-md
  transition-all duration-150
  @container
">
  <span class="text-balance">Get started with our 14-day trial</span>
  <svg class="w-4 h-4" aria-hidden="true">...</svg>
</button>
```

With `@theme`:

```css
@import "tailwindcss";

@theme {
  --color-brand-500: oklch(60% 0.18 250);
  --color-brand-600: oklch(55% 0.20 250);
}
```

What's used:
- `bg-brand-500` / `bg-brand-600` — `oklch()` palette from `@theme`
- `text-balance` — balanced wrapping if the button label wraps to two lines
- Standard utilities (`flex`, `gap-2`, `px-4 py-2`, `rounded-lg`, `shadow-sm`) — same as v3

What's NOT used (but available):
- Container queries (would matter if the button were inside a responsive grid)
- `--spacing()` (only useful in hand-written CSS, not utility classes)
- `light-dark()` (would matter if you wanted automatic dark-mode pair)

## Breaks if

- The project uses Tailwind v4 but keeps a `tailwind.config.js` from v3 instead of migrating tokens to `@theme`. The config file is silently ignored; the team thinks the tokens are applied but they aren't.
- `oklch()` colors are introduced without a fallback for unsupported browsers in an enterprise context where IE11 or old corporate Chrome is still active. Use `@supports` or push the team to upgrade Tailwind's stated minimum browser window.
- Container-query breakpoints are confused with viewport breakpoints. `@md:grid-cols-2` is NOT the same as `md:grid-cols-2`; the team writes both, expecting one, gets the other.
- `text-balance` is applied to body paragraphs. The browser balances by repositioning line-breaks across the entire block, which on a 200-word paragraph produces uneven leading and looks worse than no balance. Use `text-pretty` for long-form, `text-balance` for short titles only.
- The plugin's 3-tier token system isn't mapped into `@theme`. Tier 1 primitives leak as utilities (`bg-blue-500` becomes available, confusing the team into using primitive colors directly).
- `@source` is overused, scanning files that don't contain any Tailwind classes. Build times grow without benefit. Trust the v4 auto-detection and add explicit sources only when needed.

## Cross-references

- [TECH-css-modern-syntax.md](TECH-css-modern-syntax.md) — the underlying CSS features (oklch, container queries, color-mix); Tailwind v4 packages these into utilities.
- [TECH-css-variable-discipline.md](TECH-css-variable-discipline.md) — the plugin's 3-tier token system and how `@theme` integrates with it.
- [TECH-enterprise-system-overrides.md](TECH-enterprise-system-overrides.md) — multi-brand Tailwind v4 setups; how to scope `@theme` for theming.
- [amw-tailwind-4/SKILL.md](../../amw-tailwind-4/SKILL.md) — the executor skill that emits Tailwind v4 code; this reference is the pre-read.
- [color-system.md](../color-system.md) — color-palette construction principles; v4's `oklch()` defaults match the plugin's perceptual approach.
- [spacing-rhythm.md](../spacing-rhythm.md) — the 4/8 spacing scale that v4's `--spacing-*` tokens mirror.
- [typography-system.md](../typography-system.md) — `text-balance` / `text-pretty` integrate with the plugin's headings + body-copy guidance.
- [ai-slop-avoid.md](../ai-slop-avoid.md) — keep the AI-slop checks running on v4-rendered output; tooling changes don't change the visual rules.
