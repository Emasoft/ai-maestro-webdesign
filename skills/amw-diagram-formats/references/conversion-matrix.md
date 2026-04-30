# Conversion Matrix — 5 formats, N×N cells

**Authoritative dispatch table** consumed by `/amw-convert-any-diagram-format` and every `wd-create-or-modify-*-diagram` command that needs to normalize an incoming diagram to a specific format.

The 5 formats: `ASCII`, `HTML`, `SVG`, `Mermaid`, `PNG`. Per user directive 2026-04-22, **PNG is OUTPUT-ONLY**: every PNG-as-source cell is `impossible`, and the dispatcher refuses PNG inputs with a fixed message. PNG remains a valid TARGET for every other source.

Format specs referenced below:

- `./ascii.md` — ASCII format spec
- `./html.md` — HTML+inline-SVG format spec
- `./svg.md` — Standalone SVG format spec
- `./mermaid.md` — Mermaid grammar subset spec
- `./png.md` — PNG output-only pipelines

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
- **via IR** — parse source → IR → emit target. Lossy on styling details (colors, fonts, filters). Structure is preserved. See `./ir-schema.md` §5 for the lossy-conversion table.
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

See `./png.md` for the full rasterization pipeline spec, including DPI / background / padding options per backend.

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

**ASCII → HTML (direct)** — uses `../../amw-ascii-to-html/SKILL.md` machinery + design-principles starter-components. Output is a full responsive `.html`, not a `<pre>` embed. See `./html.md`.

**ASCII → SVG (direct)** — uses `../../amw-ascii-to-svg/SKILL.md` + `bin/amw-ascii-parse.py` to tokenize, then `bin/amw-svg-render.py` to emit SVG primitives. See `./svg.md`.

**ASCII → Mermaid (via IR)** — lossy. ASCII positional information (exact cell coordinates) is dropped; the IR carries the node+edge graph, and the Mermaid emitter lays out via `flowchart TD` auto-layout. Users with position-critical ASCII should route ASCII → SVG (which preserves positions).

**HTML → ASCII / SVG / Mermaid (via IR / direct)** — HTML parsing extracts the inline `<svg>` if present (direct HTML → SVG); otherwise it walks the DOM structure (via IR). Styling (CSS) is always dropped. Phase 1's `bin/amw-parse-html-diagram.py` replaces the raw-source stub with proper structural extraction.

**SVG → ASCII (via IR)** — geometric interpretation: `<rect>` → nodes, `<line>` / `<path>` + `<marker>` → edges. Heuristic. Best-effort. Users with dense SVGs should treat this as a starting draft.

**SVG → HTML (wrap)** — one-step: wrap the SVG in a minimal HTML document with `<!DOCTYPE html><html><body>{svg}</body></html>`. No styling transformation. Use `./html.md` starter-components for production HTML.

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

- `./ir-schema.md` — IR shape, versioning, lossy-conversion table.
- `./modify-flow.md` — shared detect → parse → patch → emit → validate pipeline. Conversion is a degenerate modify-flow.
- `./detect-format.md` — format sniffer rules.
- `./validation-dispatcher.md` — unified validator contract (every conversion ends with validation).
