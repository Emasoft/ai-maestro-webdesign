---
name: amw-ascii-to-html
description: >-
  Convert a validated ASCII wireframe into responsive, accessible, Tweaks-compatible HTML. Triggers on "convert this ASCII to HTML", "render this wireframe as HTML", "ascii-to-html", "turn my ASCII mockup into a webpage". Does NOT trigger on generic "design a landing page" — that routes to design-principles. Upstream consumer is /amw-sketch's approved variant. Use when an approved ASCII wireframe must be rendered as HTML. Trigger with /amw-ascii-to-html.
version: 0.1.0
---

# ASCII → HTML converter

> Orchestrated by [SKILL](../amw-design-principles/SKILL.md). Terminal step of the `/amw-sketch` plan-phase loop. Do not run without explicit user approval of the ASCII (see Satisfaction Gate).

## Overview

Converts a validated ASCII wireframe into a single-file responsive, accessible, Tweaks-compatible HTML page. Terminal step of the plan phase — runs only after the user has explicitly approved an ASCII sketch.

This skill is a SYNTHESIS — it composes techniques from 9 sources (starter-components, AI-slop rules, ui-ux-pro-max, ux-designer+a11y, create-infographics, diagram-design-editorial, ascii-creator catalog, CHI'24 ASCII classics, and the in-repo `ascii-parse.py`). Every design decision below cites a `TECH-NN` from [techniques](references/techniques.md).

## Activation

Direct via `/amw-ascii-to-html` (fast path), or invoked by `design-principles` as the Phase B terminal step after Phase A approval. Autonomous and self-contained — any agent can use it by reading this SKILL.md.

## Position in flow

**OUTPUT (terminal — Phase B).** Validated + approved ASCII wireframe → single-file responsive HTML. Acceptable inputs:

- [SKILL](../amw-ascii-sketch/SKILL.md) — approved variant at `/tmp/amw-sketch-<slug>-final.txt`.
- [SKILL](../amw-ascii-creator/SKILL.md) — Mode B freeform wireframe, validator-PASS.
- User-supplied ASCII via `$ARGUMENTS` (direct mode — flag that iteration loop was skipped).

All inputs must have already passed `bin/amw-validate-ascii.py` (TECH-99).

## Trigger conditions

Narrow. Examples: "convert this ASCII to HTML", "render this wireframe as HTML", "turn my ASCII mockup into a webpage", "build the HTML from the approved sketch", "/amw-ascii-to-html <path>".

Generic design intent ("design a landing page" / "make a mockup" / "build a dashboard") → routes to [SKILL](../amw-design-principles/SKILL.md) first.

## Preconditions (all three must hold)

1. **Validator-PASS.** Input ASCII passed `bin/amw-validate-ascii.py`. If the upstream producer skipped validation, re-run it; hard-stop on FAIL (TECH-99).
2. **Explicit approval.** User said exactly one of `yes`, `ship it`, `convert it`, `that's the one`, `perfect`, `done`. Silence, "looks good", "sure", "ok", "fine" do NOT count — STOP and ask once: *"To confirm — convert this ASCII to HTML now?"*
3. **Tokens on file.** Design tokens exist from a prior `/amw-extract-style` run OR the user supplied an inline palette OR the user explicitly opted into starter-components defaults. NEVER invent tokens (TECH-63, TECH-24).

## Component detection table (synthesis evidence)

Every ASCII pattern maps to an HTML element, a canonical starter-component source, and the CSS tokens that drive it. The full 18-row table (frame / button / dropdown / card / card-grid / pipe-table / alert / attribution / route-line / form-inputs / checkbox-radio / sidebar / multi-col / nav-tabs / numbered-stages / sparkline / classic-ASCII / empty-row) lives at [component-detection-table](references/component-detection-table.md). Step 3 of `## Instructions` pattern-matches each parsed box/line against it.

## Instructions

1. **Validate** with `bin/amw-validate-ascii.py --in <source>`. FAIL → stop and return the validator report verbatim. (TECH-99)
2. **Parse** with `bin/amw-ascii-parse.py --in <source> --mode wireframe --out /tmp/amw-ascii-html-<slug>-layout.json`. This runs `detect_format`, `to_grid`, `find_boxes`, `find_arrows`, `find_wireframe_components`. (TECH-91..TECH-97)
3. **Pattern-match** each box/line against the component detection table above. Unknown shapes become literal text inside a `<div>` with a comment listing the glyphs that did not match — so the user can extend the parser if needed.
4. **Emit** semantic HTML:
   - `<header>` for the outer title row (if the wireframe has one — breadcrumbs, app name, date chip).
   - `<nav role="tablist">` for the tab row; each tab is `<button role="tab" aria-selected="<bool>" aria-controls="panel-N">`.
   - `<main>` for the viewport interior; use CSS grid with column count matching T-junctions.
   - `<section>` per horizontal-rule-delimited band (`├──┤` rows separate sections).
   - `<article>` for each card; `<article role="alert">` when the card has `[!]` / `[*]`.
   - `<table>` for any pipe-table region. `<thead>`, `<tbody>`, `<th scope="col">`.
   - `<footer>` only when the wireframe has one.
5. **Apply design tokens** from `/amw-extract-style` or user-supplied palette. Map to `:root { --primary; --text; --bg; --radius; --font-size; --space-1..--space-6; }` (TECH-07). Never invent values.
6. **Insert Tweaks block** (optional — only if the user requested live-editable tuning). Preserve the three invariants verbatim:
   - Listener registered BEFORE `__edit_mode_available` is posted (TECH-05).
   - `__edit_mode_set_keys` carries partial updates only (TECH-06).
   - `/*EDITMODE-BEGIN*/.../*EDITMODE-END*/` stays valid JSON with double-quoted keys AND values (TECH-04).
7. **React/Babel pins** — if and ONLY if the wireframe requires React (live state, interactive charts). Use the exact CDN URLs + integrity hashes in [react-babel-pins](../amw-design-principles/starter-components/react-babel-pins.md) (TECH-01). Name every styles object with a component prefix (TECH-02).
8. **AI-slop gate** — mentally walk `ai-slop-avoid.md` top to bottom. Self-check every rule 1..26 and the density principle. Any FAIL → revise the section and re-check. Record PASS per rule in the file header comment. (TECH-19..TECH-30)
9. **Smoke test** — optionally load in `dev-browser` and check console for zero errors. Do NOT run this inside the plan phase if the user just asked for a static file.
10. **Save** to `<cwd>/<Descriptive Filename>.html` (Title-Case, no `v2`/`v3`). Return the file path + AI-slop checklist + a one-line summary.

## AI-slop avoidance gate (checklist, in order)

Run these before saving — each is pulled from [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md):

1. No purple-blue `linear-gradient(135deg, #667eea, #764ba2)` (TECH-19); 2. no `border-left: 4px solid` on cards (TECH-20); 3. no AI-drawn SVG illustrations — sized gray placeholder instead (TECH-21); 4. no emoji carpet-bombing (TECH-22); 5. no default Inter/Roboto/Arial/system-ui/Fraunces/Poppins body font (TECH-24); 6. max 3 font weights (TECH-25); 7. no alternating white/pale-gray bands (TECH-26); 8. no "3 features in a row, icon each" hero (TECH-27); 9. no fabricated testimonials (TECH-28); 10. no `scrollIntoView({behavior:'smooth'})` (TECH-29); 11. borders ≥ `rgba(primary, 0.3)` or solid (TECH-52); 12. every element earns its place (TECH-30).

## Starter-component cross-reference

Canonical chrome lives in `../amw-design-principles/starter-components/`: `browser-window.html` (default desktop chrome, TECH-08), `ios-frame.html` / `android-frame.html` (mobile viewports, TECH-09), `macos-window.html` (sidebar + main shell, TECH-11), `deck-stage.html` (multi-screen deck, TECH-10), `design-canvas.html` (free-standing canvas), `animations.html` (timeline core ~50 LOC — use FIRST before Popmotion, TECH-12), `tweaks-block.html` (live-edit protocol, TECH-04/05/06/13), and [react-babel-pins](../amw-design-principles/starter-components/react-babel-pins.md) (version lock, TECH-01/02/03).

## Output

Produces a single artifact at the path specified in the `## Instructions` conversion pipeline — a self-contained `.html` file with inline CSS and JS, no external dependencies except the CDN pins declared in starter-components.

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Prerequisites

```yaml
runtime_binaries:
  - python3   # runs bin/amw-ascii-parse.py
  - perl      # runs bin/amw-validate-ascii.py

python_packages: []   # ascii-parse.py is stdlib-only

npm: []              # no build; emitted HTML uses UMD CDN for React only

external_services:
  - none   # offline-capable
```

## Non-negotiables

- Approval gate is non-skippable. Ambiguous acknowledgement is NOT approval. (TECH rule from upstream design-principles)
- Single source file by default. Split only if > 1000 lines. (TECH-61)
- React/Babel pinned to exact versions with integrity hashes. No `react@18` shorthand. No `type="module"`. (TECH-01)
- Three Tweaks protocol invariants preserved verbatim when Tweaks block is included. (TECH-04, TECH-05, TECH-06)
- `scrollIntoView` is banned everywhere. (TECH-29)
- No Framer Motion, no GSAP. Timeline core first, Popmotion as physics fallback. (TECH-12)
- Inherits the three hard rules from [SKILL](../amw-design-principles/SKILL.md) — context gathered, variants offered upstream, AI-slop refused.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| Validator FAIL on input | Upstream producer skipped validation or user hand-edited ASCII | Stop. Return the validator FIX hints verbatim. Do not attempt to guess-repair. |
| Parser returns empty `boxes` | Input exceeds `MAX_GRID_DIM` and got truncated | Ask the user to split into multiple frames. (TECH-96) |
| Unknown glyphs in wireframe | ASCII uses custom symbols not in the parser's classifier | Parse what's parseable; list unknown glyphs in the emitted file's header comment; ask whether to extend the parser. |
| No prior `/amw-sketch` run but user pasted ASCII | Direct mode | Flag it: *"Skipping iteration loop. If you want to iterate in ASCII first, run /amw-sketch."* Proceed only on explicit confirm. |
| User approval is ambiguous ("looks good", "sure") | Not a satisfaction token | STOP. Ask once: *"To confirm — convert this ASCII to HTML now?"* |
| Slop-gate FAIL (rule 1..26) | Default tokens leaked, emoji in header, purple gradient, etc. | Revise the affected section once and re-check. Record the rule that triggered. |
| React pin mismatch | User upgraded `react@18` → UMD integrity hash mismatch | Re-pin to `react@18.3.1` exactly; restore the three CDN lines from `react-babel-pins.md`. |

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (ALWAYS activate this first when user says "design").
- [SKILL](../amw-ascii-sketch/SKILL.md) — upstream producer of the approved ASCII.
- [SKILL](../amw-ascii-creator/SKILL.md) — upstream single-artifact authoring skill.
- [SKILL](../amw-ascii-validator/SKILL.md) — the mandatory validation gate (wraps `bin/amw-validate-ascii.py` + `bin/amw-ascii-render.py`).
- `../amw-design-principles/starter-components/` — canonical chrome + tweaks protocol.
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — output-ban list (final gate).
- [color-system](../amw-design-principles/color-system.md) — oklch tokens, WCAG contrast, palette structure.
- [typography-system](../amw-design-principles/typography-system.md) — type scale + font stacks (no Inter/Roboto/Arial default).
- [spacing-rhythm](../amw-design-principles/spacing-rhythm.md) — 8pt grid, radius, shadow tokens, hit-target rules.
- `../../bin/amw-ascii-parse.py` — parser.
- `../../bin/amw-validate-ascii.py` — validator.
- [SKILL](../amw-dev-browser/SKILL.md) — preview pipeline (optional).
- `/amw-ascii-to-html` — user-facing slash command.
- `/amw-preview` — automatic next step when requested.

### Technique catalog

Full catalog with source citations and per-step TECH-NN mapping: [techniques](references/techniques.md) (100 techniques, 9 sources).
