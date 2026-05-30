---
name: TECH-uxeval-scorecard
category: uxeval-output
source: T-097 (batch9 Wave 1 Track E)
also-in:
---

# TECH-uxeval-scorecard — Machine-parseable severity-tiered scorecard (T-097)

The YAML scorecard is a structured, machine-parseable sidecar that the `amw-ux-evaluator` skill emits alongside its existing Markdown report. It does NOT replace the Markdown report — the human-readable evaluation stays the canonical output; the scorecard is an additional artifact consumed programmatically by downstream agents.

## Table of Contents

- [1. What this is](#1-what-this-is)
- [2. When to emit](#2-when-to-emit)
- [3. File naming and location](#3-file-naming-and-location)
- [4. Schema — the YAML 1.2 contract](#4-schema--the-yaml-12-contract)
- [5. Field semantics](#5-field-semantics)
- [6. Severity vs priority — the distinction](#6-severity-vs-priority--the-distinction)
- [7. How the verdict aggregates](#7-how-the-verdict-aggregates)
- [8. Worked example — full YAML](#8-worked-example--full-yaml)
- [9. Consumer contracts](#9-consumer-contracts)
- [10. Cross-references](#10-cross-references)

---

## 1. What this is

The Markdown evaluation report produced by `amw-ux-evaluator` (see `TECH-uxeval-output-format.md`) is designed for human readers: prose rationale, a three-row analysis table, prioritized recommendations in Markdown. It cannot be mechanically consumed by `amw-browser-tester-agent` or by the main orchestrator without LLM re-parsing, which is fragile and token-expensive.

The YAML scorecard solves this. It encodes the same evaluation findings in a fixed schema that:

- Is parseable by `yaml.safe_load()` in Python with zero post-processing.
- Assigns `severity` to every dimension finding (distinct from `priority` — see §6).
- Provides a deterministic `overall.verdict` field (`PASS | NEEDS_CHANGES | BLOCKED`) that agents can gate on without reading prose.
- Carries a `recommendations` list with structured fields so the main orchestrator can surface action items without parsing free-form text.

The Markdown report remains unchanged. The YAML scorecard is written as a sidecar file with the same slug.

---

## 2. When to emit

**Always emit** when `amw-ux-evaluator` runs in agent-orchestrated mode — that is, when invoked by `amw-browser-tester-agent` or any other sub-agent as part of a Phase B pipeline. In this mode the scorecard is consumed programmatically and is as mandatory as the Markdown report.

**Optional** when invoked directly via the `/amw-eval` command from the user. In direct-command mode the user reads the Markdown; the YAML scorecard adds noise unless the user explicitly requests it (e.g. "give me the scorecard too" or "I need the YAML output").

---

## 3. File naming and location

The scorecard is a sidecar to the Markdown report, derived by appending `.scorecard.yaml` to the Markdown base slug:

```
<eval-report>.md               # existing Markdown report (unchanged)
<eval-report>.scorecard.yaml   # new YAML sidecar (this format)
```

Example:

```
reports/webdesigner/20260526_143200+0200-pricing-page-cta-eval.md
reports/webdesigner/20260526_143200+0200-pricing-page-cta-eval.scorecard.yaml
```

Both files live in the same directory, resolved by the canonical output-routing rules in `../../amw-design-principles/references/project-output-routing.md`.

---

## 4. Schema — the YAML 1.2 contract

Every field in the schema is documented in §5. Replace `<...>` placeholders with real values when emitting; the skeleton below uses illustrative examples inline.

```yaml
schema_version: "1.0"
scorecard_id: "a3f2b1c4-9d8e-4f7a-b5c6-1e2d3f4a5b6c"
component: "Pricing Page CTA"
input:
  type: "html"
  source: "/path/to/project/design/mockups/Pricing Page.html"
  viewport: "1440x900"
  captured_at: "2026-05-26T14:32:00+0200"
dimensions:
  position:
    verdict: "fail"
    severity: "high"
    evidence:
      - selector: ".pricing-cta .btn-primary"
        computed_style_or_value: "order: 1; float: left"
        convention_violated: "primary-right"
        convention_source: "Balsamiq #4 — primary action on the right"
      - selector: ".pricing-cta .btn-secondary"
        computed_style_or_value: "order: 2; float: right"
        convention_violated: "secondary-left"
        convention_source: "Industry: GitHub, Stripe, Notion — secondary precedes primary (left)"
    rationale: "Primary CTA is left of secondary, inverting the universal primary-right convention. Users accustomed to GitHub and Stripe will click the wrong button."
  visual_weight:
    verdict: "pass"
    severity: "none"
    evidence:
      - selector: ".pricing-cta .btn-primary"
        computed_style_or_value: "background-color: #1a73e8; font-weight: 600; padding: 12px 24px"
        convention_violated: ""
        convention_source: "Material Design — filled primary with sufficient weight delta"
    rationale: "Primary is filled brand color with heavier padding than the ghost secondary. Hierarchy is legible at a glance."
  spacing:
    verdict: "warn"
    severity: "low"
    evidence:
      - selector: ".pricing-cta .btn-primary + .btn-secondary"
        computed_style_or_value: "margin-left: 6px"
        convention_violated: "intra-group-gap-min-8"
        convention_source: "amw-ux-evaluator conventions — intra-group gap 8–12 px"
    rationale: "6 px intra-group gap is 2 px below the 8 px minimum. Buttons feel slightly cramped but remain functionally usable."
overall:
  verdict: "NEEDS_CHANGES"
  blocking_count: 0
  high_count: 1
  medium_count: 0
  low_count: 1
recommendations:
  - id: "REC-001"
    dimension: "position"
    severity: "high"
    priority: "P1"
    change: "Swap CTA order: move .btn-secondary before .btn-primary in the DOM (or reverse flex order)"
    evidence_ref: ".pricing-cta .btn-primary — order: 1; float: left"
    cited_principle: "Balsamiq #4 — primary action on the right"
  - id: "REC-002"
    dimension: "spacing"
    severity: "low"
    priority: "P3"
    change: "Increase intra-group gap from 6 px to 8 px (add margin-left: 8px on .btn-secondary)"
    evidence_ref: ".pricing-cta .btn-primary + .btn-secondary — margin-left: 6px"
    cited_principle: "amw-ux-evaluator conventions — intra-group gap 8–12 px"
ai_slop_scan:
  ran: true
  violations_high: 0
  violations_medium: 0
  violations_low: 0
notes: "Evaluated at desktop viewport 1440x900. Mobile breakpoint not included in this scorecard run — invoke separately for 375x812."
```

---

## 5. Field semantics

| Key | Type | Required | Allowed values | Consumer use |
|---|---|---|---|---|
| `schema_version` | string | yes | `"1.0"` | Version gate — consumers reject unknown versions |
| `scorecard_id` | string | yes | UUID4 | Correlates scorecard to Markdown report and to browser-tester YAML header |
| `component` | string | yes | free text, ≤ 80 chars | Display label in orchestrator summaries |
| `input.type` | string | yes | `"html"` or `"url"` | Determines how the source was read |
| `input.source` | string | yes | abs path or URL | Reproduced in test reports for traceability |
| `input.viewport` | string | yes | `"<width>x<height>"` | Viewport-sensitive evaluations depend on this |
| `input.captured_at` | string | yes | ISO 8601 with TZ offset | Timestamp for deduplication and audit trail |
| `dimensions.<dim>.verdict` | string | yes | `"pass"`, `"warn"`, `"fail"` | Primary gate per dimension |
| `dimensions.<dim>.severity` | string | yes | `"blocker"`, `"high"`, `"medium"`, `"low"`, `"none"` | Drives `overall.verdict` aggregation; `"none"` only when verdict is `"pass"` |
| `dimensions.<dim>.evidence` | list | yes (if verdict != pass) | list of evidence objects | Proof required; empty list only when verdict is `"pass"` |
| `evidence[].selector` | string | yes | CSS selector | Locates the element in DOM for re-inspection |
| `evidence[].computed_style_or_value` | string | yes | CSS property: value pair or measured value | Observable measurement, never prose |
| `evidence[].convention_violated` | string | yes | kebab-case short name | Machine-taggable convention breach |
| `evidence[].convention_source` | string | yes | "Balsamiq #N", "Nielsen #N", "Material …", "Industry: …" | Citation; never "I prefer" |
| `dimensions.<dim>.rationale` | string | yes | 1–3 sentence prose | Human-readable explanation passed through to Markdown report |
| `overall.verdict` | string | yes | `"PASS"`, `"NEEDS_CHANGES"`, `"BLOCKED"` | Main orchestrator gates Phase B on this field |
| `overall.blocking_count` | int | yes | ≥ 0 | Count of dimensions with severity=blocker |
| `overall.high_count` | int | yes | ≥ 0 | Count of dimensions with severity=high |
| `overall.medium_count` | int | yes | ≥ 0 | Count of dimensions with severity=medium |
| `overall.low_count` | int | yes | ≥ 0 | Count of dimensions with severity=low |
| `recommendations` | list | yes | list of recommendation objects | Consumed by orchestrator for action routing |
| `recommendations[].id` | string | yes | `"REC-NNN"` (3-digit, 1-indexed) | Stable reference within this scorecard |
| `recommendations[].dimension` | string | yes | `"position"`, `"visual_weight"`, `"spacing"`, `"cross-cutting"` | Routes fix to the right sub-agent |
| `recommendations[].severity` | string | yes | `"blocker"`, `"high"`, `"medium"`, `"low"` | Matches parent dimension severity unless cross-cutting |
| `recommendations[].priority` | string | yes | `"P1"`, `"P2"`, `"P3"` | Per existing priority rubric (§6) |
| `recommendations[].change` | string | yes | imperative sentence ≤ 120 chars | Actionable change description |
| `recommendations[].evidence_ref` | string | yes | selector + value | Locates the element the change applies to |
| `recommendations[].cited_principle` | string | yes | short name | Same citation as `evidence[].convention_source` |
| `ai_slop_scan.ran` | bool | yes | `true`, `false` | Was the slop scan executed? |
| `ai_slop_scan.violations_high` | int | yes | ≥ 0 | High-severity slop violations from `ai-slop-avoid.md` |
| `ai_slop_scan.violations_medium` | int | yes | ≥ 0 | Medium-severity slop violations |
| `ai_slop_scan.violations_low` | int | yes | ≥ 0 | Low-severity slop violations |
| `notes` | string | optional | free text | Caveats about SPA rendering, viewport ambiguity, incomplete data |

---

## 6. Severity vs priority — the distinction

Both `severity` and `priority` appear in this scorecard. They are different axes and must NOT be conflated.

**Severity** — how badly the issue hurts the user right now, objectively, regardless of the development calendar or effort required to fix it.

- `blocker`: the UI is broken for the user. Contrast below AA floor, primary CTA hidden below the fold, form submit unreachable without a workaround. The user cannot accomplish their goal.
- `high`: the UI significantly misleads or frustrates the user. Wrong CTA order, primary and secondary visually indistinguishable, spacing so tight buttons merge visually.
- `medium`: the UI is suboptimal in ways that slow users down or cause occasional errors. Label text ambiguous, spacing inconsistent with the grid.
- `low`: polish-level imperfections. 2 px gap deviation, minor token drift, slight alignment offset.
- `none`: dimension passes cleanly; no degradation.

**Priority** (P1/P2/P3) — how urgently the fix should be scheduled, accounting for: severity, effort to fix, blast radius, and whether a workaround exists.

The same issue can score at different positions on each axis:

| Scenario | Severity | Priority | Reasoning |
|---|---|---|---|
| CTA invisible — contrast 1.8:1 | blocker | P1 | User blocked; no workaround; fix is one CSS line |
| CTA swapped (primary left) | high | P1 | Significant user confusion; fix is trivial DOM reorder |
| Intra-group gap 6 px instead of 8 px | low | P3 | Functionally usable; purely cosmetic |
| Dark-mode color wrong — ships tomorrow | medium | P1 | Severity is medium (some users affected); priority is P1 because release is imminent and blast radius is all dark-mode users |
| Animation missing reduced-motion fallback | high | P2 | High severity for affected users; effort is moderate; workaround exists (user can disable animations globally) |

The evaluator assigns severity by measuring the user impact. The evaluator assigns priority using the P1/P2/P3 rubric defined in `TECH-uxeval-priority-rubric.md`. The user or project manager may override priority scheduling but may NOT override severity — severity is a factual measure of impact, not a negotiable deadline.

---

## 7. How the verdict aggregates

The `overall.verdict` field is derived deterministically from per-dimension results. Apply these rules in order; the first matching rule wins:

1. **BLOCKED** — one or more dimensions have `severity: blocker`. The artifact must not ship. Main orchestrator stops Phase B and routes back to the upstream producer.

2. **NEEDS_CHANGES** — no blocker severity, but one or more dimensions have `verdict: fail`. The artifact has significant issues that must be resolved before the user accepts it.

3. **PASS** — all dimensions are `verdict: pass` or `verdict: warn`, and no dimension has severity above `low`. The artifact is acceptable; recommendations are advisory.

Count fields (`blocking_count`, `high_count`, `medium_count`, `low_count`) reflect the number of individual dimensions at that severity, not the number of recommendations. These counts let the orchestrator surface a summary line without parsing the full recommendations list.

---

## 8. Worked example — full YAML

Evaluation: Pricing Page CTA at desktop 1440x900.

Findings:
- Position: primary CTA on the left, secondary on the right — inverts the universal convention. verdict=fail, severity=high.
- Visual Weight: primary filled brand color, heavier padding, clear hierarchy. verdict=pass, severity=none.
- Spacing: intra-group gap 6 px, convention minimum is 8 px. verdict=warn, severity=low.

```yaml
schema_version: "1.0"
scorecard_id: "f7e2a9b3-4c1d-4e8f-a2b6-3d5e7f9a0b1c"
component: "Pricing Page CTA"
input:
  type: "html"
  source: "/path/to/project/design/mockups/Pricing Page.html"
  viewport: "1440x900"
  captured_at: "2026-05-26T14:32:00+0200"
dimensions:
  position:
    verdict: "fail"
    severity: "high"
    evidence:
      - selector: ".pricing-cta .btn-primary"
        computed_style_or_value: "order: 1; margin-right: 8px"
        convention_violated: "primary-right"
        convention_source: "Balsamiq #4 — primary action on the right"
      - selector: ".pricing-cta .btn-secondary"
        computed_style_or_value: "order: 2"
        convention_violated: "secondary-left"
        convention_source: "Industry: GitHub, Stripe, Google — secondary precedes primary"
    rationale: "Primary CTA occupies the leftmost position in the button stack. Industry convention and Balsamiq both require primary to the right. Users trained on GitHub and Stripe will instinctively click the secondary action."
  visual_weight:
    verdict: "pass"
    severity: "none"
    evidence:
      - selector: ".pricing-cta .btn-primary"
        computed_style_or_value: "background-color: #1a73e8; padding: 12px 24px; font-weight: 600"
        convention_violated: ""
        convention_source: "Material Design — filled button with brand color for primary"
    rationale: "Primary button is visually dominant: filled brand blue versus outline secondary. Weight delta is sufficient to establish hierarchy at a glance."
  spacing:
    verdict: "warn"
    severity: "low"
    evidence:
      - selector: ".pricing-cta .btn-primary + .btn-secondary"
        computed_style_or_value: "margin-left: 6px"
        convention_violated: "intra-group-gap-min-8"
        convention_source: "amw-ux-evaluator — intra-group gap 8–12 px minimum"
    rationale: "6 px gap is 2 px below the 8 px floor. Buttons remain distinct and usable but feel slightly compressed. Easily corrected in one CSS rule."
overall:
  verdict: "NEEDS_CHANGES"
  blocking_count: 0
  high_count: 1
  medium_count: 0
  low_count: 1
recommendations:
  - id: "REC-001"
    dimension: "position"
    severity: "high"
    priority: "P1"
    change: "Swap CTA order so .btn-secondary appears before .btn-primary in the DOM, or set flex order: primary gets order 2, secondary gets order 1"
    evidence_ref: ".pricing-cta .btn-primary — order: 1; leftmost position"
    cited_principle: "Balsamiq #4 — primary action on the right"
  - id: "REC-002"
    dimension: "spacing"
    severity: "low"
    priority: "P3"
    change: "Increase intra-group gap from 6 px to 8 px by setting margin-left: 8px on .btn-secondary"
    evidence_ref: ".pricing-cta .btn-primary + .btn-secondary — margin-left: 6px"
    cited_principle: "amw-ux-evaluator conventions — intra-group gap 8–12 px"
ai_slop_scan:
  ran: true
  violations_high: 0
  violations_medium: 0
  violations_low: 0
notes: "Evaluated at desktop viewport 1440x900 only. Mobile breakpoint requires a separate evaluation run."
```

---

## 9. Consumer contracts

**Emits:**

- `amw-ux-evaluator` skill, always in agent-orchestrated mode (when invoked by `amw-browser-tester-agent` or any other sub-agent as part of a Phase B pipeline).
- `amw-ux-evaluator` skill, optionally on direct `/amw-eval` invocation when the user requests YAML output.

**Consumes:**

- `amw-browser-tester-agent` — surfaces scorecard data in its §13 return contract under `ux_scorecards: []`. Each entry is a path to a `.scorecard.yaml` file plus the `overall.verdict` value. The browser-tester agent does not re-parse the YAML body; it passes the path through to the main orchestrator.
- `ai-maestro-webdesign-main-agent` — gates Phase B delivery on `overall.verdict`. If `overall.verdict == "BLOCKED"`, Phase B halts and the issue routes back to the upstream producer (typically `amw-wireframe-builder-agent`). If `overall.verdict == "NEEDS_CHANGES"`, the main agent presents recommendations to the user and waits for a decision before proceeding.

---

## 10. Cross-references

- [TECH-uxeval-3-dimension-framework](./TECH-uxeval-3-dimension-framework.md) — Position / Visual Weight / Spacing rubric, verdict definitions, evaluation workflow
- [TECH-uxeval-output-format](./TECH-uxeval-output-format.md) — Markdown report format (the human-readable sidecar this scorecard complements)
- [TECH-uxeval-priority-rubric](./TECH-uxeval-priority-rubric.md) — P1 / P2 / P3 priority definitions (distinct from severity)
- [../../amw-design-principles/references/sub-agent-return-contract.md](../../amw-design-principles/references/sub-agent-return-contract.md) — YAML header schema used by all sub-agents in this plugin
- [../../../agents/amw-browser-tester-agent.md](../../../agents/amw-browser-tester-agent.md) — §13 return contract, which surfaces `ux_scorecards` from this format
