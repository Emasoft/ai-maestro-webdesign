---
name: amw-vecui
description: vecui reference — tiny immutable vec2 + rect math library (MIT) for JS-driven animated layouts CSS cannot express. Covers vec()/rect() factories, immutable operators (add/sub/mul/div/dot/cross/rotRad/rotDeg/norm/len/lookAt/angleTo) and rect.as.styleObject() for absolutely-positioned elements. Triggers on "vecui", "vec2 layout math", "vector math for layout". Does NOT trigger on generic "animate this", "lay out my page", or CSS layout. Use when doing JS-driven vec2/rect layout math.
---

# vecui Reference — vec2 + rect math for JS-driven layouts

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Offline reference for [`vecui`](https://github.com/AndrewPrifer/vecui) (MIT, by Andrew Prifer) — a tiny (<1 KB), ergonomic, **immutable** 2D vector library aimed at UI engineers. It exists for one job: layouts with complex constraints that CSS cannot express, where the practical answer is to position elements absolutely in a flat hierarchy and compute their coordinates in JavaScript.

The core idea: a UI is made of rectangles, and a rectangle is two vectors — an **origin** (`o`, top-left point) and a **dimension** (`d`, width/height). Modeling layout as vector arithmetic (offset by a width, center by half a delta, rotate to look at the cursor) collapses the spaghetti you'd otherwise write by hand.

vecui has **no required runtime peer dependencies** — it is framework-agnostic plain TypeScript. It pairs well with React (the demo uses framer-motion's animated style values), but works equally with vanilla DOM, Svelte, or a `<canvas>`. The library exports exactly four public symbols: the `vec()` and `rect()` factory functions, and the `Vec` and `Rect` types.

## Core model

```typescript
import { vec, rect } from "vecui";

const v = vec(3, 4);        // a 2D vector  {x: 3, y: 4}
const r = rect(vec(0, 0),   // origin (top-left)
               vec(100, 40)); // dimension (width, height)

r.o; // => vec(0, 0)    the origin vector
r.d; // => vec(100, 40) the dimension vector
```

- **Immutable.** `v.add(...)`, `r.setO(...)`, etc. all return a fresh value; the receiver is never modified. `x`/`y` (on `Vec`) and `o`/`d` (on `Rect`) are `readonly`.
- **Chaining.** Because every op returns a new `Vec`/`Rect`, calls chain fluently: `r.o.add(r.d.x, 0).add(8, 0)`.
- **Overloaded inputs.** Most vector ops accept either another `Vec` or loose `(x, y)` scalar components, so you can write `v.add(other)` or `v.add(8, 0)` interchangeably.

There is **no `lerp`, no `scale`, no 3D, no matrix, no mutable setter**. Interpolate by hand (`a.add(b.sub(a).mul(t))`) and scale via `mul(scalar)`.

## Reference index

The full API tables and worked layout patterns live under `references/` — read the matching file for the exact signatures and overloads taken from the source `lib/main.ts` (not the README).

[Vector API](references/vector-api.md) covers the `Vec` instance methods, constructors, overloads, and return types. Its complete TOC:

- Value model
- Constructors
- Vec members
- Missing operators

[Rect API](references/rect-api.md) covers the `Rect` instance methods plus the DOM bridge. Its complete TOC:

- Rect model
- rect constructor
- Rect members
- Applying to the DOM

[Layout recipes](references/layout-recipes.md) covers the canonical positioning patterns from the upstream demo. Its complete TOC:

- Layout recipe
- Worked example
- Rotation and coordinate system

## Instructions

1. Classify the question: vector op lookup, rect op lookup, constructor/overload signature, the immutability model, the chaining ergonomics, or "how do I position element X relative to element Y".
2. For a single vector operator or constructor, read the Vector API reference; for a rect operator or the DOM bridge, read the Rect API reference. Each lists the real signatures (including overloads) and return type from `lib/main.ts`.
3. For a positioning/animation task, read the Layout recipes reference — it shows the "center, then align-to-side, then expand-on-hover" pattern verbatim from the upstream demo.
4. For applying the result to the DOM, use `rect.as.styleObject()` (React/`element.style`) or `rect.as.cssText()` (string) — see the Rect API reference, § Applying to the DOM.
5. Remember every operation returns a **new** value — there is no in-place mutation. Treat vectors and rects like number primitives.
6. Extract the specific answer; do not paste the whole API back to the user.

## Examples

The canonical positioning patterns — "center, then align-to-side, then expand-on-hover" verbatim from the upstream demo, plus the rotation/coordinate-system worked example — live in [Layout recipes](references/layout-recipes.md), linked with its full TOC in the [Reference index](#reference-index) above.
> [layout-recipes.md] Layout recipe · Worked example · Rotation and coordinate system

## Output

This skill produces no standalone artifacts — it provides `vecui` API lookups and JS layout-math snippets. Any HTML/React output that embeds vecui-computed coordinates is assembled by `amw-ascii-to-html` / `amw-wireframe-builder-agent`, and any animation timeline that drives the values comes from the animations starter. vecui supplies the math; it does not own the render surface.

## Trigger conditions

Invoke this skill when the question is specifically about `vecui` or vec2 layout math:

- looking up a `vecui` vector or rect operator (`add`, `sub`, `mul`, `div`, `dot`, `cross`, `rotRad`/`rotDeg`, `norm`, `len`, `lookAt`, `angleTo`, `isInRect`, `map`, `reduce`) and confirming its real signature / overloads / return type
- understanding the immutable value model or the chaining ergonomics
- modeling a UI element as a `rect` (origin + dimension vectors) and computing the position of one element relative to another in JavaScript
- positioning absolutely-placed elements via vector arithmetic, or computing a "look-at-the-cursor" rotation
- bridging a live element (`getBoundingClientRect()`) into vector space and back out via `as.styleObject()` / `as.cssText()`

Do NOT invoke for generic "animate this", "make it move", "lay out my page", or framework-agnostic CSS layout requests — those belong to the orchestrator or to `design-principles` sub-skills. vecui is the right answer only once the decision to do JS-driven, absolutely-positioned, vector-computed layout has already been made.

## Prerequisites

- `runtime_binaries`: none for the reference itself (this SKILL.md is self-contained and works fully offline).
- To **use** `vecui` in a project: a JS/TS toolchain and the package installed (`yarn add vecui` / `npm i vecui`). It ships ESM + CJS + types and has no required runtime peer dependencies. The demo additionally uses `framer-motion` and `leva`, but those are demo-only, not vecui requirements.

## Position in flow

REFERENCE. Loaded when the orchestrator (or a producer agent like `amw-wireframe-builder-agent`) needs authoritative `vecui` API facts or a JS layout-math pattern during **Phase B**, after the design direction is approved and the chosen execution surface requires computed, absolutely-positioned coordinates.

## Resources

| Resource | Why this skill links it |
|---|---|
| [SKILL](../amw-design-principles/SKILL.md) | The orchestrator. It decides whether JS-driven vector layout is the right execution surface; this skill only answers `vecui`-specific questions and never owns broad design intent. |
| [animations.html](../amw-design-principles/starter-components/animations.html) | The ≈50-LOC timeline core that is the plugin's default animation driver. Use it to tween the values vecui computes (vecui is pure math with no time/loop concept). Per the animation stack-order rule: this starter first, Popmotion only for physics/spring/drag — **no Framer Motion, no GSAP** in plugin output (framer-motion appears only in vecui's own upstream demo). |
| [SKILL](../amw-shadcn-ui/SKILL.md) | When the absolutely-positioned vecui math overlays or anchors shadcn/Tailwind components. |

Keep computed paddings/gaps on the 8pt grid — feed those values into the vector offsets (`.add(padding, 0)`). The grid rules live in [spacing-rhythm](../amw-design-principles/spacing-rhythm.md) (owned by `amw-design-principles`):

- I. 8pt grid system
- II. Fibonacci spacing rhythm (large-scale)
- III. Vertical rhythm (baseline grid)
- IV. Hit targets (tappable areas)
- V. Alignment
- VI. Three principles of whitespace
- VII. Border radius
- VIII. Shadow system
- IX. Self-check

## Non-negotiables

- Does NOT own broad design intent. The orchestrator ([SKILL](../amw-design-principles/SKILL.md)) decides whether vecui is appropriate; this skill only answers vecui-specific questions.
- Never invent API. `vecui` has exactly four public exports (`vec`, `rect`, `Vec`, `Rect`) and the operator set documented in the references, taken from the source `lib/main.ts`. There is **no `lerp`, no `scale`, no 3D, no matrix, no mutable setter** — do not paraphrase a richer API from memory or from generic vector-library knowledge.
- vecui values are immutable; every operation returns a new value. Never present an in-place-mutation pattern.
- vecui is math only — it has no animation loop, no `requestAnimationFrame`, no time concept. Drive its values from the animations starter or the host framework's value layer.
- The `references/` files are the single source of truth for vecui's API in this plugin. If upstream `vecui` changes, re-read its `lib/main.ts` and update them — do not patch around a stale entry.
- English-only content. No third-language characters in any file.

## Error Handling

- **User asks for an operator vecui doesn't have (e.g. `lerp`, `scale`, `clamp`, `distanceTo`, 3D `vec3`):** state that vecui doesn't expose it, then give the idiomatic composition — interpolate with `a.add(b.sub(a).mul(t))`, scale with `mul(scalar)`, distance with `b.sub(a).len()`. Do not fabricate a method.
- **`map`/`reduce` callback returns the wrong shape:** `Vec.map` / `Rect.map` throw `Error("The function must return an array of length 2, …")` when the callback returns anything other than a length-2 array. Surface that constraint when writing a `map` call.
- **Single-number `vec(n)` surprise:** `vec(100)` sets **both** components to `100` (not `vec(100, 0)`). Flag this when a user expects a one-axis vector — they want `vec(100, 0)` or `vec(0, 100)`.
- **README vs source discrepancies:** the upstream README has minor inaccuracies (e.g. an `isInRect(rect(0,0,2,3))` snippet whose `rect()` call does not match the real `rect()` signatures). The references follow the actual source `lib/main.ts` signatures — trust the tables there over the README when they disagree.
- **Positioned element doesn't move:** `as.styleObject()` only emits `left/top/width/height`; the element must be `position: absolute` (or `fixed`) for those to take effect. Remind the user to set positioning context.
- **Coordinate-system / rotation sign confusion:** `rotRad`/`rotDeg` rotate counterclockwise in standard math orientation; `lookAt` assumes a left-handed system and offsets by `front`. If a rotation looks mirrored, check the y-axis direction (screen y grows downward) and the `front` argument before assuming a bug.
