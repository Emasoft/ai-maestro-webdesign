---
name: TECH-10-clear-cache
category: api
source: pretext-skills/amw-pretext-docs/SKILL.md
also-in: SKILL-11.md, use-pretext/SKILL.md
---

# clearCache() — release global measurement cache

**Category:** api
**Status:** stable

## What it does

`clearCache()` clears pretext's global Canvas-measurement cache shared across all calls. Only needed when fonts change at runtime (e.g. a custom font is swapped in after initial load) or when you want to free memory after heavy font churn.

## When to use

- A web font finishes loading AFTER some `prepare()` calls already ran (measurements would be stale)
- You cycle through many fonts and want to release memory
- A library like SSR / node-canvas re-registers fonts

## How it works

Drops the internal font/segment cache map. Subsequent `prepare()` calls re-measure from scratch.

```ts
// Source: pretext-docs/SKILL.md
import { clearCache } from '@chenglou/pretext'
document.fonts.ready.then(() => {
  clearCache()  // drop fallback-font measurements now that real font is loaded
  // now safely call prepare() again
})
```

## Minimal example

```ts
// Source: use-pretext/SKILL.md
clearCache()  // free caches; next prepare() is cold again
```

## Gotchas

- Do NOT call in hot paths — every subsequent `prepare()` pays the measurement cost again.
- Cache is process-global; affects every prepared handle's future invalidation behavior.

## Cross-references

- Related: TECH-01-prepare-basics, TECH-32-font-loading-sync
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
