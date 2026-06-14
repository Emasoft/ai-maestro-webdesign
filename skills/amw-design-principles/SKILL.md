---
name: amw-design-principles
description: Orchestrator for any web, UI, slide, prototype, or design task. Enforces three hard rules — (1) gather context, (2) produce ≥3 variants, (3) reject AI-slop — and routes to executors. Triggers on "design a page", "landing page", "mockup", "UI for", "prototype", "wireframe", "slide deck", "dashboard", "website". Plan phase runs in ASCII via /amw-sketch; HTML follows approval. Use when the user requests any visual design artifact. Trigger with /amw-sketch.
version: 0.1.0
author: ai-maestro-webdesign
---

# Design Principles — the orchestrator

> **Core insight:** good design is not guessed from scratch; it grows out of existing context. This skill compresses the Claude Design judgment set into an executable checklist, enforces three hard rules (gather context, produce three variants, reject AI-slop), and routes execution to the plugin's executor sub-skills. The plan phase runs in ASCII via `amw-ascii-sketch`; HTML follows only after explicit approval.

## When to trigger

Activates on: websites, landing pages, component libraries; slide decks, pitch decks, presentation documents; app and web prototypes, interactive demos; posters, visual assets, infographics; brand collateral, cards, badges; any HTML or SVG output that "must not look AI-generated". Trigger vocabulary: *design, UI, mockup, prototype, slide, deck, poster, landing, wireframe, mock, interface, page, website, dashboard, brand, style, visual.*

When active it **owns the task** until it explicitly routes to an executor; other plugin skills (`ascii-sketch`, `diagram-*`, `infographics`, `svg-creator`, `design-extract`, etc.) are executors run under its rules. **Prerequisites:** standard plugin runtime — nothing skill-specific beyond the global plugin dependencies.

## Two operating modes

Two modes per request: **Command mode (fast path)** — a `/amw-*` command or concrete format + parameters → dispatch directly to the matching sub-skill (no Phase A loop, no Phase B spawning); **Main-agent mode (requirements path)** — goals/broad intent without a concrete format → Phase A (conversational, low-fi, low-token ASCII iteration) via `ai-maestro-webdesign-main-agent`, then Phase B (sub-agent spawning, real artifacts) ONLY after explicit satisfaction. The **Phase A → Phase B approval gate is a hard invariant**: do NOT spawn sub-agents or produce real artifacts (HTML, SVG, PNG, MP4) until the user confirms with a satisfaction token (`yes`, `ship it`, `approved`, `that's the one`, `perfect`, `done`, `go ahead`, `let's do it`). Full per-mode spec + deep-dive: `two-mode-summary` and `two-mode-workflow` (linked + embedded under Resources below).

## The three hard rules (violating any one is a failure)

1. **Gather context before designing.** Require a design system, brand tokens, or reference examples; the `last resort` fallback is `amw-ui-ux-reasoning` — never "let me guess."
2. **Always produce at least three variants** (baseline → advanced → experimental). Single-answer output is a failure mode; use `amw-ascii-sketch` before HTML — cheap to iterate.
3. **Reject AI-slop patterns.** The full list is in [ai-slop-avoid](ai-slop-avoid.md); any HTML runs a final check against it before delivery.
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)

These rules apply to every skill in the plugin (sub-skills inherit them via the orchestrator, never override them); full text + rationale + last-resort path: [three-hard-rules](./references/three-hard-rules.md).
> [three-hard-rules.md] Rule 1: Gather design context before designing · Rule 2: Deliver at least three variants, baseline → advanced → experimental · Rule 3: Reject every AI-slop pattern

## Instructions and ASCII-first plan phase

The 7-step execution recipe (read brief → gather context → [question-templates](question-templates.md) checklist + declare visual system → `/amw-sketch` ≥ 3 ASCII variants to satisfaction → AI-slop gate → `/amw-ascii-to-html` + `/amw-preview` → route to executors) and the ASCII-first plan-phase rules live in [orchestrator-execution-flow](./references/orchestrator-execution-flow.md). **When the user asks for a webpage design, the plan phase runs in ASCII, not HTML** — iterate cheaply to satisfaction, then convert; skip only when the user already committed to a layout.
> [question-templates.md] Universal must-ask (every design task) · Task-specific additions · Questions NOT to ask · Suggested format · Design Read — declare before iterating · Tip
> [orchestrator-execution-flow.md] Instructions · ASCII-first plan phase (the default workflow)

## Runtime conventions

Detailed conventions (Tweaks live-tuning, dimensional hard limits, animation stack order, decision tree, file-management, workflow rhythm) live in [runtime-conventions](./references/runtime-conventions.md) — every HTML/SVG emitter under this orchestrator MUST follow them.
> [runtime-conventions.md] Tweaks live-tuning mode (recommended) · Dimensional hard limits (no discussion) · Animation stack order · Decision tree — which file to load when · File-management rules · Workflow rhythm

## Output, error handling, and examples

Produces a single artifact at the path the Instructions flow specifies — HTML (plan-phase → ASCII → approval → HTML), SVG, or other executor-directed format. On failure, emit a non-zero exit code or structured error (`bin/` scripts carry the tool-specific semantics). Worked examples: the per-mode sub-sections above and `references/`.

## Resources

Per-file annotations (the "what is this for" gloss for every link below) live in [orchestrator-reference-index](./references/orchestrator-reference-index.md).
> [orchestrator-reference-index.md] Workflow + agent references · Token references · UX-laws encyclopedia · Token systems · Process and craft references

**Workflow + agent references:**

- [two-mode-summary](./references/two-mode-summary.md)
> [two-mode-summary.md] Command mode (fast path) · Main-agent mode (requirements path) · Approval gate invariant
- [two-mode-workflow](./references/two-mode-workflow.md)
> [two-mode-workflow.md] Sub-agent delegation (Main-agent mode only) · Mode Detection · Phase A — Iterative Low-Fi Loop · Phase B — Implementation and Spawning · Scenario Testing via dev-browser (mandatory in Phase B) · Anti-Patterns
- [downstream-executors](./references/downstream-executors.md) — full sub-skill routing table.
> [downstream-executors.md] Input — gather context for Rule 1 · Plan phase — satisfy Rule 2 in ASCII · Output — render the approved direction · Text visualization — ASCII artifacts for PRs, ADRs, terminals, and chat · Validation + reference · Tier-4 specialists (on-demand, Phase B only)
- [agent-authoring-philosophy](./references/agent-authoring-philosophy.md)
> [agent-authoring-philosophy.md] Skills and agents are not the same kind of thing · What an agent actually needs · Why the judgment layer matters in this plugin specifically · The 14-section canonical template · What this document is NOT · Cross-references
- [agent-interaction-patterns](./references/agent-interaction-patterns.md)
> [agent-interaction-patterns.md] Topology invariants · Phase A data flow · Phase B data flow · What main-agent does between sub-agent calls · Error propagation · Why this topology (instead of peer-to-peer) · Enforcement
- [authority-hierarchy](./references/authority-hierarchy.md)
> [authority-hierarchy.md] Domains and authority · Veto power — what it means · Resolution rules by conflict pattern · How main-agent applies the hierarchy · What the hierarchy does NOT do · Enforcement
- [sub-agent-return-contract](./references/sub-agent-return-contract.md)
> [sub-agent-return-contract.md] Schema · Field semantics · Markdown body structure · How main-agent consumes the contract · Contract invariants (enforced by smoke tests)
- [skill-invocation-protocol](./references/skill-invocation-protocol.md)
> [skill-invocation-protocol.md] The problem · The protocol · Examples · Enforcement
- [phase-a-frozen-spec](./references/phase-a-frozen-spec.md)
> [phase-a-frozen-spec.md] Schema · Producers · Consumers · Mutability · Path conventions · Worked example · Cross-references
- [project-output-routing](./references/project-output-routing.md)
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
- [pivot-formats](./references/pivot-formats.md)
> [pivot-formats.md] ASCII (chat-native plan-phase pivot) · DESIGN.md (design-system pivot) · Diagram IR — schema-name diagram-ir version 1.0 (cross-format diagram pivot) · How agents pick the right pivot · Adding a fourth pivot

**Token references** (`ai-slop-avoid` and `question-templates` are linked + embedded in the body above — rule 3 / Instructions step 3):

- [typography-system](typography-system.md), [color-system](color-system.md), [spacing-rhythm](spacing-rhythm.md), [design-heuristics](design-heuristics.md)
> [typography-system.md] I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
> [color-system.md] I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
> [spacing-rhythm.md] I. 8pt grid system · II. Fibonacci spacing rhythm (large-scale) · III. Vertical rhythm (baseline grid) · IV. Hit targets (tappable areas) · V. Alignment · VI. Three principles of whitespace · VII. Border radius · VIII. Shadow system · IX. Self-check
> [design-heuristics.md] I. Gestalt's five principles (organizing the visual field) · II. Fitts's Law · III. Hick's Law · IV. Miller's Law (7 ± 2) · V. Jakob's Law · VI. The four dimensions of visual hierarchy · VII. F-Pattern vs Z-Pattern reading · VIII. Peak-End Rule · IX. Aesthetic-Usability Effect · Self-check list · X. Refactoring-UI atomic audit rules (T-054)

**UX-laws encyclopedia:**

- [TECH-ux-laws-encyclopedia](./references/TECH-ux-laws-encyclopedia.md), [quick-reference table](./references/TECH-ux-laws-quick-reference-table.md)
> [TECH-ux-laws-encyclopedia.md] Motor and perceptual laws (Fitts, Hick-Hyman, Doherty) · Memory and cognition (Miller, Cognitive Load, Information Foraging, Chunking) · Motivation and emotion (Goal-Gradient, Von Restorff, Zeigarnik, Peak-End, Aesthetic-Usability, Jakob, Pareto) · Gestalt perception (Proximity, Similarity, Closure, Continuity, Common Region, Common Fate, Figure-Ground) · Attention and habituation (Banner Blindness, Serial Position) · Behavioral models (Fogg B=MAT, Sigmoid Adoption) · Norman's vocabulary (Mental Model, Affordance, Signifier, Mapping, Constraints, Feedback) · Meta-laws of software (Tesler, Postel, Conway, Hofstadter) · Cross-references
> [TECH-ux-laws-quick-reference-table.md] Motor and perceptual laws · Memory and cognition laws · Motivation and emotion laws · Gestalt grouping principles · Attention, behavior, and system laws · How to use this table · Cross-references

## Token systems

The plugin's design-token contract spans four mandatory families, resolved through every DESIGN.md / preset / wireframe emission:

- [TECH-token-system-color-roles](./references/TECH-token-system-color-roles.md)
> [TECH-token-system-color-roles.md] What this is · The 14 mandatory color roles · The on-* pair invariants (WCAG-AA gate) · Token block — canonical declaration · Breaks if · Component example A — pricing card · Component example B — toast/alert stack · Cross-references
- [TECH-token-system-spacing-and-grid](./references/TECH-token-system-spacing-and-grid.md)
> [TECH-token-system-spacing-and-grid.md] What this is · The 4/8pt baseline · The 10-step spacing scale · Inline vs block axis tokens · Responsive grid — 12-col / 16-col + breakpoints · Token block — canonical declaration · Breaks if · Component example A — card grid with section rhythm · Component example B — form field stack · Cross-references
- [TECH-token-system-elevation-and-radius](./references/TECH-token-system-elevation-and-radius.md)
> [TECH-token-system-elevation-and-radius.md] What this is · The z-index layer table · The 7-tier elevation/shadow scale · The 7-step radius scale + role mapping · Token block — canonical declaration · Breaks if · Component example A — modal stack with backdrop · Component example B — card with hover lift · Cross-references
- [TECH-token-system-density-modes](./references/TECH-token-system-density-modes.md)
> [TECH-token-system-density-modes.md] What this is · The three density modes · The multiplier table — how density scales each token family · Density and type-scale interaction · Responsive density vs user-toggle density · Token block — canonical declaration · Breaks if · Component example A — data table at three densities · Component example B — responsive density on a sidebar · Cross-references

## Process and craft references

Load when the relevant trigger applies — not blanket-required on every project:

- [TECH-influence-and-persuasion](./references/TECH-influence-and-persuasion.md)
> [TECH-influence-and-persuasion.md] What it does · When this file fires · The 7 Cialdini principles → UI patterns · Reciprocity · Scarcity · Authority · Social proof · Liking · Commitment & consistency · Unity · The 8-category friction audit · Conversion-impact data (use to back proposals with numbers) · Anti-patterns — when persuasion becomes dark UX · Breaks if · Cross-references
- [TECH-cross-cultural-design](./references/TECH-cross-cultural-design.md)
> [TECH-cross-cultural-design.md] What it does · When this file fires · Wu-Xing five-phase palette framework · The five phases and their hue families · The 5 × 8 = 40-shade palette · Cultural pairings — when to use, when to skip · Fibonacci spacing scale · The values · Why Fibonacci over 4 / 8 px linear scales · Implementation as CSS variables · Typographic waterfall scale · The 0.75× ratio · The reference waterfall · Swiss 12 / 16-column grid pairing · Worked example — Asian-market editorial site · Breaks if · Cross-references
- [TECH-enterprise-system-overrides](./references/TECH-enterprise-system-overrides.md)
> [TECH-enterprise-system-overrides.md] What it does · When this file fires · Section 1 — Enterprise design-system override table · Why this table exists · The four enterprise systems · How to use the table · Section 2 — 3-tier design-token architecture · The three tiers · Naming convention · Concrete example — a Primary button · Signals you need a token system · Signals you do NOT need one · Section 3 — Agentic UX patterns (Tool → Copilot → Agent) · The three modes of agentic interaction · Intent modeling · Progressive disclosure of agent actions · Audit trails · Breaks if · Cross-references
- [TECH-css-modern-syntax](./references/TECH-css-modern-syntax.md)
> [TECH-css-modern-syntax.md] What it does · When this file fires · Baseline-availability summary · Color features · `oklch()` and `oklab()` — perceptual color spaces · `color-mix()` — programmatic tinting / shading · `light-dark()` — automatic dark-mode pairs · Relative color syntax — derive from a base · Container queries · `@container` — query the parent's size · Container query units (`cqw`, `cqh`, `cqi`, `cqb`) · Scoping and cascade control · `@layer` — explicit cascade ordering · `@scope` — bounded style application · Native CSS nesting · Selector ergonomics · `:has()` — parent / sibling-aware selectors · `:is()` and `:where()` · Transitions and motion · `@starting-style` — first-paint transitions · View Transitions API · Anchor positioning · Tailwind v4 native-CSS features · Layout & viewport correctness · Dynamic viewport units — `100dvh`, never `100vh` · CSS Grid for structure — not flexbox percentage math · Fallback strategies · Breaks if · Cross-references

## Closing note

Ninety percent of design failures come from not asking enough questions, too little context, and delivering only one option — treat this SKILL.md as a checklist and walk every step. "Fast output" and "good design" differ; ASCII-first iteration gets both.
