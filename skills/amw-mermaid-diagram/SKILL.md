---
name: amw-mermaid-diagram
description: Author OR edit Mermaid source — flowchart, sequenceDiagram, stateDiagram-v2, classDiagram, erDiagram, gantt, pie, journey, mindmap. Triggers on "create Mermaid diagram", "modify Mermaid at a file path", "edit .mmd file", "write mermaid source". Does NOT claim generic design vocabulary. Distinct from mermaid-render (renders only) — this skill OWNS AUTHORING + MODIFYING. Use when authoring/editing Mermaid source. Trigger with /amw-create-or-modify-mermaid-diagram.
version: 0.1.0
---

# Mermaid Diagram — thin authoring + modify skill

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Format spec (authoritative):** [mermaid](../amw-diagram-formats/references/mermaid.md).
> **Modify pipeline (authoritative):** [modify-flow](../amw-diagram-formats/references/modify-flow.md).

This skill does not redefine Mermaid grammar / themes / mmdc flags / output paths / the 40-technique catalog — every one of those lives once in [mermaid](../amw-diagram-formats/references/mermaid.md). The skill's job is to AUTHOR Mermaid source text from a natural-language brief (for all 9 grammar types), and to run the shared modify-flow when the input is an existing `.mmd` / `.mermaid` file. Rendering is delegated to `../amw-mermaid-render/` — this skill produces and mutates the SOURCE; it does not emit SVG/PNG/ASCII directly.

## Overview

Thin authoring and modify skill for Mermaid diagram source text. Accepts a natural-language brief (create path) or an existing `.mmd` / `.mermaid` file (modify path). Runs the shared 5-step modify-flow (detect → parse → IR → re-render to Mermaid source → lint). Supports all 9 Mermaid grammar types: flowchart, sequenceDiagram, stateDiagram-v2, classDiagram, erDiagram, gantt, pie, journey, mindmap. Validates emitted source via `bin/amw-mermaid-lint.sh` (`mmdc` dry-run). Delegates actual SVG/PNG/ASCII rendering to `amw-mermaid-render`.

## Instructions

1. Detect whether the input is a natural-language brief (create path) or an existing `.mmd`/`.mermaid` file with a Mermaid grammar header (modify path).
2. For modify path: parse to IR with `bin/amw-parse-mermaid-diagram.py`; apply the requested edit to `nodes[*].label` or `edges[*].label` in the IR.
3. For create path: select the grammar type from the brief (flowchart for "flow/process", sequenceDiagram for "request/response", erDiagram for "schema/DB", etc.); emit grammar directly.
4. Re-render to Mermaid source text via `bin/amw-diagram-ir.py emit --format mermaid`.
5. Validate with `bin/amw-mermaid-lint.sh` (mmdc dry-run); a FAIL aborts and leaves the original file untouched (retry budget = 3).
6. See [pipeline-detail](./references/pipeline-detail.md) for the authoritative execution sequence + component detection table + output contract.

## Activation

Callable directly via the `/amw-create-or-modify-mermaid-diagram` command (user shortcut for users who already know they want Mermaid source and have either a brief or an existing `.mmd` to modify), or invoked by the `design-principles` orchestrator during **Phase B** when the approved deliverable is Mermaid diagram source. An agent in Main-agent mode may also invoke this skill directly via the orchestrator without going through the command.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT (mid-pipeline). Emits exactly one `.mmd` (or `.mermaid`) source file containing valid Mermaid grammar. The caller typically chains this with `/amw-convert-any-diagram-format` or directly with `../amw-mermaid-render/` via `bin/amw-mermaid-render.sh` for SVG/PNG/ASCII output. Upstream of `../amw-mermaid-render/`; downstream of `../amw-ux-flows/` (PRD → Mermaid) and `../amw-diagram-architecture/` (arch → Mermaid emission).

## Trigger conditions

- "create a Mermaid flowchart / sequence / state / class / ER / gantt / pie / journey / mindmap"
- "write Mermaid source for <subject>" / "author a `.mmd` file for <subject>"
- "modify this Mermaid diagram" / "edit the Mermaid at `<path>`" / "update `<something>.mmd>`"
- "/amw-create-or-modify-mermaid-diagram <brief-or-path>"

Do NOT activate on:
- "render this Mermaid to SVG / PNG / ASCII" — that is `../amw-mermaid-render/`'s job.
- Generic "diagram the login flow" without an explicit Mermaid request — orchestrator may pick a different format.
- Validating a Mermaid file only (`/amw-validate-any-diagram-format`).

## Pipeline (5 steps)

Authoritative sequence + component detection table + output contract: [pipeline-detail](./references/pipeline-detail.md). Summary:

1. **Detect** — modify path (existing `.mmd`/`.mermaid` or grammar header content) vs create path (natural-language brief).
2. **Parse** (modify only) → IR via `bin/amw-parse-mermaid-diagram.py`.
3. **IR op** — emit grammar (create) or text-substitute on `nodes[*].label`/`edges[*].label` (modify).
4. **Re-render** to Mermaid source via `bin/amw-diagram-ir.py emit --format mermaid`.
5. **Re-validate** via `bin/amw-mermaid-lint.sh` (mmdc dry-run). FAIL aborts; retry budget = 3.

## Rendering (delegated)

This skill emits `.mmd` source only. To render the emitted source to SVG / PNG / ASCII, call `../amw-mermaid-render/` via `bin/amw-mermaid-render.sh`:

```bash
bin/amw-mermaid-render.sh --input <file>.mmd --format svg --theme tokyo-night --out <file>.svg
```

See [SKILL](../amw-mermaid-render/SKILL.md) and [mermaid](../amw-diagram-formats/references/mermaid.md) §5 for the full output-path options (SVG default, PNG via cairosvg, ASCII via `--format ascii`, pure-ASCII via `--use-ascii`).

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8`, `node >= 22`, `mmdc` (mermaid-cli) — all checked by `/amw-doctor`; `mmdc` installed by `/amw-init`.
- **python_packages:** none (`bin/amw-parse-mermaid-diagram.py` is stdlib-only).
- **npm:** `@mermaid-js/mermaid-cli` (for `mmdc` dry-run validation); auto-installed by the vendored `external/mermaid-render/` if absent.
- **Shared scripts:** `bin/amw-parse-mermaid-diagram.py`, `bin/amw-diagram-ir.py`, `bin/amw-mermaid-lint.sh`, `bin/amw-mermaid-render.sh` (for downstream rendering only — not part of this skill's pipeline).

## Resources

- [pipeline-detail](./references/pipeline-detail.md) — 5-step execution sequence + component detection table + output contract + completion checklist.
- [technique-catalog](./references/technique-catalog.md) — decision tree + per-TECH file TOC summary (14 TECH files across 9 grammar branches).
- [mermaid](../amw-diagram-formats/references/mermaid.md) — authoritative Mermaid format spec + 40-technique catalog.
- [modify-flow](../amw-diagram-formats/references/modify-flow.md) — authoritative 6-step modify pipeline.
- [ir-schema](../amw-diagram-formats/references/ir-schema.md) — IR schema consumed by `bin/amw-diagram-ir.py`.
- [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md) — unified validator output contract.
- [SKILL](../amw-mermaid-render/SKILL.md) — rendering skill (source → SVG/PNG/ASCII). This skill delegates rendering to that one.
- [SKILL](../amw-diagram-architecture/SKILL.md) — upstream when architecture brief emits Mermaid.
- [SKILL](../amw-ux-flows/SKILL.md) — upstream when PRD emits Mermaid wireframes.
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.

## Non-negotiables

- Exactly one `.mmd` source file per invocation. Content starts with a Mermaid grammar header — no prose preamble inside the file.
- Every emitted `.mmd` passes `bin/amw-mermaid-lint.sh` (`mmdc` dry-run). A FAIL aborts; the original file is untouched.
- Labels with spaces / special chars are quoted: `A["Two Words"]`. (mermaid TECH-MM-35)
- Multi-statement input uses `\n` separators, never `;` (shell-safe). (mermaid TECH-MM-34)
- This skill does NOT render `.mmd` → SVG/PNG/ASCII — that is `../amw-mermaid-render/`'s role. The two skills are intentionally separated.
- Do NOT re-author the Mermaid spec inside this skill — reference [mermaid](../amw-diagram-formats/references/mermaid.md). If a rule is wrong, fix it there.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| `bin/amw-mermaid-lint.sh` FAIL: `Parse error on line N` | Syntax typo in node/edge | Return the validator report verbatim; test at `https://mermaid.live`; do not guess-repair. |
| Labels contain shell metacharacters | User brief embedded quotes / semicolons | Quote labels with `A["..."]` form (TECH-MM-35). |
| Modify path hits retry budget 3 FAILs | Patch conflicts with grammar structure | Surface the lint report; ask the user to refine the edit. |
| Parser returns empty IR (modify path) | File is NOT Mermaid (missing header) or uses an unsupported grammar | Raw-source stub per `modify-flow.md` §5.4; warn that structural patching is unavailable until the Phase 1 grammar parser lands. |
| User asks for render | Wrong skill | Produce / modify the `.mmd` here, then call `bin/amw-mermaid-render.sh` or route through `../amw-mermaid-render/`. |

## Examples

See the technique reference files under `./references/` for grammar examples (e.g. `TECH-flowchart-grammar.md`, `TECH-sequence-grammar.md`, `TECH-er-grammar.md`) and the worked minimal examples in each file's "Minimal example" section.

## Technique selection

Top-level branches (counts of techniques) — full decision tree + per-TECH TOC summary at [technique-catalog](./references/technique-catalog.md):

- **sequence** (3): activations · grammar · notes-and-loops
- **edge** (2): best-practices · styles
- **er** (2): best-practices · grammar
- **flowchart** (2): best-practices · grammar
- **class** (1): grammar
- **diagram** (1): file-organization
- **state** (1): grammar
- **subgraph** (1): grouping
- **terminal** (1): ascii-wrapper

## Output

Produces a `.mmd` source file at a project-inferred path + a job-completion report at `$MAIN_ROOT/reports/webdesigner/<ts>_<slug>_<hash>.md`. Full output contract + completion checklist: [pipeline-detail](./references/pipeline-detail.md) §"Output contract" and §"Completion checklist".
