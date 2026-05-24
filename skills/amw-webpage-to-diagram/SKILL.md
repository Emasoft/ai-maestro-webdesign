---
name: amw-webpage-to-diagram
description: Extract a webpage (URL or local `.html`) as a diagram — two modes. STRUCTURAL emits a landmark/link graph as ASCII / SVG / Mermaid. SPATIAL emits an ASCII wireframe with boxes sized and positioned to match the page's visual layout (rendered-DOM geometry). Triggers on "diagram this URL", "structure of https://...", "sitemap from this HTML", "spatial layout of a page", "ascii wireframe of the layout". Refuses PNG; not generic "design a page". Structural mode: /amw-create-diagram-from-webpage.
version: 0.1.0
---

# Webpage to Diagram — DOM-to-IR extractor

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Format spec (authoritative):** [html](../amw-diagram-formats/references/html.md).
> **IR schema:** [ir-schema](../amw-diagram-formats/references/ir-schema.md).
> **Modify pipeline (for the re-emit leg):** [modify-flow](../amw-diagram-formats/references/modify-flow.md).

This skill has **two modes** for turning a webpage into a diagram:

- **STRUCTURAL mode** (default; the `/amw-create-diagram-from-webpage` path) — **URL/HTML → IR → target format**. A specialization of `parse-html-diagram.py`: where that tool focuses on inline-`<svg>` diagrams, this mode treats the whole page as a structural graph: every HTML5 landmark (`<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<aside>`, `<header>`) becomes an IR node, every internal anchor link becomes an IR edge, and every nested `<svg>` diagram is attached as children of its containing landmark. Output: ASCII / SVG / Mermaid.
- **SPATIAL mode** (agent-facing; no `/command`) — **URL/HTML → rendered-DOM geometry → ASCII wireframe**. Reads `getBoundingClientRect` for every significant layout block and draws nested ASCII boxes positioned and sized to match the page's *visual* layout. Output: a single validated ASCII wireframe, suitable for cheap plan-phase iteration. Backed by `bin/amw-page-to-ascii-layout.py`.

### Which mode? (do not confuse the two)

| You want… | Use | What you get |
|---|---|---|
| The *graph* of landmarks + how internal links connect them (sitemap / outline / IR for round-trip editing) | **STRUCTURAL** | nodes + edges, in ASCII / SVG / Mermaid |
| A *picture* of where things sit on the page — a wireframe whose boxes mirror the real positions and sizes | **SPATIAL** | one ASCII layout wireframe |

Rule of thumb: if the answer should be an **outline/graph** (what connects to what), pick structural. If the answer should *look like the page* (where each block is, how big), pick spatial. They never overlap — one emits a relationship graph, the other emits a positioned wireframe.

HTML-as-target is a no-op (already HTML) — the dispatcher skips it. PNG-as-target is reachable via the standard IR → SVG → rasterize chain in `diagram-convert`, but the typical ask is ASCII (for round-trip editing) or Mermaid (for embedding in markdown). SPATIAL mode is ASCII-only by design (it is a wireframe primitive, not an IR producer).

## Overview
Extracts a webpage (URL or local `.html`) as a diagram in one of two modes.

**STRUCTURAL mode** emits the structural diagram in a chosen format — ASCII (default, for round-trip editing), SVG, or Mermaid. Treats HTML5 landmarks (`<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<aside>`, `<header>`) as IR nodes and internal anchor links as IR edges. Uses `bin/amw-dom-to-ir.py` for DOM-to-IR extraction and `bin/amw-dev-browser-wrapper.sh` for post-JS HTML capture. Refuses all PNG input absolutely. One leg of the webpage round-trip — the reverse leg is `amw-diagram-webpage-sync`.

**SPATIAL mode** emits a single ASCII wireframe whose nested boxes are positioned and sized to match the page's *visual* layout, read from rendered-DOM geometry (`getBoundingClientRect` of every significant layout block). Uses `bin/amw-page-to-ascii-layout.py`, which drives the `dev-browser` primitive to capture geometry, maps viewport coords onto a ≤78-column grid × proportional rows, and self-validates the result through `bin/amw-validate-ascii.py` before returning. When `dev-browser` is unavailable it falls back to a best-effort *stacked* layout from the static HTML (document order only — the limitation is stamped into the output header). Spatial mode is **agent-facing**: it is invoked during the plan phase for cheap, low-token ASCII iteration and does not get its own `/command`. It is the EXTRACT-from-an-existing-page sibling of `amw-ascii-sketch` (which CREATES a wireframe from scratch).

## Instructions

First decide the mode (see the "Which mode?" table above): a **graph of landmarks/links** → STRUCTURAL; a **wireframe that mirrors the page's visual layout** → SPATIAL.

### STRUCTURAL mode (default, `/command`-backed)

1. Classify input: URL (`http(s)://`), local `.html`/`.htm` path, or `.png` path — refuse PNG input immediately with the standard refusal message.
2. For URLs, send a `HEAD` request to check `Content-Type`; if it starts with `image/`, refuse as PNG; for local files check the first 8 bytes for PNG magic.
3. Fetch HTML: use `bin/amw-dev-browser-wrapper.sh` (post-JS rendered DOM) for URLs; fall back to `urllib.request` when the wrapper is unavailable.
4. Parse DOM to IR with `bin/amw-dom-to-ir.py --in <html> --out <ir.json> [--target-kind arch|flowchart|tree]`; default target-kind is `arch` (HTML5 landmarks as nodes, anchor links as edges).
5. Emit to the chosen format via `bin/amw-diagram-ir.py emit --in <ir> --format <ascii|svg|mermaid> --out <out-path>`; skip emission if target format is `html` (already HTML).
6. Validate with `bin/amw-validate-diagram.sh <out-path>`; a FAIL surfaces FIX hints verbatim and leaves a `.tentative` file on disk — no retry budget here (failures indicate a parser bug, not a fixable IR patch).
7. Return the output file path.

See `## Pipeline — STRUCTURAL mode (7 steps)` below.

### SPATIAL mode (agent-facing, no `/command`)

1. Classify input the same way (URL / local `.html` / refuse `.png`). The engine performs the same PNG gates internally.
2. Run `python3 bin/amw-page-to-ascii-layout.py <url-or-html> --out <out.txt>` (add `--no-browser` to force the static fallback, `--headful` only for debugging, `--width N` to cap below 78 cols). The engine:
   - drives the `dev-browser` primitive to capture `getBoundingClientRect` geometry for every significant layout block (landmarks, headings, images, buttons, forms, tables, large divs, flex/grid items), filtering tiny/invisible/offscreen/over-nested noise in the browser;
   - builds a containment tree, drops redundant wrappers, and maps viewport pixel coords onto a ≤78-col grid × proportional rows;
   - draws nested ASCII boxes (`+`/`-`/`|`) preserving relative position and size, each labeled with its type + truncated text;
   - **self-validates through `bin/amw-validate-ascii.py` and auto-repairs until PASS** (this is mandatory and built into the script — alignment, width ≤ 78, no wide-char/forbidden-char leak).
3. If `dev-browser` is unavailable the engine automatically falls back to a stacked layout from the static HTML and stamps the limitation into the output header — report that limitation to the user.
4. Return the wireframe path. Exit codes: `0` PASS, `1` no significant blocks, `2` PNG refusal / misuse, `3` self-validation failed after the repair budget (engine bug — a `.tentative` file is left for inspection).

## Activation

**STRUCTURAL mode** is callable directly via the `/amw-create-diagram-from-webpage` command, or invoked by the `design-principles` orchestrator during **Phase B** as the forward leg of the webpage round-trip. **SPATIAL mode** has no `/command`: it is agent-facing, invoked during the plan phase (Phase A or an agent in Main-agent mode) when a cheap ASCII picture of an existing page's layout is needed for iteration. An agent in Main-agent mode may invoke either mode directly — the skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**INPUT + OUTPUT.** Input side: URL or local `.html`. Output side: STRUCTURAL produces one diagram file in the user's chosen format (upstream of `/amw-modify-diagram-of-webpage`, which chains this skill with `diagram-webpage-sync` for the full round-trip); SPATIAL produces one validated ASCII wireframe for plan-phase iteration (sibling of `amw-ascii-sketch`, which creates a wireframe from scratch rather than extracting one from a live page).

## Trigger conditions

STRUCTURAL mode:
- "extract the diagram from `<url>`" / "diagram this URL" / "show me the structure of `<url>`"
- "sitemap from this HTML" / "landmark diagram of this page"
- "what's the structure of `https://...`" / "what does this webpage look like as an outline"
- "/amw-create-diagram-from-webpage `<url-or-path>`"

SPATIAL mode:
- "spatial layout of `<url-or-page>`" / "show me the spatial layout of this page in ascii"
- "ascii wireframe matching the visual layout" / "wireframe that mirrors where things sit on the page"
- "what does this page look like spatially in ascii" / "draw the page layout as boxes positioned like the real page"

Do NOT activate on:
- "design a landing page" — orchestrator's job (`../amw-design-principles/`).
- "take a screenshot of `<url>`" — `../amw-dev-browser/` owns pure automation.
- "extract design tokens from `<url>`" — `../amw-design-extract/` owns style-token extraction.
- "build a webpage from a diagram" — `/amw-create-webpage-from-diagram` owns the reverse direction.
- "sketch me a new dashboard wireframe" (no existing page to read) — `../amw-ascii-sketch/` CREATES from scratch; SPATIAL mode only EXTRACTS from a real page's geometry.

## Pipeline — STRUCTURAL mode (7 steps)

1. **Classify input.** Is `$ARGUMENTS` a URL (scheme `http(s)://`), a local path ending in `.html`/`.htm`, or a PNG path? URL and HTML are both in scope. `.png` extension → refuse immediately with the standard PNG-refusal message.
2. **Detect mime (URL only).** Call `HEAD` via urllib to read `Content-Type`. If the header starts with `image/` → refuse with the standard PNG-refusal message (`REFUSE: PNG-embedded diagram cannot be modified — provide the source artifact`). This catches the case where the URL resolves to an image directly (e.g. a screenshot exported as `.png`).
3. **Check PNG magic (local file only).** If `--in <path>` and the first 8 bytes are the PNG magic `0x89 50 4E 47 0D 0A 1A 0A`, refuse with the same message. File extension alone is not authoritative — content check closes the loophole.
4. **Fetch HTML (URL only).** Call `bin/amw-dev-browser-wrapper.sh` (via the raw `dev-browser eval` command) to capture the post-JS rendered `document.documentElement.outerHTML`. Fall back to plain `urllib.request` when the wrapper is unavailable — the wrapper's fallback is documented as pre-JS HTML only, which is usually enough for structural extraction but may miss SPA-rendered content.
5. **Parse DOM to IR.** Call `bin/amw-dom-to-ir.py --in <tmp-or-local-html> --out /tmp/amw-page-<hash>.json [--target-kind arch|flowchart|tree]`. The target-kind flag hints downstream emitters; `arch` (layered landmarks) is the default because it matches the dominant page-skeleton pattern.
6. **Emit to target format.** If target is `html` (no-op — already HTML), skip emission and report the input path. Otherwise, chain to `bin/amw-diagram-ir.py emit --in <ir> --format <target> --out <out-path>`. ASCII is the default (pair-able with `/amw-modify-diagram-of-webpage` for round-trip editing).
7. **Validate.** Run `bin/amw-validate-diagram.sh <out-path>`. A FAIL aborts the skill, surfaces FIX hints verbatim, and leaves the emitted file (marked `.tentative`) on disk for inspection. Retry budget is NOT applied here — validation failure is usually a parser bug, not a fixable IR patch.

## Pipeline — SPATIAL mode (6 steps)

All six steps are performed by `bin/amw-page-to-ascii-layout.py` in one invocation; the skill's job is to pick the input, run it, and report.

1. **Classify input.** URL / local `.html` / refuse `.png` (same gates as structural — extension, magic bytes, and `Content-Type: image/*` are all checked inside the engine).
2. **Capture geometry.** Drive the `dev-browser` primitive to run a DOM walker that returns `getBoundingClientRect` `{x,y,w,h}` plus tag / role / short-text for every significant layout block (`header`/`nav`/`main`/`section`/`article`/`aside`/`footer`, `h1`–`h3`, `img`, `button`, `form`, `table`, large divs, flex/grid items). Tiny, invisible, offscreen, and over-nested elements are filtered in the browser so only signal reaches Python.
3. **Build containment tree.** Parents enclose children by rect; redundant single-child wrappers are collapsed; siblings are ordered top-to-bottom, left-to-right.
4. **Map to grid.** Viewport pixel coords → ≤78-col grid × proportional rows. Nested boxes are inset on every side so child walls never sit 1–2 cols from a parent wall (keeps vertical-continuity intact); a parent grows to fully enclose any child pushed down by collision resolution.
5. **Render.** Draw nested ASCII rectangles (`+`/`-`/`|`) preserving relative position and size, each labeled with its type + truncated text. Border rows are kept pure (one box's corners per horizontal run) and every line is padded to one uniform width.
6. **Self-validate + repair.** Run `bin/amw-validate-ascii.py`; on FAIL, strip any stray wide/forbidden glyph, re-pad to uniform width, re-render at a slightly narrower grid, and retry until PASS or the repair budget is exhausted (exit 3 + `.tentative` artifact on exhaustion — an engine bug, not a user error).

**Fallback (no `dev-browser`):** the engine parses the static HTML with stdlib `html.parser` and emits a best-effort *stacked* layout (document order, full-width rows — no true geometry). The limitation is stamped into the output header comment and printed on stderr. Report it to the user.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| PNG refusal | Input file extension is `.png`, file magic bytes are PNG, OR URL HEAD returns `Content-Type: image/*` | Provide the source artifact (ASCII / HTML / SVG / Mermaid) that produced the PNG. No OCR, no best-effort workaround. |
| `dev-browser: command not found` | `/amw-init` hasn't been run | Run `/amw-init` to install dev-browser, OR let the skill fall back to urllib (pre-JS HTML only — SPA content may be missed). |
| Empty `nodes` in IR | Page has no HTML5 landmarks (div-soup site) | The parser emits a single `kind:"freeform"` node with the page title as label; target-format emission still succeeds, but downstream edits won't have landmark granularity. |
| URL 4xx / 5xx | Target page unreachable or auth-gated | Report the HTTP status verbatim; ask the user to supply a local `.html` export instead. |
| Validation FAIL on emitted ASCII | Downstream renderer produced misaligned output | Save the IR to `/tmp/amw-page-<hash>.json` for inspection; ask the user to rerun with `--target-kind flowchart` (less strict alignment). |
| SPATIAL exit 1 (no significant blocks) | Page is empty or every block was filtered (trivial page, all content below the size/visibility threshold) | Confirm the page actually renders visible layout; for a near-empty page there is no spatial layout to draw. |
| SPATIAL exit 3 (self-validation failed after repair budget) | An engine bug produced un-fixable ASCII | A `.tentative` file is left on disk with the validator report — inspect it and file the bug; do NOT hand the un-validated `.tentative` to the user as a result. |
| SPATIAL fell back to stacked layout | `dev-browser` unavailable, timed out, or returned no JSON | The header comment says "static-HTML fallback — document ORDER only". Tell the user it is low-fidelity; run `/amw-init` and retry for true geometry. |
| SPATIAL wireframe looks shallow (deep nesting missing) | The ≤78-col inset budget runs out for blocks nested many levels deep | Expected for an ASCII wireframe — top-level partitions are preserved; reduce `--width` is NOT the fix (it only crowds further). Use STRUCTURAL mode if full nesting depth matters more than visual fidelity. |

## Output

STRUCTURAL mode: one diagram file per invocation in the user's chosen format (ASCII `.txt` by default, `.svg`, or `.mmd`). Output path follows project-inference rules from [project-output-routing](../amw-design-principles/references/project-output-routing.md). The original HTML is never modified.

SPATIAL mode: one validated ASCII wireframe (`.txt`) written to `--out` (or stdout when omitted), preceded by a short header comment recording the page title, source, and capture method (rendered-DOM geometry vs static fallback). The wireframe is guaranteed to PASS `bin/amw-validate-ascii.py` before it is returned (≤78 cols, aligned, no wide/forbidden chars). The original page is never modified.

## Prerequisites

```yaml
runtime_binaries:
  - python3   # >= 3.8 — runs bin/amw-dom-to-ir.py, bin/amw-diagram-ir.py,
              #          bin/amw-page-to-ascii-layout.py (SPATIAL), bin/amw-validate-ascii.py
  - node      # >= 22 — runtime for dev-browser (via /amw-init)
  - dev-browser   # installed via /amw-init — post-JS HTML capture (STRUCTURAL)
                  #   AND rendered-DOM geometry capture (SPATIAL). Absent ⇒
                  #   SPATIAL auto-falls-back to a static stacked layout.

python_packages:
  - lxml              # OPTIONAL — more reliable nested HTML handling
  - beautifulsoup4    # OPTIONAL — same
  # Both are auto-detected; stdlib path works without them. SPATIAL mode is
  # pure stdlib — no extra packages.

npm_packages:
  - dev-browser   # global, installed by /amw-init
```

## Non-negotiables

- **PNG refusal is absolute** (both modes). File extension, magic bytes, or URL `Content-Type: image/*` — any hit aborts with the standard message. No OCR, no guess-reconstruct.
- **No direct scraping with a new browser stack** (both modes). Page capture flows through the `dev-browser` primitive only — never `puppeteer`, `playwright-mcp`, `selenium`, or any other automation surface.
- **IR is the pivot for STRUCTURAL mode.** Even when the target is HTML, the path is DOM → IR → HTML (the no-op case is just "don't re-emit"). Bypassing IR for direct HTML rewriting is OUT of scope — use `/amw-modify-webpage-from-diagram` or `/amw-ascii-to-html` for that. (SPATIAL mode does NOT produce IR — it is a wireframe primitive, not a round-trip leg.)
- **SPATIAL output obeys the ASCII contract.** ≤ 78 columns; MUST PASS `bin/amw-validate-ascii.py` before it is returned (the engine self-validates and auto-repairs — a result that has not passed is never handed to the user). No wide chars (CJK/emoji), no forbidden glyphs (`▼▲▶◀⟶⇒` …).
- **CLEAN-ROOM.** The SPATIAL capability is built fresh from the W3C-standard `getBoundingClientRect` geometry and the repo's own ASCII renderer/validator conventions. It does NOT copy, read, or derive from any third-party Figma-to-markdown plugin or any material under `SKILLS-TO-INTEGRATE/`.
- Inherits the three hard rules from [SKILL](../amw-design-principles/SKILL.md) (context, variants, AI-slop refusal) whenever the downstream target is a design artifact (e.g. emitting ASCII for a `/amw-ascii-to-html` round-trip).

## Examples
See [SKILL](../amw-diagram-webpage-sync/SKILL.md) for a complete round-trip example (extract → edit → re-apply).

## Resources

- [html](../amw-diagram-formats/references/html.md) — authoritative HTML format spec.
- [ir-schema](../amw-diagram-formats/references/ir-schema.md) — IR schema produced by `bin/amw-dom-to-ir.py`.
- [modify-flow](../amw-diagram-formats/references/modify-flow.md) — shared 6-step pipeline consumed by the round-trip skills.
- [SKILL](../amw-dev-browser/SKILL.md) — upstream page-capture primitive (used by both modes).
- [SKILL](../amw-design-extract/SKILL.md) — sibling tool for token extraction (not structure).
- [SKILL](../amw-ascii-validator/SKILL.md) — documents the mandatory ASCII validation gate that SPATIAL output must pass.
- [SKILL](../amw-ascii-sketch/SKILL.md) — the CREATE-from-scratch sibling of SPATIAL mode (SPATIAL extracts a wireframe from a real page; ascii-sketch authors one from a brief).
- `../../bin/amw-dom-to-ir.py` — DOM-to-IR extractor (STRUCTURAL mode's core backend).
- `../../bin/amw-page-to-ascii-layout.py` — rendered-DOM-geometry → ASCII layout-wireframe engine (SPATIAL mode's core backend).
- `../../bin/amw-validate-ascii.py` — ASCII alignment/width/char validator that SPATIAL output self-validates against.
- `../../bin/amw-parse-html-diagram.py` — inline-SVG extractor (called as subprocess by `dom-to-ir.py` for nested SVGs).
- `../../bin/amw-diagram-ir.py` — IR parse/emit/validate CLI.
- `../../bin/amw-validate-diagram.sh` — unified validator dispatcher.
- `../../bin/amw-dev-browser-wrapper.sh` — sanctioned browser automation wrapper.
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.

## Related commands

- `/amw-create-diagram-from-webpage` — primary entry point for this skill.
- `/amw-modify-diagram-of-webpage` — MVP: chains this skill (extract) with a user-edit pause, then `/amw-modify-webpage-from-diagram` on `apply`.
- `/amw-convert-any-diagram-format` — sibling when the user wants to continue converting the extracted IR beyond the initial target.
