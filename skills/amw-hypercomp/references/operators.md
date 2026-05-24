# hypercomp — Operator Catalog

Verified against the library TypeScript source (`hypercomp` 0.4.x). Every method below returns a **new** `Effect` (immutable builder). Every config object also accepts the base region keys `x`, `y`, `width`, `height` (`string | number`) to bound the primitive's filter region — these are omitted from each entry. Shorthand config keys shown here are the public API; they are remapped to raw SVG attribute names internally, so use the shorthand exactly as written.

## Table of Contents

- [Constant inputs](#constant-inputs)
- [Basis functions (static on `Effect`)](#basis-functions-static-on-effect)
- [Compositing functions (`feComposite`)](#compositing-functions-fecomposite)
- [Common transforms](#common-transforms)
- [Blending functions (`feBlend`)](#blending-functions-feblend)
- [Morphology functions (`feMorphology`)](#morphology-functions-femorphology)
- [Color manipulation (`feColorMatrix` / `feComponentTransfer`)](#color-manipulation-fecolormatrix--fecomponenttransfer)
- [Lighting functions](#lighting-functions)

## Constant inputs

Static getters on `Effect`; usable as a chain start or as an input to a compositing/blending method.

| Accessor | SVG input |
|---|---|
| `Effect.source` | `SourceGraphic` |
| `Effect.sourceAlpha` | `SourceAlpha` |
| `Effect.background` | `BackgroundImage` |
| `Effect.backgroundAlpha` | `BackgroundAlpha` |
| `Effect.fill` | `FillPaint` |
| `Effect.stroke` | `StrokePaint` |

## Basis functions (static on `Effect`)

| Call | Args | Config keys | Compiles to |
|---|---|---|---|
| `Effect.flood(color, config?)` | `color: string` | `opacity?: number` | `feFlood` |
| `Effect.image(href, config?)` | `href: string` | `preserveAspectRatio?: string`, `crossorigin?: "anonymous" \| "use-credentials"` | `feImage` |
| `Effect.merge(inputs, config?)` | `inputs: Effect[]` | (region only) | `feMerge` |
| `Effect.turbulence(frequency, config?)` | `frequency: number` | `octaves?: number`, `seed?: number`, `stitch?: "noStitch" \| "stitch"` | `feTurbulence` (`type="turbulence"`) |
| `Effect.fractalNoise(frequency, config?)` | `frequency: number` | `octaves?: number`, `seed?: number`, `stitch?: "noStitch" \| "stitch"` | `feTurbulence` (`type="fractalNoise"`) |

`merge` layers its array with the **last** element on top.

## Compositing functions (`feComposite`)

Pixel/Porter-Duff operators. Signature pattern: `.<op>(input, config?)`, where `input` is the **bottom** layer and `this` is the top.

| Method | Operator |
|---|---|
| `.over(input, config?)` | `over` |
| `.in(input, config?)` | `in` (method is named `in`) |
| `.out(input, config?)` | `out` |
| `.atop(input, config?)` | `atop` |
| `.xor(input, config?)` | `xor` |
| `.arithmetic(input, config?)` | `arithmetic` — config adds `k1?, k2?, k3?, k4?: number` |

All compile to `feComposite`. Arithmetic result = `k1·i1·i2 + k2·i1 + k3·i2 + k4`.

## Common transforms

| Method | Args | Config keys | Compiles to |
|---|---|---|---|
| `.blur(stdDeviation, config?)` | `stdDeviation: number` | `edgeMode?: "duplicate" \| "wrap" \| "none"` | `feGaussianBlur` |
| `.convolve(kernel, config?)` | `kernel: number[]` | `order?: number \| [number, number]`, `divisor?: number`, `bias?: number`, `targetX?: number`, `targetY?: number`, `edgeMode?: "duplicate" \| "wrap" \| "none"`, `preserveAlpha?: boolean` | `feConvolveMatrix` |
| `.displace(map, scale, config?)` | `map: Effect` (displacement map, **first** arg), `scale: number` | `xChannel?: "R" \| "G" \| "B" \| "A"`, `yChannel?: "R" \| "G" \| "B" \| "A"` | `feDisplacementMap` |
| `.offset(config?)` | — | `dx?: number`, `dy?: number` | `feOffset` |
| `.shadow(stdDeviation, config?)` | `stdDeviation: number` (the `Effect` method requires it; the standalone `shadow()` function defaults it to `2`) | `dx?: number`, `dy?: number`, `color?: string`, `opacity?: number` | `feDropShadow` |
| `.tile(config?)` | — | (region only) | `feTile` |

`order` for `.convolve`: a single number ⇒ square kernel; an array ⇒ `[width, height]`.

## Blending functions (`feBlend`)

All share the signature `.<mode>(input, config?)` (`input` is the bottom layer) and compile to `feBlend` with the corresponding `mode`.

`.normal` · `.multiply` · `.screen` · `.overlay` · `.darken` · `.lighten` · `.colorDodge` · `.colorBurn` · `.hardLight` · `.softLight` · `.difference` · `.exclusion` · `.hue` · `.saturation` · `.color` · `.luminosity`

(Method `.colorDodge` → SVG `color-dodge`, `.hardLight` → `hard-light`, etc. Use the camelCase method name; the kebab-case is internal.)

## Morphology functions (`feMorphology`)

| Method | Args | Compiles to |
|---|---|---|
| `.dilate(radius, config?)` | `radius: number` | `feMorphology` (`operator="dilate"`) |
| `.erode(radius, config?)` | `radius: number` | `feMorphology` (`operator="erode"`) |

Config is region-only.

## Color manipulation (`feColorMatrix` / `feComponentTransfer`)

| Method | Args | Compiles to |
|---|---|---|
| `.colorMatrix(matrix, config?)` | `matrix: number[] \| ColorMatrix` | `feColorMatrix` (`type="matrix"`) |
| `.saturate(amount, config?)` | `amount: number` | `feColorMatrix` (`type="saturate"`) |
| `.hueRotate(angle, config?)` | `angle: number` | `feColorMatrix` (`type="hueRotate"`) |
| `.luminanceToAlpha(config?)` | — | `feColorMatrix` (`type="luminanceToAlpha"`) |
| `.componentTransfer(config?)` | — | `feComponentTransfer` — config keys `r?, g?, b?, a?` each take a `Transfer.*` function |

`matrix` is the SVG 4×5 color matrix (last column = offset). Provide either 20 numbers, or a sparse `ColorMatrix` object (defaults: 1 on the diagonal, 0 elsewhere):

```typescript
type ColorMatrixRow = { r?: number; g?: number; b?: number; a?: number; o?: number /* offset */ };
type ColorMatrix    = { r?: ColorMatrixRow; g?: ColorMatrixRow; b?: ColorMatrixRow; a?: ColorMatrixRow };
```

Example — boost alpha contrast: `.colorMatrix({ a: { a: 19, o: -9 } })`.

For `.componentTransfer`, see the `Transfer.*` functions in [render-and-react](render-and-react.md):

```typescript
Effect.source.componentTransfer({ a: Transfer.linear(18, -9) }); // raise alpha contrast
```

## Lighting functions

Take a light source and use the input as a height/bump map.

| Method | Args | Config keys | Compiles to |
|---|---|---|---|
| `.specular(light, config?)` | `light: PointLight \| DistantLight \| Spotlight` | `strength?: number`, `shininess?: number`, `scale?: number`, `color?: string` | `feSpecularLighting` |
| `.diffuse(light, config?)` | `light: PointLight \| DistantLight \| Spotlight` | `strength?: number`, `scale?: number`, `color?: string` | `feDiffuseLighting` |

Compositing guidance from the library docs: composite a `.specular(...)` result with **additive** blending (e.g. `.screen(...)`); composite a `.diffuse(...)` result with the **`.multiply(...)`** blend mode. Light sources are constructed via `Light.*` — see [render-and-react](render-and-react.md).
