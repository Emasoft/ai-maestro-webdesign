# vecui — Rect API

> Authoritative `Rect` method reference plus the DOM bridge, taken from the source `lib/main.ts`, not the README.

## Table of Contents

- [Rect model](#rect-model)
- [rect constructor](#rect-constructor)
- [Rect members](#rect-members)
- [Applying to the DOM](#applying-to-the-dom)

## Rect model

A `Rect` is `{ o: Vec, d: Vec }` — an **origin** (`o`, top-left point) and a **dimension** (`d`, width/height). Immutable; every method returns a new value. `o`/`d` are `readonly`.

```typescript
import { vec, rect } from "vecui";

const r = rect(vec(0, 0),     // origin (top-left)
               vec(100, 40)); // dimension (width, height)
r.o; // => vec(0, 0)
r.d; // => vec(100, 40)
```

## rect constructor

### `rect(...)` overloads

```typescript
rect(vec(1, 2), vec(3, 4))               // (origin, dimension)
rect({ x: 1, y: 2, width: 3, height: 4 })// InputRect object
rect(el.getBoundingClientRect())          // a DOMRect IS a valid InputRect
```

`rect(el.getBoundingClientRect())` is the bridge from a live DOM element into vecui space — read a real element's box, do vector math, write the result back via `.as.styleObject()`. (The upstream README's `rect(0,0,2,3)` snippet does **not** match any real `rect()` signature — trust this table.)

## Rect members

| Member | Signature → returns | Notes |
|---|---|---|
| `o` / `d` | `readonly Vec` | Origin (top-left) and dimension (width/height) vectors. |
| `setO(origin)` | `Rect` | New rect with a different origin (keeps dimension). |
| `setD(dim)` | `Rect` | New rect with a different dimension (keeps origin). |
| `map(fn)` | `Rect` | `fn(o, d) => [newO, newD]` (must return length-2 array, else throws). |
| `as.styleObject()` | `{ left, top, width, height }` (all `px` strings) | Apply to `element.style` or spread into a React `style` prop. |
| `as.cssText()` | `string` | `"left: …px; top: …px; width: …px; height: …px;"`. |
| `equals(other)` | `boolean` | True when both `o` and `d` are equal. |

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

For the absolutely-positioned element to honor `left`/`top`, set `position: absolute` (and give the parent `position: relative` for a local coordinate space). `as.styleObject()` only emits `left/top/width/height`; if a positioned element does not move, it is missing its positioning context. vecui computes the numbers; CSS positioning + your animation layer place and tween them.
