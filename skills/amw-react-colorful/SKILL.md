---
name: amw-react-colorful
description: react-colorful reference — the tiny dependency-free React/Preact color-picker component (HexColorPicker, RgbaColorPicker, HslColorPicker, HexColorInput, setNonce). Covers the 15 picker components, their controlled color/onChange/onChangeEnd props, the 6 color-model types, HexColorInput's alpha/prefixed props, CSS class hooks for theming, and the CSP nonce helper. Triggers on "react-colorful", "color picker component", "hex color input", "rgba color picker", "hsl color picker", "HexColorPicker", "RgbaColorPicker", "HexColorInput". Does NOT trigger on generic "color help", "pick a color scheme", "choose brand colors", or palette/token design — those belong to the orchestrator and color-system. Use when wiring an interactive in-page color-picker widget into a React/Preact UI. Trigger with "react-colorful" or "color picker component".
version: 0.1.0
---

# react-colorful Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Reference for [`react-colorful`](https://github.com/omgovich/react-colorful) (v5.7.0) — a tiny (~2.8 KB gzipped), dependency-free, tree-shakeable color-picker component for React and Preact. It is the recommended widget whenever a design needs an **interactive in-page color picker** (a draggable saturation/hue surface, optionally with an alpha track and a hex text input).

This skill documents the real exported API — component names, the controlled `color`/`onChange`/`onChangeEnd` contract, the six color-model TypeScript types, `HexColorInput`'s extra props, the CSS class hooks for theming, and the `setNonce` CSP helper — so an agent can wire the component correctly **offline** without re-reading the upstream source. It is API reference only; it does not bundle the library source and does not emit HTML/JSX artifacts itself.

This is distinct from [color-system](../amw-design-principles/color-system.md): that file owns palette/token *design* (which colors, oklch scales, contrast). This skill owns the *runtime widget* a user drags to pick a value.

## Instructions

1. Confirm the request is about an interactive picker **widget** in a React/Preact app — not about choosing a palette or designing tokens. If it is the latter, hand back to the orchestrator / [color-system](../amw-design-principles/color-system.md).
2. Pick the component by required value format from the [picker matrix](#picker-component-matrix): HEX string → `HexColorPicker`; RGB(A) object → `RgbColorPicker`/`RgbaColorPicker`; CSS string → the `*StringColorPicker` variants; etc.
3. Wire it as a **controlled** component: hold the value in `useState` (initialized in the chosen format), pass `color={value}` and `onChange={setValue}`. The component never holds its own state — a missing `onChange` makes it read-only.
4. Use `onChangeEnd` (not `onChange`) for expensive side-effects — DB writes, undo/redo snapshots, network calls — because `onChange` fires on every drag tick and key press.
5. For a text field, add `HexColorInput` driven by the **same** state; set `prefixed` to show `#`, set `alpha` to accept `#rgba`/`#rrggbbaa`.
6. Style via the documented [CSS class hooks](#styling-css-class-hooks) (override in your own stylesheet) — the base stylesheet auto-injects, so do NOT import a CSS file.
7. Under a strict Content-Security-Policy without Webpack nonce support, call `setNonce(hash)` once before the first picker renders.
8. In TypeScript, import the matching color-model type (`RgbColor`, `HslaColor`, …) to type your state.

See the [worked example](#worked-example) below.

## Picker component matrix

All 15 picker components share the same props (`color`, `onChange`, `onChangeEnd?`, plus every `<div>` attribute). They differ only in the **value format** of `color` and the callback argument:

| Import                      | `color` value example              | Format       |
| --------------------------- | ---------------------------------- | ------------ |
| `HexColorPicker`            | `"#ffffff"`                        | HEX string   |
| `HexAlphaColorPicker`       | `"#ffffff88"`                      | HEX+alpha    |
| `RgbColorPicker`            | `{ r: 255, g: 255, b: 255 }`       | object       |
| `RgbaColorPicker`           | `{ r: 255, g: 255, b: 255, a: 1 }` | object       |
| `RgbStringColorPicker`      | `"rgb(255, 255, 255)"`             | CSS string   |
| `RgbaStringColorPicker`     | `"rgba(255, 255, 255, 1)"`         | CSS string   |
| `HslColorPicker`            | `{ h: 0, s: 0, l: 100 }`           | object       |
| `HslaColorPicker`           | `{ h: 0, s: 0, l: 100, a: 1 }`     | object       |
| `HslStringColorPicker`      | `"hsl(0, 0%, 100%)"`               | CSS string   |
| `HslaStringColorPicker`     | `"hsla(0, 0%, 100%, 1)"`           | CSS string   |
| `HsvColorPicker`            | `{ h: 0, s: 0, v: 100 }`           | object       |
| `HsvaColorPicker`           | `{ h: 0, s: 0, v: 100, a: 1 }`     | object       |
| `HsvStringColorPicker`      | `"hsv(0, 0%, 100%)"`               | CSS string   |
| `HsvaStringColorPicker`     | `"hsva(0, 0%, 100%, 1)"`           | CSS string   |

Plus one input component: `HexColorInput` (a hex text field, see below). And one tooling export: `setNonce`.

## Picker props

Every picker accepts `Partial<ColorPickerBaseProps<T>>`:

| Prop          | Type                | Required | Description                                                                  |
| ------------- | ------------------- | -------- | ---------------------------------------------------------------------------- |
| `color`       | format-specific `T` | no\*     | Current color value. Defaults to the model's default (e.g. black) if omitted. |
| `onChange`    | `(color: T) => void`| no\*     | Fires on every change — during drag, on each arrow-key press.                |
| `onChangeEnd` | `(color: T) => void`| no       | Fires once when the gesture ends (mouseup / touchend / keyup).               |

\* All props are optional in the type (`Partial`), but a controlled picker needs both `color` and `onChange`. Without `onChange` the picker renders but cannot be changed by the parent.

Pickers also accept **every** standard `<div>` attribute (`className`, `style`, `aria-label`, `id`, …) — except `color`, `onChange`, and `onChangeCapture`, which are reserved. The component renders a single root `<div class="react-colorful">`.

## HexColorInput props

`HexColorInput` is a hex text field (no built-in styling) that pairs with any picker via shared state. It extends `ColorInputBaseProps`:

| Prop       | Type                     | Default | Description                                  |
| ---------- | ------------------------ | ------- | -------------------------------------------- |
| `color`    | `string`                 | —       | Current hex value (shared with the picker).  |
| `onChange` | `(color: string) => void`| —       | Fires with a **valid** hex string only.      |
| `prefixed` | `boolean`                | `false` | Display the leading `#`.                     |
| `alpha`    | `boolean`                | `false` | Accept `#rgba` / `#rrggbbaa` (8-digit) hex.  |

It also accepts every standard `<input>` attribute (`placeholder`, `autoFocus`, `className`, …) except `value` and `onChange`, which are reserved. It validates and escapes non-hex characters internally and only calls `onChange` with a syntactically valid value.

## Color-model types (TypeScript)

Exported from the package root for typing your own state:

```ts
interface RgbColor  { r: number; g: number; b: number }
interface RgbaColor extends RgbColor { a: number }
interface HslColor  { h: number; s: number; l: number }
interface HslaColor extends HslColor { a: number }
interface HsvColor  { h: number; s: number; v: number }
interface HsvaColor extends HsvColor { a: number }
```

```ts
import { HslColorPicker, HslColor } from "react-colorful";
const initial: HslColor = { h: 0, s: 0, l: 0 };
```

## Styling (CSS class hooks)

The base stylesheet is injected automatically on first render — **do not import any CSS file**. Override appearance by targeting these class hooks in your own stylesheet (scope under a parent class to avoid global overrides):

| Class                              | Targets                          |
| ---------------------------------- | -------------------------------- |
| `.react-colorful`                  | root container (set width/height)|
| `.react-colorful__saturation`      | saturation/value square          |
| `.react-colorful__hue`             | hue slider track                 |
| `.react-colorful__hue-pointer`     | hue slider handle                |
| `.react-colorful__alpha`           | alpha slider track (alpha pickers)|
| `.react-colorful__alpha-pointer`   | alpha slider handle              |
| `.react-colorful__last-control`    | the bottom-most slider (rounded corners) |

```css
.my-picker .react-colorful { height: 240px; }
.my-picker .react-colorful__hue { height: 40px; border-radius: 0 0 4px 4px; }
```

## CSP nonce

For a strict Content-Security-Policy environment that is **not** using Webpack's `__webpack_nonce__`, call `setNonce` once before any picker mounts so the injected `<style>` tag carries a matching nonce:

```ts
import { setNonce } from "react-colorful";
setNonce("r4nd0m-base64-nonce");
```

## Worked example

A controlled hex picker with a matching text input and an expensive save on gesture end:

```jsx
import { useState } from "react";
import { HexColorPicker, HexColorInput } from "react-colorful";

export function BrandColorField({ onSave }) {
  const [color, setColor] = useState("#aabbcc");

  return (
    <div className="my-picker">
      <HexColorPicker
        color={color}
        onChange={setColor}                 // every drag tick — keeps UI live
        onChangeEnd={(c) => onSave(c)}       // once on mouseup — the DB write
        aria-label="Brand color"
      />
      <HexColorInput
        color={color}
        onChange={setColor}                  // shares the same state
        prefixed
        placeholder="Type a color"
      />
    </div>
  );
}
```

For an RGBA object value, swap to `RgbaColorPicker` and initialize state as `{ r, g, b, a }`; the `onChange` argument is then an `RgbaColor` object, not a string.

## Output

This skill produces no standalone artifacts — it provides `react-colorful` API answers and JSX snippets. Any HTML/React UI that embeds the picker is assembled by `amw-wireframe-builder-agent` (with [shadcn-ui](../amw-shadcn-ui/SKILL.md) / [tailwind-4](../amw-tailwind-4/SKILL.md) for the surrounding chrome).

## Trigger conditions

Invoke this skill when the request is specifically about the `react-colorful` color-picker widget:

- wiring an interactive in-page color picker into a React or Preact UI
- choosing the right picker component for a value format (HEX string, RGB(A)/HSL(A)/HSV(A) object, or CSS string)
- the controlled `color`/`onChange`/`onChangeEnd` pattern and why `onChangeEnd` exists
- adding a hex text input (`HexColorInput`) with `prefixed` / `alpha`
- theming the picker via its CSS class hooks
- the `setNonce` CSP helper or the exported color-model types

Do NOT invoke this skill for generic "color help", "pick a color scheme", "choose brand colors", palette/contrast/token design, or framework-agnostic CSS — those belong to the orchestrator or to [color-system](../amw-design-principles/color-system.md). This skill is about the runtime widget, not about which colors to choose.

## Prerequisites

- **Peer dependencies (user responsibility):** `react >=16.8.0` and `react-dom >=16.8.0` (hooks-era React; works with Preact via React aliasing). The host project must already use React/Preact — this is a component, not a standalone tool.
- **Install:** `npm install react-colorful` (no transitive dependencies; ships its own TypeScript types).
- No build step, no CSS import, and no runtime binaries are required by this skill — it is pure documentation. The base stylesheet self-injects at runtime.

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during **Phase B** when an approved design includes an interactive color-picker widget, or pulled in by `amw-wireframe-builder-agent` while assembling React UI. Callable directly on `react-colorful` API questions. The skill's techniques are NOT limited to what any command exposes.

## Position in flow

REFERENCE. Loaded when the orchestrator (or a producer sub-agent) needs authoritative `react-colorful` API guidance to embed a working picker into a React/Preact target.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — the orchestrator; decides whether an interactive picker belongs in the design at all and routes here.
- [color-system](../amw-design-principles/color-system.md) — palette and token *design* (oklch scales, contrast). The picker reads/writes a color value; this file decides which color values are on-brand and accessible.
- [SKILL](../amw-shadcn-ui/SKILL.md) — for the popover / button / dialog chrome commonly wrapped around a picker (e.g. a swatch button that opens the picker in a popover).
- [SKILL](../amw-tailwind-4/SKILL.md) — for utility-class styling of the wrapper; the picker's own appearance is overridden via its CSS class hooks documented above.
- Upstream: `https://github.com/omgovich/react-colorful` (MIT). This skill reflects v5.7.0.

## Non-negotiables

- Does NOT own broad design intent or color *selection*. The orchestrator ([SKILL](../amw-design-principles/SKILL.md)) decides whether an interactive picker is the right surface; [color-system](../amw-design-principles/color-system.md) decides which colors. This skill only answers `react-colorful` widget questions.
- Pickers are **controlled** components with no internal state. Always pass both `color` and `onChange`, with `color` in the format the chosen component expects. Mixing formats (e.g. an object value into `HexColorPicker`) breaks the widget.
- Never import a CSS file for the base styles — the stylesheet self-injects. Theme only via the documented class hooks, scoped under a parent selector.
- Use `onChangeEnd` for expensive side-effects; never run DB writes / network calls / undo snapshots inside `onChange` (it fires on every drag frame).
- Never paraphrase component names, prop names, or value formats from memory — they are fixed by the upstream API documented here (v5.7.0). If the installed version differs and behavior conflicts, defer to the installed package's own types.
- English-only content across the skill. No third-language characters in any file.

## Error Handling

- **Picker renders but won't change:** `onChange` is missing or not updating state — it is a controlled component, so the parent must own and update the value.
- **Value format mismatch (e.g. `[object Object]` in a hex field, or NaN channels):** the component does not match the value format. Match the component to the value: object pickers (`Rgb*`, `Hsl*`, `Hsv*` without `String`) take objects; `*StringColorPicker` and `Hex*` take strings.
- **`HexColorInput` "swallows" typed characters:** by design — it escapes non-hex characters and only emits valid hex via `onChange`. Enable `alpha` to allow 8-digit hex; enable `prefixed` to show the `#`.
- **Base styles missing under strict CSP:** the auto-injected `<style>` tag was blocked. Call `setNonce(hash)` before the first render (when not relying on Webpack's `__webpack_nonce__`).
- **Custom styles not applying:** the override selector is not specific enough or not scoped under a parent class. Increase specificity (e.g. `.your-wrapper .react-colorful__hue`) rather than editing the package.
- **Preact + TypeScript type conflicts (`@types/react` present):** add the `declaration.d.ts` React-namespace augmentation from the upstream README's Preact section; do not patch the package.
- **User actually wants a palette / color scheme, not a widget:** stop and hand back to the orchestrator / [color-system](../amw-design-principles/color-system.md) — that is outside this skill's scope.
