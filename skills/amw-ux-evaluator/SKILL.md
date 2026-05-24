---
name: amw-ux-evaluator
description: Systematic UX evaluation of a rendered UI via 3-dimension framework (Position, Weight, Spacing) cross-checked against Balsamiq, Nielsen, Material. Triggers on "evaluate UX", "review this component", "check button design", "evaluate layout", "UX feedback on", "run UX audit". Does NOT trigger on "design a page", "mockup", "style my page" — routes to `design-principles`. Use when evaluating a UI against heuristics. Trigger with /amw-eval.
version: 0.1.0
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

## Usage

Invoked by `/amw-eval [file.html | url]` or directly on an evaluation trigger.

**Step 1 — Gather context.** Identify the component, the reason for evaluation, and the input source. Classify the component's role (primary CTA, secondary action, utility control, navigation, form field).

**Step 2 — Score the 3 dimensions.** For every inspected component:

| Dimension | What to analyze | Key questions |
|---|---|---|
| **Position** | Location relative to other elements, reading flow, adjacency | Does position follow conventions (primary right, utility far right)? Discoverable? |
| **Visual Weight** | Fill vs ghost vs icon-only, color, shadow, size, font weight | Does it compete with the primary action? Is the hierarchy legible at a glance? |
| **Spacing** | Gaps from adjacent elements, touch target, rhythm | Adequate separation (≥ 8 px intra-group, ≥ 24 px between groups)? Touch targets ≥ 44 × 44 px mobile? |

Each dimension gets one of: **Pass** (matches convention), **Warn** (acceptable but suboptimal — improvement attached), **Fail** (breaks convention or accessibility floor — recommendation mandatory).

**Step 3 — Report.** Markdown output, every Fail / Warn citing concrete evidence (selector, computed-style value, DOM attribute, measured pixel distance). Prose-only verdicts are rejected.

```markdown
## [Component Name] Evaluation

### Current State
- **Position:** [selector + coordinates]
- **Visual Weight:** [selector + computed-style evidence]
- **Spacing:** [measured gaps + selector pairs]

### Analysis
| Dimension | Verdict | Evidence | Rationale |
|---|---|---|---|
| Position | Pass / Warn / Fail | `selector` + value | Why + cited convention |
| Visual Weight | Pass / Warn / Fail | `selector` + computed-style | Why + cited convention |
| Spacing | Pass / Warn / Fail | measured gap + selectors | Why + cited convention |

### Verdict: PASS / NEEDS CHANGES

### Recommendations
| Priority | Change | Evidence | Cited principle |
|---|---|---|---|
| P1 | [Specific change] | [selector / value] | [e.g. Balsamiq #4 — primary on right] |
| P2 | [Specific change] | [selector / value] | [e.g. Nielsen #4 — consistency] |
```

**Priority rubric:** **P1** breaks UX (wrong button order, inaccessible touch target, buried primary, contrast below AA). **P2** suboptimal but usable (tight spacing, non-standard utility placement, weak label). **P3** polish only (token drift, micro-alignment, aesthetic).

**Step 4 — Hand off.** All Pass → emit report and stop. Warnings only → report; user decides. Fails present → recommendations return to `design-principles`, which decides patch-in-place vs re-enter `../amw-ascii-sketch/`.

## Technique catalog

Every technique is in `./references/TECH-uxeval-*.md`. Each contains: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references.

- [TECH-uxeval-3-dimension-framework](./references/TECH-uxeval-3-dimension-framework.md) — Position / Visual Weight / Spacing rubric
- [TECH-uxeval-button-conventions](./references/TECH-uxeval-button-conventions.md) — button design rules
- [TECH-uxeval-form-conventions](./references/TECH-uxeval-form-conventions.md) — labels / submit / errors / spacing
- [TECH-uxeval-navigation-conventions](./references/TECH-uxeval-navigation-conventions.md) — logo / primary / utilities
- [TECH-uxeval-output-format](./references/TECH-uxeval-output-format.md) — structured evaluation report
- [TECH-uxeval-priority-rubric](./references/TECH-uxeval-priority-rubric.md) — P1 / P2 / P3

## Quick-lookup conventions

Full reference in [balsamiq-button-principles](references/balsamiq-button-principles.md). Summary:

- **Buttons:** primary right + filled + brand color; secondary left + ghost/outline; utility far right, icon-only. ≥ 24 px between groups, 8–12 px intra-group, ≥ 44 × 44 px mobile touch. Labels: "Sign Up" not "Get Started"; "Delete Account" not "Proceed"; verb-first.
- **Navigation:** logo left, primary nav centre or after logo, utilities (search / auth / theme) right. Active state clearly distinguished; nav does not compete with content.
- **Forms:** labels above/left of inputs; submit bottom, right-aligned or full-width; errors adjacent; label-to-input 0.25–0.5 rem; field-to-field 1–1.5 rem.
- **Industry cross-check:** button order secondary LEFT, primary RIGHT (GitHub, Stripe, Google, Notion). Theme toggle far right after user menu or in settings (GitHub, VS Code Docs, Stripe Docs).

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

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — UX evaluation `.md` reports scoring Position / Visual Weight / Spacing. Output path determined by **project inference** per [project-output-routing](../amw-design-principles/references/project-output-routing.md) (priority: user-supplied → framework convention → `./design/<subtype>/` → generic fallback → `/tmp/amw-ux-evaluator-<slug>/` scratch).
2. **Job-completion report** at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md` with sections: Inputs, Method, Artifacts (each `- <path> — <desc> — **How to use:** <tip> — **Next steps:** <followup>`), Checklist (PASS/FAIL/N/A), Deviations.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. Every artifact MUST be linked.

## Resources

- Upstream: [amw-design-principles](../amw-design-principles/SKILL.md) (orchestrator), [spacing-rhythm](../amw-design-principles/spacing-rhythm.md), [typography-system](../amw-design-principles/typography-system.md), [color-system](../amw-design-principles/color-system.md), [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
- Inputs: [amw-dev-browser](../amw-dev-browser/SKILL.md) (live-page DOM + computed-style capture).
- Related: [amw-ascii-to-html](../amw-ascii-to-html/SKILL.md) (upstream producer), [amw-ui-ux-reasoning](../amw-ui-ux-reasoning/SKILL.md) (industry-specific anti-pattern taxonomy).
- References: [balsamiq-button-principles](references/balsamiq-button-principles.md) — full button-design corpus.
- Command: `/amw-eval`.

## Non-negotiables

- **Read-only.** Never modifies the HTML it evaluates. Fixes are proposed; applying them is routed by `design-principles`.
- **Every Fail or Warn cites concrete evidence** — selector, computed-style value, DOM attribute, or measured pixel distance. Prose-only verdicts are rejected.
- **All three dimensions, always.** Partial evaluations are a failure mode.
- **Cite authoritative conventions, not preference.** Balsamiq, Nielsen, Material, or observable industry pattern (GitHub, Stripe, Notion, VS Code Docs).
- **Does not substitute for Lighthouse or axe-core.**
- **Prioritization is mandatory.** Every recommendation carries P1 / P2 / P3.
- **Run the `ai-slop-avoid.md` scan before emitting a Pass.** Non-skippable.

## Error Handling

- **Auth-walled URL → blank DOM:** ask user for session cookie or local copy; don't score a login page.
- **JS-heavy SPA missing component:** use `dev-browser` with wait flag; don't score a skeleton state.
- **Viewport-dependent layout scored at wrong width:** specify viewport; evaluate breakpoints separately if ambiguous.
- **Missing computed-style data (CSS-in-JS / shadow DOM):** fall back to screenshot-based visual evaluation; flag missing evidence; never fabricate selectors.
- **Report emitted without evidence:** reject and re-run. Evidence is a hard requirement.
- **All Warnings downgraded to Pass:** Warnings remain Warnings. The user decides, not the evaluator.
- **Activated on generic design intent:** "Design a landing page" belongs to `design-principles`. Activate only when HTML exists.
