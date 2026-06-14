# Orchestrator reference index — annotated

This index holds the per-file annotations for the orchestrator's reference
library. `SKILL.md` keeps the bare links plus each file's complete embedded
Table of Contents; load this index when you want the one-line "what is this
file for" gloss before opening it.

## Table of Contents

- [Workflow + agent references](#workflow--agent-references)
- [Token references](#token-references)
- [UX-laws encyclopedia](#ux-laws-encyclopedia)
- [Token systems](#token-systems)
- [Process and craft references](#process-and-craft-references)

## Workflow + agent references

- [two-mode-summary](./two-mode-summary.md) — quick summary of command vs main-agent mode.
- [two-mode-workflow](./two-mode-workflow.md) — authoritative deep-dive on Phase A/B contract.
- [three-hard-rules](./three-hard-rules.md) — full text of the three hard rules + last-resort path.
- [agent-authoring-philosophy](./agent-authoring-philosophy.md) — judgment layer vs recipe layer; canonical 14-section sub-agent template.
- [agent-interaction-patterns](./agent-interaction-patterns.md) — cross-agent data hand-offs, one-way tree topology.
- [authority-hierarchy](./authority-hierarchy.md) — veto power and conflict-resolution rules.
- [sub-agent-return-contract](./sub-agent-return-contract.md) — YAML return-contract schema every sub-agent emits.
- [skill-invocation-protocol](./skill-invocation-protocol.md) — DO/DON'T rules agents follow when invoking skills.
- [phase-a-frozen-spec](./phase-a-frozen-spec.md) — Phase A.5 frozen-spec format and producer contract.
- [project-output-routing](./project-output-routing.md) — detection rules for project-inferred artifact output paths.
- [pivot-formats](./pivot-formats.md) — ASCII / DESIGN.md / Diagram-IR pivot formats.
- [downstream-executors](./downstream-executors.md) — full sub-skill routing table (Input / Plan / Output / Text-Visualization / Validation tiers).
- [runtime-conventions](./runtime-conventions.md) — Tweaks protocol, dimensional limits, animation stack, decision tree, file-management.

## Token references

- [ai-slop-avoid](../ai-slop-avoid.md) — 26 patterns to reject + positive-stance section.
- [question-templates](../question-templates.md) — universal must-ask + task-specific question checklists.
- [typography-system](../typography-system.md), [color-system](../color-system.md), [spacing-rhythm](../spacing-rhythm.md) — canonical token references.
- [design-heuristics](../design-heuristics.md) — Gestalt / Fitts / Hick principles for "something feels off" diagnosis.

## UX-laws encyclopedia

- [TECH-ux-laws-encyclopedia](./TECH-ux-laws-encyclopedia.md) — full 31-law reference (Fitts, Hick, Miller, Doherty, Goal-Gradient, Von Restorff, Tesler, Jakob, Pareto, Zeigarnik, Peak-End, Aesthetic-Usability, Cognitive Load, Information Foraging, 7 Gestalt principles, Banner Blindness, Serial Position, Chunking, Fogg, Sigmoid, Norman's vocabulary, Postel, Conway, Hofstadter); [quick-reference table](./TECH-ux-laws-quick-reference-table.md).

## Token systems

The plugin's design-token contract spans four mandatory families. Every DESIGN.md, every preset, every wireframe-builder emission resolves through these. Load the relevant file when authoring or auditing tokens:

- [TECH-token-system-color-roles](./TECH-token-system-color-roles.md) — 14 mandatory semantic color roles (primary/secondary/tertiary/surface/background/error + on-* pairs) with WCAG-AA pair-contrast invariants.
- [TECH-token-system-spacing-and-grid](./TECH-token-system-spacing-and-grid.md) — 4/8pt baseline, 10-step spacing scale, 12-col / 16-col grid + 6 breakpoints.
- [TECH-token-system-elevation-and-radius](./TECH-token-system-elevation-and-radius.md) — 8-layer z-index table, 7-tier elevation/shadow scale, 7-step radius scale with role-mapped defaults.
- [TECH-token-system-density-modes](./TECH-token-system-density-modes.md) — compact / comfortable / spacious as a multiplier over the spacing scale; responsive vs user-toggle decision matrix.

## Process and craft references

Load when the relevant trigger applies — not blanket-required on every project.

- [TECH-influence-and-persuasion](./TECH-influence-and-persuasion.md) — Cialdini's 7 principles mapped to UI patterns + 8-category friction audit + conversion-impact data; gate for landing / pricing / checkout / signup flows.
- [TECH-cross-cultural-design](./TECH-cross-cultural-design.md) — Wu-Xing 5-phase palette + Fibonacci spacing + 0.75× typographic waterfall + Swiss 12/16-col grid; load when audience is East Asian or aesthetic is Swiss-modernist.
- [TECH-enterprise-system-overrides](./TECH-enterprise-system-overrides.md) — IBM Carbon / Shopify Polaris / Trimble Modus / Adobe Spectrum override table + 3-tier (Global / Semantic / Component) token architecture + agentic UX patterns (Tool → Copilot → Agent + intent modeling + audit trails).
- [TECH-css-modern-syntax](./TECH-css-modern-syntax.md) — `oklch()` / `color-mix()` / `light-dark()` / `@container` / `@layer` / `@scope` / native nesting / `:has()` / `@starting-style` / View Transitions / anchor positioning / Tailwind v4 native-CSS features + fallback strategies.
