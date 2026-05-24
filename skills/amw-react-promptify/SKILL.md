---
name: amw-react-promptify
description: react-promptify reference — the tiny dependency-free window.prompt replacement for React (createPrompter, the Prompter render-host component, and the async prompt() function). Covers the createPrompter() factory, the Prompter render-prop contract ({children, open, cancel}), the prompt<T>(render => done) async pattern that resolves to a typed value or null on cancel, custom-modal integration, multiple prompters, the CallbackFn/RenderFn/PrompterProps types, and the no-hooks-in-render caveat. Triggers on "react-promptify", "custom prompt modal", "window.prompt replacement", "async prompt dialog returning a value", "promise-based modal", "createPrompter", "prompt() returning a value". Does NOT trigger on generic "add a modal", "make a form", "open a dialog", or design-intent modal work — those belong to the orchestrator and shadcn-ui. Use when wiring an async, value-returning prompt/dialog into a React UI. Trigger with "react-promptify" or "prompt modal".
version: 0.1.0
---

# react-promptify Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Reference for [`react-promptify`](https://github.com/AndrewPrifer/react-promptify) (MIT, v0.3.0) — a tiny (~0.5 KB gzipped), dependency-free, platform-agnostic `window.prompt` replacement for React. It lets you define **once** where and how prompts render, then call an async `prompt()` function **anywhere** in the app to open a custom modal and get a typed value back exactly where you need it — the modal open/close state is managed for you.

This skill documents the real exported API — the `createPrompter()` factory, the `Prompter` render-host component and its `{children, open, cancel}` render-prop contract, the `prompt<T>(render)` async function that resolves to `T | null`, the `done` callback wiring, and the `CallbackFn` / `RenderFn` / `PrompterProps` TypeScript types — so an agent can wire it correctly **offline** without re-reading the upstream source. It is API reference only; it does not bundle the library source and does not emit React/JSX artifacts itself.

This is distinct from generic modal/dialog work: [shadcn-ui](../amw-shadcn-ui/SKILL.md) owns the *visual* modal/dialog components and accessibility chrome; react-promptify owns the *async value-returning request/response control flow* that drives any modal you bring. The two compose — a shadcn `Dialog` is a natural "bring your own modal" target inside `Prompter`.

## Instructions

1. Confirm the request is about an **async, value-returning** prompt — "ask the user, wait, get the answer right here" — not about rendering a static modal or a multi-field form with its own persistent state. If it is plain modal markup or design intent, hand back to the orchestrator / [shadcn-ui](../amw-shadcn-ui/SKILL.md).
2. Create a prompter instance once, at module scope: `const { Prompter, prompt } = createPrompter();`. Create additional prompters (e.g. an `alert`-style one) only when different prompt kinds need different host modals.
3. Mount `<Prompter>` once, where the modal should appear, with a **render function** child: `{({ children, open, cancel }) => <YourModal open={open} onClose={cancel}>{children}</YourModal>}`. The `children` it hands you is the active prompt's content; `open` is `true` while a prompt is pending; `cancel` closes the modal and resolves the pending promise with `null`.
4. Call `prompt()` from anywhere — typically inside an `async` handler — passing a render function `(done) => <JSX/>`. Call `done(value)` from inside that JSX to resolve. `await` the call to receive the value.
5. Type the result: `prompt<T>(...)` resolves to `Promise<T | null>` — `T` when `done(value)` was called, `null` when the user cancelled. Always handle the `null` branch (`?? fallback`).
6. Do **not** call React hooks inside the `render` function passed to `prompt()` — it causes undefined behavior. If the prompt needs state (an `<input>`, validation, etc.), extract a separate component and render `<MyPrompt done={done} />` instead.
7. Wrap the body of the host modal so it returns `null` (or the modal stays closed) when `open` is `false`, OR pass `open` straight to a modal that handles its own visibility.

See the [worked example](#worked-example) below.

## API

### `createPrompter()`

The factory. Returns a fresh prompter instance — its own isolated modal stack. Create as many as you want (different prompt kinds, different host modals).

```ts
import { createPrompter } from "react-promptify";

const { Prompter, prompt } = createPrompter();
const { Prompter: AlertPrompter, prompt: alert } = createPrompter();
```

**Returns** an object with exactly two members: `Prompter` (the host component) and `prompt` (the async function).

### `Prompter` (component)

The render-host. Place it once where prompts should appear. Its single child is a **render function** (not normal children).

| Render-fn arg | Type            | Description                                                                 |
| ------------- | --------------- | --------------------------------------------------------------------------- |
| `children`    | `ReactNode`     | The active prompt's content to render inside your modal (undefined when idle). |
| `open`        | `boolean`       | `true` while a prompt is pending, `false` when none is active.               |
| `cancel`      | `() => void`    | Closes the modal and resolves the pending promise with `null`.              |

```tsx
<Prompter>
  {({ children, open, cancel }) => (
    <SomeModal open={open} onClose={cancel}>
      {children}
    </SomeModal>
  )}
</Prompter>
```

`PrompterProps` types the component: its `children` prop is the `({ children, open, cancel }) => ReactNode` render function.

### `prompt(render)`

The async request. Works like `window.prompt`, except it is asynchronous and you render whatever you want.

| Param    | Type                                          | Description                                                                                  |
| -------- | --------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `render` | `(done: CallbackFn<T \| null>) => ReactElement` | A function that returns the prompt content. Call `done(value)` inside it to resolve the promise. |

**Returns** `Promise<T | null>` — resolves to the value `done` was called with, or `null` if the prompt was cancelled (via `cancel` from the host, or `done(null)`).

```tsx
const answer = await prompt<string>((done) => (
  <div>
    <button onClick={() => done("yes")}>Yes</button>
    <button onClick={() => done("no")}>No</button>
  </div>
));
// answer: "yes" | "no" | null
```

### Exported TypeScript types

The package root exports these types (plus the `createPrompter` value):

```ts
type CallbackFn<T> = (value: T) => void;
type RenderFn<T>   = (callback: CallbackFn<T | null>) => React.ReactElement;
// PrompterProps — props of the Prompter component (its render-function child)
```

`done` (the argument your `render` receives) has type `CallbackFn<T | null>` — so calling `done(null)` is valid and resolves the promise to `null`, the same as cancelling.

## Worked example

A custom modal host plus a stateful prompt extracted into its own component (the correct pattern when the prompt needs hooks):

```tsx
import { useState } from "react";
import { createPrompter, CallbackFn } from "react-promptify";

const { Prompter, prompt } = createPrompter();

// Define ONCE where/how prompts render.
function App() {
  return (
    <>
      <Prompter>
        {({ children, open, cancel }) =>
          open ? (
            <div className="modal-backdrop">
              <div className="modal">
                {children}
                <button onClick={cancel}>Cancel</button>
              </div>
            </div>
          ) : null
        }
      </Prompter>
      <Settings />
    </>
  );
}

// Hooks are NOT allowed inside the prompt() render fn — extract a component.
function NameForm({ done }: { done: CallbackFn<string | null> }) {
  const [value, setValue] = useState("");
  return (
    <form onSubmit={(e) => { e.preventDefault(); done(value); }}>
      <input value={value} onChange={(e) => setValue(e.target.value)} autoFocus />
      <button type="submit">Submit</button>
    </form>
  );
}

// Call prompt() anywhere, get the value RIGHT here.
function Settings() {
  const [name, setName] = useState("");
  async function edit() {
    const result = await prompt<string>((done) => <NameForm done={done} />);
    setName(result ?? name); // handle the cancel (null) branch
  }
  return (
    <div>
      <p>Name: {name}</p>
      <button onClick={edit}>Edit name</button>
    </div>
  );
}
```

For a confirm-style prompt with no state, inline the render function directly (no extracted component needed) and call `done(true)` / `done(false)`.

## Output

This skill produces no standalone artifacts — it provides `react-promptify` API answers and JSX snippets. Any HTML/React UI that embeds a prompter is assembled by `amw-wireframe-builder-agent` (with [shadcn-ui](../amw-shadcn-ui/SKILL.md) / [tailwind-4](../amw-tailwind-4/SKILL.md) for the modal chrome and surrounding layout).

## Trigger conditions

Invoke this skill when the request is specifically about the `react-promptify` async-prompt control flow:

- replacing `window.prompt` / `window.confirm` with a custom React modal that returns a value
- wiring an `await prompt(...)` call that resolves where the data is needed
- the `createPrompter()` factory and what it returns (`Prompter`, `prompt`)
- the `Prompter` render-prop contract (`children` / `open` / `cancel`)
- typing the resolved value (`prompt<T>` → `T | null`) and handling the `null` (cancel) branch
- bringing your own modal (e.g. a shadcn `Dialog`) as the host
- the "no hooks inside the render function — extract a component" caveat
- using multiple independent prompters

Do NOT invoke this skill for generic "add a modal", "open a dialog", "make a form", modal styling/animation, or design-intent modal decisions — those belong to the orchestrator or to [shadcn-ui](../amw-shadcn-ui/SKILL.md). This skill is about the async value-returning *flow*, not the modal's appearance.

## Prerequisites

- **Peer dependency (user responsibility):** `react` (declared as `react: "*"`; hooks-era React 16.8+ in practice, since the store uses `useState`/`useEffect`). The host project must already use React — this is a component/utility, not a standalone tool. Note `react-dom` is needed by the host app to render, though the package itself declares only `react` as a peer.
- **Install:** `npm install react-promptify` (zero runtime dependencies; ships its own TypeScript types).
- No build step, no CSS import, and no runtime binaries are required by this skill — it is pure documentation. You bring your own modal markup/styles for the `Prompter` host.

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during **Phase B** when an approved design includes an async value-returning prompt/confirm flow, or pulled in by `amw-wireframe-builder-agent` while assembling React UI. Callable directly on `react-promptify` API questions. The skill's techniques are NOT limited to what any command exposes.

## Position in flow

REFERENCE. Loaded when the orchestrator (or a producer sub-agent) needs authoritative `react-promptify` API guidance to embed a working async prompt into a React target.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — the orchestrator; decides whether an async prompt flow belongs in the design at all and routes here.
- [SKILL](../amw-shadcn-ui/SKILL.md) — the visual modal/dialog components (`Dialog`, `AlertDialog`) and their accessibility chrome. A shadcn `Dialog` is a natural "bring your own modal" host inside `Prompter`; this skill drives the async value flow, shadcn renders the box.
- [SKILL](../amw-tailwind-4/SKILL.md) — for utility-class styling of the modal host and backdrop you supply to `Prompter`.
- Upstream: `https://github.com/AndrewPrifer/react-promptify` (MIT). This skill reflects v0.3.0.

## Non-negotiables

- Does NOT own broad design intent or modal *appearance*. The orchestrator ([SKILL](../amw-design-principles/SKILL.md)) decides whether an async prompt is the right surface; [shadcn-ui](../amw-shadcn-ui/SKILL.md) decides how the modal looks. This skill only answers `react-promptify` flow questions.
- `Prompter`'s child is a **render function**, not normal JSX children. Always destructure `{ children, open, cancel }` and return your modal from it — passing static children breaks the host.
- Never call React hooks inside the `render` function passed to `prompt()`. Extract a component and pass `done` to it as a prop. This is a hard upstream caveat — violating it causes undefined behavior.
- `prompt<T>()` resolves to `T | null`. Always handle the `null` (cancel) branch; never assume a value came back.
- Wire `cancel` to the modal's own dismiss affordance (backdrop click / Escape / Close button) so dismissing the modal resolves the promise with `null` rather than leaving it pending forever.
- Never paraphrase the export names, render-prop shape, or return type from memory — they are fixed by the upstream API documented here (v0.3.0): the exports are `createPrompter` (value) and `CallbackFn` / `RenderFn` / `PrompterProps` (types). There is no `usePrompt` hook and no context `Provider`. If the installed version differs and behavior conflicts, defer to the installed package's own types.
- English-only content across the skill. No third-language characters in any file.

## Error Handling

- **Prompt never opens (`open` stays `false`):** the `Prompter` host is not mounted, or its render function never renders the modal when `open` is `true`. Mount exactly one `Prompter` for that prompter instance and ensure the render function shows the modal on `open`.
- **`children` is empty inside the modal:** the host is returning static children instead of using the render-prop arg. Use `{({ children }) => <Modal>{children}</Modal>}`, not `<Prompter><Modal/></Prompter>`.
- **`await prompt(...)` hangs forever:** neither `done()` was called nor was the prompt cancelled. Provide a dismiss path wired to `cancel` (resolves to `null`) and a `done(value)` call inside the rendered content.
- **"Rendered more/fewer hooks than expected" / erratic state:** a hook was called inside the `prompt()` render function. Extract the stateful UI into its own component and render `<MyPrompt done={done} />`.
- **Result is `null` unexpectedly:** the user cancelled (via `cancel`) or `done(null)` was called. This is the documented cancel signal — handle it (`result ?? fallback`), it is not an error.
- **Two prompts collide / second overwrites first:** the render stack shows the most-recent prompt first; for distinct, independent prompt kinds create separate prompters with `createPrompter()` rather than reusing one.
- **TypeScript: `done` rejects `null`:** type the callback as `CallbackFn<T | null>` (the `done` argument is `CallbackFn<T | null>`), or type the prompt as `prompt<T>` and let the return be `T | null`.
- **User actually wants a styled modal/dialog, not an async value flow:** stop and hand back to the orchestrator / [shadcn-ui](../amw-shadcn-ui/SKILL.md) — modal appearance is outside this skill's scope.
