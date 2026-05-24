# amw-svg-creator — Technique Catalog

This is the full reference index for the GATED `amw-svg-creator` skill.
The orchestrator should read only the technique file whose topic matches
the current need; this catalog exists so the SKILL.md itself stays compact.

## Decision tree (top-down)

Walk this tree top-down to pick the right reference. If a branch does
not match the user's intent, skip to the next. Every technique in the
catalog is a leaf of this tree.

- Which aspect of `svg-creator` is the user asking about?
  - **fe** (2 techniques)
    - [TECH-fe-component-transfer-color-grading](./TECH-fe-component-transfer-color-grading.md)
      > `feComponentTransfer` — per-channel color grading
    - [TECH-fe-turbulence-noise](./TECH-fe-turbulence-noise.md)
      > `feTurbulence` — noise texture that breaks digital perfection
  - **atmospheric** (1) — [TECH-atmospheric-effects](./TECH-atmospheric-effects.md)
  - **character** (1, OUT OF SCOPE) — [TECH-character-incremental-construction](./TECH-character-incremental-construction.md) (retained as filter cookbook only; the skill REFUSES character SVG requests).
  - **colored** (1) — [TECH-colored-shadows](./TECH-colored-shadows.md)
  - **css** (1) — [TECH-css-smil-animation](./TECH-css-smil-animation.md)
  - **data** (1) — [TECH-data-visualization-svg](./TECH-data-visualization-svg.md)
  - **drop** (1) — [TECH-drop-shadow-filter](./TECH-drop-shadow-filter.md)
  - **five** (1) — [TECH-five-zone-lighting](./TECH-five-zone-lighting.md)
  - **glassmorphism** (1) — [TECH-glassmorphism-filter](./TECH-glassmorphism-filter.md)
  - **icon** (1) — [TECH-icon-construction](./TECH-icon-construction.md)
  - **landscape** (1, OUT OF SCOPE) — [TECH-landscape-composition](./TECH-landscape-composition.md) (filter cookbook only).
  - **material** (1) — [TECH-material-simulation](./TECH-material-simulation.md)
  - **mesh** (1) — [TECH-mesh-gradient-workaround](./TECH-mesh-gradient-workaround.md)
  - **multi** (1) — [TECH-multi-stop-gradients](./TECH-multi-stop-gradients.md)
  - **paint** (1) — [TECH-paint-order-and-spread-method](./TECH-paint-order-and-spread-method.md)
  - **paper** (1) — [TECH-paper-texture-filter](./TECH-paper-texture-filter.md)
  - **pattern** (1) — [TECH-pattern-tiles](./TECH-pattern-tiles.md)
  - **reduced** (1) — [TECH-reduced-motion](./TECH-reduced-motion.md)
  - **render** (1) — [TECH-render-verify-loop](./TECH-render-verify-loop.md)
  - **salt** (1) — [TECH-salt-pepper-texture](./TECH-salt-pepper-texture.md)
  - **soft** (1) — [TECH-soft-glow-filter](./TECH-soft-glow-filter.md)
  - **specular** (1) — [TECH-specular-diffuse-lighting](./TECH-specular-diffuse-lighting.md)
  - **vignette** (1) — [TECH-vignette-overlay](./TECH-vignette-overlay.md)

## Per-technique TOC index

Every technique in this skill is documented as a single `TECH-*.md` file
under `./` (this directory). Each file has the same TOC shape: *What it
does · When to use · How it works · Minimal example · Gotchas ·
Cross-references*. Read only the file whose topic matches the current need.

- **chart**: [TECH-chart-rendering](./TECH-chart-rendering.md)
- **icon**: [TECH-icon-construction](./TECH-icon-construction.md)
- **filters**: [TECH-drop-shadow-filter](./TECH-drop-shadow-filter.md),
  [TECH-soft-glow-filter](./TECH-soft-glow-filter.md),
  [TECH-paper-texture-filter](./TECH-paper-texture-filter.md),
  [TECH-glassmorphism-filter](./TECH-glassmorphism-filter.md),
  [TECH-vignette-overlay](./TECH-vignette-overlay.md)
- **textures**: [TECH-fe-turbulence-noise](./TECH-fe-turbulence-noise.md),
  [TECH-salt-pepper-texture](./TECH-salt-pepper-texture.md)
- **gradients & lighting**: [TECH-multi-stop-gradients](./TECH-multi-stop-gradients.md),
  [TECH-mesh-gradient-workaround](./TECH-mesh-gradient-workaround.md),
  [TECH-five-zone-lighting](./TECH-five-zone-lighting.md),
  [TECH-colored-shadows](./TECH-colored-shadows.md),
  [TECH-specular-diffuse-lighting](./TECH-specular-diffuse-lighting.md),
  [TECH-fe-component-transfer-color-grading](./TECH-fe-component-transfer-color-grading.md)
- **materials**: [TECH-material-simulation](./TECH-material-simulation.md)
- **patterns**: [TECH-pattern-tiles](./TECH-pattern-tiles.md),
  [TECH-paint-order-and-spread-method](./TECH-paint-order-and-spread-method.md)
- **animation**: [TECH-css-smil-animation](./TECH-css-smil-animation.md),
  [TECH-reduced-motion](./TECH-reduced-motion.md)
- **data-vis**: [TECH-data-visualization-svg](./TECH-data-visualization-svg.md)
- **render workflow**: [TECH-render-verify-loop](./TECH-render-verify-loop.md)
- **out-of-scope reference only**: [TECH-character-incremental-construction](./TECH-character-incremental-construction.md),
  [TECH-landscape-composition](./TECH-landscape-composition.md),
  [TECH-atmospheric-effects](./TECH-atmospheric-effects.md)

## Cross-references

- [SKILL](../SKILL.md) — parent skill (orchestrator for this catalog)
- [advanced-techniques](./advanced-techniques.md) — historical cookbook with the upstream skill's filter library
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — item 3 (illustration ban) — this skill is GATED away from character / scene / mascot output
