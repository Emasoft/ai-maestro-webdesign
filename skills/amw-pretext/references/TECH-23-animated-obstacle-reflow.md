---
name: TECH-23-animated-obstacle-reflow
category: layout
source: pretext-skills/SKILL-11.md
also-in: pretext-skill-main/patterns.md (Text Around Obstacles — Animated)
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# 60 fps text reflow around animated obstacles

**Category:** layout
**Status:** stable

## What it does

Re-run the obstacle-routed layout every frame as an obstacle (draggable orb, moving creature, scroll-scrubbed element) moves. Because `layout()` / `layoutNextLine()` are pure arithmetic (~0.09 ms for 500 texts), full-page reflow is safe at 60 fps.

## When to use

- Interactive editorial demos (dragging an element, text parts)
- Scroll-scrubbed obstacle-aware reveals
- Creature-following / cursor-following reflow effects

## How it works

```ts
// Concept — Source: SKILL-11.md / pretext-skill-main/patterns.md
function animate() {
  obstaclePos = nextObstaclePos()
  const lines = computeObstacleRoutedLines(prepared, obstaclePos)
  syncDOMLinePool(lines)  // element pooling avoids create/destroy churn
  requestAnimationFrame(animate)
}
```

## Minimal example

```ts
// Concept only — positions updated each frame
while (cursor) {
  const w = getFreeWidthAt(y, obstaclePos)
  const line = layoutNextLine(prepared, cursor, w)
  if (!line) break
  positionLineAt(line, y)
  cursor = line.end
  y += LINE_HEIGHT
}
```

## Gotchas

- DO NOT create / destroy DOM nodes per frame — pool them (`syncPool` pattern from SKILL-11 anti-patterns).
- Do NOT re-call `prepare()` in the animation loop — cache it.
- Clamp `MIN_SLOT_WIDTH` (~50 px) so narrow slivers don't wreck the layout.
- `setInterval` is forbidden here — use `requestAnimationFrame`.

## Cross-references

- Related: TECH-20-polygon-obstacle-mask, TECH-44-editorial-engine, TECH-54-dragon-text-reflow
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
