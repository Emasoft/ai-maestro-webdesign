<!--
ai-maestro-webdesign / skills / amw-ascii-pixel-art / references / TECH-pipeline.md
Adapted from Chris Korhonen's `ascii-pixel-art` skill in https://github.com/ckorhonen/claude-skills
Original work © 2025 Chris Korhonen — MIT License.
Adaptation © 2026 Emasoft — MIT License.
-->

# TECH-pipeline — image-to-animated-ASCII pipeline

## Table of Contents

- [Step 1 — Load and resize](#step-1-load-and-resize)
- [Step 2 — Build blurred background](#step-2-build-blurred-background)
- [Step 3 — Subject detection (rembg)](#step-3-subject-detection-rembg)
- [Step 4 — Pixel-grid overlay](#step-4-pixel-grid-overlay)
- [Step 5 — Build the character grid](#step-5-build-the-character-grid)
- [Step 6 — Composite three layers](#step-6-composite-three-layers)
- [Step 7 — Animate (JavaScript on `<canvas id="chars">`)](#step-7-animate-javascript-on-canvas-idchars)
- [Failure modes](#failure-modes)
- [References](#references)

The full 7-step pipeline that maps an input image to a self-contained animated-ASCII HTML file. Parameters in [SKILL § Parameters](../SKILL.md#parameters) are authoritative; this file describes *how each step uses them*.

## Step 1 — Load and resize

- Open the image with `PIL.Image.open(path).convert("RGB")`.
- Resize to `TARGET_WIDTH = 900 px`, preserving aspect ratio.
- Use `Image.Resampling.LANCZOS` (Pillow ≥ 10) — high-quality downscaling, no aliasing on subsequent steps.

```python
from PIL import Image
img = Image.open(input_path).convert("RGB")
w, h = img.size
new_h = int(h * (900 / w))
img = img.resize((900, new_h), Image.Resampling.LANCZOS)
```

## Step 2 — Build blurred background

The atmospheric base layer behind the ASCII characters. Four operations in order:

1. **Gaussian blur** — `radius = 14`.
2. **Darken** — multiply pixel values by `0.65` (35 % darker).
3. **Desaturate 50 %** — blend with luminance grayscale (`0.299 R + 0.587 G + 0.114 B`) at 0.5 alpha.
4. **Pixelate** — downscale via `Image.Resampling.BOX` to `(w/8, h/8)` then upscale via `Image.Resampling.NEAREST` to original — produces hard 8-px squares (cyberpunk aesthetic).

The result is base64-embedded as the bottom layer of the HTML.

## Step 3 — Subject detection (rembg)

Run `rembg.remove(img)` to produce an RGBA image; extract the alpha channel as a `numpy` mask in `[0.0, 1.0]`.

For each character cell, compute the **mean** of the mask values inside the cell. A cell is a *subject cell* iff:

```
mask_mean(cell) > 0.25
```

**Critical:** use the mask **only**. Do not supplement with luminance — bright backgrounds (sky, sand, lights) would otherwise pass and render ASCII characters in the wrong place, collapsing the figure/ground composition.

## Step 4 — Pixel-grid overlay

Static layer drawn once into its own canvas:

- White rectangles at `GRID_STEP = 24 px` intervals.
- Alpha = 0.05 (5 % opacity).
- Painted **only** on cells where `mask_mean > 0.25`.

Subtle cyberpunk lattice; never animated.

## Step 5 — Build the character grid

Iterate over cells of `CELL_W × CELL_H = 11 × 14 px`. For each cell:

1. Compute average RGB `(r, g, b)` and luminance `L = 0.299 r + 0.587 g + 0.114 b`.
2. If `mask_mean(cell) > 0.25` (subject):
   - Map `L` to an index into the **inverted** density ramp `@#S08Xox+=;:-,. ` (16 chars, dark → light): `idx = floor((1 - L/255) * 15)`.
   - Color = `normalize_color(r, g, b)` (preserve hue, brightest channel → 255).
3. Else (background):
   - Char = `.`
   - Color = `rgb(40, 65, 100)` (dark blue), drawn at 30 % opacity, static.

The ramp choice is critical: 16 graphemes spanning maximum density (`@`) to whitespace (` `). Substituting a shorter ramp loses subject definition; a longer ramp adds noise.

## Step 6 — Composite three layers

The HTML wraps three stacked elements inside a single `<div class="wrapper">`:

| Layer | Element | Content | Animates? |
|---|---|---|---|
| 1 (bottom) | `<img>` | Base64 background (step 2) | no |
| 2 (middle) | `<canvas id="grid">` | Pixel grid (step 4) | no |
| 3 (top) | `<canvas id="chars">` | Character grid (step 5) | yes — JS |

All layers share `position: absolute; inset: 0` inside a relatively-positioned wrapper sized to the resized image's dimensions.

## Step 7 — Animate (JavaScript on `<canvas id="chars">`)

Six effect channels, all driven by a single `requestAnimationFrame` loop at 60 fps:

| Effect | Math | Visible |
|---|---|---|
| Sine-wave pulse | bright subject cells: `brightness *= 1 + 0.15 * sin(t / 600 + cellIndex * 0.02)` | subtle breathing |
| Diagonal shine | sweeping highlight `x + y = t * speed` band, additive 0.3 alpha | film-grain shimmer |
| Random flicker | per-cell: 0.25 % chance per frame; flickers 2–8 frames | starfield twinkle |
| Hover ripple | within 8-cell radius of mouse: cyan glow added to color, intensity ∝ `1 - dist/8` | interactive |
| Character scatter | within 2-cell radius of mouse: random char from ramp on each frame | interactive |
| Dynamic glow | `shadowBlur = baseLuminance * (1 + pulse)` | brighter cells glow more |

Background cells render once as static `.` glyphs at 30 % opacity — never animated, never glow.

The JS source for these effects is generated by the Python pipeline as an inline `<script>`. The source repo at `reports_dev/batch9/extracted/claude-skills-main/skills/ascii-pixel-art/scripts/` contains the reference implementation — read it before modifying parameters.

## Failure modes

| Symptom | Root cause | Recovery |
|---|---|---|
| **"Subject not detected"** — output has no ASCII at all, only background dots | `rembg` mask mean ≤ 0.25 across every cell — the source has no clear figure/ground separation | Pick a different image (portrait, product on clean background). Do NOT lower the threshold — bright backgrounds will then leak ASCII chars and ruin the composition |
| **`rembg` model download blocked** — `URLError` / `ConnectionError` on first run | `rembg` needs network to fetch its ~180 MB model into the user's cache dir | Brief network access, then re-run; or pre-seed `~/.u2net/` from another machine |
| **`AttributeError: Image.LANCZOS`** — pipeline crashes in step 1 | Pillow ≥ 10 moved the constant to `Image.Resampling.LANCZOS` | Pin `pillow >= 10` and use the new namespace (the snippet in step 1 already does this) |
| **Output file > 5 MB** — slow to open, mobile chokes | Source image was very high resolution; the base64 background dominates file size | Pre-resize the source to ~1500 px max width before feeding the pipeline |
| **ASCII chars leak into the sky / background** — figure-ground collapse | Mask threshold lowered, or luminance fallback added to step 3 | Restore mask-only detection at threshold 0.25 — never supplement with luminance |
| **Animation choppy at < 30 fps** in the browser | Cell count too high (huge image), or browser tab without hardware acceleration | Resize source to 900 px (the default); confirm browser GPU acceleration |
| **Subject is centered but composition is unbalanced** | Source crop puts the subject too low/high | Recrop the source so the subject occupies the central 60 %–80 % of the frame; the pipeline does not auto-center |

## References

- Upstream source (MIT, © 2025 Chris Korhonen): `reports_dev/batch9/extracted/claude-skills-main/skills/ascii-pixel-art/`
- See [SKILL](../SKILL.md) for trigger conditions, prerequisites, and the parameter table.

<!--
Original sources adapted under MIT License.
ckorhonen/claude-skills · skills/ascii-pixel-art · © 2025 Chris Korhonen.
Adaptation © 2026 Emasoft. Both upstream and adaptation are MIT-licensed.
-->
