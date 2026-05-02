---
name: TECH-62-ssr-node-canvas
category: integrate
source: pretext-skills/amw-pretext-integrate/SKILL.md
also-in: pretext-docs/SKILL.md, pretext-main-2 docs/cross-platform.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# SSR / Node.js integration (node-canvas shim)

**Category:** integrate
**Status:** stable

## What it does

Pretext uses `CanvasRenderingContext2D.measureText` internally. In Node.js, install `node-canvas` and register a global document.createElement shim before importing pretext. Then `prepare()` + `layout()` work identically to the browser for build-time metrics / server-rendered layouts / test suites.

## When to use

- Static-site generators computing exact layout heights
- Test suites validating text metrics
- Server-rendered pages needing pre-measured sizes

## How it works

```ts
// Source: pretext-integrate/SKILL.md — Path E
import { createCanvas, registerFont } from 'canvas'
registerFont('./fonts/Inter.ttf', { family: 'Inter' })
;(globalThis as any).document = {
  createElement: (tag) => tag === 'canvas' ? createCanvas(0, 0) : null
}
import { prepare, layout } from '@chenglou/pretext'
const prepared = prepare(text, '16px Arial')
const { height, lineCount } = layout(prepared, 320, 24)
```

## Minimal example

```bash
npm install @chenglou/pretext canvas
```

```ts
// Setup once at app startup — see How-it-works
```

## Gotchas

- Font rendering in Node differs slightly from browser — match fonts precisely with `registerFont`.
- Pretext-main-2 lists server-side support as "coming soon" (STATUS.md) — the shim works but is not officially supported; verify measurements match production.
- Some fonts have licensing constraints for server use — check before shipping.

## Cross-references

- Related: TECH-17-font-loading-sync
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
