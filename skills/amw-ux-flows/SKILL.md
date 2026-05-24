---
name: amw-ux-flows
description: PRD → use cases → Mermaid diagrams (flowchart + state + sequence) → mobile-first clickable HTML wireframes with inter-screen navigation → consolidated handoff. Triggers on "user flows from the PRD", "wireframe this feature", "generate a screen map", "clickable prototype", "flow/sequence diagram for a screen". Does NOT trigger on "design a page", "style the UI" — routes to design-principles. Use when converting a PRD into flows and wireframes. Trigger with "user flows from the PRD".
version: 0.1.0
author: ai-maestro-webdesign
---

# UX Flows

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is an executor. Triggers are PRD-to-wireframe-specific only — generic design vocabulary stays with the orchestrator.

## Overview

PRD (or feature list) → use cases → Mermaid diagrams (flowchart + state + sequence) → mobile-first 375px clickable HTML wireframes with inter-screen navigation → consolidated handoff document (`UX-FLOWS.md`). Bridges Product and Visual Design. Four mandatory phases in order — none skippable. Wireframes are prototype-grade only (dashed-border greyscale, no brand tokens); production HTML routes downstream to `amw-ascii-to-html`. Optional Figma Dev Mode MCP export on explicit user request.

## Instructions

1. Read or request the PRD (or feature list) — if `<docs/product/prd.md>` exists, read it; otherwise ask the user; do not synthesize use cases from nothing.
2. **Phase 1 — Use Case Extraction**: see [TECH-prd-to-usecases](references/TECH-prd-to-usecases.md) and [TECH-use-case-document-schema](references/TECH-use-case-document-schema.md). Save to `<docs/ux-flows/use-cases.md>`; wait for explicit user confirmation before Phase 2.
3. **Phase 2 — Mermaid Diagrams**: read [mermaid-patterns](references/mermaid-patterns.md) first; generate a master screen-map flowchart plus per-use-case flow/state/sequence diagrams under `docs/ux-flows/diagrams/`; max 15-20 nodes per diagram. See [TECH-mermaid-flowchart-screen-map](references/TECH-mermaid-flowchart-screen-map.md), [TECH-mermaid-state-diagram-screen](references/TECH-mermaid-state-diagram-screen.md), [TECH-mermaid-sequence-authenticated](references/TECH-mermaid-sequence-authenticated.md), [TECH-split-large-flows-subflow-linking](references/TECH-split-large-flows-subflow-linking.md).
4. **Phase 3 — HTML Wireframes (MANDATORY)**: see [TECH-wireframe-html-mobile-first](references/TECH-wireframe-html-mobile-first.md), [TECH-clickable-prototype-navigation](references/TECH-clickable-prototype-navigation.md), [TECH-no-dead-end-screens](references/TECH-no-dead-end-screens.md), [TECH-wireframe-index-inventory](references/TECH-wireframe-index-inventory.md). Self-contained, mobile-first 375px, dashed-border greyscale; inter-screen `<a href>` navigation only.
5. **Phase 4 — Handoff**: compile `<docs/ux-flows/UX-FLOWS.md>`; route to `../amw-ascii-sketch/` for ASCII iteration, `../amw-ascii-to-html/` for production HTML lift, or `../amw-diagram-editorial/` if Mermaid diagrams need editorial upgrade.

Full end-to-end example: see [TECH-4-phase-mandatory-workflow](references/TECH-4-phase-mandatory-workflow.md). Optional Figma export: [TECH-figma-code-to-canvas-export](references/TECH-figma-code-to-canvas-export.md).

## Activation and triggers

No dedicated slash command — this skill is invoked by the `design-principles` orchestrator (Phase A wireframe validation, or Phase B implementation deliverable). Self-contained: any agent can use it by reading this SKILL.md plus the relevant TECH references.

Fires on specific phrasings: "design the user flows from the PRD", "wireframe the <feature> feature", "generate a screen map for <app>", "document the use cases from the PRD", "create the clickable prototype for <feature>", "flow / state / sequence diagram for <screen / API>", "map the navigation for <app>", "build the user journey for <feature>".

Does NOT fire on: "design a landing page", "make a nice dashboard", "build the UI" → those route to design-principles. Bare "flowchart" → route to `../amw-diagram-architecture/` (system diagram) or `../amw-diagram-svg/` (freeform).

Position in flow: PROCESS (Phase A/B bridge). Consumes a PRD or feature list, emits four artifact classes — use cases, Mermaid diagrams, clickable HTML wireframes, master handoff. Outputs feed downstream into `../amw-ascii-sketch/` (ASCII iteration), `../amw-ascii-to-html/` (responsive HTML lift), or `../amw-infographics/` / `../amw-diagram-editorial/` (editorial diagram upgrade). Wireframes here are prototype-grade only.

## Prerequisites

- **runtime_binaries (system):** none — Mermaid is text-only and Claude renders the blocks; HTML wireframes are self-contained.
- **runtime_binaries (bundled):** `../../bin/amw-dev-browser-wrapper.sh` — plugin-standard browser wrapper, used for optional wireframe preview in Phase 3.
- **runtime_binaries (via /amw-init):** `dev-browser` CLI — required only when the user wants an in-browser preview of the clickable prototype.
- **mcp_servers (optional, on explicit request):** Figma Dev Mode MCP Server — see [figma-integration](references/figma-integration.md) and [TECH-figma-code-to-canvas-export](references/TECH-figma-code-to-canvas-export.md). Never activated silently.

## Resources

All techniques live as standalone reference files under `./references/`. Load only the file matching the current need.

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator
- [SKILL](../amw-dev-browser/SKILL.md) — wireframe preview primitive
- [SKILL](../amw-ascii-sketch/SKILL.md) — downstream ASCII iteration option
- [SKILL](../amw-ascii-to-html/SKILL.md) — downstream lift from wireframe prototype to responsive HTML
- [SKILL](../amw-ux-designer/SKILL.md) — broader UX methodology the wireframes slot into
- [SKILL](../amw-ux-evaluator/SKILL.md) — consumes the clickable prototype for heuristic scoring
- `../../bin/amw-dev-browser-wrapper.sh` — plugin-standard browser wrapper
- `assets/wireframe-template.html` — mobile-first 375px wireframe base template
- [mermaid-patterns](references/mermaid-patterns.md) — Mermaid syntax cookbook (node shapes, subgraphs, sequence patterns, styling)
- [figma-integration](references/figma-integration.md) — Figma Dev Mode MCP workflow (on explicit request only)
- [install-commands](references/install-commands.md) — auxiliary skill + dev-browser install references

### TECH references (one per technique)

- [TECH-4-phase-mandatory-workflow](references/TECH-4-phase-mandatory-workflow.md) — full Phase 1→4 walk-through
- [TECH-prd-to-usecases](references/TECH-prd-to-usecases.md) — extracting use cases from a PRD
- [TECH-use-case-document-schema](references/TECH-use-case-document-schema.md) — UC field schema
- [TECH-mermaid-flowchart-screen-map](references/TECH-mermaid-flowchart-screen-map.md) — master screen-map flowchart
- [TECH-mermaid-state-diagram-screen](references/TECH-mermaid-state-diagram-screen.md) — per-screen state machine
- [TECH-mermaid-sequence-authenticated](references/TECH-mermaid-sequence-authenticated.md) — auth-aware sequence diagrams
- [TECH-split-large-flows-subflow-linking](references/TECH-split-large-flows-subflow-linking.md) — splitting > 20-node flows
- [TECH-wireframe-html-mobile-first](references/TECH-wireframe-html-mobile-first.md) — 375px wireframe scaffold
- [TECH-clickable-prototype-navigation](references/TECH-clickable-prototype-navigation.md) — inter-screen `<a href>` navigation
- [TECH-no-dead-end-screens](references/TECH-no-dead-end-screens.md) — every screen needs an outgoing link
- [TECH-wireframe-index-inventory](references/TECH-wireframe-index-inventory.md) — INDEX.md inventory schema
- [TECH-figma-code-to-canvas-export](references/TECH-figma-code-to-canvas-export.md) — opt-in Figma export

## Completion checklist

Before reporting a job using this skill as complete, verify every item:

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-ux-flows/references/` was consulted and is cited in the final report.
- Output passes the skill's non-negotiables (see below).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

Two outputs:

1. **Artifacts** — use-case `.md`, Mermaid diagrams, HTML wireframes, `UX-FLOWS.md`. Path determined by project inference per [project-output-routing](../amw-design-principles/references/project-output-routing.md): user-supplied → framework convention → existing `./design/<subtype>/` → fallback `./design/wireframes/` or `./design/diagrams/` → last-resort `/tmp/amw-ux-flows-<slug>/`.

2. **Job report** — `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md` with Inputs, Method, Artifacts, Checklist, Deviations sections. Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. Every artifact MUST be linked from the report.

## Non-negotiables

- **`dev-browser` is the only authorized browser-automation primitive.** Any wireframe preview, inter-screen click-through, or live inspection routes through `bin/amw-dev-browser-wrapper.sh`. Chrome DevTools MCP is not used by this plugin.
- **Figma Dev Mode MCP stays intact** but opt-in — only activated when the user explicitly says "export to figma". Never probe automatically.
- **Phase 3 is mandatory.** Reaching Phase 2 and then stopping (diagrams only, no clickable prototype) is a failure mode — the whole value of this skill is the wireframe handoff.
- **Pure-HTML prototypes.** Wireframes use `<a href>` navigation only; no JS, no form submits, no onclick. Guarantees the prototype works in any browser, preserves the back button, and makes Figma Code-to-Canvas export deterministic.
- **Wireframes are prototype-grade.** Dashed-border wireframe aesthetic, mobile-first 375px, no brand tokens, no real typography. Production HTML belongs to `../amw-ascii-to-html/` or direct design-principles output — not here.
- **No dead-end screens.** Every screen has at least one outgoing link. Enforced in the Phase 3 INDEX review.
- **Respect design-principles Rule 1.** If no PRD and no feature list, stop and ask — do not synthesize use cases.
- **Never silent on Figma.** Always present prerequisites before touching the Dev Mode MCP.

## Error Handling

- **No PRD, no feature list** → cannot proceed. Ask the user; optionally route to `product-manager-toolkit` via [install-commands](references/install-commands.md).
- **Phase 2 stops before Phase 3** → orchestrator should abort and re-enter Phase 3.
- **Mermaid block rendering conflict** → use fenced `mermaid` blocks with unique IDs or delegate render to `../amw-diagram-architecture/`.
- **Figma MCP requested but not installed** → stop, present the two-step install from [install-commands](references/install-commands.md). Do not try alternate paths.
- **`dev-browser` CLI missing for preview** → surface `/amw-doctor` and `/amw-init`; wireframes still open in any browser without the wrapper.
- **Wireframe aesthetic drift** → real colors/images/typography belong to a downstream skill, not here.
- **Inter-screen dead ends** → breaks the clickable prototype and fails Phase 3 review. Fix before emitting the INDEX.
