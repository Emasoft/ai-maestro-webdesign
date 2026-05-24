# Webpage to Diagram — STRUCTURAL mode

## Table of Contents

- [Overview](#overview)
- [Instructions](#instructions)
- [Pipeline (7 steps)](#pipeline-7-steps)
- [Error Handling](#error-handling)
- [Output](#output)

## Overview

STRUCTURAL mode is the default, `/amw-create-diagram-from-webpage`-backed path: **URL/HTML → IR → target format**. A specialization of `parse-html-diagram.py`: where that tool focuses on inline-`<svg>` diagrams, this mode treats the whole page as a structural graph — every HTML5 landmark (`<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<aside>`, `<header>`) becomes an IR node, every internal anchor link becomes an IR edge, and every nested `<svg>` diagram is attached as children of its containing landmark. Output: ASCII (default, for round-trip editing), SVG, or Mermaid.

Uses `bin/amw-dom-to-ir.py` for DOM-to-IR extraction and `bin/amw-dev-browser-wrapper.sh` for post-JS HTML capture. Refuses all PNG input absolutely. This is one leg of the webpage round-trip — the reverse leg is the `amw-diagram-webpage-sync` skill.

HTML-as-target is a no-op (already HTML) — the dispatcher skips it. PNG-as-target is reachable via the standard IR → SVG → rasterize chain in the `amw-diagram-convert` skill, but the typical ask is ASCII (for round-trip editing) or Mermaid (for embedding in markdown).

## Instructions

1. Classify input: URL (`http(s)://`), local `.html`/`.htm` path, or `.png` path — refuse PNG input immediately with the standard refusal message.
2. For URLs, send a `HEAD` request to check `Content-Type`; if it starts with `image/`, refuse as PNG; for local files check the first 8 bytes for PNG magic.
3. Fetch HTML: use `bin/amw-dev-browser-wrapper.sh` (post-JS rendered DOM) for URLs; fall back to `urllib.request` when the wrapper is unavailable.
4. Parse DOM to IR with `bin/amw-dom-to-ir.py --in <html> --out <ir.json> [--target-kind arch|flowchart|tree]`; default target-kind is `arch` (HTML5 landmarks as nodes, anchor links as edges).
5. Emit to the chosen format via `bin/amw-diagram-ir.py emit --in <ir> --format <ascii|svg|mermaid> --out <out-path>`; skip emission if target format is `html` (already HTML).
6. Validate with `bin/amw-validate-diagram.sh <out-path>`; a FAIL surfaces FIX hints verbatim and leaves a `.tentative` file on disk — no retry budget here (failures indicate a parser bug, not a fixable IR patch).
7. Return the output file path.

## Pipeline (7 steps)

1. **Classify input.** Is `$ARGUMENTS` a URL (scheme `http(s)://`), a local path ending in `.html`/`.htm`, or a PNG path? URL and HTML are both in scope. `.png` extension → refuse immediately with the standard PNG-refusal message.
2. **Detect mime (URL only).** Call `HEAD` via urllib to read `Content-Type`. If the header starts with `image/` → refuse with the standard PNG-refusal message (`REFUSE: PNG-embedded diagram cannot be modified — provide the source artifact`). This catches the case where the URL resolves to an image directly (e.g. a screenshot exported as `.png`).
3. **Check PNG magic (local file only).** If `--in <path>` and the first 8 bytes are the PNG magic `0x89 50 4E 47 0D 0A 1A 0A`, refuse with the same message. File extension alone is not authoritative — content check closes the loophole.
4. **Fetch HTML (URL only).** Call `bin/amw-dev-browser-wrapper.sh` (via the raw `dev-browser eval` command) to capture the post-JS rendered `document.documentElement.outerHTML`. Fall back to plain `urllib.request` when the wrapper is unavailable — the wrapper's fallback is documented as pre-JS HTML only, which is usually enough for structural extraction but may miss SPA-rendered content.
5. **Parse DOM to IR.** Call `bin/amw-dom-to-ir.py --in <tmp-or-local-html> --out /tmp/amw-page-<hash>.json [--target-kind arch|flowchart|tree]`. The target-kind flag hints downstream emitters; `arch` (layered landmarks) is the default because it matches the dominant page-skeleton pattern.
6. **Emit to target format.** If target is `html` (no-op — already HTML), skip emission and report the input path. Otherwise, chain to `bin/amw-diagram-ir.py emit --in <ir> --format <target> --out <out-path>`. ASCII is the default (pair-able with `/amw-modify-diagram-of-webpage` for round-trip editing).
7. **Validate.** Run `bin/amw-validate-diagram.sh <out-path>`. A FAIL aborts the skill, surfaces FIX hints verbatim, and leaves the emitted file (marked `.tentative`) on disk for inspection. Retry budget is NOT applied here — validation failure is usually a parser bug, not a fixable IR patch.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| PNG refusal | Input file extension is `.png`, file magic bytes are PNG, OR URL HEAD returns `Content-Type: image/*` | Provide the source artifact (ASCII / HTML / SVG / Mermaid) that produced the PNG. No OCR, no best-effort workaround. |
| `dev-browser: command not found` | `/amw-init` hasn't been run | Run `/amw-init` to install dev-browser, OR let the skill fall back to urllib (pre-JS HTML only — SPA content may be missed). |
| Empty `nodes` in IR | Page has no HTML5 landmarks (div-soup site) | The parser emits a single `kind:"freeform"` node with the page title as label; target-format emission still succeeds, but downstream edits won't have landmark granularity. |
| URL 4xx / 5xx | Target page unreachable or auth-gated | Report the HTTP status verbatim; ask the user to supply a local `.html` export instead. |
| Validation FAIL on emitted ASCII | Downstream renderer produced misaligned output | Save the IR to `/tmp/amw-page-<hash>.json` for inspection; ask the user to rerun with `--target-kind flowchart` (less strict alignment). |

## Output

One diagram file per invocation in the user's chosen format (ASCII `.txt` by default, `.svg`, or `.mmd`). Output path follows the project-output-routing rules documented in the `amw-design-principles` skill (its project-output-routing reference file). The original HTML is never modified.
