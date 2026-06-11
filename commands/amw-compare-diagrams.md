---
name: amw-compare-diagrams
description: "Shortcut for users who want a structural IR-level diff between two specific diagrams directly — formats may differ, produces a markdown diff report. An agent in Main-agent mode may also invoke skills/amw-diagram-compare/ directly via the orchestrator, using additional comparison techniques the skill exposes."
---

# /amw-compare-diagrams

Compare two diagram files at the structural (IR) level and produce a markdown diff report. Source formats may differ — comparing an ASCII diagram against its Mermaid equivalent is fully supported.

## Arguments

```
/amw-compare-diagrams <a> <b> [--out <path>] [--format markdown|json]
```

- `<a>` — path to the first diagram (baseline). Required.
- `<b>` — path to the second diagram (modified). Required.
- `--out <path>` — output report path. Default: `./diagram-compare-<timestamp>.md`.
- `--format markdown|json` — report format. Default: `markdown`.

## PNG hard rule

If either `<a>` or `<b>` is PNG (`.png` extension or PNG magic bytes), refuse immediately:

```
PNG is output-only by plugin directive — compare the source artifacts instead.
Provide the ASCII / HTML / SVG / Mermaid source that produced each PNG.
```

Exit 2. Both inputs must be source-format diagrams.

## Dispatch flow

1. Detect format of both inputs via `bin/amw-diagram-detect-format.sh`.
2. Refuse if either is PNG (exit 2).
3. Parse both to IR via `bin/amw-diagram-ir.py parse`.
4. Validate both IRs via `bin/amw-diagram-ir.py validate`.
5. Compute structural diff via `bin/amw-diagram-ir.py diff --a <ir-a> --b <ir-b>`.
6. Render markdown (or JSON) report from the patch ops.
7. Write report to `--out` path.

Full algorithm: [diff-algorithm](../skills/amw-diagram-formats/references/diff-algorithm.md).
> [diff-algorithm.md] Inputs · Output: ordered list of patch ops · Node / edge matching · Deep object equality for `change-*` · Markdown report format · Id normalization (caller preprocessing) · Exit codes (CLI) · Known limitations · Visual mode (optional, future) · Related references

## Report contents

The markdown report includes:

- **Header:** both input paths with detected format, kind, layout, node/edge counts.
- **Summary table:** added / removed / changed counts for nodes and edges.
- **Nodes added** — table: id, label, annotations.
- **Nodes removed** — table: id.
- **Nodes changed** — table: id, field, from, to.
- **Edges added / removed / changed** — same pattern.

If no structural differences: `No structural differences between A and B.`

If formats differ, a note explains that styling changes may be format-conversion artefacts.

## Exit codes

| Exit | Meaning |
|---|---|
| 0 | No structural differences. |
| 1 | Structural differences present — see report. |
| 2 | PNG-as-input refusal or unknown format. |
| 3 | Missing CLI tool — run `/amw-init` / `/amw-doctor`. |
