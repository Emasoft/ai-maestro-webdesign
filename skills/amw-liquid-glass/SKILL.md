---
name: amw-liquid-glass
description: >-
  liquid-glass-js implementation skill — WebGL 2.0 Apple visionOS-style
  frosted-glass UI (real-time refraction, blur, rim lighting, warp
  distortion). Activates on narrow triggers only: "liquid-glass-js",
  "liquid-glass library", "dashersw liquid glass", "visionOS glass
  component", "glass refraction WebGL", "glass container.js / button.js",
  "tintOpacity / blurRadius / edgeIntensity / rimIntensity / warp" used
  together. Does NOT activate on generic "glassmorphism", "frosted glass",
  "backdrop-filter blur", "transparent card" — those route to
  amw-design-principles or the S-034 Liquid Glass preset.
author: ai-maestro-webdesign (direct-port from liquid-glass-js, MIT, Arman Dashar 2024)
---

<!-- MIT — adapted from liquid-glass-js (Copyright (c) 2024 Arman Dashar) -->
<!-- Source: https://github.com/dashersw/liquid-glass-js — see external/ for any vendored bundle. Reorganised for the ai-maestro-webdesign plugin. -->

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Activated when the user explicitly names liquid-glass-js,
> asks to wire `Container` / `Button` glass classes, or tune
> `edgeIntensity` / `rimIntensity` / `blurRadius` / `tintOpacity` /
> `warp` together. The orchestrator routes here; do not re-route generic
> "make it glassy" intent back to this skill.

## Scope

This skill ships the **runtime contract** for the [liquid-glass-js](https://github.com/dashersw/liquid-glass-js) library — a WebGL 2.0 vanilla-JS implementation of Apple visionOS-style glass surfaces with real-time refraction, blur, rim lighting, and warp distortion. It covers:

- CDN / vanilla integration (no npm, no build step).
- Next.js / React integration (client-only, `ssr: false` mandatory).
- `Container` and `Button` class API (constructor options, methods).
- Global tuning via `window.glassControls`.
- Browser compatibility envelope (WebGL 2.0 required).

It does **not** ship: the aesthetic palette / typography tokens for the visionOS look — those live in `amw-design-system-presets/references/S-034-liquid-glass.md` (and the related `S-018-understated-elegance.md` for the softer / lighter variant). Use this skill **with** that preset: the preset chooses the colors and typography; this skill wires the refraction.

It also does **not** ship a CSS `backdrop-filter` fallback — that is a different aesthetic, covered by `amw-design-principles` patterns. Use liquid-glass-js when you need real-time WebGL refraction; use `backdrop-filter` when a CSS-only blur is enough.

## Why this skill is separate from S-034

- **S-034 Liquid Glass preset** = token block + 9 mandatory acceptance criteria. It tells you what "Liquid Glass" looks like.
- **amw-liquid-glass** (this skill) = how to wire the actual `Container` / `Button` JavaScript classes that produce the WebGL refraction. It tells you how to build it.

Two preset entries (S-018 Understated Elegance, S-034 Liquid Glass) already describe the aesthetic family; both can be implemented with liquid-glass-js plus their own token blocks.

## Setup (vanilla / CDN)

```html
<link rel="stylesheet" href="styles.css" />
<link rel="stylesheet" href="glass.css" />
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="container.js"></script>
<script src="button.js"></script>
```

`container.js`, `button.js`, `styles.css`, and `glass.css` are **not on npm**. Copy them from the upstream repo into the project — `liquid-glass-js` ships only as source files.

`html2canvas` is a hard dependency: the library samples the page behind each glass surface so the refraction can sample real DOM pixels. Without it, the glass shows a solid tint instead of refracting.

## Next.js integration

Client-only. The library uses the WebGL context and `document` directly, so it must run in the browser:

```ts
const GlassButton = dynamic(() => import('@/components/GlassButton'), { ssr: false })
```

**Do NOT** import liquid-glass-js files in server components, at module top-level, or in any code path that runs during SSR — the build will fail with `window is not defined`.

## Core API

### Container — base glass element

Wrap any DOM node in a glass layer.

| Option         | Type   | Default     | Description                                |
| -------------- | ------ | ----------- | ------------------------------------------ |
| `borderRadius` | number | `48`        | Corner radius in pixels                    |
| `type`         | string | `'rounded'` | `'rounded'` \| `'circle'` \| `'pill'`      |
| `tintOpacity`  | number | `0.2`       | Tint overlay transparency (0..1)           |

```js
const card = new Container({
  borderRadius: 32,
  type: 'rounded',
  tintOpacity: 0.15,
});
document.body.appendChild(card.element);
card.addChild(myContentElement);
```

**Methods:**

| Method                 | Purpose                                                        |
| ---------------------- | -------------------------------------------------------------- |
| `addChild(el)`         | Attach a DOM node inside the glass surface (no React refs).    |
| `removeChild(el)`      | Detach a node from the glass surface.                          |
| `updateSizeFromDOM()`  | Recalculate the WebGL sampling region after layout changes.    |

### Button — interactive glass element

Extends `Container`. Adds text rendering, click handling, and warp distortion.

| Option         | Type     | Default     | Description                              |
| -------------- | -------- | ----------- | ---------------------------------------- |
| `text`         | string   | `'Button'`  | Visible label                            |
| `size`         | number   | `48`        | Font size in pixels                      |
| `type`         | string   | `'rounded'` | Same as Container                        |
| `onClick`      | function | `null`      | Signature `(text: string) => void`       |
| `warp`         | boolean  | `false`     | Center distortion on hover / press       |
| `tintOpacity`  | number   | `0.2`       | Same as Container                        |

```js
const btn = new Button({
  text: 'Save Changes',
  size: 28,
  type: 'pill',
  tintOpacity: 0.4,
  warp: true,
  onClick: (text) => console.log(`${text} clicked`),
});
document.body.appendChild(btn.element);
```

## Shape types

- `'rounded'` — rounded rectangle. Use `borderRadius` to control corners.
- `'circle'` — perfect circle. Ignores `borderRadius`.
- `'pill'` — full-radius capsule, auto-sized by the content box.

## Global effect tuning

Override the four shader uniforms via `window.glassControls` **before** instantiating any `Container` or `Button`:

```js
window.glassControls = {
  edgeIntensity: 0.02,  // 0..0.1   — refraction strength at the glass edge
  rimIntensity:  0.08,  // 0..0.2   — rim-light brightness
  blurRadius:    7.0,   // 1..15    — background blur in shader pixels
  tintOpacity:   0.3,   // 0..1.0   — gradient overlay on top of the refraction
};
```

See [TECH-tuning](references/TECH-tuning.md) for the full tuning matrix (when to push each uniform up or down, and which uniform conflicts with which).
> [TECH-tuning.md] The four uniforms · Uniform conflicts · Suggested presets · When to NOT use this library · Performance notes

## Constraints

- **WebGL 2.0 required** — Chrome 80+, Firefox 75+, Safari 14+, Edge 80+. On unsupported browsers the glass surfaces render as opaque rectangles (fail-safe but not the intended look).
- **No SSR** — runs in the browser only.
- **No npm package** — vendor the source files into the project.
- **`html2canvas` required** — without it the background sampling fails and the glass shows a solid tint.
- **Not compatible with restricted Canvas environments** — workers with `OffscreenCanvas`-only contexts, sandboxed iframes that block WebGL, and similar restricted runtimes cannot host the library.

## Acceptance gate (per-output)

Before shipping a page that uses liquid-glass-js, every output must pass:

1. **CDN script tag for `html2canvas` is present and loads BEFORE `container.js` / `button.js`** — load order matters.
2. **Glass classes are instantiated client-side only** (in `useEffect`, `componentDidMount`, or a `dynamic(..., { ssr: false })` import).
3. **Each `Container` / `Button` has a `borderRadius` that matches the design preset** — S-018 prefers 24..32px; S-034 prefers 32..48px (capsule pills 9999).
4. **`tintOpacity` falls in the design preset's documented range** — S-018 0.10..0.18; S-034 0.15..0.25.
5. **`window.glassControls` is set ONCE at the top of the script** — multiple writes leak state across hot reloads.
6. **WebGL fallback is acceptable** — the page is still usable when WebGL 2.0 is missing (CSS `background-color` on the underlying DOM, not a blank screen).
7. **No glass surface contains more than one nested `Container`** — recursive glass layers crash the shader sampler.

Skills that produce pages using this library MUST run this checklist before delivery.

## Cross-references

- **Aesthetic presets that USE this skill:**
  - [S-018-understated-elegance](../amw-design-system-presets/references/S-018-understated-elegance.md) — soft / light variant.
> [S-018-understated-elegance.md] Identity · Token block · "Breaks if" invariants · Canonical render-test pointer · Render-test verdict · Cross-references
  - [S-034-liquid-glass](../amw-design-system-presets/references/S-034-liquid-glass.md) — full visionOS variant.
> [S-034-liquid-glass.md] Identity · Token block · "Breaks if" invariants · Canonical render-test pointer · Render-test verdict · Cross-references
- **Sibling aesthetic skills:**
  - [SKILL](../amw-evangelion-design/SKILL.md) — the polar-opposite aesthetic (severe geometry, no glass, restrained color).
- **Orchestrator:** [SKILL](../amw-design-principles/SKILL.md).
