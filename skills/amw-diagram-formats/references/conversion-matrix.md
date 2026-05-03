## Table of Contents

- [1. Full N×N table](#1-full-nn-table)
- [2. Cell semantics](#2-cell-semantics)
- [3. PNG-as-source refusal (mandatory)](#3-png-as-source-refusal-mandatory)
- [4. PNG-as-target pipelines (all supported)](#4-png-as-target-pipelines-all-supported)
- [5. Dispatch algorithm](#5-dispatch-algorithm)
- [6. Per-cell implementation notes](#6-per-cell-implementation-notes)
- [7. Tools index (required backends)](#7-tools-index-required-backends)
- [8. Related references](#8-related-references)


# Conversion Matrix — 5 formats, N×N cells

**Authoritative dispatch table** consumed by `/amw-convert-any-diagram-format` and every `wd-create-or-modify-*-diagram` command that needs to normalize an incoming diagram to a specific format.

The 5 formats: `ASCII`, `HTML`, `SVG`, `Mermaid`, `PNG`. Per user directive 2026-04-22, **PNG is OUTPUT-ONLY**: every PNG-as-source cell is `impossible`, and the dispatcher refuses PNG inputs with a fixed message. PNG remains a valid TARGET for every other source.

Format specs referenced below:

- [ascii](./ascii.md) — ASCII format spec
  > Format definition · Dimensional constraints · Parse rules · Emission rules · Validation rules · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · SKILL · SKILL · SKILL · SKILL · SKILL · SKILL · `../../text-visual-{workflows,arch,state,cheatsheets,retro}/SKILL.md` — specialized ASCII archetypes · `../../bin/amw-ascii-parse.py` — tokenizer (IR input) · `../../bin/amw-ascii-render.py` — renderer (4 JSON modes) · `../../bin/amw-validate-ascii.py` — validator (Perl, mandatory gate) · `../../bin/amw-validate-ascii.py` — validator (Python mirror) · ir-schema · conversion-matrix · modify-flow · validation-dispatcher
  > Format definition · 1 Character repertoire · 2 Forbidden characters (validator rejects) · 3 State / status markers · Dimensional constraints · Parse rules · Emission rules · 1 Four JSON modes · 2 Key renderer invariants · Validation rules · 1 Checks · 2 Validation is MANDATORY before delivery · Per-source breakdown of the technique catalog · Technique catalog · S1 — box-diagram-master (gold examples) · S2 — ascii-diagrams-skill (CHI'24 refs, 7 files) · S3 — cc-plugin-text-visualizations (5 skills) · S4 — perfect-ascii (renderer) · S5 — diagram-skill styles (ASCII-STYLES.md) · S6 — baybee-diagram (SVG patterns with ASCII equivalents) · S7 — diagram-design-editorial (editorial) · S8 — Structural pairing rules (enforced by validator) · S9 — Cross-cutting style rules · Migration note (2026-04-22) · SKILL · SKILL · SKILL · SKILL · SKILL · SKILL · …(+9)
- [html](./html.md) — HTML+inline-SVG format spec
  > Format definition · 1 File structure (baseline) · 2 Semantic-HTML requirements · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · 1 Listener-before-announce · 2 Partial-keys only · 3 Valid JSON EDITMODE block · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · S1 — design-principles starter-components (canonical chrome) · S2 — ai-slop-avoid (output-ban gate) · S3 — ui-ux-pro-max-skill (industry patterns) · S4 — ux-designer + accessibility · S5 — create-infographics (editorial density) · S6 — diagram-design-editorial (self-contained HTML+SVG) · S7 — ascii-creator mirror (pattern recognition) · S8 — CHI'24 ASCII classics (mockup → HTML skeleton) · S9 — ascii-parse.py (in-repo tokenizer hooks) · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · …(+9)
- [svg](./svg.md) — Standalone SVG format spec
  > Format definition · 1 Non-negotiables · 2 Allowed primitives · 3 Forbidden primitives · Structural primitives (diagram-grade usage) · 1 Node shapes by type · 2 Edges · Viewport rules · 1 Canonical viewBoxes · 2 `preserveAspectRatio` · 3 Responsive sizing · 4 Margin reserves · Text rendering rules · 1 Font stack · 2 Centering · 3 Long labels · Rasterization path · 1 SVG → PNG via cairosvg · 2 Filter compatibility with cairosvg · 3 SMIL in rasterized output · Validation · 1 Check list · 2 Output contract · 3 Render-verify as final gate · Per-source breakdown of the technique catalog · Technique catalog · S1 — svg-creator filter cookbook · S2 — diagram-svg + baybee-diagram · S3 — animations (SMIL + CSS) · S4 — diagram-design-editorial · …(+14)
- [mermaid](./mermaid.md) — Mermaid grammar subset spec
  > Format definition · Supported grammars · Themes · mmdc CLI flags (17 total) · Output paths · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · Anti-patterns · SKILL · SKILL · SKILL · `../../external/mermaid-render/` — vendored beautiful-mermaid backend · `../../bin/amw-mermaid-render.sh` — shell wrapper (SVG / PNG / ASCII) · `../../bin/amw-mermaid-lint.sh` (planned; Task 0c) — validator wrapper (`mmdc` dry-run) · `../../bin/amw-validate-ascii.py` — warn-only gate on ASCII rendering · ir-schema · conversion-matrix · validation-dispatcher
  > Format definition · 1 File conventions · 2 Minimal example · Supported grammars · 1 Node shapes (flowchart) · 2 Edges (flowchart) · Themes · 1 Built-in themes (15) · 2 Theme-selection guide · 3 Mono Mode (2-color derivation) · 4 7-color enriched palette · 5 Live theme-switching (browser) · mmdc CLI flags (17 total) · Output paths · 1 Mermaid → SVG (default, high fidelity) · 2 Mermaid → PNG (via `mmdc -t png`) · 3 Mermaid → ASCII (Unicode default) · 4 Mermaid → pure ASCII (README-safe) · 5 Batch rendering (parallel) · Validation · 1 Dry-run linting · 2 Common validation failures · Per-source breakdown of the technique catalog · Technique catalog · S1 — beautiful-mermaid (backend) · S2 — Pretty-mermaid + mermaid-render/SKILL.md (CLI) · S3 — Mermaid grammar · S4 — agent-skill-diagramming-flows · S5 — bin/amw-mermaid-render.sh wrapper · Failure modes · …(+11)
- [png](./png.md) — PNG output-only pipelines
  > PNG is OUTPUT-ONLY — why · 1 Refusal messages (verbatim) · Rasterization pipelines (per source format → PNG) · 1 SVG → PNG (via cairosvg) · 2 HTML → PNG (via Playwright screenshot) · 3 ASCII → PNG (two-step: ASCII → SVG → PNG) · 4 Mermaid → PNG (direct via `mmdc -t png` OR via SVG) · 5 Hand-drawn-style PNG (via `excalidraw-illustrations`) · Refusal path implementation · 1 `bin/amw-diagram-detect-format.sh` · 2 `bin/amw-validate-diagram.sh` — PNG branch · 3 Conversion dispatcher · Per-source technique catalog · S1 — bin/amw-svg-render.py + cairosvg · S2 — bin/amw-html-export.py + Playwright · S3 — bin/amw-mermaid-render.sh + beautiful-mermaid + mmdc · S4 — Hand-drawn (excalidraw-illustrations) · PNG as INPUT is refused — the full story · 1 Format detection (`bin/amw-diagram-detect-format.sh`) · 2 Per-command refusal · 3 No OCR, no vision-model retry · Failure modes · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG via Playwright screenshot · `../../bin/amw-svg-render.py` — SVG → PNG via cairosvg · `../../bin/amw-mermaid-render.sh` — Mermaid → SVG then → PNG · `../../bin/amw-validate-diagram.sh` (planned; Task 0c) — unified validator dispatcher, PNG branch = hardcoded refusal · conversion-matrix · …(+1)

## 1. Full N×N table

| From \ To | ASCII | HTML | SVG | Mermaid | PNG |
|---|---|---|---|---|---|
| **ASCII** | — | direct (`ascii-to-html`) | direct (`ascii-to-svg`) | via IR (manual layout → mermaid; lossy on positions) | direct (ASCII → SVG via `ascii-to-svg`, then rasterize via `bin/amw-svg-render.py` / cairosvg) |
| **HTML** | via IR (parse inline SVG → IR → ASCII; lossy on styling) | — | direct (`bin/amw-parse-html-diagram.py` extracts SVG; wrap / strip CSS) | via IR (lossy; extract graph structure only) | direct (Playwright screenshot via `bin/amw-html-export.py`) |
| **SVG** | via IR (SVG → IR → ASCII via `bin/amw-ascii-render.py`; lossy) | wrap (SVG embedded in minimal HTML wrapper) | — | via IR (lossy; rebuild as mermaid text) | direct (cairosvg or `bin/amw-svg-render.py --png`) |
| **Mermaid** | direct (`bin/amw-mermaid-render.sh --ascii`) | via SVG then wrap | direct (`bin/amw-mermaid-render.sh --svg`) | — | direct (`mmdc -i x.mmd -o x.png` or render to SVG then cairosvg) |
| **PNG** | impossible (user directive — PNG is output-only) | impossible (same) | impossible (same) | impossible (same) | — |

## 2. Cell semantics

Three label types appear in the cells above. Their semantics are:

- **direct** — a one-step pipeline, already plumbed or a trivial wrapper. No IR needed. Fastest path, best fidelity.
- **via IR** — parse source → IR → emit target. Lossy on styling details (colors, fonts, filters). Structure is preserved. See [ir-schema](./ir-schema.md) §5 for the lossy-conversion table.
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
- **via SVG** / **via HTML** — a two-step chain through an existing `direct` cell. Combines two direct pipelines.
- **wrap** — a trivial transform (e.g. SVG embedded in `<html><body>`). No semantic transformation.
- **impossible** — not supported. PNG-as-source cells all take this path by user directive.

## 3. PNG-as-source refusal (mandatory)

When the dispatcher detects a PNG input, it MUST refuse with this exact message:

```
PNG is output-only by plugin directive — re-authoring required from source artifact.
Provide the ASCII / HTML / SVG / Mermaid source instead.
```

The refusal is implemented in `bin/amw-validate-diagram.sh` (exit code 2) and MUST be mirrored in `/amw-convert-any-diagram-format`, `/amw-compare-diagrams`, and every skill that dispatches through this matrix. No OCR fallback, no "best-effort" re-interpretation.

Detection: PNG magic bytes (`\x89PNG\r\n\x1a\n`) + `.png` extension. Either signal alone triggers refusal — a file named `.txt` that starts with PNG magic is still refused.

## 4. PNG-as-target pipelines (all supported)

Every non-PNG source has a `direct` cell for PNG emission. The canonical pipelines:

| Source | Pipeline to PNG |
|---|---|
| ASCII | `bin/amw-ascii-parse.py` → `bin/amw-ascii-render.py` → ASCII → `bin/amw-svg-render.py --png` (SVG rasterization via cairosvg) |
| HTML | `bin/amw-html-export.py` (Playwright / Chromium headless screenshot) |
| SVG | `bin/amw-svg-render.py --png` (cairosvg rasterization) |
| Mermaid | `mmdc -i x.mmd -o x.png` (mermaid-cli built-in PNG output) |

Every pipeline respects the target file extension (`.png`) and is idempotent. Re-running on the same input overwrites the output byte-for-byte.

See [png](./png.md) for the full rasterization pipeline spec, including DPI / background / padding options per backend.
> [png.md] PNG is OUTPUT-ONLY — why · 1 Refusal messages (verbatim) · Rasterization pipelines (per source format → PNG) · 1 SVG → PNG (via cairosvg) · 2 HTML → PNG (via Playwright screenshot) · 3 ASCII → PNG (two-step: ASCII → SVG → PNG) · 4 Mermaid → PNG (direct via `mmdc -t png` OR via SVG) · 5 Hand-drawn-style PNG (via `excalidraw-illustrations`) · Refusal path implementation · 1 `bin/amw-diagram-detect-format.sh` · 2 `bin/amw-validate-diagram.sh` — PNG branch · 3 Conversion dispatcher · Per-source technique catalog · S1 — bin/amw-svg-render.py + cairosvg · S2 — bin/amw-html-export.py + Playwright · S3 — bin/amw-mermaid-render.sh + beautiful-mermaid + mmdc · S4 — Hand-drawn (excalidraw-illustrations) · PNG as INPUT is refused — the full story · 1 Format detection (`bin/amw-diagram-detect-format.sh`) · 2 Per-command refusal · 3 No OCR, no vision-model retry · Failure modes · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG via Playwright screenshot · `../../bin/amw-svg-render.py` — SVG → PNG via cairosvg · `../../bin/amw-mermaid-render.sh` — Mermaid → SVG then → PNG · `../../bin/amw-validate-diagram.sh` (planned; Task 0c) — unified validator dispatcher, PNG branch = hardcoded refusal · conversion-matrix · …(+1)

## 5. Dispatch algorithm

The algorithm consumed by `/amw-convert-any-diagram-format`:

```
1. detect-format(src_path) → src_fmt                        (see ./detect-format.md)
2. If src_fmt == "png":
     emit REFUSE message (§3) and exit 2.
3. If target_fmt not in {ascii, html, svg, mermaid, png}:
     error: unknown target format.
4. If src_fmt == target_fmt:
     return identity copy (no transformation).
5. Look up (src_fmt, target_fmt) in the matrix.
6. If "direct":
     run the named tool with (src, tgt) paths. Done.
7. If "via IR":
     bin/amw-diagram-ir.py parse --in src --out /tmp/<hash>.ir.json
     bin/amw-diagram-ir.py emit  --in /tmp/<hash>.ir.json --format <target> --out tgt
8. If "via X":
     first-step: convert(src, X) → /tmp/<hash>.<X>
     second-step: convert(/tmp/<hash>.<X>, target) → tgt
9. Validate target via bin/amw-validate-diagram.sh tgt. Fail the whole op if validation fails.
```

Round-tripping through `via IR` chains is ALLOWED but lossy. The dispatcher logs each intermediate file so the user can inspect.

## 6. Per-cell implementation notes

**ASCII → HTML (direct)** — uses [SKILL](../../amw-ascii-to-html/SKILL.md) machinery + design-principles starter-components. Output is a full responsive `.html`, not a `<pre>` embed. See [html](./html.md).
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG/PDF rasterizer (Playwright) · `../../bin/amw-ascii-parse.py` — ASCII → layout JSON consumed by HTML emitter · ir-schema · conversion-matrix · modify-flow · validation-dispatcher

**ASCII → SVG (direct)** — uses [SKILL](../../amw-ascii-to-svg/SKILL.md) + `bin/amw-ascii-parse.py` to tokenize, then `bin/amw-svg-render.py` to emit SVG primitives. See [svg](./svg.md).
> [svg.md] Format definition · Structural primitives (diagram-grade usage) · Viewport rules · Text rendering rules · Rasterization path · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · SKILL · SKILL · SKILL · SKILL · SKILL · advanced-techniques · `../../bin/amw-svg-render.py` — render-verify-finish loop (`render` / `finish` / `status` / `reset`) · ir-schema · conversion-matrix · png · validation-dispatcher

**ASCII → Mermaid (via IR)** — lossy. ASCII positional information (exact cell coordinates) is dropped; the IR carries the node+edge graph, and the Mermaid emitter lays out via `flowchart TD` auto-layout. Users with position-critical ASCII should route ASCII → SVG (which preserves positions).

**HTML → ASCII / SVG / Mermaid (via IR / direct)** — HTML parsing extracts the inline `<svg>` if present (direct HTML → SVG); otherwise it walks the DOM structure (via IR). Styling (CSS) is always dropped. Phase 1's `bin/amw-parse-html-diagram.py` replaces the raw-source stub with proper structural extraction.

**SVG → ASCII (via IR)** — geometric interpretation: `<rect>` → nodes, `<line>` / `<path>` + `<marker>` → edges. Heuristic. Best-effort. Users with dense SVGs should treat this as a starting draft.

**SVG → HTML (wrap)** — one-step: wrap the SVG in a minimal HTML document with `<!DOCTYPE html><html><body>{svg}</body></html>`. No styling transformation. Use [html](./html.md) starter-components for production HTML.
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG/PDF rasterizer (Playwright) · `../../bin/amw-ascii-parse.py` — ASCII → layout JSON consumed by HTML emitter · ir-schema · conversion-matrix · modify-flow · validation-dispatcher

**Mermaid → ASCII / SVG (direct)** — `bin/amw-mermaid-render.sh` already supports both. The `--ascii` flag uses the vendored `beautiful-mermaid` backend's ASCII renderer.

**X → PNG (direct)** — see §4.

## 7. Tools index (required backends)

| Tool | Purpose | Installed via |
|---|---|---|
| `bin/amw-ascii-parse.py` | ASCII → structured JSON | ships with plugin |
| `bin/amw-ascii-render.py` | JSON → ASCII | ships with plugin |
| `bin/amw-svg-render.py` | SVG → PNG / preview | ships with plugin (needs `cairosvg`) |
| `bin/amw-html-export.py` | HTML → PNG / PDF | ships with plugin (needs `playwright`) |
| `bin/amw-mermaid-render.sh` | Mermaid → SVG / ASCII / PNG | ships with plugin (needs `mmdc` + `beautiful-mermaid`) |
| `bin/amw-parse-html-diagram.py` | HTML → IR | Phase 1 (Task 1a) |
| `bin/amw-parse-svg-diagram.py` | SVG → IR | Phase 1 (Task 1b) |
| `bin/amw-parse-mermaid-diagram.py` | Mermaid → IR | Phase 1 (Task 1c) |
| `bin/amw-diagram-ir.py` | IR parse / emit / validate / diff | ships with plugin |
| `bin/amw-diagram-detect-format.sh` | Format sniffer | ships with plugin |
| `bin/amw-validate-diagram.sh` | Top-level validator | ships with plugin |

`xmllint`, `tidy`, `mmdc`, `cairosvg`, `playwright` are user-installed via `/amw-init`; `/amw-doctor` reports status.

## 8. Related references

- [ir-schema](./ir-schema.md) — IR shape, versioning, lossy-conversion table.
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
- [modify-flow](./modify-flow.md) — shared detect → parse → patch → emit → validate pipeline. Conversion is a degenerate modify-flow.
  > The pipeline · Create vs modify dispatch · Step-by-step detail · Step 1 — Detect · Step 2 — Parse to IR · Step 3 — Patch · Step 4 — (loop point) · Step 5 — Emit · Step 6 — Re-validate · Work directory and file naming · Per-format guidance · 1 ASCII modify (MVP structural) · 2 HTML modify (MVP raw-source; Phase 1 structural) · 3 SVG modify (MVP raw-source; Phase 1 structural) · 4 Mermaid modify (MVP raw-source; Phase 1 structural) · Conversion is a modify-flow variant · Composition with round-trip skills · 1 `diagram-webpage-sync` (`/amw-modify-webpage-from-diagram`) · 2 `webpage-to-diagram` (`/amw-modify-diagram-of-webpage`) · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
- [detect-format](./detect-format.md) — format sniffer rules.
  > Contract · Decision tree (precedence top-down) · Content sniff window · Corner cases (by example) · 1 Mermaid-in-markdown · 2 HTML with inline `<svg>` · 3 SVG served as XHTML · 4 ASCII with a Mermaid-looking first line · 5 `.txt` wireframe without box-drawing · 6 PNG with a non-`.png` extension · 7 Empty file · Known limitations · Callers · When to extend this
- [validation-dispatcher](./validation-dispatcher.md) — unified validator contract (every conversion ends with validation).
  > Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · 1 ASCII — `bin/amw-validate-ascii.py` (primary) and `bin/amw-validate-ascii.py` (fallback) · 2 SVG — `bin/amw-validate-svg-diagram.sh` · 3 HTML — `bin/amw-validate-html-diagram.sh` · 4 Mermaid — `bin/amw-mermaid-lint.sh` · Caller integration patterns · 1 Post-create gate · 2 Post-convert gate · 3 Modify-flow loop · 4 Multi-format mode (ascii-validator) · Known limitations (Phase 0) · Related references
