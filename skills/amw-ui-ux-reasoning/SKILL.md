---
name: amw-ui-ux-reasoning
description: LAST-RESORT fallback library — 161 reasoning rules, 67 UI styles, 161 color palettes, 57 font pairings, 24 landing-page patterns — consulted ONLY when no design system, brand tokens, or reference exists. Triggers on "pick a style for me", "I have no design system", "choose a palette", "suggest a font pairing", "what UI style should I use". Does NOT trigger on generic design intent. Use when no design system is available. Trigger with "pick a style for me".
author: ai-maestro-webdesign
---

# UI/UX Reasoning (Last-Resort Library)

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Only run this skill when design-principles has determined that Rule 1 context-gathering has no anchor — no UI kit, no brand tokens, no reference URL, no existing components, and the user cannot name a style. If any anchor exists, skip this skill entirely.

## Overview

Last-resort fallback library consulted only when design-principles has exhausted Rule 1 context-gathering with no result. Collapses an infinite-choice space into a confirmable shortlist: 3 style + 3 palette + 3 font DNA candidates drawn from 67 UI styles, 161 color palettes, and 57 font pairings — all pre-filtered against [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md). Produces named anchors only; the user picks, then `amw-ascii-sketch` resumes with those anchors.
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during Phase A as a fallback library when Rule 1 context-gathering finds no anchor. The orchestrator may consult any reasoning rule, palette, font pairing, or landing-page pattern from this skill without command-layer restriction.

This skill is **autonomous and self-contained** — any agent can use it by reading this SKILL.md and its references.

## Position in flow

PLAN phase (Phase A fallback sub-branch). Normal plan-phase routing goes through `../amw-ascii-sketch/`. This skill is consulted only when ASCII sketching has nothing to anchor on.

```
design-principles
    ├─ Rule 1 context found?  YES → ../amw-ascii-sketch/ (normal path)
    └─ Rule 1 context EMPTY → ui-ux-reasoning (this skill)
                                 │ 3 style + 3 palette + 3 font DNA candidates
                                 ▼
                              user picks
                                 ▼
                              ../amw-ascii-sketch/ resumes with anchors
```

Output is a set of named visual-DNA anchors, not HTML. The user picks; `ascii-sketch` produces the three plan-phase variants required by Rule 2.

## Trigger conditions

Activate ONLY when the user's message contains an explicit "no context" signal AND design-principles has already asked and failed to gather anchors. Valid phrases: "pick a style for me", "I don't have a design system", "no preference — just make it professional", "choose a palette for me", "suggest a font pairing", "what UI style should I use", "surprise me" (after orchestrator confirmed no anchor).

Do NOT trigger on: "design a landing page", "make a nice site", "build a dashboard", "I want something modern". Those go through the orchestrator's normal context-gathering path.

## Prerequisites

- **runtime_binaries:** none — the reasoning library is inlined in companion reference files.
- **npm_packages (optional):** `uipro-cli` (`npm install -g uipro-cli`) exposes the same taxonomy as a CLI. Not wired into the orchestrator; the skill works identically without it.

## Library inventory

| Dimension | Count | Purpose |
|---|---|---|
| Reasoning rules | 161 | Industry / product-type decisions — layout archetype, style priority, color mood, anti-patterns |
| UI styles | 67 | Named visual languages (Glassmorphism, Brutalism, Editorial, Soft UI, Bento Grid, Claymorphism, Data-Dense, …) with keywords + best-for |
| Color palettes | 161 | Industry-matched, slotted into primary / secondary / CTA / background / text with mood tags |
| Font pairings | 57 | Heading + body combos with Google Fonts URLs; pre-filtered to exclude ai-slop defaults |
| Landing-page patterns | 24 | Conversion-optimized section structures, CTA placement, social-proof cadence |

All outputs are descriptive anchors, not production tokens. Any palette chosen here must be re-expressed in oklch via [color-system](../amw-design-principles/color-system.md) before output.
> [color-system.md] I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list

## Instructions

1. Confirm activation: only proceed if design-principles has already attempted Rule 1 context-gathering and found no anchors.
2. Acknowledge the fallback in one sentence: "No anchors found — three visual-DNA candidates from 67 styles / 161 palettes / 57 font pairings, filtered against ai-slop."
3. Present three style candidates — each: name, 3-5 keywords, best-for, one-sentence feel — pre-filtered against the **ai-slop-avoid** checklist (link + TOC under Overview above).
4. Present three palette candidates (mood tag, primary/secondary/CTA/background/text, one-sentence industry fit) and three font-pair candidates (heading + body, pairing rationale, tone).
5. Ask the user to pick one from each column, or mix across columns; do not emit HTML, ASCII wireframes, or CSS — those belong to `../amw-ascii-sketch/`.

This skill's only job is to collapse an infinite-choice space into a confirmable shortlist — never a single recommendation.

## Usage

See **Instructions** above — when design-principles routes here, emit exactly one response covering all five steps (acknowledge fallback → 3 style → 3 palette → 3 font-pair candidates → ask the user to pick one from each column, or mix). For each font-pair candidate state heading + body, why the pair works, tone.

## Non-negotiables

- **Never runs on the happy path.** If any anchor exists (reference URL, brand doc, existing component, screenshot), skip this skill entirely.
- **Every candidate is screened against ai-slop-avoid BEFORE emission** (link + full checklist embedded under Overview). Inter, Roboto, Arial, system-default stacks are never proposed. Purple-blue linear gradients, rounded-card + 4px accent bar, AI-illustrated mascots — all filtered out at source.
- **At least three candidates per dimension.** Never a single recommendation — matches design-principles Rule 2.
- **Palettes must be oklch-convertible** per **color-system** (link + TOC under Library inventory). If a palette can't be cleanly re-expressed in oklch, drop it.
- **Font pairings must satisfy [typography-system](../amw-design-principles/typography-system.md)** — two-family limit, full weight coverage, Google-Fonts-available.
> [typography-system.md] I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
- **Does not emit HTML or code.** Output is named anchors. Handoff to `../amw-ascii-sketch/` is mandatory.
- **Industry anti-patterns travel with every candidate.** If the rule for "finance" says avoid playful fonts and neon, the fallback output must annotate that constraint on fintech-leaning candidates.

## Technique catalog

Every technique is in `./references/TECH-*.md`. Each contains: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references.

- [TECH-uiux-design-system-generator](./references/TECH-uiux-design-system-generator.md) — end-to-end composition
> [TECH-uiux-design-system-generator.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-uiux-rules-catalog](./references/TECH-uiux-rules-catalog.md) — 161 reasoning rules
> [TECH-uiux-rules-catalog.md] What it does · When to use · How it works · Minimal example · Gotchas · Top 10 distinctive rules — broken out as individual TECH files · Cross-references
- [TECH-uiux-styles-catalog](./references/TECH-uiux-styles-catalog.md) — 67 named visual languages
> [TECH-uiux-styles-catalog.md] What it does · When to use · How it works · Representative styles (partial list — full 67 are in the upstream corpus) · Minimal example · Gotchas · Cross-references
- [TECH-uiux-palettes-catalog](./references/TECH-uiux-palettes-catalog.md) — 161 industry-matched palettes
> [TECH-uiux-palettes-catalog.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-uiux-font-pairings-catalog](./references/TECH-uiux-font-pairings-catalog.md) — 57 heading+body combos
> [TECH-uiux-font-pairings-catalog.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-uiux-lp-patterns-catalog](./references/TECH-uiux-lp-patterns-catalog.md) — 24 conversion-optimized structures
> [TECH-uiux-lp-patterns-catalog.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-uiux-pre-delivery-checklist](./references/TECH-uiux-pre-delivery-checklist.md) — universal pre-delivery checklist
> [TECH-uiux-pre-delivery-checklist.md] What it does · When to use · How it works · Accessibility · Responsive · Performance · Interaction · Minimal example · Gotchas · Cross-references
- Industry-specific rules: [TECH-uiux-rule-fintech](./references/TECH-uiux-rule-fintech.md), [TECH-uiux-rule-food-restaurant](./references/TECH-uiux-rule-food-restaurant.md), [TECH-uiux-rule-healthcare](./references/TECH-uiux-rule-healthcare.md), [TECH-uiux-rule-luxury-ecommerce](./references/TECH-uiux-rule-luxury-ecommerce.md), [TECH-uiux-rule-saas-dashboard](./references/TECH-uiux-rule-saas-dashboard.md)
> [TECH-uiux-rule-saas-dashboard.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-uiux-rule-luxury-ecommerce.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-uiux-rule-healthcare.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-uiux-rule-food-restaurant.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-uiux-rule-fintech.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

## Completion checklist

Verify every item before reporting complete. FAIL triggers a remediation loop.

- Inputs captured verbatim (no silent paraphrasing).
- At least one `TECH-*.md` from `references/` was consulted and cited.
- Output passes the Non-negotiables section.
- No AI-slop per the **ai-slop-avoid** checklist (link + TOC under Overview).
- Cross-skill hand-offs documented.
- User-facing filename is descriptive English.

## Examples

1. **Fallback activation.** User says "I don't have a design system, pick a style for me" after design-principles exhausted Rule 1. Output: three contrasting style anchors (e.g., Glassmorphism / Brutalist / Refined-modern) with ascii-friendly palette + font-pairing summaries. User picks; orchestrator passes anchors to `amw-ascii-sketch` for Rule-2 variants.
2. **Industry-aware guardrails.** Fallback for "finance dashboard" — playful fonts and neon palettes excluded a priori. User sees only candidates that survive both raw taxonomy AND industry-specific rules.
3. **ai-slop filter applied.** Raw taxonomy returns Inter/Roboto pairing and a purple-blue gradient. Pairing rejected by `ai-slop-avoid` filter; substituted with a non-trope alternative (e.g., Söhne / IBM Plex Sans + a flat oklch palette).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — UI/UX reasoning notes (picked rules, palette, font pairing, pattern) as `.md`. Output path determined by **project inference** per [project-output-routing](../amw-design-principles/references/project-output-routing.md) (priority: user-supplied → framework convention → `./design/<subtype>/` → generic fallback → `/tmp/amw-ui-ux-reasoning-<slug>/` scratch).
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
2. **Job-completion report** at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md` with sections: Inputs, Method, Artifacts (each `- <path> — <desc> — **How to use:** <tip> — **Next steps:** <followup>`), Checklist (PASS/FAIL/N/A), Deviations.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. Every artifact MUST be linked.

## Resources

- Upstream: [amw-design-principles](../amw-design-principles/SKILL.md) (orchestrator); **color-system**, **typography-system**, **ai-slop-avoid** (each linked with its TOC embedded above); and [question-templates](../amw-design-principles/question-templates.md).
> [question-templates.md] Universal must-ask (every design task) · Task-specific additions · Questions NOT to ask · Suggested format · Quick questions before we start · Design Read — declare before iterating · Tip
- Downstream: [amw-ascii-sketch](../amw-ascii-sketch/SKILL.md) — resumes variant exploration with picked anchors.

## Error Handling

- **Activating too eagerly.** Triggering on "design a landing page" instead of "pick a style for me". Orchestrator must have exhausted Rule 1 first.
- **Single-option output.** Emitting "I suggest Glassmorphism" instead of three candidates. Violates Rule 2.
- **Skipping the ai-slop filter.** Proposing Inter/Roboto, purple-blue gradients, or the 4px accent bar because they appear in the raw library. The filter runs BEFORE emission — always.
- **Emitting HTML or CSS.** This skill produces anchors only.
- **Forgetting the handoff.** After the user picks, routing must return to `../amw-ascii-sketch/` with the chosen anchors as visual DNA — not straight to `ascii-to-html`, because Rule 2 still needs three plan-phase variants.
- **Ignoring industry anti-patterns.** Proposing a playful-font / neon-palette combo for a finance product because the raw taxonomy allowed it — the reasoning rules for that industry forbid it.
