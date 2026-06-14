---
name: amw-html-diagram
description: Author OR edit an HTML-rendered diagram — editorial architecture / flowchart / sequence / state / ER / timeline / swimlane / quadrant / tree / layer / venn, or an infographic page. Triggers on "create HTML diagram", "modify HTML diagram", "render structure as HTML", "edit .html diagram". Does NOT claim generic design / UI / landing-page vocabulary — routes to design-principles. Use when authoring an HTML diagram. Trigger with /amw-create-or-modify-html-diagram.
version: 0.1.0
---

# HTML Diagram — thin authoring + modify dispatcher

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Format spec (authoritative):** [html](../amw-diagram-formats/references/html.md).
> **Modify pipeline (authoritative):** [modify-flow](../amw-diagram-formats/references/modify-flow.md).
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references

This skill does not redefine HTML / SVG / a11y / Tweaks / React-pins / AI-slop-avoid rules — every one of those lives once in [html](../amw-diagram-formats/references/html.md). The skill's job is to DISPATCH to the right backing producer (editorial vs infographic) and to run the shared modify-flow when the input is an existing `.html`.

## Overview

Thin dispatcher for HTML-rendered diagrams and infographic-style pages. Accepts either a new brief or an existing `.html` file. Routes create requests to `amw-diagram-editorial` (13-archetype editorial diagrams) or `amw-infographics` (dense HTML/PNG/PDF infographics) based on `--style editorial|infographic` or brief cues. Routes modify requests through the shared 5-step modify-flow (parse → IR → patch → re-render → validate). Emits exactly one self-contained `.html` file per invocation.

## Instructions

1. Detect whether the input is a brief (create path) or an existing `.html` file (modify path).
2. For create path: dispatch to `../amw-diagram-editorial/` (editorial diagrams, default) or `../amw-infographics/` (dense infographics) based on `--style editorial|infographic` or brief cues.
3. For modify path: parse the existing file to IR with `bin/amw-parse-html-diagram.py`, apply the requested edit to the IR, and re-render via `bin/amw-diagram-ir.py emit --format html`.
4. Validate the output with `bin/amw-validate-html-diagram.sh`; a FAIL aborts and leaves the original file untouched (retry budget = 3).
5. See the `## Pipeline (6 steps — matches shared modify-flow)` section below for the authoritative execution sequence.

## Activation

Callable directly via the `/amw-create-or-modify-html-diagram` command, or invoked by the `design-principles` orchestrator during **Phase B** when the approved deliverable is an HTML-rendered diagram. An agent in Main-agent mode may also invoke this skill directly. This skill is **autonomous and self-contained** — any agent can use it by reading this SKILL.md and its references.

## Position in flow

OUTPUT (terminal). Emits exactly one self-contained `.html` file (inline CSS + inline SVG, no external build). Downstream of `design-principles` orchestration when the user has committed to an HTML-diagram deliverable. Upstream of `/amw-preview`, `/amw-eval`, and the webpage-sync round-trip skills.

## Trigger conditions

- "create an HTML diagram" / "build an HTML diagram of <subject>"
- "render this structure as HTML"
- "HTML architecture diagram / flowchart / sequence / ER / swimlane / timeline / tree / venn / funnel / pyramid of <subject>"
- "modify this HTML diagram" / "edit the HTML at `<path>`" / "update `<something>.html`"
- "/amw-create-or-modify-html-diagram <brief-or-path>"

Do NOT activate on:
- Generic "design a landing page" / "build a dashboard UI" — orchestrator's job (`../amw-design-principles/`).
- Converting an existing diagram to HTML (`/amw-convert-any-diagram-format --to html`).
- Validating an HTML file only (`/amw-validate-any-diagram-format`).

## Component detection table (excerpt)

Full table + technique-level citations live in [html](../amw-diagram-formats/references/html.md) §2 + §9 (100 techniques). The 8 rows below are the most common dispatch cues — consult the ref for the rest.

| HTML construct | IR node/edge kind | Ref |
|---|---|---|
| `<article class="card">` with heading + body | `node{shape:rect, kind:card}` | [html](../amw-diagram-formats/references/html.md) TECH-71 |
| `<button type="button">` (min-h 44px) | `node{kind:cta}` | ref TECH-70 + TECH-16 |
| `<nav role="tablist"><button role="tab">` | `node{kind:tab-group}` + edges to panels | ref TECH-08 + TECH-43 |
| Inline `<svg>` with `<rect>` + `<line marker-end>` | structural IR (`nodes[]`, `edges[]`) | ref §1.1 + `<./svg.md>` TECH-SV-20 |
| `<table><thead><th scope>` | `node{kind:table}` (cells as child nodes) | ref TECH-82 + TECH-49 |
| `<ol class="stages">` / `<ol class="timeline">` | edges with `order` attribute | ref TECH-79 + TECH-87 |
| `<article role="alert" aria-live="polite">` | `node{kind:alert, annotations:["alert"]}` | ref TECH-75 + TECH-47 |
| `<fieldset><legend>` | `node{kind:group-container}` (child nodes inside) | ref TECH-89 |

## Pipeline (6 steps — matches shared modify-flow)

1. **Detect** source shape. If `$ARGUMENTS` is a path to an existing `.html` → **modify path**. If it's a brief → **create path** (further dispatch by `--style editorial|infographic` or by brief cues; editorial is default).
2. **Parse** (modify path only) via `bin/amw-parse-html-diagram.py` → IR (schema: [ir-schema](../amw-diagram-formats/references/ir-schema.md)). Create path skips this step.
> [ir-schema.md] Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Validation · Consumers
3. **IR operation:**
   - Create path → generate IR from the brief, route to [SKILL](../amw-diagram-editorial/SKILL.md) (13-archetype path) or [SKILL](../amw-infographics/SKILL.md) (dense editorial path) based on `--style` / brief cues, let the producer emit.
   - Modify path → apply the user's requested edit to the IR (text substitution on `nodes[*].label` for MVP; structural operations once Phase 1 lands — see [modify-flow](../amw-diagram-formats/references/modify-flow.md) §5.2).
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references
4. **Re-render** via `bin/amw-diagram-ir.py emit --format html` (wraps the chosen producer for create path; emits the patched IR back to HTML for modify path).
5. **Re-validate** via `bin/amw-validate-html-diagram.sh` (wraps `xmllint --html --noout` + `tidy -e -q -errors`; unified PASS/FAIL contract per [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md)). A FAIL aborts and leaves the original file untouched. Retry budget = 3 (per shared modify-flow).
> [validation-dispatcher.md] Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · Caller integration patterns · Known limitations (Phase 0) · Related references

## Final gate (every emitted `.html`)

Before save, the AI-slop-avoid 12-item checklist runs — see [html](../amw-diagram-formats/references/html.md) §5 for the full list and the final grep command. Any FAIL → revise the affected region and re-check; record the rule that triggered in the file-header comment.

## Output

Produces one self-contained `.html` file (inline CSS + inline SVG, no external build) at the user-supplied path or a descriptive default. On validation failure the original file is left untouched. See the Pipeline section for the full output contract.

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8` (for `bin/amw-parse-html-diagram.py`, `bin/amw-diagram-ir.py`), `xmllint` (libxml2), `tidy` (HTML Tidy) — installed by `/amw-init`; checked by `/amw-doctor`.
- **python_packages:** `lxml` (HTML parsing in `bin/amw-parse-html-diagram.py`).
- **npm:** none. Emitted HTML uses pinned React/Babel UMD CDN ONLY if the artifact is interactive (see [html](../amw-diagram-formats/references/html.md) §4).
- **Shared scripts:** `bin/amw-parse-html-diagram.py`, `bin/amw-diagram-ir.py`, `bin/amw-validate-html-diagram.sh`, `bin/amw-html-export.py` (optional PNG export).

## Examples

**Create path:**
- **Input:** "Build a flow diagram showing a 4-step user-onboarding funnel with conversion rates."
- **Operation:** parse brief → IR via `bin/amw-diagram-ir.py`, emit HTML through editorial template, lint via `bin/amw-validate-html-diagram.sh`.
- **Output:** `onboarding-funnel.html` (self-contained, Tweaks-protocol-compliant, AI-slop-avoid gate passed).

**Modify path:**
- **Input:** `existing-diagram.html` + patch "rename stage 3 'Verify' → 'Confirm', conversion → 84%".
- **Operation:** detect format, parse to IR, apply patch, emit, re-validate (per the modify-flow).
- **Output:** updated `existing-diagram.html` with string + numeric edits, no structural drift.

See more worked examples in [SKILL](../amw-diagram-editorial/SKILL.md) (editorial path) and [SKILL](../amw-infographics/SKILL.md) (infographic path), and the technique catalog at [html](../amw-diagram-formats/references/html.md).

## Resources

- [html](../amw-diagram-formats/references/html.md) — authoritative HTML format spec + 100-technique catalog.
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22)
- [modify-flow](../amw-diagram-formats/references/modify-flow.md) — authoritative 6-step modify pipeline.
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references
- [ir-schema](../amw-diagram-formats/references/ir-schema.md) — IR schema consumed by `bin/amw-diagram-ir.py`.
> [ir-schema.md] Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Validation · Consumers
- [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md) — unified validator output contract.
> [validation-dispatcher.md] Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · Caller integration patterns · Known limitations (Phase 0) · Related references
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — final output-ban gate (12 items).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- `../amw-design-principles/starter-components/` — canonical chrome + tweaks protocol + React/Babel pins.
- [SKILL](../amw-ascii-to-html/SKILL.md) — upstream when input is ASCII (ASCII → HTML path).
- [SKILL](../amw-diagram-editorial/SKILL.md) — create-path backend for `--style editorial` (13-archetype).
- [SKILL](../amw-infographics/SKILL.md) — create-path backend for `--style infographic` (dense editorial).
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.

## Non-negotiables

- Exactly one self-contained `.html` per invocation. Inline CSS + inline SVG. No external `<link>` to CDN CSS, no npm install, no bundler. ([html](../amw-diagram-formats/references/html.md) TECH-61)
- Every emitted `.html` passes `bin/amw-validate-html-diagram.sh` AND the AI-slop-avoid 12-item checklist. A FAIL aborts; the original file is untouched.
- Tweaks block (when included) preserves the three invariants verbatim — listener-before-announce, partial-keys only, valid JSON EDITMODE block. ([html](../amw-diagram-formats/references/html.md) §3)
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22)
- React/Babel pins are exact — `react@18.3.1`, `react-dom@18.3.1`, `<@babel/standalone@7.29.0>` — with integrity hashes. No `react@18` shorthand, no `type="module"`. ([html](../amw-diagram-formats/references/html.md) §4)
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22)
- `scrollIntoView` is banned everywhere. Use `window.scrollTo({top, behavior:'smooth'})` with manual offset. ([html](../amw-diagram-formats/references/html.md) TECH-29)
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22)
- Do NOT re-author the HTML spec inside this skill — reference [html](../amw-diagram-formats/references/html.md). If a rule is wrong, fix it there.
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22)

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| `bin/amw-validate-html-diagram.sh` FAIL | Unclosed tag, stray `&`, invalid nesting | Return the validator report verbatim; do not guess-repair. |
| AI-slop-avoid FAIL on rule 1-12 | Default tokens leaked, emoji in header, purple gradient, etc. | Revise the affected region once and re-check. Record the rule in the file-header comment. |
| Modify path hits retry budget 3 FAILs | Patch conflicts with another part of the HTML | Surface the validator findings; ask the user to refine the edit. |
| Parser returns empty IR (modify path) | HTML has no detectable diagram structure | Treat the whole body as `nodes[0].label` (raw-source stub per `modify-flow.md` §5.2); warn the user that structural patching is unavailable until Phase 1 parsers land. |
