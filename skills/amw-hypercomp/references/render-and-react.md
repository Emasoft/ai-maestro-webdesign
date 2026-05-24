# hypercomp — Rendering, React, Lights, Transfer Functions, Recipes

Verified against the library TypeScript source (`hypercomp` 0.4.x). Covers everything outside the chainable-operator catalog (which lives in [operators](operators.md)): how a composed `Effect` is turned into something a browser can use, the React hook, light-source and transfer-function constructors, the shared base config, the data-URL gotcha, and worked recipes.

## Table of Contents

- [Render functions](#render-functions)
- [The `.filter()` attributes](#the-filter-attributes)
- [Usage with React](#usage-with-react)
- [Light sources (`Light.*`)](#light-sources-light)
- [Transfer functions (`Transfer.*`)](#transfer-functions-transfer)
- [Base region config](#base-region-config)
- [Gotchas](#gotchas)
- [Recipes](#recipes)

## Render functions

Top-level exports from `hypercomp`. They accept either an `Effect` or a `Filter` (the result of `effect.filter()` / `filter(effect)`).

### `css(filter, key?)`

Compiles the filter and returns a string for the CSS `filter` property.

- **With `key`** (recommended): mounts a real `<filter>` element into a hidden `<svg>` appended to `document.body`, and returns `url(#hypercomp-…-key)`. Calling again with the same key updates that filter in place. Pass the same key to `unmount(key)` to remove it.
- **Without `key`**: renders to a `data:` URL and returns `url(data:image/svg+xml;…)`. **Not recommended** — Safari does not support data-URL CSS filters, and `.image()` fails in Chrome.

Returns: `string`.

### `unmount(key)`

Removes the keyed filter element from the DOM. When the last keyed filter is removed, the hidden host `<svg>` is removed too.

### `compile(filter)`

Returns the compiled SVG as a string.

- `compile(effect)` → just the inner primitives, **no** wrapping tag. E.g. `compile(Effect.source.blur(2))` → `<feGaussianBlur stdDeviation="2"/>`.
- `compile(filter(effect))` (or `compile(effect.filter())`) → the full `<filter>…</filter>` element.

Use `compile` for static/server-side output, snapshot tests, or hand-pasting into an SVG document. Use `css` (keyed) for live DOM use.

## The `.filter()` attributes

`effect.filter(attributes?)` wraps an `Effect` in a `Filter`, letting you set attributes on the emitted `<filter>` tag. Optional — without it, behavior depends on the render function used.

```typescript
interface SVGFilterAttributes {
  id?: string;
  x?: string | number;
  y?: string | number;
  width?: string | number;
  height?: string | number;
  filterUnits?: "userSpaceOnUse" | "objectBoundingBox";
  primitiveUnits?: "userSpaceOnUse" | "objectBoundingBox";
  colorInterpolationFilters?: "auto" | "sRGB" | "linearRGB" | "inherit";
  [key: string]: string | number | undefined; // additional attributes allowed
}
```

## Usage with React

Import the hook from the **`hypercomp/react`** entry point (peer dependency: `react`). `useFilter` ties the lifetime of a DOM-mounted filter to the component: it generates a stable key, renders on mount via `useLayoutEffect`, and unmounts on cleanup.

```tsx
import { Effect, useFilter } from "hypercomp/react";

const MyComponent = () => {
  return (
    <div style={{ filter: useFilter(Effect.source.dilate(2)) }}>
      hello world
    </div>
  );
};
```

`useFilter(filter: Filter | Effect)` returns the `url(#…)` string. This is the recommended path for React projects — it avoids both the data-URL gotcha and manual `unmount` bookkeeping.

## Light sources (`Light.*`)

Constructed via the `Light` export; passed to `.specular(...)` / `.diffuse(...)` (see [operators](operators.md)).

| Constructor | Config keys |
|---|---|
| `Light.pointLight(config?)` | `x?: number`, `y?: number`, `z?: number` |
| `Light.distantLight(config?)` | `azimuth?: number`, `elevation?: number` |
| `Light.spotlight(config?)` | `x?`, `y?`, `z?`, `pointsAtX?`, `pointsAtY?`, `pointsAtZ?` (all `number`), `falloff?: number` (→ `specularExponent`), `angle?: number` (→ `limitingConeAngle`) |

```typescript
import { Light } from "hypercomp";
Light.pointLight({ x: 460, y: 110, z: 680 });
```

## Transfer functions (`Transfer.*`)

Constructed via the `Transfer` export; passed to a `.componentTransfer({ r, g, b, a })` channel (see [operators](operators.md)).

| Constructor | Args |
|---|---|
| `Transfer.gamma(amplitude, exponent, offset)` | three `number` |
| `Transfer.linear(slope, intercept)` | two `number` |
| `Transfer.table(values)` | `values: number[]` |
| `Transfer.discrete(values)` | `values: number[]` |

```typescript
import { Effect, Transfer } from "hypercomp";
// Increase contrast of the alpha channel:
Effect.source.componentTransfer({ a: Transfer.linear(18, -9) });
```

## Base region config

Every operator's `config` extends `BaseConfig`, which defines the filter-effect subregion:

```typescript
interface BaseConfig {
  x?: string | number;
  y?: string | number;
  width?: string | number;
  height?: string | number;
}
```

Set these when a primitive should only affect part of the filter region; otherwise omit them.

## Gotchas

- **Always render with a key** (`css(effect, key)`) or `useFilter`. Keyless data-URL rendering breaks in Safari (no data-URL CSS-filter support) and breaks `.image()` in Chrome.
- **Effects are immutable.** Each method returns a new `Effect`; chain or reassign — there is no in-place mutation.
- **`.displace(map, scale, config?)`** — the displacement-map `Effect` is the FIRST argument, the numeric `scale` is SECOND. Mixing them up is the most common type error.
- **Shorthand keys are remapped**, so an unknown/raw-SVG key is silently ignored: drop-shadow color is `color` (not `flood-color`); turbulence octaves is `octaves` (not `numOctaves`); spotlight cone is `angle` (not `limitingConeAngle`); lighting strength is `strength` (not `specularConstant`/`diffuseConstant`).
- **A DOM is required** at `css(effect, key)` time — it appends a hidden `<svg>` to `document.body`. For non-DOM/SSR output, use `compile` instead.
- **`.in()` is a method named `in`** (the `in` compositing operator). It is valid as a method name even though `in` is a JS keyword.
- **Lighting compositing:** specular wants additive blending (`.screen`), diffuse wants `.multiply` — per the library's own guidance.

## Recipes

All verified-shape examples from the library README / examples.

### Squiggly outline (flood + dilation difference + fractal-noise displacement)

```tsx
import { Effect, css, fractalNoise } from "hypercomp";

const radius = 2, width = 2, freq = 0.01, octaves = 1, scale = 15;

const effects = Effect.flood("#30597E")
  .in(Effect.source.dilate(radius + width))   // flood, clipped to the wider dilation
  .out(Effect.source.dilate(radius))          // minus the narrower dilation = a stroke band
  .displace(fractalNoise(freq, { octaves }), scale) // wobble it with noise
  .over(Effect.source);                        // draw over the original

return <div style={{ filter: css(effects, "squiggle") }}>hello world</div>;
```

(`fractalNoise` is also available as `Effect.fractalNoise`.)

### Sharp-edge dilate + blue shadow (Sobel via convolution)

```tsx
import { Effect, css } from "hypercomp";

const withEdges = Effect.merge([
  Effect.source,
  Effect.source.convolve([1, 0, -1, 2, 0, -2, 1, 0, -1]), // x-direction Sobel
  Effect.source.convolve([1, 2, 1, 0, 0, 0, -1, -2, -1]), // y-direction Sobel
])
  .dilate(2)
  .shadow(1, { color: "blue" });

return <div style={{ filter: css(withEdges, "edges") }}>hello world</div>;
```

### Lit relief (blur as bump map → specular light → screen onto black)

```tsx
import { Effect, Light, css } from "hypercomp";

const withLight = Effect.flood("black").screen(
  Effect.sourceAlpha
    .blur(1)
    .specular(Light.pointLight({ x: 460, y: 110, z: 680 }), {
      strength: 4,
      shininess: 20,
    })
);

return <div style={{ filter: css(withLight, "lit") }}>hello world</div>;
```

### Gooey edges (single-element, no merge)

```tsx
import { Effect, css } from "hypercomp";

const goo = Effect.source.atop(
  Effect.source.blur(10).colorMatrix({ a: { a: 19, o: -9 } })
);

return <div style={{ filter: css(goo, "goo") }}>hello world</div>;
```
