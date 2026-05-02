---
name: TECH-24-carve-text-line-slots
category: layout
source: pretext-skills/SKILL-11.md
also-in: pretext-frontend-motion-main
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# carveTextLineSlots — fill both sides of a mid-line obstacle

**Category:** layout
**Status:** stable

## What it does

When an obstacle sits in the MIDDLE of a line band (not hugging an edge), text can flow on BOTH sides of it. `carveTextLineSlots` is the SKILL-11 pattern that, for each line band, subtracts the obstacle's horizontal interval from the full line, yielding two sub-slots (left + right). Each slot is laid out with its own `layoutNextLine()` call, using a shared cursor.

## When to use

- Obstacles near the horizontal center of the text column
- Multi-obstacle layouts where several cutouts per line are possible
- Editorial engines with draggable centered illustrations

## How it works

```ts
// Concept — Source: SKILL-11.md
function carveLineSlots(lineY, obstacles, fullWidth) {
  const blocked = obstacles.filter(o => o.topY <= lineY && lineY <= o.bottomY)
  let slots = [{ x: 0, w: fullWidth }]
  for (const o of blocked) {
    slots = slots.flatMap(s => splitSlot(s, o.leftX, o.rightX, hPad))
  }
  return slots.filter(s => s.w >= MIN_SLOT_WIDTH)
}
// Then: layoutNextLine once per slot, advancing the shared cursor
```

## Minimal example

```ts
// Per line band
const slots = carveLineSlots(y, obstacles, fullW)
for (const slot of slots) {
  const line = layoutNextLine(prepared, cursor, slot.w)
  if (!line) return
  ctx.fillText(line.text, slot.x, y)
  cursor = line.end
}
```

## Gotchas

- Forgetting to share the cursor across slots duplicates text.
- `hPad` (8-20 px) around each obstacle prevents text kissing the edge.
- `MIN_SLOT_WIDTH` must exceed the widest single word (including grapheme-level breakable clusters).

## Cross-references

- Related: TECH-23-animated-obstacle-reflow, TECH-20-polygon-obstacle-mask
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
