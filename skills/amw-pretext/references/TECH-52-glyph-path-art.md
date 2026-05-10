---
name: TECH-52-glyph-path-art
category: art
source: pretext-skills/SKILL-11.md
also-in: pretext-skill-main (3D / splat-editor)
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Glyph path art (SVG letterforms with stroke-draw animation)

**Category:** art
**Status:** demo-only

## What it does

Render each letter as an SVG `<path>` extracted via opentype.js `glyph.getPath()`, then animate `stroke-dashoffset` to draw the letterforms on. Pretext handles the line layout; opentype.js handles the per-glyph path. Supports fill, stroke, control-point modes.

## When to use

- Hero animations where letters draw in
- Typography design tool visualizations
- Brand reveal sequences

## How it works

```js
// Source: SKILL-11 opentype.js section
// 1. Load font as .woff or .ttf via fetch + opentype.parse
// 2. For each glyph: opentype.font.getPath(glyph, 0, 0, size).toPathData()
// 3. Create <path d="..."> with stroke-dasharray = path length, stroke-dashoffset animated
// 4. Use pretext for positional layout (x/y of glyph start)
```

## Minimal example

```js
// Source: SKILL-11 defaults
// Stroke-dashoffset draw speed 30-150 ms per glyph (default 80)
// Use @fontsource/inter@5.0.8 .woff via jsdelivr (do NOT use Google Fonts TTF URLs — 404)
```

## Gotchas

- Opentype.js cannot parse `.woff2` — `.woff` or `.ttf` only.
- Render at `(0,0)` and position via `<g transform="translate(x,y)">` — rendering at absolute positions then moving breaks.
- Always scale by `fontSize / font.unitsPerEm`.
- Always apply kerning: `font.getKerningValue(glyph, nextGlyph) * scale`.

## Cross-references

- Related: TECH-35-text-on-path, TECH-43-glyph-morphing
- API reference: [TECH-02-prepare-with-segments](TECH-02-prepare-with-segments.md)
  > What it does · When to use · How it works · Minimal example · TypeScript types (source: pretext-skill-master/SKILL.md) · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
