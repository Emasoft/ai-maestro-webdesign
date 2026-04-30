---
name: amw-html-diagram
description: Author OR edit an HTML-rendered diagram — editorial architecture / flowchart / sequence / state / ER / timeline / swimlane / quadrant / tree / layer / venn / funnel / pyramid / nested wall, or an infographic-style dense editorial page. Triggers on narrow technical intents only — "create HTML diagram", "modify HTML diagram at <path>", "render this structure as HTML", "edit this .html diagram", "/amw-create-or-modify-html-diagram". Does NOT claim generic design / UI / landing-page vocabulary — those go to design-principles. Thin dispatcher over ../amw-diagram-editorial/ (13-archetype create) and ../amw-infographics/ (dense HTML).
version: 0.1.0
---

# HTML Diagram — thin authoring + modify dispatcher

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> **Format spec (authoritative):** `../amw-diagram-formats/references/html.md`.
> **Modify pipeline (authoritative):** `../amw-diagram-formats/references/modify-flow.md`.

This skill does not redefine HTML / SVG / a11y / Tweaks / React-pins / AI-slop-avoid rules — every one of those lives once in `../amw-diagram-formats/references/html.md`. The skill's job is to DISPATCH to the right backing producer (editorial vs infographic) and to run the shared modify-flow when the input is an existing `.html`.

## Activation

Callable directly via the `/amw-create-or-modify-html-diagram` command (user shortcut for users who already know they want an HTML diagram and have either a brief or an existing `.html` file to modify), or invoked by the `design-principles` orchestrator during **Phase B** when the approved deliverable is an HTML-rendered diagram. An agent in Main-agent mode may also invoke this skill directly via the orchestrator without going through the command.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

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

Full table + technique-level citations live in `../amw-diagram-formats/references/html.md` §2 + §9 (100 techniques). The 8 rows below are the most common dispatch cues — consult the ref for the rest.

| HTML construct | IR node/edge kind | Ref |
|---|---|---|
| `<article class="card">` with heading + body | `node{shape:rect, kind:card}` | `../amw-diagram-formats/references/html.md` TECH-71 |
| `<button type="button">` (min-h 44px) | `node{kind:cta}` | ref TECH-70 + TECH-16 |
| `<nav role="tablist"><button role="tab">` | `node{kind:tab-group}` + edges to panels | ref TECH-08 + TECH-43 |
| Inline `<svg>` with `<rect>` + `<line marker-end>` | structural IR (`nodes[]`, `edges[]`) | ref §1.1 + `./svg.md` TECH-SV-20 |
| `<table><thead><th scope>` | `node{kind:table}` (cells as child nodes) | ref TECH-82 + TECH-49 |
| `<ol class="stages">` / `<ol class="timeline">` | edges with `order` attribute | ref TECH-79 + TECH-87 |
| `<article role="alert" aria-live="polite">` | `node{kind:alert, annotations:["alert"]}` | ref TECH-75 + TECH-47 |
| `<fieldset><legend>` | `node{kind:group-container}` (child nodes inside) | ref TECH-89 |

## Pipeline (5 steps — matches shared modify-flow)

1. **Detect** source shape. If `$ARGUMENTS` is a path to an existing `.html` → **modify path**. If it's a brief → **create path** (further dispatch by `--style editorial|infographic` or by brief cues; editorial is default).
2. **Parse** (modify path only) via `bin/amw-parse-html-diagram.py` → IR (schema: `../amw-diagram-formats/references/ir-schema.md`). Create path skips this step.
3. **IR operation:**
   - Create path → generate IR from the brief, route to `../amw-diagram-editorial/SKILL.md` (13-archetype path) or `../amw-infographics/SKILL.md` (dense editorial path) based on `--style` / brief cues, let the producer emit.
   - Modify path → apply the user's requested edit to the IR (text substitution on `nodes[*].label` for MVP; structural operations once Phase 1 lands — see `../amw-diagram-formats/references/modify-flow.md` §5.2).
4. **Re-render** via `bin/amw-diagram-ir.py emit --format html` (wraps the chosen producer for create path; emits the patched IR back to HTML for modify path).
5. **Re-validate** via `bin/amw-validate-html-diagram.sh` (wraps `xmllint --html --noout` + `tidy -e -q -errors`; unified PASS/FAIL contract per `../amw-diagram-formats/references/validation-dispatcher.md`). A FAIL aborts and leaves the original file untouched. Retry budget = 3 (per shared modify-flow).

## Final gate (every emitted `.html`)

Before save, the AI-slop-avoid 12-item checklist runs — see `../amw-diagram-formats/references/html.md` §5 for the full list and the final grep command. Any FAIL → revise the affected region and re-check; record the rule that triggered in the file-header comment.

## Dependencies

- **runtime_binaries:** `python3 >= 3.8` (for `bin/amw-parse-html-diagram.py`, `bin/amw-diagram-ir.py`), `xmllint` (libxml2), `tidy` (HTML Tidy) — installed by `/amw-init`; checked by `/amw-doctor`.
- **python_packages:** `lxml` (HTML parsing in `bin/amw-parse-html-diagram.py`).
- **npm:** none. Emitted HTML uses pinned React/Babel UMD CDN ONLY if the artifact is interactive (see `../amw-diagram-formats/references/html.md` §4).
- **Shared scripts:** `bin/amw-parse-html-diagram.py`, `bin/amw-diagram-ir.py`, `bin/amw-validate-html-diagram.sh`, `bin/amw-html-export.py` (optional PNG export).

## Cross-references

- `../amw-diagram-formats/references/html.md` — authoritative HTML format spec + 100-technique catalog.
- `../amw-diagram-formats/references/modify-flow.md` — authoritative 6-step modify pipeline.
- `../amw-diagram-formats/references/ir-schema.md` — IR schema consumed by `bin/amw-diagram-ir.py`.
- `../amw-diagram-formats/references/validation-dispatcher.md` — unified validator output contract.
- `../amw-design-principles/ai-slop-avoid.md` — final output-ban gate (12 items).
- `../amw-design-principles/starter-components/` — canonical chrome + tweaks protocol + React/Babel pins.
- `../amw-ascii-to-html/SKILL.md` — upstream when input is ASCII (ASCII → HTML path).
- `../amw-diagram-editorial/SKILL.md` — create-path backend for `--style editorial` (13-archetype).
- `../amw-infographics/SKILL.md` — create-path backend for `--style infographic` (dense editorial).
- `../amw-design-principles/SKILL.md` — orchestrator.

## Non-negotiables

- Exactly one self-contained `.html` per invocation. Inline CSS + inline SVG. No external `<link>` to CDN CSS, no npm install, no bundler. (`../amw-diagram-formats/references/html.md` TECH-61)
- Every emitted `.html` passes `bin/amw-validate-html-diagram.sh` AND the AI-slop-avoid 12-item checklist. A FAIL aborts; the original file is untouched.
- Tweaks block (when included) preserves the three invariants verbatim — listener-before-announce, partial-keys only, valid JSON EDITMODE block. (`../amw-diagram-formats/references/html.md` §3)
- React/Babel pins are exact — `react@18.3.1`, `react-dom@18.3.1`, `@babel/standalone@7.29.0` — with integrity hashes. No `react@18` shorthand, no `type="module"`. (`../amw-diagram-formats/references/html.md` §4)
- `scrollIntoView` is banned everywhere. Use `window.scrollTo({top, behavior:'smooth'})` with manual offset. (`../amw-diagram-formats/references/html.md` TECH-29)
- Do NOT re-author the HTML spec inside this skill — reference `../amw-diagram-formats/references/html.md`. If a rule is wrong, fix it there.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `bin/amw-validate-html-diagram.sh` FAIL | Unclosed tag, stray `&`, invalid nesting | Return the validator report verbatim; do not guess-repair. |
| AI-slop-avoid FAIL on rule 1-12 | Default tokens leaked, emoji in header, purple gradient, etc. | Revise the affected region once and re-check. Record the rule in the file-header comment. |
| Modify path hits retry budget 3 FAILs | Patch conflicts with another part of the HTML | Surface the validator findings; ask the user to refine the edit. |
| Parser returns empty IR (modify path) | HTML has no detectable diagram structure | Treat the whole body as `nodes[0].label` (raw-source stub per `modify-flow.md` §5.2); warn the user that structural patching is unavailable until Phase 1 parsers land. |
