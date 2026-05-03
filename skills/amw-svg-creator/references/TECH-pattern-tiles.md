---
name: TECH-pattern-tiles
category: svg-gradient
source: image-generation/svg-creator/SKILL.md
also-in: image-generation/svg-creator/references/advanced-techniques.md
---
## Table of Contents

- [What it does](#what-it-does)
- [Dots](#dots)
- [Diagonal lines](#diagonal-lines)
- [Waves](#waves)
- [`patternUnits` — the critical attribute](#patternunits-the-critical-attribute)
- [`patternTransform` — rotate / scale / translate the whole pattern](#patterntransform-rotate-scale-translate-the-whole-pattern)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# `<pattern>` tiles — dots, diagonal lines, waves

## What it does

SVG's `<pattern>` element repeats a small tile across a fill area.
Use for backgrounds, watermarks, or texture fills. The library of
common patterns covers dots, diagonal lines (via
`patternTransform`), and sine waves.

## Dots

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<pattern id="dots" patternUnits="userSpaceOnUse" width="20" height="20">
  <circle cx="10" cy="10" r="1.5" fill="#cbd5e1"/>
</pattern>
<rect width="800" height="600" fill="url(#dots)"/>
```

`width="20" height="20"` — the tile is 20×20. Dot center at
`(10, 10)` puts it in the middle of each tile.

## Diagonal lines

```xml
<pattern id="diag" patternUnits="userSpaceOnUse" width="10" height="10"
  patternTransform="rotate(45)">
  <line x1="0" y1="0" x2="0" y2="10" stroke="#e2e8f0" stroke-width="1"/>
</pattern>
```

The line is vertical inside the tile; `patternTransform="rotate(45)"`
rotates the entire pattern 45° — produces diagonal stripes.

## Waves

```xml
<pattern id="wave" patternUnits="userSpaceOnUse" width="100" height="20">
  <path d="M0,10 Q25,0 50,10 Q75,20 100,10" fill="none" stroke="#e2e8f0"/>
</pattern>
```

The path must start and end at the same Y so tiles join seamlessly.

## `patternUnits` — the critical attribute

```
patternUnits="userSpaceOnUse"      Tiles size in the SVG coordinate system
                                    (width/height are raw px) — usually what you want.
patternUnits="objectBoundingBox"   Tiles size as fractions of the element
                                    being filled — confusing; rarely used.
```

Always use `userSpaceOnUse` unless you know exactly why you don't.

## `patternTransform` — rotate / scale / translate the whole pattern

```xml
patternTransform="rotate(45)"      45° diagonal
patternTransform="scale(2)"        Double-sized tiles
patternTransform="translate(5 0)"  Offset horizontally
```

## Gotchas

- Tile size matters for scale — 20×20 dots on a 100×100 area look
  different than on a 1000×1000 area.
- Pattern fills don't scale with element transforms by default. Use
  `patternTransform` explicitly if you want the pattern to scale too.
- Some renderers have rounding bugs at pattern tile edges — artifacts
  appear as thin lines. Add 1-2px of bleed in the tile design.

## Cross-references

- [TECH-mesh-gradient-workaround](TECH-mesh-gradient-workaround.md) — overlapping radials as an
  > What it does · The technique · Best practices · Gradient parameters that matter · When to use · Gotchas · Cross-references
  alternative "organic" background.
- [TECH-fe-turbulence-noise](TECH-fe-turbulence-noise.md) — stochastic noise instead of
  > What it does · The basic filter · `baseFrequency` — texture scale · Directional stretch — two-value baseFrequency · `numOctaves` — complexity · `type="fractalNoise"` vs `type="turbulence"` · `stitchTiles="stitch"` · `seed` — reproducibility · Salt & Pepper texture (advanced) · Gotchas · Cross-references
  regular tiling.
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

