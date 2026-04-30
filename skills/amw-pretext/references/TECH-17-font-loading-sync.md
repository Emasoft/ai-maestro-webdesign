---
name: TECH-17-font-loading-sync
category: measure
source: pretext-skills/amw-pretext-integrate/SKILL.md
also-in: SKILL-11.md, SKILL-14.md, SKILL-16.md, SKILL-21.md, SKILL-23.md, use-pretext/SKILL.md
---

# Font-loading sync point before prepare()

**Category:** measure
**Status:** stable

## What it does

`prepare()` measures using whichever font the Canvas has loaded at call time. If the custom font hasn't finished loading yet, measurements fall back to the system font and will be wrong. The canonical fix in the browser is `await document.fonts.ready` before the first `prepare()`. In Node.js, register fonts with `node-canvas`'s `registerFont` synchronously before import.

## When to use

- Every time a custom web font is the measurement target
- SSR / node-canvas pipelines
- Initial mount inside React/Svelte components — wrap `prepare()` in `onMount` / `useEffect` behind the `document.fonts.ready` promise

## How it works

```ts
// Browser — Source: pretext-integrate/SKILL.md
await document.fonts.ready
const prepared = prepare(text, '16px "My Custom Font"')

// Node — Source: pretext-integrate/SKILL.md
import { registerFont } from 'canvas'
registerFont('./fonts/Inter.ttf', { family: 'Inter' })
// prepare('...', '16px Inter') is now safe
```

## Minimal example

```ts
// Source: use-pretext/SKILL.md — Recipe 1 Masonry
onMount(() => {
  document.fonts.ready.then(() => {
    positioned = computeLayout(containerEl.clientWidth)
  })
})
```

## Gotchas

- Silent failure mode — measurements with the fallback font look plausible but are off by a few pixels per line.
- `document.fonts.ready` resolves once per page lifecycle; a font swapped in later requires `clearCache()` before the next `prepare()`.

## Cross-references

- Related: TECH-10-clear-cache, TECH-58-ssr-node-canvas
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
