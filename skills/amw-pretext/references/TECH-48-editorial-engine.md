---
name: TECH-48-editorial-engine
category: motion
source: pretext-skills/amw-pretext-frontend-motion-main/core/bundle/references/demo-family-map.md
also-in: SKILL-15.md (editorial-engine.ts), pretext-skill-main/patterns.md, pretext-typography-skill-main/references/patterns.md
---

# Editorial engine (live multi-column reflow around animated geometry)

**Category:** motion
**Status:** stable

## What it does

The most complex demo family — a full-page multi-column editorial layout where ALL obstacles (pull quotes, images, draggable orbs) can move at 60 fps and text continuously reflows. Aggregates TECH-20, TECH-21, TECH-23, TECH-24, TECH-47.

## When to use

- Portfolio / showcase pieces
- Design agency hero demos
- Any "wow" text-reflow interactive

## How it works

```ts
// Source: pretext-frontend-motion-main demo-family-map + SKILL-15 editorial-engine.ts
// requestAnimationFrame loop:
// 1. Advance obstacle positions (physics, cursor, scroll)
// 2. Recompute per-band free slots (carveTextLineSlots)
// 3. layoutNextLine across all slots with shared cursor
// 4. Sync DOM element pool to line positions (no create/destroy)
```

## Minimal example

See SKILL-15 `demos/editorial-engine.ts` — the full working demo is too long to quote inline (~300 LOC).

## Gotchas

- Element pooling is mandatory — see SKILL-11 anti-patterns (`syncPool`).
- Do NOT reintroduce `getBoundingClientRect` for any measurement — defeats the performance gain.
- `prefers-reduced-motion` should disable the animation and fall back to a static layout.

## Cross-references

- Related: TECH-20-polygon-obstacle-mask, TECH-23-animated-obstacle-reflow, TECH-24-carve-text-line-slots, TECH-47-dynamic-layout-routing
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
