---
name: amw-webpage-to-diagram
description: Extract the structural diagram of a webpage (URL or local `.html`) and emit it as ASCII / SVG / Mermaid (default ASCII). Triggers on "extract diagram from webpage", "diagram this URL", "what's the structure of https://...", "sitemap from this HTML", "landmark diagram of this page". Does NOT claim generic "design a page" — those route to design-principles. Refuses PNG input. Use when extracting a structural diagram from a URL or HTML file. Trigger with /amw-create-diagram-from-webpage.
version: 0.1.0
---

# Webpage to Diagram — DOM-to-IR extractor

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Format spec (authoritative):** [html](../amw-diagram-formats/references/html.md).
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG/PDF rasterizer (Playwright) · `../../bin/amw-ascii-parse.py` — ASCII → layout JSON consumed by HTML emitter · ir-schema · conversion-matrix · modify-flow · validation-dispatcher
> **IR schema:** [ir-schema](../amw-diagram-formats/references/ir-schema.md).
> [ir-schema.md] Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Validation · Consumers
> **Modify pipeline (for the re-emit leg):** [modify-flow](../amw-diagram-formats/references/modify-flow.md).
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`

This skill owns one direction of the webpage round-trip: **URL/HTML → IR → target format**. It is a specialization of `parse-html-diagram.py` — where that tool focuses on inline-`<svg>` diagrams, this skill treats the whole page as a structural graph: every HTML5 landmark (`<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<aside>`, `<header>`) becomes an IR node, every internal anchor link becomes an IR edge, and every nested `<svg>` diagram is attached as children of its containing landmark.

HTML-as-target is a no-op (already HTML) — the dispatcher skips it. PNG-as-target is reachable via the standard IR → SVG → rasterize chain in `diagram-convert`, but the typical ask is ASCII (for round-trip editing) or Mermaid (for embedding in markdown).

## Overview
Extracts the structural diagram of a webpage (URL or local `.html`) and emits it in a chosen format — ASCII (default, for round-trip editing), SVG, or Mermaid. Treats HTML5 landmarks (`<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<aside>`, `<header>`) as IR nodes and internal anchor links as IR edges. Uses `bin/amw-dom-to-ir.py` for DOM-to-IR extraction and `bin/amw-dev-browser-wrapper.sh` for post-JS HTML capture. Refuses all PNG input absolutely. One leg of the webpage round-trip — the reverse leg is `amw-diagram-webpage-sync`.

## Instructions

1. Classify input: URL (`http(s)://`), local `.html`/`.htm` path, or `.png` path — refuse PNG input immediately with the standard refusal message.
2. For URLs, send a `HEAD` request to check `Content-Type`; if it starts with `image/`, refuse as PNG; for local files check the first 8 bytes for PNG magic.
3. Fetch HTML: use `bin/amw-dev-browser-wrapper.sh` (post-JS rendered DOM) for URLs; fall back to `urllib.request` when the wrapper is unavailable.
4. Parse DOM to IR with `bin/amw-dom-to-ir.py --in <html> --out <ir.json> [--target-kind arch|flowchart|tree]`; default target-kind is `arch` (HTML5 landmarks as nodes, anchor links as edges).
5. Emit to the chosen format via `bin/amw-diagram-ir.py emit --in <ir> --format <ascii|svg|mermaid> --out <out-path>`; skip emission if target format is `html` (already HTML).
6. Validate with `bin/amw-validate-diagram.sh <out-path>`; a FAIL surfaces FIX hints verbatim and leaves a `.tentative` file on disk — no retry budget here (failures indicate a parser bug, not a fixable IR patch).
7. Return the output file path.

See `## Pipeline (7 steps)` below.

## Activation

Callable directly via the `/amw-create-diagram-from-webpage` command (user shortcut for users who have a URL or local `.html` and want to extract its structural diagram), or invoked by the `design-principles` orchestrator during **Phase B** as the forward leg of the webpage round-trip. An agent in Main-agent mode may also invoke this skill directly via the orchestrator without going through the command.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**INPUT + OUTPUT.** Input side: URL or local `.html`. Output side: one diagram file in the user's chosen format. Upstream of `/amw-modify-diagram-of-webpage` (which chains this skill with `diagram-webpage-sync` for the full round-trip).

## Trigger conditions

- "extract the diagram from `<url>`" / "diagram this URL" / "show me the structure of `<url>`"
- "sitemap from this HTML" / "landmark diagram of this page"
- "what's the structure of `https://...`" / "what does this webpage look like as an outline"
- "/amw-create-diagram-from-webpage `<url-or-path>`"

Do NOT activate on:
- "design a landing page" — orchestrator's job (`../amw-design-principles/`).
- "take a screenshot of `<url>`" — `../amw-dev-browser/` owns pure automation.
- "extract design tokens from `<url>`" — `../amw-design-extract/` owns style-token extraction.
- "build a webpage from a diagram" — `/amw-create-webpage-from-diagram` owns the reverse direction.

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
One diagram file per invocation in the user's chosen format (ASCII `.txt` by default, `.svg`, or `.mmd`). Output path follows project-inference rules from [project-output-routing](../amw-design-principles/references/project-output-routing.md). The original HTML is never modified.
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references

## Prerequisites

```yaml
runtime_binaries:
  - python3   # >= 3.8 — runs bin/amw-dom-to-ir.py, bin/amw-diagram-ir.py
  - node      # >= 22 — runtime for dev-browser (via /amw-init)
  - dev-browser   # installed via /amw-init — post-JS HTML capture

python_packages:
  - lxml              # OPTIONAL — more reliable nested HTML handling
  - beautifulsoup4    # OPTIONAL — same
  # Both are auto-detected; stdlib path works without them.

npm_packages:
  - dev-browser   # global, installed by /amw-init
```

## Non-negotiables

- **PNG refusal is absolute.** File extension, magic bytes, or URL `Content-Type: image/*` — any hit aborts with the standard message. No OCR, no guess-reconstruct.
- **No direct scraping with a new browser stack.** Page fetch flows through `bin/amw-dev-browser-wrapper.sh` — never `puppeteer`, `playwright-mcp`, `selenium`, or any other automation surface.
- **IR is the pivot.** Even when the target is HTML, the path is DOM → IR → HTML (the no-op case is just "don't re-emit"). Bypassing IR for direct HTML rewriting is OUT of scope — use `/amw-modify-webpage-from-diagram` or `/amw-ascii-to-html` for that.
- Inherits the three hard rules from [SKILL](../amw-design-principles/SKILL.md) (context, variants, AI-slop refusal) whenever the downstream target is a design artifact (e.g. emitting ASCII for a `/amw-ascii-to-html` round-trip).

## Examples
See [SKILL](../amw-diagram-webpage-sync/SKILL.md) for a complete round-trip example (extract → edit → re-apply).

## Resources

- [html](../amw-diagram-formats/references/html.md) — authoritative HTML format spec (consumed via `bin/amw-parse-html-diagram.py` for nested SVGs).
  > Format definition · 1 File structure (baseline) · 2 Semantic-HTML requirements · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · 1 Listener-before-announce · 2 Partial-keys only · 3 Valid JSON EDITMODE block · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · S1 — design-principles starter-components (canonical chrome) · S2 — ai-slop-avoid (output-ban gate) · S3 — ui-ux-pro-max-skill (industry patterns) · S4 — ux-designer + accessibility · S5 — create-infographics (editorial density) · S6 — diagram-design-editorial (self-contained HTML+SVG) · S7 — ascii-creator mirror (pattern recognition) · S8 — CHI'24 ASCII classics (mockup → HTML skeleton) · S9 — ascii-parse.py (in-repo tokenizer hooks) · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · …(+9)
- [ir-schema](../amw-diagram-formats/references/ir-schema.md) — IR schema produced by `bin/amw-dom-to-ir.py`.
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
- [modify-flow](../amw-diagram-formats/references/modify-flow.md) — shared 6-step pipeline consumed by the round-trip skills.
  > The pipeline · Create vs modify dispatch · Step-by-step detail · Step 1 — Detect · Step 2 — Parse to IR · Step 3 — Patch · Step 4 — (loop point) · Step 5 — Emit · Step 6 — Re-validate · Work directory and file naming · Per-format guidance · 1 ASCII modify (MVP structural) · 2 HTML modify (MVP raw-source; Phase 1 structural) · 3 SVG modify (MVP raw-source; Phase 1 structural) · 4 Mermaid modify (MVP raw-source; Phase 1 structural) · Conversion is a modify-flow variant · Composition with round-trip skills · 1 `diagram-webpage-sync` (`/amw-modify-webpage-from-diagram`) · 2 `webpage-to-diagram` (`/amw-modify-diagram-of-webpage`) · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
- [SKILL](../amw-dev-browser/SKILL.md) — upstream page-capture primitive.
- [SKILL](../amw-design-extract/SKILL.md) — sibling tool for token extraction (not structure).
- `../../bin/amw-dom-to-ir.py` — DOM-to-IR extractor (this skill's core backend).
- `../../bin/amw-parse-html-diagram.py` — inline-SVG extractor (called as subprocess by `dom-to-ir.py` for nested SVGs).
- `../../bin/amw-diagram-ir.py` — IR parse/emit/validate CLI.
- `../../bin/amw-validate-diagram.sh` — unified validator dispatcher.
- `../../bin/amw-dev-browser-wrapper.sh` — sanctioned browser automation wrapper.
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.

## Related commands

- `/amw-create-diagram-from-webpage` — primary entry point for this skill.
- `/amw-modify-diagram-of-webpage` — MVP: chains this skill (extract) with a user-edit pause, then `/amw-modify-webpage-from-diagram` on `apply`.
- `/amw-convert-any-diagram-format` — sibling when the user wants to continue converting the extracted IR beyond the initial target.
