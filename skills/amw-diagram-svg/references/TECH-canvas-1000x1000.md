---
name: TECH-canvas-1000x1000
category: svg-shape
source: SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md
also-in:
---

# TECH-canvas-1000x1000

## What it does

Renders every SVG diagram inside a fixed **1000×1000 viewBox** with the
center at `(500, 500)`. All primitives stay inside the canvas; the
coordinate system is predictable for every downstream consumer.

## When to use

- **Every mechanical SVG diagram** emitted by `diagram-svg`.
- **Whenever the caller expects a standalone SVG file** they can embed
  in HTML, rasterise, or share.
- **Whenever coordinates need to be computed arithmetically** — the
  fixed 1000×1000 system is pleasant to reason about (centre is 500,
  quadrant boundaries at 250/750, grid divisible into 10s/20s/50s).

Do not use when the diagram is embedded inside a larger scaffold with
its own layout constraints — in that case the parent scaffold owns the
canvas size and this skill emits only the inner primitives.

## How it works

Single root element:

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  ...
</svg>
```

Mental model:

- `(0, 0)` = top-left
- `(500, 500)` = center
- `(1000, 1000)` = bottom-right
- `(x, y)` coordinates in between; `viewBox` makes the canvas
  responsive — consumers can render it at any size without distortion.

Every element must stay inside `0 ≤ x, y ≤ 1000`. Clipping is left to
the consumer's `max-width: 100%` style; the SVG itself assumes nothing
about display size.

## Minimal example

Standalone diagram:

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <rect x="400" y="400" width="200" height="80" rx="20"
        fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>
  <text x="500" y="450" text-anchor="middle" font-size="24"
        fill="#0f172a">Centre Node</text>
</svg>
```

Embedded inside responsive HTML:

```html
<div style="max-width: 800px;">
  <svg viewBox="0 0 1000 1000" style="width: 100%; height: auto;">
    ...
  </svg>
</div>
```

## Gotchas

- **Do not set `width` and `height` attributes on the root `<svg>`.**
  The `viewBox` alone lets the consumer pick render size. Hard-coding
  `width="1000"` forces a fixed pixel dimension and breaks responsive
  layouts.
- **Minimum spacing between nodes: 120 units.** At 1000×1000, 120 units
  is ~12% of the canvas — roughly one node width. Tighter spacing
  produces cramped layouts; looser wastes canvas.
- **No external fonts on canvas-standalone SVGs.** If the SVG references
  a Google Font that isn't loaded, the text falls back to the system
  default, which may not fit the pre-measured layout. Use
  `font-family="system-ui, sans-serif"` and accept the fallback.
- **Text anchor at `(500, 500)`** is NOT the same as centered inside a
  node at `(500, 500)`. The text baseline, not the text centre, sits at
  the y coordinate. Use `dominant-baseline="middle"` OR compute `y +
  fontSize * 0.35` to visually centre.
- **Fixed viewBox forces proportional scaling.** If the caller shows
  the SVG at 200×400, it will be letterboxed. Adjust the `viewBox` to
  match the desired aspect ratio if you know the display size in
  advance; keep it at 1000×1000 otherwise.

## Cross-references

- `../SKILL.md` — canvas is defined in the Usage section
- `TECH-svg-group-structure.md` — recommended layering inside the canvas
- `TECH-stroke-width-4-palette.md` — default strokes at this canvas size
- `TECH-node-shape-vocabulary.md` — the shapes fit this canvas grid
- `../../amw-diagram-architecture/references/TECH-svg-layered-layout.md` —
  alternative fixed-width 820 canvas for layered architecture diagrams
