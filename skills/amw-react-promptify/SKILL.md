---
name: amw-react-promptify
description: react-promptify reference — the dependency-free window.prompt replacement for React (createPrompter factory, the Prompter render-host, the async prompt() resolving to a typed value or null on cancel). Triggers on "react-promptify", "custom prompt modal", "window.prompt replacement", "createPrompter", "promise-based modal returning a value". Does NOT trigger on generic "add a modal", "open a dialog", or "make a form". Use when wiring a react-promptify async value-returning prompt flow.
version: 0.1.0
---

# react-promptify Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor-reference under the design-principles rules. It does not own broad design intent.

## Overview

Reference for [`react-promptify`](https://github.com/AndrewPrifer/react-promptify) (MIT, v0.3.0) — a tiny (~0.5 KB gzipped), dependency-free `window.prompt` replacement for React. Define **once** where prompts render, then call an async `prompt()` **anywhere** to open a custom modal and get a typed value back where you need it; open/close state is managed for you.

This skill documents the real exported API so an agent can wire it **offline**: the `createPrompter()` factory, the `Prompter` render-host with its `{children, open, cancel}` render-prop contract, the `prompt<T>(render)` async function resolving to `T | null`, and the `CallbackFn` / `RenderFn` / `PrompterProps` types. API reference only — bundles no source, emits no React/JSX. It is distinct from generic modal work: [shadcn-ui](../amw-shadcn-ui/SKILL.md) owns the *visual* modal; react-promptify owns the *async value-returning flow*. They compose — a shadcn `Dialog` is a natural host inside `Prompter`.

## Instructions

1. Confirm the request is about an **async, value-returning** prompt ("ask, wait, get the answer here"), not static markup or design intent. If it is appearance, hand back to the orchestrator / [shadcn-ui](../amw-shadcn-ui/SKILL.md).
2. Create a prompter once at module scope: `const { Prompter, prompt } = createPrompter();`. Add more only when different prompt kinds need different host modals.
3. Mount `<Prompter>` once where the modal appears, with a **render-function** child: `{({ children, open, cancel }) => <YourModal open={open} onClose={cancel}>{children}</YourModal>}`. `children` is the active prompt's content; `open` is `true` while pending; `cancel` closes and resolves the promise with `null`.
4. Call `prompt()` from anywhere (typically an `async` handler) passing `(done) => <JSX/>`. Call `done(value)` inside that JSX to resolve; `await` the call to receive the value.
5. `prompt<T>(...)` resolves to `Promise<T | null>` — `T` on `done(value)`, `null` on cancel. Always handle the `null` branch (`?? fallback`).
6. Do **not** call React hooks inside the `render` function passed to `prompt()` (undefined behavior). If state is needed, extract a component and render `<MyPrompt done={done} />`.
7. Make the host modal return `null` when `open` is `false`, OR pass `open` to a modal that handles its own visibility.

Full API, worked code, and failure modes are in the reference files below — read them before answering detailed questions.

## Reference index

This skill owns three reference files. Each link below is followed by that file's complete table of contents.

- [api](references/api.md) — full API surface: factory, component, `prompt()`, types, caveats.
  - [createPrompter()](references/api.md#createprompter)
  - [Prompter (component)](references/api.md#prompter-component)
  - [prompt(render)](references/api.md#promptrender)
> [api.md] createPrompter() · Prompter (component) · prompt(render) · Exported TypeScript types · The no-hooks-in-render caveat · Multiple prompters
  - [Exported TypeScript types](references/api.md#exported-typescript-types)
> [api.md] createPrompter() · Prompter (component) · prompt(render) · Exported TypeScript types · The no-hooks-in-render caveat · Multiple prompters
  - [The no-hooks-in-render caveat](references/api.md#the-no-hooks-in-render-caveat)
> [api.md] createPrompter() · Prompter (component) · prompt(render) · Exported TypeScript types · The no-hooks-in-render caveat · Multiple prompters
  - [Multiple prompters](references/api.md#multiple-prompters)
> [api.md] createPrompter() · Prompter (component) · prompt(render) · Exported TypeScript types · The no-hooks-in-render caveat · Multiple prompters
- [examples](references/examples.md) — worked code (custom host, confirm, shadcn host).
  - [Stateful prompt with a custom modal host](references/examples.md#stateful-prompt-with-a-custom-modal-host)
  - [Stateless confirm-style prompt](references/examples.md#stateless-confirm-style-prompt)
  - [Bring-your-own-modal (shadcn Dialog) host](references/examples.md#bring-your-own-modal-shadcn-dialog-host)
- [troubleshooting](references/troubleshooting.md) — failure modes + non-negotiables.
  - [Common failure modes](references/troubleshooting.md#common-failure-modes)
  - [Non-negotiables](references/troubleshooting.md#non-negotiables)
> [troubleshooting.md] Common failure modes · Non-negotiables

## Trigger conditions

Invoke for the `react-promptify` async-prompt control flow specifically: replacing `window.prompt`/`window.confirm` with a value-returning custom React modal; wiring `await prompt(...)`; the `createPrompter()` factory and what it returns; the `Prompter` render-prop contract (`children`/`open`/`cancel`); typing `prompt<T>` → `T | null` and handling cancel; bringing your own modal (e.g. a shadcn `Dialog`) as host; the no-hooks-in-render caveat; multiple prompters.

Do NOT invoke for generic "add a modal", "open a dialog", "make a form", modal styling/animation, or design-intent decisions — those belong to the orchestrator or to [shadcn-ui](../amw-shadcn-ui/SKILL.md). This skill is about the async value-returning *flow*, not appearance.

## Prerequisites

- **Peer dependency (user responsibility):** `react` (declared `react: "*"`; hooks-era 16.8+ in practice). The host app must already use React; `react-dom` is needed to render, though the package declares only `react` as a peer.
- **Install:** `npm install react-promptify` (zero runtime deps; ships TypeScript types).
- No build step, CSS import, or runtime binaries — pure documentation. You bring your own modal markup/styles for the `Prompter` host.

## Activation / Position

No dedicated slash command. Invoked by the `design-principles` orchestrator during **Phase B** when an approved design needs an async value-returning prompt/confirm flow, or pulled in by `amw-wireframe-builder-agent` while assembling React UI; also callable directly on API questions. REFERENCE in the flow. Techniques are NOT limited to what any command exposes.

## Examples

Worked code — a stateful custom-modal host, a stateless confirm-style prompt, and a bring-your-own shadcn `Dialog` host — lives in [examples](references/examples.md), linked with its full TOC in the [Reference index](#reference-index) above.
> [examples.md] Stateful prompt with a custom modal host · Stateless confirm-style prompt · Bring-your-own-modal (shadcn Dialog) host

## Output

This skill produces no standalone artifacts — only `react-promptify` API answers and JSX snippets. Any UI that hosts a prompter is assembled by `amw-wireframe-builder-agent` (with [shadcn-ui](../amw-shadcn-ui/SKILL.md) / [tailwind-4](../amw-tailwind-4/SKILL.md) for the surrounding chrome).

## Error Handling

Failure modes and fixes live in the troubleshooting reference linked in the [Reference index](#reference-index) above (prompt never opens, empty `children`, hung `await`, hook-in-render errors, unexpected `null`, colliding prompts, TypeScript `null` rejection, wrong-tool handback).

## Resources

This skill's own reference files (api, examples, troubleshooting) are linked with their complete TOCs in the [Reference index](#reference-index) above. Cross-skill resources:

| Resource | Role |
|---|---|
| [SKILL](../amw-design-principles/SKILL.md) | Orchestrator — decides whether an async prompt flow belongs in the design and routes here |
| [SKILL](../amw-shadcn-ui/SKILL.md) | Visual modal/dialog components (`Dialog`, `AlertDialog`) + a11y chrome; a natural host inside `Prompter` |
| [SKILL](../amw-tailwind-4/SKILL.md) | Utility-class styling of the modal host and backdrop you supply to `Prompter` |

## Non-negotiables

The hard rules — full list (with cancel-wiring and TypeScript detail) in the troubleshooting reference's Non-negotiables section, linked in the [Reference index](#reference-index) above:

- Does NOT own broad design intent or modal *appearance* — the orchestrator decides whether an async prompt is the right surface; [shadcn-ui](../amw-shadcn-ui/SKILL.md) decides how it looks.
- `Prompter`'s child is a **render function**, not normal JSX children. Always destructure `{ children, open, cancel }` and return your modal from it.
- Never call React hooks inside the `render` function passed to `prompt()` (undefined behavior). Extract a component and pass `done` as a prop.
- `prompt<T>()` resolves to `T | null`. Always handle the `null` (cancel) branch, and wire `cancel` to the modal's dismiss affordance.
- Never paraphrase the export names from memory — exports are `createPrompter` (value) and `CallbackFn` / `RenderFn` / `PrompterProps` (types). There is **no** `usePrompt` hook and **no** context `Provider`. If the installed version differs, defer to its own types.
- English-only content. No third-language characters in any file.
