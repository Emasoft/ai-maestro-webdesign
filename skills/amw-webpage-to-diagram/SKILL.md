---
name: amw-webpage-to-diagram
description: Extract the structural diagram of a webpage (URL or local `.html`) and emit it in a chosen format (ASCII / SVG / Mermaid — default ASCII). Triggers on narrow technical intents only — "extract diagram from webpage", "diagram this URL", "what's the structure of https://...", "sitemap from this HTML", "landmark diagram of this page", "/amw-create-diagram-from-webpage". Does NOT claim generic "design a page" / "build a landing page" vocabulary — those go to design-principles. Refuses every PNG input (file or URL returning image/*) per plugin directive.
version: 0.1.0
---

# Webpage to Diagram — DOM-to-IR extractor

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> **Format spec (authoritative):** `../amw-diagram-formats/references/html.md`.
> **IR schema:** `../amw-diagram-formats/references/ir-schema.md`.
> **Modify pipeline (for the re-emit leg):** `../amw-diagram-formats/references/modify-flow.md`.

This skill owns one direction of the webpage round-trip: **URL/HTML → IR → target format**. It is a specialization of `parse-html-diagram.py` — where that tool focuses on inline-`<svg>` diagrams, this skill treats the whole page as a structural graph: every HTML5 landmark (`<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<aside>`, `<header>`) becomes an IR node, every internal anchor link becomes an IR edge, and every nested `<svg>` diagram is attached as children of its containing landmark.

HTML-as-target is a no-op (already HTML) — the dispatcher skips it. PNG-as-target is reachable via the standard IR → SVG → rasterize chain in `diagram-convert`, but the typical ask is ASCII (for round-trip editing) or Mermaid (for embedding in markdown).

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

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| PNG refusal | Input file extension is `.png`, file magic bytes are PNG, OR URL HEAD returns `Content-Type: image/*` | Provide the source artifact (ASCII / HTML / SVG / Mermaid) that produced the PNG. No OCR, no best-effort workaround. |
| `dev-browser: command not found` | `/amw-init` hasn't been run | Run `/amw-init` to install dev-browser, OR let the skill fall back to urllib (pre-JS HTML only — SPA content may be missed). |
| Empty `nodes` in IR | Page has no HTML5 landmarks (div-soup site) | The parser emits a single `kind:"freeform"` node with the page title as label; target-format emission still succeeds, but downstream edits won't have landmark granularity. |
| URL 4xx / 5xx | Target page unreachable or auth-gated | Report the HTTP status verbatim; ask the user to supply a local `.html` export instead. |
| Validation FAIL on emitted ASCII | Downstream renderer produced misaligned output | Save the IR to `/tmp/amw-page-<hash>.json` for inspection; ask the user to rerun with `--target-kind flowchart` (less strict alignment). |

## Dependencies

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
- Inherits the three hard rules from `../amw-design-principles/SKILL.md` (context, variants, AI-slop refusal) whenever the downstream target is a design artifact (e.g. emitting ASCII for a `/amw-ascii-to-html` round-trip).

## Cross-references

- `../amw-diagram-formats/references/html.md` — authoritative HTML format spec (consumed via `bin/amw-parse-html-diagram.py` for nested SVGs).
- `../amw-diagram-formats/references/ir-schema.md` — IR schema produced by `bin/amw-dom-to-ir.py`.
- `../amw-diagram-formats/references/modify-flow.md` — shared 6-step pipeline consumed by the round-trip skills.
- `../amw-dev-browser/SKILL.md` — upstream page-capture primitive.
- `../amw-design-extract/SKILL.md` — sibling tool for token extraction (not structure).
- `../../bin/amw-dom-to-ir.py` — DOM-to-IR extractor (this skill's core backend).
- `../../bin/amw-parse-html-diagram.py` — inline-SVG extractor (called as subprocess by `dom-to-ir.py` for nested SVGs).
- `../../bin/amw-diagram-ir.py` — IR parse/emit/validate CLI.
- `../../bin/amw-validate-diagram.sh` — unified validator dispatcher.
- `../../bin/amw-dev-browser-wrapper.sh` — sanctioned browser automation wrapper.
- `../amw-design-principles/SKILL.md` — orchestrator.

## Related commands

- `/amw-create-diagram-from-webpage` — primary entry point for this skill.
- `/amw-modify-diagram-of-webpage` — MVP: chains this skill (extract) with a user-edit pause, then `/amw-modify-webpage-from-diagram` on `apply`.
- `/amw-convert-any-diagram-format` — sibling when the user wants to continue converting the extracted IR beyond the initial target.
