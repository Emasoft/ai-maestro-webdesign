---
name: TECH-41-illuminated-manuscript
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

# Illuminated manuscript (medieval page with living ornaments)

**Category:** art
**Status:** demo-only

## What it does

Combine pretext obstacle routing with opentype.js path animation to build a "living" medieval page: wet-ink amplitude on drawn glyphs, vine growth that reflows body text in real time, capital-letter inflation on hover, aging effects (yellowing), and "erasure poetry" where body text dissolves into the illuminated ornaments.

## When to use

- Portfolio / showcase demos
- Literary brand pages
- Kinetic "wow" interactives

## How it works

The composition uses every pretext primitive plus opentype.js:
- pretext routes body text around the growing vines (TECH-23 animated obstacles)
- opentype.js `glyph.getPath()` renders the capitals as SVG, animated per-segment
- "wet ink" is a per-glyph micro-offset decaying with tau 800-3000 ms (SKILL-11 defaults)

```js
// Source: SKILL-11 params
// Wet ink amplitude 0.5-3 px, decay 800-3000 ms, stroke draw 30-150 ms per glyph
```

## Minimal example

Not runnable in a few lines — full demo is in SKILL-11 `references/opentype-integration.md`.

## Gotchas

- Opentype.js cannot parse `.woff2` — use `.woff` or `.ttf` only.
- Rendering per-glyph at high frame rates is CPU-heavy; cache `glyph.getPath()` output strings.
- Do not skip `font.getKerningValue(glyph, next) * scale` — missing kerning looks broken.

## Cross-references

- Related: TECH-23-animated-obstacle-reflow, TECH-52-glyph-path-art
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
