---
name: amw-mermaid-diagram
description: Author OR edit Mermaid diagram source — flowchart, sequenceDiagram, stateDiagram-v2, classDiagram, erDiagram, gantt, pie, journey, mindmap. Triggers on narrow technical intents only — "create Mermaid diagram", "modify Mermaid at a file path", "edit this .mmd file", "write mermaid source for a subject", "/amw-create-or-modify-mermaid-diagram". Does NOT claim generic design vocabulary. Distinct from mermaid-render (which only renders source → SVG/PNG/ASCII). This skill owns AUTHORING + MODIFYING Mermaid source text. Use when authoring or editing Mermaid diagram source text across any of the nine supported grammar types. Trigger with /amw-create-or-modify-mermaid-diagram.
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
6. See the `## Pipeline (5 steps — matches shared modify-flow)` section below for the authoritative execution sequence.

See the `## Pipeline (5 steps — matches shared modify-flow)` section below for the authoritative execution sequence.

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

## Component detection table (excerpt)

Full 9-grammar + node-shape + edge + theme + flag catalog lives in [mermaid](../amw-diagram-formats/references/mermaid.md) §2 + §8 (40 techniques). The 8 rows below are the most common dispatch cues — consult the ref for the rest.

| Mermaid construct | IR node/edge kind | Ref |
|---|---|---|
| `A[Text]` | `node{shape:rect, kind:process}` | [mermaid](../amw-diagram-formats/references/mermaid.md) TECH-MM-24 |
| `A([Text])` | `node{shape:stadium, kind:start-end}` | ref §2.1 |
| `A[(Text)]` | `node{shape:cylinder, kind:database}` | ref §2.1 |
| `A{Text}` | `node{shape:diamond, kind:decision}` | ref §2.1 |
| `A --> B` | `edge{style:solid, kind:sync}` | ref TECH-MM-25 |
| `A -.-> B` | `edge{style:dotted, kind:async}` | ref TECH-MM-25 |
| `A -->\|label\| B` | `edge{label:"label"}` | ref TECH-MM-26 |
| `subgraph Name ... end` | group container (`layout:nested`) | ref TECH-MM-27 |

## Pipeline (5 steps — matches shared modify-flow)

1. **Detect** source shape. If `$ARGUMENTS` is a path to an existing `.mmd` / `.mermaid` OR content starts with a Mermaid grammar header (`flowchart|graph|sequenceDiagram|stateDiagram|stateDiagram-v2|classDiagram|erDiagram|gantt|pie|journey|mindmap|quadrantChart|gitGraph|C4Context`) → **modify path**. If it's a natural-language brief → **create path**.
2. **Parse** (modify path only) via `bin/amw-parse-mermaid-diagram.py` → IR (schema: [ir-schema](../amw-diagram-formats/references/ir-schema.md)). Regex-based per-grammar parsing. Create path skips this step.
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
3. **IR operation:**
   - Create path → select the grammar type from the brief (flowchart is default for "flow" / "process" intent; sequenceDiagram for "request/response" / "handshake"; erDiagram for "schema" / "database relationships"; etc — see [mermaid](../amw-diagram-formats/references/mermaid.md) §2). Emit grammar directly.
     > Format definition · Supported grammars · Themes · mmdc CLI flags (17 total) · Output paths · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · Anti-patterns · SKILL · SKILL · SKILL · `../../external/mermaid-render/` — vendored beautiful-mermaid backend · `../../bin/amw-mermaid-render.sh` — shell wrapper (SVG / PNG / ASCII) · `../../bin/amw-mermaid-lint.sh` (planned; Task 0c) — validator wrapper (`mmdc` dry-run) · `../../bin/amw-validate-ascii.py` — warn-only gate on ASCII rendering · ir-schema · conversion-matrix · validation-dispatcher
     > Format definition · 1 File conventions · 2 Minimal example · Supported grammars · 1 Node shapes (flowchart) · 2 Edges (flowchart) · Themes · 1 Built-in themes (15) · 2 Theme-selection guide · 3 Mono Mode (2-color derivation) · 4 7-color enriched palette · 5 Live theme-switching (browser) · mmdc CLI flags (17 total) · Output paths · 1 Mermaid → SVG (default, high fidelity) · 2 Mermaid → PNG (via `mmdc -t png`) · 3 Mermaid → ASCII (Unicode default) · 4 Mermaid → pure ASCII (README-safe) · 5 Batch rendering (parallel) · Validation · 1 Dry-run linting · 2 Common validation failures · Per-source breakdown of the technique catalog · Technique catalog · S1 — beautiful-mermaid (backend) · S2 — Pretty-mermaid + mermaid-render/SKILL.md (CLI) · S3 — Mermaid grammar · S4 — agent-skill-diagramming-flows · S5 — bin/amw-mermaid-render.sh wrapper · Failure modes · …(+11)
   - Modify path → apply the user's requested edit to the IR (text substitution on `nodes[*].label` / `edges[*].label` for MVP; grammar-aware structural operations once Phase 1 parsers land — see [modify-flow](../amw-diagram-formats/references/modify-flow.md) §5.4).
     > The pipeline · Create vs modify dispatch · Step-by-step detail · Step 1 — Detect · Step 2 — Parse to IR · Step 3 — Patch · Step 4 — (loop point) · Step 5 — Emit · Step 6 — Re-validate · Work directory and file naming · Per-format guidance · 1 ASCII modify (MVP structural) · 2 HTML modify (MVP raw-source; Phase 1 structural) · 3 SVG modify (MVP raw-source; Phase 1 structural) · 4 Mermaid modify (MVP raw-source; Phase 1 structural) · Conversion is a modify-flow variant · Composition with round-trip skills · 1 `diagram-webpage-sync` (`/amw-modify-webpage-from-diagram`) · 2 `webpage-to-diagram` (`/amw-modify-diagram-of-webpage`) · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
4. **Re-render** (to Mermaid source, not SVG/PNG) via `bin/amw-diagram-ir.py emit --format mermaid`. Per-kind grammar emitters map IR back to the appropriate Mermaid syntax.
5. **Re-validate** via `bin/amw-mermaid-lint.sh` (wraps `mmdc -i <file> -o /tmp/_mermaid_lint.svg` dry-run — exit 0 = valid; unified PASS/FAIL contract per [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md)). A FAIL aborts and leaves the original file untouched. Retry budget = 3.
  > Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · 1 ASCII — `bin/amw-validate-ascii.py` (primary) and `bin/amw-validate-ascii.py` (fallback) · 2 SVG — `bin/amw-validate-svg-diagram.sh` · 3 HTML — `bin/amw-validate-html-diagram.sh` · 4 Mermaid — `bin/amw-mermaid-lint.sh` · Caller integration patterns · 1 Post-create gate · 2 Post-convert gate · 3 Modify-flow loop · 4 Multi-format mode (ascii-validator) · Known limitations (Phase 0) · Related references

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

- [mermaid](../amw-diagram-formats/references/mermaid.md) — authoritative Mermaid format spec + 40-technique catalog.
  > Format definition · Supported grammars · Themes · mmdc CLI flags (17 total) · Output paths · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · Anti-patterns · SKILL · SKILL · SKILL · `../../external/mermaid-render/` — vendored beautiful-mermaid backend · `../../bin/amw-mermaid-render.sh` — shell wrapper (SVG / PNG / ASCII) · `../../bin/amw-mermaid-lint.sh` (planned; Task 0c) — validator wrapper (`mmdc` dry-run) · `../../bin/amw-validate-ascii.py` — warn-only gate on ASCII rendering · ir-schema · conversion-matrix · validation-dispatcher
  > Format definition · 1 File conventions · 2 Minimal example · Supported grammars · 1 Node shapes (flowchart) · 2 Edges (flowchart) · Themes · 1 Built-in themes (15) · 2 Theme-selection guide · 3 Mono Mode (2-color derivation) · 4 7-color enriched palette · 5 Live theme-switching (browser) · mmdc CLI flags (17 total) · Output paths · 1 Mermaid → SVG (default, high fidelity) · 2 Mermaid → PNG (via `mmdc -t png`) · 3 Mermaid → ASCII (Unicode default) · 4 Mermaid → pure ASCII (README-safe) · 5 Batch rendering (parallel) · Validation · 1 Dry-run linting · 2 Common validation failures · Per-source breakdown of the technique catalog · Technique catalog · S1 — beautiful-mermaid (backend) · S2 — Pretty-mermaid + mermaid-render/SKILL.md (CLI) · S3 — Mermaid grammar · S4 — agent-skill-diagramming-flows · S5 — bin/amw-mermaid-render.sh wrapper · Failure modes · …(+11)
- [modify-flow](../amw-diagram-formats/references/modify-flow.md) — authoritative 6-step modify pipeline.
  > The pipeline · Create vs modify dispatch · Step-by-step detail · Step 1 — Detect · Step 2 — Parse to IR · Step 3 — Patch · Step 4 — (loop point) · Step 5 — Emit · Step 6 — Re-validate · Work directory and file naming · Per-format guidance · 1 ASCII modify (MVP structural) · 2 HTML modify (MVP raw-source; Phase 1 structural) · 3 SVG modify (MVP raw-source; Phase 1 structural) · 4 Mermaid modify (MVP raw-source; Phase 1 structural) · Conversion is a modify-flow variant · Composition with round-trip skills · 1 `diagram-webpage-sync` (`/amw-modify-webpage-from-diagram`) · 2 `webpage-to-diagram` (`/amw-modify-diagram-of-webpage`) · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
- [ir-schema](../amw-diagram-formats/references/ir-schema.md) — IR schema consumed by `bin/amw-diagram-ir.py`.
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
- [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md) — unified validator output contract.
  > Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · 1 ASCII — `bin/amw-validate-ascii.py` (primary) and `bin/amw-validate-ascii.py` (fallback) · 2 SVG — `bin/amw-validate-svg-diagram.sh` · 3 HTML — `bin/amw-validate-html-diagram.sh` · 4 Mermaid — `bin/amw-mermaid-lint.sh` · Caller integration patterns · 1 Post-create gate · 2 Post-convert gate · 3 Modify-flow loop · 4 Multi-format mode (ascii-validator) · Known limitations (Phase 0) · Related references
- [SKILL](../amw-mermaid-render/SKILL.md) — rendering skill (source → SVG/PNG/ASCII). This skill delegates rendering to that one.
- [SKILL](../amw-diagram-architecture/SKILL.md) — upstream when architecture brief emits Mermaid.
- [SKILL](../amw-ux-flows/SKILL.md) — upstream when PRD emits Mermaid wireframes.
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.

## Non-negotiables

- Exactly one `.mmd` source file per invocation. Content starts with a Mermaid grammar header — no prose preamble inside the file.
- Every emitted `.mmd` passes `bin/amw-mermaid-lint.sh` (`mmdc` dry-run). A FAIL aborts; the original file is untouched.
- Labels with spaces / special chars are quoted: `A["Two Words"]`. ([mermaid](../amw-diagram-formats/references/mermaid.md) TECH-MM-35)
  > Format definition · Supported grammars · Themes · mmdc CLI flags (17 total) · Output paths · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · Anti-patterns · SKILL · SKILL · SKILL · `../../external/mermaid-render/` — vendored beautiful-mermaid backend · `../../bin/amw-mermaid-render.sh` — shell wrapper (SVG / PNG / ASCII) · `../../bin/amw-mermaid-lint.sh` (planned; Task 0c) — validator wrapper (`mmdc` dry-run) · `../../bin/amw-validate-ascii.py` — warn-only gate on ASCII rendering · ir-schema · conversion-matrix · validation-dispatcher
  > Format definition · 1 File conventions · 2 Minimal example · Supported grammars · 1 Node shapes (flowchart) · 2 Edges (flowchart) · Themes · 1 Built-in themes (15) · 2 Theme-selection guide · 3 Mono Mode (2-color derivation) · 4 7-color enriched palette · 5 Live theme-switching (browser) · mmdc CLI flags (17 total) · Output paths · 1 Mermaid → SVG (default, high fidelity) · 2 Mermaid → PNG (via `mmdc -t png`) · 3 Mermaid → ASCII (Unicode default) · 4 Mermaid → pure ASCII (README-safe) · 5 Batch rendering (parallel) · Validation · 1 Dry-run linting · 2 Common validation failures · Per-source breakdown of the technique catalog · Technique catalog · S1 — beautiful-mermaid (backend) · S2 — Pretty-mermaid + mermaid-render/SKILL.md (CLI) · S3 — Mermaid grammar · S4 — agent-skill-diagramming-flows · S5 — bin/amw-mermaid-render.sh wrapper · Failure modes · …(+11)
- Multi-statement input uses `\n` separators, never `;` (shell-safe). ([mermaid](../amw-diagram-formats/references/mermaid.md) TECH-MM-34)
  > Format definition · Supported grammars · Themes · mmdc CLI flags (17 total) · Output paths · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · Anti-patterns · SKILL · SKILL · SKILL · `../../external/mermaid-render/` — vendored beautiful-mermaid backend · `../../bin/amw-mermaid-render.sh` — shell wrapper (SVG / PNG / ASCII) · `../../bin/amw-mermaid-lint.sh` (planned; Task 0c) — validator wrapper (`mmdc` dry-run) · `../../bin/amw-validate-ascii.py` — warn-only gate on ASCII rendering · ir-schema · conversion-matrix · validation-dispatcher
  > Format definition · 1 File conventions · 2 Minimal example · Supported grammars · 1 Node shapes (flowchart) · 2 Edges (flowchart) · Themes · 1 Built-in themes (15) · 2 Theme-selection guide · 3 Mono Mode (2-color derivation) · 4 7-color enriched palette · 5 Live theme-switching (browser) · mmdc CLI flags (17 total) · Output paths · 1 Mermaid → SVG (default, high fidelity) · 2 Mermaid → PNG (via `mmdc -t png`) · 3 Mermaid → ASCII (Unicode default) · 4 Mermaid → pure ASCII (README-safe) · 5 Batch rendering (parallel) · Validation · 1 Dry-run linting · 2 Common validation failures · Per-source breakdown of the technique catalog · Technique catalog · S1 — beautiful-mermaid (backend) · S2 — Pretty-mermaid + mermaid-render/SKILL.md (CLI) · S3 — Mermaid grammar · S4 — agent-skill-diagramming-flows · S5 — bin/amw-mermaid-render.sh wrapper · Failure modes · …(+11)
- This skill does NOT render `.mmd` → SVG/PNG/ASCII — that is `../amw-mermaid-render/`'s role. The two skills are intentionally separated.
- Do NOT re-author the Mermaid spec inside this skill — reference [mermaid](../amw-diagram-formats/references/mermaid.md). If a rule is wrong, fix it there.
  > Format definition · Supported grammars · Themes · mmdc CLI flags (17 total) · Output paths · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · Anti-patterns · SKILL · SKILL · SKILL · `../../external/mermaid-render/` — vendored beautiful-mermaid backend · `../../bin/amw-mermaid-render.sh` — shell wrapper (SVG / PNG / ASCII) · `../../bin/amw-mermaid-lint.sh` (planned; Task 0c) — validator wrapper (`mmdc` dry-run) · `../../bin/amw-validate-ascii.py` — warn-only gate on ASCII rendering · ir-schema · conversion-matrix · validation-dispatcher
  > Format definition · 1 File conventions · 2 Minimal example · Supported grammars · 1 Node shapes (flowchart) · 2 Edges (flowchart) · Themes · 1 Built-in themes (15) · 2 Theme-selection guide · 3 Mono Mode (2-color derivation) · 4 7-color enriched palette · 5 Live theme-switching (browser) · mmdc CLI flags (17 total) · Output paths · 1 Mermaid → SVG (default, high fidelity) · 2 Mermaid → PNG (via `mmdc -t png`) · 3 Mermaid → ASCII (Unicode default) · 4 Mermaid → pure ASCII (README-safe) · 5 Batch rendering (parallel) · Validation · 1 Dry-run linting · 2 Common validation failures · Per-source breakdown of the technique catalog · Technique catalog · S1 — beautiful-mermaid (backend) · S2 — Pretty-mermaid + mermaid-render/SKILL.md (CLI) · S3 — Mermaid grammar · S4 — agent-skill-diagramming-flows · S5 — bin/amw-mermaid-render.sh wrapper · Failure modes · …(+11)

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| `bin/amw-mermaid-lint.sh` FAIL: `Parse error on line N` | Syntax typo in node/edge | Return the validator report verbatim; test at `https://mermaid.live`; do not guess-repair. |
| Labels contain shell metacharacters | User brief embedded quotes / semicolons | Quote labels with `A["..."]` form (TECH-MM-35). |
| Modify path hits retry budget 3 FAILs | Patch conflicts with grammar structure | Surface the lint report; ask the user to refine the edit. |
| Parser returns empty IR (modify path) | File is NOT Mermaid (missing header) or uses an unsupported grammar | Raw-source stub per `modify-flow.md` §5.4; warn that structural patching is unavailable until the Phase 1 grammar parser lands. |
| User asks for render | Wrong skill — produce / modify the `.mmd` here, then call `bin/amw-mermaid-render.sh` or route through `../amw-mermaid-render/`. |

## Examples

See the technique reference files under `./references/` for grammar examples (e.g. `TECH-flowchart-grammar.md`, `TECH-sequence-grammar.md`, `TECH-er-grammar.md`) and the worked minimal examples in each file's "Minimal example" section.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `mermaid-diagram` is the user asking about?
  - **sequence** (3 techniques)
    - [TECH-sequence-activations](./references/TECH-sequence-activations.md) — Sequence diagram activations
      > What it does · When to use · Syntax · Nested activations — double-stacking · Manual activate/deactivate (alt syntax) · Minimal example · Gotchas · Cross-references
    - [TECH-sequence-grammar](./references/TECH-sequence-grammar.md) — Sequence diagram grammar
      > What it does · When to use · Participants · Message arrow types · Activations — show processing time · Notes · Loops & alt/else · Minimal example · Gotchas · Cross-references
    - [TECH-sequence-notes-and-loops](./references/TECH-sequence-notes-and-loops.md) — Sequence diagram — notes, loops, alt/else blocks
      > What it does · Notes · Loops · Alt/else · `opt` — optional block (one-sided alt) · `par` — parallel block · Minimal example — realistic API flow · Gotchas · Cross-references
  - **edge** (2 techniques)
    - [TECH-edge-best-practices](./references/TECH-edge-best-practices.md) — Edge best practices — when to use which arrow
    - [TECH-edge-styles](./references/TECH-edge-styles.md) — Edge styles — arrows, lines, labels
  - **er** (2 techniques)
    - [TECH-er-best-practices](./references/TECH-er-best-practices.md) — ER diagram best practices
    - [TECH-er-grammar](./references/TECH-er-grammar.md) — ER diagram grammar (`erDiagram`)
  - **flowchart** (2 techniques)
    - [TECH-flowchart-best-practices](./references/TECH-flowchart-best-practices.md) — Flowchart authoring best practices
    - [TECH-flowchart-grammar](./references/TECH-flowchart-grammar.md) — Flowchart grammar — nodes, shapes, direction
      > What it does · When to use · Node shapes (authoritative list) · Direction tokens · Connections · Minimal example · Gotchas · Cross-references
  - **class** (1 techniques)
    - [TECH-class-grammar](./references/TECH-class-grammar.md) — Class diagram grammar
  - **diagram** (1 techniques)
    - [TECH-diagram-file-organization](./references/TECH-diagram-file-organization.md) — Diagram file organization — folder layout for `.mmd` libraries
  - **state** (1 techniques)
    - [TECH-state-grammar](./references/TECH-state-grammar.md) — State diagram grammar (`stateDiagram-v2`)
      > What it does · When to use · Basic syntax · Composite states — nested state machines · Choice pseudo-state — conditional branching · Concurrency — parallel regions · Notes · Minimal example · Gotchas · Cross-references
  - **subgraph** (1 techniques)
    - [TECH-subgraph-grouping](./references/TECH-subgraph-grouping.md) — Subgraphs — grouped nodes in flowcharts
  - **terminal** (1 techniques)
    - [TECH-terminal-ascii-wrapper](./references/TECH-terminal-ascii-wrapper.md) — Terminal ASCII authoring — Bun-style one-liner
      > What it does · When to use · The minimal wrapper · Usage patterns · The key convention — newlines not semicolons · Gotchas · Cross-references

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-class-grammar.md](./references/TECH-class-grammar.md)**
  - Description: Class diagram grammar
  - TOC:
    - What it does
    - When to use
    - Class definition
    - Visibility markers
    - Relationship arrows (UML)
    - Cardinality
    - Abstract / interface / generic
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-diagram-file-organization.md](./references/TECH-diagram-file-organization.md)**
  - Description: Diagram file organization — folder layout for `.mmd` libraries
  - TOC:
    - What it does
    - When to use
    - Recommended layout
    - Why this works
    - Naming conventions
    - Minimal example — integrated with batch render
    - Gotchas
    - Cross-references
- **[./references/TECH-edge-best-practices.md](./references/TECH-edge-best-practices.md)**
  - Description: Edge best practices — when to use which arrow
  - TOC:
    - What it does
    - When to use
    - The heuristic table
    - Label conventions
    - Arrow density rule
    - Minimal example — mixed arrows with purpose
    - Gotchas
    - Cross-references
- **[./references/TECH-edge-styles.md](./references/TECH-edge-styles.md)**
  - Description: Edge styles — arrows, lines, labels
  - TOC:
    - What it does
    - Line-and-arrow combinations
    - Inline label — two syntaxes
    - Minimal example
    - Styling edges with `linkStyle`
    - Gotchas
    - Cross-references
- **[./references/TECH-er-best-practices.md](./references/TECH-er-best-practices.md)**
  - Description: ER diagram best practices
  - TOC:
    - What it does
    - When to use
    - The rules
    - Cardinality clarity
    - Minimal example — good style
    - Gotchas
    - Cross-references
- **[./references/TECH-er-grammar.md](./references/TECH-er-grammar.md)**
  - Description: ER diagram grammar (`erDiagram`)
  - TOC:
    - What it does
    - When to use
    - Basic syntax
    - Cardinality crowsfeet
    - Attributes (optional but almost always used)
    - Attribute constraints
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-flowchart-best-practices.md](./references/TECH-flowchart-best-practices.md)**
  - Description: Flowchart authoring best practices
  - TOC:
    - What it does
    - When to use
    - The rules
    - Anti-patterns to reject
    - Minimal example — good vs bad
    - Gotchas
    - Cross-references
- **[./references/TECH-flowchart-grammar.md](./references/TECH-flowchart-grammar.md)**
  - Description: Flowchart grammar — nodes, shapes, direction
  - TOC:
    - What it does
    - When to use
    - Node shapes (authoritative list)
    - Direction tokens
    - Connections
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-sequence-activations.md](./references/TECH-sequence-activations.md)**
  - Description: Sequence diagram activations
  - TOC:
    - What it does
    - When to use
    - Syntax
    - Nested activations — double-stacking
    - Manual activate/deactivate (alt syntax)
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-sequence-grammar.md](./references/TECH-sequence-grammar.md)**
  - Description: Sequence diagram grammar
  - TOC:
    - What it does
    - When to use
    - Participants
    - Message arrow types
    - Activations — show processing time
    - Notes
    - Loops & alt/else
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-sequence-notes-and-loops.md](./references/TECH-sequence-notes-and-loops.md)**
  - Description: Sequence diagram — notes, loops, alt/else blocks
  - TOC:
    - What it does
    - Notes
    - Loops
    - Alt/else
    - `opt` — optional block (one-sided alt)
    - `par` — parallel block
    - Minimal example — realistic API flow
    - Gotchas
    - Cross-references
- **[./references/TECH-state-grammar.md](./references/TECH-state-grammar.md)**
  - Description: State diagram grammar (`stateDiagram-v2`)
  - TOC:
    - What it does
    - When to use
    - Basic syntax
    - Composite states — nested state machines
    - Choice pseudo-state — conditional branching
    - Concurrency — parallel regions
    - Notes
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-subgraph-grouping.md](./references/TECH-subgraph-grouping.md)**
  - Description: Subgraphs — grouped nodes in flowcharts
  - TOC:
    - What it does
    - When to use
    - Syntax
    - With direction override per subgraph
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-terminal-ascii-wrapper.md](./references/TECH-terminal-ascii-wrapper.md)**
  - Description: Terminal ASCII authoring — Bun-style one-liner
  - TOC:
    - What it does
    - When to use
    - The minimal wrapper
    - Usage patterns
    - The key convention — newlines not semicolons
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-mermaid-diagram/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. `.mmd` Mermaid source files). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-mermaid-diagram-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.
