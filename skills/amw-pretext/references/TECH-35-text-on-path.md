---
name: TECH-35-text-on-path
category: art
source: skills/amw-pretext-art/SKILL.md
also-in: SKILL-11.md (Pretext + opentype.js)
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Text on a path (glyph-level placement along a curve)

**Category:** art
**Status:** stable

## What it does

Walk a 2D path (Bezier, custom curve) and advance by each grapheme's measured width, placing each character at the path tangent angle. Pretext supplies the widths; the caller supplies the path sampler. Pairs best with opentype.js for per-glyph SVG path rendering, but can also use `ctx.fillText` with per-glyph transforms.

## When to use

- Circular / spiral text around logos
- Text following a Bezier curve (posters, editorial)
- Animated path-following titles

## How it works

```ts
// Concept — Source: skills/amw-pretext-art/SKILL.md (effect 7) and SKILL-11 (opentype + arc-length)
const prepared = prepareWithSegments(TEXT, FONT)
const { lines } = layoutWithLines(prepared, Infinity, LINE_HEIGHT)
const glyphs = [...lines[0].text]
let arcLen = 0
for (const g of glyphs) {
  const gw = measureGrapheme(g, FONT)  // via prepareWithSegments+layoutWithLines on single char
  const { x, y, angle } = samplePath(path, arcLen + gw / 2)
  ctx.save()
  ctx.translate(x, y)
  ctx.rotate(angle)
  ctx.fillText(g, 0, 0)
  ctx.restore()
  arcLen += gw
}
```

## Minimal example

```ts
// Source: SKILL-11.md — opentype variant
// Use opentype.js glyph.getPath() for SVG <path> with tangent rotation
```

## Gotchas

- When remaining arc length < next grapheme width, clip or switch path segment.
- Kerning is LOST in per-glyph rendering; optional opentype.js `font.getKerningValue()` restores it.
- Grapheme-level rendering disables shaping (Arabic, Devanagari) — use for Latin/CJK only.

## Cross-references

- Related: TECH-34-wavy-baseline, TECH-43-calligram-shapes, TECH-52-glyph-path-art
- API reference: [TECH-04-layout-with-lines](TECH-04-layout-with-lines.md)
  > What it does · When to use · How it works · Minimal example · Return types (source: pretext-skill-master/SKILL.md) · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
