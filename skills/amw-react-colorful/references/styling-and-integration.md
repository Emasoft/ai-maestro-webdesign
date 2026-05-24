# react-colorful — Styling, CSP & Integration

## Table of Contents

- [Styling (CSS class hooks)](#styling-css-class-hooks)
- [CSP nonce](#csp-nonce)
- [Worked example](#worked-example)
- [Error handling](#error-handling)

How to theme the picker, wire it under a strict Content-Security-Policy, a
full controlled-component example, and the failure modes you will hit. The
picker is always a **controlled** component with no internal state.

## Styling (CSS class hooks)

The base stylesheet is injected automatically on first render — **do not
import any CSS file**. Override appearance by targeting these class hooks in
your own stylesheet (scope under a parent class to avoid global overrides):

| Class                            | Targets                                   |
| -------------------------------- | ----------------------------------------- |
| `.react-colorful`                | root container (set width/height)         |
| `.react-colorful__saturation`    | saturation/value square                   |
| `.react-colorful__hue`           | hue slider track                          |
| `.react-colorful__hue-pointer`   | hue slider handle                         |
| `.react-colorful__alpha`         | alpha slider track (alpha pickers)        |
| `.react-colorful__alpha-pointer` | alpha slider handle                       |
| `.react-colorful__last-control`  | the bottom-most slider (rounded corners)  |

```css
.my-picker .react-colorful { height: 240px; }
.my-picker .react-colorful__hue { height: 40px; border-radius: 0 0 4px 4px; }
```

## CSP nonce

For a strict Content-Security-Policy environment that is **not** using
Webpack's `__webpack_nonce__`, call `setNonce` once before any picker mounts
so the injected `<style>` tag carries a matching nonce:

```ts
import { setNonce } from "react-colorful";
setNonce("r4nd0m-base64-nonce");
```

## Worked example

A controlled hex picker with a matching text input and an expensive save on
gesture end:

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

For an RGBA object value, swap to `RgbaColorPicker` and initialize state as
`{ r, g, b, a }`; the `onChange` argument is then an `RgbaColor` object, not
a string.

## Error handling

- **Picker renders but won't change:** `onChange` is missing or not updating
  state — it is a controlled component, so the parent must own and update the
  value.
- **Value format mismatch (e.g. `[object Object]` in a hex field, or NaN
  channels):** the component does not match the value format. Match the
  component to the value: object pickers (`Rgb*`, `Hsl*`, `Hsv*` without
  `String`) take objects; `*StringColorPicker` and `Hex*` take strings.
- **`HexColorInput` "swallows" typed characters:** by design — it escapes
  non-hex characters and only emits valid hex via `onChange`. Enable `alpha`
  to allow 8-digit hex; enable `prefixed` to show the `#`.
- **Base styles missing under strict CSP:** the auto-injected `<style>` tag
  was blocked. Call `setNonce(hash)` before the first render (when not
  relying on Webpack's `__webpack_nonce__`).
- **Custom styles not applying:** the override selector is not specific
  enough or not scoped under a parent class. Increase specificity (e.g.
  `.your-wrapper .react-colorful__hue`) rather than editing the package.
- **Preact + TypeScript type conflicts (`@types/react` present):** add the
  `declaration.d.ts` React-namespace augmentation from the upstream README's
  Preact section; do not patch the package.
- **User actually wants a palette / color scheme, not a widget:** stop and
  hand back to the orchestrator / color-system — that is outside this skill's
  scope.
