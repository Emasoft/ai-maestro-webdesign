---
name: TECH-36-generative-poster-grid
category: art
source: pretext-skills/amw-pretext-art/SKILL.md
also-in: skills/amw-pretext-art/SKILL.md, SKILL-14.md
---

# Generative poster / text-block grid

**Category:** art
**Status:** stable

## What it does

Compose multiple text blocks (each with its own font, line height, width) into a grid or editorial layout. Batch `prepareWithSegments()` for all cells up front, then render each cell at its computed position with independent typography.

## When to use

- Typographic posters
- Editorial "spread" mockups
- Social-share cards with mixed font blocks

## How it works

```ts
// Source: pretext-art/SKILL.md — Path E
const CELLS = [
  { text: 'LARGE\nHEADLINE', font: 'bold 48px sans-serif', lineHeight: 52 },
  { text: 'A secondary thought in smaller type.', font: '18px serif', lineHeight: 26 },
  { text: 'Caption text.', font: '12px monospace', lineHeight: 18 },
]
const prepared = CELLS.map(c => prepareWithSegments(c.text, c.font))
let y = PADDING
CELLS.forEach((cell, i) => {
  const { lines } = layoutWithLines(prepared[i], colWidth - PADDING * 2, cell.lineHeight)
  ctx.font = cell.font
  lines.forEach((line, j) => ctx.fillText(line.text, PADDING, y + j * cell.lineHeight))
  y += lines.length * cell.lineHeight + PADDING
})
```

## Minimal example

```ts
// Source: skills/amw-pretext-art/SKILL.md (plugin)
// Same pattern — batch prepare, iterate, render
```

## Gotchas

- Mixed baselines across fonts require careful `y` bookkeeping — pretext gives you line heights but not cap/x-height.
- For symmetric grids, compute the total height in a first pass and center vertically.

## Cross-references

- Related: TECH-04-layout-with-lines, TECH-66-masonry-grid
- API reference: [TECH-04-layout-with-lines](TECH-04-layout-with-lines.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
