---
name: amw-design-principles
description: Orchestrator for any web, UI, slide, prototype, or design task. Enforces three hard rules — (1) gather context, (2) produce ≥3 variants, (3) reject AI-slop — and routes to executors. Triggers on "design a page", "landing page", "mockup", "UI for", "prototype", "wireframe", "slide deck", "dashboard", "website". Plan phase runs in ASCII via /amw-sketch; HTML follows approval. Use when the user requests any visual design artifact. Trigger with /amw-sketch.
version: 0.1.0
author: ai-maestro-webdesign
---

# Design Principles — the orchestrator

> **Core insight:** good design is not guessed from scratch; it grows out of existing context. This skill compresses the Claude Design judgment set into an executable checklist and routes technical execution to the sub-skills in this plugin.

## Overview

Orchestrator for any web, UI, slide, prototype, poster, or design task. Enforces three hard rules (gather context, produce three variants, reject AI-slop) and routes to the appropriate executor skill. The plan phase runs in ASCII via `amw-ascii-sketch` until the user is explicitly satisfied; HTML is generated only after approval.

## When to trigger

Any of the following task types activates this skill:

- Websites, landing pages, component libraries
- Slide decks, pitch decks, presentation documents
- App and web prototypes, interactive demos
- Posters, visual assets, infographics
- Brand collateral, cards, badges
- Any HTML or SVG output that "must not look AI-generated"

Trigger vocabulary: *design, UI, mockup, prototype, slide, deck, poster, landing, wireframe, mock, interface, page, website, dashboard, brand, style, visual.*

When this skill activates, it **owns the task** until it explicitly routes to an executor. Other skills in this plugin — `ascii-sketch`, `diagram-*`, `infographics`, `svg-creator`, `design-extract`, etc. — are executors that run under this skill's rules.

## Two operating modes

The orchestrator distinguishes two modes on every incoming request:

- **Command mode (fast path)** — user invokes a `/amw-*` slash command explicitly, or supplies a concrete format + parameters. Dispatch directly to the matching sub-skill; no Phase A iteration loop, no Phase B spawning.
- **Main-agent mode (requirements path)** — user states goals or broad intent without a concrete format. Phase A (conversational, low-fi, low-token ASCII iteration) runs first via `ai-maestro-webdesign-main-agent`; Phase B (sub-agent spawning, real artifacts) starts ONLY after explicit satisfaction tokens are received.

The Phase A → Phase B approval gate is a hard invariant: do NOT spawn sub-agents or produce real artifacts (HTML, SVG, PNG, MP4) until the user has confirmed the low-fi direction with `yes`, `ship it`, `approved`, `that's the one`, `perfect`, `done`, `go ahead`, or `let's do it`. Full spec: [two-mode-summary](./references/two-mode-summary.md); authoritative deep-dive: [two-mode-workflow](./references/two-mode-workflow.md).
> [two-mode-workflow.md] Sub-agent delegation (Main-agent mode only) · Mode Detection · Phase A — Iterative Low-Fi Loop · Phase B — Implementation and Spawning · Scenario Testing via dev-browser (mandatory in Phase B) · Anti-Patterns
> [two-mode-summary.md] Command mode (fast path) · Main-agent mode (requirements path) · Approval gate invariant

## The three hard rules (violating any one of these is a failure)

1. **Gather context before designing.** Require design system, brand tokens, or reference examples. The `last resort` fallback is `amw-ui-ux-reasoning` — do not fall back to "let me guess."
2. **Always produce at least three variants** (baseline → advanced → experimental). Single-answer output is a failure mode. Use `amw-ascii-sketch` when the user hasn't committed to HTML yet — it is cheap to iterate.
3. **Reject AI-slop patterns.** The full list is in [ai-slop-avoid](ai-slop-avoid.md). Any HTML output runs a final check against that file before delivery.
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)

Full text, rationale, and last-resort path: [three-hard-rules](./references/three-hard-rules.md).
> [three-hard-rules.md] Rule 1: Gather design context before designing · Rule 2: Deliver at least three variants, baseline → advanced → experimental · Rule 3: Reject every AI-slop pattern

These rules apply to every skill in the plugin. Sub-skills inherit them via the orchestrator; they do not override them.

## Prerequisites

Standard plugin runtime — no skill-specific prerequisites beyond the global plugin dependencies.

## Instructions

1. Read the brief and decide if this skill fires (broad design vocabulary: design, UI, mockup, landing page, wireframe, prototype, slide, deck, poster, website).
2. Gather context: request UI kit, brand assets, or reference examples; use `amw-ui-ux-reasoning` as last resort if none are available.
3. Run the question checklist from [question-templates](question-templates.md) (ask ≥ 10 questions), then declare the visual system (font + palette + spacing rhythm).
> [question-templates.md] Universal must-ask (every design task) · Task-specific additions · Questions NOT to ask · Suggested format · Design Read — declare before iterating · Tip
4. Run `/amw-sketch` to iterate ≥ 3 ASCII variants with the user; loop until an explicit satisfaction token is received.
5. Apply the AI-slop-avoid.md gate over the approved direction before conversion.
6. Convert to HTML via `/amw-ascii-to-html`, apply tokens, and deliver via `/amw-preview`.
7. Route specialized requests (diagrams, infographics, video, SEO, forms) to the appropriate executor skill — see [downstream-executors](./references/downstream-executors.md) for the full routing table.
> [downstream-executors.md] Input — gather context for Rule 1 · Plan phase — satisfy Rule 2 in ASCII · Output — render the approved direction · Text visualization — ASCII artifacts for PRs, ADRs, terminals, and chat · Validation + reference · Tier-4 specialists (on-demand, Phase B only)

## ASCII-first plan phase (the default workflow)

**When the user asks for a webpage design, the plan phase runs in ASCII, not HTML.** Iterate on position, size, alignment, and component choice in ASCII until the user explicitly says they are satisfied. Only then convert to HTML.

```
  User asks for a design
         │
         ▼
  ┌────────────────────────────────────┐
  │ 1. design-principles orchestrator  │
  │    Rules 1, 2, 3 apply             │
  └────────────────┬───────────────────┘
                   ▼
  ┌────────────────────────────────────┐
  │ 2. /amw-sketch                      │
  │    3 ASCII variants → feedback →   │
  │    revision → feedback → ...       │
  │    (loop until "ship it")          │
  └────────────────┬───────────────────┘
                   ▼
  ┌────────────────────────────────────┐
  │ 3. /amw-ascii-to-html (terminal)    │
  │    tokens applied, chrome wrapped, │
  │    preview via /amw-preview         │
  └────────────────────────────────────┘
```

The loop is cheap because ASCII costs ~1% of the tokens of HTML iteration. Users can push 10+ revisions without context decay. Iteration ends only on the canonical satisfaction tokens: `yes`, `ship it`, `convert it`, `that's the one`, `perfect`, `done`. Ambiguous acknowledgement (`looks good`, `sure`, `ok`, `fine`) is NOT approval — ask a clarifying question before proceeding.

Skip the loop only when the user has already committed to a layout (e.g. they pasted a wireframe and said "build this"). Otherwise, ASCII-first is default.

## 7-step execution flow

```
1. Read the brief       → decide whether this skill fires
2. Gather context       → request UI kit / brand assets / references; ask if absent
3. Question checklist   → use question-templates.md; ask ≥ 10 questions
4. Declare visual system → state "I will use X font + Y palette + Z spacing rhythm"
5. Build variants       → ≥ 3 in ASCII via /amw-sketch; loop to satisfaction
6. Self-check           → run ai-slop-avoid.md over the chosen direction
7. Deliver              → /amw-ascii-to-html → /amw-preview → show the user
```

## Runtime conventions

Detailed conventions (Tweaks live-tuning protocol, dimensional hard limits, animation stack order, decision tree, file-management rules, workflow rhythm) live in [runtime-conventions](./references/runtime-conventions.md). Every HTML/SVG emitter under this orchestrator MUST follow them.
> [runtime-conventions.md] Tweaks live-tuning mode (recommended) · Dimensional hard limits (no discussion) · Animation stack order · Decision tree — which file to load when · File-management rules · Workflow rhythm

## Downstream executor sub-skills

Full per-skill routing table (40+ executors across input / plan / output / text-visualization / validation tiers, plus Tier-4 specialists) lives in [downstream-executors](./references/downstream-executors.md). Load that reference when picking a sub-skill for a specific task domain (diagram type, video, infographic, SEO, etc.).
> [downstream-executors.md] Input — gather context for Rule 1 · Plan phase — satisfy Rule 2 in ASCII · Output — render the approved direction · Text visualization — ASCII artifacts for PRs, ADRs, terminals, and chat · Validation + reference · Tier-4 specialists (on-demand, Phase B only)

## Output

Produces a single artifact at the path specified in the 7-step execution flow — an HTML file (plan-phase → ASCII → approval → HTML), SVG, or other format as directed by the executor skill.

## Error Handling

On failure, the skill emits a non-zero exit code or returns a structured error in the response. See `bin/` scripts for tool-specific error semantics.

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Resources

- [two-mode-summary](./references/two-mode-summary.md) — quick summary of command vs main-agent mode.
> [two-mode-summary.md] Command mode (fast path) · Main-agent mode (requirements path) · Approval gate invariant
- [two-mode-workflow](./references/two-mode-workflow.md) — authoritative deep-dive on Phase A/B contract.
> [two-mode-workflow.md] Sub-agent delegation (Main-agent mode only) · Mode Detection · Phase A — Iterative Low-Fi Loop · Phase B — Implementation and Spawning · Scenario Testing via dev-browser (mandatory in Phase B) · Anti-Patterns
- [three-hard-rules](./references/three-hard-rules.md) — full text of the three hard rules + last-resort path.
> [three-hard-rules.md] Rule 1: Gather design context before designing · Rule 2: Deliver at least three variants, baseline → advanced → experimental · Rule 3: Reject every AI-slop pattern
- [agent-authoring-philosophy](./references/agent-authoring-philosophy.md) — judgment layer vs recipe layer; canonical 14-section sub-agent template.
> [agent-authoring-philosophy.md] Skills and agents are not the same kind of thing · What an agent actually needs · Why the judgment layer matters in this plugin specifically · The 14-section canonical template · What this document is NOT · Cross-references
- [agent-interaction-patterns](./references/agent-interaction-patterns.md) — cross-agent data hand-offs, one-way tree topology.
> [agent-interaction-patterns.md] Topology invariants · Phase A data flow · Phase B data flow · What main-agent does between sub-agent calls · Error propagation · Why this topology (instead of peer-to-peer) · Enforcement
- [authority-hierarchy](./references/authority-hierarchy.md) — veto power and conflict-resolution rules.
> [authority-hierarchy.md] Domains and authority · Veto power — what it means · Resolution rules by conflict pattern · How main-agent applies the hierarchy · What the hierarchy does NOT do · Enforcement
- [sub-agent-return-contract](./references/sub-agent-return-contract.md) — YAML return-contract schema every sub-agent emits.
> [sub-agent-return-contract.md] Schema · Field semantics · Markdown body structure · How main-agent consumes the contract · Contract invariants (enforced by smoke tests)
- [skill-invocation-protocol](./references/skill-invocation-protocol.md) — DO/DON'T rules agents follow when invoking skills.
> [skill-invocation-protocol.md] The problem · The protocol · Examples · Enforcement
- [phase-a-frozen-spec](./references/phase-a-frozen-spec.md) — Phase A.5 frozen-spec format and producer contract.
- [project-output-routing](./references/project-output-routing.md) — detection rules for project-inferred artifact output paths.
- [pivot-formats](./references/pivot-formats.md) — ASCII / DESIGN.md / Diagram-IR pivot formats.
- [downstream-executors](./references/downstream-executors.md) — full sub-skill routing table (Input / Plan / Output / Text-Visualization / Validation tiers).
- [runtime-conventions](./references/runtime-conventions.md) — Tweaks protocol, dimensional limits, animation stack, decision tree, file-management.
- [ai-slop-avoid](ai-slop-avoid.md) — 26 patterns to reject + positive-stance section.
- [question-templates](question-templates.md) — universal must-ask + task-specific question checklists.
- [typography-system](typography-system.md), [color-system](color-system.md), [spacing-rhythm](spacing-rhythm.md) — canonical token references.
- [design-heuristics](design-heuristics.md) — Gestalt / Fitts / Hick principles for "something feels off" diagnosis.
- [TECH-ux-laws-encyclopedia](./references/TECH-ux-laws-encyclopedia.md) — full 31-law reference (Fitts, Hick, Miller, Doherty, Goal-Gradient, Von Restorff, Tesler, Jakob, Pareto, Zeigarnik, Peak-End, Aesthetic-Usability, Cognitive Load, Information Foraging, 7 Gestalt principles, Banner Blindness, Serial Position, Chunking, Fogg, Sigmoid, Norman's vocabulary, Postel, Conway, Hofstadter); [quick-reference table](./references/TECH-ux-laws-quick-reference-table.md).

## Token systems

The plugin's design-token contract spans four mandatory families. Every DESIGN.md, every preset, every wireframe-builder emission resolves through these. Load the relevant file when authoring or auditing tokens:

- [TECH-token-system-color-roles](./references/TECH-token-system-color-roles.md) — 14 mandatory semantic color roles (primary/secondary/tertiary/surface/background/error + on-* pairs) with WCAG-AA pair-contrast invariants.
- [TECH-token-system-spacing-and-grid](./references/TECH-token-system-spacing-and-grid.md) — 4/8pt baseline, 10-step spacing scale, 12-col / 16-col grid + 6 breakpoints.
- [TECH-token-system-elevation-and-radius](./references/TECH-token-system-elevation-and-radius.md) — 8-layer z-index table, 7-tier elevation/shadow scale, 7-step radius scale with role-mapped defaults.
- [TECH-token-system-density-modes](./references/TECH-token-system-density-modes.md) — compact / comfortable / spacious as a multiplier over the spacing scale; responsive vs user-toggle decision matrix.

## Process and craft references

Load when the relevant trigger applies — not blanket-required on every project.

- [TECH-influence-and-persuasion](./references/TECH-influence-and-persuasion.md) — Cialdini's 7 principles mapped to UI patterns + 8-category friction audit + conversion-impact data; gate for landing / pricing / checkout / signup flows.
- [TECH-cross-cultural-design](./references/TECH-cross-cultural-design.md) — Wu-Xing 5-phase palette + Fibonacci spacing + 0.75× typographic waterfall + Swiss 12/16-col grid; load when audience is East Asian or aesthetic is Swiss-modernist.
- [TECH-enterprise-system-overrides](./references/TECH-enterprise-system-overrides.md) — IBM Carbon / Shopify Polaris / Trimble Modus / Adobe Spectrum override table + 3-tier (Global / Semantic / Component) token architecture + agentic UX patterns (Tool → Copilot → Agent + intent modeling + audit trails).
- [TECH-css-modern-syntax](./references/TECH-css-modern-syntax.md) — `oklch()` / `color-mix()` / `light-dark()` / `@container` / `@layer` / `@scope` / native nesting / `:has()` / `@starting-style` / View Transitions / anchor positioning / Tailwind v4 native-CSS features + fallback strategies.

## Closing note

Ninety percent of design failures come from not asking enough questions, not enough context, and delivering only one option. Treat this SKILL.md as a checklist; walk every step.

"Fast output" and "good design" are not the same thing. Use ASCII-first iteration to get both — fast iteration *and* good judgment.
