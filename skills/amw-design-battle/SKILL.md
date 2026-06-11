---
name: amw-design-battle
description: >-
  Head-to-head two-site design comparison. Audits two artifacts on the same
  8-dimension rubric as amw-design-grade, then emits a battle card with
  per-dimension bars, per-dimension winner, and an overall verdict. Outputs
  battle.html / battle.md / battle.json. Activates on narrow comparison
  triggers — "compare two sites' design", "design battle", "head to head
  design audit", "which site has better design", "design comparison card".
  Does NOT activate on broad design vocabulary ("design a page", "build a
  UI") — those route to amw-design-principles.
version: 0.1.0
author: ai-maestro-webdesign (clean-room)
---

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Triggers are comparison-specific only — `amw-design-principles` routes here when the user explicitly asks for a head-to-head visual comparison of two artifacts. For single-artifact audit use `amw-design-grade`. For spec-vs-implementation drift use `amw-design-drift-audit`.

## Overview

`amw-design-battle` runs two `amw-design-grade` audits on two artifacts using the SAME canonical 8-dimension rubric, then synthesises a side-by-side comparison card. The card declares a winner per dimension, computes an overall verdict, and visualises the gap between the two artifacts with paired horizontal bars.

This skill is a SYNTHESISER, not a separate rubric. The scoring authority remains `amw-design-grade/references/TECH-rubric.md`. The comparison card adds only the head-to-head presentation layer; the scores themselves come from running the grader twice.

## Inputs

The skill accepts EXACTLY TWO artifacts. Each artifact independently is one of:

- A URL (fetched via `amw-dev-browser`)
- A local HTML file path
- An extracted `DESIGN.md`
- A live extraction JSON from `amw-design-extract`
- An existing `design-grade-data.json` produced by an earlier `amw-design-grade` run (skip the re-audit step)

The two artifacts SHOULD be from the same category for the comparison to be meaningful (two SaaS landing pages; two e-commerce product detail pages; two dashboard apps). Cross-category comparisons (a marketing landing vs an internal dashboard) are allowed but the report footer notes "categories differ; weighting is unweighted by default but consider domain-specific weighting."

The user MAY supply a label per artifact ("Site A: Stripe", "Site B: Square") to override the default labels (the URLs or file basenames).

## Workflow

1. **Audit both artifacts.** If a pre-existing `design-grade-data.json` is supplied for one or both sides, load it. Otherwise run `amw-design-grade` on each artifact using the same rubric version.
2. **Validate rubric parity.** If the two grade-data JSONs were produced under different `rubric_version` values, refuse to compare and tell the user: "rubric versions differ (A=1.0, B=1.1); re-grade A under the current rubric before comparing." Comparing across rubric versions is invalid.
3. **Compute per-dimension winner.** For each of the 8 dimensions:
   - If both scores are NULL → "n/a" (no winner).
   - If exactly one score is NULL → the non-NULL side wins by forfeit (mark "by forfeit" in the card).
   - If both scores are non-NULL and the absolute delta is ≤0.5 → "tie".
   - If both scores are non-NULL and delta is >0.5 → the higher score wins. Record the delta.
4. **Compute overall verdict.** Tally per-dimension wins (ignore "tie" and "n/a"). Whichever side has more dimension-wins is the overall winner. If equal, the verdict is "tie overall" and the report-card footer notes "no clear winner; consider which dimensions matter most for your context."
5. **Emit `battle.html`.** Two-column visual card (responsive: stacks on narrow viewports) with the structure documented in [TECH-comparison](references/TECH-comparison.md). Per-dimension paired bars in the same row so the gap is immediately visible.
6. **Emit `battle.md`.** Markdown summary: overall verdict, per-dimension table (Dimension | A score | B score | Winner | Delta | Evidence A | Evidence B), and the explicit list of dimensions where each side wins.
7. **Emit `battle.json`.** Machine-readable: the two source `design-grade-data.json` snapshots, the winner per dimension, the overall verdict, the rubric version. Downstream consumers (regression tests, dashboards) read this.
8. **Cross-check.** Print the dimension table to the user. Sanity-test that the winner list lines up with the score deltas — if Site A wins on a dimension where the recorded delta favours Site B, the JSON was assembled wrong; rebuild.

## Output shape

Three files written to the user's working directory (or a path the user specifies):

- `design-battle-card.html` — visual battle card (the canonical deliverable)
- `design-battle-summary.md` — markdown table + verdict
- `design-battle-data.json` — machine record

The HTML card structure and visual rules are documented in detail in [TECH-comparison](references/TECH-comparison.md). The MD summary contract is also there. The JSON schema:

```json
{
  "rubric_version": "1.0",
  "audited_at": "<ISO 8601 + TZ>",
  "side_a": { "label": "<user-supplied or default>", "grade_data": { /* full design-grade-data.json from side A */ } },
  "side_b": { "label": "<user-supplied or default>", "grade_data": { /* full design-grade-data.json from side B */ } },
  "per_dimension": [
    { "dimension": "palette", "a": 8.5, "b": 7.0, "winner": "a", "delta": 1.5 },
    { "dimension": "typography", "a": 7.0, "b": 9.0, "winner": "b", "delta": 2.0 },
    { "dimension": "rhythm", "a": 6.5, "b": 6.5, "winner": "tie", "delta": 0.0 },
    { "dimension": "hierarchy", "a": 9.0, "b": 8.5, "winner": "tie", "delta": 0.5 },
    { "dimension": "motion", "a": null, "b": 7.0, "winner": "b", "delta": null, "note": "by forfeit; A is spec-only" },
    { "dimension": "accessibility", "a": 5.0, "b": 8.0, "winner": "b", "delta": 3.0 },
    { "dimension": "consistency", "a": 8.0, "b": 7.5, "winner": "tie", "delta": 0.5 },
    { "dimension": "signature", "a": 4.0, "b": 9.0, "winner": "b", "delta": 5.0 }
  ],
  "wins": { "a": 1, "b": 4, "tie": 3 },
  "overall_verdict": "b",
  "verdict_note": "Side B wins overall (4 dimensions vs 1, 3 ties). The signature gap is the largest single delta."
}
```

## Non-negotiables

1. **Same rubric, same version.** Both audits MUST use the same `rubric_version`. Mixed versions → refuse to compare. State exactly why.
2. **Delta-based winner.** A 0.5 delta or less is always a tie. The threshold is non-negotiable; it prevents noise-driven "winners" on essentially equal scores.
3. **NULL handling is explicit.** "By forfeit" wins MUST be labelled in the card and the MD summary; never let a forfeit silently appear as a normal win.
4. **No weighting unless explicit.** The default is unweighted (one dimension = one vote). If the user requested weighting (e.g. "accessibility counts double"), the verdict_note records the weights used.
5. **Categories matter.** If the two artifacts are clearly different categories (marketing landing vs internal admin), state it in the footer — the rubric is universal but dimensional emphasis often differs by category.
6. **Cross-check before delivery.** Verify the winner column in the JSON matches the score deltas. Mismatch = stop and rebuild.
7. **No skipping the rubric.** Even when one side has a pre-computed grade-data.json, NEVER pretend to compare without loading and validating it. Trust the JSON only after the rubric_version check.

## When to recommend a different skill

- **Spec vs implementation drift, not two sites** → `amw-design-drift-audit`
- **One site, want a single grade** → `amw-design-grade`
- **Want to apply a different style to one site** → `amw-design-remix`
- **Want to compare 3+ sites** → run `amw-design-grade` on each, then assemble the comparison manually (battle card is two-sided by design; a 3-way card requires a different layout discipline)

## Resources

- [TECH-comparison](references/TECH-comparison.md) — battle card layout, per-dimension bar visual contract, MD summary template, verdict-note phrasing rules
> [TECH-comparison.md] `design-battle-card.html` — visual card · `design-battle-summary.md` — markdown table · Winner-determination algorithm (canonical) · Cross-category note (when to add it) · Verdict-note anti-patterns (do not emit)
- The scoring authority: [TECH-rubric](../amw-design-grade/references/TECH-rubric.md)
> [TECH-rubric.md] Palette · Typography · Rhythm · Hierarchy · Motion · Accessibility · Consistency · Signature · Cross-dimension calibration notes · NULL handling · Versioning
- Companion: [`amw-design-grade`](../amw-design-grade/SKILL.md) (single-artifact audit), [`amw-design-remix`](../amw-design-remix/SKILL.md) (reskin)
- Input pipelines: [`amw-dev-browser`](../amw-dev-browser/SKILL.md), [`amw-design-extract`](../amw-design-extract/SKILL.md)
