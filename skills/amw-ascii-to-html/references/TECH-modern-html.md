---
name: TECH-modern-html
category: ascii-to-html-modern-standards
source: amw-wireframe-builder-agent §9 (modern HTML primitives row)
also-in: globalCC `modern-web-development` skill (informational only — not a plugin skill)
---

# Modern HTML / CSS primitives — 2024-2025 standards

## What it does

Catalog of modern HTML elements and CSS features the wireframe-builder
agent should reach for instead of legacy patterns. Each entry includes a
minimal working example, browser-support note (current as of 2026-04;
verify on caniuse.com when in doubt), and a "use this instead of" pointer
to the legacy pattern it supersedes.

## `<dialog>` element

Native modal dialog with built-in focus trap, ESC-to-close, and
backdrop. Replaces hand-rolled `div.modal` + `aria-modal` choreography.

```html
<dialog id="signup-modal" aria-labelledby="signup-title">
  <form method="dialog">
    <h2 id="signup-title">Sign up</h2>
    <input type="email" name="email" required>
    <button value="confirm">Sign up</button>
    <button value="cancel">Cancel</button>
  </form>
</dialog>

<button onclick="document.getElementById('signup-modal').showModal()">
  Open
</button>
```

Browser support: Chrome 37+, Firefox 98+, Safari 15.4+, Edge 79+ —
universally supported as of 2026. Use `dialog.showModal()` for the
focus-trapped variant; `dialog.show()` for non-modal popovers (use
popover API for non-modal).

Use this instead of: hand-rolled `div.modal[role="dialog"]` with
manual focus-trap JS.

## Popover API

Lightweight non-modal popovers (tooltips, menus, comboboxes) without JS.

```html
<button popovertarget="user-menu">Open menu</button>
<div id="user-menu" popover>
  <a href="/account">Account</a>
  <a href="/settings">Settings</a>
  <a href="/logout">Logout</a>
</div>
```

Attribute variants:
- `popover` (default `popover="auto"`) — light-dismiss, only one open
  at a time
- `popover="manual"` — must be explicitly closed
- `popovertarget="<id>"` on a trigger button — toggle binding

Browser support: Chrome 114+, Safari 17+, Firefox 125+. Polyfillable
via the `popover-polyfill` package for older browsers.

Use this instead of: jQuery `.toggle()` patterns, hand-coded event
listeners on document for outside-click dismissal.

## `<details>` / `<summary>`

Built-in disclosure widget — accessible by default.

```html
<details>
  <summary>FAQ: Is shipping included?</summary>
  <p>Yes, on orders over $50. International orders incur shipping.</p>
</details>
```

Open by default: `<details open>`. Style the marker via
`summary::marker { content: '+'; }` or set `summary::-webkit-details-marker { display: none; }` and supply your own.

Use this instead of: hand-coded accordion components for static FAQ.

## Container Queries (`@container`)

Element queries — components that respond to their parent container's
width, not the viewport. Critical for component-driven design where the
same Card component renders in a 200px sidebar and a 1000px hero.

```css
.container {
  container-type: inline-size;
  container-name: card-host;
}

@container card-host (min-width: 400px) {
  .card { display: grid; grid-template-columns: 1fr 2fr; }
}

@container card-host (min-width: 800px) {
  .card { padding: 2rem; font-size: 1.125rem; }
}
```

Browser support: Chrome 105+, Safari 16+, Firefox 110+. Universally
supported as of 2026.

Use this instead of: viewport breakpoints when the component lives in
multiple layout contexts.

## View Transitions API

Smooth same-document and cross-document transitions without a SPA
framework.

Same-document (route change in JS):

```js
document.startViewTransition(() => {
  // mutate the DOM (swap content)
  mainContent.innerHTML = newHTML;
});
```

Cross-document (full page navigation):

```html
<meta name="view-transition" content="same-origin">
```

Targeted transitions via `view-transition-name`:

```css
.hero-image { view-transition-name: hero; }
/* Browser auto-animates the matching named element across pages */
```

Browser support: Chrome 111+ (same-doc), Chrome 126+ (cross-doc),
Safari 18+, Firefox: enabled in 2025 nightlies. Not yet universally
shipped — wrap in `if (document.startViewTransition)` capability check.

Use this instead of: route-change libraries that hand-roll fade/slide
transitions.

## `<picture>` + `srcset` + `sizes`

Responsive images with art direction (different crops per breakpoint)
AND density-aware delivery.

```html
<picture>
  <source media="(min-width: 1024px)"
          srcset="/img/hero-desktop.avif 1x, /img/hero-desktop-2x.avif 2x"
          type="image/avif">
  <source media="(min-width: 1024px)"
          srcset="/img/hero-desktop.webp 1x, /img/hero-desktop-2x.webp 2x"
          type="image/webp">
  <source media="(min-width: 1024px)"
          srcset="/img/hero-desktop.jpg 1x, /img/hero-desktop-2x.jpg 2x"
          type="image/jpeg">

  <source srcset="/img/hero-mobile.avif"   type="image/avif">
  <source srcset="/img/hero-mobile.webp"   type="image/webp">

  <img src="/img/hero-mobile.jpg"
       alt="Couple on overwater villa deck"
       width="1024" height="640"
       loading="eager"
       fetchpriority="high"
       decoding="async">
</picture>
```

Always specify `width` + `height` to prevent CLS (the browser reserves
the box before the image loads).

For non-art-directed responsive (same image at different sizes), use
`srcset` with `sizes` directly on `<img>`:

```html
<img src="/img/article-800.jpg"
     srcset="/img/article-400.jpg 400w,
             /img/article-800.jpg 800w,
             /img/article-1200.jpg 1200w"
     sizes="(min-width: 1024px) 800px, 100vw"
     alt="Article cover"
     width="800" height="450"
     loading="lazy"
     decoding="async">
```

## `loading="lazy"` and `decoding="async"`

Built-in lazy loading for off-screen images:

```html
<img src="/img/footer-graphic.png"
     loading="lazy"
     decoding="async"
     alt="" width="200" height="120">
```

Rules:
- `loading="eager"` (default) for above-the-fold images, especially the
  LCP candidate
- `loading="lazy"` for everything below the fold
- `decoding="async"` for everything (lets the browser decode off the
  main thread; harmless even on eager-loaded images)
- `fetchpriority="high"` ONLY on the LCP candidate (1 per page); lets
  the preload scanner promote the image fetch above other resources

## `<link rel="preload">` for fonts + `font-display: swap`

Preload the brand display font to avoid FOIT (flash of invisible
text) without blocking render:

```html
<link rel="preload"
      href="/fonts/BebasNeue-Variable.woff2"
      as="font"
      type="font/woff2"
      crossorigin>
```

Pair with `font-display: swap`:

```css
@font-face {
  font-family: 'Bebas Neue';
  src: url('/fonts/BebasNeue-Variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}
```

`font-display` values:
- `swap` — show fallback immediately, swap when font loads (best for
  brand fonts where the swap is acceptable)
- `optional` — show fallback immediately, only use brand font if
  cached (best for body fonts where flash is jarring)
- `block` — invisible text for up to 3s waiting for font (avoid)
- `fallback` — short block (~100ms) then swap (compromise)

Use this instead of: Google Fonts `<link>` tags without preload (which
blocks LCP by 200-800ms on slow networks).

## CSS `:has()` selector

Parent selector — style a parent based on its descendants.

```css
/* Style cards that contain a video */
.card:has(video) { border: 2px solid var(--accent); }

/* Hide the entire form group when the input is invalid */
.form-group:has(input:invalid) { background: var(--danger-bg); }

/* Different layout when the article has a hero image */
article:has(> .hero) { padding-top: 0; }
```

Browser support: Chrome 105+, Safari 15.4+, Firefox 121+. Universally
supported as of 2026.

Use this instead of: JS that adds/removes classes on a parent based on
descendant state.

## CSS `color-mix()` and Cascade Layers (`@layer`)

`color-mix()` blends colors at runtime — use for hover states, dark-mode
derivations, alpha overlays:

```css
.btn { background: var(--primary); }
.btn:hover { background: color-mix(in oklch, var(--primary), white 12%); }
.btn:active { background: color-mix(in oklch, var(--primary), black 8%); }
```

`oklch` is the recommended interpolation space — perceptually uniform,
no hue-shift artifacts.

Cascade Layers — explicit specificity ordering for utility-class
frameworks like Tailwind:

```css
@layer reset, base, components, utilities;

@layer base { /* design tokens, typography */ }
@layer components { /* shadcn-ui components */ }
@layer utilities { /* Tailwind utilities — last, so they override */ }
```

Browser support for `@layer`: Chrome 99+, Safari 15.4+, Firefox 97+.
Universally supported.

## CSS Subgrid

Lets a grid item participate in its parent's grid tracks.

```css
.parent { display: grid; grid-template-columns: 1fr 2fr 1fr; gap: 1rem; }
.child { display: grid; grid-template-columns: subgrid; grid-column: 1 / -1; }
```

Browser support: Chrome 117+, Safari 16+, Firefox 71+. Universally
supported as of 2026.

Use this instead of: nested grids with hand-tuned column widths to
align with the parent.

## Media-feature: `prefers-color-scheme`, `prefers-contrast`, `prefers-reduced-data`, `prefers-reduced-motion`

```css
/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0b0b0c;
    --text: #f5f5f5;
  }
}

/* High-contrast users */
@media (prefers-contrast: more) {
  :root { --text: #000; --bg: #fff; --border-width: 2px; }
}

/* Data-saver mode */
@media (prefers-reduced-data: reduce) {
  .hero-image { display: none; }
  .video-bg { display: none; }
  body { background-image: none; }
}

/* Reduced motion (already covered globally — never ship without this) */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Browser support:
- `prefers-color-scheme`: universal
- `prefers-reduced-motion`: universal
- `prefers-contrast`: Chrome 96+, Safari 14.1+, Firefox 101+
- `prefers-reduced-data`: Chrome 85+, Safari unsupported, Firefox unsupported (treat as progressive enhancement)

Always pair `prefers-color-scheme` derivations with the brand-tokens
bundle's `dark` variant — never hand-pick darker hexes.

## `<input>` modern attributes

```html
<input type="email"
       inputmode="email"
       autocomplete="email"
       enterkeyhint="next"
       required>

<input type="search"
       enterkeyhint="search"
       results="5"
       autocomplete="off">

<input type="tel"
       inputmode="tel"
       autocomplete="tel"
       pattern="[0-9 +()-]+">
```

`inputmode` controls the mobile keyboard layout. `enterkeyhint` controls
the enter-key label. `autocomplete` enables password managers and
form-fill.

## Anti-patterns to NOT use

- `tabindex="0"` on `<div>` for interactivity → use `<button>`
- Hand-rolled focus-trap JS → use `<dialog>` or popover API
- jQuery `.toggle()` for menus → use `<details>` or popover API
- `scrollIntoView()` (banned plugin-wide per CLAUDE.md) → manual
  `window.scrollTo({top, behavior: 'smooth'})` with offset math
- Background images without `prefers-reduced-data` opt-out
- Dark-mode CSS without testing the contrast ratios in the dark variant
- `<img>` without `width`/`height` (causes CLS, fails Lighthouse)
- Web fonts without `font-display: swap` (causes FOIT, fails Lighthouse)
- `<a>` for actions (use `<button>`); `<button>` for navigation (use `<a>`)

## What the agent MUST do

1. Prefer `<dialog>` for modals; popover API for non-modal floats
2. Always emit `width` + `height` on `<img>`
3. Always emit `loading="lazy"` + `decoding="async"` on below-fold images
4. Always emit `loading="eager"` + `fetchpriority="high"` on the single
   LCP candidate
5. Always preload brand display fonts with `font-display: swap`
6. Always include `prefers-reduced-motion` reset
7. Prefer `:has()`, `color-mix()`, container queries, subgrid for layout
   when they replace JS or duplicated CSS
8. Document any feature whose support is < 95% in `warnings`

## What the agent MUST NOT do

- Use `<dialog>` for tooltips (use popover API)
- Use container queries for viewport-level breakpoints (use media queries)
- Use `:has()` for performance-critical selectors that match the entire
  body (browser engines de-optimize `body:has(...)` patterns)
- Skip image dimensions to "let CSS handle it" — that breaks LCP
