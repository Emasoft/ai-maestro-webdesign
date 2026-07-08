---
name: amw-diagram-architecture
description: Convert a free-text system description into a layered architecture diagram (graph JSON, SVG, or PNG). Triggers on "draw my architecture", "architecture diagram for X", "layered diagram", "export architecture as SVG/PNG", "component diagram". Does NOT trigger on "design", "sketch the UI" — routes to design-principles / diagram-editorial. For Mermaid, use `amw-mermaid-diagram`. Use when converting a system description into a layered diagram. Trigger with /amw-create-or-modify-svg-diagram.
---

# Diagram Architecture

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). Executor skill — architecture-diagram-specific triggers only.

## Overview

Converts a free-text system description into a clean, visually-balanced, layered architecture diagram. Three output formats: canvas-renderable graph JSON, SVG (browser-renderable), and PNG (SVG + export instructions). Visual quality is a first-class constraint — 3–5 layers, 6–12 nodes. Includes opt-in on-disk versioning for iterative refinement.

## Activation

Callable directly via the `/amw-create-or-modify-svg-diagram` command (user shortcut — fast path for architecture diagram creation), or invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode. The skill is **autonomous and self-contained** — any agent can use it by reading this SKILL.md and its references; the techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT (Phase B). Structural architecture diagrammer — transforms a free-text system description into a single layered diagram rendered in the caller's chosen format. One graph, three surfaces: canvas-renderable graph JSON, SVG, or PNG (SVG + export instructions). Visual quality is a first-class constraint: 3–5 layers, 6–12 nodes, balanced layouts, bounded edges — a clean 8-node diagram always beats a cluttered 18-node one.

**Mermaid output is intentionally NOT emitted by this skill.** Per CLAUDE.md's one-renderer rule, all Mermaid generation routes through [SKILL](../amw-mermaid-diagram/SKILL.md) (source authoring, 9 grammars) and [SKILL](../amw-mermaid-render/SKILL.md) (rendering to SVG/ASCII). When Mermaid output is requested, this skill produces graph JSON; hand the JSON to `amw-mermaid-diagram` to emit Mermaid source.

## Trigger conditions

Fires on architecture-specific phrasings: "draw my architecture", "architecture diagram for <system>", "generate a layered diagram of <system>", "component diagram of <backend>", "render this architecture as SVG", "export the architecture as PNG", "structure this system into layers", "visualise the system as a layered graph", or a free-text paste of a technical system accompanied by an explicit visualisation request.

Do NOT fire on: generic "design X" / "sketch the UI" (→ `design-principles`); editorial infographic requests (→ `diagram-editorial` / `infographics`); freeform / non-layered SVGs (→ `diagram-svg`); user-flow / UX journey charts (→ `ux-flows`); "convert this ASCII diagram to SVG" (→ `ascii-to-svg`, which may route back here when the subject is architectural).

## Prerequisites

- **runtime_binaries (system):** none — the pipeline is pure text-to-diagram, driven by an LLM call.
- **API access:** Claude (a capable modern Sonnet or Opus model — e.g. `claude-sonnet-4-6` or newer Opus) for the graph-generation LLM call. When running inside Claude.ai or Claude Code, the platform supplies authentication; embedded or standalone callers must supply their own `ANTHROPIC_API_KEY`.
- **Optional downstream:** `../../bin/amw-svg-render.py` for the render-verify-finish loop when the output path is SVG or PNG.

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

1. **Graph generation** — call the LLM with the verbatim system prompt in [prompts](references/prompts.md) (assistant prefill `{` to force JSON-first output). The prompt encodes the 3–5-layer, 6–12-node, ≤ floor(n × 0.8) edge rules and the five-layer color palette. Parse and repair if needed via the recipe in prompts.md.
> [prompts.md] System Prompt · API Call Pattern · JSON Repair
2. **Stage 1 validation** — run every check in [validation](references/validation.md) § Stage 1 on the raw graph (layer count, node count, balanced layout, label/description quality, edge integrity, ID integrity, layer-order sequence). Apply every listed fix inline. If re-generation is required, discard and repeat step 1.
> [validation.md] Stage 1 — Graph Validation (all formats) · Stage 2 — Format Validation · Validation Summary (quick reference)
3. **Format transformation** — run the transform matching `output_format`, per [formats](references/formats.md): `graph` returns the validated JSON; `svg` runs the layout algorithm (820px canvas, 160×64 node cards, centred per-layer rows, cubic-bezier downward edges); `png` appends the five-line PNG-export instructions block after `</svg>`.
> [formats.md] Format 1: `graph` (default) · Format 2: `mermaid` · Format 3: `svg` · Format 4: `png`
4. **Stage 2 validation** — run the format-specific checks in [validation](references/validation.md) § Stage 2 (SVG well-formedness, layout sanity, PNG instructions order). Apply every listed fix. If any check fails, discard and re-run step 3 from the validated graph.
> [validation.md] Stage 1 — Graph Validation (all formats) · Stage 2 — Format Validation · Validation Summary (quick reference)
5. **Return** — return the output. No prose wrapper.

## Versioning (optional, opt-in)

For users iterating on an architecture diagram across a long session, this skill supports an **opt-in on-disk versioning layout** so each revision is preserved and can be compared or rolled back. The feature is dormant by default — it activates only when the caller uses one of the versioned-trigger forms, or explicitly passes an output directory.

See **[versioning](references/versioning.md)** for the full opt-in triggers, storage layout (`claude-diagrams/<name>/v1.yaml` + `history.yaml`), YAML schema, conversational versioning operations (save, show, rollback, diff, list), the conversational mini-DSL for natural-language edits (add/remove/connect/move/rename), and when NOT to use versioning.
> [versioning.md] Opt-in triggers · Storage layout (per user working directory) · YAML shape (canonical graph + meta) · Rendering saved versions to ASCII · Versioning operations (conversational, not slash-command) · Conversational edits (mini-DSL for editing saved diagrams) · When NOT to use versioning

## Instructions

1. Call the LLM with the system prompt from [prompts](references/prompts.md) (assistant prefill `{` to force JSON output) to generate the graph; enforce 3–5 layers, 6–12 nodes, and the edge budget rule.
> [prompts.md] System Prompt · API Call Pattern · JSON Repair
2. Run Stage 1 validation per [validation](references/validation.md); apply all listed fixes inline.
> [validation.md] Stage 1 — Graph Validation (all formats) · Stage 2 — Format Validation · Validation Summary (quick reference)
3. Select the output format (`graph`, `svg`, or `png`) and run the matching format transformation from [formats](references/formats.md).
> [formats.md] Format 1: `graph` (default) · Format 2: `mermaid` · Format 3: `svg` · Format 4: `png`
4. Run Stage 2 validation (format-specific checks); fix issues; regenerate if any check fails.
5. If versioning is enabled, persist via [versioning](references/versioning.md).
> [versioning.md] Opt-in triggers · Storage layout (per user working directory) · YAML shape (canonical graph + meta) · Rendering saved versions to ASCII · Versioning operations (conversational, not slash-command) · Conversational edits (mini-DSL for editing saved diagrams) · When NOT to use versioning
6. Return the output without a prose wrapper; report artifact paths.

## Technique selection

See [technique-index](references/technique-index.md) for the full decision tree mapping user-intent aspects (arrow / assistant / edge / export / graph / json / layer / png / stage1 / style / svg / version / yaml) to the specific TECH-*.md file in `references/`.
> [technique-index.md] Decision tree (top-down) · Per-file TOC summary

## Examples

See the worked examples in the per-mode sub-sections above and in [examples](references/examples.md).
> [examples.md] Input · Design Decisions · Output 1: `graph` · Output 2: `mermaid` · Output 3: `svg` · Output 4: `png`

## Completion checklist & output protocol

See [completion-protocol](references/completion-protocol.md) for the full pre-delivery checklist, artifact-routing rules, job-completion-report schema, and per-error-mode handling.

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the work product (graph JSON / layered SVG / PNG export). Output path determined by project inference per [project-output-routing](../amw-design-principles/references/project-output-routing.md).
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
2. **Job-completion report** at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md` per [completion-protocol](references/completion-protocol.md).

## Resources

- [color-system](../amw-design-principles/color-system.md) — five-layer hex palette in oklch for print/contrast parity.
> [color-system.md] I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — node label minimum-font thresholds.
> [typography-system.md] I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
- `../../bin/amw-svg-render.py` — visual-verify loop for SVG / PNG output.
- `../../bin/amw-ascii-render.py` — perfect-ASCII renderer for the versioning preview layer.
- [SKILL](../amw-ascii-validator/SKILL.md) — ASCII render + validate contract used by the versioning layer.
- [SKILL](../amw-diagram-editorial/SKILL.md) — route here for editorial-infographic-style requests (not architecture).
- [SKILL](../amw-diagram-svg/SKILL.md) — route here for freeform / non-layered single-figure SVGs.
- [SKILL](../amw-ascii-to-svg/SKILL.md) — receives routing when the user pastes an ASCII architecture sketch.
- [SKILL](../amw-ux-flows/SKILL.md) — sibling for user-journey / task-flow / onboarding-funnel charts.
- `/amw-ascii-to-svg` — user-facing slash command that routes here when pasted ASCII is architectural.
- [prompts](references/prompts.md) — verbatim LLM system prompt, API call pattern, JSON-repair recipe.
> [prompts.md] System Prompt · API Call Pattern · JSON Repair
- [validation](references/validation.md) — Stage 1 (graph) and Stage 2 (format) validation checks and fixes.
> [validation.md] Stage 1 — Graph Validation (all formats) · Stage 2 — Format Validation · Validation Summary (quick reference)
- [formats](references/formats.md) — transform specifications for all four output formats.
> [formats.md] Format 1: `graph` (default) · Format 2: `mermaid` · Format 3: `svg` · Format 4: `png`
- [examples](references/examples.md) — fully worked SaaS-analytics-platform example across all four formats.
> [examples.md] Input · Design Decisions · Output 1: `graph` · Output 2: `mermaid` · Output 3: `svg` · Output 4: `png`
- [versioning](references/versioning.md) — opt-in on-disk versioning layout (YAML + history + rollback + mini-DSL).
> [versioning.md] Opt-in triggers · Storage layout (per user working directory) · YAML shape (canonical graph + meta) · Rendering saved versions to ASCII · Versioning operations (conversational, not slash-command) · Conversational edits (mini-DSL for editing saved diagrams) · When NOT to use versioning
- [technique-index](references/technique-index.md) — decision tree → TECH-*.md mapping.
> [technique-index.md] Decision tree (top-down) · Per-file TOC summary
- [completion-protocol](references/completion-protocol.md) — completion checklist + output protocol + error handling.
- [non-negotiables](references/non-negotiables.md) — hard limits (layer/node budgets, palette, validation).
> [non-negotiables.md] Hard limits · Model & output · Palette coherence · Validation

## Non-negotiables

See **[non-negotiables](references/non-negotiables.md)** for the full list of hard rules. Summary:
> [non-negotiables.md] Hard limits · Model & output · Palette coherence · Validation

- **Layer/node budgets.** 3–5 layers, 6–12 nodes. Edge budget: `floor(nodeCount × 0.8)`.
- **Model freshness.** Modern Sonnet or Opus only; never the retired 2025-05 dated snapshot.
- **No prose wrapper by default.** The output IS the diagram.
- **Palette coherence.** Five canonical oklch hues (slate-ink / rust / teal / amber / sage). The retired indigo-purple defaults triggered the AI-slop gate.
- **Validation is mandatory, not advisory.** Every Stage 1 and Stage 2 check must pass before return.

## Error Handling

See [completion-protocol](references/completion-protocol.md) § Error Handling for the full per-error-mode handling matrix (overloaded layer, too-few/too-many layers, SVG text overflow, model timeout / parse failure, auth missing, empty / too-abstract description).
> [completion-protocol.md] Completion checklist · Output protocol · Error Handling
