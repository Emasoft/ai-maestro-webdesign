---
name: amw-diagram-svg
description: Natural-language request to SVG diagram primitives — flowcharts, architecture diagrams, system illustrations with nodes, edges, arrowheads. Triggers on "draw a flowchart of X", "SVG diagram of X", "render data flow as SVG", "draw the architecture as SVG", "node-and-arrow diagram". Does NOT trigger on broad design vocabulary — those route to `design-principles`. Use when authoring an SVG flowchart or architecture diagram. Trigger with /amw-create-or-modify-svg-diagram.
version: 0.1.0
---

# Diagram SVG

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor. Narrow technical triggers only — the orchestrator routes here for structured node-and-edge visuals.

## Overview

Natural-language-to-SVG diagram generator for flowcharts, architecture diagrams, and system illustrations. Produces one self-contained `.svg` file composed from standard primitives (`<rect>`, `<circle>`, `<path>`, `<marker>`, etc.) with a 0–1000 viewBox, flat colors, and optional SMIL animation. Mandatory render-verify loop via `bin/amw-svg-render.py` before delivery.

## Activation

Callable directly via `/amw-create-or-modify-svg-diagram` (user shortcut), or invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode. In Main-agent mode the orchestrator may apply any composition/layout technique in this skill's references, not just what the command's `--kind` flag exposes.

This skill is **autonomous and self-contained** — any agent can use it by reading this SKILL.md and its references.

## Position in flow

**OUTPUT (Phase B).** Mechanical SVG generator: turns a natural-language diagram brief into clean SVG composed of primitives (`<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<line>`, `<path>`, `<text>`, `<marker>`). Downstream receiver of [SKILL](../amw-ascii-to-svg/SKILL.md) when the upstream input is an ASCII freeform diagram. Output: one self-contained `.svg` file in the working directory.

## Trigger conditions

- "draw a flowchart", "render a flowchart as SVG"
- "SVG diagram of <system>", "diagram this as SVG"
- "sketch the data flow as SVG", "visualize the pipeline as SVG"
- "draw the architecture as SVG", "system illustration"
- "make a node-and-arrow diagram", "render this graph as SVG"

Do **not** activate on "design a page", "UI", "landing page", "mockup", "prototype" — `design-principles` owns those. For layered software-architecture diagrams (tiered boxes, labelled zones) route to [SKILL](../amw-diagram-architecture/SKILL.md) instead.

## Prerequisites

- **runtime_binaries:** none (pure LLM → SVG markup)
- **python_packages:** none (optional `cairosvg` used by `../../bin/amw-svg-render.py`)
- **npm_packages / mcp_servers:** none
- **Strongly recommended:** `../../bin/amw-svg-render.py` for the render → view → fix loop — the source skill treats this as mandatory.

## Instructions

1. Determine create vs modify: a natural-language brief → create path; an existing `.svg` file or path → modify path (parse to IR first via `bin/amw-diagram-ir.py parse`).
2. Author the SVG inside a `1000×1000 viewBox` using the four logical groups (`background`, `nodes`, `connections`, `labels`); substitute the user's oklch tokens when supplied. Full primitive vocabulary (canvas, node shapes, styles, text, connections, layout shapes, flowchart/architecture rules) is in [TECH-svg-authoring-primitives](references/TECH-svg-authoring-primitives.md).
   > Canvas and structure · Node types and style · Text labels · Connections and arrowheads · Layout shapes · Flowchart and architecture rules · Cross-references
3. Define arrow markers in `<defs>`; draw connections before nodes so arrowheads are not occluded.
4. If the brief mentions movement / flow, add subtle SMIL animation per [TECH-svg-animation-patterns](references/TECH-svg-animation-patterns.md) — one or two focal elements only, always with the `prefers-reduced-motion` guard.
   > When to animate · Primitive 1 — data-flow pulse on a connector · Primitive 2 — blinking / pulsing active node · Accessibility — prefers-reduced-motion guard · Cross-references
5. Validate with `bin/amw-validate-diagram.sh`; fix any well-formedness or layout issues.
6. **Render-verify loop (mandatory):** run `python3 ../../bin/amw-svg-render.py <path>` to rasterize and visually verify. If the render shows overlap, clipped text, missing arrowheads, or invalid XML, fix the SVG and re-run. Do not ship unverified output.
7. Save to a `.svg` file with a descriptive English name and return the file path. Output routing, the job-completion report, the completion checklist, and the error-handling table are in [TECH-output-and-completion-contract](references/TECH-output-and-completion-contract.md).
   > Output — artifacts and report · Completion checklist · Error handling · Cross-references

> **Token banner.** Every hex in the references is the mechanical slate default — always substitute the user's oklch tokens first when supplied. `design-principles` prefers oklch; hex values are kept only for human-readable pattern matching.

## Technique references

Every technique is documented as one reference file under `./references/`. Read only the file whose TOC matches the current need.

- [TECH-svg-authoring-primitives](references/TECH-svg-authoring-primitives.md) — canvas, structure, node vocabulary, style, text, connections, layout, flowchart/architecture rules
  > Canvas and structure · Node types and style · Text labels · Connections and arrowheads · Layout shapes · Flowchart and architecture rules · Cross-references
- [TECH-svg-animation-patterns](references/TECH-svg-animation-patterns.md) — the two SMIL primitives + reduced-motion guard
  > When to animate · Primitive 1 — data-flow pulse on a connector · Primitive 2 — blinking / pulsing active node · Accessibility — prefers-reduced-motion guard · Cross-references
- [TECH-svg-animate-motion](references/TECH-svg-animate-motion.md) — full SMIL catalogue (three patterns, attribute breakdown, deprecation notes)
  > What it does · When to use · How it works · Animate a dot along a path (data-in-transit pattern) · Blink a node (alert pattern) · Pulse a ring (activation pattern) · Mandatory attributes · Minimal example · Gotchas · Cross-references
- [TECH-svg-group-structure](references/TECH-svg-group-structure.md) — the four logical groups and why connections precede nodes
  > What it does · When to use · How it works · Why this order · Minimal example · Gotchas · Cross-references
- [TECH-svg-output-robustness](references/TECH-svg-output-robustness.md) — well-formedness, closed tags, no external resources
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-arrow-marker-def](references/TECH-arrow-marker-def.md) — arrowhead marker definition and `marker-end` wiring
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-canvas-1000x1000](references/TECH-canvas-1000x1000.md) — the 0–1000 viewBox convention
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-node-shape-vocabulary](references/TECH-node-shape-vocabulary.md) — shape → node-type mapping
  > What it does · When to use · How it works · Gotchas · Cross-references
- [TECH-stroke-width-4-palette](references/TECH-stroke-width-4-palette.md) — stroke-width 4 + the slate palette
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-output-and-completion-contract](references/TECH-output-and-completion-contract.md) — artifact routing, report contract, completion checklist, error-handling table
  > Output — artifacts and report · Completion checklist · Error handling · Cross-references

### Cross-skill references

- [color-system](../amw-design-principles/color-system.md) — `oklch` preferred; source slate palette (`#0f172a` / `#f1f5f9` / `#334155` / `#38bdf8`) is the mechanical default, substitute user tokens when supplied; never emit raw `#000` / `#fff`.
  > I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — keep in-node font sizes in the `18`–`28` band.
  > I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — the anti-slop checklist the output is graded against.
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- [project-output-routing](../amw-design-principles/references/project-output-routing.md) — full artifact-path detection rules.
  > When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
- `../../bin/amw-svg-render.py` — render → view → fix loop. Upstream [SKILL](../amw-ascii-to-svg/SKILL.md) routes here when input is ASCII; route to [SKILL](../amw-diagram-architecture/SKILL.md) for layered architecture instead. Slash command: `/amw-ascii-to-svg`.

## Non-negotiables

- **SVG only.** One `<svg>` element and its contents. No prose, no markdown fences, no `<script>`, no external resources (no remote fonts, no `<image href="http…">`, no `@import`).
- **Only SVG primitives.** `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<line>`, `<path>`, `<text>`, `<tspan>`, `<g>`, `<defs>`, `<marker>`, `<animate>`, `<animateMotion>`. No raster embeds, no AI-drawn illustrations — icons and technical geometry only.
- **Valid XML; all tags closed.** The file parses without fixups.
- **Use plugin tokens when supplied;** otherwise the slate palette. Never raw `#000` / `#fff`.
- **Always run `bin/amw-svg-render.py` before delivery.** Source skill rules make render-verify mandatory.
- **Do not claim broad design vocabulary.** `design-principles` owns "design", "UI", "landing page" — execute only when the orchestrator routes here or the request is unambiguously an SVG diagram.
