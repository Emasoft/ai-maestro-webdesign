---
name: amw-diagram-editorial
description: Editorial-quality HTML+SVG diagrams with brand-matched styling — 13 fixed types (architecture, flowchart, sequence, state machine, ER, timeline, swimlane, quadrant, nested, tree, layer stack, Venn, pyramid/funnel). Triggers on narrow editorial-diagram intents like "sequence diagram", "ER diagram", "blog-ready architecture diagram". NOT for generic design intent, freeform SVG, or pure architecture-graph JSON — those belong to design-principles, svg-creator, and diagram-architecture respectively. Full trigger list in Trigger conditions section. Use when creating a polished editorial HTML+SVG diagram of one of the 13 supported diagram types. Trigger with /amw-create-or-modify-html-diagram.
version: 0.1.0
author: ai-maestro-webdesign
---

# Diagram Editorial

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is an executor. Its triggers are editorial-diagram-specific only — `design-principles` routes here when the user wants a blog-ready or documentation-ready diagram and has committed to one of the 13 canonical types.

## Overview

Editorial-quality HTML+SVG diagrams with brand-matched styling. Supports 13 fixed diagram types (architecture, flowchart, sequence, state machine, ER, timeline, swimlane, quadrant, nested, tree, layer stack, Venn, pyramid/funnel). Emits self-contained HTML with inline CSS and inline SVG, respecting the 4px grid, oklch palette, WCAG AA, and the three-family typography system.

## Activation

Callable directly via the `/amw-create-or-modify-html-diagram` command with `--style editorial` (user shortcut — fast path for editorial diagram creation). Also invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode. In Main-agent mode the orchestrator may apply any of the 13 diagram types and brand-onboarding techniques from this skill beyond what the command's `--style` flag exposes.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**OUTPUT (Phase B).** Emits self-contained HTML files — inline CSS + inline SVG, no external assets other than optional Google Fonts / Bunny Fonts. Each file respects design-principles color and typography tokens (4px grid, oklch palette, WCAG AA) and is ready to paste into a blog post, docs site, or MDX article.

This skill does NOT substitute for:
- `../amw-diagram-svg/` — freeform SVG primitives from natural-language intent. Plain `flowchart` intent (no "editorial" / "blog-ready" qualifier) routes to `../amw-diagram-svg/` unless the user explicitly asks for an editorial or blog-ready flowchart.
- `../amw-diagram-architecture/` — graph JSON / Mermaid / SVG / PNG for architecture-only diagrams.
- `../amw-svg-creator/` — icons, logos, animated SVG (gated scope).

When in doubt about which diagram skill to use, route back to `design-principles`.

## Trigger conditions

Activate only on editorial-diagram intents that name one of the 13 canonical types or explicitly ask for a "blog-ready" / "editorial" diagram:

- "make me an editorial diagram of <topic>"
- "sequence diagram of <flow>" / "OAuth sequence"
- "ER diagram for <schema>" / "data model diagram"
- "state machine for <lifecycle>"
- "timeline of <events>"
- "swimlane for <cross-functional flow>"
- "quadrant of X vs Y" / "impact-vs-effort chart"
- "Venn diagram of <sets>"
- "layer stack diagram" / "OSI-style stack"
- "pyramid diagram" / "conversion funnel"
- "nested hierarchy diagram" / "containment diagram"
- "tree diagram" / "org chart" / "file tree diagram"
- "architecture diagram for my blog post" / "editorial architecture diagram"
- "onboard editorial diagrams to <url>" (brand-onboarding flow)

Do NOT activate on generic intent ("draw a picture", "design a page", "make an illustration"). Those are `design-principles`' territory and it will route here once the user commits to a specific type.

## Prerequisites

- **runtime_binaries (system):** none at run-time — the HTML output opens in any browser. `node ≥ 22` is needed only if the user pairs this skill with `../amw-dev-browser/` for preview screenshots.
- **runtime_binaries (installed via `/amw-init`):** none required. Optional: `dev-browser` CLI for `/amw-preview`, `python ≥ 3.8` + `cairosvg` for `bin/amw-svg-render.py` render-verify loop.
- **python_packages:** none required.
- **npm_packages:** none required.
- **mcp_servers:** none.
- **Optional upstream:** `../amw-dev-browser/` — used only during the brand-onboarding flow to fetch the user's homepage and extract palette + font stack. Never use raw WebFetch for onboarding — always route through `dev-browser`.

## The 13 diagram types (selection table)

| Type | Use when… |
|---|---|
| **architecture** | Components + connections (services, APIs, infra). |
| **flowchart** | Decision logic, yes/no branches. |
| **sequence** | Messages over time (OAuth, API calls, user flows). |
| **state machine** | States + transitions (order lifecycle, auth state). |
| **ER / data model** | Entities + fields + relationships. |
| **timeline** | Events on a horizontal or vertical axis. |
| **swimlane** | Cross-functional flows (who does what, when). |
| **quadrant** | Two-axis positioning (impact vs effort, risk vs value). |
| **nested** | Hierarchy by containment (layers inside layers). |
| **tree** | Parent → children (org chart, file tree, decision tree). |
| **layer stack** | Stacked abstractions (OSI model, tech stack). |
| **Venn** | Set overlap (2–3 circles). |
| **pyramid / funnel** | Ranked hierarchy or conversion drop-off. |

**Selection rule:** ask *"would a reader learn more from this than from a well-written paragraph?"* If no, do not draw. Default to deletion over addition. Full per-type rules (canonical layout, anchor coordinates, concrete HTML+SVG scaffolds) live in [type-rules](references/type-rules.md) — load that file only when the chosen type needs its specific scaffold.

## Design system (compact)

Every diagram this skill emits respects these non-negotiables. Full spec with code samples in [design-system](references/design-system.md).

- **Grid.** Every coordinate, width, and gap divisible by **4px**. No shadows anywhere. Max `border-radius: 10px`. Borders are **1px hairline** only.
- **Typography (three families, three roles).** `Instrument Serif` → titles, italic editorial callouts. `Geist Sans` → node names, labels. `Geist Mono` → technical sublabels (ports, URLs, field types, IDs). Mono is for technical content specifically, not a blanket "dev aesthetic." These three families are load-bearing — keep them as-is.
- **Color discipline.** One accent color per diagram. Accent reserved for **1–2 focal nodes** — the things the reader looks at first. Everything else uses `ink`, `muted`, `paper-2`. Target visual density: **4/10** — ruthlessly sparse.
- **Tokens.** Semantic color roles: `paper` (background), `ink` (primary text, borders), `muted` (secondary labels, grid lines), `paper-2` (card fills, lane backgrounds), `accent` (focal nodes — 1–2 per diagram), `accent-fg` (text on accent-colored nodes). Defaults are stone + rust — warm off-white paper, charcoal ink, rust-orange accent. Override via brand onboarding. Concrete default values: `paper: oklch(96% 0.01 80)`, `ink: oklch(25% 0.02 80)`, `accent: oklch(62% 0.19 45)` — full table in [design-system](references/design-system.md).
  > Grid · Typography · Loading the fonts · Type scale · Colour discipline · Rules · Focal node vs standard node · Connection styling · Density calibration · Coordinate-level checklist

## Brand onboarding (60 seconds)

To match the user's existing site:

1. User invokes: `"onboard editorial diagrams to https://<site>"`.
2. This skill routes through `../amw-dev-browser/` (**never** raw WebFetch) to fetch the homepage and serialize the DOM.
3. Extract dominant palette + font stack. Map values to semantic roles — `paper`, `ink`, `muted`, `paper-2`, `accent`, `accent-fg`.
4. Run WCAG AA contrast checks against [color-system](../amw-design-principles/color-system.md). Auto-propose adjustments for failures; never silently ship a failing pair.
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
5. Show a proposed diff to the user; on confirmation, write tokens to [style-guide](references/style-guide.md) (user-editable) inside this skill folder.
  > Semantic color tokens (oklch) · Font stack · Grid + line rules · Brand onboarding flow

**First-run gate.** If the default tokens are still in place on first use in a new project, pause and ask the user: *"Run onboarding, paste tokens manually, or proceed with default (stone + rust)?"* Do not guess.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — upstream orchestrator; route here only when the user has committed to a specific editorial type.
- [color-system](../amw-design-principles/color-system.md) — oklch palette + WCAG AA — extracted tokens must validate against this.
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — type scale and font-stack rules; the three families named above (Instrument Serif / Geist Sans / Geist Mono) are kept exactly as-is from the source skill and are load-bearing for editorial feel.
  > I. Modular type scale · Default recommendation (Perfect Fourth, base = 16px) · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · Successful combinations · Failure modes · VI. Recommended font stacks (avoiding AI slop) · Latin · CJK / other scripts · Banned list (AI slop) · VII. Fallback-stack syntax
- [spacing-rhythm](../amw-design-principles/spacing-rhythm.md) — the 4px grid rule rides on top of this.
  > I. 8pt grid system · Allowed spacing values · T-shirt naming (use tokens) · Forbidden · II. Fibonacci spacing rhythm (large-scale) · III. Vertical rhythm (baseline grid) · Core rule · Result · IV. Hit targets (tappable areas) · V. Alignment · Left vs centered vs justified · Forbidden · VI. Three principles of whitespace · The most important element gets the most whitespace around it · Related elements cluster, unrelated elements separate (Gestalt proximity) · Outer whitespace > inner whitespace · VII. Border radius · Rules · VIII. Shadow system · Rules · IX. Self-check
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — every emitted diagram runs a final check against this file before delivery.
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- [SKILL](../amw-dev-browser/SKILL.md) — the *only* authorized browser-automation primitive; use for brand onboarding instead of WebFetch.
- `../../bin/amw-svg-render.py` — optional render-verify-finish loop when pixel-level inspection of the emitted SVG is needed before handoff.
- [type-rules](references/type-rules.md) — full per-type scaffolds and anchor coordinates for all 13 types.
  > Architecture · Flowchart · Sequence · State machine · ER / data model · Timeline · Swimlane · Quadrant · Nested · Tree · Layer stack · Venn · Pyramid / funnel · Primitives (cross-type) · Annotation callout — italic Instrument Serif + dashed Bézier leader · Sketchy filter — hand-drawn variant
- [design-system](references/design-system.md) — full 4px-grid / typography / color / primitive spec with worked HTML+SVG code.
  > Grid · Typography · Loading the fonts · Type scale · Colour discipline · Rules · Focal node vs standard node · Connection styling · Density calibration · Coordinate-level checklist
- [troubleshooting](references/troubleshooting.md) — symptom-to-fix table (misaligned grid, brand-color mismatch, font loading, contrast failure, too dense, wrong type chosen).
  > Symptom-to-fix table · Diagrams look generic / AI-generated · Colours don't match the user's site · Fonts fall back to Times / Arial · WCAG contrast fails on brand colour · Diagram is too dense / cluttered · Wrong type chosen · `bin/amw-svg-render.py` render check fails · Brand onboarding fetched the wrong palette · Diagram output opens blank · When NOT to use this skill
- [primitive-sketchy](references/primitive-sketchy.md) — cross-type `<feTurbulence>` + `<feDisplacementMap>` filter for hand-drawn essay-style variants, full parameter reference.
  > When to use · Required SVG primitives · Canonical snippet · Parameter reference · 4px grid still applies · Accessibility caveat · Source citation
- [primitive-annotation](references/primitive-annotation.md) — cross-type italic Instrument Serif callout with dashed Bézier leader line for in-margin asides, full geometry spec.
  > When to use · Required SVG primitives · Canonical snippet · Parameter reference · Leader-line geometry · 4px grid still applies · Source citation

## Instructions

1. Identify the diagram type from the user's intent using the 13-type selection table (architecture, ER, flowchart, layers, nested, pyramid, sequence, swimlane, timeline, decision-matrix, metrics, funnel, or dependency).
2. Run the 60-second brand onboarding: extract or confirm primary, secondary, accent, and neutral colors plus typeface; apply these as the editorial design system tokens.
3. Select the relevant TECH reference file(s) from the technique selection tree below and read only the needed file.
4. Author the HTML+SVG diagram following the editorial design system: 4px grid snap, three-family typography, WCAG-AA contrast on every color pair.
5. Render and visually inspect the output with `bin/amw-svg-render.py` or in `dev-browser`; apply AI-slop gate.
6. Export the final artifact and write the job-completion report with all artifact paths.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `diagram-editorial` is the user asking about?
  - **type** (14 techniques)
    - [TECH-type-architecture](./references/TECH-type-architecture.md) — TECH-type-architecture
    - [TECH-type-er](./references/TECH-type-er.md) — TECH-type-er
    - [TECH-type-flowchart](./references/TECH-type-flowchart.md) — TECH-type-flowchart
    - [TECH-type-layers](./references/TECH-type-layers.md) — TECH-type-layers
    - [TECH-type-nested](./references/TECH-type-nested.md) — TECH-type-nested
    - [TECH-type-pyramid](./references/TECH-type-pyramid.md) — TECH-type-pyramid
    - (see `## References` for the remaining 8 in this group)
  - **bezier** (1 techniques)
    - [TECH-bezier-annotation-callout](./references/TECH-bezier-annotation-callout.md) — TECH-bezier-annotation-callout
  - **brand** (1 techniques)
    - [TECH-brand-url-onboarding](./references/TECH-brand-url-onboarding.md) — TECH-brand-url-onboarding
  - **density** (1 techniques)
    - [TECH-density-4-of-10](./references/TECH-density-4-of-10.md) — TECH-density-4-of-10
  - **focal** (1 techniques)
    - [TECH-focal-accent-discipline](./references/TECH-focal-accent-discipline.md) — TECH-focal-accent-discipline
  - **four** (1 techniques)
    - [TECH-four-px-grid-snap](./references/TECH-four-px-grid-snap.md) — TECH-four-px-grid-snap
  - **sketchy** (1 techniques)
    - [TECH-sketchy-fractal-filter](./references/TECH-sketchy-fractal-filter.md) — TECH-sketchy-fractal-filter
  - **three** (1 techniques)
    - [TECH-three-family-typography](./references/TECH-three-family-typography.md) — TECH-three-family-typography
  - **wcag** (1 techniques)
    - [TECH-wcag-contrast-validation](./references/TECH-wcag-contrast-validation.md) — TECH-wcag-contrast-validation

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-bezier-annotation-callout.md](./references/TECH-bezier-annotation-callout.md)**
  - Description: TECH-bezier-annotation-callout
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-brand-url-onboarding.md](./references/TECH-brand-url-onboarding.md)**
  - Description: TECH-brand-url-onboarding
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-density-4-of-10.md](./references/TECH-density-4-of-10.md)**
  - Description: TECH-density-4-of-10
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-focal-accent-discipline.md](./references/TECH-focal-accent-discipline.md)**
  - Description: TECH-focal-accent-discipline
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-four-px-grid-snap.md](./references/TECH-four-px-grid-snap.md)**
  - Description: TECH-four-px-grid-snap
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-sketchy-fractal-filter.md](./references/TECH-sketchy-fractal-filter.md)**
  - Description: TECH-sketchy-fractal-filter
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Browser-support caveat
    - Cross-references
- **[./references/TECH-three-family-typography.md](./references/TECH-three-family-typography.md)**
  - Description: TECH-three-family-typography
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Minimal `<head>` snippet
    - Cross-references
- **[./references/TECH-type-architecture.md](./references/TECH-type-architecture.md)**
  - Description: TECH-type-architecture
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-er.md](./references/TECH-type-er.md)**
  - Description: TECH-type-er
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-flowchart.md](./references/TECH-type-flowchart.md)**
  - Description: TECH-type-flowchart
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-layers.md](./references/TECH-type-layers.md)**
  - Description: TECH-type-layers
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-nested.md](./references/TECH-type-nested.md)**
  - Description: TECH-type-nested
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-pyramid.md](./references/TECH-type-pyramid.md)**
  - Description: TECH-type-pyramid
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-quadrant.md](./references/TECH-type-quadrant.md)**
  - Description: TECH-type-quadrant
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-selection-rule.md](./references/TECH-type-selection-rule.md)**
  - Description: TECH-type-selection-rule
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-sequence.md](./references/TECH-type-sequence.md)**
  - Description: TECH-type-sequence
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-state-machine.md](./references/TECH-type-state-machine.md)**
  - Description: TECH-type-state-machine
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-swimlane.md](./references/TECH-type-swimlane.md)**
  - Description: TECH-type-swimlane
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-timeline.md](./references/TECH-type-timeline.md)**
  - Description: TECH-type-timeline
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-tree.md](./references/TECH-type-tree.md)**
  - Description: TECH-type-tree
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-type-venn.md](./references/TECH-type-venn.md)**
  - Description: TECH-type-venn
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-wcag-contrast-validation.md](./references/TECH-wcag-contrast-validation.md)**
  - Description: TECH-wcag-contrast-validation
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
- At least one `TECH-*.md` file from `skills/amw-diagram-editorial/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. editorial-quality HTML + SVG diagram files). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` or `./design/mockups/` created fresh)
   - Last-resort scratch: `/tmp/amw-diagram-editorial-<slug>/`

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

- **Output is self-contained HTML.** Inline `<style>` + inline `<svg>` in a single `.html` file. No external CDN assets except optional Google Fonts / Bunny Fonts `<link>` (offline-tolerant fallback to system fonts). Bunny Fonts is a GDPR-friendly Google Fonts mirror at `fonts.bunny.net`; canonical inline form: `<link rel="stylesheet" href="https://fonts.bunny.net/css?family=geist:400,600|instrument-serif:400i">`.
- **No AI-drawn illustrations.** Structural diagram primitives only — rectangles, lines, circles, arrows, text. Never generate portraits, scenes, mascots, or decorative SVG art; that is explicitly banned by `ai-slop-avoid.md`.
- **Every coordinate divisible by 4.** Misaligned grids are the AI-generated tell. Enforce even for sketch filters.
- **One accent color, 1–2 focal nodes.** If everything is accent, nothing is accent. Pick the node the reader should look at first, and leave the rest on `paper-2` + `ink`.
- **Delete nodes until it hurts, then delete one more.** Target density is 4/10. Twelve-plus nodes means split into two diagrams or switch to a nested / layers type.
- **Brand onboarding flows through `dev-browser`, not raw WebFetch.** Any URL-reading step in this skill must use `../amw-dev-browser/`.
- **oklch colors, WCAG AA.** All palette changes go through [color-system](../amw-design-principles/color-system.md) validation. Do not hard-code hex without oklch equivalents in the token file.
  > I. Always prefer oklch over rgb / hex / hsl · Why · Syntax · Comfort ranges · II. WCAG contrast — hard requirement · Checking tools · III. Palette structure (cap at 5–7 colors) · Standard 6-color framework · Rules · IV. Dark mode is not a simple inversion · Wrong approach · Right approach · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- **This skill does not substitute for `../amw-diagram-svg/`, `../amw-diagram-architecture/`, or `../amw-svg-creator/`.** If the user wants a freeform shape, an architecture graph, or an icon, route back to `design-principles` and let it pick.

## Error Handling

| Symptom | Likely cause | Fix |
|---|---|---|
| Diagram looks "AI-generated" / generic | Coordinates not on 4px grid, or too many accent nodes | Re-snap every x/y/width/gap to a multiple of 4; drop accent on all but 1–2 focal nodes; see [troubleshooting](references/troubleshooting.md). |
> [troubleshooting.md] Symptom-to-fix table · Diagrams look generic / AI-generated · Colours don't match the user's site · Fonts fall back to Times / Arial · WCAG contrast fails on brand colour · Diagram is too dense / cluttered · Wrong type chosen · `bin/amw-svg-render.py` render check fails · Brand onboarding fetched the wrong palette · Diagram output opens blank · When NOT to use this skill
| Colours don't match the user's site | Brand onboarding never ran, or tokens are still defaults | Re-run onboarding through `../amw-dev-browser/`, or have the user paste hex values into [style-guide](references/style-guide.md). |
> [style-guide.md] Semantic color tokens (oklch) · Font stack · Grid + line rules · Brand onboarding flow
| Fonts fall back to Times/Arial | Google Fonts / Bunny Fonts `<link>` missing from `<head>` | Add the Bunny Fonts `<link>` shown in [troubleshooting](references/troubleshooting.md); fallbacks to system fonts are expected but degrade the editorial look. |
> [troubleshooting.md] Symptom-to-fix table · Diagrams look generic / AI-generated · Colours don't match the user's site · Fonts fall back to Times / Arial · WCAG contrast fails on brand colour · Diagram is too dense / cluttered · Wrong type chosen · `bin/amw-svg-render.py` render check fails · Brand onboarding fetched the wrong palette · Diagram output opens blank · When NOT to use this skill
| WCAG contrast fails on brand color | Onboarding couldn't find a 4.5:1 pair at 12px | Darken `ink` or lighten `paper` until ratio ≥ 4.5:1; onboarding auto-proposes; never ship a failing pair. |
| Diagram is cluttered / too dense | Node count above ~8, density above 6/10 | Delete non-essential nodes; split into overview + detail; switch to `nested` or `layer stack` if the intent is hierarchy. |
| Wrong type was chosen | User's intent maps better to a different type | Ask the user to override explicitly (*"Make this a swimlane, not a flowchart — rows for Design, Eng, PM"*); do not silently switch. |
| User wants ASCII/unicode terminal diagram | Intent belongs elsewhere | Route to `../amw-ascii-sketch/` or a wiretext tool; this skill only emits HTML+SVG. |
| User wants before/after comparison | Intent is tabular, not diagrammatic | Route back to `design-principles`; a table beats a diagram for comparisons. |

See [troubleshooting](references/troubleshooting.md) for the full symptom-to-fix list and the "when NOT to use this skill" section.
> [troubleshooting.md] Symptom-to-fix table · Diagrams look generic / AI-generated · Colours don't match the user's site · Fonts fall back to Times / Arial · WCAG contrast fails on brand colour · Diagram is too dense / cluttered · Wrong type chosen · `bin/amw-svg-render.py` render check fails · Brand onboarding fetched the wrong palette · Diagram output opens blank · When NOT to use this skill
