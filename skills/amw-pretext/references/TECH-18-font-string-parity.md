---
name: TECH-18-font-string-parity
category: measure
source: pretext-skills/amw-pretext-docs/SKILL.md
also-in: SKILL-11.md, SKILL-16.md, SKILL-17.md, use-pretext/SKILL.md, pretext-art/SKILL.md
---

# Font-string parity between pretext and renderer

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** measure
**Status:** stable

## What it does

The `font` argument to `prepare()` is a **CSS font shorthand** (`style weight size/line-height family`) — same format as `CanvasRenderingContext2D.font`. It MUST match EXACTLY what the renderer (Canvas `ctx.font` or the rendered CSS) uses; any drift (missing weight, different family fallback) produces wrong measurements.

## When to use

- Every pretext project — this is non-negotiable.
- When integrating with a design-system token pipeline — derive the font string from the same token both sides consume.

## How it works

Pretext parses the font shorthand and queries Canvas for width metrics using that exact string. Canvas's font resolver can fall back silently (e.g. `system-ui` resolves differently on macOS), producing measurements that don't match the rendered glyphs.

```ts
// Correct: Source: pretext-docs/SKILL.md
const FONT = 'bold 16px "Helvetica Neue", sans-serif'
const prepared = prepare(text, FONT)
ctx.font = FONT  // byte-identical
```

## Minimal example

```ts
// Source: pretext-art/SKILL.md
const FONT = 'bold 32px sans-serif'
const prepared = prepare(TEXT, FONT)
// ... later in draw loop:
ctx.font = FONT
```

## Gotchas

- `'16px Inter'` vs `'16px Inter, sans-serif'` can differ if Inter isn't loaded.
- Pinned advice: never pass `system-ui` — on macOS Canvas resolves a different optical variant than DOM.
- CSS `line-height` in the shorthand is informational; pretext reads `lineHeight` from `layout()`'s argument.

## Cross-references

- Related: TECH-17-font-loading-sync
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
  > What it does · When to use · How it works · Minimal example · Configuration options (source: pretext-skill-master/SKILL.md) · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
