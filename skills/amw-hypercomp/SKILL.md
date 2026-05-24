---
name: amw-hypercomp
description: hypercomp reference — TypeScript library compiling a chainable Effect API to SVG filters. Triggers on "hypercomp", "SVG filter", "SVG filter composition", "compose SVG filter effects", "feTurbulence", "feDisplacementMap", "feGaussianBlur", "feColorMatrix", "image-processing filter chain". Does NOT trigger on generic "add an effect" or broad design intent. Use when authoring or reading a hypercomp Effect chain or compiled SVG filter. Trigger with "hypercomp" or "SVG filter composition".
version: 0.1.0
---

# hypercomp — SVG Filter Composition Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Offline reference for [`hypercomp`](https://github.com/AndrewPrifer/hypercomp) (MIT, by Andrew Prifer) — a functional TypeScript image-processing library that compiles a composable `Effect` chain down to an equivalent SVG `<filter>`, applicable to any HTML or SVG element via the CSS `filter` property.

SVG filters are a powerful node-based effect system, but XML cannot express function composition naturally, so they are hard to write, compose, and reuse. hypercomp fixes this: you compose effects with chained JavaScript methods (`Effect.source.blur(2).shadow(1)`), then `css()` / `compile()` the result. Each method maps 1:1 to an SVG filter primitive (`feGaussianBlur`, `feTurbulence`, `feDisplacementMap`, `feColorMatrix`, `feComposite`, `feBlend`, `feMorphology`, `feDiffuseLighting`, `feSpecularLighting`, …).

This skill documents the **real, verified API** (read from the library's TypeScript source, not paraphrased). The full operator catalog and the render/React/lights/transfer reference live in `references/` (progressive disclosure) so this file stays small.

## Instructions

1. Classify the request: (a) author a new filter chain, (b) read / explain an existing chain or its compiled SVG, (c) look up one operator's signature or config, (d) wire rendering into HTML/React.
2. For an operator signature or its config options → read [operators](references/operators.md). Do not guess parameter names — the shorthand config keys (e.g. `color`, `strength`, `octaves`) differ from the raw SVG attribute names they compile to.
3. For rendering, `.filter()` attributes, React `useFilter`, light sources, transfer functions, the base region config (`x`/`y`/`width`/`height`), gotchas, and worked recipes → read [render-and-react](references/render-and-react.md).
4. Build the chain from a basis (`Effect.source`, `Effect.flood(...)`, `Effect.turbulence(...)`, `Effect.image(...)`) and chain transforms onto it. Inputs to compositing/blending/displacement methods are themselves `Effect` chains.
5. Always render with a **key** (`css(effect, "my-key")`) or the React `useFilter` hook — keyless data-URL rendering is unreliable (Safari does not support data-URL CSS filters; `.image()` breaks in Chrome). This is a hard rule (see Non-negotiables).
6. Extract only the specific answer; do not reload the whole reference set.

## At-a-glance API map

```
import { Effect, Light, Transfer, css, compile, unmount } from "hypercomp";
import { useFilter } from "hypercomp/react";          // React entry point

Effect.source / .sourceAlpha / .background / .backgroundAlpha / .fill / .stroke   // constant inputs
Effect.flood(color) / .image(href) / .merge([...]) / .turbulence(f) / .fractalNoise(f)   // basis fns

// chainable on any Effect:
.blur(stdDev) .shadow(stdDev) .offset() .tile() .convolve(kernel) .displace(map, scale)
.dilate(r) .erode(r)                                                  // morphology
.colorMatrix(m) .saturate(n) .hueRotate(deg) .luminanceToAlpha() .componentTransfer({...})
.over(in) .in(in) .out(in) .atop(in) .xor(in) .arithmetic(in,{k1..k4})   // compositing
.normal/.multiply/.screen/.overlay/.darken/.lighten/.colorDodge/.colorBurn/
 .hardLight/.softLight/.difference/.exclusion/.hue/.saturation/.color/.luminosity(in)  // blend
.specular(light,{...}) .diffuse(light,{...})                          // lighting
.filter({ id, x, y, width, height, ... })                            // optional <filter> attrs

Light.pointLight({x,y,z}) / .distantLight({azimuth,elevation}) / .spotlight({x,y,z,pointsAtX,...})
Transfer.gamma(amp,exp,off) / .linear(slope,intercept) / .table([...]) / .discrete([...])
```

## Quick start

```tsx
import { Effect, css } from "hypercomp";

// Gooey edges: source over a high-blur, high-alpha-contrast copy of itself.
const goo = Effect.source.atop(
  Effect.source.blur(10).colorMatrix({ a: { a: 19, o: -9 } })
);

return <div style={{ filter: css(goo, "goo") }}>hello world</div>;
```

`compile(Effect.source.blur(2))` → `<feGaussianBlur stdDeviation="2"/>`. Wrapping in `filter()` first emits the full `<filter>…</filter>` tag. See [render-and-react](references/render-and-react.md) for the rules.

## Output

This skill produces **no standalone artifact**. It provides hypercomp lookup answers, verified operator signatures, and TypeScript snippets. The resulting filter is consumed inside HTML/SVG produced by `amw-ascii-to-html` / `amw-wireframe-builder-agent`, or applied to SVG authored via [SKILL](../amw-svg-creator/SKILL.md). It is an effect layer, never a substitute for the geometry/markup.

## Trigger conditions

Invoke this skill when the request is specifically about hypercomp or hand-composed SVG filter effects:

- authoring a chained `Effect` filter (blur, drop-shadow, turbulence/fractal-noise, displacement, color-matrix, morphology, blend/composite, lighting)
- reading or explaining an existing hypercomp chain or the SVG `<filter>` it compiles to
- looking up one operator's signature, its shorthand config keys, or which SVG primitive it maps to
- wiring a compiled filter into a CSS `filter` property or the React `useFilter` hook
- choosing a compositing vs blending operator, or a light source / transfer function

Do NOT invoke for generic "add an effect", "make it pop/look cool", animation/transition work, or design-intent decisions — those belong to the orchestrator ([SKILL](../amw-design-principles/SKILL.md)) or its sub-skills (motion, color-system, typography-system).

## Prerequisites

- **Peer dependency: `react`** — required only for the `hypercomp/react` entry point (`useFilter`). The core `hypercomp` module (`Effect`, `css`, `compile`, `Light`, `Transfer`) is framework-agnostic and runs without React.
- **Install:** `npm install hypercomp` (or `bun add hypercomp`). The library is published as ESM + CJS with bundled types; no build step or remote service is needed. This skill is fully offline.
- **Runtime:** filters render in the browser via the DOM. `css(effect, key)` injects a hidden `<svg><filter>` into `document.body`, so a DOM is required at render time (it is a no-op argument-builder otherwise).
- Helpful background: a working intuition for SVG filter primitives and image-processing concepts (convolution kernels, displacement maps, blend modes). Study the recipes in [render-and-react](references/render-and-react.md).

## Structure

- [operators](references/operators.md) — full chainable-operator catalog: basis functions, compositing, common transforms, all 16 blend modes, morphology, color manipulation, lighting. Verified signatures + shorthand config keys + the SVG primitive each compiles to.
- [render-and-react](references/render-and-react.md) — render functions (`css` / `compile` / `unmount` / `.filter()`), React `useFilter`, light sources (`Light.*`), transfer functions (`Transfer.*`), the base region config, key-rendering gotchas, and worked recipes.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — the orchestrator decides whether an SVG-filter effect is the right execution surface and enforces the three hard design rules (gather context, three variants, reject AI-slop).
- [SKILL](../amw-svg-creator/SKILL.md) — authors the SVG geometry (icons, logos, technical shapes) that a hypercomp filter is then applied to. hypercomp adds the effect layer; svg-creator owns the shapes.
- [SKILL](../amw-diagram-svg/SKILL.md) — natural-language → SVG diagrams; a hypercomp filter can post-process a generated diagram (e.g. soft shadow, glow, distortion) once the structure is settled.

## Non-negotiables

- Does NOT own broad design intent. The orchestrator decides whether an effect is warranted; this skill only answers hypercomp-specific questions.
- Never paraphrase an operator name or its config keys from memory. Confirm against [operators](references/operators.md) — shorthand keys (`color`, `strength`, `shininess`, `octaves`, `falloff`) are remapped to raw SVG attribute names internally and are easy to get wrong.
- Always render with a `key` (`css(effect, key)`) or React `useFilter`. Never recommend keyless data-URL rendering for production — it fails in Safari and breaks `.image()` in Chrome.
- Effects are immutable builders: each method returns a NEW `Effect`. Reassign or chain; mutating in place is not how the API works.
- This is a reference for an external MIT library. Do not vendor or copy the library source into the skill. If behavior looks wrong, check the installed package version against the documented `0.4.x` surface rather than patching this SKILL.md.
- English-only content across the skill. No third-language characters in any file.

## Error Handling

- **Filter does not appear / element vanishes:** the most common cause is keyless rendering. Switch to `css(effect, "key")` or `useFilter`. Confirm a DOM exists at render time.
- **`.image()` renders blank in Chrome, or any filter blank in Safari:** that is the documented data-URL limitation — use the keyed/`useFilter` path, which mounts a real `<filter>` element.
- **Wrong / no effect from a config option:** verify the shorthand key against [operators](references/operators.md) (e.g. drop-shadow color is `color`, not `flood-color`; turbulence octaves is `octaves`, not `numOctaves`). An unknown key is silently ignored by the SVG renderer.
- **`useFilter` import fails:** import it from `hypercomp/react` (not `hypercomp`), and ensure `react` is installed as a peer dependency.
- **TypeScript error on `.displace(...)`:** the signature is `.displace(displacementMapEffect, scale, config?)` — the displacement-map `Effect` is the FIRST argument, the numeric scale is SECOND. See [operators](references/operators.md).
- **Library version differs from this reference:** this skill documents the `0.4.x` API. If the installed package exposes a different surface, report the version mismatch instead of guessing — do not invent methods.
