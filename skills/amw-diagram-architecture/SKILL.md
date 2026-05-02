---
name: amw-diagram-architecture
description: Convert a free-text system description into a clean, visually-balanced, layered architecture diagram in a user-selectable format (graph JSON for canvas renderers, SVG for browsers, or PNG for sharing). Triggers on "draw my architecture", "architecture diagram for X", "map out my system as a layered diagram", "export this architecture as SVG/PNG", "component diagram of this backend". Do NOT trigger on generic "design", "draw me a picture", "sketch the UI", "make a flowchart of the onboarding funnel" — those are design-principles or diagram-editorial territory. For Mermaid output, route through `amw-mermaid-diagram` instead — this skill does NOT emit Mermaid (one-renderer rule). Use when converting a free-text system description into a layered architecture diagram. Trigger with /amw-create-or-modify-svg-diagram.
version: 0.2.0
---

# Diagram Architecture

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> This skill is an executor. Triggers are architecture-diagram-specific only.

## Overview

Converts a free-text system description into a clean, visually-balanced, layered architecture diagram. Supports three output formats: canvas-renderable graph JSON, SVG (browser-renderable), and PNG (SVG + export instructions). Visual quality is a first-class constraint — 3–5 layers, 6–12 nodes. Includes opt-in on-disk versioning for iterative refinement.

## Activation

Callable directly via the `/amw-create-or-modify-svg-diagram` command (user shortcut — fast path for architecture diagram creation), or invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode. In Main-agent mode the orchestrator may apply layering, node-reduction, and multi-format export techniques from this skill beyond what the command exposes.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT (Phase B). Structural architecture diagrammer — transforms a free-text system description into a single layered diagram rendered in the caller's chosen format. One graph, three surfaces: canvas-renderable graph JSON, SVG, or PNG (SVG + export instructions). Visual quality is a first-class constraint: 3–5 layers, 6–12 nodes, balanced layouts, bounded edges — a clean 8-node diagram always beats a cluttered 18-node one.

**Mermaid output is intentionally NOT emitted by this skill.** Per CLAUDE.md's one-renderer rule, all Mermaid generation routes through `../amw-mermaid-diagram/SKILL.md` (source authoring, 9 grammars) and `../amw-mermaid-render/SKILL.md` (rendering to SVG/ASCII). When Mermaid output is requested, this skill produces graph JSON; hand the JSON to `amw-mermaid-diagram` to emit Mermaid source.

## Trigger conditions

Fires on these specific phrasings:

- "draw my architecture", "draw the system architecture"
- "architecture diagram for <system>", "map out my system as an architecture diagram"
- "generate a layered diagram of <system>", "component diagram of <backend>"
- "render this architecture as SVG", "export the architecture as PNG"
- "structure this system into layers", "visualise the system as a layered graph"
- free-text paste of a technical system accompanied by an explicit visualisation request

Do NOT fire on:

- generic "design X", "draw X", "sketch the UI", "make the landing page look good" — `design-principles` owns these
- editorial infographic requests (timeline, comparison table, dense narrative graphic) — those are `diagram-editorial` / `infographics`
- freeform / non-layered SVG diagrams (icons, illustrations, single-component figures) — that is `diagram-svg`
- user-flow / UX journey charts — those are `ux-flows`
- "convert this ASCII diagram to SVG" — the ASCII-input path is `ascii-to-svg`; that skill may route to this one when the ASCII subject is architectural

## Prerequisites

- **runtime_binaries (system):** none — the pipeline is pure text-to-diagram, driven by an LLM call
- **API access:** Claude (a capable modern Sonnet or Opus model — e.g. `claude-sonnet-4-6` or newer Opus) for the graph-generation LLM call. When running inside Claude.ai or Claude Code, the platform supplies authentication; embedded or standalone callers must supply their own `ANTHROPIC_API_KEY`.
- **Optional downstream:** `../../bin/amw-svg-render.py` for the render-verify-finish loop when the output path is SVG or PNG — rasterises the generated SVG so the caller can eyeball layout before delivery.

## Interface

```
Input:
  description    (string, required)   — free-text system description
  output_format  (string, optional)   — "graph" | "svg" | "png"
                                        Default: "graph"

Output:
  "graph"    → JSON object  { title, subtitle, layers, nodes, edges }
  "svg"      → SVG string  (self-contained, browser-renderable, ~820px wide)
  "png"      → Same SVG + appended PNG export instructions block

For Mermaid output: produce "graph" then route the JSON through
`../amw-mermaid-diagram/SKILL.md` (one-renderer rule).
```

The output is the diagram. No prose wrapper, no explanation, unless the caller explicitly asks for one.

## Core pipeline

1. **Graph generation** — call the LLM with the verbatim system prompt in [prompts](references/prompts.md) (assistant prefill `{` to force JSON-first output). The prompt encodes the 3–5-layer, 6–12-node, ≤ floor(n × 0.8) edge rules and the five-layer color palette. The JSON response is parsed (and repaired if needed via the recipe in `prompts.md`) to produce the internal graph — the single source of truth for all formats.
2. **Stage 1 validation** — run every check in [validation](references/validation.md) § Stage 1 on the raw graph: layer count (2–6 hard, 3–5 preferred), node count (4–14 hard, 8–10 preferred), balanced layout (≤ 5 nodes per layer), label/description quality, edge integrity (no danglers, no self-loops, no reverse duplicates, edge budget enforced), ID integrity, layer-order sequence. Apply every listed fix inline. If re-generation is required (too few layers or nodes), discard and repeat step 1.
3. **Format transformation** — run the transform matching `output_format`, per [formats](references/formats.md):
   - `graph` → return the validated JSON as-is
   - `svg` → run the layout algorithm (820px canvas, 160×64 node cards, centred per-layer rows, cubic-bezier downward edges, defs/grid/arrow marker, accent bars, title block)
   - `png` → same SVG + the standard five-line PNG-export instructions block appended after `</svg>`
4. **Stage 2 validation** — run the format-specific checks in [validation](references/validation.md) § Stage 2: SVG well-formedness (`<svg>` root + `<defs>` + arrow marker + no unescaped `&` / `<` in text), SVG layout sanity (node count, layer band count, no overflow, no overlap, edges drawn before nodes), PNG (SVG checks + instructions appended after SVG, never before). Apply every listed fix. If any SVG layout-sanity check fails, discard and re-run step 3 from the validated graph.
5. **Return** — return the output. No prose wrapper.

## Versioning (optional, opt-in)

For users iterating on an architecture diagram across a long session (adding services, swapping the data layer, pulling a component out of a layer, etc.), this skill supports an **opt-in on-disk versioning layout** so each revision is preserved and can be compared or rolled back. The feature is dormant by default — it activates only when the caller uses one of the versioned-trigger forms below, or explicitly passes an output directory.

### Opt-in triggers

- "save this as v1" / "save the current architecture as a new version"
- "show me v2 of the <name> diagram"
- "rollback <name> to v3"
- "diff v2 and v4 of <name>"
- "list versions of <name>"

### Storage layout (per user working directory)

```
claude-diagrams/
└── <kebab-name>/
    ├── current.yaml     Canonical active version (copy of the latest vN.yaml)
    ├── v1.yaml          First saved graph (validated, post-Stage 1)
    ├── v2.yaml          Second saved graph
    ├── ...
    └── history.yaml     Log of { version, timestamp, description, author }
```

### YAML shape (canonical graph + meta)

The YAML that gets persisted is the validated internal graph (same structure the skill uses in step 2 of the core pipeline — layers, nodes, edges) plus a `meta` block:

```yaml
meta:
  name: "System architecture"
  type: architecture               # architecture | sequence | flowchart | erd
  created: 2026-04-22T10:00:00+02:00
  version: 3
  description: "Added Redis cache between gateway and services"

layers:
  - id: layer-1
    label: Frontend
  # ...

nodes:
  - id: client
    label: "Web Client"
    layer: layer-1
    description: "Browser-based SPA"
  # ...

edges:
  - from: client
    to: gateway
    label: "HTTPS"
  # ...
```

This is a superset of the in-memory graph — the `meta` block adds versioning metadata; `layers`, `nodes`, `edges` are the validated graph unchanged.

### Rendering saved versions to ASCII

When the user asks to view a specific version (`show me v2 of the payment-flow diagram`), the flow is:

1. Load `claude-diagrams/<name>/v2.yaml`.
2. Convert the layered-graph into `bin/amw-ascii-render.py` input (the `layers` JSON mode is the structural match for architecture diagrams; the `diagram` mode is used for flowchart/ERD; `sequence` for sequence diagrams).
3. Pipe to `bin/amw-ascii-render.py` and return the ASCII preview.

ASCII preview is the default viewing format for a saved version because it is token-cheap and fits inline in chat. SVG / PNG are still available by re-running step 3 of the core pipeline on the loaded graph — same output formats, same validations.

### Versioning operations (conversational, not slash-command)

| User says | Skill does |
|---|---|
| "save this as a new version" | Increment version number in `history.yaml`; write `vN.yaml`; update `current.yaml`. |
| "show me v2 of <name>" | Load `vN.yaml`; render via `bin/amw-ascii-render.py` (layers/diagram/sequence mode). |
| "rollback <name> to v2" | Copy `v2.yaml` over `current.yaml`; do NOT delete v3/v4 — rollback is a new version, not a destructive revert. Log a new entry in `history.yaml` noting the rollback source. |
| "diff v2 and v4" | Load both YAMLs; report layer/node/edge additions, removals, and label changes as a structured list (not a textual unified diff — graphs don't diff well as text). |
| "list versions of <name>" | Read `history.yaml`; print a one-line-per-version table (version, timestamp, description). |
| "open <name>" | Load `claude-diagrams/<name>/current.yaml`; render via ASCII as the quick view; prompt for next action. |

The versioning layer is a thin wrapper — it does NOT bypass Stage 1 / Stage 2 validation. Every saved version must pass validation before persistence; a graph that fails validation is never committed to disk.

### Conversational edits (mini-DSL for editing saved diagrams)

When the user has loaded a saved YAML diagram (`open <name>` or `show me v2`),
they can mutate it with natural-language edits instead of re-authoring the
whole system description. This is a **mini-DSL** — a small fixed vocabulary of
NL → graph-operation mappings. After each edit, the skill re-runs Stage 1
validation, bumps the version via the versioning flow above, and renders the
new ASCII preview inline. This is the conversational companion to the YAML
versioning layout — they share one storage substrate.

Source: ported and translated from the diagram-skill-main source (originally
Spanish — "Agrega un servicio de cache", etc.). Translated to English below.

| User says | Skill does |
|---|---|
| "add a cache service" / "add a Redis cache between frontend and auth" | Add one `service`-type node; if a position hint is given ("between X and Y"), insert it on that edge (split the X→Y edge into X→new and new→Y). |
| "remove service X" / "delete the X component" | Remove node X and every edge with `source == X` or `target == X`. |
| "connect X to Y" / "link X with Y" | Create a new edge `{source: X, target: Y}`. If an edge already exists, no-op. |
| "move X before Y" / "move X into the Frontend layer" | Re-assign `node.layerId` for X; re-run Stage 1.3 (layer balance). |
| "group these into Backend" / "wrap X, Y, Z in a new layer called Backend" | Create a new layer with the given label; move the listed nodes into it. |
| "rename X to Z" | Update `node.label` for X (keep `node.id` stable so edges don't break); re-run Stage 1.4 (label quality). |
| "label the edge X→Y as 'HTTPS'" | Set `edge.label` for the matching edge. |
| "disconnect X from Y" | Remove the edge `{source: X, target: Y}` only — leaves nodes in place. |
| "save this" / "commit this version" | Persist via the versioning flow above — increment `vN.yaml`, update `current.yaml`, append to `history.yaml`. |

**Rules for the mini-DSL:**

- **No edit bypasses validation.** After every NL edit, re-run Stage 1 on the
  mutated graph. If the edit violates a hard constraint (e.g. would empty a
  layer, or push node count past 14), reject the edit and tell the user which
  rule was violated — do not silently patch.
- **IDs are stable; labels are free.** A rename updates `node.label`, never
  `node.id`. This keeps the edges intact across edits.
- **The YAML is the source of truth between edits.** After each confirmed
  edit, the new graph is persisted via the versioning flow — there is no
  in-memory-only "dirty" state that can be lost to a crash or a context reset.
- **Ambiguous edits require clarification.** "move X" with no destination,
  "connect these" with no explicit node pair, "remove the red one" — the skill
  asks one clarifying question rather than guess.

### When NOT to use versioning

- **Single-shot requests.** "Draw the architecture of X as SVG" — no versioning, no disk writes, just the SVG.
- **Claude.ai sandboxed environments without filesystem write access.** The skill degrades gracefully: version operations become in-memory-only for the session, and the caller is told that versions will not persist.
- **Large teams with shared architecture repos.** The on-disk layout is per-user-working-directory by design; it is not a substitute for a shared ADR / diagrams repo. Tell the user to commit `claude-diagrams/<name>/` to their own repo if they want persistence beyond the session.

(This versioning feature subsumes the scope of the upstream read-only `diagram-skill-main` source, which produced ASCII-previewed versioned architecture / flowchart / sequence / ERD diagrams on disk. That source's slash-command surface — `/diagram new`, `/diagram history`, `/diagram rollback` — is intentionally NOT reimplemented as slash commands in this plugin; the conversational triggers above replace them. The plugin reserves the `/amw-*` namespace for capabilities that cannot be invoked via natural-language intent alone.)

## Instructions

1. Call the LLM with the system prompt from [prompts](references/prompts.md) (assistant prefill `{` to force JSON output) to generate the graph; enforce 3–5 layers, 6–12 nodes, and the edge budget rule.
2. Run Stage 1 validation per [validation](references/validation.md): check layer count, node count, balanced layout, label quality, edge integrity, and ID integrity; apply all listed fixes inline.
3. Select the output format (`graph`, `svg`, or `png`) and run the matching format transformation from [formats](references/formats.md).
4. Run Stage 2 validation (format-specific checks); fix any SVG well-formedness or layout-sanity issues; if re-generation is required, discard and repeat from step 1.
5. If versioning is enabled, write the output and update `history.yaml` with the new version entry.
6. Return the output without a prose wrapper; report artifact paths.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `diagram-architecture` is the user asking about?
  - **arrow** (1 techniques)
    - [TECH-arrow-vocabulary](./references/TECH-arrow-vocabulary.md) — 6-type connection taxonomy
  - **assistant** (1 techniques)
    - [TECH-assistant-prefill-json](./references/TECH-assistant-prefill-json.md) — TECH-assistant-prefill-json
  - **edge** (1 techniques)
    - [TECH-edge-budget-rule](./references/TECH-edge-budget-rule.md) — TECH-edge-budget-rule
  - **export** (1 techniques)
    - [TECH-export-mermaid-plantuml-d2](./references/TECH-export-mermaid-plantuml-d2.md) — one YAML, four output formats
  - **graph** (1 techniques)
    - [TECH-graph-json-schema](./references/TECH-graph-json-schema.md) — TECH-graph-json-schema
  - **json** (1 techniques)
    - [TECH-json-repair-recipe](./references/TECH-json-repair-recipe.md) — TECH-json-repair-recipe
  - **layer** (1 techniques)
    - [TECH-layer-palette-5-colors](./references/TECH-layer-palette-5-colors.md) — TECH-layer-palette-5-colors
  - **png** (1 techniques)
    - [TECH-png-export-bridge](./references/TECH-png-export-bridge.md) — TECH-png-export-bridge
  - **stage1** (1 techniques)
    - [TECH-stage1-graph-validation](./references/TECH-stage1-graph-validation.md) — TECH-stage1-graph-validation
  - **style** (1 techniques)
    - [TECH-style-presets](./references/TECH-style-presets.md) — `detallado` / `unicode` / `clasico` / `compacto`
  - **svg** (1 techniques)
    - [TECH-svg-layered-layout](./references/TECH-svg-layered-layout.md) — TECH-svg-layered-layout
  - **version** (1 techniques)
    - [TECH-version-history-yaml](./references/TECH-version-history-yaml.md) — v1 / v2 / ... + history.yaml + rollback
  - **yaml** (1 techniques)
    - [TECH-yaml-canonical-schema](./references/TECH-yaml-canonical-schema.md) — `meta / nodes / edges / groups / notes`

## Examples

See the worked examples in the per-mode sub-sections above and in [examples](references/examples.md).

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-arrow-vocabulary.md](./references/TECH-arrow-vocabulary.md)**
  - Description: 6-type connection taxonomy
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-assistant-prefill-json.md](./references/TECH-assistant-prefill-json.md)**
  - Description: TECH-assistant-prefill-json
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-edge-budget-rule.md](./references/TECH-edge-budget-rule.md)**
  - Description: TECH-edge-budget-rule
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-graph-json-schema.md](./references/TECH-graph-json-schema.md)**
  - Description: TECH-graph-json-schema
  - TOC:
    - What it does
    - When to use
    - How it works
    - Constraints
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-json-repair-recipe.md](./references/TECH-json-repair-recipe.md)**
  - Description: TECH-json-repair-recipe
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-layer-palette-5-colors.md](./references/TECH-layer-palette-5-colors.md)**
  - Description: TECH-layer-palette-5-colors
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-png-export-bridge.md](./references/TECH-png-export-bridge.md)**
  - Description: TECH-png-export-bridge
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-stage1-graph-validation.md](./references/TECH-stage1-graph-validation.md)**
  - Description: TECH-stage1-graph-validation
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-style-presets.md](./references/TECH-style-presets.md)**
  - Description: `detallado` / `unicode` / `clasico` / `compacto`
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-svg-layered-layout.md](./references/TECH-svg-layered-layout.md)**
  - Description: TECH-svg-layered-layout
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-version-history-yaml.md](./references/TECH-version-history-yaml.md)**
  - Description: v1 / v2 / ... + history.yaml + rollback
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-yaml-canonical-schema.md](./references/TECH-yaml-canonical-schema.md)**
  - Description: `meta / nodes / edges / groups / notes`
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-diagram-architecture/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per `../amw-design-principles/ai-slop-avoid.md` (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. graph JSON / layered SVG / PNG export). The output path is determined by **project inference**, NOT hardcoded. See [`../amw-design-principles/references/project-output-routing.md`](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-diagram-architecture-<slug>/`

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

## Resources

- `../amw-design-principles/color-system.md` — when emitting SVG palettes, prefer mapping the five-layer hex palette into oklch for print/contrast parity with the rest of the plugin's output surface
- `../amw-design-principles/typography-system.md` — node label and description legibility must respect the minimum-font thresholds (desktop body ≥ 16px, slides ≥ 24px) when the SVG is scaled for presentation
- `../../bin/amw-svg-render.py` — visual-verify loop for the SVG / PNG output paths; renders the generated SVG so the caller can confirm layout before delivery
- `../../bin/amw-ascii-render.py` — perfect-ASCII renderer; used by the versioning layer to preview saved versions inline in chat (layers / diagram / sequence JSON modes)
- `../amw-ascii-validator/SKILL.md` — owns the ASCII render + validate contract; the versioning layer consumes `bin/amw-ascii-render.py` via the interface documented there
- `../amw-diagram-editorial/SKILL.md` — route here when the request is editorial-infographic-style rather than architecture-layered (timelines, comparison tables, dense narrative)
- `../amw-diagram-svg/SKILL.md` — route here for freeform, non-layered, single-figure SVGs (icons, illustrations, custom diagrams)
- `../amw-ascii-to-svg/SKILL.md` — receives routing when the user pastes an ASCII architecture sketch; that skill may defer here when the subject is a layered architecture rather than a freeform figure
- `../amw-ux-flows/SKILL.md` — the sibling for user-journey / task-flow / onboarding-funnel charts (not architecture)
- `/amw-ascii-to-svg` — the user-facing slash command that routes here when the pasted ASCII is architectural in nature
- [prompts](references/prompts.md) — verbatim LLM system prompt, API call pattern, and JSON-repair recipe
- [validation](references/validation.md) — Stage 1 (graph) and Stage 2 (format) validation checks and fixes
- [formats](references/formats.md) — transform specifications for all four output formats, plus SVG layout constants and height formula
- [examples](references/examples.md) — a fully worked SaaS-analytics-platform example rendered across all four formats

## Non-negotiables

- **Never exceed the layer/node budgets.** 3–5 layers, 6–12 nodes. Visual quality over completeness — merge, drop, or simplify minor components rather than overflow a layer or crowd the canvas.
- **Layers are the spine.** Every diagram is top-down, strictly layered; nodes connect within their layer's slot first, then across layers.
- **Edges signal flow, not exhaustion.** Maximum edges = `floor(nodeCount × 0.8)`. Draw only primary data or control flow; drop the rest.
- **Model freshness.** Use a capable modern Claude Sonnet or Opus (e.g. `claude-sonnet-4-6` or newer). NEVER pin the legacy dated Sonnet-4 snapshot from the 2025-05 series — that snapshot is outdated and scheduled for retirement. Update the model string in [prompts](references/prompts.md) whenever Anthropic ships a newer production model.
- **No prose wrapper by default.** The output IS the diagram. Add narration only when the caller explicitly asks for it.
- **Palette coherence.** Five non-adjacent-hue anchors form the canonical identity of this diagram family — each layer gets a distinct hue band so layers remain distinguishable at a glance. Use the oklch values as the primary spec; hex fallbacks are provided for legacy tooling only:
  - Layer 1 — frontend: `oklch(30% 0.04 260)` / hex `#3B4252` (slate-ink)
  - Layer 2 — gateway / orchestration: `oklch(62% 0.16 45)` / hex `#C87341` (rust-accent)
  - Layer 3 — logic / services / agents: `oklch(65% 0.13 190)` / hex `#4FA9A3` (teal-accent)
  - Layer 4 — tools / integrations: `oklch(78% 0.14 85)` / hex `#D9A441` (amber-accent)
  - Layer 5 — data / storage: `oklch(60% 0.09 140)` / hex `#6E9B6A` (sage-accent)
  The previous indigo-purple defaults (`#6366F1` / `#8B5CF6`) were retired because they sit in the "purple-blue gradient" band flagged by `../amw-design-principles/ai-slop-avoid.md` item #1. Substituting tokens from `../amw-design-principles/color-system.md` is permitted only when the caller has supplied an explicit design-token override; silent recoloring breaks cross-diagram recognisability.
- **Validation is mandatory, not advisory.** Every Stage 1 and Stage 2 check must pass before return. Surfacing an error to the caller is the last resort — apply the listed fixes first, regenerate if the triggers fire.

## Error Handling

- **Overloaded layer (> 5 nodes after generation)** — Stage 1.3 fix: move the least-essential node to an adjacent layer; if every adjacent layer is also full, re-run generation with an explicit merge instruction.
- **Too-few or too-many layers/nodes** — re-run generation. The skill does not silently stretch (too few) or truncate (too many) — it regenerates. Patching these conditions produces visually incoherent diagrams.
- **SVG text overflow** — a label longer than `NODE_W = 160px` at 13pt wraps visually ugly. Stage 1.4 fix: truncate to 3 title-case words. If that still overflows, re-run generation and ask the model for a shorter label.
- **Model timeout / parse failure** — the LLM returned prose instead of JSON, or the JSON is malformed. Apply the `repairAndParse` recipe from [prompts](references/prompts.md) in order (strip fences → extract outermost braces → strip trailing commas → normalise newlines in string values). If both attempts fail, re-run generation once; on a second failure, surface the raw parse error to the caller rather than fabricate a graph.
- **Auth missing** (embedded / standalone callers only) — `ANTHROPIC_API_KEY` is not set; surface the error immediately, do not retry. Inside Claude.ai / Claude Code, the platform handles auth — this failure mode does not apply.
- **Empty / too-abstract description** — the caller gave one sentence or a single noun. The prompt explicitly says "infer a clean canonical architecture — do not ask"; the model produces a best-effort default. If the result feels wrong, the caller should re-invoke with more specifics rather than iterate inside this skill.
