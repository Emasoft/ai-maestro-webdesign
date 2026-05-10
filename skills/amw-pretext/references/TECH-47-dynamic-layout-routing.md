---
name: TECH-47-dynamic-layout-routing
category: motion
source: pretext-skills/amw-pretext-frontend-motion-main/core/bundle/references/demo-family-map.md
also-in: SKILL-15.md (dynamic-layout.ts demo), pretext-main-2 demos
---

# Dynamic layout — fixed-height editorial spread with routed text

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** motion
**Status:** stable

## What it does

A fixed-height editorial composition with obstacle-routed text spanning multiple columns. Builds on TECH-20 (polygon obstacle), TECH-21 (multi-column handoff), and TECH-22 (floated image). The "Dynamic Layout" family in pretext-frontend-motion is exactly this spread — it proves pretext can hold a complex editorial page at 60 fps.

## When to use

- Magazine / editorial demo pages
- Reading apps with illustrations
- Pretext showcase pages

## How it works

```ts
// Source: SKILL-15.md dynamic-layout.ts demo
const prepared = prepareWithSegments(article, font)
let cursor = { segmentIndex: 0, graphemeIndex: 0 }
for (const band of lineBands) {
  const slots = carveLineSlots(band.y, obstacles, band.columns)  // TECH-24
  for (const slot of slots) {
    const line = layoutNextLine(prepared, cursor, slot.width)
    if (!line) break
    renderLine(line, slot.x, band.y)
    cursor = line.end
  }
}
```

## Minimal example

See SKILL-15 `demos/dynamic-layout.ts` and `wrap-geometry.ts` for working code.

## Gotchas

- Spread height must be FIXED — dynamic content requires a rolling recomputation.
- Pair with `text-wrap: balance` for headlines as progressive enhancement.

## Cross-references

- Related: TECH-20-polygon-obstacle-mask, TECH-21-multi-column-handoff, TECH-24-carve-text-line-slots, TECH-48-editorial-engine
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
