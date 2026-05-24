# react-promptify troubleshooting

## Table of Contents

- [Common failure modes](#common-failure-modes)
- [Non-negotiables](#non-negotiables)

## Common failure modes

- **Prompt never opens (`open` stays `false`):** the `Prompter` host is not mounted, or its render function never renders the modal when `open` is `true`. Mount exactly one `Prompter` for that prompter instance and ensure the render function shows the modal on `open`.
- **`children` is empty inside the modal:** the host is returning static children instead of using the render-prop arg. Use `{({ children }) => <Modal>{children}</Modal>}`, not `<Prompter><Modal/></Prompter>`.
- **`await prompt(...)` hangs forever:** neither `done()` was called nor was the prompt cancelled. Provide a dismiss path wired to `cancel` (resolves to `null`) and a `done(value)` call inside the rendered content.
- **"Rendered more/fewer hooks than expected" / erratic state:** a hook was called inside the `prompt()` render function. Extract the stateful UI into its own component and render `<MyPrompt done={done} />`.
- **Result is `null` unexpectedly:** the user cancelled (via `cancel`) or `done(null)` was called. This is the documented cancel signal — handle it (`result ?? fallback`), it is not an error.
- **Two prompts collide / second overwrites first:** the render stack shows the most-recent prompt first; for distinct, independent prompt kinds create separate prompters with `createPrompter()` rather than reusing one.
- **TypeScript: `done` rejects `null`:** type the callback as `CallbackFn<T | null>` (the `done` argument is `CallbackFn<T | null>`), or type the prompt as `prompt<T>` and let the return be `T | null`.
- **User actually wants a styled modal/dialog, not an async value flow:** stop and hand back to the orchestrator / [shadcn-ui](../../amw-shadcn-ui/SKILL.md) — modal appearance is outside this skill's scope.

## Non-negotiables

- Does NOT own broad design intent or modal *appearance*. The orchestrator ([design-principles](../../amw-design-principles/SKILL.md)) decides whether an async prompt is the right surface; [shadcn-ui](../../amw-shadcn-ui/SKILL.md) decides how the modal looks. This skill only answers `react-promptify` flow questions.
- `Prompter`'s child is a **render function**, not normal JSX children. Always destructure `{ children, open, cancel }` and return your modal from it — passing static children breaks the host.
- Never call React hooks inside the `render` function passed to `prompt()`. Extract a component and pass `done` to it as a prop. This is a hard upstream caveat — violating it causes undefined behavior.
- `prompt<T>()` resolves to `T | null`. Always handle the `null` (cancel) branch; never assume a value came back.
- Wire `cancel` to the modal's own dismiss affordance (backdrop click / Escape / Close button) so dismissing the modal resolves the promise with `null` rather than leaving it pending forever.
- Never paraphrase the export names, render-prop shape, or return type from memory — they are fixed by the upstream API (v0.3.0): the exports are `createPrompter` (value) and `CallbackFn` / `RenderFn` / `PrompterProps` (types). There is no `usePrompt` hook and no context `Provider`. If the installed version differs and behavior conflicts, defer to the installed package's own types.
- English-only content across the skill. No third-language characters in any file.
