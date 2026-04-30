---
name: amw-modify-webpage-from-diagram
description: "Shortcut for users who have an edited diagram and want to re-emit a specific webpage from it directly — chains diagram → IR → ASCII → HTML with .bak backup. An agent in Main-agent mode may also invoke skills/amw-diagram-webpage-sync/ directly via the orchestrator, applying the full sync and diff techniques the skill exposes."
---

# /amw-modify-webpage-from-diagram

Thin dispatcher over `skills/amw-diagram-webpage-sync/`. Takes an existing webpage and a new diagram source, re-runs the ascii-to-html pipeline, and overwrites the page after backing up the original.

## Arguments

```
/amw-modify-webpage-from-diagram <webpage.html> <new-diagram> [--out <path>]
```

- `<webpage.html>` — **required.** Path to the existing HTML page to modify. Must be a regular file.
- `<new-diagram>` — **required.** Path to the new / edited diagram. Format is auto-detected (`ascii` / `svg` / `mermaid`). `html` and `png` sources are refused.
- `--out <path>` — override output path. Default: **overwrite `<webpage.html>`** after moving the original to `<webpage.html>.bak`. When `--out` is supplied, the original is left untouched and the fresh output is written to `<path>`.

## Dispatch

1. **Input-file gate.** Both `<webpage.html>` and `<new-diagram>` must exist and be readable. Absent → exit 2 with path in the error.
2. **Format gate.**
   - `bin/amw-diagram-detect-format.sh <new-diagram>` must be one of `ascii` / `svg` / `mermaid`. `html` → hint to use `/amw-ascii-to-html` directly; `png` → standard PNG refusal; `unknown` → ask the user for a recognized extension or a `--format` override.
   - `bin/amw-diagram-detect-format.sh <webpage.html>` must be `html`. Otherwise exit 2.
3. **PNG-embedded detection.** Scan `<webpage.html>` for `<img src="*.png">` and `data:image/png;base64,...`. If either appears in what the parser considers the diagram region (primary inline SVG / primary landmark with `data-diagram-*` attrs), exit 2 with `REFUSE: PNG-embedded diagram cannot be modified — provide the source artifact (ASCII / HTML / SVG / Mermaid)`. No OCR, no best-effort recovery.
4. **Route to skill.** Invoke `skills/amw-diagram-webpage-sync/SKILL.md` pipeline steps 1–7:
   - parse old HTML to IR,
   - parse new diagram to IR,
   - compute IR-level diff,
   - full re-emission via `/amw-ascii-to-html` (backing up to `.bak` first),
   - run `bin/amw-html-diff.py --before <webpage>.bak --after <webpage>`,
   - validate with `bin/amw-validate-diagram.sh`,
   - announce result.
5. **Report.** On PASS: print the IR-level diff summary + the HTML-level diff summary + the `.bak` location. On FAIL: restore from `.bak` atomically, surface the validator FIX hints verbatim.

## MVP limit (explicit call-out)

This MVP **re-emits the full webpage.** Any manual post-generation edits the user made to the original HTML (custom CSS outside the diagram region, third-party script integrations, handwritten copy) will NOT be preserved — they remain only in `.bak`. Full DOM-surgical sync-back (preserving original styling while only swapping the diagram) is **DEFERRED** to a future phase.

If you rely on manual styling outside the diagram, consider using `/amw-sketch` + `/amw-ascii-to-html` fresh and hand-grafting the diagram region.

## Exit codes

| Exit | Meaning |
|---|---|
| 0 | Re-emission + validation succeeded; `.bak` is at `<webpage>.bak`. |
| 1 | Re-emission or validation FAIL (restored from `.bak`). |
| 2 | PNG-embedded refusal, bad input format, or missing files. |
| 3 | Missing runtime dep (run `/amw-doctor` / `/amw-init`). |

## Cross-references

- `skills/amw-diagram-webpage-sync/SKILL.md` — primary backing skill.
- `skills/amw-diagram-formats/references/modify-flow.md` — shared modify pipeline (§7.1 webpage-sync composition).
- `skills/amw-diagram-formats/references/html.md` — HTML format spec (consumed at re-emission step).
- `bin/amw-html-diff.py`, `bin/amw-diagram-ir.py`, `bin/amw-parse-html-diagram.py`, `bin/amw-validate-diagram.sh` — backing tools.
- `/amw-ascii-to-html` — terminal step of the re-emit pipeline.
- `/amw-modify-diagram-of-webpage` — pair command for the two-half round-trip (extract → user-edit → apply).
- `/amw-create-webpage-from-diagram` — greenfield sibling (no existing page).
