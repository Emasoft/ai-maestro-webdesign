---
name: amw-ascii-creator
description: Produce ONE validated perfect-ASCII artifact from a brief — structured via bin/amw-ascii-render.py, freeform via validate-iterate loop. Triggers on "ASCII diagram of", "ASCII wireframe of", "perfect ASCII of", "build ASCII mockup". Does NOT trigger on generic design intent — routes to design-principles → ascii-sketch. FINISHING skill — one validated .txt file delivered. Use when finalizing a single ASCII artifact to file. Trigger with /amw-create-or-modify-ascii-diagram.
---

# ASCII Creator

> Orchestrated by [SKILL](../amw-design-principles/SKILL.md). Single-artifact ASCII authoring — the opposite of `../amw-ascii-sketch/` (multi-variant plan-phase). ASCII twin of `../amw-svg-creator/`.

## Overview

Produces ONE validated perfect-ASCII artifact from a brief. Uses `bin/amw-ascii-render.py` for structured diagrams (Mode A) or a hand-author-validate-iterate loop via `bin/amw-validate-ascii.py` (Mode B). The finishing skill — one invocation, one validated `.txt` file delivered.

## Activation, position in flow, trigger conditions

Callable via `/amw-create-or-modify-ascii-diagram` (user shortcut), or invoked by `../amw-design-principles/` as a Phase B finisher after Phase A approval. **OUTPUT (Phase B)** — takes a natural-language diagram brief and produces exactly one validated `.txt` file. Upstream of `../amw-ascii-to-html/` when the artifact is a wireframe and the user wants HTML next.

Trigger phrases: *"ASCII diagram of <system>"*, *"perfect ASCII diagram of <flow>"*, *"ASCII wireframe of <screen>"*, *"finalize this ASCII"*, *"create an ASCII flowchart / table / sequence / layered architecture"*, *"build an ASCII mockup of <screen>"* — single mockup, not a set. After `/amw-sketch` approval, when the approved variant needs to be rendered to file (alternative path to `/amw-ascii-to-html` for ASCII-only deliverables).

Do NOT trigger on broad design vocabulary ("design a dashboard" / "mockup a UI" — `../amw-design-principles/`'s job) or multi-variant intent ("show me three options" — `../amw-ascii-sketch/`'s job). This skill is **autonomous and self-contained** — any agent can use it by reading this SKILL.md and its references; the techniques are NOT limited to what matching commands expose.

## Instructions

1. Classify the brief: Mode A (structured — flowchart, table, layers, sequence) or Mode B (freeform rectangular wireframe).
2. Mode A: build JSON spec, run `bin/amw-ascii-render.py`, sanity-check, fix JSON errors and re-render until correct.
3. Mode B: author the ASCII frame, substitute banned chars, save to `/tmp/ascii-creator-<slug>.txt`, run `bin/amw-validate-ascii.py`.
4. Iterate on validator `FIX:` hints until PASS.
5. Apply matching style preset (`detallado` / `unicode` / `clasico` / `compacto`).
6. Save with a descriptive English filename; write the job-completion report.

## Two authoring modes (the skill classifies automatically)

### Mode A — Structured (flowchart, table, layers, sequence)

Use when the brief describes a STRUCTURE — nodes + edges, rows + columns, tiers, messages between actors. The renderer `../../bin/amw-ascii-render.py` draws it pixel-perfect from a JSON spec, so alignment is guaranteed by construction.

| Sub-mode | When to use |
|---|---|
| `diagram` | Flowcharts, ER diagrams, state machines, block diagrams |
| `table`   | Data grids, comparison matrices |
| `layers`  | Layered architecture with bus connectors between tiers |
| `sequence`| Sequence diagrams with lifelines |

Workflow:

1. Parse the brief; pick sub-mode; extract entities (boxes, rows, connectors, lanes).
2. Build JSON matching the schema in `../../bin/amw-ascii-render.py`'s top-of-file docstring. Keep labels under ~15 chars.
3. `echo '<JSON>' | python3 ../../bin/amw-ascii-render.py > /tmp/ascii-creator-<slug>.txt` — non-zero exit means fix the JSON and retry (label too long, missing box id, total width > 78 cols).
4. Sanity-check the rendered file; adjust the `grid` / `connectors` / `lanes` in the JSON and re-render if connections look wrong.
5. Save to `<working-dir>/<Descriptive Name>.txt`.

Structured output is trimmed-line (not framed) — Mode A skips the frame validator. If the brief wants the structured diagram wrapped in a frame, switch to Mode B after rendering.

### Mode B — Freeform wireframe (framed rectangular UI mockup)

Use when the brief describes a RECTANGULAR artifact — dashboard, mobile frame, editorial poster, newspaper-column layout. Hand-authored, with alignment enforced by `../../bin/amw-validate-ascii.py`.

Workflow:

1. Parse the brief: frame width (60/66/72/78), required elements, banned-char substitutions (see [style-presets-and-banned-chars](./references/style-presets-and-banned-chars.md)).
> [style-presets-and-banned-chars.md] Style presets (orthogonal to mode selection) · Banned characters (severity-rated — enforced by validate-ascii.py) · Cross-references
2. Substitute banned chars BEFORE authoring — do NOT rely on the validator to flag them.
3. Author using either pure-ASCII (`+---+`) OR Unicode box-drawing (`+---+`, T-junctions, corner glyphs). Mixing them in one artifact breaks alignment — pick one and stay consistent.
4. Write to `/tmp/ascii-creator-<slug>.txt`.
5. `python3 ../../bin/amw-validate-ascii.py /tmp/ascii-creator-<slug>.txt` — on FAIL, apply every emitted `FIX:` hint (they are exact, e.g. "Move '|' on line 5 right by 1 position(s) to column 64"); re-validate. Loop until PASS.
6. Save to `<working-dir>/<Descriptive Name>.txt`.

Typical iteration counts: simple wireframe 1, dashboard 2-3, dense editorial 3-5. Never present or save a FAILing artifact — the entire value of "perfect ASCII" is validator-PASS.

### Technique catalog and Mode B gold-standards

12 JSON-render techniques + Mode B reference diagrams (`incident-response.txt`, `ci-cd-pipeline.txt`, `microservices.txt`) are documented at [technique-catalog-and-gold-standards](./references/technique-catalog-and-gold-standards.md). Pick at least 10 distinct TECH-IDs per variant so each diagram demonstrates deliberate construction.

## References

Every technique lives in `./references/` (same TOC: *What it does · When to use · How it works · Minimal example · Gotchas · Cross-references*):

- [TECH-78-column-cap](./references/TECH-78-column-cap.md), [TECH-bus-connectors](./references/TECH-bus-connectors.md), [TECH-cell-spanning](./references/TECH-cell-spanning.md), [TECH-eval-rubric-six-axes](./references/TECH-eval-rubric-six-axes.md)
> [TECH-eval-rubric-six-axes.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-cell-spanning.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-bus-connectors.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-78-column-cap.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-json-render-four-modes](./references/TECH-json-render-four-modes.md), [TECH-lane-labeled-diagrams](./references/TECH-lane-labeled-diagrams.md), [TECH-multi-line-box-body](./references/TECH-multi-line-box-body.md)
> [TECH-multi-line-box-body.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-lane-labeled-diagrams.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-json-render-four-modes.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-render-mode-diagram](./references/TECH-render-mode-diagram.md), [TECH-render-mode-layers](./references/TECH-render-mode-layers.md), [TECH-render-mode-sequence](./references/TECH-render-mode-sequence.md), [TECH-render-mode-table](./references/TECH-render-mode-table.md)
> [TECH-render-mode-table.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-render-mode-sequence.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-render-mode-layers.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-render-mode-diagram.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-sequence-notes](./references/TECH-sequence-notes.md), [style-presets-and-banned-chars](./references/style-presets-and-banned-chars.md)
> [style-presets-and-banned-chars.md] Style presets (orthogonal to mode selection) · Banned characters (severity-rated — enforced by validate-ascii.py) · Cross-references
> [TECH-sequence-notes.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
<!-- end of references -->

## Output

Exactly one validated perfect-ASCII `.txt` file with a descriptive English filename, plus a job-completion report. Mode A output must execute `bin/amw-ascii-render.py` cleanly (non-zero exit = not delivered); Mode B output must PASS `bin/amw-validate-ascii.py` before save. See [skill-completion-and-output-contract](../amw-design-principles/references/skill-completion-and-output-contract.md) for the shared checklist and report contract; this skill's `## Non-negotiables` lists the Mode-specific additions.

## Style presets and banned characters

The four presets (`detallado` / `unicode` / `clasico` / `compacto`) and the full validator-enforced ban-list (severity-rated CRITICAL/HIGH/MEDIUM + always-banned emoji/CJK) live at [style-presets-and-banned-chars](./references/style-presets-and-banned-chars.md).
> [style-presets-and-banned-chars.md] Style presets (orthogonal to mode selection) · Banned characters (severity-rated — enforced by validate-ascii.py) · Cross-references

## Prerequisites

- runtime: `python3 >= 3.8` (pre-installed; `/amw-doctor` checks)
- python_packages / npm / mcp: none (pure stdlib)
- Shared scripts: `../../bin/amw-ascii-render.py` (renderer, 4 modes, 78-col max), `../../bin/amw-validate-ascii.py` (alignment / width / wide-char / forbidden-char validator)

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Resources

- [SKILL](../amw-ascii-sketch/SKILL.md) — upstream multi-variant iterator (sketch 3 → pick one → finalize here OR go straight to ascii-to-html)
- [SKILL](../amw-ascii-validator/SKILL.md) — validator tool-chain + validation contract
- [SKILL](../amw-ascii-to-html/SKILL.md) — downstream Mode B output to HTML
- [SKILL](../amw-ascii-to-svg/SKILL.md) — downstream Mode A output to SVG
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator
- `../amw-box-diagram/examples/` — gold-standard Mode B reference diagrams (incident-response, ci-cd-pipeline, microservices)
- `../../bin/amw-ascii-render.py` — renderer (JSON to ASCII)
- `../../bin/amw-validate-ascii.py` — validator (ASCII to PASS/FAIL + FIX hints)

## Non-negotiables

- One invocation emits exactly one `.txt` file (multi-variant → `../amw-ascii-sketch/`).
- Mode B output must PASS `bin/amw-validate-ascii.py` before save.
- Mode A output must successfully execute `bin/amw-ascii-render.py` (non-zero exit = not delivered).
- Banned chars substituted BEFORE authoring, never during FIX iteration.
- Descriptive English filename, never `diagram.txt` / `output.txt`.
- If a FIX iteration hits 8+ retries, STOP — propose widening the frame or switching modes.

## Error Handling

| Symptom | Fix |
|---|---|
| `ascii-render.py` exits "width exceeds 78" | Shorten labels, split into multiple diagrams, or switch to Mode A `layers` for wide architecture |
| Validator reports `WIDTH_MISMATCH` on every line | Pad each line with trailing spaces to match the max-width line |
| Validator reports `VERTICAL_MISALIGNED` | Nested box corners drift between rows; lock each `\|` to an explicit column number |
| Validator reports `WIDE_CHAR` | Emoji / CJK / filled triangle — substitute per the [banned-char ban-list](./references/style-presets-and-banned-chars.md) |
> [style-presets-and-banned-chars.md] Style presets (orthogonal to mode selection) · Banned characters (severity-rated — enforced by validate-ascii.py) · Cross-references
| Validator reports `FORBIDDEN_CHAR_MEDIUM` | Variable-width triangle or long arrow — substitute per the ban-list |
| Mode classification wrong | Brief mixes structural + freeform; split into two invocations |
| User wants THREE variants OR HTML | Wrong skill — route to `../amw-ascii-sketch/` or `../amw-ascii-to-html/` respectively |

## Modify flow (shared)

When the user points at an existing `.txt` / `.ascii` / `.md` file and asks to edit it (rather than author from scratch), this skill runs the **shared modify pipeline** instead of Mode A or Mode B. The pipeline is: detect format → parse to IR (`bin/amw-diagram-ir.py parse`) → diff-aware IR patch → re-render (`bin/amw-diagram-ir.py emit --format ascii`) → re-validate (`bin/amw-validate-ascii.py`). The full, authoritative 6-step spec — including retry budget, atomic-move semantics, per-format emitter fast paths, and ASCII-specific patching guidance (§5.1) — lives at [modify-flow](../amw-diagram-formats/references/modify-flow.md). Do NOT re-implement the pipeline locally.
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references

User intents that trigger the modify path (vs. create):

- "edit this ASCII diagram" / "modify this `.txt` file" / "update the ASCII at `<path>`"
- "change the label of box X" / "rename node X to Y" / "replace label A with label B"
- "add a connector from A to B" / "remove the edge between X and Y" / "insert a box between X and Y"

All three intents resolve to the same pipeline; the only thing that varies is step 3 (patch). MVP patching is text substitution on the parsed IR's `nodes[*].label` and `edges[*]` fields. Every modified artifact re-passes `bin/amw-validate-ascii.py` before save — a modify that would FAIL validation is rejected and the original file is left untouched.
