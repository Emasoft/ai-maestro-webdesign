---
name: amw-ux-evaluator
description: Systematic UX evaluation of a rendered UI via 3-dimension framework (Position, Weight, Spacing) cross-checked against Balsamiq, Nielsen, Material. Triggers on "evaluate UX", "review this component", "check button design", "evaluate layout", "UX feedback on", "run UX audit". Does NOT trigger on "design a page", "mockup", "style my page" — routes to `design-principles`. Use when evaluating a UI against heuristics. Trigger with /amw-eval.
author: ai-maestro-webdesign
---

# UX Evaluator

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Triggers are evaluation-specific only — `design-principles` routes already-rendered HTML here when the workflow calls for scored feedback before ship.

## Overview

Systematic UX evaluation of rendered HTML or live URLs using a 3-dimension framework: Position (reading flow, adjacency conventions), Visual Weight (hierarchy, fill vs ghost vs icon-only), and Spacing (gaps, touch targets, rhythm). Each dimension scores Pass / Warn / Fail with concrete selector + computed-style evidence. Cross-checks against Balsamiq, Nielsen, and Material conventions. Produces a structured evaluation report with prioritized recommendations (P1 = UX-breaking, P2 = suboptimal, P3 = polish). Read-only — never modifies HTML.

## Activation

Callable directly via the `/amw-eval` command. Also invoked by the `design-principles` orchestrator as a Phase B validation step after HTML is produced in Main-agent mode. In Main-agent mode the orchestrator may apply the full 3-dimension framework and heuristic checklist beyond what the `/amw-eval` command parameters expose.

This skill is **autonomous and self-contained** — any agent can use it by reading this SKILL.md and its references.

## Position in flow

**VALIDATION (Phase B).** Runs on finished HTML or already-rendered components (not sketches, not wireframes) to produce scored feedback against Balsamiq + Nielsen + Material conventions. Positioned **after** `../amw-ascii-to-html/` has produced an HTML variant and **before** the user accepts it as shippable. Never writes HTML — reads, scores, reports.

## Trigger conditions

Activate only on explicit evaluation intents: "evaluate the UX of this page", "review this component", "score this layout", "check button design", "UX feedback on …", "evaluate this page against Nielsen heuristics", "run a UX audit on …", "is this button positioned correctly", "check the spacing / visual weight of …".

Do **not** activate on generic design intent ("design a landing page", "make it look nicer", "build the UI", "style my page"). Those are owned by `design-principles`, which routes here only once an HTML artifact exists.

## Prerequisites

- **runtime_binaries (system):** none beyond plugin baseline (`node ≥ 22`).
- **runtime_binaries (via /amw-init):** none unique. Live-URL inspection delegates DOM + computed-style capture to `../amw-dev-browser/`; static HTML is read from disk directly.

## Instructions

1. Gather context: identify the component (hero, navbar, CTA stack, form, pricing card), the evaluation trigger, and the input source (local HTML → `Read`; live URL → `../amw-dev-browser/`).
2. Score the three dimensions — Position, Visual Weight, Spacing — using concrete selector + computed-style evidence; each dimension gets Pass / Warn / Fail.
3. Produce a structured Markdown report with every Fail/Warn citing the selector, computed-style value, and the convention violated; prioritize findings as P1 (UX-breaking), P2 (suboptimal), P3 (polish).
4. When invoked by an agent (not via `/amw-eval` direct), ALSO emit a YAML scorecard sidecar (`<eval-report>.scorecard.yaml`) with `severity` tiers and an `overall.verdict` downstream agents gate on — full contract in [TECH-uxeval-scorecard](references/TECH-uxeval-scorecard.md) (TOC embedded in the Technique catalog below).

## Usage

Invoked by `/amw-eval [file.html | url]` or directly on an evaluation trigger. The full four-step workflow (gather context → score the 3 dimensions → report → hand off), the per-dimension scoring table, the canonical Markdown report template, and the P1/P2/P3 priority rubric live in [uxeval-usage-and-report-template](references/uxeval-usage-and-report-template.md). In short: Step 1 classify the component and capture the input source; Step 2 score Position / Visual Weight / Spacing as Pass / Warn / Fail with concrete selector + computed-style evidence; Step 3 emit the Markdown report (every Fail/Warn cites evidence; prose-only verdicts are rejected); Step 4 hand off — all Pass → emit and stop, Warnings → user decides, Fails → recommendations return to `design-principles`.

## Technique catalog

Every technique is in `./references/TECH-uxeval-*.md`. Each contains: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references.

- [TECH-uxeval-3-dimension-framework](./references/TECH-uxeval-3-dimension-framework.md) — Position / Visual Weight / Spacing rubric
> [TECH-uxeval-3-dimension-framework.md] What it does · When to use · How it works · Verdict rubric per dimension · Evaluation workflow · Minimal example · Gotchas · Cross-references
- [TECH-uxeval-button-conventions](./references/TECH-uxeval-button-conventions.md) — button design rules
- [TECH-uxeval-form-conventions](./references/TECH-uxeval-form-conventions.md) — labels / submit / errors / spacing
> [TECH-uxeval-form-conventions.md] What it does · When to use · How it works · Position · Visual weight · Spacing · Accessibility floor · Minimal example · Gotchas · Cross-references
- [TECH-uxeval-navigation-conventions](./references/TECH-uxeval-navigation-conventions.md) — logo / primary / utilities
> [TECH-uxeval-navigation-conventions.md] What it does · When to use · How it works · Position (top bar, LTR) · Theme toggle placement (industry cross-check) · Visual weight · Utility control visual weight · Spacing · Mobile patterns · Minimal example · Gotchas · Cross-references
- [TECH-uxeval-output-format](./references/TECH-uxeval-output-format.md) — structured evaluation report
- [TECH-uxeval-scorecard](./references/TECH-uxeval-scorecard.md) — machine-parseable severity-tiered YAML scorecard sidecar (T-097); emitted alongside the Markdown report in agent-orchestrated mode
- [TECH-uxeval-priority-rubric](./references/TECH-uxeval-priority-rubric.md) — P1 / P2 / P3
> [TECH-uxeval-priority-rubric.md] What it does · When to use · How it works · Assignment rule · Output structure · Minimal example · Gotchas · Cross-references

## Quick-lookup conventions

Full reference in [balsamiq-button-principles](references/balsamiq-button-principles.md). Summary:

Full rules in the `TECH-uxeval-*-conventions` refs (Technique catalog above). Summary:

- **Buttons:** primary right + filled; secondary left + ghost; utility far right icon-only; ≥ 24 px between groups, ≥ 44 px mobile touch; verb-first labels.
- **Navigation:** logo left, primary centre/after-logo, utilities right; active state distinct.
- **Forms:** labels above/left, submit bottom-right or full-width, errors adjacent.
- **Industry cross-check:** secondary LEFT / primary RIGHT (GitHub, Stripe, Google, Notion); theme toggle far-right after user menu.

## Completion checklist

Verify every item before reporting complete. FAIL triggers a remediation loop.

- Inputs captured verbatim (no silent paraphrasing).
- At least one `TECH-*.md` from `references/` was consulted and cited.
- Output passes the Non-negotiables section.
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
- Cross-skill hand-offs documented.
- User-facing filename is descriptive English.

## Examples

See [TECH-uxeval-output-format](references/TECH-uxeval-output-format.md) for a complete evaluation report example ("Pricing Page CTA Evaluation").
> [TECH-uxeval-output-format.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

## Output

This skill produces THREE kinds of output:

1. **Artifact(s)** — UX evaluation `.md` reports scoring Position / Visual Weight / Spacing. Output path determined by **project inference** per [project-output-routing](../amw-design-principles/references/project-output-routing.md) (priority: user-supplied → framework convention → `./design/<subtype>/` → generic fallback → `/tmp/amw-ux-evaluator-<slug>/` scratch).
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
2. **Scorecard sidecar (T-097)** — when invoked by an agent (browser-tester, main-orchestrator, etc.) the evaluator ALSO emits a machine-parseable YAML scorecard at `<eval-report>.scorecard.yaml` with severity tiers (`blocker | high | medium | low`), per-dimension verdicts, evidence references, and an overall verdict (`PASS | NEEDS_CHANGES | BLOCKED`). Schema and aggregation rules: [TECH-uxeval-scorecard](references/TECH-uxeval-scorecard.md). OPTIONAL when invoked via `/amw-eval` directly (the human Markdown report is sufficient).
3. **Job-completion report** at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md` with sections: Inputs, Method, Artifacts (each `- <path> — <desc> — **How to use:** <tip> — **Next steps:** <followup>`), Checklist (PASS/FAIL/N/A), Deviations.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. Every artifact MUST be linked.

## Resources

- Upstream: [amw-design-principles](../amw-design-principles/SKILL.md) (orchestrator), [spacing-rhythm](../amw-design-principles/spacing-rhythm.md), [typography-system](../amw-design-principles/typography-system.md), [color-system](../amw-design-principles/color-system.md), [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
> [color-system.md] I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
> [typography-system.md] I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
> [spacing-rhythm.md] I. 8pt grid system · II. Fibonacci spacing rhythm (large-scale) · III. Vertical rhythm (baseline grid) · IV. Hit targets (tappable areas) · V. Alignment · VI. Three principles of whitespace · VII. Border radius · VIII. Shadow system · IX. Self-check
- Inputs: [amw-dev-browser](../amw-dev-browser/SKILL.md) (live-page DOM + computed-style capture).
- Related: [amw-ascii-to-html](../amw-ascii-to-html/SKILL.md) (upstream producer), [amw-ui-ux-reasoning](../amw-ui-ux-reasoning/SKILL.md) (industry-specific anti-pattern taxonomy).
- References: [balsamiq-button-principles](references/balsamiq-button-principles.md) — full button-design corpus.
> [balsamiq-button-principles.md] Core Principles · Use Conventional Labels · Say Exactly What Happens · Primary and Secondary Should Look Different · Primary Action on the Right · Use Adequate Spacing · Make Buttons Look Clickable · Size Appropriately · Use Icons Wisely · Consider Loading States · Error Prevention · Button Hierarchy Summary · Common Mistakes
- UX-law citations: [TECH-ux-laws-encyclopedia](../amw-design-principles/references/TECH-ux-laws-encyclopedia.md) — 31-law reference; the evaluator cites laws by name in P1/P2/P3 findings (Fitts for hit-target sizing, Hick for choice overload, Von Restorff for primary-CTA isolation, Banner Blindness for CTA tone, Feedback Loop for action affordance) — see also [quick-reference table](../amw-design-principles/references/TECH-ux-laws-quick-reference-table.md).
> [TECH-ux-laws-quick-reference-table.md] Motor and perceptual laws · Memory and cognition laws · Motivation and emotion laws · Gestalt grouping principles · Attention, behavior, and system laws · How to use this table · Cross-references
> [TECH-ux-laws-encyclopedia.md] Motor and perceptual laws (Fitts, Hick-Hyman, Doherty) · Memory and cognition (Miller, Cognitive Load, Information Foraging, Chunking) · Motivation and emotion (Goal-Gradient, Von Restorff, Zeigarnik, Peak-End, Aesthetic-Usability, Jakob, Pareto) · Gestalt perception (Proximity, Similarity, Closure, Continuity, Common Region, Common Fate, Figure-Ground) · Attention and habituation (Banner Blindness, Serial Position) · Behavioral models (Fogg B=MAT, Sigmoid Adoption) · Norman's vocabulary (Mental Model, Affordance, Signifier, Mapping, Constraints, Feedback) · Meta-laws of software (Tesler, Postel, Conway, Hofstadter) · Cross-references
- Art-direction diagnostic lens: [TECH-art-direction-tells](../amw-design-principles/references/TECH-art-direction-tells.md) — a QA-pass checklist of ~16 subtle art-direction tells (pill-scale coexistence, color voltage, weight ceiling, polarity-flipped bands, alpha-overlay scale, elevation discipline, …). Apply it when the evaluation is diagnosing *why* a design reads as deliberate vs sloppy, not just whether components pass.
> [TECH-art-direction-tells.md] What this is · How to run the pass · Surface-rhythm tells · Token-coexistence tells · Color-discipline tells · Elevation-discipline tells · Composition-discipline tells · Cross-references
- Command: `/amw-eval`.

## Non-negotiables

- **Read-only.** Never modifies the HTML it evaluates. Fixes are proposed; applying them is routed by `design-principles`.
- **Every Fail or Warn cites concrete evidence** — selector, computed-style value, DOM attribute, or measured pixel distance. Prose-only verdicts are rejected.
- **All three dimensions, always.** Partial evaluations are a failure mode.
- **Cite authoritative conventions, not preference.** Balsamiq, Nielsen, Material, or observable industry pattern (GitHub, Stripe, Notion, VS Code Docs).
- **Does not substitute for Lighthouse or axe-core.**
- **Prioritization is mandatory.** Every recommendation carries P1 / P2 / P3.
- **Scorecard sidecar in agent-orchestrated mode is mandatory.** When the evaluator is invoked by an agent (not via `/amw-eval` direct), the YAML scorecard at `<eval-report>.scorecard.yaml` is required alongside the Markdown report; downstream agents gate on `overall.verdict != BLOCKED`. Schema: [TECH-uxeval-scorecard](references/TECH-uxeval-scorecard.md).
> [TECH-uxeval-scorecard.md] What this is · When to emit · File naming and location · Schema — the YAML 1.2 contract · Field semantics · Severity vs priority — the distinction · How the verdict aggregates · Worked example — full YAML · Consumer contracts · Cross-references
- **Run the `ai-slop-avoid.md` scan before emitting a Pass.** Non-skippable.

## Error Handling

- **Auth-walled URL → blank DOM:** ask user for session cookie or local copy; don't score a login page.
- **JS-heavy SPA missing component:** use `dev-browser` with wait flag; don't score a skeleton state.
- **Viewport-dependent layout scored at wrong width:** specify viewport; evaluate breakpoints separately if ambiguous.
- **Missing computed-style data (CSS-in-JS / shadow DOM):** fall back to screenshot-based visual evaluation; flag missing evidence; never fabricate selectors.
- **Report emitted without evidence:** reject and re-run. Evidence is a hard requirement.
- **All Warnings downgraded to Pass:** Warnings remain Warnings. The user decides, not the evaluator.
- **Activated on generic design intent:** "Design a landing page" belongs to `design-principles`. Activate only when HTML exists.
