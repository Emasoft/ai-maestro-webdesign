---
name: amw-webpage-to-diagram
description: Extract a webpage (URL or local `.html`) as a diagram — two modes. STRUCTURAL emits a landmark/link graph as ASCII / SVG / Mermaid. SPATIAL emits an ASCII wireframe with boxes sized and positioned to match the page's visual layout (rendered-DOM geometry). Triggers on "diagram this URL", "structure of https://...", "sitemap from this HTML", "spatial layout of a page", "ascii wireframe of the layout". Refuses PNG; not generic "design a page". Use when extracting a webpage as a diagram.
version: 0.1.0
---

# Webpage to Diagram — DOM-to-IR extractor

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Format spec, IR schema, modify pipeline:** the authoritative HTML format spec, the IR schema produced by `bin/amw-dom-to-ir.py`, and the shared modify pipeline live in the `amw-diagram-formats` skill (its html, ir-schema, and modify-flow reference files) — consult that skill, not a copy here.

## Overview

Extracts a webpage (URL or local `.html`) as a diagram in one of two modes. Full pipeline for each is in the matching reference file below.

- **STRUCTURAL mode** (default; the `/amw-create-diagram-from-webpage` path) — **URL/HTML → IR → target format** (ASCII / SVG / Mermaid). Treats the whole page as a structural graph: every HTML5 landmark becomes an IR node, every internal anchor link becomes an IR edge, every nested `<svg>` is attached to its containing landmark. Backed by `bin/amw-dom-to-ir.py` (DOM-to-IR) and `bin/amw-dev-browser-wrapper.sh` (post-JS HTML capture). One leg of the webpage round-trip — the reverse leg is the `amw-diagram-webpage-sync` skill.
- **SPATIAL mode** (agent-facing; no `/command`) — **URL/HTML → rendered-DOM geometry → ASCII wireframe**. Reads `getBoundingClientRect` for every significant layout block and draws nested ASCII boxes positioned and sized to match the page's *visual* layout, for cheap plan-phase iteration. Backed by `bin/amw-page-to-ascii-layout.py`, which captures geometry via the `dev-browser` primitive, maps viewport coords onto a ≤78-column grid, and self-validates through `bin/amw-validate-ascii.py`. Without `dev-browser` it falls back to a static *stacked* layout (document order only — limitation stamped into the header). It is the EXTRACT-from-an-existing-page sibling of `amw-ascii-sketch` (which CREATES from scratch).

## Which mode? (do not confuse the two)

| You want… | Use | What you get |
|---|---|---|
| The *graph* of landmarks + how internal links connect them (sitemap / outline / IR for round-trip editing) | **STRUCTURAL** | nodes + edges, in ASCII / SVG / Mermaid |
| A *picture* of where things sit on the page — a wireframe whose boxes mirror the real positions and sizes | **SPATIAL** | one ASCII layout wireframe |

Rule of thumb: if the answer should be an **outline/graph** (what connects to what), pick structural; if it should *look like the page*, pick spatial. They never overlap. HTML-as-target is a no-op (already HTML). PNG-as-target is reachable via the IR → SVG → rasterize chain in the `amw-diagram-convert` skill, but the typical ask is ASCII (round-trip) or Mermaid (markdown). SPATIAL is ASCII-only (a wireframe primitive, not an IR producer).

## Instructions

1. **Decide the mode** (see the "Which mode?" table above): a **graph of landmarks/links** → STRUCTURAL; a **wireframe that mirrors the page's visual layout** → SPATIAL.
2. **Classify the input** (both modes): URL / local `.html` / refuse `.png` via extension, magic bytes, and `Content-Type: image/*`.
3. **Run the matching pipeline** from the reference file below: STRUCTURAL chains `dom-to-ir.py` → `diagram-ir.py emit` → `validate-diagram.sh` (7 steps); SPATIAL runs the single `bin/amw-page-to-ascii-layout.py` engine — capture → containment-tree → grid-map → render → self-validate-and-repair (6 steps).
4. **Confirm the terminating condition**: STRUCTURAL is done when `bin/amw-validate-diagram.sh` returns PASS on the emitted file; SPATIAL is done when the engine exits `0` (PASS). SPATIAL exit `1`/`2`/`3` (no blocks / PNG refusal / self-validation failure) are documented in the spatial-mode reference — a `.tentative` artifact is never returned as a result.
5. **Return the output file path** (and report any SPATIAL static-fallback limitation to the user).

## Per-mode reference files

- [structural-mode](./references/structural-mode.md) — full STRUCTURAL pipeline, instructions, error handling, output. Complete table of contents:
  - Overview
  - Instructions
  - Pipeline (7 steps)
  - Error Handling
  - Output
- [spatial-mode](./references/spatial-mode.md) — full SPATIAL pipeline, instructions, fallback, error handling, output. Complete table of contents:
  - Overview
  - Instructions
  - Pipeline (6 steps)
  - Fallback (no dev-browser)
  - Error Handling
  - Output

## Activation

**STRUCTURAL mode** is callable via `/amw-create-diagram-from-webpage`, or invoked by the `design-principles` orchestrator during **Phase B** as the forward leg of the round-trip. **SPATIAL mode** has no `/command` — it is agent-facing, invoked during the plan phase (Phase A, or an agent in Main-agent mode) when a cheap ASCII picture of an existing page's layout is needed. An agent in Main-agent mode may invoke either mode directly — the skill's techniques are NOT limited to what commands expose.

## Position in flow

**INPUT + OUTPUT.** Input: URL or local `.html`. Output: STRUCTURAL produces one diagram file (upstream of `/amw-modify-diagram-of-webpage`, which chains this skill with `amw-diagram-webpage-sync` for the round-trip); SPATIAL produces one validated ASCII wireframe (sibling of `amw-ascii-sketch`).

## Trigger conditions

STRUCTURAL mode:
- "diagram this URL" / "show me the structure of `<url>`" / "what does this webpage look like as an outline"
- "sitemap from this HTML" / "landmark diagram of this page" / "/amw-create-diagram-from-webpage `<url-or-path>`"

SPATIAL mode:
- "spatial layout of `<url-or-page>` in ascii" / "ascii wireframe matching the visual layout"
- "wireframe that mirrors where things sit on the page" / "draw the page layout as boxes positioned like the real page"

Do NOT activate on:
- "design a landing page" — orchestrator's job (`../amw-design-principles/`).
- "take a screenshot of `<url>`" — `../amw-dev-browser/` owns pure automation.
- "extract design tokens from `<url>`" — `../amw-design-extract/` owns style-token extraction.
- "build a webpage from a diagram" — `/amw-create-webpage-from-diagram` owns the reverse direction.
- "sketch me a new dashboard wireframe" (no existing page to read) — `../amw-ascii-sketch/` CREATES from scratch; SPATIAL only EXTRACTS from a real page's geometry.

## Output

STRUCTURAL: one diagram file per invocation in the chosen format (ASCII `.txt` default, `.svg`, or `.mmd`); output path follows the project-output-routing rules documented in the `amw-design-principles` skill (its project-output-routing reference file). SPATIAL: one validated ASCII wireframe (`.txt`) with a header comment recording page title, source, and capture method, guaranteed to PASS `bin/amw-validate-ascii.py`. The original page/HTML is never modified. Full per-mode output detail lives in the two reference files above.

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

## Error Handling

Each mode's error table lives in its reference file (full TOCs in "Per-mode reference files" above): STRUCTURAL in [structural-mode](./references/structural-mode.md) § Error Handling; SPATIAL in [spatial-mode](./references/spatial-mode.md) § Error Handling (incl. exit `1`/`2`/`3` codes + the static-fallback limitation).
> [spatial-mode.md] Overview · Instructions · Pipeline (6 steps) · Fallback (no dev-browser) · Error Handling · Output
> [structural-mode.md] Overview · Instructions · Pipeline (7 steps) · Error Handling · Output

## Resources

The structural-mode and spatial-mode reference files are linked with their full TOCs in the "Per-mode reference files" section above.

- [SKILL](../amw-dev-browser/SKILL.md) — upstream page-capture primitive (used by both modes).
- [SKILL](../amw-design-extract/SKILL.md) — sibling tool for token extraction (not structure).
- [SKILL](../amw-ascii-validator/SKILL.md) — documents the mandatory ASCII validation gate that SPATIAL output must pass.
- [SKILL](../amw-ascii-sketch/SKILL.md) — the CREATE-from-scratch sibling of SPATIAL mode (SPATIAL extracts a wireframe from a real page; ascii-sketch authors one from a brief).
- [SKILL](../amw-diagram-formats/SKILL.md) — authoritative HTML format spec, IR schema, and modify pipeline (its html, ir-schema, and modify-flow reference files).
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.

Backing `bin/` scripts: `amw-dom-to-ir.py` (DOM-to-IR, STRUCTURAL backend), `amw-page-to-ascii-layout.py` (rendered-DOM-geometry → ASCII wireframe, SPATIAL backend), `amw-validate-ascii.py` (ASCII validator SPATIAL self-validates against), `amw-parse-html-diagram.py` (inline-SVG extractor, subprocess of `dom-to-ir.py`), `amw-diagram-ir.py` (IR parse/emit/validate CLI), `amw-validate-diagram.sh` (unified validator dispatcher), `amw-dev-browser-wrapper.sh` (sanctioned browser automation wrapper).

## Related commands

- `/amw-create-diagram-from-webpage` — primary entry point for this skill.
- `/amw-modify-diagram-of-webpage` — MVP: chains this skill (extract) with a user-edit pause, then `/amw-modify-webpage-from-diagram` on `apply`.
- `/amw-convert-any-diagram-format` — sibling when the user wants to continue converting the extracted IR beyond the initial target.
