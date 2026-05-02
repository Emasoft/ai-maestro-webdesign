---
name: TECH-33-kinetic-width-animation
category: art
source: pretext-skills/amw-pretext-art/SKILL.md
also-in: skills/amw-pretext-art/SKILL.md, SKILL-14.md, SKILL-11.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Kinetic typography (text reflows as width animates)

**Category:** art
**Status:** stable

## What it does

Animate `maxWidth` over time in `requestAnimationFrame`. `layout()` re-runs each frame but is pure arithmetic (~0.09 ms) — text visibly reflows live as the container "breathes", oscillates, or eases. This is Path A of pretext-art.

## When to use

- Hero sections with breathing width
- Scroll-scrubbed reveals where text widens as you scroll
- Demoware kinetic typography

## How it works

```ts
// Source: pretext-art/SKILL.md — Path A
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'
const prepared = prepareWithSegments(TEXT, FONT)  // once
function draw() {
  const elapsed = (performance.now() - start) / 1000
  const maxWidth = 80 + ((canvas.width - 80) / 2) * (1 + Math.sin(elapsed * 0.8))
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  const { lines } = layoutWithLines(prepared, maxWidth, LINE_HEIGHT)
  const offsetY = (canvas.height - lines.length * LINE_HEIGHT) / 2
  lines.forEach((line, i) => ctx.fillText(line.text, (canvas.width - line.width) / 2, offsetY + i * LINE_HEIGHT))
  requestAnimationFrame(draw)
}
```

## Minimal example

```ts
// Source: skills/amw-pretext-art/SKILL.md (plugin)
const maxWidth = 80 + ((canvas.width - 80) / 2) * (1 + Math.sin(elapsed * 0.8))
const { lines } = layoutWithLines(prepared, maxWidth, LINE_HEIGHT)
```

## Gotchas

- Clamp `maxWidth >= widestGraphemeWidth` or layout returns empty and the canvas goes blank.
- Never re-call `prepare()` in the loop; lift to module scope.
- HiDPI: scale canvas by `devicePixelRatio` at setup.

## Cross-references

- Related: TECH-04-layout-with-lines, TECH-48-editorial-engine
- API reference: [TECH-04-layout-with-lines](TECH-04-layout-with-lines.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
