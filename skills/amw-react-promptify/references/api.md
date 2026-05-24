# react-promptify API reference

## Table of Contents

- [createPrompter()](#createprompter)
- [Prompter (component)](#prompter-component)
- [prompt(render)](#promptrender)
- [Exported TypeScript types](#exported-typescript-types)
- [The no-hooks-in-render caveat](#the-no-hooks-in-render-caveat)
- [Multiple prompters](#multiple-prompters)

The complete, verified surface of [`react-promptify`](https://github.com/AndrewPrifer/react-promptify) (MIT, v0.3.0). The exports are `createPrompter` (value) and the `CallbackFn` / `RenderFn` / `PrompterProps` types. There is **no** `usePrompt` hook and **no** context `Provider`. Never paraphrase these names from memory; if the installed version differs and behavior conflicts, defer to the installed package's own types.

## createPrompter()

The factory. Returns a fresh prompter instance — its own isolated modal stack. Create as many as you want (different prompt kinds, different host modals).

```ts
import { createPrompter } from "react-promptify";

const { Prompter, prompt } = createPrompter();
const { Prompter: AlertPrompter, prompt: alert } = createPrompter();
```

**Returns** an object with exactly two members: `Prompter` (the host component) and `prompt` (the async function).

## Prompter (component)

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

## prompt(render)

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

## Exported TypeScript types

The package root exports these types (plus the `createPrompter` value):

```ts
type CallbackFn<T> = (value: T) => void;
type RenderFn<T>   = (callback: CallbackFn<T | null>) => React.ReactElement;
// PrompterProps — props of the Prompter component (its render-function child)
```

`done` (the argument your `render` receives) has type `CallbackFn<T | null>` — so calling `done(null)` is valid and resolves the promise to `null`, the same as cancelling.

## The no-hooks-in-render caveat

Do **not** call React hooks inside the `render` function passed to `prompt()` — it causes undefined behavior ("Rendered more/fewer hooks than expected" / erratic state). This is a hard upstream caveat.

If the prompt needs state (an `<input>`, validation, etc.), extract a separate component and render `<MyPrompt done={done} />` instead, passing `done` to it as a prop. See the worked example in [examples](./examples.md).

## Multiple prompters

The render stack of one prompter shows the most-recent prompt first. For distinct, independent prompt kinds (e.g. a value prompt and an `alert`-style confirmation that need different host modals), create separate prompters with `createPrompter()` rather than reusing one — each gets its own `Prompter` mount and its own isolated stack.
