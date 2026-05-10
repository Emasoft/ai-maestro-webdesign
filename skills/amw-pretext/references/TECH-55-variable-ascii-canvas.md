---
name: TECH-55-variable-ascii-canvas
category: art
source: pretext-skills/amw-pretext-frontend-motion-main/core/bundle/references/demo-family-map.md (Variable Typographic ASCII)
also-in: SKILL-15.md (variable-typographic-ascii.ts)
---

# Variable Typographic ASCII (Canvas glyph field anchored to measured lines)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** art
**Status:** stable

## What it does

A Canvas glyph field where character density, weight, opacity, and style vary per-cell, but the layout is ANCHORED to pretext-measured line positions. Proves `prepareWithSegments()` doubles as a per-glyph width measurement primitive — not just a paragraph layout tool.

## When to use

- Demo art / showcases
- Loading indicators with dense text visuals
- Decorative hero panels

## How it works

```ts
// Source: SKILL-15.md demo pointer + pretext-frontend-motion-main
// 1. prepareWithSegments() with a compact charset ('.:-=+*#%@')
// 2. layoutWithLines() to get line anchors
// 3. Within each line's bounding box, draw a grid of characters whose density varies
// 4. Each grid cell picks a character based on a noise / physics function
```

## Minimal example

See SKILL-15 `demos/variable-typographic-ascii.ts`.

## Gotchas

- Use a serif / proportional font — monospace looks boring (SKILL-11 recommendation).
- Opacity bands should be ~10 levels for smooth gradients.
- Never pure black `#000` — use off-blacks (SKILL-11 defaults).

## Cross-references

- Related: TECH-37-typographic-ascii, TECH-04-layout-with-lines
- API reference: [TECH-04-layout-with-lines](TECH-04-layout-with-lines.md)
  > What it does · When to use · How it works · Minimal example · Return types (source: pretext-skill-master/SKILL.md) · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
