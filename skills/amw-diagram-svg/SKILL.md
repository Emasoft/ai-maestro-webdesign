---
name: amw-diagram-svg
description: Natural-language request to SVG diagram primitives — flowcharts, architecture diagrams, system illustrations with nodes, edges, and arrowheads. Triggers on narrow technical intents only — "draw a flowchart of X", "SVG diagram of X", "render the data flow as SVG", "draw the architecture as SVG", "sketch the system as SVG", "make a node-and-arrow diagram". Does NOT trigger on broad design vocabulary ("design", "UI", "landing page", "mockup", "prototype") — those belong to the `design-principles` orchestrator, which routes here when a workflow needs an SVG diagram. Use when authoring or editing a standalone SVG flowchart or architecture diagram with nodes and edges. Trigger with /amw-create-or-modify-svg-diagram.
version: 0.1.0
---

# Diagram SVG

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor. Narrow technical triggers only — the orchestrator routes here for structured node-and-edge visuals.

## Overview

Natural-language-to-SVG diagram generator for flowcharts, architecture diagrams, and system illustrations. Produces one self-contained `.svg` file composed from standard primitives (`<rect>`, `<circle>`, `<path>`, `<marker>`, etc.) with a 0–1000 viewBox, flat colors, and optional SMIL animation. Mandatory render-verify loop via `bin/amw-svg-render.py` before delivery.

## Activation

Callable directly via the `/amw-create-or-modify-svg-diagram` command (user shortcut — fast path for SVG diagram creation/modification), or invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode. In Main-agent mode the orchestrator may apply SVG primitive composition and layout techniques from this skill beyond what the command's `--kind` flag exposes.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

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

## Usage

> **Token banner.** Every hex shown below is the mechanical slate default — always substitute the user's oklch tokens first when supplied. `design-principles` prefers oklch; hex values are kept in the examples only for human-readable pattern matching.

Produce one self-contained SVG inside the canvas and write it to a `.svg` file. Return only the file path.

### Canvas

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
```

Coordinate system `0–1000`; center `(500, 500)`; all elements stay inside.

### Structure

Organize with logical groups (omit any unused):

```xml
<g id="background"></g>
<g id="nodes"></g>
<g id="connections"></g>
<g id="labels"></g>
```

### Node types

| Node type         | Shape                                         |
|-------------------|-----------------------------------------------|
| Process / Service | `<rect>` with rounded corners (`rx=20 ry=20`) |
| Database          | Cylinder — `<ellipse>` + `<rect>` + `<ellipse>` |
| User / Actor      | `<circle>`                                    |
| Decision          | Diamond — `<polygon>`                         |
| External system   | `<rect>` with a dashed stroke                 |

### Node style

- Stroke width `4`, stroke color `#0f172a` (slate-950; oklch ≈ `oklch(20% 0.03 240)`).
- Fill: `#f1f5f9` (slate-100, `oklch(96% 0.01 240)`, light), `#334155` (slate-700, `oklch(37% 0.04 240)`, mid), or `#38bdf8` (sky-400, `oklch(74% 0.15 230)`, accent). Flat colors only.
- Rounded rectangles use `rx="20" ry="20"`.

### Text labels

```xml
<text x="500" y="500" text-anchor="middle" font-size="24" fill="#0f172a">Label</text>
```

- Center text (`text-anchor="middle"`). Font size `18`–`28`.
- Avoid long labels — split into `<tspan>` lines or shorten.

### Connections

Use `<line>` or `<path>`:

```xml
<line x1="200" y1="500" x2="400" y2="500" stroke="#0f172a" stroke-width="4"/>
```

Directional flow uses an arrowhead marker in `<defs>`:

```xml
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
    <polygon points="0 0, 10 3, 0 6" fill="#0f172a"/>
  </marker>
</defs>
```

Apply with `marker-end="url(#arrow)"`.

### Layout

Diagrams are one of three explicit layout shapes — choose ONE before placing
nodes, never mix:

| Layout | When to use | Direction | Minimum spacing |
|---|---|---|---|
| **horizontal-flow** | Linear pipelines, before/after, left-to-right sequences | left → right | `120` units on x, free on y |
| **vertical-flow** | Tiered / layered architecture, top-to-bottom hierarchies | top → bottom | `120` units on y, free on x |
| **grid-layout** | Dense matrices, 3+ parallel branches, quadrant diagrams | both axes | `120` units on both x and y |

Minimum node spacing is `120` units on the active axis of each layout shape
(both axes for grid) — enforced inside the 0-1000 viewBox. No node overlap.
Nodes never touch the canvas edge: reserve ≥ 40 units of margin on all sides.

### Flowchart rules

**Start → Process → Decision → Branch paths → End.** Decisions must use diamond shapes; branch edges must be clearly separated and labelled (`yes` / `no` or domain-specific).

### Architecture diagram rules

Typical nodes: API, Service, Database, Queue, Client, External system. Edges represent data flow or communication direction. For tiered/layered architectures, hand off to `../amw-diagram-architecture/`.

### Optional: Animation

If the brief explicitly mentions movement, flow, or "show data moving", add
subtle SMIL animations to connection lines or active nodes. Every animation
MUST specify both `dur` (e.g. `1s`, `2s`, `3s`) and
`repeatCount="indefinite"`. Keep it low-key — the diagram must still read as
a static image when the animation freezes.

Two canonical animation primitives:

**1. Data-flow pulse on a connector line** — a small dot follows a `<path>`
from source to target, repeating. Use `<animateMotion>` attached to a
`<circle>`, with `<mpath href="#…">` pointing at the line path:

```xml
<path id="flow-a-b" d="M 200 500 L 400 500" stroke="#0f172a"
      stroke-width="4" fill="none" marker-end="url(#arrow)"/>
<circle r="6" fill="#38bdf8">
  <animateMotion dur="2s" repeatCount="indefinite">
    <mpath href="#flow-a-b"/>
  </animateMotion>
</circle>
```

**2. Blinking / pulsing active node** — an `<animate>` on `opacity` or `r`
drives a gentle pulse on a focal component (e.g. the node being described
"right now"):

```xml
<circle cx="500" cy="500" r="40" fill="#38bdf8">
  <animate attributeName="opacity" values="1;0.4;1"
           dur="1.5s" repeatCount="indefinite"/>
</circle>
```

**Accessibility — `prefers-reduced-motion` guard.** Any diagram with animation
MUST include a CSS rule that pauses the animation when the user has enabled
reduced motion. Embed inside a single `<style>` element inside the SVG:

```xml
<style>
  @media (prefers-reduced-motion: reduce) {
    * { animation: none !important; }
    animate, animateMotion, animateTransform { display: none; }
  }
</style>
```

Keep animations to one or two focal elements. Animating every edge at once
turns the diagram into noise and is the fast-track to an AI-slop pattern.

### Render-verify loop (mandatory)

After writing the `.svg`, run `python3 ../../bin/amw-svg-render.py <path>` to rasterize and visually verify. If the render shows overlap, clipped text, missing arrowheads, or invalid XML, fix the SVG and re-run. Do not ship unverified output.

## Resources

- [color-system](../amw-design-principles/color-system.md) — design-principles prefers `oklch`. Source slate palette (`#0f172a` / `#f1f5f9` / `#334155` / `#38bdf8`) is the mechanical default; substitute user tokens when supplied. Never emit raw `#000` / `#fff`.
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — keep in-node font sizes in the `18`–`28` band.
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- `../../bin/amw-svg-render.py` — render → view → fix loop.
- [SKILL](../amw-ascii-to-svg/SKILL.md) — upstream, routes here when input is ASCII.
- [SKILL](../amw-diagram-architecture/SKILL.md) — route there for layered architecture instead.
- Slash command: `/amw-ascii-to-svg`.

## Instructions

1. Determine whether this is a create or modify request: a natural-language brief → create path; an existing `.svg` file or path → modify path (parse to IR first via `bin/amw-diagram-ir.py parse`).
2. Author the SVG inside a `1000×1000 viewBox` using the four logical group structure (`background`, `nodes`, `connections`, `labels`); substitute the user's oklch tokens when supplied.
3. Use the node-shape vocabulary (rect for services, cylinder for databases, diamond for decisions, parallelogram for I/O) and the stroke-width-4-palette from the technique reference.
4. Define arrow markers in `<defs>`; draw connections before nodes so arrow heads are not occluded.
5. Validate the SVG with `bin/amw-validate-diagram.sh`; fix any well-formedness or layout issues before delivery.
6. Save to a `.svg` file with a descriptive English name and return the file path.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `diagram-svg` is the user asking about?
  - **svg** (3 techniques)
    - [TECH-svg-animate-motion](./references/TECH-svg-animate-motion.md) — TECH-svg-animate-motion
      > What it does · When to use · How it works · Animate a dot along a path (data-in-transit pattern) · Blink a node (alert pattern) · Pulse a ring (activation pattern) · Mandatory attributes · Minimal example · Gotchas · Cross-references
    - [TECH-svg-group-structure](./references/TECH-svg-group-structure.md) — TECH-svg-group-structure
    - [TECH-svg-output-robustness](./references/TECH-svg-output-robustness.md) — TECH-svg-output-robustness
  - **arrow** (1 techniques)
    - [TECH-arrow-marker-def](./references/TECH-arrow-marker-def.md) — TECH-arrow-marker-def
  - **canvas** (1 techniques)
    - [TECH-canvas-1000x1000](./references/TECH-canvas-1000x1000.md) — TECH-canvas-1000x1000
  - **node** (1 techniques)
    - [TECH-node-shape-vocabulary](./references/TECH-node-shape-vocabulary.md) — TECH-node-shape-vocabulary
  - **stroke** (1 techniques)
    - [TECH-stroke-width-4-palette](./references/TECH-stroke-width-4-palette.md) — TECH-stroke-width-4-palette

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-arrow-marker-def.md](./references/TECH-arrow-marker-def.md)**
  - Description: TECH-arrow-marker-def
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-canvas-1000x1000.md](./references/TECH-canvas-1000x1000.md)**
  - Description: TECH-canvas-1000x1000
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-node-shape-vocabulary.md](./references/TECH-node-shape-vocabulary.md)**
  - Description: TECH-node-shape-vocabulary
  - TOC:
    - What it does
    - When to use
    - How it works
    - Gotchas
    - Cross-references
- **[./references/TECH-stroke-width-4-palette.md](./references/TECH-stroke-width-4-palette.md)**
  - Description: TECH-stroke-width-4-palette
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-svg-animate-motion.md](./references/TECH-svg-animate-motion.md)**
  > What it does · When to use · How it works · Animate a dot along a path (data-in-transit pattern) · Blink a node (alert pattern) · Pulse a ring (activation pattern) · Mandatory attributes · Minimal example · Gotchas · Cross-references
  - Description: TECH-svg-animate-motion
  - TOC:
    - What it does
    - When to use
    - How it works
    - Mandatory attributes
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-svg-group-structure.md](./references/TECH-svg-group-structure.md)**
  - Description: TECH-svg-group-structure
  - TOC:
    - What it does
    - When to use
    - How it works
    - Why this order
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-svg-output-robustness.md](./references/TECH-svg-output-robustness.md)**
  - Description: TECH-svg-output-robustness
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-diagram-svg/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. standalone `.svg` diagrams). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-diagram-svg-<slug>/`

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

## Non-negotiables

- **SVG only.** One `<svg>` element and its contents. No prose, no markdown fences, no `<script>`, no external resources (no remote fonts, no `<image href="http…">`, no `@import`).
- **Only SVG primitives.** `<rect>`, `<circle>`, `<ellipse>`, `<polygon>`, `<line>`, `<path>`, `<text>`, `<tspan>`, `<g>`, `<defs>`, `<marker>`, `<animate>`, `<animateMotion>`. No raster embeds, no AI-drawn illustrations — icons and technical geometry only.
- **Valid XML; all tags closed.** The file parses without fixups.
- **Use plugin tokens when supplied;** otherwise the slate palette above. Never raw `#000` / `#fff`.
- **Always run `bin/amw-svg-render.py` before delivery.** Source skill rules make render-verify mandatory.
- **Do not claim broad design vocabulary.** `design-principles` owns "design", "UI", "landing page" — execute only when the orchestrator routes here or the request is unambiguously an SVG diagram.

## Error Handling

| Symptom | Likely cause | Fix |
|---|---|---|
| SVG fails to parse | Unclosed tag, stray `&`, missing `xmlns` | Close all tags; include `xmlns="http://www.w3.org/2000/svg"` on the root. |
| Labels overflow nodes | Font too large or label too long | `font-size=18` is expressed in viewBox units, not rendered px — when the SVG ships inside a slide at 1920×1080 (viewBox 0–1000, factor ≈1.92×) it renders ≈35px, safely above the 24px slide floor; when inlined at <600px width it falls below 16px. Prefer splitting via `<tspan>` or shortening the label before dropping below 18 viewBox units. |
| Arrowheads invisible | `<marker>` absent, or `marker-end` URL typo | Verify `<marker id="arrow">` in `<defs>` and `marker-end="url(#arrow)"` id match. |
| Edges tangle / cross nodes | Spacing < 120 units or too dense | Increase spacing, reflow, or switch to grid. |
| Decision branches unclear | Diamond outputs unlabelled | Label edges `yes` / `no` or domain-specific. |
| Animation saturates diagram | Too many concurrent animations | Keep to one or two subtle pulses; prefer static when ambiguous. |
| Render script shows blank | `cairosvg` missing, or content outside `0–1000` viewBox | Install via `/amw-init`; reposition inside canvas. |
| User wanted a layered architecture | Wrong skill | Hand off to [SKILL](../amw-diagram-architecture/SKILL.md). |
