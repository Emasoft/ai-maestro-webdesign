# TECH-tuning — liquid-glass-js shader uniform tuning matrix

## Table of Contents

- [The four uniforms](#the-four-uniforms)
- [Uniform conflicts](#uniform-conflicts)
- [Suggested presets](#suggested-presets)
- [When to NOT use this library](#when-to-not-use-this-library)
- [Performance notes](#performance-notes)

Each glass surface is parameterised by four shader uniforms exposed via `window.glassControls`. This file documents what each uniform does, when to push it up vs down, and which uniforms conflict.

## The four uniforms

| Uniform         | Range      | Default | Visual axis                                              |
| --------------- | ---------- | ------- | -------------------------------------------------------- |
| `edgeIntensity` | `0..0.1`   | `0.02`  | Refraction strength along the bevel at the surface edge. |
| `rimIntensity`  | `0..0.2`   | `0.08`  | Bright rim halo around the surface perimeter.            |
| `blurRadius`    | `1..15`    | `7.0`   | Background blur in shader pixels.                        |
| `tintOpacity`   | `0..1.0`   | `0.2`   | Solid gradient overlay above the refraction.             |

### `edgeIntensity` — refraction strength

The headline visionOS effect: light bending through the bevel at the glass edge. Pushed too low, the surface looks like a flat translucent rectangle (no glass). Pushed too high, the edge looks distorted and "wet."

- **Range 0.01..0.025** — subtle, premium-SaaS / Understated-Elegance (S-018) tone.
- **Range 0.03..0.06** — assertive, visionOS-faithful (S-034) tone.
- **Range 0.07..0.10** — exaggerated; reads as a stylised stage prop, not "glass."

### `rimIntensity` — rim halo

A bright micro-band tracing the surface perimeter. It is what makes the glass "pop" off the background.

- **0..0.04** — invisible. Surfaces blend into the scene. Useful on stacked panels where multiple rims would compete.
- **0.05..0.10** — recommended default. Each surface reads as distinct without shouting.
- **0.11..0.20** — bright halo. Use on a HERO surface only; never on every card.

### `blurRadius` — background blur

How much the content behind the glass is blurred before being refracted.

- **1..3** — almost transparent. Used to make TEXT behind the glass legible (e.g., a glass nav bar over a hero headline).
- **4..8** — recommended default. Blurs enough to soften branding behind the glass without erasing it.
- **9..15** — heavy frost. Use only when the content behind the glass is meant to be ATMOSPHERIC, not informational.

### `tintOpacity` — gradient overlay

A solid colour gradient laid over the refraction. The library's CSS sets the gradient stops; this uniform sets how OPAQUE that gradient is.

- **0.05..0.15** — S-018 Understated Elegance range. Glass reads as nearly clear.
- **0.15..0.25** — S-034 Liquid Glass range. Glass clearly tinted but still translucent.
- **0.26..0.50** — heavy. Use when the surface contains a single hero element (e.g., a CTA button) that must stand against a noisy background.
- **0.51..1.0** — opaque. The glass effect is essentially defeated; prefer a solid card with a separate `backdrop-filter` blur layer.

## Uniform conflicts

Some uniforms cancel each other; pushing both to their max produces a visually NOISY surface, not a more dramatic one.

| Pair                              | Why it conflicts                                                                  | Recommended pairing                                |
| --------------------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------- |
| `edgeIntensity` + `tintOpacity`   | High edge refraction is invisible under a high-opacity tint.                      | High edge → low tint, low edge → high tint.        |
| `blurRadius` + `tintOpacity`      | Heavy blur already obscures content; adding heavy tint reduces it to a flat rect. | One axis at a time.                                |
| `rimIntensity` + multiple panels  | Bright rims on every stacked panel produce neon clutter.                          | Bright rim on the FOCUS panel; dim rims elsewhere. |
| `edgeIntensity` + nested glass    | Nested glass layers compound refraction and crash the sampler.                    | Never nest `Container` instances.                  |

## Suggested presets

These are the four uniform tuples this skill recommends. Use them as starting points, not hard rules.

```js
// S-018 — Understated Elegance (premium SaaS / hero panels)
window.glassControls = {
  edgeIntensity: 0.018,
  rimIntensity:  0.06,
  blurRadius:    5.0,
  tintOpacity:   0.12,
};

// S-034 — Liquid Glass (visionOS-faithful, immersive app surfaces)
window.glassControls = {
  edgeIntensity: 0.04,
  rimIntensity:  0.09,
  blurRadius:    7.0,
  tintOpacity:   0.20,
};

// CTA button (single hero element on a noisy backdrop)
window.glassControls = {
  edgeIntensity: 0.05,
  rimIntensity:  0.14,
  blurRadius:    6.0,
  tintOpacity:   0.30,
};

// Translucent navigation bar (text behind must remain legible)
window.glassControls = {
  edgeIntensity: 0.025,
  rimIntensity:  0.05,
  blurRadius:    2.5,
  tintOpacity:   0.10,
};
```

## When to NOT use this library

- The page must render server-side (Next.js RSC, static export, AMP). Use CSS `backdrop-filter` instead.
- The target audience runs old Safari (< 14) or WebView (Android < 6). WebGL 2.0 is missing.
- The design preset is NOT in the liquid-glass family (e.g., evangelion-design, brutalist, terminal). The aesthetic of "frosted glass" conflicts with severe / dense / mechanical UI languages.
- The page already uses a heavy CSS `backdrop-filter` layer — stacking both yields a muddy composite.

## Performance notes

- Each `Container` / `Button` instance spawns a WebGL canvas. Keep the live instance count under 12 per page on mid-range mobile.
- `updateSizeFromDOM()` is **not free** — call it on resize / scroll-end / layout-change, not every animation frame.
- `html2canvas` resamples the page when called; pages with thousands of DOM nodes can stutter on first render. Prefer placing glass surfaces over CSS gradients or fixed background imagery, not over dynamic content trees.
