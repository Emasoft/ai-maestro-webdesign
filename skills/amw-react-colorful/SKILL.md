---
name: amw-react-colorful
description: react-colorful reference — the tiny dependency-free React/Preact color-picker component (HexColorPicker, RgbaColorPicker, HslColorPicker, HexColorInput, setNonce). Covers the 15 picker components, the controlled color/onChange/onChangeEnd props, the 6 color-model types, HexColorInput alpha/prefixed props, CSS class hooks, and the setNonce CSP helper. Does NOT trigger on generic color help, palette/token design, or choosing brand colors. Use when wiring a react-colorful color-picker widget.
version: 0.1.0
---

# react-colorful Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Reference for [`react-colorful`](https://github.com/omgovich/react-colorful) (v5.7.0) — a tiny (~2.8 KB gzipped), dependency-free, tree-shakeable color-picker component for React and Preact. It is the recommended widget whenever a design needs an **interactive in-page color picker** (a draggable saturation/hue surface, optionally with an alpha track and a hex text input).

This skill documents the real exported API so an agent can wire the component correctly **offline** without re-reading the upstream source. It is API reference only — it does not bundle the library source and does not emit HTML/JSX artifacts itself.

This skill owns the *runtime widget* a user drags to pick a value. It is distinct from color *selection*: the orchestrator's color-system reference owns palette/token *design* (which colors, oklch scales, contrast).

## Reference index

Detailed API tables and integration recipes live in this skill's own reference files. The COMPLETE table of contents of each is embedded immediately after its link.

[component-api](./references/component-api.md) — exported components, prop contracts, and the TypeScript color-model types:

- Picker component matrix
- Picker props
- HexColorInput props
- Color-model types (TypeScript)

[styling-and-integration](./references/styling-and-integration.md) — theming, CSP, a full worked example, and the failure-mode playbook:

- Styling (CSS class hooks)
- CSP nonce
- Worked example
- Error handling

## Instructions

1. Confirm the request is about an interactive picker **widget** in a React/Preact app — not about choosing a palette or designing tokens. If it is the latter, hand back to the orchestrator (color-system owns palette design).
2. Pick the component by required value format from the picker matrix in component-api: HEX string → `HexColorPicker`; RGB(A) object → `RgbColorPicker`/`RgbaColorPicker`; CSS string → the `*StringColorPicker` variants; etc.
3. Wire it as a **controlled** component: hold the value in `useState` (initialized in the chosen format), pass `color={value}` and `onChange={setValue}`. The component never holds its own state — a missing `onChange` makes it read-only.
4. Use `onChangeEnd` (not `onChange`) for expensive side-effects — DB writes, undo/redo snapshots, network calls — because `onChange` fires on every drag tick and key press.
5. For a text field, add `HexColorInput` driven by the **same** state; set `prefixed` to show `#`, set `alpha` to accept `#rgba`/`#rrggbbaa`. Props are in component-api.
6. Style via the CSS class hooks (override in your own stylesheet) — the base stylesheet auto-injects, so do NOT import a CSS file. Hooks and a CSS example are in styling-and-integration.
7. Under a strict Content-Security-Policy without Webpack nonce support, call `setNonce(hash)` once before the first picker renders (see styling-and-integration).
8. In TypeScript, import the matching color-model type (`RgbColor`, `HslaColor`, …) from the package root; the type definitions are in component-api.

A full controlled hex-picker example (picker + matching `HexColorInput` + expensive save on gesture end) is in styling-and-integration § Worked example.

## Examples

The worked example — a controlled hex picker with a matching `HexColorInput` and an expensive save deferred to `onChangeEnd` — lives in [styling-and-integration](./references/styling-and-integration.md) § Worked example.
> [styling-and-integration.md] Styling (CSS class hooks) · CSP nonce · Worked example · Error handling

## Output

This skill produces no standalone artifacts — it provides `react-colorful` API answers and JSX snippets. Any HTML/React UI that embeds the picker is assembled by `amw-wireframe-builder-agent` (with [SKILL](../amw-shadcn-ui/SKILL.md) / [SKILL](../amw-tailwind-4/SKILL.md) for the surrounding chrome).

## Error Handling

The failure-mode playbook (uncontrolled/read-only picker from a missing `onChange`, format mismatch, jank from heavy work in `onChange`, CSP nonce errors) lives in [styling-and-integration](./references/styling-and-integration.md) § Error handling.
> [styling-and-integration.md] Styling (CSS class hooks) · CSP nonce · Worked example · Error handling

## Trigger conditions

Invoke this skill when the request is specifically about the `react-colorful` color-picker widget:

- wiring an interactive in-page color picker into a React or Preact UI
- choosing the right picker component for a value format (HEX string, RGB(A)/HSL(A)/HSV(A) object, or CSS string)
- the controlled `color`/`onChange`/`onChangeEnd` pattern and why `onChangeEnd` exists
- adding a hex text input (`HexColorInput`) with `prefixed` / `alpha`
- theming the picker via its CSS class hooks
- the `setNonce` CSP helper or the exported color-model types

Do NOT invoke this skill for generic "color help", "pick a color scheme", "choose brand colors", palette/contrast/token design, or framework-agnostic CSS — those belong to the orchestrator or to its color-system reference. This skill is about the runtime widget, not about which colors to choose.

## Prerequisites

- **Peer dependencies (user responsibility):** `react >=16.8.0` and `react-dom >=16.8.0` (hooks-era React; works with Preact via React aliasing). The host project must already use React/Preact — this is a component, not a standalone tool.
- **Install:** `npm install react-colorful` (no transitive dependencies; ships its own TypeScript types).
- No build step, no CSS import, and no runtime binaries are required by this skill — it is pure documentation. The base stylesheet self-injects at runtime.

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during **Phase B** when an approved design includes an interactive color-picker widget, or pulled in by `amw-wireframe-builder-agent` while assembling React UI. Callable directly on `react-colorful` API questions. The skill's techniques are NOT limited to what any command exposes.

## Position in flow

REFERENCE. Loaded when the orchestrator (or a producer sub-agent) needs authoritative `react-colorful` API guidance to embed a working picker into a React/Preact target.

## Resources

This skill's own reference files are linked with their full TOCs in the Reference index above (component-api; styling-and-integration). Related skills and upstream:

- [SKILL](../amw-design-principles/SKILL.md) — the orchestrator; decides whether an interactive picker belongs in the design at all and routes here. It also owns the color-system reference (palette and token design — oklch scales, contrast).
- [SKILL](../amw-shadcn-ui/SKILL.md) — for the popover / button / dialog chrome commonly wrapped around a picker (e.g. a swatch button that opens the picker in a popover).
- [SKILL](../amw-tailwind-4/SKILL.md) — for utility-class styling of the wrapper; the picker's own appearance is overridden via its CSS class hooks.
- Upstream: `https://github.com/omgovich/react-colorful` (MIT). This skill reflects v5.7.0.

## Non-negotiables

- Does NOT own broad design intent or color *selection*. The orchestrator ([SKILL](../amw-design-principles/SKILL.md)) decides whether an interactive picker is the right surface; its color-system reference decides which colors. This skill only answers `react-colorful` widget questions.
- Pickers are **controlled** components with no internal state. Always pass both `color` and `onChange`, with `color` in the format the chosen component expects. Mixing formats (e.g. an object value into `HexColorPicker`) breaks the widget.
- Never import a CSS file for the base styles — the stylesheet self-injects. Theme only via the documented class hooks, scoped under a parent selector.
- Use `onChangeEnd` for expensive side-effects; never run DB writes / network calls / undo snapshots inside `onChange` (it fires on every drag frame).
- Never paraphrase component names, prop names, or value formats from memory — they are fixed by the upstream API documented here (v5.7.0). If the installed version differs and behavior conflicts, defer to the installed package's own types.
- English-only content across the skill. No third-language characters in any file.
