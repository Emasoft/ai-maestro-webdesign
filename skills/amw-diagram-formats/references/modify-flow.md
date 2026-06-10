# Modify flow — shared pipeline for create-or-modify commands

## Table of Contents

- [1. The pipeline](#1-the-pipeline)
- [2. Create vs modify dispatch](#2-create-vs-modify-dispatch)
- [3. Step-by-step detail](#3-step-by-step-detail)
- [4. Work directory and file naming](#4-work-directory-and-file-naming)
- [5. Per-format guidance](#5-per-format-guidance)
- [6. Conversion is a modify-flow variant](#6-conversion-is-a-modify-flow-variant)
- [7. Composition with round-trip skills](#7-composition-with-round-trip-skills)
- [8. Related references](#8-related-references)

## Overview

**Authoritative spec for the "modify" path** used by all 4 `wd-create-or-modify-*-diagram` commands:

- `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator`
- `/amw-create-or-modify-html-diagram` → backed by `html-diagram`
- `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram`
- `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram`

And by the round-trip skills:

- `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram`
- `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`

All of them share the same 6-step pipeline below. They DO NOT re-implement these steps locally — they reference this file.

## 1. The pipeline

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  1. DETECT    │ ──► │  2. PARSE     │ ──► │  3. PATCH     │
│     format    │     │     to IR     │     │     IR        │
└───────────────┘     └───────────────┘     └───────────────┘
                                                    │
┌───────────────┐     ┌───────────────┐             │
│  6. RE-VALIDATE│ ◄─ │  5. EMIT      │ ◄───────────┘
│     output    │     │     new file  │
└───────────────┘     └───────────────┘
       │                     ▲
       │  (if FAIL)          │
       └──── 4. re-patch ────┘
```

Steps:

1. **Detect** the source format.
2. **Parse** the source to IR.
3. **Patch** the IR with the user-requested changes.
4. (Loop point — re-patch on validation failure.)
5. **Emit** the IR back to the original format (or to a new target format — conversion is a modify-flow with an empty patch).
6. **Re-validate** the emitted file.

If step 6 FAILs, re-patch (step 4, which loops back into step 3) and re-emit. Termination: PASS or a retry budget (default 3).

## 2. Create vs modify dispatch

Every `wd-create-or-modify-*-diagram` command accepts either a brief (creation) or a path (modification). The dispatch rule:

```
If $ARGUMENTS is a path AND the path exists AND bin/amw-diagram-detect-format.sh says it's a diagram:
    modify flow (6 steps below)
Else:
    create flow (skill-specific — see the skill's SKILL.md)
```

Each per-format skill also publishes its own dispatch specifics in the command `.md` file — e.g. "ASCII creation uses the ascii-creator 2-mode pipeline" vs "ASCII modification uses this shared modify-flow".

## 3. Step-by-step detail

### Step 1 — Detect

```bash
fmt="$(bin/amw-diagram-detect-format.sh "$INPUT_PATH")"
```

See [detect-format](./detect-format.md). If `fmt == "png"`, abort with the standard PNG refusal. If `fmt == "unknown"`, ask the user to disambiguate via `--format`.
> [detect-format.md] Contract · Decision tree (precedence top-down) · Content sniff window · Corner cases (by example) · 1 Mermaid-in-markdown · 2 HTML with inline `<svg>` · 3 SVG served as XHTML · 4 ASCII with a Mermaid-looking first line · 5 `.txt` wireframe without box-drawing · 6 PNG with a non-`.png` extension · 7 Empty file · Known limitations · Callers · When to extend this

### Step 2 — Parse to IR

```bash
bin/amw-diagram-ir.py parse --in "$INPUT_PATH" --out "$WORK_DIR/ir.json"
```

MVP: only ASCII parses to a structural IR. HTML / SVG / Mermaid parse to a **raw-source stub** (see [ir-schema](./ir-schema.md) §4). Phase 1 replaces these stubs with native parsers; the modify-flow does not change.
> [ir-schema.md] Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Validation · Consumers

The IR is validated immediately after parsing:

```bash
bin/amw-diagram-ir.py validate --in "$WORK_DIR/ir.json"
```

A failed validation here is a parser bug, not a user error — the modify flow aborts with an internal error and the user is asked to file an issue.

### Step 3 — Patch

Patching is the one step the caller OWNS. The per-format skill / command decides HOW to apply the user's requested change to the IR. Patterns the caller may use:

| Pattern | When | Example |
|---|---|---|
| **Direct edit** | Known node/edge IDs | User: "rename the 'Login' node to 'Auth'". Caller: find node by label, mutate `.label`. |
| **Add / remove** | New graph elements | User: "add a /logout edge from dashboard to home". Caller: push onto `edges`. |
| **Re-rank / re-layout** | Structural moves | User: "make this horizontal instead of vertical". Caller: flip `layout`, recompute ranks. |
| **Raw-source substitution** | Freeform IR (raw-source) | User: "change the CTA copy". Caller: find-and-replace inside `nodes[0].label`. |

For the MVP raw-source case, patching is essentially text editing on `nodes[0].label`. When Phase 1 lands structural parsers, the same commands pick up real structural editing without a flow change.

### Step 4 — (loop point)

Re-enter step 3 with the same IR if validation (step 6) failed. The command decides whether to retry automatically (apply a `FIX: ...` hint from the validator) or whether to surface the FAIL to the user and ask them to refine their request.

Budget: 3 attempts. After 3 consecutive FAILs, surface the validator findings and stop the loop. The user can invoke again with adjustments.

### Step 5 — Emit

```bash
bin/amw-diagram-ir.py emit --in "$WORK_DIR/ir.json" --format "$TARGET_FMT" --out "$OUTPUT_PATH"
```

`$TARGET_FMT` is usually the same as `$fmt` (in-place modify) but may differ when the modify-flow is reused for conversion (conversion = modify-flow with an empty patch + different target).

Emitters respect the raw-source fast path: if the IR is a single freeform node with `annotations: ["raw-source"]` and the target format matches `source_format`, the output is the label verbatim — byte-perfect round-trip for files that weren't structurally parsed.

### Step 6 — Re-validate

```bash
bin/amw-validate-diagram.sh "$OUTPUT_PATH"
```

Exit 0 → done; print `PASS` line + output path. Exit 1 → feed findings back into step 3. Exit 2 / 3 → hard fail.

## 4. Work directory and file naming

```
$WORK_DIR = /tmp/amw-modify-$HASH  (unique per invocation)
  ├── ir.json               (the parsed IR)
  ├── ir.patched.json       (after step 3; may be overwritten by loop)
  └── <basename>.<ext>.new  (step 5 output; atomically moved to $OUTPUT_PATH on PASS)
```

The "atomic move on PASS" rule prevents partial outputs: a failed validate leaves the original `$OUTPUT_PATH` untouched. Callers that need pre-modify backups should write `$OUTPUT_PATH.bak` BEFORE step 5.

## 5. Per-format guidance

### 5.1 ASCII modify (MVP structural)

- Parse uses `bin/amw-ascii-parse.py` → structured boxes+connectors → IR (see `../../bin/amw-diagram-ir.py::parse_ascii`).
- Patch: direct edits on `nodes[*].label`, `edges[*]`.
- Emit uses `bin/amw-ascii-render.py` (if structure is usable) OR falls back to raw-source passthrough.
- Validate: `bin/amw-validate-ascii.py` (or `.py` on Windows).

Known limitation: not every hand-authored ASCII wireframe has clean boxes + connectors that `ascii-parse.py` can extract. When extraction yields zero boxes, parse falls through to raw-source stub; patching in that case is text editing only (no structural operations available until Phase 1).

### 5.2 HTML modify (MVP raw-source; Phase 1 structural)

- Parse: raw-source stub (MVP). Phase 1 (`bin/amw-parse-html-diagram.py`) extracts inline SVG and DOM structure.
- Patch: text substitution inside `nodes[0].label` for MVP. Structural patching once Phase 1 lands.
- Emit: for MVP, label verbatim. Phase 1 emits via design-principles starter-components.
- Validate: `bin/amw-validate-html-diagram.sh` (xmllint --html + tidy).

### 5.3 SVG modify (MVP raw-source; Phase 1 structural)

- Parse: raw-source stub. Phase 1 (`bin/amw-parse-svg-diagram.py`) does geometric interpretation (rects → nodes, lines/paths+markers → edges).
- Patch: text substitution for MVP. Structural once Phase 1.
- Emit: raw-source passthrough for MVP; minimal SVG for structured IRs.
- Validate: `bin/amw-validate-svg-diagram.sh` (xmllint --noout + namespace check).

### 5.4 Mermaid modify (MVP raw-source; Phase 1 structural)

- Parse: raw-source stub. Phase 1 (`bin/amw-parse-mermaid-diagram.py`) parses Mermaid grammars (flowchart / sequence / state / class / ER).
- Patch: text substitution for MVP. Grammar-aware once Phase 1.
- Emit: raw-source passthrough for MVP; Phase 1 produces per-kind Mermaid grammars.
- Validate: `bin/amw-mermaid-lint.sh` (mmdc dry-render).

## 6. Conversion is a modify-flow variant

`/amw-convert-any-diagram-format` is a modify-flow with an **empty patch** (step 3 is a no-op) and a different target format (step 5 emits to `$TARGET`, not `$SOURCE_FMT`). See [conversion-matrix](./conversion-matrix.md) for the cell-by-cell dispatch, but the 6-step pipeline is identical.

This means improvements to the modify-flow (better parsers, stricter validation) automatically benefit every cross-format conversion.

## 7. Composition with round-trip skills

### 7.1 `diagram-webpage-sync` (`/amw-modify-webpage-from-diagram`)

Two modify-flows back-to-back:

```
1. diagram-modify-flow on the DIAGRAM source
2. ascii-to-html OR conversion via IR -> HTML
3. html-modify-flow on the existing HTML (merge changes vs regenerate)
```

Step 3 is the interesting one — it's a 3-way merge (original HTML, regenerated HTML, user's post-gen HTML edits). MVP: overwrite + `.bak`. Phase 2: diff-match-patch-based merge.

### 7.2 `webpage-to-diagram` (`/amw-modify-diagram-of-webpage`)

Two modify-flows in reverse:

```
1. DOM -> IR extraction (via bin/amw-dom-to-ir.py)
2. diagram-modify-flow on the extracted IR
3. IR -> DOM patch (via bin/amw-ir-to-dom-patch.py) OR user edits the diagram manually
```

Phase 0 / 1: MVP extract only (step 1). Phase 2 adds step 3 (selector-aware sync-back).

## 8. Related references

- [ir-schema](./ir-schema.md) — what the IR looks like (step 2 output shape).
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
- [conversion-matrix](./conversion-matrix.md) — step 5 target-format table.
  > Full N×N table · Cell semantics · PNG-as-source refusal (mandatory) · PNG-as-target pipelines (all supported) · Dispatch algorithm · Per-cell implementation notes · Tools index (required backends) · Related references · ascii · html · svg · mermaid · png
- [detect-format](./detect-format.md) — step 1 decision tree.
  > Contract · Decision tree (precedence top-down) · Content sniff window · Corner cases (by example) · 1 Mermaid-in-markdown · 2 HTML with inline `<svg>` · 3 SVG served as XHTML · 4 ASCII with a Mermaid-looking first line · 5 `.txt` wireframe without box-drawing · 6 PNG with a non-`.png` extension · 7 Empty file · Known limitations · Callers · When to extend this
- [validation-dispatcher](./validation-dispatcher.md) — step 6 contract.
  > Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · 1 ASCII — `bin/amw-validate-ascii.py` (primary) and `bin/amw-validate-ascii.py` (fallback) · 2 SVG — `bin/amw-validate-svg-diagram.sh` · 3 HTML — `bin/amw-validate-html-diagram.sh` · 4 Mermaid — `bin/amw-mermaid-lint.sh` · Caller integration patterns · 1 Post-create gate · 2 Post-convert gate · 3 Modify-flow loop · 4 Multi-format mode (ascii-validator) · Known limitations (Phase 0) · Related references
- [diff-algorithm](./diff-algorithm.md) — consumed by `/amw-compare-diagrams`, which is a related but NON-modify pipeline (it does steps 1+2 on two inputs and then diffs the IRs).
  > Inputs · Output: ordered list of patch ops · Node / edge matching · Deep object equality for `change-*` · Markdown report format · Id normalization (caller preprocessing) · Exit codes (CLI) · Known limitations · Visual mode (optional, future) · Related references
