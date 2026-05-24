---
name: amw-vecui
description: vecui reference — tiny immutable vec2 + rect math library (MIT) for JS-driven animated layouts that CSS can't express. Covers vec()/rect() factories, immutable operators (add/sub/mul/div/dot/cross/rotRad/rotDeg/norm/len/lookAt/angleTo), rect.as.styleObject() for absolutely-positioned elements, and the chaining ergonomics. Triggers on "vecui", "vec2", "vec2 layout math", "vector math for layout", "JS-driven animated layout", "absolutely-positioned vector animation". Does NOT trigger on generic "animate this", "lay out my page", "make it move", or framework-agnostic CSS layout. Use when looking up vecui's vector/rect API or writing JS layout math. Trigger with "vecui" or "vec2 layout math".
version: 0.1.0
---

# vecui Reference — vec2 + rect math for JS-driven layouts

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Offline reference for [`vecui`](https://github.com/AndrewPrifer/vecui) (MIT, by Andrew Prifer) — a tiny (<1 KB), ergonomic, **immutable** 2D vector library aimed at UI engineers. It exists for one job: layouts with complex constraints that CSS cannot express, where the practical answer is to position elements absolutely in a flat hierarchy and compute their coordinates in JavaScript.

The core idea: a UI is made of rectangles, and a rectangle is two vectors — an **origin** (`o`, top-left point) and a **dimension** (`d`, width/height). Modeling layout as vector arithmetic (offset by a width, center by half a delta, rotate to look at the cursor) collapses the spaghetti you'd otherwise write by hand.

vecui has **no required runtime peer dependencies** — it is framework-agnostic plain TypeScript. It pairs well with React (the demo uses framer-motion's animated style values), but works equally with vanilla DOM, Svelte, or a `<canvas>`. The library exports exactly four public symbols: the `vec()` and `rect()` factory functions, and the `Vec` and `Rect` types.

This reference is self-contained — the API is small enough that no `references/` split is needed.

## Instructions

1. Classify the question: vector op lookup, rect op lookup, constructor/overload signature, the immutability model, the chaining ergonomics, or "how do I position element X relative to element Y".
2. For a single operator, jump to the matching entry in **## Vector API** or **## Rect API** below — each lists the real signatures (including overloads) and return type taken from the source `lib/main.ts`, not the README.
3. For a positioning/animation task, read **## Layout recipe** and **## Worked example** — they show the canonical "center, then align-to-side, then expand-on-hover" pattern verbatim from the upstream demo.
4. For applying the result to the DOM, use `rect.as.styleObject()` (React/`element.style`) or `rect.as.cssText()` (string). See **## Applying to the DOM**.
5. Remember every operation returns a **new** value — there is no in-place mutation. Treat vectors and rects like number primitives.
6. Extract the specific answer; do not paste the whole API back to the user.

## Output

This skill produces no standalone artifacts — it provides `vecui` API lookups and JS layout-math snippets. Any HTML/React output that embeds vecui-computed coordinates is assembled by `amw-ascii-to-html` / `amw-wireframe-builder-agent`, and any animation timeline that drives the values comes from the [animations starter](../amw-design-principles/starter-components/animations.html). vecui supplies the math; it does not own the render surface.

## Core model

```typescript
import { vec, rect } from "vecui";

const v = vec(3, 4);        // a 2D vector  {x: 3, y: 4}
const r = rect(vec(0, 0),   // origin (top-left)
               vec(100, 40)); // dimension (width, height)

r.o; // => vec(0, 0)   the origin vector
r.d; // => vec(100, 40) the dimension vector
```

- **Immutable.** `v.add(...)`, `r.setO(...)`, etc. all return a fresh value; the receiver is never modified. `x`/`y` (on `Vec`) and `o`/`d` (on `Rect`) are `readonly`.
- **Chaining.** Because every op returns a new `Vec`/`Rect`, calls chain fluently: `r.o.add(r.d.x, 0).add(8, 0)`.
- **Overloaded inputs.** Most vector ops accept either another `Vec` or loose `(x, y)` scalar components, so you can write `v.add(other)` or `v.add(8, 0)` interchangeably.

## Constructors

### `vec(...)` overloads

```typescript
vec(1, 2)          // (x, y)
vec(100)           // single number → both components: vec(100, 100)
vec([1, 2])        // [x, y] tuple
vec({ x: 1, y: 2 })// { x, y } object
```

When called with a single number, **both** components are set to it (`vec(100)` ⇒ `{x:100, y:100}`) — handy for square dimensions and uniform scaling.

### `rect(...)` overloads

```typescript
rect(vec(1, 2), vec(3, 4))               // (origin, dimension)
rect({ x: 1, y: 2, width: 3, height: 4 })// InputRect object
rect(el.getBoundingClientRect())          // a DOMRect IS a valid InputRect
```

`rect(el.getBoundingClientRect())` is the bridge from a live DOM element into vecui space — read a real element's box, do vector math, write the result back via `.as.styleObject()`.

## Vector API

Every method is on a `Vec` instance and returns a new value (immutable). Methods marked **overloaded** also accept loose `(x, y)` scalars in place of a `Vec` argument.

| Member | Signature → returns | Notes |
|---|---|---|
| `x` / `y` | `readonly number` | Components. |
| `yx` | `Vec` (getter) | Components swapped: `vec(1,2).yx ⇒ vec(2,1)`. |
| `setX(x)` / `setY(y)` | `Vec` | New vector with one component replaced. |
| `map(fn)` | `Vec` | `fn(x, y) => [nx, ny]` (must return length-2 array, else throws). |
| `reduce(fn)` | `T` | `fn(x, y) => T` collapse to a scalar/any value: `vec(1,2).reduce((x,y)=>x+y) ⇒ 3`. |
| `add(v)` / `add(x, y?)` | `Vec` | Vector addition. **overloaded** |
| `sub(v)` / `sub(x, y?)` | `Vec` | Vector subtraction. **overloaded** |
| `mul(v)` / `mul(x, y)` / `mul(scalar)` | `Vec` | Element-wise (Hadamard) product, **or** scalar scale when given one number. This is the scaling operator — there is no separate `scale`. **overloaded** |
| `div(scalar)` / `div(v)` / `div(x, y)` | `Vec` | Element-wise division, or divide by one scalar. `vec(d).div(-2)` centers a box of dimension `d`. **overloaded** |
| `dot(v)` / `dot(x, y)` | `number` | Dot product `x·x' + y·y'`. **overloaded** |
| `cross(v)` / `cross(x, y?)` | `number` | 2D cross product `x·y' − y·x'` (a scalar, the signed z of the 3D cross). **overloaded** |
| `len()` | `number` | L2 norm (length). `vec(3,4).len() ⇒ 5`. |
| `norm()` | `Vec` | Unit vector (divides by `len()`). `vec(3,4).norm() ⇒ vec(0.6, 0.8)`. |
| `rotRad(radians)` | `Vec` | Rotate counterclockwise by radians. |
| `rotDeg(degrees)` | `Vec` | Rotate counterclockwise by degrees (`rotRad(deg·π/180)`). |
| `angleTo(target)` | `number` | Unsigned angle (radians) between the two vectors via `acos`. |
| `lookAt(target, front?)` | `number` | Rotation (radians) so an object at this point faces `target`. `front` ∈ `"x" \| "y" \| "-x" \| "-y"`, default `"x"`. Built on `atan2`; used in the demo to rotate an element toward the cursor. |
| `asArray()` | `[number, number]` | Tuple form. |
| `isInRect(rect)` / `isInRect(input)` / `isInRect(o, d)` | `boolean` | Point-in-rectangle test; accepts a `Rect`, an `InputRect` object, or `(origin, dimension)` vectors. |
| `equals(v)` / `equals(x, y)` | `boolean` | Strict component equality. **overloaded** |

There is **no `lerp`** and **no `scale`** method in this library — interpolate by hand (`a.add(b.sub(a).mul(t))`) and scale via `mul(scalar)`.

## Rect API

A `Rect` is `{ o: Vec, d: Vec }` — origin and dimension. Immutable; every method returns a new value.

| Member | Signature → returns | Notes |
|---|---|---|
| `o` / `d` | `readonly Vec` | Origin (top-left) and dimension (width/height) vectors. |
| `setO(origin)` | `Rect` | New rect with a different origin (keeps dimension). |
| `setD(dim)` | `Rect` | New rect with a different dimension (keeps origin). |
| `map(fn)` | `Rect` | `fn(o, d) => [newO, newD]` (must return length-2 array, else throws). |
| `as.styleObject()` | `{ left, top, width, height }` (all `px` strings) | Apply to `element.style` or spread into a React `style` prop. |
| `as.cssText()` | `string` | `"left: …px; top: …px; width: …px; height: …px;"`. |
| `equals(other)` | `boolean` | True when both `o` and `d` are equal. |

## Layout recipe

The vecui mental model for "position element B relative to element A", expressed as vector arithmetic:

1. **Build the anchor rect.** `const anchor = rect(dim.div(-2), dim)` centers a box of dimension `dim` on the origin (offset origin by minus half the dimension).
2. **Walk to the target slot.** Start from `anchor.o`, then chain offsets: `.add(anchor.d.x, 0)` moves right by the anchor's width, `.add(padding, 0)` adds a gap.
3. **Center on the cross axis.** `anchor.d.sub(box.d).div(2).y` is the vertical offset that centers `box` against `anchor`; add it (use `.y` to take only the vertical component).
4. **Apply.** Spread `placed.as.styleObject()` onto the element.

## Worked example

Verbatim shape from the upstream demo (`src/App.tsx`) — a centered "anchor" box with a second box aligned to its right edge, kept vertically centered, expandable on hover:

```typescript
import { vec, rect } from "vecui";

const padding = 16;

// Anchor (yellow): centered on the origin.
const anchorDim = vec({ x: 200, y: 200 });
const anchorRect = rect(anchorDim.div(-2), anchorDim);

// Aligned (pink): right of the anchor, vertically centered.
const otherRect = rect(vec(0), vec(150, 150));
const alignedRect = otherRect.setO(
  anchorRect.o
    .add(anchorRect.d.x, 0)               // move to the anchor's right edge
    .add(
      padding,                            // horizontal gap
      anchorRect.d.sub(otherRect.d).div(2).y  // vertical centering offset
    )
);

// Expand-on-hover by a fixed pixel amount, regardless of size:
const hoverExpand = vec(8, 8);
const hoveredRect = rect(
  alignedRect.o.sub(hoverExpand),         // grow toward top-left
  alignedRect.d.add(hoverExpand.mul(2))   // ...and add to both sides
);

// "Look at the cursor" rotation for a centered element:
const angleRad = vec(window.innerWidth / 2, window.innerHeight / 2)
  .lookAt(vec(mouseX, mouseY));
```

## Applying to the DOM

```typescript
// Vanilla DOM:
const el = document.getElementById("aligned");
Object.assign(el.style, alignedRect.as.styleObject());
// or, as a string:
el.style.cssText = alignedRect.as.cssText();

// React:
<div style={{ ...alignedRect.as.styleObject() }} />

// framer-motion (drives the values over time — see the animations starter):
<motion.div animate={{ ...alignedRect.as.styleObject() }} />
```

For the absolutely-positioned element to honor `left`/`top`, set `position: absolute` (and give the parent `position: relative` if you want a local coordinate space). vecui computes the numbers; CSS positioning + your animation layer place and tween them.

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

- [SKILL](../amw-design-principles/SKILL.md) — the orchestrator. It decides whether JS-driven vector layout is the right execution surface; this skill only answers `vecui`-specific questions and never owns broad design intent.
- [animations.html](../amw-design-principles/starter-components/animations.html) — the ≈50-LOC timeline core that is the plugin's default animation driver. Use it to tween the values vecui computes (vecui is pure math with no time/loop concept of its own). Per the plugin animation stack-order rule: this starter first, Popmotion only for physics/spring/drag — **no Framer Motion, no GSAP** in plugin output (framer-motion appears only in vecui's own upstream demo).
- [spacing-rhythm](../amw-design-principles/spacing-rhythm.md) — keep computed paddings/gaps on the 8pt grid; feed those values into the vector offsets (`.add(padding, 0)`).
- [SKILL](../amw-shadcn-ui/SKILL.md) — when the absolutely-positioned vecui math overlays or anchors shadcn/Tailwind components.

## Non-negotiables

- Does NOT own broad design intent. The orchestrator ([SKILL](../amw-design-principles/SKILL.md)) decides whether vecui is appropriate; this skill only answers vecui-specific questions.
- Never invent API. `vecui` has exactly four public exports (`vec`, `rect`, `Vec`, `Rect`) and the operator set documented above, taken from the source `lib/main.ts`. There is **no `lerp`, no `scale`, no 3D, no matrix, no mutable setter** — do not paraphrase a richer API from memory or from generic vector-library knowledge.
- vecui values are immutable; every operation returns a new value. Never present an in-place-mutation pattern.
- vecui is math only — it has no animation loop, no `requestAnimationFrame`, no time concept. Drive its values from the [animations starter](../amw-design-principles/starter-components/animations.html) or the host framework's value layer.
- This reference is the single source of truth for vecui's API in this plugin. If upstream `vecui` changes, re-read its `lib/main.ts` and update this file — do not patch around a stale entry.
- English-only content. No third-language characters in any file.

## Error Handling

- **User asks for an operator vecui doesn't have (e.g. `lerp`, `scale`, `clamp`, `distanceTo`, 3D `vec3`):** state that vecui doesn't expose it, then give the idiomatic composition — interpolate with `a.add(b.sub(a).mul(t))`, scale with `mul(scalar)`, distance with `b.sub(a).len()`. Do not fabricate a method.
- **`map`/`reduce` callback returns the wrong shape:** `Vec.map` / `Rect.map` throw `Error("The function must return an array of length 2, …")` when the callback returns anything other than a length-2 array. Surface that constraint when writing a `map` call.
- **Single-number `vec(n)` surprise:** `vec(100)` sets **both** components to `100` (not `vec(100, 0)`). Flag this when a user expects a one-axis vector — they want `vec(100, 0)` or `vec(0, 100)`.
- **README vs source discrepancies:** the upstream README has minor inaccuracies (e.g. an `isInRect(rect(0,0,2,3))` snippet whose `rect()` call does not match the real `rect()` signatures). This SKILL.md follows the actual source `lib/main.ts` signatures — trust the tables here over the README when they disagree.
- **Positioned element doesn't move:** `as.styleObject()` only emits `left/top/width/height`; the element must be `position: absolute` (or `fixed`) for those to take effect. Remind the user to set positioning context.
- **Coordinate-system / rotation sign confusion:** `rotRad`/`rotDeg` rotate counterclockwise in standard math orientation; `lookAt` assumes a left-handed system and offsets by `front`. If a rotation looks mirrored, check the y-axis direction (screen y grows downward) and the `front` argument before assuming a bug.
