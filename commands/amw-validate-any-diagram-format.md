---
name: amw-validate-any-diagram-format
description: "Shortcut for users who want to validate a specific diagram file against its format rules directly — auto-detects ASCII/HTML/SVG/Mermaid, reports PASS/FAIL with FIX hints. An agent in Main-agent mode may also invoke the format-specific validators (bin/amw-validate-ascii.py, bin/amw-validate-svg-diagram.sh, bin/amw-mermaid-lint.sh) directly as part of Phase B artifact validation."
---

# /amw-validate-any-diagram-format

Validate any supported diagram file. Auto-sniffs format and routes to the appropriate per-format validator. Never rewrites the file — read-only diagnostic tool.

## Arguments

```
/amw-validate-any-diagram-format <path>
```

- `<path>` — path to the diagram file. Required.

## What it does

1. Detects format via `bin/amw-diagram-detect-format.sh <path>` → one of `ascii|html|svg|mermaid|png|unknown`.
2. Dispatches to `bin/amw-validate-diagram.sh <path>`, which routes internally:
   - **ascii** → `bin/amw-validate-ascii.py` (Python)
   - **svg** → `bin/amw-validate-svg-diagram.sh` (xmllint + namespace check)
   - **html** → `bin/amw-validate-html-diagram.sh` (xmllint --html + tidy if available)
   - **mermaid** → `bin/amw-mermaid-lint.sh` (mmdc dry-run)
   - **png** → immediate refusal (exit 2)
   - **unknown** → exit 2 with `UNKNOWN:` message
3. Reports the unified output: PASS count and/or FAIL lines with line numbers and `FIX:` hints.

Full routing spec: `skills/amw-diagram-formats/references/validation-dispatcher.md`.

## PNG hard rule

PNG validation is refused per plugin directive:

```
REFUSE: PNG is output-only by plugin directive; validate the source artifact instead.
        Provide the ASCII / HTML / SVG / Mermaid source that produced this PNG.
```

Exit 2. Validate the source artifact that produced the PNG, not the PNG itself.

## Output format

On PASS:

```
PASS: <path>
```

On FAIL (one line per finding):

```
FAIL: <line>: <message> [FIX: <hint>]
FAIL: <line>: <message> [FIX: <hint>]
...
<N> issue(s) found in <path>
```

The command surfaces the **first 10 findings** inline; if more than 10 are present, it notes "… and N more — see full output above". Every finding includes a `FIX:` hint pointing at the exact repair needed.

## Exit codes

| Exit | Meaning |
|---|---|
| 0 | PASS — no issues found. |
| 1 | FAIL — one or more findings. Apply `FIX:` hints and re-run. |
| 2 | PNG refusal or unknown format. |
| 3 | Required CLI tool missing — run `/amw-init` / `/amw-doctor`. |

## Typical usage

```
/amw-validate-any-diagram-format /tmp/arch-diagram.svg
/amw-validate-any-diagram-format ./flowchart.mmd
/amw-validate-any-diagram-format sketch-v3.txt
```
