---
name: TECH-37-typographic-ascii
category: art
source: pretext-skills/SKILL-11.md
also-in: pretext-frontend-motion-main (Variable Typographic ASCII), pretext-skill-main/patterns.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Typographic ASCII art (proportional-width characters)

**Category:** art
**Status:** stable

## What it does

Render fluid simulations / particle systems / 3D wireframes as grids of ASCII characters using their PROPORTIONAL widths (measured by pretext) instead of monospace placement. The visual result looks like traditional ASCII art but characters align because each cell knows its exact Canvas width.

## When to use

- Fluid smoke demos
- Particle systems rendered as glyphs
- Retro terminal aesthetics on a proportional font

## How it works

```js
// Source: SKILL-11.md and pretext-skill-main/patterns.md
const chars = ' .:-=+*#%@'
// Pre-measure each character's width via prepareWithSegments on single char
const charWidths = Object.fromEntries(chars.split('').map(c => [c, measureNaturalWidth(prepareWithSegments(c, FONT))]))

function renderFrame(densityGrid) {
  for (let row = 0; row < rows; row++) {
    let x = 0
    for (let col = 0; col < cols; col++) {
      const density = densityGrid[row][col]
      const char = chars[Math.floor(density * (chars.length - 1))]
      ctx.fillText(char, x, row * lineHeight)
      x += charWidths[char]
    }
  }
}
```

## Minimal example

```js
// See How-it-works above
```

## Gotchas

- Serif fonts (Georgia, Palatino) look better for this — source advice from SKILL-11 defaults.
- Use inline CSS classes `.a1`–`.a10` for opacity levels if rendering via DOM; directly use `globalAlpha` in Canvas.
- Never pure black `#000` background — SKILL-11 recommends off-blacks like `#08080e`.

## Cross-references

- Related: TECH-08-measure-natural-width, TECH-55-variable-ascii-canvas
- API reference: [TECH-02-prepare-with-segments](TECH-02-prepare-with-segments.md)
  > What it does · When to use · How it works · Minimal example · TypeScript types (source: pretext-skill-master/SKILL.md) · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
