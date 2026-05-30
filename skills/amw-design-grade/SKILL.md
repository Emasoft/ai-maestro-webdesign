---
name: amw-design-grade
description: >-
  Quantitative A-F design audit of a single artifact (URL, local HTML, or
  extracted DESIGN.md). Scores 8 dimensions 0-10, each with an evidence
  excerpt and letter grade, then emits an HTML report-card plus an SVG grade
  badge. Activates on narrow audit triggers — "grade this design", "design
  report card", "audit design quality", "design A-F score", "design badge",
  "rate this site's design". Does NOT activate on broad design vocabulary
  ("design a page", "build a UI") — those route to amw-design-principles.
version: 0.1.0
author: ai-maestro-webdesign (clean-room)
---

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Triggers are audit-specific only — `amw-design-principles` routes here when the user explicitly asks for a quantitative design assessment of an existing artifact. For comparative grading (two sites head-to-head) use `amw-design-battle`. For drift detection against a `DESIGN.md` spec use `amw-design-drift-audit`. For accessibility-only audit use `amw-accessibility-auditor-agent`.

## Overview

`amw-design-grade` performs a deterministic, evidence-backed audit of one design artifact and produces three deliverables:

1. A per-dimension table of scores (0-10) with one-line evidence excerpts
2. An HTML report card laying out the 8 dimensions, scores, grades, and overall verdict
3. An SVG badge encoding the overall letter grade for embedding in READMEs / project pages

The rubric is the authority. Every score must be backed by a concrete excerpt from the audited artifact (a token value, a CSS rule, a screenshot region, a measured contrast ratio). Subjective adjectives without a structural anchor are not evidence and produce a NULL score (the dimension is marked "insufficient evidence" rather than guessed).

This skill audits ONE artifact at a time. For two-up comparison see `amw-design-battle`.

## Inputs

The skill accepts ONE of:

- **A URL** — fetched via `amw-dev-browser` (DOM snapshot + computed styles + screenshots). Live-page audits require the user to have `dev-browser` installed (`/amw-init` handles this).
- **A local HTML file path** — opened directly; computed styles via headless render.
- **An extracted `DESIGN.md`** — token-only audit (no rendered evidence); dimensions that require rendered output (motion observed in practice, signature recognisability) score from the spec text and flag "spec-only" in evidence.
- **A live extraction result** — JSON produced by `amw-design-extract` from `designlang`; same as DESIGN.md mode plus any captured screenshots.

Mixed inputs (URL + DESIGN.md to grade implementation fidelity against intent) are valid and bias the rubric toward the consistency dimension.

## The 8-dimension rubric

The canonical rubric definitions, scoring criteria, and evidence requirements live in `references/TECH-rubric.md`. Load that file before any audit; do NOT score from memory. The 8 dimensions in canonical order:

1. **Palette** — colour-system coherence, OKLCH structure, chromatic balance, dark/light parity
2. **Typography** — type-scale ratio, family pairing, vertical-rhythm anchoring, optical adjustments
3. **Rhythm** — spacing-token discipline, baseline grid, density variance across sections
4. **Hierarchy** — primary-action discoverability, heading-level stack, visual weight order
5. **Motion** — duration/easing token discipline, prefers-reduced-motion compliance, purposefulness
6. **Accessibility** — WCAG-AA contrast ratios, focus-state visibility, semantic landmarks, hit-target sizes
7. **Consistency** — token reuse (no orphan values), component variant cohesion, repeated-pattern fidelity
8. **Signature** — recognisable identity beyond stock components, opinionated choices, memorable details

Each dimension scores 0-10. Letter grades are deterministic:

| Score range | Grade |
|---|---|
| 9.0-10.0 | A |
| 7.0-8.9 | B |
| 5.0-6.9 | C |
| 3.0-4.9 | D |
| 0.0-2.9 | F |

The **overall grade** is the unweighted arithmetic mean of the 8 dimensions, rounded to 1 decimal place, then mapped to a letter via the same table. The rubric is unweighted by design — every dimension is treated as equally important. If the user supplies an explicit weighting in the prompt ("prioritise accessibility 2x"), apply it and note the weighting in the report-card footer.

## Workflow

1. **Gather artifact.** URL → fetch with `amw-dev-browser` (snapshot DOM, computed styles, fold and full-page screenshots). Local HTML → headless render via the same browser. DESIGN.md → parse and identify which dimensions are spec-only.
2. **Load rubric.** Read `references/TECH-rubric.md` in full. Do NOT skip to a single dimension — the cross-dimension calibration notes at the bottom of the rubric matter for consistent scoring.
3. **Score each dimension.** For each of the 8 dimensions in order:
   - Identify the concrete evidence (token values, CSS rules, computed contrast ratios, screenshot crops).
   - Apply the per-dimension scoring criteria from `references/TECH-rubric.md`.
   - Record: dimension name, score 0-10, evidence excerpt (≤120 chars), grade letter.
   - If evidence is insufficient (e.g. motion dimension on a static DESIGN.md), score NULL and explain in evidence.
4. **Compute overall.** Arithmetic mean of the 8 scores. Skip NULL dimensions and divide by the number of scored dimensions (note the partial coverage in the report-card footer).
5. **Emit HTML report-card.** One H1 with overall letter and numeric, eight cards (one per dimension) showing score / grade / evidence excerpt, and a footer with: artifact source, audit timestamp, rubric version, any weighting applied, any NULL dimensions.
6. **Emit SVG badge.** A 200×60 SVG showing "DESIGN GRADE: X" where X is the overall letter; colour-coded background per grade (A green, B blue, C yellow, D orange, F red). The badge is self-contained — no external font references; embed system-font fallback stack.
7. **Cross-check before delivery.** Sanity-test: would a senior reviewer who has never seen this artifact arrive at the same letter grade given only the evidence excerpts? If not, revisit the weakest-evidence dimension.

## Output shape

Three files written to the user's working directory (or a path the user specifies):

- `design-grade-report.html` — the report-card
- `design-grade-badge.svg` — the embeddable badge
- `design-grade-data.json` — machine-readable record (artifact URL, per-dimension scores, evidence, timestamp, rubric version)

The JSON shape is canonical for downstream consumers (e.g. `amw-design-battle` reads two `design-grade-data.json` files to produce a head-to-head card). Schema:

```json
{
  "rubric_version": "1.0",
  "artifact": { "type": "url|html|design.md|extract", "ref": "<source>" },
  "audited_at": "<ISO 8601 + TZ>",
  "weighting": null,
  "dimensions": [
    { "name": "palette", "score": 8.5, "grade": "B", "evidence": "8-step OKLCH ramp, hue 264, chroma .04-.18; dark/light parity confirmed" },
    { "name": "typography", "score": 7.0, "grade": "B", "evidence": "1.250 minor-third scale, Inter+JetBrains Mono pair, line-height 1.5 body / 1.2 display" },
    { "name": "rhythm", "score": 6.5, "grade": "C", "evidence": "4px base + 8/12/16/24/32/48, but 3 sections breach with 14/20/28px orphans" },
    { "name": "hierarchy", "score": 9.0, "grade": "A", "evidence": "primary CTA 48px / accent-bg / white-text; secondary 36px / outline; 12px gap to body copy" },
    { "name": "motion", "score": null, "grade": null, "evidence": "spec-only — no rendered transitions observed; durations stated 150/250/400ms with ease-out" },
    { "name": "accessibility", "score": 5.0, "grade": "C", "evidence": "body 4.7:1 (AA pass); accent CTA 3.8:1 (fails AA on 14px); focus rings present but 1px / low-chroma" },
    { "name": "consistency", "score": 8.0, "grade": "B", "evidence": "tokens reused across 87% of inspected rules; 3 orphan colour values in footer + form" },
    { "name": "signature", "score": 4.0, "grade": "D", "evidence": "shadcn defaults dominate; no opinionated typography pairing or chromatic identity beyond hue choice" }
  ],
  "overall": { "score": 6.9, "grade": "C" },
  "files": {
    "html": "<path>",
    "svg": "<path>",
    "json": "<path>"
  }
}
```

## Non-negotiables

1. **Evidence-backed scoring.** Every non-NULL score MUST cite a concrete excerpt. "Looks balanced" / "feels coherent" are NOT evidence. If you cannot point to a token value, computed style, contrast ratio, or screenshot region, the score is NULL.
2. **Rubric is the contract.** Always load `references/TECH-rubric.md` before scoring. Do NOT score from memory; cross-dimension calibration drifts within 5 audits.
3. **NULL is better than guessed.** When a dimension cannot be evaluated against the available artifact (e.g. motion on a static spec), mark NULL and explain in evidence. Never invent a score to keep the table tidy.
4. **No weighting unless the user asks.** Equal-weight mean is the default and the report-card footer says so. Custom weighting requires explicit user input and is logged in the footer.
5. **Badge is self-contained.** SVG must render in a stripped README — no external font fetches, no `<script>` tags, no remote resources. Use the system-font fallback stack.
6. **Audit one artifact at a time.** For comparisons use `amw-design-battle`; for drift use `amw-design-drift-audit`. Each skill has a single mandate.
7. **Subjective adjectives are flagged.** If the rubric criteria force a subjective judgement (e.g. "memorable details" on the signature dimension), state the criterion verbatim from the rubric in the evidence excerpt — never paraphrase to soften.

## Resources

- [`references/TECH-rubric.md`](references/TECH-rubric.md) — canonical 8-dimension scoring rubric (read before every audit)
- Companion skills: [`amw-design-battle`](../amw-design-battle/SKILL.md) (two-site comparison), [`amw-design-remix`](../amw-design-remix/SKILL.md) (reskin extracted designs), [`amw-design-drift-audit`](../amw-design-drift-audit/) (spec-fidelity audit)
- Input pipelines: [`amw-dev-browser`](../amw-dev-browser/SKILL.md), [`amw-design-extract`](../amw-design-extract/SKILL.md), [`amw-design-md`](../amw-design-md/SKILL.md)
- Style vocabulary: [`amw-design-system-presets`](../amw-design-system-presets/references/catalogue.md)
