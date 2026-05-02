## Table of Contents

- [1. PNG is OUTPUT-ONLY — why](#1-png-is-output-only-why)
  - [1.1 Refusal messages (verbatim)](#11-refusal-messages-verbatim)
- [2. Rasterization pipelines (per source format → PNG)](#2-rasterization-pipelines-per-source-format-png)
  - [2.1 SVG → PNG (via cairosvg)](#21-svg-png-via-cairosvg)
  - [2.2 HTML → PNG (via Playwright screenshot)](#22-html-png-via-playwright-screenshot)
  - [2.3 ASCII → PNG (two-step: ASCII → SVG → PNG)](#23-ascii-png-two-step-ascii-svg-png)
  - [2.4 Mermaid → PNG (direct via `mmdc -t png` OR via SVG)](#24-mermaid-png-direct-via-mmdc-t-png-or-via-svg)
  - [2.5 Hand-drawn-style PNG (via `excalidraw-illustrations`)](#25-hand-drawn-style-png-via-excalidraw-illustrations)
- [3. Refusal path implementation](#3-refusal-path-implementation)
  - [3.1 `bin/amw-diagram-detect-format.sh`](#31-binamw-diagram-detect-formatsh)
  - [3.2 `bin/amw-validate-diagram.sh` — PNG branch](#32-binamw-validate-diagramsh-png-branch)
  - [3.3 Conversion dispatcher](#33-conversion-dispatcher)
- [4. Per-source technique catalog](#4-per-source-technique-catalog)
  - [S1 — bin/amw-svg-render.py + cairosvg](#s1-binamw-svg-renderpy-cairosvg)
  - [S2 — bin/amw-html-export.py + Playwright](#s2-binamw-html-exportpy-playwright)
  - [S3 — bin/amw-mermaid-render.sh + beautiful-mermaid + mmdc](#s3-binamw-mermaid-rendersh-beautiful-mermaid-mmdc)
  - [S4 — Hand-drawn (excalidraw-illustrations)](#s4-hand-drawn-excalidraw-illustrations)
- [5. PNG as INPUT is refused — the full story](#5-png-as-input-is-refused-the-full-story)
  - [5.1 Format detection (`bin/amw-diagram-detect-format.sh`)](#51-format-detection-binamw-diagram-detect-formatsh)
  - [5.2 Per-command refusal](#52-per-command-refusal)
  - [5.3 No OCR, no vision-model retry](#53-no-ocr-no-vision-model-retry)
- [6. Failure modes](#6-failure-modes)


# PNG — canonical format reference (OUTPUT-ONLY)

> **⚠️ USER DIRECTIVE (2026-04-22): PNG is OUTPUT-ONLY.**
>
> **PNG is never a valid INPUT to any plugin operation.** The conversion matrix, validators, compare, and webpage-round-trip commands all REFUSE PNG-as-source with a fixed error message: *"PNG is output-only by user directive — re-authoring required from source artifact. Provide the ASCII/HTML/SVG/Mermaid source instead."*
>
> This file documents how each source format **rasterizes TO** PNG, and explicitly documents the refusal of PNG as input.

**Consumers (cross-references):**
- `../../amw-excalidraw-illustrations/SKILL.md` — hand-drawn-style PNG via Gemini API (GATED, cost-consent required)
- `../../amw-infographics/SKILL.md` — HTML → PNG/PDF producer (Playwright screenshot)
- `../../amw-hyperframes-bridge/SKILL.md` — HTML → MP4 (uses same Playwright stack)
- `../../bin/amw-html-export.py` — HTML → PNG via Playwright screenshot
- `../../bin/amw-svg-render.py` — SVG → PNG via cairosvg
- `../../bin/amw-mermaid-render.sh` — Mermaid → SVG then → PNG
- `../../bin/amw-validate-diagram.sh` (planned; Task 0c) — unified validator dispatcher, PNG branch = hardcoded refusal
- [conversion-matrix](./conversion-matrix.md) — PNG-input row = all `impossible`
- [validation-dispatcher](./validation-dispatcher.md) — PNG branch = fixed-message refusal

---

## 1. PNG is OUTPUT-ONLY — why

1. **Round-tripping PNG loses source semantics.** OCR + vision-model interpretation is neither deterministic nor structure-preserving. Re-authoring from a PNG produces a fabricated IR that doesn't match the original source's node IDs, labels, or styling.
2. **The plugin has a better path.** Every PNG emitted by the plugin is produced from an ASCII / HTML / SVG / Mermaid source. That source is the canonical artifact. Ask the user to supply it instead.
3. **Refusal is predictable.** A fixed refusal message is a cleaner UX than "I'll try OCR but it might be wrong" — users know exactly why the operation stopped and what to do.

### 1.1 Refusal messages (verbatim)

Emitted by `bin/amw-validate-diagram.sh`, `bin/amw-diagram-detect-format.sh`, and the conversion / compare commands:

| Context | Exact message |
|---|---|
| `amw-convert-any-diagram-format <file.png> --to X` | *"PNG is output-only by user directive — re-authoring required from source artifact. Provide the ASCII/HTML/SVG/Mermaid source instead."* |
| `amw-validate-any-diagram-format <file.png>` | *"PNG is output-only; validate the source artifact instead."* |
| `amw-compare-diagrams` with a PNG operand | *"PNG is output-only; compare the source artifacts instead."* |
| `amw-modify-diagram-of-webpage` finds `<img src="*.png">` inside the page | *"The webpage's diagram is embedded as PNG. PNG is output-only; please provide the source artifact (ASCII/HTML/SVG/Mermaid) that produced this PNG."* |

---

## 2. Rasterization pipelines (per source format → PNG)

### 2.1 SVG → PNG (via cairosvg)

**Already available** — `cairosvg` auto-installs via `bin/amw-svg-render.py` on first use; also declared by `/amw-init`.

```python
import cairosvg
cairosvg.svg2png(url="diagram.svg", write_to="diagram.png",
                 output_width=1920, dpi=96)
```

Wrapper: `../../bin/amw-svg-render.py render <file>` rasterizes to PNG in the plugin state dir. `finish <file>` finalizes and refuses if `render` was never called (see [svg](./svg.md) §5).

**Dimension guidance**:
- Icon PNG: `output_width=256` (from 24×24 viewBox, 10.7× upscale)
- Logo PNG: `output_width=1024` (from 64×64 or 200×200 viewBox)
- Diagram PNG (freeform / architecture): `output_width=1920`
- Editorial / slide PNG: `output_width=1920` @ `dpi=96` or `output_width=3840` @ `dpi=192` (retina)

### 2.2 HTML → PNG (via Playwright screenshot)

Already used by `infographics/` — `../../bin/amw-html-export.py` wraps Playwright:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1440})
    page.goto(f"file://{abs_path}")
    page.screenshot(path="diagram.png", full_page=True)
    browser.close()
```

**Dimension guidance**:
- Slide (16:9): `viewport=1920×1080`, `full_page=False`
- Editorial poster (portrait): `viewport=1080×1440`, `full_page=True`
- Dashboard / full-page HTML: `viewport=1920×1200`, `full_page=True`
- Retina: append `device_scale_factor=2` to viewport config

### 2.3 ASCII → PNG (two-step: ASCII → SVG → PNG)

There is no direct ASCII → PNG path. Chain through SVG:

```bash
# Step 1: ASCII → SVG
/amw-ascii-to-svg path/to/diagram.txt
# → writes /tmp/amw-ascii-<slug>-out.svg

# Step 2: SVG → PNG
python3 bin/amw-svg-render.py render /tmp/amw-ascii-<slug>-out.svg
# → writes PNG next to the SVG
```

**Dimension guidance**: ASCII diagrams typically fit in 800×600 at 1× scale; for PR embedding bump to 1600×1200.

### 2.4 Mermaid → PNG (direct via `mmdc -t png` OR via SVG)

**Direct**:

```bash
mmdc -i diagram.mmd -o diagram.png -t default
```

**Themed (via plugin wrapper → SVG → cairosvg, preserves the 15 built-in themes)**:

```bash
bin/amw-mermaid-render.sh --input diagram.mmd --format svg \
  --theme tokyo-night --out /tmp/x.svg
python3 -c "import cairosvg; cairosvg.svg2png(url='/tmp/x.svg', write_to='diagram.png', output_width=1920)"
```

**Dimension guidance**: `mmdc -w 1920 -H auto` for wide aspect; use the SVG → cairosvg path when brand theme matters.

### 2.5 Hand-drawn-style PNG (via `excalidraw-illustrations`)

GATED behind a cost-consent prompt (Gemini API cost per call). Not a rasterization of plugin-owned source; it's a Gemini image generation.

```bash
# Requires $GEMINI_API_KEY; emits single .png
```

See `../../amw-excalidraw-illustrations/SKILL.md` for the full protocol and cost-consent contract.

---

## 3. Refusal path implementation

### 3.1 `bin/amw-diagram-detect-format.sh`

Recognizes `.png` extension + PNG magic bytes (`89 50 4E 47 0D 0A 1A 0A`). Returns format `png`.

### 3.2 `bin/amw-validate-diagram.sh` — PNG branch

Hardcoded:

```bash
if [[ "$format" == "png" ]]; then
  echo "FAIL: PNG is output-only; validate the source artifact instead." >&2
  exit 2
fi
```

### 3.3 Conversion dispatcher

In [conversion-matrix](./conversion-matrix.md), every PNG-row cell is `impossible`. The dispatcher:

```bash
if [[ "$from" == "png" ]]; then
  echo "PNG is output-only by user directive — re-authoring required from source artifact." >&2
  echo "Provide the ASCII/HTML/SVG/Mermaid source instead." >&2
  exit 2
fi
```

---

## 4. Per-source technique catalog

Format: `TECH-PN-NN <name>: <description> | source: <path>:<section> | applies-to: <use-case>`

### S1 — bin/amw-svg-render.py + cairosvg

TECH-PN-01 cairosvg-svg2png-basic: `cairosvg.svg2png(url=..., write_to=..., output_width=W, dpi=D)` | source: bin/amw-svg-render.py wrapper | applies-to: every SVG → PNG step
TECH-PN-02 cairosvg-auto-install: bin/amw-svg-render.py pip-installs cairosvg on first call; /amw-init pre-installs | source: bin/amw-svg-render.py runtime | applies-to: cold-clone bootstrap
TECH-PN-03 render-verify-finish-guard: `finish` subcommand REFUSES if `render` was never called — forces visual inspection before delivery | source: bin/amw-svg-render.py subcommands | applies-to: every SVG-producing skill
TECH-PN-04 output-width-upscale-icon: icon viewBox 24×24 → PNG 256×256 (10.7× upscale produces crisp screen-ready PNG) | source: svg-creator scope | applies-to: icon exports

### S2 — bin/amw-html-export.py + Playwright

TECH-PN-05 playwright-screenshot-full-page: `page.screenshot(path=..., full_page=True)` captures scrolling content | source: bin/amw-html-export.py | applies-to: long dashboards, infographics, editorial posters
TECH-PN-06 playwright-viewport-1920-1080: slide default `viewport=1920×1080`, no scroll; `full_page=False` | source: bin/amw-html-export.py | applies-to: slides / presentations
TECH-PN-07 playwright-retina-2x: `device_scale_factor=2` doubles pixel density for retina display | source: bin/amw-html-export.py | applies-to: high-DPI exports
TECH-PN-08 file-url-scheme: Playwright needs `file://<absolute-path>` for local HTML | source: bin/amw-html-export.py | applies-to: local HTML rasterization

### S3 — bin/amw-mermaid-render.sh + beautiful-mermaid + mmdc

TECH-PN-09 mmdc-direct-png: `mmdc -i x.mmd -o x.png -t default` emits PNG without SVG intermediate | source: mmdc CLI docs | applies-to: quick-path PNG when default theme is OK
TECH-PN-10 themed-mermaid-via-svg: beautiful-mermaid → SVG → cairosvg preserves the 15 themes | source: skills/amw-mermaid-render/SKILL.md 5.1-5.2 | applies-to: brand-themed PNG

### S4 — Hand-drawn (excalidraw-illustrations)

TECH-PN-11 gemini-cost-consent: excalidraw-illustrations prompts for per-call cost consent before invoking Gemini | source: excalidraw-illustrations/SKILL.md | applies-to: every Gemini-API PNG call
TECH-PN-12 gemini-key-required: `$GEMINI_API_KEY` env var required; /amw-doctor verifies presence | source: excalidraw-illustrations/SKILL.md | applies-to: gate check before attempting render

Total: **12 techniques**, 4 sources.

---

## 5. PNG as INPUT is refused — the full story

The refusal is enforced at THREE layers:

### 5.1 Format detection (`bin/amw-diagram-detect-format.sh`)

Returns `png` for PNG-extension + magic-byte match. All downstream dispatchers see `png` and route to their refusal branch.

### 5.2 Per-command refusal

| Command | Behavior on PNG input |
|---|---|
| `amw-convert-any-diagram-format` | Refuse, exit 2 |
| `amw-validate-any-diagram-format` | Refuse, exit 2 |
| `amw-compare-diagrams` | Refuse if EITHER operand is PNG, exit 2 |
| `amw-modify-diagram-of-webpage` | Refuse if the page's diagram is `<img src="*.png">` or `data:image/png;base64`, exit 2 |
| `amw-create-diagram-from-webpage` | No PNG-check needed (output only); a page with PNG-embedded diagrams just won't extract anything useful — refuse upstream via `amw-modify-diagram-of-webpage` |
| `wd-create-or-modify-*` | `.png` path → refuse, exit 2 (PNG is never a valid "existing diagram" to edit) |

### 5.3 No OCR, no vision-model retry

The dispatcher NEVER falls back to OCR or vision-model interpretation. The refusal is intentional — it guards against fabricated IR that doesn't match the original source's structure. Tell the user to supply the source artifact.

---

## 6. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| PNG rendered looks blocky | `output_width` too low for target display | Bump `output_width` or add `dpi=192` |
| Playwright screenshot cuts off content | `full_page=False` with overflowing content | Set `full_page=True` |
| Mermaid PNG wrong theme | `mmdc -t png` uses default theme | Use the SVG → cairosvg path with `bin/amw-mermaid-render.sh --theme ...` |
| Gemini PNG refuses | `$GEMINI_API_KEY` missing | Set env var; `/amw-doctor` flags this |
| User supplies a PNG asking to edit | Expected refusal | Show the refusal message; ask for source artifact |
