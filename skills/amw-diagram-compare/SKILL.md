---
name: amw-diagram-compare
description: Structural comparison of two diagrams — diff two flowcharts, compare v1/v2, find what changed, cross-format diagram diff. Triggers on "compare these diagrams", "diff two flowcharts", "what changed between v1 and v2", "structural diff of two diagrams". Source formats may differ (ASCII vs Mermaid is valid). PNG-as-input is refused. Does NOT claim generic design vocabulary — those route to design-principles. Use when comparing two diagrams structurally. Trigger with /amw-compare-diagrams.
version: 0.1.0
---

# Diagram Compare — IR-level structural diff

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Diff algorithm (authoritative):** [diff-algorithm](../amw-diagram-formats/references/diff-algorithm.md).
> [diff-algorithm.md] Inputs · Output: ordered list of patch ops · Node / edge matching · Deep object equality for `change-*` · Markdown report format · Id normalization (caller preprocessing) · Exit codes (CLI) · Known limitations · Visual mode (optional, future) · Related references
> **IR schema (authoritative):** [ir-schema](../amw-diagram-formats/references/ir-schema.md).
> [ir-schema.md] Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Validation · Consumers
> **Conversion matrix (authoritative):** [conversion-matrix](../amw-diagram-formats/references/conversion-matrix.md).
> [conversion-matrix.md] Full N×N table · Cell semantics · PNG-as-source refusal (mandatory) · PNG-as-target pipelines (all supported) · Dispatch algorithm · Per-cell implementation notes · Tools index (required backends) · Related references · ascii · html · svg · mermaid · png
> **Format detection (authoritative):** [detect-format](../amw-diagram-formats/references/detect-format.md).
> [detect-format.md] Contract · Decision tree (precedence top-down) · Content sniff window · Corner cases (by example) · 1 Mermaid-in-markdown · 2 HTML with inline `<svg>` · 3 SVG served as XHTML · 4 ASCII with a Mermaid-looking first line · 5 `.txt` wireframe without box-drawing · 6 PNG with a non-`.png` extension · 7 Empty file · Known limitations · Callers · When to extend this

This skill does not redefine IR or diff semantics — those live once in the shared reference library. The skill's job is to execute the parse → diff → report pipeline and surface findings to the user in a clear markdown report.

## Overview

Structural comparison of two diagrams via IR-level diff. Accepts any two source-format diagrams (ASCII, HTML, SVG, or Mermaid; formats may differ). Parses both to the shared IR, computes an id-based structural patch, and renders a markdown diff report showing added/removed/changed nodes and edges. PNG input is refused — provide source-format artifacts instead.

## Activation

Callable directly via the `/amw-compare-diagrams` command (user shortcut for users who already have two diagram paths and want a structural diff), or invoked by the `design-principles` orchestrator during **Phase B** when a compare task is part of a broader design workflow. An agent in Main-agent mode may also invoke this skill directly via the orchestrator without going through the command.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

ANALYSIS (terminal). Accepts two diagram paths in any supported format (formats may differ). Emits a structured markdown diff report. Does not modify either input. Downstream consumers may use the report to guide edits via `/amw-create-or-modify-*-diagram`.

## Trigger conditions

- "compare these diagrams" / "diff these two diagrams"
- "what changed between v1 and v2 of this diagram"
- "show me the differences between these flowcharts"
- "structural diff of two diagrams"
- "/amw-compare-diagrams \<a\> \<b\>"

Do NOT activate on:
- Converting format (`/amw-convert-any-diagram-format`).
- Validating a single diagram (`/amw-validate-any-diagram-format`).
- Creating or editing diagrams (`wd-create-or-modify-*`).

## PNG hard rule

**PNG is OUTPUT-ONLY by plugin directive.** If either input `a` or `b` is PNG (`.png` extension or PNG magic bytes `\x89PNG\r\n\x1a\n`), refuse immediately:

```
PNG is output-only by plugin directive — compare the source artifacts instead.
Provide the ASCII / HTML / SVG / Mermaid source that produced each PNG.
```

Exit 2. Both inputs must be source-format diagrams for comparison to proceed.

## Instructions

1. Detect the format of each input with `bin/amw-diagram-detect-format.sh`; refuse immediately if either input is PNG.
2. Parse both inputs to IR using `bin/amw-diagram-ir.py parse`; cross-format comparison is fully supported via IR normalization.
3. Validate both IR documents with `bin/amw-diagram-ir.py validate`; abort on dangling edges or schema errors.
4. Compute the structural diff with `bin/amw-diagram-ir.py diff`; the diff focuses on semantic changes (nodes, edges, labels), not cosmetic styling.
5. Format the diff report as a Markdown summary (added/removed/moved nodes and edges); present to the user before overwriting anything.
6. Save the diff report and both IR files to `/tmp/` with a content-addressed hash in the filename.

## Comparison pipeline (6 steps)

### Step 1 — Detect format of each input

```bash
fmt_a=$(bin/amw-diagram-detect-format.sh "$A_PATH")
fmt_b=$(bin/amw-diagram-detect-format.sh "$B_PATH")
```

If `fmt_a == "png"` or `fmt_b == "png"` → emit the PNG refusal message and stop.

If either is `unknown` → ask the user to clarify the format of the unrecognized file.

Cross-format comparison is fully supported — an ASCII file vs a Mermaid file is valid. The IR normalization in Steps 2 and 3 bridges the formats.

### Step 2 — Parse both to IR

```bash
bin/amw-diagram-ir.py parse --in "$A_PATH" --out "/tmp/${HASH}-a.ir.json"
bin/amw-diagram-ir.py parse --in "$B_PATH" --out "/tmp/${HASH}-b.ir.json"
```

Both parsers must succeed. Per-format parsers:

| Format | Backend |
|---|---|
| ASCII | `bin/amw-ascii-parse.py` (internal to `bin/amw-diagram-ir.py`) |
| HTML | `bin/amw-parse-html-diagram.py` (Phase 1 Task 1a) |
| SVG | `bin/amw-parse-svg-diagram.py` (Phase 1 Task 1b) |
| Mermaid | `bin/amw-parse-mermaid-diagram.py` (Phase 1 Task 1c) |

**Cross-format comparison and IR fidelity:** when comparing across formats, the IR normalizes structural content (nodes, edges, kinds, labels) but drops format-specific styling (CSS classes, SVG filters, ASCII box decoration). This is intentional — the diff focuses on **semantic changes**, not cosmetic ones. See [ir-schema](../amw-diagram-formats/references/ir-schema.md) §5 for the per-format lossy-conversion table.

### Step 3 — Validate both IRs

```bash
bin/amw-diagram-ir.py validate --in "/tmp/${HASH}-a.ir.json"
bin/amw-diagram-ir.py validate --in "/tmp/${HASH}-b.ir.json"
```

Dangling edges, missing required fields, or wrong IR version abort the diff before any comparison.

### Step 4 — Compute structural diff

```bash
bin/amw-diagram-ir.py diff --a "/tmp/${HASH}-a.ir.json" --b "/tmp/${HASH}-b.ir.json" \
  --out "/tmp/${HASH}-patch.json"
```

The diff algorithm is **id-based**: nodes and edges match by their `id` field. See [diff-algorithm](../amw-diagram-formats/references/diff-algorithm.md) §3 for matching semantics, §6 for id normalization if the two inputs use different id schemes.

Patch op types (JSON list in `--out`):
`change-kind`, `change-layout`, `add-node`, `remove-node`, `change-node`, `add-edge`, `remove-edge`, `change-edge`.

### Step 5 — Render markdown report

Convert the JSON patch to the canonical markdown layout from [diff-algorithm](../amw-diagram-formats/references/diff-algorithm.md) §5:

```markdown
# Diagram comparison

- **A:** `<path-a>` (source_format=<fmt>, kind=<kind>, layout=<layout>, N nodes, M edges)
- **B:** `<path-b>` (source_format=<fmt>, kind=<kind>, layout=<layout>, N nodes, M edges)

## Summary
...

## Nodes added
...

## Nodes removed
...

## Nodes changed
...

## Edges added / Edges removed / Edges changed
...
```

Color coding (markdown annotations; visual only when rendered):
- Added nodes/edges → note as `+`
- Removed nodes/edges → note as `-`
- Changed label → note field as `~label`
- Changed style → note as `~style`

If the patch is empty → single line: `No structural differences between A and B.`

### Step 6 — Write report to output path

Default output path: `<cwd>/diagram-compare-<timestamp>.md` (or `--out <path>` override). Timestamp format: `$(date +%Y%m%d_%H%M%S%z)`.

Report includes:
1. The two input paths and their detected formats.
2. The summary table (added / removed / changed counts per category).
3. Sections for each op type with full node/edge details.
4. A note on cross-format lossy comparison if formats differ (with a link to [ir-schema](../amw-diagram-formats/references/ir-schema.md) §5).
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers

## Cross-format comparison: lossy-conversion impact

When A and B are in different formats, both are parsed to the same IR — but the IR is lossy. Example: comparing an ASCII diagram (`a.txt`) against its HTML rendering (`a.html`). The HTML version drops ASCII box characters; the ASCII version drops CSS styling. The diff will report changes in `style.*` fields that are actually just format-conversion artefacts, not semantic edits. The skill warns the user when formats differ:

> "Note: A (`ascii`) and B (`html`) use different source formats. Styling differences may reflect format-conversion artefacts rather than intentional edits. Structure (nodes, edges, labels) is format-agnostic."

## Error Handling

| Symptom | Cause | Resolution |
|---|---|---|
| Either input is PNG | User supplied PNG instead of source artifact | Emit refusal message; ask for the source diagram |
| `bin/amw-diagram-ir.py parse` fails for one input | Unsupported or empty diagram structure | Surface the error; recommend `/amw-validate-any-diagram-format` on the failing input first |
| Both IRs parse but diff exits 2 | IR validation failure (dangling edge, bad version) | Surface `bin/amw-diagram-ir.py validate` output; the source diagram may need repair |
| Patch reports many spurious `change-node` ops | Different id schemes across formats (e.g. ASCII → `n1/n2` vs Mermaid → user names) | Apply label-based id normalization per [diff-algorithm](../amw-diagram-formats/references/diff-algorithm.md) §6; re-diff |
| Report file already exists at `--out` path | Prior compare run | Overwrite with new timestamp in filename; the old file is preserved in `/tmp/` |

## Output

Produces a markdown diff report at the output path (default: `<cwd>/diagram-compare-<timestamp>.md`). The report lists the two input paths and their detected formats, a summary table (added/removed/changed counts), and sections for each op type. Written by Step 6 of the comparison pipeline.

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Prerequisites

```yaml
runtime_binaries:
  - python3 >= 3.8   # bin/amw-diagram-ir.py, bin/amw-ascii-parse.py
  - lxml             # bin/amw-parse-html-diagram.py (Phase 1 Task 1a)

python_packages:
  - lxml   # HTML parsing

installed_via_wd_init: [python3]
checked_by_wd_doctor:  [python3]
```

No new bin scripts needed — `bin/amw-diagram-ir.py diff` is the implementation.

## Resources

- [diff-algorithm](../amw-diagram-formats/references/diff-algorithm.md) — authoritative IR diff spec, patch op format, markdown report layout.
  > Inputs · Output: ordered list of patch ops · Node / edge matching · Deep object equality for `change-*` · Markdown report format · Id normalization (caller preprocessing) · Exit codes (CLI) · Known limitations · Visual mode (optional, future) · Related references
- [ir-schema](../amw-diagram-formats/references/ir-schema.md) — IR shape and lossy-conversion table.
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
- [detect-format](../amw-diagram-formats/references/detect-format.md) — format sniffer spec.
  > Contract · Decision tree (precedence top-down) · Content sniff window · Corner cases (by example) · 1 Mermaid-in-markdown · 2 HTML with inline `<svg>` · 3 SVG served as XHTML · 4 ASCII with a Mermaid-looking first line · 5 `.txt` wireframe without box-drawing · 6 PNG with a non-`.png` extension · 7 Empty file · Known limitations · Callers · When to extend this
- [conversion-matrix](../amw-diagram-formats/references/conversion-matrix.md) — cross-format parse paths (Steps 2–3 use this).
  > Full N×N table · Cell semantics · PNG-as-source refusal (mandatory) · PNG-as-target pipelines (all supported) · Dispatch algorithm · Per-cell implementation notes · Tools index (required backends) · Related references · ascii · html · svg · mermaid · png
- [modify-flow](../amw-diagram-formats/references/modify-flow.md) — diff is a read-only sibling of the modify pipeline (shares Steps 1+2).
  > The pipeline · Create vs modify dispatch · Step-by-step detail · Step 1 — Detect · Step 2 — Parse to IR · Step 3 — Patch · Step 4 — (loop point) · Step 5 — Emit · Step 6 — Re-validate · Work directory and file naming · Per-format guidance · 1 ASCII modify (MVP structural) · 2 HTML modify (MVP raw-source; Phase 1 structural) · 3 SVG modify (MVP raw-source; Phase 1 structural) · 4 Mermaid modify (MVP raw-source; Phase 1 structural) · Conversion is a modify-flow variant · Composition with round-trip skills · 1 `diagram-webpage-sync` (`/amw-modify-webpage-from-diagram`) · 2 `webpage-to-diagram` (`/amw-modify-diagram-of-webpage`) · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
- [SKILL](../amw-diagram-convert/SKILL.md) — when comparing cross-format, both inputs go through IR parse (same pipeline entry).
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.
- `/amw-compare-diagrams` — user-facing slash command.
