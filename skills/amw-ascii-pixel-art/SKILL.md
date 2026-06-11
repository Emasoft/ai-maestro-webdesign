<!--
ai-maestro-webdesign / skills / amw-ascii-pixel-art
Adapted from Chris Korhonen's `ascii-pixel-art` skill in https://github.com/ckorhonen/claude-skills
Original work © 2025 Chris Korhonen — MIT License (see SKILLS-TO-INTEGRATE/.../LICENSE).
Adaptation © 2026 Emasoft — MIT License.
-->
---
name: amw-ascii-pixel-art
description: Image-to-animated-ASCII-art generator — Pillow + rembg + numpy 7-step pipeline producing a self-contained HTML file with a 60fps canvas (sine-pulse, diagonal shine, random flicker, hover ripple). Triggers on "image to ASCII art", "animated ASCII portrait", "ASCII pixel-effect HTML", "convert photo to ASCII canvas", "rembg ASCII output". Does NOT trigger on generic "ASCII art", "make a wireframe", "infographic", or layout sketching — those route to ascii-sketch/ascii-creator/infographics. Use when the goal is a single self-contained animated-canvas HTML produced from a portrait/object photo.
version: 0.1.0
---

# ASCII Pixel-Art Generator

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md). This skill is an executor under the design-principles rules. It does not own broad design intent.

## Overview

Generates an animated ASCII-art piece from a single input image (portrait, product, distinct object). Output is a **self-contained HTML file** with three stacked layers — base64-embedded blurred background, low-opacity pixel grid, and a 60fps `<canvas>` running the character animation — opens directly in a browser with no external dependencies.

The pipeline isolates the subject via `rembg` alpha-mask thresholding, samples per-cell average RGB + luminance, maps luminance to an inverted density ramp (`@#S08Xox+=;:-,. `), and normalizes color so the brightest channel reaches 255 (preserves hue, maximizes saturation). Background cells render a static `.` in dark-blue at 30% opacity; subject cells animate.

This skill is the **artistic-visualization** path. For layout wireframes use [SKILL](../amw-ascii-sketch/SKILL.md); for a single perfect-alignment ASCII artifact use [SKILL](../amw-ascii-creator/SKILL.md); for static `+-|` diagrams use [SKILL](../amw-ascii-diagrams-reference/SKILL.md).

## Instructions

1. Confirm the request is image-driven and wants an **animated HTML** output (not a static ASCII string or a wireframe). If it is layout/wireframe/diagram, hand back to the orchestrator.
2. Verify the input image is suitable: portrait, product photo, or distinct object on a clean background. Landscapes / abstract patterns / busy backgrounds detect poorly and waste runtime. State this gate to the user before processing.
3. Confirm `pillow`, `rembg`, and `numpy` are installed (`pip install pillow rembg numpy`). The `rembg` model auto-downloads (~180 MB) on first run; warn the user about the one-time download.
4. Run the 7-step pipeline (load+resize → blurred background → rembg mask → pixel grid → character grid → composite → JS animation). The full step-by-step parameters and formulas live in [pipeline](references/TECH-pipeline.md).
> [TECH-pipeline.md] Step 1 — Load and resize · Step 2 — Build blurred background · Step 3 — Subject detection (rembg) · Step 4 — Pixel-grid overlay · Step 5 — Build the character grid · Step 6 — Composite three layers · Step 7 — Animate (JavaScript on `<canvas id="chars">`) · Failure modes · References
5. The output is a single `.html` file. Open it directly in a browser; no server needed. File size is ~500 KB – 2 MB depending on the embedded base64 background.
6. After delivery, link the user to the orchestrator's ai-slop-avoid checklist if the surrounding page chrome (header, footer, copy) needs validation — this skill produces *one artwork*, not a page.

## Parameters

Defaults the pipeline ships with — change only with a stated reason:

| Parameter | Value | Purpose |
|---|---|---|
| `TARGET_WIDTH` | 900 px | Resized image width (aspect preserved) |
| `CELL_W` × `CELL_H` | 11 × 14 px | Character cell dimensions |
| `GRID_STEP` | 24 px | Pixel-grid overlay interval |
| Blur radius | 14 | Gaussian blur on background |
| BG darken | 0.65 | Multiply 35% darker |
| BG desaturate | 50 % | Blend with luminance grayscale |
| Subject threshold | 0.25 | `rembg` mask mean to count as subject |
| ASCII ramp | `@#S08Xox+=;:-,. ` | Density gradient (dark → light, inverted) |
| BG dot color | `rgb(40, 65, 100)` | Background `.` character RGB |
| BG dot opacity | 30 % | Background character alpha |
| Grid opacity | 5 % | Pixel-grid alpha |

Color normalization (preserve hue, maximize brightness):

```python
def normalize_color(r, g, b):
    mx = max(r, g, b, 1)
    return int(r/mx*255), int(g/mx*255), int(b/mx*255)
```

## Trigger conditions

Invoke when the request is specifically:

- a photo/portrait → animated ASCII canvas in HTML
- "image to ASCII art" with cinematic / cyberpunk / retro aesthetic
- a `rembg`-based subject-mask ASCII pipeline
- an interactive (hover-ripple, flicker) ASCII output
- a self-contained, base64-embedded ASCII art file

Do NOT invoke for:

- generic "ASCII art" requests (route to `amw-ascii-sketch` for wireframes / `amw-ascii-creator` for perfect single artifacts)
- static text-only ASCII diagrams (route to `amw-ascii-diagrams-reference` or `amw-box-diagram`)
- typography effects without an input image (route to `amw-pretext`)
- batch image processing pipelines (this is one image at a time)

## Prerequisites

- **System-required (user responsibility):** Python 3.7 +, ~500 MB free RAM for image processing.
- **Install:** `pip install pillow rembg numpy` (in a venv or `uv venv --python 3.12` per CLAUDE.md). The first `rembg` invocation downloads ~180 MB of model weights into the user's cache dir.
- **No browser-automation, no external services.** Output is offline-only.

## Position in flow

EXECUTOR. Invoked when the orchestrator confirms (Phase B) that an animated ASCII canvas is the right artifact for a photo asset. Not part of the default plan-phase ASCII loop — that uses `amw-ascii-sketch`.

## Output

A single self-contained `.html` file:

- No external CSS, no external JS, no CDN dependencies.
- Background image base64-embedded (`data:image/jpeg;base64,...`).
- Inline `<style>` and `<script>` blocks; opens directly in any modern browser.
- 60 fps canvas animation, responds to mouse hover within an 8-cell radius (cyan glow + character-scatter within 2 cells).
- File size ~500 KB – 2 MB depending on source image dimensions.

## Error Handling

Failure modes and how to recover live in [pipeline § Failure modes](references/TECH-pipeline.md#failure-modes). Highlights:

- **"Subject not detected" (mask mean ≤ 0.25):** the source has no clear figure/ground separation — recommend a different image, do not lower the threshold (silently widening makes bright backgrounds spill ASCII chars).
- **`rembg` model download blocked:** the user is offline or behind a strict proxy — the model is needed; advise enabling network briefly or pre-seeding the cache.
- **`pillow` LANCZOS unavailable on Pillow ≥ 10:** use `Image.Resampling.LANCZOS`. Pin Pillow ≥ 10 (the constant moved namespaces).
- **Output > 5 MB:** the source image was huge — resize to ~1500 px max before feeding the pipeline.

## Non-negotiables

- Does NOT own broad design intent. The orchestrator decides whether an animated ASCII canvas is the right artifact at all.
- Subject detection uses the `rembg` alpha mask **only** — never supplement with luminance, or bright backgrounds will get ASCII characters and the composition collapses.
- ASCII ramp is inverted: dark pixels → dense chars (`@`), light pixels → space. Do not re-order without a stated reason.
- Output is one HTML file — no fragments, no companion CSS/JS. If the user wants a page, route the wrapper to `amw-wireframe-builder-agent` or the orchestrator.
- English-only content. No third-language characters in any file.

## Resources

- [pipeline](references/TECH-pipeline.md) — full 7-step pipeline, density ramp, color formula, failure modes.
> [TECH-pipeline.md] Step 1 — Load and resize · Step 2 — Build blurred background · Step 3 — Subject detection (rembg) · Step 4 — Pixel-grid overlay · Step 5 — Build the character grid · Step 6 — Composite three layers · Step 7 — Animate (JavaScript on `<canvas id="chars">`) · Failure modes · References

Cross-skill:

| Resource | Role |
|---|---|
| [SKILL](../amw-design-principles/SKILL.md) | Orchestrator — decides whether an animated ASCII canvas is the right artifact |
| [SKILL](../amw-ascii-sketch/SKILL.md) | Plan-phase ASCII wireframe loop (different goal — layout, not art) |
| [SKILL](../amw-ascii-creator/SKILL.md) | Single perfect-alignment ASCII artifact (text-mode, not image-derived) |
| [SKILL](../amw-ascii-validator/SKILL.md) | Validation gate for any emitted ASCII (HTML output here is pixel-canvas, not text-block — validator does NOT apply to the canvas content) |
| [SKILL](../amw-pretext/SKILL.md) | Typography effects (text-on-path, kinetic) — different artifact class |

<!--
Original sources adapted under MIT License:
- ckorhonen/claude-skills · skills/ascii-pixel-art · © 2025 Chris Korhonen
Adapted © 2026 Emasoft. Both upstream and adaptation are MIT-licensed.
-->
