---
name: amw-ux-designer
description: UX-process methodology — user research plans, persona creation, journey/empathy maps, usability-test protocols, WCAG AA audits, IA (card sort / tree test). Triggers on "user research plan", "persona template", "heuristic review", "WCAG audit", "IA review", "journey map". Does NOT trigger on "design a page" (design-principles), "PRD to flows" (ux-flows), "evaluate this page" (ux-evaluator). Use when producing a UX plan, persona, or journey map. Trigger with "user research plan".
version: 0.1.0
---

# UX Designer

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

UX-process methodology reference covering the full 5-phase research-to-handoff lifecycle: Discover (user research, interviews, 5 Whys), Define (personas, journey maps, empathy maps), Ideate (task flows, IA card sort), Prototype & Test (usability-test protocols, moderated/unmoderated), and Handoff (WCAG AA checklists, microcopy review). Produces written deliverables only — personas, journey maps, IA sitemaps, usability plans, WCAG checklists. Visual output routes downstream to `amw-ascii-sketch` or `amw-ux-flows`.

## Instructions

1. Identify the UX-methodology deliverable requested: persona, user journey map, empathy map, research plan, usability-test protocol, IA sitemap, WCAG AA checklist, or microcopy review.
2. Walk the `## Technique selection` tree and open the relevant TECH reference file from `references/` (e.g. `TECH-ux-persona-template.md`, `TECH-ux-process-discover.md`).
3. Read the appropriate rule file from `rules/` for the deliverable type (e.g. [research](rules/research.md) for interviews/personas, [accessibility](rules/accessibility.md) for WCAG).
4. Produce the structured deliverable using the template in the TECH file (persona: goals/pain points/behaviors/quote; research plan: interview script + participant criteria + synthesis method; WCAG checklist: criteria + pass/fail per component).
5. Route downstream when done: PRD + wireframes → `../amw-ux-flows/`; visual iterations → `../amw-ascii-sketch/`; evaluation of an existing design → `../amw-ux-evaluator/`.

See `## Usage` below.

## Examples

See [TECH-ux-persona-template](references/TECH-ux-persona-template.md) for a complete persona example ("Sarah, The Busy Parent") and [TECH-ux-process-discover](references/TECH-ux-process-discover.md) for a user-research plan example.
> [TECH-ux-persona-template.md] What it does · When to use · How it works · Minimal example · Good persona · Bad persona · Gotchas · Cross-references

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during Phase A (UX methodology deliverables) or Phase B (WCAG audit, IA review). Skill's techniques are NOT limited to what matching commands expose.

## Position in flow

PLAN (Phase A support). Provides UX-process methodology (research → define → ideate → prototype → handoff) that complements design-principles' visual focus. Produces written deliverables (personas, journey maps, flow analyses, usability-test plans, WCAG checklists) that feed downstream visual skills.

## Trigger conditions
Activate only on UX-process-specific phrases:
- "user research", "research plan", "user interviews", "5 Whys"
- "create personas", "persona template", "build a persona"
- "user journey map", "empathy map", "pain points"
- "user flow diagram", "task flow", "happy path and error states"
- "usability test plan", "moderated/unmoderated test", "task success rate"
- "accessibility review", "WCAG audit", "WCAG AA checklist"
- "information architecture", "card sort", "tree test", "navigation audit"
- "microcopy review", "button copy", "error message review"

Do **not** activate on generic "design a page", "make a UI", "landing page", "wireframe a dashboard" — those belong to the orchestrator (`design-principles`).

## Prerequisites
- runtime_binaries: none (methodology reference)
- python_packages: none
- npm_packages: none

## Usage
Invoked by the orchestrator or directly when a UX-process trigger fires. Reads the appropriate rule file from `rules/` and returns a structured deliverable using the templates below.

**Deliverables produced:**
- Persona (goals, pain points, behaviors, quote)
- User flow (entry point, steps, error states, decision points)
- Design review (usability issues by severity, accessibility concerns with WCAG references, strengths)
- Research plan (interview script, participant criteria, synthesis method)
- WCAG AA audit checklist

**Rule files (read on demand):**
- [research](rules/research.md) — user interviews, personas, synthesis
- [accessibility](rules/accessibility.md) — WCAG AA, inclusive design
- [information-architecture](rules/information-architecture.md) — navigation, content organization
- [interaction-design](rules/interaction-design.md) — user flows, microcopy
- [visual-design](rules/visual-design.md) — hierarchy, design system essentials

**Handoff:**
- When the user has a PRD and wants wireframes → route to [SKILL](../amw-ux-flows/SKILL.md)
- When the user wants visual design iterations → return methodology output, then route to [SKILL](../amw-ascii-sketch/SKILL.md) for 3-variant proposals
- When the user wants validation on an existing design → route to [SKILL](../amw-ux-evaluator/SKILL.md)

## Technique selection / References

Each TECH file under `./references/` follows the standard TOC: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references.

**UX process phases (5):**
- [TECH-ux-process-discover](./references/TECH-ux-process-discover.md) — Phase 1: Discover & Research
> [TECH-ux-process-discover.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-ux-process-define](./references/TECH-ux-process-define.md) — Phase 2: Define
> [TECH-ux-process-define.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-ux-process-ideate](./references/TECH-ux-process-ideate.md) — Phase 3: Ideate & Design
> [TECH-ux-process-ideate.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-ux-process-prototype](./references/TECH-ux-process-prototype.md) — Phase 4: Prototype & Test
> [TECH-ux-process-prototype.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-ux-process-handoff](./references/TECH-ux-process-handoff.md) — Phase 5: Handoff & Iterate
> [TECH-ux-process-handoff.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

**Persona + rule references:**
- [TECH-ux-persona-template](./references/TECH-ux-persona-template.md) — persona template + good vs bad examples
> [TECH-ux-persona-template.md] What it does · When to use · How it works · Minimal example · Good persona · Bad persona · Gotchas · Cross-references
- [TECH-ux-rule-research](./references/TECH-ux-rule-research.md) — interviews + personas + synthesis
> [TECH-ux-rule-research.md] What it does · When to use · How it works · Interview planning · During interviews · Synthesis · Good vs bad questions · Minimal example · Gotchas · Cross-references
- [TECH-ux-rule-accessibility](./references/TECH-ux-rule-accessibility.md) — WCAG AA + inclusive design
> [TECH-ux-rule-accessibility.md] What it does · When to use · How it works · WCAG AA (minimum floor) — four POUR pillars · Inclusive design patterns (beyond compliance) · Testing checklist · Minimal example · Gotchas · Cross-references
- [TECH-ux-rule-ia](./references/TECH-ux-rule-ia.md) — information architecture
> [TECH-ux-rule-ia.md] What it does · When to use · How it works · Navigation structure · Navigation patterns · Mobile specifics · Content organization · Information scent · Search as navigation · Minimal example · Gotchas · Cross-references
- [TECH-ux-rule-interaction](./references/TECH-ux-rule-interaction.md) — flows + microcopy
> [TECH-ux-rule-interaction.md] What it does · When to use · How it works · Flow best practices · Multi-step flows · Error recovery · Microcopy · Specific rules · Minimal example · Gotchas · Cross-references
- [TECH-ux-rule-visual](./references/TECH-ux-rule-visual.md) — visual hierarchy + design system
> [TECH-ux-rule-visual.md] What it does · When to use · How it works · Establishing hierarchy · Typography scale · Color usage · Layout · Design-system essentials · Component documentation · Minimal example · Gotchas · Cross-references

<!-- end of references -->

## Completion checklist

Verify all items before reporting complete. FAIL on any triggers a remediation loop.

- Inputs captured verbatim — no silent paraphrasing.
- At least one `TECH-*.md` consulted and cited in the report.
- Output passes Non-negotiables (below).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- Cross-skill hand-offs documented.
- User-facing filename is descriptive English.

## Output

Two outputs per invocation:

1. **Artifact(s)** — UX methodology deliverables (personas, journey maps, IA sitemaps, wireframe instructions). Output path is determined by project inference per [project-output-routing](../amw-design-principles/references/project-output-routing.md) (user-supplied path → framework convention → existing `./design/` → `./design/references/` or `./design/wireframes/` → `/tmp/amw-ux-designer-<slug>/`).
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references

2. **Job-completion report** — `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<slug>_<8-char-hash>.md` containing: Inputs · Method · Artifacts · Checklist · Deviations. Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. **Every artifact MUST be linked from the report.**

## Resources
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator; applies the three hard rules
- [SKILL](../amw-ux-flows/SKILL.md) — PRD → wireframes pipeline
- [SKILL](../amw-ux-evaluator/SKILL.md) — end-of-process validation
- [question-templates](../amw-design-principles/question-templates.md) — patterns for user research
> [question-templates.md] Universal must-ask (every design task) · Task-specific additions · Questions NOT to ask · Suggested format · Design Read — declare before iterating · Tip
- [design-heuristics](../amw-design-principles/design-heuristics.md) — Gestalt/Fitts/Hick laws
> [design-heuristics.md] I. Gestalt's five principles (organizing the visual field) · II. Fitts's Law · III. Hick's Law · IV. Miller's Law (7 ± 2) · V. Jakob's Law · VI. The four dimensions of visual hierarchy · VII. F-Pattern vs Z-Pattern reading · VIII. Peak-End Rule · IX. Aesthetic-Usability Effect · Self-check list · X. Refactoring-UI atomic audit rules (T-054)
- [TECH-ux-laws-encyclopedia](../amw-design-principles/references/TECH-ux-laws-encyclopedia.md) — 31 laws (Fitts, Hick, Miller, Doherty, Goal-Gradient, Peak-End, Cognitive Load, all Gestalt, Norman's affordance/signifier/mapping/constraints/feedback, Fogg, Jakob, Pareto, etc.) — cite by name when justifying persona, journey-map, or usability-test design choices.
> [TECH-ux-laws-encyclopedia.md] Motor and perceptual laws (Fitts, Hick-Hyman, Doherty) · Memory and cognition (Miller, Cognitive Load, Information Foraging, Chunking) · Motivation and emotion (Goal-Gradient, Von Restorff, Zeigarnik, Peak-End, Aesthetic-Usability, Jakob, Pareto) · Gestalt perception (Proximity, Similarity, Closure, Continuity, Common Region, Common Fate, Figure-Ground) · Attention and habituation (Banner Blindness, Serial Position) · Behavioral models (Fogg B=MAT, Sigmoid Adoption) · Norman's vocabulary (Mental Model, Affordance, Signifier, Mapping, Constraints, Feedback) · Meta-laws of software (Tesler, Postel, Conway, Hofstadter) · Cross-references
- `../amw-design-principles/starter-components/design-canvas.html` — 8pt-grid canvas for handoff

## Non-negotiables
- Activates only on UX-process-specific triggers. Do not take over generic design intent.
- Output is methodology deliverables (personas, journey maps, wireframe instructions, WCAG checklists), not final visual design — the latter routes through `ascii-sketch` → `ascii-to-html`.
- Personas must be based on real research data. Flag "aspirational" or demographic-only personas as anti-patterns.
- Accessibility is not negotiable: every design-review deliverable includes a WCAG AA section.
- Priority order when issues conflict: User Needs → Accessibility → Usability → Visual Hierarchy → Consistency.

## Error Handling
- Generating personas without requiring real research input (anti-pattern).
- Recommending visual design changes instead of returning methodology output.
- Skipping accessibility review on design-review deliverables.
- Producing wireframes directly instead of handing off to `ux-flows` or `ascii-sketch`.
- Using vague microcopy recommendations ("Submit", "OK") instead of specific verbs ("Create Account", "Delete Project").
