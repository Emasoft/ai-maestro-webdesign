# Webpage to Diagram — SPATIAL mode

## Table of Contents

- [Overview](#overview)
- [Instructions](#instructions)
- [Pipeline (6 steps)](#pipeline-6-steps)
- [Fallback (no dev-browser)](#fallback-no-dev-browser)
- [Error Handling](#error-handling)
- [Output](#output)

## Overview

SPATIAL mode is agent-facing (no `/command`): **URL/HTML → rendered-DOM geometry → ASCII wireframe**. It reads `getBoundingClientRect` for every significant layout block and draws nested ASCII boxes positioned and sized to match the page's *visual* layout. Output: a single validated ASCII wireframe, suitable for cheap plan-phase iteration. Backed by `bin/amw-page-to-ascii-layout.py`.

The engine drives the `dev-browser` primitive to capture geometry, maps viewport coords onto a ≤78-column grid × proportional rows, and self-validates the result through `bin/amw-validate-ascii.py` before returning. When `dev-browser` is unavailable it falls back to a best-effort *stacked* layout from the static HTML (document order only — the limitation is stamped into the output header).

Spatial mode is invoked during the plan phase for cheap, low-token ASCII iteration. It is the EXTRACT-from-an-existing-page sibling of the `amw-ascii-sketch` skill (which CREATES a wireframe from scratch). It is ASCII-only by design — a wireframe primitive, not an IR producer.

## Instructions

1. Classify input the same way as STRUCTURAL (URL / local `.html` / refuse `.png`). The engine performs the same PNG gates internally.
2. Run `python3 bin/amw-page-to-ascii-layout.py <url-or-html> --out <out.txt>` (add `--no-browser` to force the static fallback, `--headful` only for debugging, `--width N` to cap below 78 cols). The engine:
   - drives the `dev-browser` primitive to capture `getBoundingClientRect` geometry for every significant layout block (landmarks, headings, images, buttons, forms, tables, large divs, flex/grid items), filtering tiny/invisible/offscreen/over-nested noise in the browser;
   - builds a containment tree, drops redundant wrappers, and maps viewport pixel coords onto a ≤78-col grid × proportional rows;
   - draws nested ASCII boxes (`+`/`-`/`|`) preserving relative position and size, each labeled with its type + truncated text;
   - **self-validates through `bin/amw-validate-ascii.py` and auto-repairs until PASS** (this is mandatory and built into the script — alignment, width ≤ 78, no wide-char/forbidden-char leak).
3. If `dev-browser` is unavailable the engine automatically falls back to a stacked layout from the static HTML and stamps the limitation into the output header — report that limitation to the user.
4. Return the wireframe path. Exit codes: `0` PASS, `1` no significant blocks, `2` PNG refusal / misuse, `3` self-validation failed after the repair budget (engine bug — a `.tentative` file is left for inspection).

## Pipeline (6 steps)

All six steps are performed by `bin/amw-page-to-ascii-layout.py` in one invocation; the skill's job is to pick the input, run it, and report.

1. **Classify input.** URL / local `.html` / refuse `.png` (same gates as structural — extension, magic bytes, and `Content-Type: image/*` are all checked inside the engine).
2. **Capture geometry.** Drive the `dev-browser` primitive to run a DOM walker that returns `getBoundingClientRect` `{x,y,w,h}` plus tag / role / short-text for every significant layout block (`header`/`nav`/`main`/`section`/`article`/`aside`/`footer`, `h1`–`h3`, `img`, `button`, `form`, `table`, large divs, flex/grid items). Tiny, invisible, offscreen, and over-nested elements are filtered in the browser so only signal reaches Python.
3. **Build containment tree.** Parents enclose children by rect; redundant single-child wrappers are collapsed; siblings are ordered top-to-bottom, left-to-right.
4. **Map to grid.** Viewport pixel coords → ≤78-col grid × proportional rows. Nested boxes are inset on every side so child walls never sit 1–2 cols from a parent wall (keeps vertical-continuity intact); a parent grows to fully enclose any child pushed down by collision resolution.
5. **Render.** Draw nested ASCII rectangles (`+`/`-`/`|`) preserving relative position and size, each labeled with its type + truncated text. Border rows are kept pure (one box's corners per horizontal run) and every line is padded to one uniform width.
6. **Self-validate + repair.** Run `bin/amw-validate-ascii.py`; on FAIL, strip any stray wide/forbidden glyph, re-pad to uniform width, re-render at a slightly narrower grid, and retry until PASS or the repair budget is exhausted (exit 3 + `.tentative` artifact on exhaustion — an engine bug, not a user error).

## Fallback (no dev-browser)

The engine parses the static HTML with stdlib `html.parser` and emits a best-effort *stacked* layout (document order, full-width rows — no true geometry). The limitation is stamped into the output header comment and printed on stderr. Report it to the user.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| SPATIAL exit 1 (no significant blocks) | Page is empty or every block was filtered (trivial page, all content below the size/visibility threshold) | Confirm the page actually renders visible layout; for a near-empty page there is no spatial layout to draw. |
| SPATIAL exit 3 (self-validation failed after repair budget) | An engine bug produced un-fixable ASCII | A `.tentative` file is left on disk with the validator report — inspect it and file the bug; do NOT hand the un-validated `.tentative` to the user as a result. |
| SPATIAL fell back to stacked layout | `dev-browser` unavailable, timed out, or returned no JSON | The header comment says "static-HTML fallback — document ORDER only". Tell the user it is low-fidelity; run `/amw-init` and retry for true geometry. |
| SPATIAL wireframe looks shallow (deep nesting missing) | The ≤78-col inset budget runs out for blocks nested many levels deep | Expected for an ASCII wireframe — top-level partitions are preserved; reducing `--width` is NOT the fix (it only crowds further). Use STRUCTURAL mode if full nesting depth matters more than visual fidelity. |

## Output

One validated ASCII wireframe (`.txt`) written to `--out` (or stdout when omitted), preceded by a short header comment recording the page title, source, and capture method (rendered-DOM geometry vs static fallback). The wireframe is guaranteed to PASS `bin/amw-validate-ascii.py` before it is returned (≤78 cols, aligned, no wide/forbidden chars). The original page is never modified.
