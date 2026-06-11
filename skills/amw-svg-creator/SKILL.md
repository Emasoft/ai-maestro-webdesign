---
name: amw-svg-creator
description: Produce polished technical SVG — icons, logos, badges, patterns, data-vis primitives, animations — with a render-verify-deliver loop. Triggers on "SVG icon", "SVG logo", "SVG pattern", "SVG animation", "polished SVG finish". GATED — does NOT accept illustration, character, mascot, scene, portrait, avatar (banned by ai-slop-avoid.md item 3). Use when creating a polished SVG icon, logo, badge, or pattern. Trigger with "SVG icon".
version: 0.1.0
---

# SVG Creator (GATED)

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **GATED — icons / logos / technical SVG / patterns / animations only.**
> Characters, scenes, mascots, portraits, avatars, people, animals, and any "draw me X" illustration request are **forbidden** by [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) item 3 ("AI-drawn SVG illustrations / mascots / scenes"). If the user asks for any of those, STOP and explain: "design-principles bans AI-drawn character/scene SVG; use a real asset or a placeholder box instead." Do not attempt a "quick one" or a "simplified" version — the ban is absolute.
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)

## Overview

Produces polished technical SVG (icons, logos, badges, patterns, data-vis primitives, SVG animations) via a mandatory render-verify-deliver loop using `bin/amw-svg-render.py`. GATED to geometric/technical SVG only — character illustrations, scenes, mascots, and any "draw me X" requests are absolutely refused. The render-verify loop (`write → render → view PNG → assess → fix → finish`) is non-negotiable: `finish` aborts if `render` was never called.

## Instructions

1. Confirm the request falls within scope (icons, logos, badges, patterns, data-vis primitives, SVG animations) — if it requests a character, scene, mascot, avatar, or "draw me X", stop immediately and cite `ai-slop-avoid.md` item 3; offer a placeholder box instead.
2. Write the SVG source (primitives only: `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<path>`, `<line>`, `<g>`, `<defs>`, `<filter>`, `<animate>`); for icons use 24×24 viewBox, 2px stroke, `fill="none"`, `stroke="currentColor"`.
3. Call `bin/amw-svg-render.py render <file.svg>` to rasterize — this is non-negotiable; `finish` aborts if `render` was never called.
4. View the output PNG (path printed by the render step) and assess for alignment, legibility at 64px, contrast, and animation correctness.
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

## Scope

**CAN produce:** 24×24 stroke icons (grid-aligned, 2 px stroke,
`fill="none"`, `stroke="currentColor"`); geometric logos / badges (2-3
color palettes, gradient fills, legible at 64 px); polished technical
diagrams (route via `../amw-diagram-svg/` first); SVG patterns
(`<pattern patternUnits="userSpaceOnUse">`); data-vis primitives
(computed geometry + gradient fills + rounded caps); SVG animations
(CSS / SMIL — every animated element MUST set `transform-box: fill-box`
and ship a `prefers-reduced-motion` guard).

**CANNOT produce (REFUSE):** character illustrations (people / avatars /
mascots / cartoons / portraits); scene illustrations (landscapes /
interiors / environments); animals (any body plan); abstract decorative
art ("hand-drawn", "painterly", "mood piece"); anything substituting for a
real stock / commissioned illustration. On any of these: stop, cite
[ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) item 3, and
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
offer (1) a placeholder box, (2) routing to [SKILL](../amw-design-principles/SKILL.md), or (3) real assets outside this plugin.

## Trigger conditions (narrow, technical)

**Fires on:** "SVG icon of <subject>", "stroke icon", "24×24 icon grid",
"SVG logo / badge", "geometric logo", "wordmark SVG", "SVG pattern",
"repeating tile", "data-vis SVG", "render this chart as SVG", "SVG
animation", "SMIL animation", "pulse / spinner / progress SVG", "polish
this SVG" (after `../amw-diagram-svg/`).

**Does NOT fire on:** "design a page", "UI", "landing page", "mockup",
"prototype", "illustration", "character", "scene", "avatar", "mascot",
"draw a <creature>", "cute cartoon", "emotional", "painterly".

## Mandatory workflow

```
WRITE SVG → RENDER → VIEW PNG → ASSESS → FIX → RENDER → VIEW → ... → FINISH
```

1. **Write** SVG to a working file (e.g. `draft.svg`).
2. **Render** via `python3 ../../bin/amw-svg-render.py render <draft.svg>`
   — writes `svg-preview.png` (in the state dir) and increments the iteration counter.
3. **View** the PNG (what the renderer produced, not the XML).
4. **Assess** positioning, proportions, gradient stops, filter bleed,
   text legibility, reduced-motion behaviour.
5. **Fix + repeat** 2-4. Typical iterations: icons/logos/single tiles
   1-2, multi-stop logos / filtered badges 2-3, data-vis / animations 3-5.
6. **Finish** via `python3 ../../bin/amw-svg-render.py finish <draft.svg> [name.svg]`
   — refuses to deliver if `render` was never called. By design.

## Prerequisites

- `python3` (system); `cairosvg` must be installed manually (`uv pip install cairosvg` or `python3 -m pip install --user cairosvg`) — the render script does NOT auto-install it.
- No npm / MCP dependencies.

## Visual-quality techniques

Apply these in the SVG while building. Each is expanded in
[advanced-techniques](references/advanced-techniques.md) and the matching
> [advanced-techniques.md] Filter Chain Cookbook · feTurbulence Parameter Guide · feComponentTransfer Color Grading · Material Simulation · Illustration Composition Templates · Atmospheric and Environmental Effects · Icons with Depth · Logos with Dimension · Animation (CSS + SMIL) · Data Visualizations · Patterns and Backgrounds · Power Features Reference · Character Construction Templates
`TECH-*.md` file in `references/`.

- **Multi-stop gradients (4+ stops)** — two-stop is flat; use 4-8 with hue
  shifts; offset focal `fx="0.3" fy="0.3"` for radial.
- **Five-zone lighting** — bright light + mid-tone + cool form shadow +
  reflected light reads dimensional even on a flat logo.
- **Coloured shadows** — `#1e1b4b` / `#2d1b4e` / `#0d3b4f` (never black/grey).
- **Drop-shadow filter** — `feGaussianBlur` → `feOffset` → `feFlood` →
  `feComposite` → `feMerge`; ALWAYS set `color-interpolation-filters="linearRGB"`.
- **Noise texture** — `feTurbulence` (`fractalNoise`, `baseFrequency≈0.7`)
  + `feColorMatrix saturate 0` + `feBlend soft-light` at 5-15 % opacity.
- **Animation timing** — pulses 1.2-1.8 s, spinners 0.8-1.2 s, progress
  0.4-0.8 s; always ship `prefers-reduced-motion` fallback.

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

- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — item 3 is the gating rule; re-read if tempted to stretch scope.
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- [color-system](../amw-design-principles/color-system.md) — use `oklch` tokens; never raw `#000` / `#fff`.
> [color-system.md] I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — SVG text follows the plugin's type scale.
> [typography-system.md] I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
- `../../bin/amw-svg-render.py` — the render-verify-finish loop (subcommands: `render`, `finish`, `status`, `reset`).
- [SKILL](../amw-diagram-svg/SKILL.md) / [SKILL](../amw-ascii-to-svg/SKILL.md) — upstream sources.
- [CATALOG](references/CATALOG.md) — full per-TECH index.
> [CATALOG.md] Decision tree (top-down) · Per-technique TOC index · Cross-references
- [advanced-techniques](references/advanced-techniques.md) — historical cookbook from the upstream skill. **Character-construction sections are OUT OF SCOPE** for this GATED skill; consult only when debugging a shared filter technique.
> [advanced-techniques.md] Filter Chain Cookbook · feTurbulence Parameter Guide · feComponentTransfer Color Grading · Material Simulation · Illustration Composition Templates · Atmospheric and Environmental Effects · Icons with Depth · Logos with Dimension · Animation (CSS + SMIL) · Data Visualizations · Patterns and Backgrounds · Power Features Reference · Character Construction Templates
- [README](examples/README.md) — in-scope examples (icons, logos, patterns, data-vis, animations). Character examples archived to `docs_dev/examples_archive/svg-creator-characters/`.

## Non-negotiables

- **REFUSE character / scene / mascot / avatar** requests. Cite `ai-slop-avoid.md` item 3.
- **Render-verify before delivery.** `finish` aborts if `render` was never called.
- **Only SVG primitives** (`rect`, `circle`, `ellipse`, `polygon`, `line`, `path`, `text`, `tspan`, `g`, `defs`, `filter`, `linearGradient`, `radialGradient`, `pattern`, `marker`, `clipPath`, `animate*`). No raster embeds, no `<script>`, no remote CDN fonts.
- **Self-contained** — one `<svg>` element, its `<defs>`, no remote resources.
- **Valid XML, all tags closed**, `xmlns="http://www.w3.org/2000/svg"` on root.
- **Colours via design-principles tokens** when supplied; `oklch` defaults; never raw `#000` / `#fff`.
- **Animated SVGs ship `prefers-reduced-motion` fallback** — non-negotiable.
- **Do not claim broad design vocabulary** — `design-principles` owns that.

## Error Handling

See [TECH-error-handling](references/TECH-error-handling.md) for the full
> [TECH-error-handling.md] What it does · When to use · Symptom table · Cross-references
symptom → cause → fix table (9 known failure modes, one canonical fix each).

## Technique selection and references

See [CATALOG](references/CATALOG.md) for the full decision tree (top-down,
> [CATALOG.md] Decision tree (top-down) · Per-technique TOC index · Cross-references
by user-intent keyword) and the per-TECH index. Every technique in this
skill is a single `TECH-*.md` file under `./references/`. Read only the
file whose topic matches the current need.

<!-- end of references — see references/CATALOG.md for the full per-TECH index -->

## Completion checklist

Before reporting complete (FAIL on any item triggers a remediation loop):

- Inputs captured verbatim — no silent paraphrasing.
- At least one `TECH-*.md` consulted and cited.
- Output passes `## Non-negotiables`.
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- Output rendered/validated via `bin/amw-svg-render.py`.
- Cross-skill hand-offs documented.
- Filename is descriptive English (`Logo — Acme Badge.svg`, not `out.svg`).

## Output

TWO outputs (artifact SVG + job-completion report). Full contract in
[skill-completion-and-output-contract](../amw-design-principles/references/skill-completion-and-output-contract.md)
and [project-output-routing](../amw-design-principles/references/project-output-routing.md).
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
Report path: `$MAIN_ROOT/reports/webdesigner/<ts>_<slug>_<hash>.md`.
Every artifact MUST be linked from the report.
