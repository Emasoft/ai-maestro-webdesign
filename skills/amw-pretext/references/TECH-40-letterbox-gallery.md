---
name: TECH-40-letterbox-gallery
category: art
source: pretext-skills/SKILL-11.md
also-in: 
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Letterbox gallery (each character its own filled canvas)

**Category:** art
**Status:** demo-only

## What it does

Given a short string ("BEACON"), render each character on its own `<canvas>` tile in a grid, with the character's interior filled by small text (same glyph-mask technique as TECH-39). Each tile supports independent cursor displacement and interaction (hover pushes the fill text aside).

## When to use

- Hero galleries for brand names
- Interactive poster letters
- Demo showcases for pretext capabilities

## How it works

```js
// Source: SKILL-11.md defaults
// 1. For each char in input string, create a <canvas> element
// 2. Run TECH-39 glyph-mask fill on each canvas independently
// 3. Attach pointer handlers; pass cursor position into fill algorithm
// 4. Displace fill text toward/away from cursor with damping
```

## Minimal example

```js
// Source: SKILL-11 defaults
// Grid columns 2–6 (default 3), cursor displacement radius 50–250 px, force 10–50, damping 0.85–0.98
```

## Gotchas

- 1 canvas per letter = N `getImageData` calls at init — heavy. Compute masks once, cache.
- Cursor displacement in the fill must be bounded or the text spills over adjacent tiles.

## Cross-references

- Related: TECH-39-glyph-mask-calligram, TECH-37-typographic-ascii
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
