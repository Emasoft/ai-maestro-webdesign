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

## The three hard rules (violating any one of these is a failure)

1. **Gather context before designing.** Require design system, brand tokens, or reference examples. The `last resort` fallback is `amw-ui-ux-reasoning` — do not fall back to "let me guess."
2. **Always produce at least three variants** (baseline → advanced → experimental). Single-answer output is a failure mode. Use `amw-ascii-sketch` when the user hasn't committed to HTML yet — it is cheap to iterate.
3. **Reject AI-slop patterns.** The full list is in [ai-slop-avoid](ai-slop-avoid.md). Any HTML output runs a final check against that file before delivery.

Full text, rationale, and last-resort path: [three-hard-rules](./references/three-hard-rules.md).

These rules apply to every skill in the plugin. Sub-skills inherit them via the orchestrator; they do not override them.

## Prerequisites

Standard plugin runtime — no skill-specific prerequisites beyond the global plugin dependencies.

## Instructions

1. Read the brief and decide if this skill fires (broad design vocabulary: design, UI, mockup, landing page, wireframe, prototype, slide, deck, poster, website).
2. Gather context: request UI kit, brand assets, or reference examples; use `amw-ui-ux-reasoning` as last resort if none are available.
3. Run the question checklist from [question-templates](question-templates.md) (ask ≥ 10 questions), then declare the visual system (font + palette + spacing rhythm).
4. Run `/amw-sketch` to iterate ≥ 3 ASCII variants with the user; loop until an explicit satisfaction token is received.
5. Apply the AI-slop-avoid.md gate over the approved direction before conversion.
6. Convert to HTML via `/amw-ascii-to-html`, apply tokens, and deliver via `/amw-preview`.
7. Route specialized requests (diagrams, infographics, video, SEO, forms) to the appropriate executor skill — see [downstream-executors](./references/downstream-executors.md) for the full routing table.

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

## Downstream executor sub-skills

Full per-skill routing table (40+ executors across input / plan / output / text-visualization / validation tiers, plus Tier-4 specialists) lives in [downstream-executors](./references/downstream-executors.md). Load that reference when picking a sub-skill for a specific task domain (diagram type, video, infographic, SEO, etc.).

## Output

Produces a single artifact at the path specified in the 7-step execution flow — an HTML file (plan-phase → ASCII → approval → HTML), SVG, or other format as directed by the executor skill.

## Error Handling

On failure, the skill emits a non-zero exit code or returns a structured error in the response. See `bin/` scripts for tool-specific error semantics.

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Resources

- [two-mode-summary](./references/two-mode-summary.md) — quick summary of command vs main-agent mode.
- [two-mode-workflow](./references/two-mode-workflow.md) — authoritative deep-dive on Phase A/B contract.
- [three-hard-rules](./references/three-hard-rules.md) — full text of the three hard rules + last-resort path.
- [agent-authoring-philosophy](./references/agent-authoring-philosophy.md) — judgment layer vs recipe layer; canonical 14-section sub-agent template.
- [agent-interaction-patterns](./references/agent-interaction-patterns.md) — cross-agent data hand-offs, one-way tree topology.
- [authority-hierarchy](./references/authority-hierarchy.md) — veto power and conflict-resolution rules.
- [sub-agent-return-contract](./references/sub-agent-return-contract.md) — YAML return-contract schema every sub-agent emits.
- [skill-invocation-protocol](./references/skill-invocation-protocol.md) — DO/DON'T rules agents follow when invoking skills.
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
