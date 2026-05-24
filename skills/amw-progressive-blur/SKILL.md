---
name: amw-progressive-blur
description: progressive-blur reference — the MIT drop-in progressive (gradient) backdrop-blur React component (RadialBlur + LinearBlur). Covers the two exported components, their strength/steps/falloffPercentage/tint props, LinearBlur's side direction, the layered backdrop-filter + gradient-mask mechanism, and the Chrome overflow+border-radius gotcha. Triggers on "progressive blur", "gradient backdrop blur", "progressive-blur", "linear blur mask", "radial blur mask", "fade-to-blur edge", "RadialBlur", "LinearBlur". Does NOT trigger on generic "add a blur", "make it blurry", "blur the background", or a uniform CSS filter:blur — those are plain CSS, not this component. Use when wiring a directional fade-to-blur overlay into a React UI. Trigger with "progressive blur" or "progressive-blur".
version: 0.1.0
---

# progressive-blur Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Reference for [`progressive-blur`](https://github.com/AndrewPrifer/progressive-blur) — a tiny, dependency-free, drop-in **progressive (gradient) backdrop blur** for React. A progressive blur fades the `backdrop-filter: blur()` strength along a gradient instead of applying one uniform blur, producing the "fade-to-blur" edge seen on iOS scroll bars, sticky headers, and glassy overlays. The package supports both a **linear** gradient (blur strongest on one edge) and a **radial** gradient (blur strongest at the center, clearing toward the rim).

This skill documents the real exported API — the two component names, their `strength`/`steps`/`falloffPercentage`/`tint` props, `LinearBlur`'s `side` direction, and the layered-mask rendering mechanism — so an agent can wire the component correctly **offline** without re-reading the upstream source. It is API reference only; it does not bundle the library source and does not emit HTML/JSX artifacts itself.

This is distinct from a plain CSS blur: `filter: blur()` / `backdrop-filter: blur()` apply one uniform blur over an entire box. This component renders a **gradient of blur** that ramps from clear to blurred. If the user only needs a uniform blur, the answer is plain CSS, not this component — hand back to the orchestrator.

## Instructions

1. Confirm the request needs a **gradient/progressive** blur (a fade-to-blur edge or a center-clear radial blur), not a uniform `filter: blur()`. If uniform is enough, hand back to the orchestrator — do not pull in this dependency.
2. Pick the component from the [component matrix](#component-matrix): a directional edge fade → `LinearBlur`; a center-out radial fade → `RadialBlur`.
3. The component is an **overlay**. Position it over the content you want progressively blurred, give it explicit dimensions, and set `pointer-events` is already handled (the root forces `pointer-events: none`, so clicks pass through to the content beneath). Typical placement: `position: absolute` over a scroll container or hero, sized to the band you want blurred.
4. Tune the look with the four shared props — `strength` (peak blur radius in px), `steps` (resolution/smoothness), `falloffPercentage` (how much of the band is gradient vs solid blur), `tint` (an optional color wash). See [shared props](#shared-props).
5. For `LinearBlur`, set `side` to the edge where the blur is **strongest** (`"top"` | `"bottom"` | `"left"` | `"right"`); the gradient fades toward the opposite edge. `side` also sets `transform-origin` so a `scale()` grows from the right edge.
6. Avoid the Chrome ancestor gotcha: do **not** put `overflow: hidden` **and** `border-radius` on a shared ancestor of the masked backdrop filter (see [Chrome gotcha](#chrome-gotcha-overflow--border-radius)).
7. Pass any standard `<div>` attribute (`className`, `style`, `id`, `aria-*`) for positioning/styling — both components extend `React.HTMLAttributes<HTMLDivElement>`.

See the [worked example](#worked-example) below.

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

`LinearBlur` adds:

| Prop   | Type                                       | Default | Description                                                                                              |
| ------ | ------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------ |
| `side` | `"left" \| "right" \| "top" \| "bottom"`   | `"top"` | The edge where the blur is **strongest**; the gradient fades toward the opposite edge. Also sets `transform-origin` so a `scale()` transform grows from that edge. |

Both components also accept **every** standard `<div>` attribute (`className`, `style`, `id`, `aria-label`, …) — they spread `...props` onto the root element. Use `style`/`className` for positioning the overlay. The component merges your `style` after its own, so you can override anything except `pointer-events` (intentionally forced to `none` on the root — see Non-negotiables).

### How the props interact

The library stacks `steps` absolutely-positioned `<div>`s, each with a `backdrop-filter: blur(...)` whose radius decreases per layer and a gradient `mask` that exposes only its slice of the band. The first layer carries the full `strength`; subsequent layers blur progressively less, masked to a moving window. The result is one continuous blur ramp built from `steps` discrete masks — more `steps` hides the banding.

- **`RadialBlur`** uses `radial-gradient(closest-side, …)` masks; blur is strongest at the center and clears toward the nearest edge. The solid-blur core occupies `100 - falloffPercentage`% of the radius.
- **`LinearBlur`** uses `linear-gradient(to <opposite-of-side>, …)` masks; blur is strongest at `side` and clears toward the opposite edge. The solid-blur region occupies `100 - falloffPercentage`% from the `side` edge.

## Chrome gotcha (overflow + border-radius)

Setting **both** `overflow: hidden` **and** `border-radius` on an ancestor of a masked `backdrop-filter` breaks rendering in Chrome (Chromium issue [40778541](https://issues.chromium.org/issues/40778541)). The upstream demo works around it by only applying the ancestor's `border-radius` when **not** in Chrome.

Mitigations, in order of preference:

1. Don't combine `overflow: hidden` + `border-radius` on a shared ancestor of the blur overlay.
2. Move the `border-radius` (or the clipping) to a different element than the one with `overflow: hidden`.
3. Apply rounding conditionally (skip it in Chrome) if the rounded clip is essential.

This is an upstream/browser limitation, not a config error — document it for the user; do not try to "fix" it inside the component.

## Worked example

A sticky scroll container whose top edge progressively blurs the content scrolling under a title bar:

```jsx
import { LinearBlur } from "progressive-blur";

export function FadeTopOverlay({ children }) {
  return (
    // The blur overlay must NOT share an ancestor that has BOTH
    // overflow:hidden AND border-radius (Chromium #40778541).
    <div style={{ position: "relative", height: 360 }}>
      <div style={{ overflowY: "auto", height: "100%" }}>{children}</div>

      <LinearBlur
        side="top"                 // blur strongest at the top edge, clears downward
        strength={64}              // 64px peak blur
        steps={8}                  // 8 stacked layers — smooth ramp
        falloffPercentage={95}     // almost the whole band is gradient
        tint="rgba(0,0,0,0.08)"    // faint dark wash for legibility
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 96,              // the band height to blur
          // pointer-events:none is already set by the component — clicks pass through
        }}
        aria-hidden                // decorative overlay
      />
    </div>
  );
}
```

For a center-clear radial spotlight blur (e.g. a hover effect over an image), swap to `RadialBlur`, drop `side`, size the overlay to cover the area, and animate its `transform: scale(...)`:

```jsx
import { RadialBlur } from "progressive-blur";

<RadialBlur
  strength={32}
  steps={8}
  falloffPercentage={85}     // solid-blur core is the inner 15% of the radius
  tint="transparent"
  style={{ position: "absolute", inset: 0, zIndex: -1 }}
/>
```

## Output

This skill produces no standalone artifacts — it provides `progressive-blur` API answers and JSX snippets. Any HTML/React UI that embeds the overlay is assembled by `amw-wireframe-builder-agent` (with [shadcn-ui](../amw-shadcn-ui/SKILL.md) / [tailwind-4](../amw-tailwind-4/SKILL.md) for the surrounding chrome).

## Trigger conditions

Invoke this skill when the request is specifically about the `progressive-blur` component:

- wiring a directional **fade-to-blur** edge (sticky header / scroll bar / hero overlay) into a React UI
- choosing between `LinearBlur` (edge fade) and `RadialBlur` (center-out fade)
- tuning the `strength` / `steps` / `falloffPercentage` / `tint` props or `LinearBlur`'s `side`
- understanding the layered `backdrop-filter` + gradient-mask mechanism
- the Chrome `overflow: hidden` + `border-radius` ancestor gotcha

Do NOT invoke this skill for a generic "add a blur", "make it blurry", "blur the background", or a uniform `filter: blur()` / `backdrop-filter: blur()` — those are plain one-line CSS and belong to the orchestrator, not this component. This skill is about the **gradient** progressive blur overlay, not uniform blur.

## Prerequisites

- **Peer dependencies (user responsibility):** `react` (`^18.2.0`) and `react-dom` (`^18.2.0`). The host project must already use React — this is a component, not a standalone tool.
- **Install:** `npm install progressive-blur` (no transitive runtime dependencies; ships its own TypeScript types).
- No build step, no CSS import, and no runtime binaries are required by this skill — it is pure documentation. The component is self-contained inline-styled markup.
- **Browser support:** relies on CSS `backdrop-filter` and `mask` (with `-webkit-` fallbacks already emitted by the component). Both are widely supported; effect degrades to no-blur where `backdrop-filter` is unsupported.

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during **Phase B** when an approved design includes a progressive/gradient backdrop-blur overlay, or pulled in by `amw-wireframe-builder-agent` while assembling React UI. Callable directly on `progressive-blur` API questions. The skill's techniques are NOT limited to what any command exposes.

## Position in flow

REFERENCE. Loaded when the orchestrator (or a producer sub-agent) needs authoritative `progressive-blur` API guidance to embed a working fade-to-blur overlay into a React target.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — the orchestrator; decides whether a progressive blur belongs in the design at all (vs a uniform CSS blur or no blur) and routes here.
- [SKILL](../amw-tailwind-4/SKILL.md) — for utility-class styling/positioning of the wrapper; the blur overlay itself is inline-styled via its props.
- [SKILL](../amw-shadcn-ui/SKILL.md) — for the card / header / dialog chrome commonly paired with a fade-to-blur edge.
- Upstream: `https://github.com/AndrewPrifer/progressive-blur` (MIT, © 2024 Andrew Prifer). This skill reflects the package's two-component (`RadialBlur` + `LinearBlur`) API.

## Non-negotiables

- Does NOT own broad design intent. The orchestrator ([SKILL](../amw-design-principles/SKILL.md)) decides whether a progressive blur is the right surface — and whether a blur is wanted at all; this skill only answers `progressive-blur` API questions.
- This is a **gradient** blur, not a uniform one. If the user wants a flat, even blur, the correct answer is plain CSS `filter: blur()` / `backdrop-filter: blur()` — do not pull in this dependency for that case.
- The component is a **decorative overlay** with `pointer-events: none` forced on its root so clicks pass through to the content beneath. Do not override `pointer-events` on the root — doing so traps interaction. Mark it `aria-hidden` when it is purely decorative.
- Never combine `overflow: hidden` + `border-radius` on a shared ancestor of the overlay (Chromium #40778541). This is a browser limitation, not a misconfiguration — surface it, do not patch the component.
- Never paraphrase component names, prop names, defaults, or value ranges from memory — they are fixed by the upstream API documented here (`RadialBlur` / `LinearBlur`; `strength`/`steps`/`falloffPercentage`/`tint`/`side`). If the installed version differs and behavior conflicts, defer to the installed package's own types.
- English-only content across the skill. No third-language characters in any file.

## Error Handling

- **No blur appears:** the overlay has no size, is behind the content (`z-index`), or sits over a transparent area — `backdrop-filter` blurs what is **behind** the element, so there must be content beneath it. Give the overlay explicit dimensions and ensure it stacks above the blurred content.
- **Edge looks banded/stepped instead of smooth:** `steps` is too low for the band size — raise `steps` (resolution) until the banding disappears; expect higher GPU cost.
- **Whole band is blurred with no clear region (or vice-versa):** adjust `falloffPercentage`. `0` = hard/uniform blur (no gradient); `100` = the entire band is gradient. The solid-blur region is `100 - falloffPercentage`% of the band.
- **Blur fades from the wrong edge (`LinearBlur`):** set `side` to the edge where the blur should be **strongest**; the gradient always fades toward the opposite edge.
- **Rendering breaks / artifacts in Chrome around rounded containers:** an ancestor has both `overflow: hidden` and `border-radius` (Chromium #40778541) — separate those properties onto different elements or skip the rounding in Chrome.
- **Clicks/scroll don't reach content under the overlay:** something re-enabled `pointer-events` on the overlay root. Leave it at the component's default (`none`).
- **No blur on an older/unsupported browser:** `backdrop-filter` is unavailable — the effect degrades to no blur. This is expected graceful degradation, not a bug.
- **User actually wants a uniform blur, not a gradient:** stop and hand back to the orchestrator — a one-line CSS `filter: blur()` is the right tool, not this component.
