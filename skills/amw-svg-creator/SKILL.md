---
name: amw-svg-creator
description: Produce polished technical SVG — icons, logos, badges, patterns, data-vis primitives, animations — with a render-verify-deliver loop. Triggers on "SVG icon", "SVG logo", "SVG pattern", "SVG animation", "polished SVG finish". GATED — does NOT accept illustration, character, mascot, scene, portrait, avatar (banned by ai-slop-avoid.md item 3). Use when creating a polished SVG icon, logo, badge, or pattern. Trigger with "SVG icon".
version: 0.2.0
---

# SVG Creator (GATED)

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **GATED — icons / logos / technical SVG / patterns / animations only.**
> Characters, scenes, mascots, portraits, avatars, people, animals, and any "draw me X" illustration request are **forbidden** by [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) item 3 ("AI-drawn SVG illustrations / mascots / scenes"). If the user asks for any of those, STOP and explain: "design-principles bans AI-drawn character/scene SVG; use a real asset or a placeholder box instead." Do not attempt a "quick one" or a "simplified" version — the ban is absolute.

## Overview

Produces polished technical SVG (icons, logos, badges, patterns, data-vis primitives, SVG animations) via a mandatory render-verify-deliver loop using `bin/amw-svg-render.py`. GATED to geometric/technical SVG only — character illustrations, scenes, mascots, and any "draw me X" requests are absolutely refused. The render-verify loop (`write → render → view PNG → assess → fix → finish`) is non-negotiable: `finish` aborts if `render` was never called.

## Instructions

1. Confirm the request falls within scope (icons, logos, badges, patterns, data-vis primitives, SVG animations) — if it requests a character, scene, mascot, avatar, or "draw me X", stop immediately and cite `ai-slop-avoid.md` item 3; offer a placeholder box instead.
2. Write the SVG source (primitives only: `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<path>`, `<line>`, `<g>`, `<defs>`, `<filter>`, `<animate>`); for icons use 24×24 viewBox, 2px stroke, `fill="none"`, `stroke="currentColor"`.
3. Call `bin/amw-svg-render.py render <file.svg>` to rasterize — this is non-negotiable; `finish` aborts if `render` was never called.
4. View the output PNG (`bin/amw-svg-render.py view <file.png>`) and assess for alignment, legibility at 64px, contrast, and animation correctness.
5. Fix any issues in the SVG source and re-render until the PNG assessment passes.
6. Call `bin/amw-svg-render.py finish <file.svg>` to deliver the final artifact with an optimized copy.

See the `## Mandatory workflow` section below for the authoritative 6-step render-verify-deliver loop.

## Examples

See [README](examples/README.md) for in-scope examples (icons, logos, patterns, data-vis primitives, animations). Advanced SVG techniques (filter chains, noise texture, gradients) are documented in [advanced-techniques](references/advanced-techniques.md).
> [advanced-techniques.md] Filter Chain Cookbook · feTurbulence Parameter Guide · feComponentTransfer Color Grading · Material Simulation · Illustration Composition Templates · Atmospheric and Environmental Effects · Icons with Depth · Logos with Dimension · Animation (CSS + SMIL) · Data Visualizations · Patterns and Backgrounds · Power Features Reference · Character Construction Templates

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator as a Phase B finisher in Main-agent mode when the approved design requires polished technical SVG (icons, logos, patterns, animations). The orchestrator may apply any technique this skill exposes — there is no command-layer restriction on access.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**OUTPUT (Phase B).** Technical SVG finisher: turns a narrow geometric brief into a polished self-contained `.svg` composed of SVG primitives, with a mandatory render → view → fix loop driven by `../../bin/amw-svg-render.py`. Downstream receiver of `../amw-diagram-svg/` and `../amw-ascii-to-svg/` when those need higher-fidelity finish (gradients, filters, micro-animation) on an already-structured diagram.

## Scope — what this skill CAN produce

- **Icons** — 24×24 stroke icons, grid-aligned, 2px stroke, `fill="none"`, `stroke="currentColor"`, `stroke-linecap="round"`, `stroke-linejoin="round"`, coordinates in 2–22.
- **Logos and badges** — geometric construction, centered, 2–3-color palettes, gradient fills, tested for legibility at 64px width.
- **Technical diagrams** (polished finish) — for unstyled diagrams start in `../amw-diagram-svg/`; route here only to add gradient fills, subtle shadows, or smooth transitions.
- **SVG patterns** — repeating tiles via `<pattern patternUnits="userSpaceOnUse">`; `patternTransform="rotate(45)"` for diagonal variants.
- **Data-visualisation primitives** — geometry computed from the data the user supplied; gradient fills on bars/segments; subtle grid (`#f1f5f9` or design-principles neutral); rounded caps.
- **SVG animations** — CSS transitions + SMIL (`<animate>`, `<animateTransform>`, `<animateMotion>`). Every animated element sets `transform-box: fill-box` and `transform-origin: center`. Every animated SVG wraps moving parts in an `@media (prefers-reduced-motion: reduce)` guard that disables motion.

## Scope — what this skill CANNOT produce

- **Character illustrations** — people, avatars, mascots, cartoon creatures, stylised portraits.
- **Scene illustrations** — landscapes, interiors, skies, environments, product scenes.
- **Animal illustrations** — cats, dogs, foxes, pandas, dragons, anything with a body plan.
- **Abstract decorative art** — "looks hand-drawn", "organic", "painterly", "mood piece".
- **Anything whose value is "this looks like a human illustrator drew it"** — the model cannot verify those coordinates, and the output is visibly AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) item 3.
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
- **Anything that substitutes for a real stock or commissioned illustration** — if the user's brief would normally be fulfilled by an Unsplash photo, a purchased SVG pack, or a hired illustrator, it is not this skill's job.

If the request falls in the CANNOT list, stop. Say so explicitly, cite `ai-slop-avoid.md` item 3, and route the user to one of:

1. A **placeholder box** (gray `<rect>` + size label + `alt` describing what the final asset will show) — then ask the user for real assets.
2. [SKILL](../amw-design-principles/SKILL.md) for broader design routing.
3. Real stock / commissioned assets outside this plugin.

## Trigger conditions (all narrow, all technical)

- "SVG icon of <subject>", "stroke icon", "24 × 24 icon grid", "icon set"
- "SVG logo / badge", "geometric logo", "wordmark SVG"
- "SVG pattern", "repeating tile pattern", "background pattern"
- "data-vis SVG", "render this chart as SVG", "gradient bars / arcs"
- "SVG animation", "animate this SVG", "SMIL animation", "pulse / spinner / progress SVG"
- "polish this SVG" after a diagram came out of `../amw-diagram-svg/`

Do **not** activate on "design a page", "UI", "landing page", "mockup", "prototype", "illustration", "character", "scene", "avatar", "mascot", "draw a <creature>", "cute cartoon", "emotional", "painterly".

## Mandatory workflow

The source skill treats the render-verify loop as non-negotiable. This plugin keeps that invariant.

```
WRITE SVG → RENDER → VIEW PNG → ASSESS → FIX → RENDER → VIEW → ... → FINISH
```

1. **Write** the SVG to a working file (typically `draft.svg` in the current project).
2. **Render** with `python3 ../../bin/amw-svg-render.py render <draft.svg>` — this writes `svg_preview.png` in the plugin's state dir and increments an iteration counter.
3. **View** the PNG. Look at what the renderer actually produced, not at the XML you wrote.
4. **Assess** — positioning, proportions, gradient stops, filter bleed, text legibility, reduced-motion behaviour for animations.
5. **Fix** the SVG and repeat 2–4 until correct. Typical iteration counts for this skill's scope:
   - Icons, logos, single-pattern tiles: **1–2** iterations.
   - Multi-stop-gradient logos, filtered badges: **2–3** iterations.
   - Data-vis with many series, animated SVGs: **3–5** iterations.
6. **Finish** with `python3 ../../bin/amw-svg-render.py finish <draft.svg> [name.svg]`. `finish` **refuses to deliver** if `render` was never called — the guard is by design. Claude must visually inspect the PNG at least once before shipping.

## Prerequisites

- **runtime_binaries (system):** `python3` (available on all supported platforms).
- **runtime_binaries (installed via `/amw-init`):** `cairosvg` — auto-pip-installed by `bin/amw-svg-render.py` on first call, so users on a freshly-cloned plugin do not need to pre-install.
- **npm_packages / mcp_servers:** none.

## Visual-quality techniques

Apply these inside the SVG while building. Each is expanded in [advanced-techniques](references/advanced-techniques.md).

- **Multi-stop gradients (4+ stops).** Two-stop gradients look flat; use 4–8 stops with subtle hue shifts. For radial fills (logo spheres, badge centres) offset the light source with `fx="0.3" fy="0.3"`.
- **Five-zone lighting.** Even on a flat logo, a bright light area + true-color mid-tone + cool-hued form shadow (blue / purple / teal, never black) + subtle reflected-light sliver reads more dimensional than a single tint.
- **Coloured shadows.** Shadow fills are `#1e1b4b` (indigo), `#2d1b4e` (purple), or `#0d3b4f` (teal) — never pure black or grey.
- **Drop-shadow filter.** Wrap `feGaussianBlur` → `feOffset` → `feFlood` → `feComposite` → `feMerge`. Always set `color-interpolation-filters="linearRGB"` on the `<filter>` element so blending stays physically accurate.
- **Noise texture.** `<feTurbulence type="fractalNoise" baseFrequency="0.7">` + `feColorMatrix saturate 0` + `feBlend mode="soft-light"`, applied at 5–15 % opacity, breaks digital perfection on logo plates and pattern backgrounds.
- **Animation timing (for the animations scope only).** Pulses 1.2–1.8 s, spinners 0.8–1.2 s per rotation, progress fills 0.4–0.8 s. Every animated SVG ships with a `@media (prefers-reduced-motion: reduce) { animation: none }` block or equivalent SMIL disable, per accessibility best practice.

## Document structure

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"
     role="img" aria-labelledby="svg-title">
  <title id="svg-title">Descriptive title — matches alt text</title>
  <defs><!-- gradients, filters, clipPaths, patterns, markers --></defs>
  <g id="background"></g>
  <g id="midground"></g>
  <g id="foreground"></g>
  <g id="effects"></g>
</svg>
```

## Resources

- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — item 3 is the gating rule. Re-read it if tempted to stretch scope.
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
- [color-system](../amw-design-principles/color-system.md) — use `oklch` tokens when the user supplied them; never raw `#000` / `#fff`.
  > I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — any SVG text follows the plugin's type scale.
  > I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax
- `../../bin/amw-svg-render.py` — the render-verify-finish loop; see `render`, `finish`, `status`, `reset` subcommands.
- [SKILL](../amw-diagram-svg/SKILL.md) — upstream when the request is a freeform node-and-edge diagram.
- [SKILL](../amw-ascii-to-svg/SKILL.md) — upstream when the input is ASCII that needs SVG finish.
- [advanced-techniques](references/advanced-techniques.md) — full cookbook: filter chains, `feTurbulence` parameter guide, `feComponentTransfer` color grading, material simulation, pattern / background recipes, animation timing. Note: the cookbook retains character-construction sections from the upstream skill — **those sections are out of scope here**; consult them only if you are debugging a diagram element that happens to share the same filter technique.
  > Filter Chain Cookbook · feTurbulence Parameter Guide · feComponentTransfer Color Grading · Material Simulation · Illustration Composition Templates · Atmospheric and Environmental Effects · Icons with Depth · Logos with Dimension · Animation (CSS + SMIL) · Data Visualizations · Patterns and Backgrounds · Power Features Reference · Character Construction Templates
- [README](examples/README.md) — in-scope examples (icons, logos, patterns, data-vis primitives, animations). The previously-archived character examples (`cat-astronaut.svg`, `fox-yoga-static.svg`) that shipped with the upstream skill have been moved out of `examples/` to `docs_dev/examples_archive/svg-creator-characters/` so they no longer read as templates for this GATED skill.

## Non-negotiables

- **Character / scene / mascot / avatar requests: REFUSE.** Route to placeholder box or real asset. Cite `ai-slop-avoid.md` item 3.
- **Render-verify before every delivery.** `finish` aborts if `render` was never called — do not work around the guard.
- **Only SVG primitives.** `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<line>`, `<path>`, `<text>`, `<tspan>`, `<g>`, `<defs>`, `<filter>`, `<linearGradient>`, `<radialGradient>`, `<pattern>`, `<marker>`, `<clipPath>`, `<animate>`, `<animateTransform>`, `<animateMotion>`. No raster embeds, no `<script>`, no external CDN fonts or `<image href="http…">`.
- **Self-contained.** No remote resources. One `<svg>` element, its `<defs>`, and its contents.
- **Valid XML with all tags closed.** The file parses without fixups.
- **Colours follow design-principles tokens when supplied,** otherwise `oklch` defaults. Never raw `#000` or `#fff`.
- **Animated SVGs include reduced-motion fallback.** Non-negotiable; users on `prefers-reduced-motion` must see a still frame.
- **Do not claim broad design vocabulary.** `design-principles` owns "design", "UI", "landing page", "mockup" — execute only when the orchestrator routes here or the request is unambiguously technical SVG.

## Error Handling

| Symptom | Likely cause | Fix |
|---|---|---|
| User asked for a mascot / character / avatar | Scope violation | Refuse, cite `ai-slop-avoid.md` item 3, offer placeholder box + ask for real asset. |
| `finish` refuses to deliver | `render` was never called | Run `../../bin/amw-svg-render.py render <file>` first, view the PNG, then `finish`. |
| Gradient bands visible | 2-stop gradient on a large fill | Rewrite as 4–8 stops with small hue shifts; confirm `color-interpolation="linearRGB"`. |
| Drop-shadow edges look dirty | Missing `color-interpolation-filters="linearRGB"` on `<filter>` | Add the attribute to the `<filter>` element. |
| Animation clips / transforms off-centre | Missing `transform-box: fill-box; transform-origin: center;` | Set both CSS properties on the animated element. |
| Reduced-motion users see flashing | Missing `prefers-reduced-motion` guard | Wrap CSS `@keyframes` in `@media (prefers-reduced-motion: no-preference)` or disable SMIL via `begin="indefinite"`. |
| SVG fails to parse | Unclosed tag, stray `&`, missing `xmlns` | Close all tags, escape `&` → `&amp;`, ensure `xmlns="http://www.w3.org/2000/svg"` on the root. |
| Logo illegible at 64 px | Detail density too high for small size | Simplify to 2–3 primitives; test at target size in the render-verify loop. |
| `cairosvg` import failure on first render | Fresh environment, first call | Re-run the command; `bin/amw-svg-render.py` auto-installs `cairosvg` on first use, but a second invocation may be needed on slow networks. |

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `svg-creator` is the user asking about?
  - **fe** (2 techniques)
    - [TECH-fe-component-transfer-color-grading](./references/TECH-fe-component-transfer-color-grading.md) — `feComponentTransfer` — per-channel color grading
      > What it does · Increase contrast · Warm color shift (sunset) · Cool color shift (moonlit) · Posterize (reduce color steps) · Duotone (two-color map) · Gamma curve (lighten midtones) · Gotchas · Cross-references
    - [TECH-fe-turbulence-noise](./references/TECH-fe-turbulence-noise.md) — `feTurbulence` — noise texture that breaks digital perfection
      > What it does · The basic filter · `baseFrequency` — texture scale · Directional stretch — two-value baseFrequency · `numOctaves` — complexity · `type="fractalNoise"` vs `type="turbulence"` · `stitchTiles="stitch"` · `seed` — reproducibility · Salt & Pepper texture (advanced) · Gotchas · Cross-references
  - **atmospheric** (1 techniques)
    - [TECH-atmospheric-effects](./references/TECH-atmospheric-effects.md) — Atmospheric effects — light rays, fog, stars, rain, clouds
  - **character** (1 techniques)
    - [TECH-character-incremental-construction](./references/TECH-character-incremental-construction.md) — Character construction — incremental with aggressive feedback
  - **colored** (1 techniques)
    - [TECH-colored-shadows](./references/TECH-colored-shadows.md) — Colored shadows (never pure black)
  - **css** (1 techniques)
    - [TECH-css-smil-animation](./references/TECH-css-smil-animation.md) — CSS + SMIL animation in SVG
      > What it does · The `transform-box` rule · Spinner (CSS) · Line drawing reveal (pathLength + stroke-dasharray) · Staggered entrance · SMIL animation (works in `<img>` tags) · Attribute animation · Transform animation · Motion along a path · Sequential timing via `begin` · Gotchas · Cross-references
  - **data** (1 techniques)
    - [TECH-data-visualization-svg](./references/TECH-data-visualization-svg.md) — Data visualization in SVG — bars, donuts, grids
      > [TECH-data-visualization-svg.md] What it does · Bar chart with gradient + drop shadow · Donut chart — arc math · Axis lines · Gotchas · Cross-references
  - **drop** (1 techniques)
    - [TECH-drop-shadow-filter](./references/TECH-drop-shadow-filter.md) — Drop shadow, contact shadow, cast shadow (three filter chains)
      > [TECH-drop-shadow-filter.md] What it does · Drop shadow (standard) · Contact shadow (tight, right under object) · Cast shadow (large, soft, far) · Inner shadow (not a drop shadow — opposite direction) · The obligatory `color-interpolation-filters="linearRGB"` · Gotchas · Cross-references
  - **five** (1 techniques)
    - [TECH-five-zone-lighting](./references/TECH-five-zone-lighting.md) — Five-zone lighting model
      > What it does · The five zones · Implementation — radial gradient + overlays · When to use · Gotchas · Cross-references
  - **glassmorphism** (1 techniques)
    - [TECH-glassmorphism-filter](./references/TECH-glassmorphism-filter.md) — Glassmorphism filter — frosted glass effect
      > What it does · The filter · How it works · When to use · When NOT to use · Gotchas · Cross-references
  - **icon** (1 techniques)
    - [TECH-icon-construction](./references/TECH-icon-construction.md) — Icon construction — 24×24 stroke-based + app icons
      > What it does · 24×24 UI icons · 64×64+ app icons — depth + shine · Test legibility at small size · Gotchas · Cross-references
  - **landscape** (1 techniques)
    - [TECH-landscape-composition](./references/TECH-landscape-composition.md) — Landscape scene composition — 7+ layers
      > What it does · The layer stack (back to front) · The template · The atmospheric perspective rule · Gotchas · Cross-references
  - **material** (1 techniques)
    - [TECH-material-simulation](./references/TECH-material-simulation.md) — Material simulation — metal, gold, glass, wood, water, stone, fabric
      > What it does · Metal (steel / chrome) · Gold · Glass / transparent · Wood · Water · Stone / rock · Fabric / cloth · Gotchas · Cross-references
  - **mesh** (1 techniques)
    - [TECH-mesh-gradient-workaround](./references/TECH-mesh-gradient-workaround.md) — Mesh gradient workaround — layered radial gradients
      > What it does · The technique · Best practices · Gradient parameters that matter · When to use · Gotchas · Cross-references
  - **multi** (1 techniques)
    - [TECH-multi-stop-gradients](./references/TECH-multi-stop-gradients.md) — Multi-stop gradients (4+ stops with hue shifts)
      > What it does · When to use · Sky gradient — 6 stops · Sphere radial — 5 stops with offset focal · The `color-interpolation="linearRGB"` rule · Gotchas · Cross-references
  - **paint** (1 techniques)
    - [TECH-paint-order-and-spread-method](./references/TECH-paint-order-and-spread-method.md) — `paint-order` and `spreadMethod` — power features
      > What it does · `paint-order="stroke fill"` · `spreadMethod` on gradients · Example — brushed metal with `reflect` · `vector-effect="non-scaling-stroke"` · `pathLength="1"` · `gradientTransform` · Gotchas · Cross-references
  - **paper** (1 techniques)
    - [TECH-paper-texture-filter](./references/TECH-paper-texture-filter.md) — Paper texture filter
      > What it does · The filter · Parameter walkthrough · When to use · When NOT to use · Usage · Gotchas · Cross-references
  - **pattern** (1 techniques)
    - [TECH-pattern-tiles](./references/TECH-pattern-tiles.md) — `<pattern>` tiles — dots, diagonal lines, waves
      > What it does · Dots · Diagonal lines · Waves · `patternUnits` — the critical attribute · `patternTransform` — rotate / scale / translate the whole pattern · Gotchas · Cross-references
  - **reduced** (1 techniques)
    - [TECH-reduced-motion](./references/TECH-reduced-motion.md) — `prefers-reduced-motion` — mandatory accessibility override
      > What it does · The minimum implementation · Why `0.01ms` instead of `0s` · SMIL equivalent · When it's OK to ignore · When it's partially OK · Gotchas · Cross-references
  - **render** (1 techniques)
    - [TECH-render-verify-loop](./references/TECH-render-verify-loop.md) — The render-verify-deliver loop (mandatory)
      > What it does · When to use · The six steps · Why the loop script · Iteration guidelines · Minimal example · Gotchas · Cross-references
  - **salt** (1 techniques)
    - [TECH-salt-pepper-texture](./references/TECH-salt-pepper-texture.md) — Salt & pepper texture — two-layer professional grain
      > What it does · The filter · When to use · Subtler salt — use `soft-light` instead of `overlay` · Usage pattern · Gotchas · Cross-references
  - **soft** (1 techniques)
    - [TECH-soft-glow-filter](./references/TECH-soft-glow-filter.md) — Soft glow filter
      > What it does · The basic filter · Colored glow variant · `stdDeviation` tuning · Filter region · When to use · Gotchas · Cross-references
  - **specular** (1 techniques)
    - [TECH-specular-diffuse-lighting](./references/TECH-specular-diffuse-lighting.md) — `feSpecularLighting` + `feDiffuseLighting` — physics-based shading
      > What it does · Specular — shiny surface · Diffuse — matte surface · When to use · When NOT to use · Gotchas · Cross-references
  - **vignette** (1 techniques)
    - [TECH-vignette-overlay](./references/TECH-vignette-overlay.md) — Vignette overlay — edge darkening
      > What it does · The gradient · The parameters · Layer order · Off-center vignettes · When to use · When NOT to use · Gotchas · Cross-references

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-atmospheric-effects.md](./references/TECH-atmospheric-effects.md)**
  - Description: Atmospheric effects — light rays, fog, stars, rain, clouds
  - TOC:
    - What it does
    - Light rays (god rays)
    - Fog / mist (masked gradient)
    - Stars with twinkling
    - Rain
    - Clouds
    - Gotchas
    - Cross-references
- **[./references/TECH-character-incremental-construction.md](./references/TECH-character-incremental-construction.md)**
  - Description: Character construction — incremental with aggressive feedback
  - TOC:
    - What it does
    - The incremental build order
    - The thick-line trick for static characters
    - 8-head proportions (standing adult)
    - For animated characters — React + forward kinematics
    - Animation timing
    - When to recommend external tools
    - Gotchas
    - Cross-references
- **[./references/TECH-colored-shadows.md](./references/TECH-colored-shadows.md)**
  - Description: Colored shadows (never pure black)
  - TOC:
    - What it does
    - The palette
    - Where the color goes
    - Drop-shadow filter with colored shadow
    - Opacity rules
    - Gotchas
    - Cross-references
- **[./references/TECH-css-smil-animation.md](./references/TECH-css-smil-animation.md)**
  > What it does · The `transform-box` rule · Spinner (CSS) · Line drawing reveal (pathLength + stroke-dasharray) · Staggered entrance · SMIL animation (works in `<img>` tags) · Attribute animation · Transform animation · Motion along a path · Sequential timing via `begin` · Gotchas · Cross-references
  - Description: CSS + SMIL animation in SVG
  - TOC:
    - What it does
    - The `transform-box` rule
    - Spinner (CSS)
    - Line drawing reveal (pathLength + stroke-dasharray)
    - Staggered entrance
    - SMIL animation (works in `<img>` tags)
    - Gotchas
    - Cross-references
- **[./references/TECH-data-visualization-svg.md](./references/TECH-data-visualization-svg.md)**
  - Description: Data visualization in SVG — bars, donuts, grids
  - TOC:
    - What it does
    - Bar chart with gradient + drop shadow
    - Donut chart — arc math
    - Axis lines
    - Gotchas
    - Cross-references
- **[./references/TECH-drop-shadow-filter.md](./references/TECH-drop-shadow-filter.md)**
  - Description: Drop shadow, contact shadow, cast shadow (three filter chains)
  - TOC:
    - What it does
    - Drop shadow (standard)
    - Contact shadow (tight, right under object)
    - Cast shadow (large, soft, far)
    - Inner shadow (not a drop shadow — opposite direction)
    - The obligatory `color-interpolation-filters="linearRGB"`
    - Gotchas
    - Cross-references
- **[./references/TECH-fe-component-transfer-color-grading.md](./references/TECH-fe-component-transfer-color-grading.md)**
  - Description: `feComponentTransfer` — per-channel color grading
  - TOC:
    - What it does
    - Increase contrast
    - Warm color shift (sunset)
    - Cool color shift (moonlit)
    - Posterize (reduce color steps)
    - Duotone (two-color map)
    - Gamma curve (lighten midtones)
    - Gotchas
    - Cross-references
- **[./references/TECH-fe-turbulence-noise.md](./references/TECH-fe-turbulence-noise.md)**
  - Description: `feTurbulence` — noise texture that breaks digital perfection
  - TOC:
    - What it does
    - The basic filter
    - `baseFrequency` — texture scale
    - Directional stretch — two-value baseFrequency
    - `numOctaves` — complexity
    - `type="fractalNoise"` vs `type="turbulence"`
    - `stitchTiles="stitch"`
    - `seed` — reproducibility
    - Salt & Pepper texture (advanced)
    - Gotchas
    - Cross-references
- **[./references/TECH-five-zone-lighting.md](./references/TECH-five-zone-lighting.md)**
  - Description: Five-zone lighting model
  - TOC:
    - What it does
    - The five zones
    - Implementation — radial gradient + overlays
    - When to use
    - Gotchas
    - Cross-references
- **[./references/TECH-glassmorphism-filter.md](./references/TECH-glassmorphism-filter.md)**
  - Description: Glassmorphism filter — frosted glass effect
  - TOC:
    - What it does
    - The filter
    - How it works
    - When to use
    - When NOT to use
    - Gotchas
    - Cross-references
- **[./references/TECH-icon-construction.md](./references/TECH-icon-construction.md)**
  - Description: Icon construction — 24×24 stroke-based + app icons
  - TOC:
    - What it does
    - 24×24 UI icons
    - 64×64+ app icons — depth + shine
    - Test legibility at small size
    - Gotchas
    - Cross-references
- **[./references/TECH-landscape-composition.md](./references/TECH-landscape-composition.md)**
  - Description: Landscape scene composition — 7+ layers
  - TOC:
    - What it does
    - The layer stack (back to front)
    - The template
    - The atmospheric perspective rule
    - Gotchas
    - Cross-references
- **[./references/TECH-material-simulation.md](./references/TECH-material-simulation.md)**
  - Description: Material simulation — metal, gold, glass, wood, water, stone, fabric
  - TOC:
    - What it does
    - Metal (steel / chrome)
    - Gold
    - Glass / transparent
    - Wood
    - Water
    - Stone / rock
    - Fabric / cloth
    - Gotchas
    - Cross-references
- **[./references/TECH-mesh-gradient-workaround.md](./references/TECH-mesh-gradient-workaround.md)**
  - Description: Mesh gradient workaround — layered radial gradients
  - TOC:
    - What it does
    - The technique
    - Best practices
    - Gradient parameters that matter
    - When to use
    - Gotchas
    - Cross-references
- **[./references/TECH-multi-stop-gradients.md](./references/TECH-multi-stop-gradients.md)**
  - Description: Multi-stop gradients (4+ stops with hue shifts)
  - TOC:
    - What it does
    - When to use
    - Sky gradient — 6 stops
    - Sphere radial — 5 stops with offset focal
    - The `color-interpolation="linearRGB"` rule
    - Gotchas
    - Cross-references
- **[./references/TECH-paint-order-and-spread-method.md](./references/TECH-paint-order-and-spread-method.md)**
  - Description: `paint-order` and `spreadMethod` — power features
  - TOC:
    - What it does
    - `paint-order="stroke fill"`
    - `spreadMethod` on gradients
    - `vector-effect="non-scaling-stroke"`
    - `pathLength="1"`
    - `gradientTransform`
    - Gotchas
    - Cross-references
- **[./references/TECH-paper-texture-filter.md](./references/TECH-paper-texture-filter.md)**
  - Description: Paper texture filter
  - TOC:
    - What it does
    - The filter
    - Parameter walkthrough
    - When to use
    - When NOT to use
    - Usage
    - Gotchas
    - Cross-references
- **[./references/TECH-pattern-tiles.md](./references/TECH-pattern-tiles.md)**
  - Description: `<pattern>` tiles — dots, diagonal lines, waves
  - TOC:
    - What it does
    - Dots
    - Diagonal lines
    - Waves
    - `patternUnits` — the critical attribute
    - `patternTransform` — rotate / scale / translate the whole pattern
    - Gotchas
    - Cross-references
- **[./references/TECH-reduced-motion.md](./references/TECH-reduced-motion.md)**
  - Description: `prefers-reduced-motion` — mandatory accessibility override
  - TOC:
    - What it does
    - The minimum implementation
    - Why `0.01ms` instead of `0s`
    - SMIL equivalent
    - When it's OK to ignore
    - When it's partially OK
    - Gotchas
    - Cross-references
- **[./references/TECH-render-verify-loop.md](./references/TECH-render-verify-loop.md)**
  - Description: The render-verify-deliver loop (mandatory)
  - TOC:
    - What it does
    - When to use
    - The six steps
    - Why the loop script
    - Iteration guidelines
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-salt-pepper-texture.md](./references/TECH-salt-pepper-texture.md)**
  - Description: Salt & pepper texture — two-layer professional grain
  - TOC:
    - What it does
    - The filter
    - When to use
    - Subtler salt — use `soft-light` instead of `overlay`
    - Usage pattern
    - Gotchas
    - Cross-references
- **[./references/TECH-soft-glow-filter.md](./references/TECH-soft-glow-filter.md)**
  - Description: Soft glow filter
  - TOC:
    - What it does
    - The basic filter
    - Colored glow variant
    - `stdDeviation` tuning
    - Filter region
    - When to use
    - Gotchas
    - Cross-references
- **[./references/TECH-specular-diffuse-lighting.md](./references/TECH-specular-diffuse-lighting.md)**
  - Description: `feSpecularLighting` + `feDiffuseLighting` — physics-based shading
  - TOC:
    - What it does
    - Specular — shiny surface
    - Diffuse — matte surface
    - When to use
    - When NOT to use
    - Gotchas
    - Cross-references
- **[./references/TECH-vignette-overlay.md](./references/TECH-vignette-overlay.md)**
  - Description: Vignette overlay — edge darkening
  - TOC:
    - What it does
    - The gradient
    - The parameters
    - Layer order
    - Off-center vignettes
    - When to use
    - When NOT to use
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-svg-creator/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. standalone `.svg` icons, logos, technical primitives). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` or `./public/` for icons/logos created fresh)
   - Last-resort scratch: `/tmp/amw-svg-creator-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.
