---
name: amw-box-diagram
description: Author clean Unicode rounded-corner box diagrams (╭╮╰╯│─) for pipelines, workflow charts, microservices topologies. Triggers on "box diagram of", "Unicode pipeline diagram", "fan-out/fan-in", "rounded-corner box diagram", "microservices topology". Does NOT trigger on broad design vocabulary — routes to `design-principles`. All output MUST pass `../../bin/amw-validate-ascii.py`. Use when creating a Unicode box diagram. Trigger with /amw-create-or-modify-ascii-diagram.
version: 0.1.0
---

# Box Diagram

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor. Narrow technical triggers only — the orchestrator routes here for clean rectangular Unicode box diagrams (pipelines, fan-out/fan-in, layered service topologies).

## Overview

Authors clean Unicode rounded-corner box diagrams (`╭╮╰╯│─`) for pipelines, workflow charts, microservices topologies, and incident-response flows. All output must pass `bin/amw-validate-ascii.py` before emission.

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during Phase A (low-fi pipeline/topology sketches) or Phase B (validated box-diagram artifact). Autonomous and self-contained — any agent can use it by reading this SKILL.md and its references; techniques are not limited to what matching commands expose.

## Position in flow

**OUTPUT.** Emits a monospaced Unicode box diagram (rounded corners `╭ ╮ ╰ ╯`, rules `─ │`, T-junctions `┌ ┐ └ ┘ ┬ ┴ ├ ┤ ┼`, arrowheads `▸ ▾ ▴ ◂`) for terminals, README/ADR/runbook code fences, and chat. Not a wireframe skill — structured box-and-arrow flow only.

## Trigger conditions

Fires on: *"draw a box diagram of <system>"*, *"Unicode pipeline diagram"*, *"fan-out / fan-in diagram"*, *"rounded-corner box diagram"*, *"microservices box topology / service dependency boxes"*, *"incident-response flow diagram"*, *"workflow box chart"*, *"rewrite this ASCII `+--+` with Unicode corners"*.

Do **not** activate on generic "design", "UI", "wireframe", "mockup", "landing page" → `../amw-design-principles/`. Freehand ASCII wireframes → `../amw-ascii-sketch/`; ASCII→SVG → `../amw-ascii-to-svg/`; structured JSON→ASCII (sequence/table/layers) → `../amw-ascii-validator/` render mode.

## Why rounded Unicode over ASCII `+--+`

Rounded-corner Unicode reads cleaner than classic `+--+` (single-width glyphs that don't collide with text), and the rounded-outer (`╭ ╮ ╰ ╯`) vs sharp-inner (`┌ ┐ └ ┘ ┬ ┴ ├ ┤ ┼`) split is load-bearing — it lets the reader follow branching flow without counting arrows. It pairs with the plugin's ASCII-first plan phase (same medium + validation gate as `../amw-ascii-sketch/`). If the target can't render UTF-8 (old terminals, CI log viewers), fall back to `+--+` via `../amw-ascii-diagrams-reference/`.

## Non-negotiables

Every diagram **MUST** pass `python3 bin/amw-validate-ascii.py /tmp/box-diagram-<slug>.txt` before presentation — same gate `../amw-ascii-sketch/` uses; see [SKILL](../amw-ascii-validator/SKILL.md) for the contract and full catch-list (double-width glyphs, inconsistent frame widths, connector misalignment, broken borders, stray tabs). On FAIL, apply `FIX:` hints and re-validate; never show un-validated output.

Beyond the validator: never use emoji inside boxes (all double-width); never re-type after validation — read the validated file and paste its exact bytes (one lost space shifts every corner below); max box width ≈ 60 chars (wider → split into stacked boxes or use multi-line rich content, Example C).

## Character set

Outer rounded corners `╭ ╮ ╰ ╯` (U+256D..F); inner sharp corners `┌ ┐ └ ┘` (U+250C..18); rules `─` (U+2500) `│` (U+2502); T-junctions `┬ ┴ ├ ┤ ┼` (U+252C..3C); arrowheads `▸ ◂ ▾ ▴` (U+25B8/C2/BE/B4); inline content arrows `→ ← ↑ ↓` (U+2190..3). Full table at [TECH-unicode-rounded-corner-set](./references/TECH-unicode-rounded-corner-set.md).

`▼ ▲ ▶ ◀` (U+25BC/B2/B6/C0) are BANNED — variable-width in many fonts; the validator rejects them.

## Extended connection-type vocabulary

The base unidirectional arrows above (`▸ ▾ ▴ ◂`) cover simple flows. For richer relationships — `return` (`◂───`), `bidirectional` (`◂──▸`), `async event` (`- - ▸`), hollow `dependency` (`───▷`), plain `association` (`────`) — see [TECH-arrow-head-variants](./references/TECH-arrow-head-variants.md). All survive `validate-ascii.py` (no variable-width glyphs). Keep one connector style per diagram unless the diagram's whole point is contrasting sync vs async.

## Semantic node shapes (optional authoring conventions)

For diagrams that distinguish **what kind of thing** each node is — database cylinder (`╭─╮ │ DB │ ╰─╯`), queue tilde-ribbon (`≋` U+224B), external dashed border (`╌`/`╎`), decision point (prefer a labelled `│ Valid? │` box with `──yes──▸` / `──no──▸` branches, never a diamond) — see [TECH-semantic-node-shapes](./references/TECH-semantic-node-shapes.md). These are authoring conventions, not validator rules. Keep mixed shapes on the same column grid so connectors line up.

## Example A — Simple pipeline (3 sequential boxes)

Single horizontal line, `▸` arrowhead between equal-width boxes. Trigger: *"show the CI pipeline as boxes"*.

```
╭──────────────╮   ╭──────────────╮   ╭──────────────╮
│ git push     │──▸│ Build        │──▸│ Lint         │
╰──────────────╯   ╰──────────────╯   ╰──────────────╯
```

## Example B — Fan-out / fan-in (pipeline with parallel stages)

Parallel stages between two sequential boxes: `┌──┬──┤` across the top of the child row fans three branches out, matching `└──┼──┘` at the bottom fans them back in. Full worked diagram (git push → Build → Lint → 3 parallel test suites → Release → Staging/Production) at [TECH-fan-out-fan-in-junctions](./references/TECH-fan-out-fan-in-junctions.md), and verbatim in [`examples/ci-cd-pipeline.txt`](examples/ci-cd-pipeline.txt). Trigger phrasing: *"fan-out to Unit/API/E2E then fan-in to Release"*, *"pipeline with three parallel test suites"*.

## Example C — Multi-line rich-content boxes

A box with title row + full-width `─` separator (`│ ` + `─ * inner_width` + ` │`) + 2-5 body lines, all padded to one inner width. Blank lines are `│` + spaces + `│`; inline `→ ← ↑ ↓` safe, `▼ ▲ ▶ ◀`/emoji/CJK banned. Full worked runbook at [TECH-multi-line-rich-content-box](./references/TECH-multi-line-rich-content-box.md), verbatim in [`examples/incident-response.txt`](examples/incident-response.txt). Trigger: *"detailed incident-response flow"*.

## Canonical example files

`examples/` holds three gold-standard artifacts (each passes `../../bin/amw-validate-ascii.py` verbatim). Open the closest one as an alignment baseline and copy/rename labels — alignment holds as long as the new label fits the original `inner_width`.

| File | Shape | Use as template for |
|---|---|---|
| [`examples/ci-cd-pipeline.txt`](examples/ci-cd-pipeline.txt) | Linear flow → 3-way fan-out → fan-in → 2-way fan-out | CI/CD pipelines, build stages, deploy gates |
| [`examples/microservices.txt`](examples/microservices.txt) | 2 entry points → LB → gateway → 3 services (+ sidecar queue) → 3 datastores | Microservice topology, service dependency maps |
| [`examples/incident-response.txt`](examples/incident-response.txt) | Multi-line rich boxes + 3-way branch → rejoin → 2 final boxes | Runbooks, incident playbooks, procedure flows |

## Instructions

1. Open the closest canonical example from `examples/` (incident-response, ci-cd-pipeline, or microservices) as the alignment baseline. Define a **sticky grid** — fixed column positions where every box in a column shares one left-edge offset.
2. Author/edit boxes with the Unicode rounded-corner set (`╭╮╰╯│─`), consistent `inner_width` per row. Pad each content line: `│` + space + text + `' ' * (inner_width - len(text))` + space + `│`; `assert len(text) <= inner_width` before generating. For 3+ boxes, use Python `border_top` / `border_bot` / `box_line` helpers ([TECH-python-helper-pattern](./references/TECH-python-helper-pattern.md)).
3. Build fan-out/fan-in junctions: `┌ ─ ┬ ─ ┐` across the child-row top, `└ ─ ┴ ─ ┘` across the bottom; `▸ ▾` arrowheads (never banned `▶ ▼`).
4. Validate with `bin/amw-validate-ascii.py`; all box corners must share exact column offsets.
5. Iterate on FIX hints until PASS; never present an unvalidated diagram.
6. Save the artifact with a descriptive English filename and write the job-completion report to `reports/webdesigner/`.

## References

Every technique lives in `./references/` (TOC: *What it does · When to use · How it works · Minimal example · Gotchas · Cross-references*) — arrow-head-variants, fan-out-fan-in-junctions, multi-line-rich-content-box, python-helper-pattern, semantic-node-shapes, and unicode-rounded-corner-set are linked inline above; see also [TECH-output-from-validated-file](./references/TECH-output-from-validated-file.md) (paste validated bytes, never re-type).

<!-- end of references -->

## Output

A validator-PASS Unicode box diagram (rounded corners `╭╮╰╯`, rules `─│`, T-junctions, `▸ ▾ ▴ ◂` arrowheads), pasted verbatim from the validated file into a code fence, plus a job-completion report. Every diagram MUST pass `../../bin/amw-validate-ascii.py` before presentation. See [skill-completion-and-output-contract](../amw-design-principles/references/skill-completion-and-output-contract.md) for the shared checklist + report contract; this skill's `## Non-negotiables` lists the additions.

## Prerequisites

- **runtime_binaries:** `perl >= 5.10` (pre-installed on macOS and most Linux distros — `/amw-doctor` checks) **OR** `python3 >= 3.8` (Windows-friendly fallback — `bin/amw-validate-ascii.py` has identical behavior)
- **python_packages:** none (pure stdlib)
- **cpan / npm:** none

## Examples

Example A (simple pipeline), Example B (fan-out/fan-in), and Example C (multi-line rich-content) above; full verbatim artifacts in `examples/`.

## Resources

- [SKILL](../amw-ascii-validator/SKILL.md) — mandatory validation gate; `../../bin/amw-validate-ascii.py` — validator (Python, group-aware width, FIX hints, Windows-compatible).
- [SKILL](../amw-ascii-sketch/SKILL.md) — upstream peer (wireframe layouts vs flow diagrams); [SKILL](../amw-ascii-to-svg/SKILL.md) — downstream (box → SVG); [SKILL](../amw-diagram-svg/SKILL.md) — direct-SVG path; [SKILL](../amw-ascii-diagrams-reference/SKILL.md) — classic-ASCII `+--+` counterpart for legacy contexts.
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — misaligned boxes are a form of slop.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| WIDE_CHAR on a working glyph | emoji / `▼ ▲ ▶ ◀` slipped in | Replace with `▾ ▴ ▸ ◂` or `v ^ > <` |
| WIDTH_MISMATCH on a multi-line box | content line ≠ frame inner width | Re-pad every line with trailing spaces |
| Vertical `│` walks one column between rows | upper-row boxes differ in width | Re-equalize upper-row boxes (same `inner_width`) |
| Fan-out `┌ ┬ ┐` misaligned with children | parent/child column offsets differ | Fix the grid — one left-edge offset per column |
| Looks right in reply, breaks in terminal | terminal not UTF-8 / proportional font | Fall back to `../amw-ascii-diagrams-reference/` (`+ - \|` only) |
