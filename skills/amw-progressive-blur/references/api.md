## Table of Contents

- [Component matrix](#component-matrix)
- [Shared props](#shared-props)
- [LinearBlur-only prop](#linearblur-only-prop)
- [Standard div attributes](#standard-div-attributes)
- [How the props interact](#how-the-props-interact)

# progressive-blur — API reference

Authoritative prop reference for the [`progressive-blur`](https://github.com/AndrewPrifer/progressive-blur) package (MIT, © 2024 Andrew Prifer). The two exported components, their shared props, `LinearBlur`'s `side` direction, and the layered-mask mechanism. The main `SKILL.md` keeps only the high-level entry points; this file is the authoritative source for prop names, defaults, and ranges. Never paraphrase these from memory — if the installed version differs and behavior conflicts, defer to the installed package's own TypeScript types.

## Component matrix

Both components are named exports from the package root. They share the same four props; `LinearBlur` adds `side`.

| Import        | Gradient shape                          | Strongest blur at | Extra prop |
| ------------- | --------------------------------------- | ----------------- | ---------- |
| `LinearBlur`  | linear (one axis)                       | the `side` edge   | `side`     |
| `RadialBlur`  | radial (`closest-side`, center-out)     | the center        | —          |

```tsx
import { RadialBlur, LinearBlur } from "progressive-blur";
```

## Shared props

Both `RadialBlur` and `LinearBlur` accept these (all optional, all with defaults):

| Prop                | Type     | Default         | Description                                                                                                  |
| ------------------- | -------- | --------------- | ---------------------------------------------------------------------------------------------------------- |
| `strength`          | `number` | `64`            | Peak blur radius **in pixels** at the most-blurred point of the gradient. Higher = blurrier.                |
| `steps`             | `number` | `8`             | Resolution of the gradient — how many stacked blur layers. Higher = smoother ramp but more GPU cost. Clamped to a minimum of 1. |
| `falloffPercentage` | `number` | `100`           | How much of the band is the **gradient (falloff)** region. `0` = no falloff (a hard, uniform blur edge); `100` = the entire band is a gradient. |
| `tint`              | `string` | `"transparent"` | Any valid CSS color washed over the blurred region as a gradient (clear → tint). Leave default for a pure blur with no color cast. |

## LinearBlur-only prop

`LinearBlur` adds:

| Prop   | Type                                       | Default | Description                                                                                              |
| ------ | ------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------ |
| `side` | `"left" \| "right" \| "top" \| "bottom"`   | `"top"` | The edge where the blur is **strongest**; the gradient fades toward the opposite edge. Also sets `transform-origin` so a `scale()` transform grows from that edge. |

## Standard div attributes

Both components also accept **every** standard `<div>` attribute (`className`, `style`, `id`, `aria-label`, …) — they spread `...props` onto the root element. Use `style`/`className` for positioning the overlay. The component merges your `style` after its own, so you can override anything except `pointer-events` (intentionally forced to `none` on the root — see `SKILL.md` § Non-negotiables).

## How the props interact

The library stacks `steps` absolutely-positioned `<div>`s, each with a `backdrop-filter: blur(...)` whose radius decreases per layer and a gradient `mask` that exposes only its slice of the band. The first layer carries the full `strength`; subsequent layers blur progressively less, masked to a moving window. The result is one continuous blur ramp built from `steps` discrete masks — more `steps` hides the banding.

- **`RadialBlur`** uses `radial-gradient(closest-side, …)` masks; blur is strongest at the center and clears toward the nearest edge. The solid-blur core occupies `100 - falloffPercentage`% of the radius.
- **`LinearBlur`** uses `linear-gradient(to <opposite-of-side>, …)` masks; blur is strongest at `side` and clears toward the opposite edge. The solid-blur region occupies `100 - falloffPercentage`% from the `side` edge.
