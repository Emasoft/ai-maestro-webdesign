---
name: TECH-export-pipeline
category: infographic-export
source: image-generation/create-infographics/scripts/export.py
also-in: image-generation/create-infographics/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Install](#install)
- [Basic invocation](#basic-invocation)
- [With local server (recommended)](#with-local-server-recommended)
- [Width and scale](#width-and-scale)
- [Per-platform widths](#per-platform-widths)
- [Wait-for-render helper](#wait-for-render-helper)
- [SVG export](#svg-export)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Export pipeline — HTML → PNG + PDF + SVG

## What it does

`scripts/export.py` converts the final HTML infographic to PNG
(retina), PDF, and optionally SVG using Playwright + Chromium. The
script spins up a local HTTP server so CDN fonts load correctly.

## When to use

- Final delivery step after the HTML is approved.
- Batch export for multiple formats (PNG for social, PDF for print).
- Platform-specific sizing (Twitter 1200×675, Instagram 1080×1080).

## Install

```bash
# source: image-generation/create-infographics/SKILL.md
pip install playwright --break-system-packages -q
playwright install chromium --with-deps
```

## Basic invocation

```bash
# PNG
python scripts/export.py --input infographic.html --output infographic.png --format png

# PDF
python scripts/export.py --input infographic.html --output infographic.pdf --format pdf

# All formats
python scripts/export.py --input infographic.html --output infographic --format all
```

## With local server (recommended)

```bash
python scripts/export.py --input infographic.html --output infographic --format all --serve
```

The `--serve` flag spins up a local HTTP server on port 8765 so
Google Fonts and Phosphor Icons CDNs load correctly. Without it,
`file://` requests may fail for external resources.

## Width and scale

```bash
python scripts/export.py --input x.html --output x --width 1200 --scale 2
```

- `--width` — canvas width in pixels (must match the HTML's canvas
  width).
- `--scale 2` — retina export. Doubles the pixel count.

## Per-platform widths

| Platform | `--width` |
|----------|-----------|
| Twitter/X card | 1200 |
| Twitter/X portrait | 1080 |
| Instagram post / story | 1080 |
| LinkedIn | 1200 |
| Pinterest | 1000 |
| Default / portrait-medium | 1080 |

## Wait-for-render helper

```python
# source: image-generation/create-infographics/scripts/export.py
def wait_for_render(page, extra_ms: int = 300):
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass  # timeout non-fatal
    page.wait_for_timeout(extra_ms)
```

Waits for network idle (CDN fonts loaded), then a 300ms buffer so
CSS animations reach their end state. The PNG captures the post-
animation final state.

## SVG export

Requires Inkscape OR pdf2svg:

```bash
brew install inkscape  # macOS
apt install pdf2svg    # Linux
```

If neither is installed, the script prints install instructions and
notes that the PDF can be dragged directly into Figma as a fallback.

## Gotchas

- `--width` must match the HTML's canvas width. Mismatch produces
  cropped or padded output.
- Animations — the script captures the post-animation state by
  default. If you want mid-animation, use Chart.js `animation: false`.
- `--serve` is needed for ANY external CDN resource. Without it,
  fonts fail silently and you get Times New Roman in the output.

## Cross-references

- [TECH-preview-server](TECH-preview-server.md) — the companion preview server.
  > What it does · When to use · Start the server · User instruction · How auto-refresh works · Workflow during iteration · Preview file structure · Full design fidelity in preview · Gotchas · Cross-references
- [TECH-platform-sizing](TECH-platform-sizing.md) — the per-platform width table.
  > What it does · The size table · Safe zones per platform · CSS — fixed-aspect platforms · Font size scaling by platform · Density by format · Watermark / attribution per platform · Export commands · Gotchas · Cross-references
- [TECH-anti-frontend-checklist](TECH-anti-frontend-checklist.md) — run BEFORE export.
  > What it does · The checklist · Structure · Spacing · Visual · Density · Playbook compliance (if applicable) · Data integrity · Export readiness · Common failure modes · The SaaS Landing Page · The Dashboard · The Slide Deck · The Component Demo · The Floating Islands · After checklist → run Reduction Pass · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

