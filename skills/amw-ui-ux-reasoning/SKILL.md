---
name: amw-ui-ux-reasoning
description: LAST-RESORT fallback library — 161 reasoning rules, 67 UI styles, 161 color palettes, 57 font pairings, 24 landing-page patterns — consulted ONLY when no design system, brand tokens, or reference exists. Triggers on "pick a style for me", "I have no design system", "choose a palette", "suggest a font pairing", "what UI style should I use". Does NOT trigger on generic design intent. Use when no design system is available. Trigger with "pick a style for me".
version: 0.1.0
author: ai-maestro-webdesign
---

# UI/UX Reasoning (Last-Resort Library)

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Only run this skill when design-principles has determined that Rule 1 context-gathering has no anchor — no UI kit, no brand tokens, no reference URL, no existing components, and the user cannot name a style. If any anchor exists, skip this skill entirely.

## Overview

Last-resort fallback library consulted only when design-principles has exhausted Rule 1 context-gathering with no result. Collapses an infinite-choice space into a confirmable shortlist: 3 style + 3 palette + 3 font DNA candidates drawn from 67 UI styles, 161 color palettes, and 57 font pairings — all pre-filtered against [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md). Produces named anchors only; the user picks, then `amw-ascii-sketch` resumes with those anchors.

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

## Instructions

1. Confirm activation: only proceed if design-principles has already attempted Rule 1 context-gathering and found no anchors.
2. Acknowledge the fallback in one sentence: "No anchors found — three visual-DNA candidates from 67 styles / 161 palettes / 57 font pairings, filtered against ai-slop."
3. Present three style candidates (name, 3-5 keywords, best-for, one-sentence feel), pre-filtered against [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
4. Present three palette candidates (mood tag, primary/secondary/CTA/background/text, one-sentence industry fit) and three font-pair candidates (heading + body, pairing rationale, tone).
5. Ask the user to pick one from each column (or mix); do not emit HTML, ASCII wireframes, or CSS — those belong to `../amw-ascii-sketch/`.

## Usage

When design-principles routes here, emit exactly one response:

1. **Acknowledge the fallback** (one sentence).
2. **Three style candidates** — each: name, 3-5 keywords, best-for, one-sentence feel.
3. **Three palette candidates** — each: mood tag, primary/secondary/CTA/background/text, one-sentence industry fit.
4. **Three font-pair candidates** — each: heading + body, why the pair works, tone.
5. **Ask the user to pick one from each column, or mix across columns.**

Do not generate HTML, ASCII wireframes, or CSS. This skill's only job is to collapse an infinite-choice space into a confirmable shortlist.

## Non-negotiables

- **Never runs on the happy path.** If any anchor exists (reference URL, brand doc, existing component, screenshot), skip this skill entirely.
- **Every candidate is screened against [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) BEFORE emission.** Inter, Roboto, Arial, system-default stacks are never proposed. Purple-blue linear gradients, rounded-card + 4px accent bar, AI-illustrated mascots — all filtered out at source.
- **At least three candidates per dimension.** Never a single recommendation — matches design-principles Rule 2.
- **Palettes must be oklch-convertible** per [color-system](../amw-design-principles/color-system.md). If a palette can't be cleanly re-expressed in oklch, drop it.
- **Font pairings must satisfy [typography-system](../amw-design-principles/typography-system.md)** — two-family limit, full weight coverage, Google-Fonts-available.
- **Does not emit HTML or code.** Output is named anchors. Handoff to `../amw-ascii-sketch/` is mandatory.
- **Industry anti-patterns travel with every candidate.** If the rule for "finance" says avoid playful fonts and neon, the fallback output must annotate that constraint on fintech-leaning candidates.

## Technique catalog

Every technique is in `./references/TECH-*.md`. Each contains: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references.

- [TECH-uiux-design-system-generator](./references/TECH-uiux-design-system-generator.md) — end-to-end composition
- [TECH-uiux-rules-catalog](./references/TECH-uiux-rules-catalog.md) — 161 reasoning rules
- [TECH-uiux-styles-catalog](./references/TECH-uiux-styles-catalog.md) — 67 named visual languages
- [TECH-uiux-palettes-catalog](./references/TECH-uiux-palettes-catalog.md) — 161 industry-matched palettes
- [TECH-uiux-font-pairings-catalog](./references/TECH-uiux-font-pairings-catalog.md) — 57 heading+body combos
- [TECH-uiux-lp-patterns-catalog](./references/TECH-uiux-lp-patterns-catalog.md) — 24 conversion-optimized structures
- [TECH-uiux-pre-delivery-checklist](./references/TECH-uiux-pre-delivery-checklist.md) — universal pre-delivery checklist
- Industry-specific rules: [TECH-uiux-rule-fintech](./references/TECH-uiux-rule-fintech.md), [TECH-uiux-rule-food-restaurant](./references/TECH-uiux-rule-food-restaurant.md), [TECH-uiux-rule-healthcare](./references/TECH-uiux-rule-healthcare.md), [TECH-uiux-rule-luxury-ecommerce](./references/TECH-uiux-rule-luxury-ecommerce.md), [TECH-uiux-rule-saas-dashboard](./references/TECH-uiux-rule-saas-dashboard.md)

## Completion checklist

Verify every item before reporting complete. FAIL triggers a remediation loop.

- Inputs captured verbatim (no silent paraphrasing).
- At least one `TECH-*.md` from `references/` was consulted and cited.
- Output passes the Non-negotiables section.
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
- Cross-skill hand-offs documented.
- User-facing filename is descriptive English.

## Examples

1. **Fallback activation.** User says "I don't have a design system, pick a style for me" after design-principles exhausted Rule 1. Output: three contrasting style anchors (e.g., Glassmorphism / Brutalist / Refined-modern) with ascii-friendly palette + font-pairing summaries. User picks; orchestrator passes anchors to `amw-ascii-sketch` for Rule-2 variants.
2. **Industry-aware guardrails.** Fallback for "finance dashboard" — playful fonts and neon palettes excluded a priori. User sees only candidates that survive both raw taxonomy AND industry-specific rules.
3. **ai-slop filter applied.** Raw taxonomy returns Inter/Roboto pairing and a purple-blue gradient. Pairing rejected by `ai-slop-avoid` filter; substituted with a non-trope alternative (e.g., Söhne / IBM Plex Sans + a flat oklch palette).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — UI/UX reasoning notes (picked rules, palette, font pairing, pattern) as `.md`. Output path determined by **project inference** per [project-output-routing](../amw-design-principles/references/project-output-routing.md) (priority: user-supplied → framework convention → `./design/<subtype>/` → generic fallback → `/tmp/amw-ui-ux-reasoning-<slug>/` scratch).
2. **Job-completion report** at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md` with sections: Inputs, Method, Artifacts (each `- <path> — <desc> — **How to use:** <tip> — **Next steps:** <followup>`), Checklist (PASS/FAIL/N/A), Deviations.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. Every artifact MUST be linked.

## Resources

- Upstream: [amw-design-principles](../amw-design-principles/SKILL.md) (orchestrator), [color-system](../amw-design-principles/color-system.md), [typography-system](../amw-design-principles/typography-system.md), [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md), [question-templates](../amw-design-principles/question-templates.md).
- Downstream: [amw-ascii-sketch](../amw-ascii-sketch/SKILL.md) — resumes variant exploration with picked anchors.

## Error Handling

- **Activating too eagerly.** Triggering on "design a landing page" instead of "pick a style for me". Orchestrator must have exhausted Rule 1 first.
- **Single-option output.** Emitting "I suggest Glassmorphism" instead of three candidates. Violates Rule 2.
- **Skipping the ai-slop filter.** Proposing Inter/Roboto, purple-blue gradients, or the 4px accent bar because they appear in the raw library. The filter runs BEFORE emission — always.
- **Emitting HTML or CSS.** This skill produces anchors only.
- **Forgetting the handoff.** After the user picks, routing must return to `../amw-ascii-sketch/` with the chosen anchors as visual DNA — not straight to `ascii-to-html`, because Rule 2 still needs three plan-phase variants.
- **Ignoring industry anti-patterns.** Proposing a playful-font / neon-palette combo for a finance product because the raw taxonomy allowed it — the reasoning rules for that industry forbid it.
