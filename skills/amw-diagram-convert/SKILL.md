---
name: amw-diagram-convert
description: Cross-format diagram conversion — convert a diagram from one format to another across the 5-format matrix (ASCII, HTML, SVG, Mermaid, PNG). Triggers on "convert this diagram to X", "turn my ASCII into SVG", "convert flowchart to mermaid", "export diagram as PNG". PNG-as-source is refused. Does NOT claim generic design vocabulary — those route to design-principles. Use when converting a diagram across the 5-format matrix. Trigger with /amw-convert-any-diagram-format.
version: 0.1.0
---

# Diagram Convert — cross-format dispatcher

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Authoritative references** (read each when its content is needed):
> - [conversion-matrix](../amw-diagram-formats/references/conversion-matrix.md) — N×N dispatch table.
> - [detect-format](../amw-diagram-formats/references/detect-format.md) — format sniffer spec.
> - [ir-schema](../amw-diagram-formats/references/ir-schema.md) — IR shape + lossy-conversion table.
> - [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md) — unified PASS/FAIL contract.

This skill does not redefine format semantics — every conversion rule lives once in [conversion-matrix](../amw-diagram-formats/references/conversion-matrix.md). The skill's job is to execute the dispatch algorithm and run the post-conversion validation gate.

## Overview

Cross-format diagram conversion across the full 5-format matrix (ASCII, HTML, SVG, Mermaid, PNG). Accepts a source diagram file in any supported format and emits a converted file in the requested target format via a 6-step pipeline: detect → parse to IR → (optional IR ops) → emit → validate → write. PNG as source is refused by plugin directive; PNG is a valid target from any other format.

## Activation

Callable directly via the `/amw-convert-any-diagram-format` command (user shortcut for users who have a diagram file and want to convert it to another format), or invoked by the `design-principles` orchestrator during **Phase B** as part of a broader create/convert workflow. An agent in Main-agent mode may also invoke this skill directly via the orchestrator without going through the command.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

TRANSFORM (terminal). Accepts one diagram file in any supported format and emits one file in the requested target format. Downstream of every `wd-create-or-modify-*-diagram` command (which may normalize an incoming diagram via this skill) and upstream of `/amw-preview` or further editing.

## Trigger conditions

- "convert this diagram to \<format\>" / "convert this \<format\> to \<other-format\>"
- "turn my ASCII into SVG" / "turn my SVG into ASCII"
- "cross-format diagram conversion"
- "export this diagram as PNG"
- "transform my mermaid to HTML"
- "change the format of this diagram"
- "/amw-convert-any-diagram-format \<source\> --to \<target\>"

Do NOT activate on:
- Generic "design a landing page" or "build a diagram" — use `../amw-design-principles/`.
- Validating-only requests — use `/amw-validate-any-diagram-format`.
- Comparing two diagrams — use [SKILL](../amw-diagram-compare/SKILL.md).

## PNG hard rule

**PNG is OUTPUT-ONLY by plugin directive.** Any PNG-as-source input triggers an immediate refusal:

```
PNG is output-only by plugin directive — re-authoring required from source artifact.
Provide the ASCII / HTML / SVG / Mermaid source instead.
```

Detection uses both PNG magic bytes (`\x89PNG\r\n\x1a\n`) and `.png` extension — either alone triggers refusal. No OCR fallback, no best-effort reinterpretation. Exit 2.

PNG remains a valid TARGET for every other source format (see §PNG-as-target below).

## Instructions

1. Detect the source format with `bin/amw-diagram-detect-format.sh`; refuse immediately if source is PNG (PNG is output-only).
2. For conversions labeled "via IR" in the conversion matrix: parse the source to IR with `bin/amw-diagram-ir.py parse`; for "direct" cells, skip this step.
3. Optionally apply IR-level mutations (label renames, structural edits) before emission if the caller requests a normalize-then-edit workflow.
4. Emit to the target format using the dispatch table in [conversion-matrix](../amw-diagram-formats/references/conversion-matrix.md); for two-step paths chain two conversions.
5. Validate the output with `bin/amw-validate-diagram.sh`; a FAIL aborts the skill and surfaces FIX hints verbatim.
6. Save the output artifact and report the file path; document the conversion path taken.

## Conversion pipeline (6 steps)

### Step 1 — Detect source format

```bash
src_fmt=$(bin/amw-diagram-detect-format.sh "$SOURCE_PATH")
```

Decision tree: see [detect-format](../amw-diagram-formats/references/detect-format.md) §2. Returns one of `ascii|html|svg|mermaid|png|unknown`. If `unknown`, ask the user to clarify the source format.

If `src_fmt == "png"` → emit refusal message above and stop.

### Step 2 — Parse to IR (when needed)

For cells labeled "via IR" in the conversion matrix:

```bash
bin/amw-diagram-ir.py parse --in "$SOURCE_PATH" --out "/tmp/${HASH}.ir.json"
```

- ASCII source → uses `bin/amw-ascii-parse.py` internally.
- HTML source → uses `bin/amw-parse-html-diagram.py` (Phase 1, Task 1a).
- SVG source → uses `bin/amw-parse-svg-diagram.py` (Phase 1, Task 1b).
- Mermaid source → uses `bin/amw-parse-mermaid-diagram.py` (Phase 1, Task 1c).

For "direct" cells, this step is skipped — the named single-step tool handles both parse and emit.

### Step 3 — (Optional) IR-level operations

For format-normalize-then-edit workflows, callers may mutate the IR at this step before emission. Default conversion skips this — the IR is emitted as-is.

### Step 4 — Emit to target format

Dispatch per the matrix cell `(src_fmt, target_fmt)`:

| Cell type | Action |
|---|---|
| `direct` | Run the named one-step tool (see matrix §1). |
| `via IR` | `bin/amw-diagram-ir.py emit --in /tmp/${HASH}.ir.json --format <target> --out <OUT_PATH>` |
| `via X` (two-step) | Convert(src, X) → tmp; convert(tmp, target) → out. Both steps are "direct" or "via IR". |
| `wrap` | SVG → HTML: wrap SVG in `<!DOCTYPE html><html><body>{svg}</body></html>`. One-step, no IR. |
| `impossible` | PNG-as-source — already refused at Step 1. |

The full matrix with per-cell justifications lives at [conversion-matrix](../amw-diagram-formats/references/conversion-matrix.md). This skill does NOT redefine it.

### Step 5 — Validate output

```bash
bin/amw-validate-diagram.sh "$OUT_PATH"
```

Unified PASS/FAIL contract per [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md). If FAIL, the conversion is aborted and the original source file is left untouched. Surface the FAIL lines and their `FIX:` hints to the user. Do NOT silently deliver an invalid output.

### Step 6 — Write to output path

Default output path: `<source-basename>.<target-ext>` in the same directory as the source. Accept an explicit `--out <path>` override.

Log each intermediate file created during multi-step conversions so the user can inspect them. Intermediate files are written to `/tmp/amw-convert-<HASH>-step-N.<ext>`.

## Routing summary

Full table in [conversion-matrix](../amw-diagram-formats/references/conversion-matrix.md) §1. PNG as source is **impossible** (refused at Step 1); PNG as target is supported from all four other formats. Other cells are either `direct` (single-step backend tool) or `via IR` (parse → emit through `bin/amw-diagram-ir.py`). See [png](../amw-diagram-formats/references/png.md) for DPI / background / padding options.

## Error Handling

| Symptom | Cause | Resolution |
|---|---|---|
| `bin/amw-diagram-detect-format.sh` returns `unknown` | File has no decisive extension and no recognized content signature | Ask user to specify format explicitly with `--from <fmt>` |
| Validation FAIL after conversion | Target format has structural errors (e.g. IR→ASCII produced misaligned boxes) | Surface all `FIX:` hints; do NOT deliver the invalid output; offer to retry |
| IR parse returns empty nodes | Source diagram has no detectable graph structure (e.g. HTML page with no `<svg>`) | Warn user; offer the raw-source stub per [modify-flow](../amw-diagram-formats/references/modify-flow.md) §5.2 |
| PNG-as-source input detected | User mistakenly provided a `.png` instead of a source artifact | Emit the fixed refusal message verbatim and stop |
| `cairosvg` missing for SVG→PNG | Dependency not installed | `exit 3`; direct user to `/amw-init` / `/amw-doctor` |
| `playwright` missing for HTML→PNG | Dependency not installed | `exit 3`; direct user to `/amw-init` / `/amw-doctor` |

## Output

Produces one converted diagram file at the output path (default: `<source-basename>.<target-ext>` in the same directory as the source). Intermediate files for multi-step conversions are written to `/tmp/amw-convert-<HASH>-step-N.<ext>`.

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Prerequisites

```yaml
runtime_binaries:
  - python3 >= 3.8   # bin/amw-diagram-ir.py, bin/amw-ascii-parse.py, bin/amw-ascii-render.py
  - perl >= 5.10     # bin/amw-validate-ascii.py (post-convert gate for ASCII targets)
  - xmllint          # bin/amw-validate-svg-diagram.sh, bin/amw-validate-html-diagram.sh
  - mmdc             # bin/amw-mermaid-render.sh, mermaid-lint.sh (Mermaid targets)
  - cairosvg         # bin/amw-svg-render.py --png (SVG→PNG and ASCII→PNG)
  - playwright       # bin/amw-html-export.py (HTML→PNG)

python_packages:
  - cairosvg   # for bin/amw-svg-render.py --png
  - lxml       # for bin/amw-parse-html-diagram.py (Phase 1)

installed_via_wd_init: [xmllint, mmdc, playwright, cairosvg]
checked_by_wd_doctor:  [xmllint, mmdc, playwright, cairosvg, python3, perl]
```

## Resources

- [conversion-matrix](../amw-diagram-formats/references/conversion-matrix.md) — N×N conversion dispatch table.
- [detect-format](../amw-diagram-formats/references/detect-format.md) — format sniffer spec.
- [ir-schema](../amw-diagram-formats/references/ir-schema.md) — IR JSON schema + lossy table.
- [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md) — unified PASS/FAIL contract.
- [png](../amw-diagram-formats/references/png.md) — PNG rasterization pipeline options.
- [modify-flow](../amw-diagram-formats/references/modify-flow.md) — conversion is a degenerate modify-flow.
- [amw-ascii-to-html](../amw-ascii-to-html/SKILL.md) — ASCII → HTML direct producer.
- [amw-ascii-to-svg](../amw-ascii-to-svg/SKILL.md) — ASCII → SVG direct producer.
- [amw-mermaid-render](../amw-mermaid-render/SKILL.md) — Mermaid → SVG / ASCII / PNG renderer.
- [amw-ascii-validator](../amw-ascii-validator/SKILL.md) — ASCII validation gate.
- [amw-design-principles](../amw-design-principles/SKILL.md) — orchestrator.
- `/amw-convert-any-diagram-format` — user-facing slash command.
