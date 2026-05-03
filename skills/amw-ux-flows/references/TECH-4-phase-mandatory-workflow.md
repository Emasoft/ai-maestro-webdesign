---
name: TECH-4-phase-mandatory-workflow
category: ux-flow-prd
source: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Phase 1 — Use case extraction (Phase-1 gate)](#phase-1-use-case-extraction-phase-1-gate)
  - [Phase 2 — Mermaid diagrams](#phase-2-mermaid-diagrams)
  - [Phase 3 — HTML wireframes (MANDATORY)](#phase-3-html-wireframes-mandatory)
  - [Phase 4 — Consolidation handoff](#phase-4-consolidation-handoff)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-4-phase-mandatory-workflow

## What it does

Runs UX flow generation as a **mandatory 4-phase pipeline** — use-case
extraction, Mermaid diagrams, HTML wireframes, consolidation. Every
phase must execute in order; none may be skipped, summarised, or
deferred. The MANDATORY nature of Phase 3 (HTML wireframes) is the
distinguishing feature of this skill.

## When to use

- **Every invocation** of the `ux-flows` skill. Always.
- **Never partial invocations.** If the user asks for "just the
  diagrams", decline: this skill's value is the full pipeline. Point
  them to `diagram-architecture` or `ux-flows` separately if they only
  need one artifact.

## How it works

### Phase 1 — Use case extraction (Phase-1 gate)

Input: PRD (`docs/product/prd.md`) or user-supplied feature list.
Output: `docs/ux-flows/use-cases.md` with 5-12 structured use cases.
Gate: user approves the list before Phase 2 starts.

See [TECH-prd-to-usecases](TECH-prd-to-usecases.md).

### Phase 2 — Mermaid diagrams

Input: approved use-case list.
Output: `docs/ux-flows/diagrams/` with:
- `screen-map.md` — master `graph TD` showing every screen + navigation
- `{uc-id}/flow.md` — per-UC `graph TD` flowchart
- `{uc-id}/states.md` — per-UC `stateDiagram-v2`
- `{uc-id}/sequence.md` — per-UC `sequenceDiagram` with HTTP methods
- `INDEX.md` — catalog with cross-links

See [TECH-mermaid-flowchart-screen-map](TECH-mermaid-flowchart-screen-map.md),
[TECH-mermaid-state-diagram-screen](TECH-mermaid-state-diagram-screen.md),
> [TECH-mermaid-state-diagram-screen.md] What it does · When to use · How it works · Basic transitions · Nested states · Parallel states · Minimal example · Gotchas · Cross-references
[TECH-mermaid-sequence-authenticated](TECH-mermaid-sequence-authenticated.md).
> [TECH-mermaid-sequence-authenticated.md] What it does · When to use · How it works · Actor reference · Message syntax · Error-handling pattern · Minimal example · Gotchas · Cross-references

### Phase 3 — HTML wireframes (MANDATORY)

Input: screens identified in Phase 2 flowcharts.
Output: `docs/ux-flows/wireframes/` with:
- One `.html` file per unique screen (mobile-first, 375px, self-contained)
- Inter-screen `<a href="target.html" class="wf-link">` navigation
- `INDEX.md` screen inventory

The skill does NOT ask the user whether to continue to Phase 3 — it
just runs. Skipping Phase 3 breaks the "clickable prototype" deliverable
that downstream `ui-ux-pro-max` consumers expect.

See [TECH-wireframe-html-mobile-first](TECH-wireframe-html-mobile-first.md),
[TECH-clickable-prototype-navigation](TECH-clickable-prototype-navigation.md).

### Phase 4 — Consolidation handoff

Input: all artifacts from Phases 1-3.
Output: `docs/ux-flows/UX-FLOWS.md` — master handoff document with:
- Screen map link
- Screen inventory
- Per-UC diagram links
- Clickable prototype link table
- Navigation patterns summary
- Open questions for downstream UI design

Optionally, after Phase 4 completes, offer Figma export via the Dev Mode
MCP Server — see [TECH-figma-code-to-canvas-export](TECH-figma-code-to-canvas-export.md). Never silently
attempt Figma; always inform requirements first.

## Minimal example

Invocation:

```
User: "Design the user flows from the PRD"
```

Agent runs Phase 1: parses `docs/product/prd.md`, emits 5 use cases,
asks for approval.

```
User: "Approved"
```

Agent runs Phase 2: emits 1 screen map + 5×3=15 per-UC diagrams + 1 INDEX.

Agent IMMEDIATELY runs Phase 3 (no gate question): identifies 8 unique
screens across the flowcharts, emits 8 wireframe HTML files with cross-
navigation.

Agent runs Phase 4: emits master UX-FLOWS.md and offers optional
browser preview via `dev-browser`.

Agent informs the user Figma export is available as an optional next
step.

## Gotchas

- **Phase 3 is MANDATORY.** The source skill explicitly states: "This
  phase MUST NOT be skipped, summarized, or deferred. Every invocation
  of this skill that reaches Phase 2 MUST continue to Phase 3. Do not
  ask the user whether to proceed — just do it."
- **Phase 1 gate is a hard stop.** Do not auto-approve the use-case
  list. The user must see and confirm — otherwise downstream artifacts
  reference phantom features.
- **Output goes under `docs/ux-flows/`, not `docs_dev/`**. These are
  shipping artifacts.
- **Never ship Phase 2 without Phase 3** — users who see a Mermaid flow
  without a clickable prototype think "the design is half-done". The
  4-phase guarantee is part of the skill's contract.
- **Figma export is opt-in** — mention it at the end of Phase 4, but do
  not attempt it. See [TECH-figma-code-to-canvas-export](TECH-figma-code-to-canvas-export.md) for the
  opt-in protocol.

## Cross-references

- [SKILL](../SKILL.md) — the workflow section
- [TECH-prd-to-usecases](TECH-prd-to-usecases.md) — Phase 1 details
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-mermaid-flowchart-screen-map](TECH-mermaid-flowchart-screen-map.md) — Phase 2 screen map
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-wireframe-html-mobile-first](TECH-wireframe-html-mobile-first.md) — Phase 3 wireframe template
  > What it does · When to use · How it works · Scaffold · Aesthetic tokens · Utility classes · Minimal example · Gotchas · Cross-references
- [TECH-figma-code-to-canvas-export](TECH-figma-code-to-canvas-export.md) — optional Phase 5
  > What it does · When to use · How it works · Prerequisites (MUST be mentioned before any Figma operation) · Protocol · Export workflow (once prerequisites are confirmed) · Minimal example · Gotchas · Cross-references
