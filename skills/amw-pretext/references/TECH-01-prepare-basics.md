---
name: TECH-01-prepare-basics
category: api
source: pretext-skills/amw-pretext-docs/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, SKILL-14.md, SKILL-15.md, SKILL-16.md, SKILL-17.md, SKILL-21.md, SKILL-23.md, pretext-text-measurement/SKILL.md, use-pretext/SKILL.md
---

# prepare() — one-time text analysis

**Category:** api
**Status:** stable

## What it does

`prepare(text, font, options?) -> PreparedText` tokenizes text, measures segments using the Canvas font engine, caches the results, and returns an opaque handle. This is the expensive phase (~19 ms / 500 texts). Call it once per unique `(text, font)` pair. It is the foundation for every `layout()` / measurement call that follows.

## When to use

- You only need height / line-count downstream (not per-line content)
- Measuring many texts up-front (virtualization, masonry)
- Any time `prepareWithSegments()` is not strictly required — `prepare()` is lighter

## How it works

Internally: Unicode segmentation via `Intl.Segmenter`, per-segment width measurement via Canvas `measureText`, glue rules for breakable boundaries. The returned `PreparedText` is opaque — do not inspect internals.

```ts
// Source: pretext-docs/SKILL.md
import { prepare, layout } from '@chenglou/pretext'
const prepared = prepare('Hello world', '16px Inter')
const { height, lineCount } = layout(prepared, 320, 20)
```

## Minimal example

```ts
// Source: pretext-skill-main/pretext/skills/amw-pretext/SKILL.md
import { prepare, layout } from '@chenglou/pretext'
const prepared = prepare('Hello world', '16px Inter')
const result = layout(prepared, 400, 24)  // { lineCount: 1, height: 24 }
```

## Configuration options (source: pretext-skill-master/SKILL.md)

The `options` parameter in `prepare()` / `prepareWithSegments()`:

| Option | Values | Default | Description |
|---|---|---|---|
| `whiteSpace` | `'normal'`, `'pre-wrap'` | `'normal'` | `'normal'`: collapses whitespace, trims edges. `'pre-wrap'`: preserves spaces, tabs (with `tab-size: 8` stops), and `\n` hard breaks. |

CSS target — pretext matches:
```css
white-space: normal; /* or pre-wrap */
word-break: normal;
overflow-wrap: break-word;
line-break: auto;
```
It does NOT support `break-all`, `keep-all`, `strict`, `loose`, or `anywhere`.

## Gotchas

- Argument order is `(text, font)` — swapping silently misbehaves.
- Font must match CSS exactly (size, weight, style, family); `'16px Inter'` and `'bold 16px Inter'` are different prepared states.
- Font must already be loaded; call `await document.fonts.ready` before measuring custom fonts.
- `prepare()` MUST NOT run in render loops — lift to module scope, `useMemo`, or setup.
- `system-ui` on macOS produces canvas/DOM drift — always use a named family.

## Cross-references

- Related: TECH-02-prepare-with-segments, TECH-03-layout, TECH-32-font-loading-sync
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
