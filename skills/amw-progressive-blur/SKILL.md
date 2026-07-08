---
name: amw-progressive-blur
description: progressive-blur reference — the MIT drop-in progressive (gradient) backdrop-blur React component (RadialBlur + LinearBlur). Covers the two components, their strength/steps/falloffPercentage/tint props, LinearBlur's side direction, the layered backdrop-filter plus gradient-mask mechanism, and the Chrome overflow + border-radius gotcha. Does NOT trigger on generic "add a blur", "make it blurry", or a uniform CSS filter blur. Use when wiring a progressive (gradient) backdrop-blur overlay.
---

# progressive-blur Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Reference for [`progressive-blur`](https://github.com/AndrewPrifer/progressive-blur) — a tiny, dependency-free, drop-in **progressive (gradient) backdrop blur** for React. A progressive blur fades the `backdrop-filter: blur()` strength along a gradient instead of applying one uniform blur, producing the "fade-to-blur" edge seen on iOS scroll bars, sticky headers, and glassy overlays. The package supports both a **linear** gradient (blur strongest on one edge) and a **radial** gradient (blur strongest at the center, clearing toward the rim).

This skill documents the real exported API — the two component names, their `strength`/`steps`/`falloffPercentage`/`tint` props, `LinearBlur`'s `side` direction, and the layered-mask rendering mechanism — so an agent can wire the component correctly **offline** without re-reading the upstream source. It is API reference only; it does not bundle the library source and does not emit HTML/JSX artifacts itself.

This is distinct from a plain CSS blur: `filter: blur()` / `backdrop-filter: blur()` apply one uniform blur over an entire box. This component renders a **gradient of blur** that ramps from clear to blurred. If the user only needs a uniform blur, the answer is plain CSS, not this component — hand back to the orchestrator.

## Reference index

The detailed prop reference, the Chrome ancestor gotcha, and the worked examples live in `references/` (progressive disclosure). Each entry below links the file and embeds its complete Table of Contents verbatim.

- [api](./references/api.md) — component matrix, full prop tables, prop interactions.
  - Component matrix
  - Shared props
  - LinearBlur-only prop
  - Standard div attributes
  - How the props interact
- [chrome-gotcha](./references/chrome-gotcha.md) — the Chrome `overflow: hidden` + `border-radius` ancestor bug and mitigations.
  - The bug
  - Mitigations
  - Why this is not a config error
- [examples](./references/examples.md) — copy-paste JSX (LinearBlur + RadialBlur) and the error-handling table.
  - LinearBlur — sticky top fade
  - RadialBlur — center-clear spotlight
  - Error handling

## Instructions

1. Confirm the request needs a **gradient/progressive** blur (a fade-to-blur edge or a center-clear radial blur), not a uniform `filter: blur()`. If uniform is enough, hand back to the orchestrator — do not pull in this dependency.
2. Pick the component: a directional edge fade → `LinearBlur`; a center-out radial fade → `RadialBlur`. The component matrix is in the api reference (see the Reference index above).
3. The component is an **overlay**. Position it over the content you want progressively blurred, give it explicit dimensions; `pointer-events` is already handled (the root forces `pointer-events: none`, so clicks pass through to the content beneath). Typical placement: `position: absolute` over a scroll container or hero, sized to the band you want blurred.
4. Tune the look with the four shared props — `strength` (peak blur radius in px), `steps` (resolution/smoothness), `falloffPercentage` (how much of the band is gradient vs solid blur), `tint` (an optional color wash). The shared-props table is in the api reference.
5. For `LinearBlur`, set `side` to the edge where the blur is **strongest** (`"top"` | `"bottom"` | `"left"` | `"right"`); the gradient fades toward the opposite edge. `side` also sets `transform-origin` so a `scale()` grows from that edge.
6. Avoid the Chrome ancestor gotcha: do **not** put `overflow: hidden` **and** `border-radius` on a shared ancestor of the masked backdrop filter. The detail and mitigations are in the chrome-gotcha reference.
7. Pass any standard `<div>` attribute (`className`, `style`, `id`, `aria-*`) for positioning/styling — both components extend `React.HTMLAttributes<HTMLDivElement>`.

Copy-paste JSX for both components is in the examples reference (see the Reference index above).

## Examples

Copy-paste JSX for both components — a `LinearBlur` sticky-top fade and a `RadialBlur` center-clear spotlight — lives in [examples](./references/examples.md), linked with its full TOC in the [Reference index](#reference-index) above.
> [examples.md] LinearBlur — sticky top fade · RadialBlur — center-clear spotlight · Error handling

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

## Error Handling

The full symptom → cause → fix table lives in the examples reference (see the Reference index above). Common cases: no blur (overlay has no size, wrong `z-index`, or nothing behind it), banded edge (`steps` too low), wrong fade edge (`side`), Chrome artifacts (`overflow: hidden` + `border-radius` ancestor — detail in the chrome-gotcha reference), and "user actually wants a uniform blur" (hand back to the orchestrator).

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — the orchestrator; decides whether a progressive blur belongs in the design at all (vs a uniform CSS blur or no blur) and routes here.
- [SKILL](../amw-tailwind-4/SKILL.md) — for utility-class styling/positioning of the wrapper; the blur overlay itself is inline-styled via its props.
- [SKILL](../amw-shadcn-ui/SKILL.md) — for the card / header / dialog chrome commonly paired with a fade-to-blur edge.

This skill's own references (api, chrome-gotcha, examples) are linked with their full Tables of Contents in the [Reference index](#reference-index) above.

Upstream: `https://github.com/AndrewPrifer/progressive-blur` (MIT, © 2024 Andrew Prifer). This skill reflects the package's two-component (`RadialBlur` + `LinearBlur`) API.

## Non-negotiables

- Does NOT own broad design intent. The orchestrator ([SKILL](../amw-design-principles/SKILL.md)) decides whether a progressive blur is the right surface — and whether a blur is wanted at all; this skill only answers `progressive-blur` API questions.
- This is a **gradient** blur, not a uniform one. If the user wants a flat, even blur, the correct answer is plain CSS `filter: blur()` / `backdrop-filter: blur()` — do not pull in this dependency for that case.
- The component is a **decorative overlay** with `pointer-events: none` forced on its root so clicks pass through to the content beneath. Do not override `pointer-events` on the root — doing so traps interaction. Mark it `aria-hidden` when it is purely decorative.
- Never combine `overflow: hidden` + `border-radius` on a shared ancestor of the overlay (Chromium #40778541). This is a browser limitation, not a misconfiguration — surface it, do not patch the component.
- Never paraphrase component names, prop names, defaults, or value ranges from memory — they are fixed by the upstream API documented in the api reference (`RadialBlur` / `LinearBlur`; `strength`/`steps`/`falloffPercentage`/`tint`/`side`). If the installed version differs and behavior conflicts, defer to the installed package's own types.
- English-only content across the skill. No third-language characters in any file.
