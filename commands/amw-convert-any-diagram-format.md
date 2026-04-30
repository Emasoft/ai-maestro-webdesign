---
name: amw-convert-any-diagram-format
description: "Shortcut for users who want to convert a specific diagram between formats directly — auto-detects source, targets ASCII/HTML/SVG/Mermaid/PNG. An agent in Main-agent mode may also invoke skills/amw-diagram-convert/ directly via the orchestrator, applying the full N×N conversion matrix and format-specific techniques the skill exposes."
---

# /amw-convert-any-diagram-format

Convert any supported diagram to a different format using the canonical N×N conversion matrix.

## Arguments

```
/amw-convert-any-diagram-format <source> [--to <target>] [--out <path>]
```

- `<source>` — path to the source diagram file. Required.
- `--to <target>` — target format: `ascii`, `html`, `svg`, `mermaid`, `png`. If omitted, ask the user.
- `--out <path>` — output file path. Default: `<source-basename>.<target-ext>` in the same directory.

## Supported format pairs

| From \ To | ascii | html | svg | mermaid | png |
|---|---|---|---|---|---|
| **ascii** | — | direct | direct | via IR | direct |
| **html** | via IR | — | direct | via IR | direct |
| **svg** | via IR | wrap | — | via IR | direct |
| **mermaid** | direct | via SVG | direct | — | direct |
| **PNG** | **REFUSED** | **REFUSED** | **REFUSED** | **REFUSED** | — |

Full routing rules: `skills/amw-diagram-formats/references/conversion-matrix.md`.

## PNG hard rule

PNG is **output-only** by plugin directive. If `<source>` is a PNG (`.png` extension or PNG magic bytes), refuse immediately:

```
PNG is output-only by plugin directive — re-authoring required from source artifact.
Provide the ASCII / HTML / SVG / Mermaid source instead.
```

Exit 2. No OCR, no best-effort workaround.

## Dispatch logic

1. Run `bin/amw-diagram-detect-format.sh <source>` → `src_fmt`.
2. If `src_fmt == "png"` → emit refusal above, exit 2.
3. If `--to` not supplied → ask: *"Which target format? ascii / html / svg / mermaid / png"*
4. If `src_fmt == target_fmt` → copy identity, nothing to do.
5. Look up `(src_fmt, target_fmt)` in the conversion matrix.
6. Execute the dispatch (direct one-step, via IR two-step, via SVG chain, or wrap).
7. Run `bin/amw-validate-diagram.sh <out>`. If FAIL → abort, leave source untouched, surface FIX hints.
8. Report the output path and validation result.

## Output

- One file at the output path.
- Intermediate files (for multi-step conversions) written to `/tmp/amw-convert-<hash>-step-N.<ext>` and listed in the response so the user can inspect.
- Validation result: `PASS: <path>` or `FAIL: ...` lines with `FIX:` hints.

## Failure exits

| Exit | Meaning |
|---|---|
| 0 | Conversion succeeded, target validates. |
| 1 | Conversion produced output but validation FAIL. |
| 2 | PNG-as-source refusal, or unknown source format. |
| 3 | Missing CLI dependency — run `/amw-init` / `/amw-doctor`. |
