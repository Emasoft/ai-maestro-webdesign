# react-colorful — Component & Prop API

## Table of Contents

- [Picker component matrix](#picker-component-matrix)
- [Picker props](#picker-props)
- [HexColorInput props](#hexcolorinput-props)
- [Color-model types (TypeScript)](#color-model-types-typescript)

Authoritative export list, prop contracts, and TypeScript types for
[`react-colorful`](https://github.com/omgovich/react-colorful) v5.7.0. Match
component names, prop names, and value formats to this file verbatim — never
paraphrase them from memory. If the installed version differs and behavior
conflicts, defer to the installed package's own types.

## Picker component matrix

All 15 picker components share the same props (`color`, `onChange`,
`onChangeEnd?`, plus every `<div>` attribute). They differ only in the
**value format** of `color` and the callback argument:

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

Plus one input component: `HexColorInput` (a hex text field, see below). And
one tooling export: `setNonce`.

## Picker props

Every picker accepts `Partial<ColorPickerBaseProps<T>>`:

| Prop          | Type                 | Required | Description                                                                   |
| ------------- | -------------------- | -------- | ----------------------------------------------------------------------------- |
| `color`       | format-specific `T`  | no\*     | Current color value. Defaults to the model's default (e.g. black) if omitted. |
| `onChange`    | `(color: T) => void` | no\*     | Fires on every change — during drag, on each arrow-key press.                 |
| `onChangeEnd` | `(color: T) => void` | no       | Fires once when the gesture ends (mouseup / touchend / keyup).                |

\* All props are optional in the type (`Partial`), but a controlled picker
needs both `color` and `onChange`. Without `onChange` the picker renders but
cannot be changed by the parent.

Pickers also accept **every** standard `<div>` attribute (`className`,
`style`, `aria-label`, `id`, …) — except `color`, `onChange`, and
`onChangeCapture`, which are reserved. The component renders a single root
`<div class="react-colorful">`.

## HexColorInput props

`HexColorInput` is a hex text field (no built-in styling) that pairs with any
picker via shared state. It extends `ColorInputBaseProps`:

| Prop       | Type                      | Default | Description                                 |
| ---------- | ------------------------- | ------- | ------------------------------------------- |
| `color`    | `string`                  | —       | Current hex value (shared with the picker). |
| `onChange` | `(color: string) => void` | —       | Fires with a **valid** hex string only.     |
| `prefixed` | `boolean`                 | `false` | Display the leading `#`.                    |
| `alpha`    | `boolean`                 | `false` | Accept `#rgba` / `#rrggbbaa` (8-digit) hex. |

It also accepts every standard `<input>` attribute (`placeholder`,
`autoFocus`, `className`, …) except `value` and `onChange`, which are
reserved. It validates and escapes non-hex characters internally and only
calls `onChange` with a syntactically valid value.

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
