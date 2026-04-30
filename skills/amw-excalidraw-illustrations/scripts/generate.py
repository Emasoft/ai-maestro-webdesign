#!/usr/bin/env python3
"""
Hybrid Excalidraw-style illustration generator.

Primary path: a single Gemini Pro image call with reference-image conditioning
produces a complete hand-drawn illustration with integrated text.

Fallback two-phase path (for stubborn text-rendering cases):
  Phase 1 — Gemini Flash (cheaper) generates a VISUAL-ONLY illustration (no text)
  Phase 2 — Pillow overlays hand-written text labels in a Caveat-style font at
            user-specified coordinates.

Requires:
  - GEMINI_API_KEY env var (Google AI Studio: https://aistudio.google.com/)
  - Pillow ONLY for the text-overlay path (phase 2). Install via /amw-init
    section 7 when the skill is expected to be used, or skip if only the
    primary path matters.
  - The reference images live at <skill_dir>/references/reference{1,2}.png
  - The hand-written font lives at <skill_dir>/fonts/Caveat-Variable.ttf

Primary path CLI:
  generate.py --concept "..." --output <path.png> --model pro [--aspect 16:9]

Fallback two-phase CLI:
  generate.py --concept "..." --labels '<json-array>' --output <path.png> --model flash

Visual-only sketch (no text, no overlay; for layout iteration):
  generate.py --concept "..." --output <path.png> --model flash --visual-only
"""

import argparse
import base64
import io
import json
import os
import sys
import textwrap
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
FONT_PATH = SKILL_DIR / "fonts" / "Caveat-Variable.ttf"
REF_DIR = SKILL_DIR / "references"

# Available Gemini image models.
# - "pro": produces text-correct illustrations (recommended for final output).
# - "flash": cheaper, text is unreliable; useful only for visual-only layout
#            iteration or as phase 1 of the two-phase overlay path.
MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
}


def load_references():
    """Load the two reference PNGs as base64-encoded strings."""
    refs = []
    for i in (1, 2):
        ref_path = REF_DIR / f"reference{i}.png"
        if ref_path.exists():
            with open(ref_path, "rb") as f:
                refs.append(base64.b64encode(f.read()).decode())
    return refs


def generate_visual(concept: str, model: str = "flash", aspect: str = "16:9") -> bytes:
    """
    Call Gemini to produce a VISUAL-ONLY illustration (no text).

    Used as phase 1 of the overlay fallback. The generated image is plain
    hand-drawn sketch; text is added afterwards by `overlay_text`.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not set. Obtain one at https://aistudio.google.com/ "
            "and export it before invoking this skill."
        )

    model_name = MODELS.get(model, MODELS["flash"])
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model_name}:generateContent?key={api_key}"
    )

    refs = load_references()
    if not refs:
        raise RuntimeError(
            f"No reference images found at {REF_DIR}. The plugin ships two "
            f"Excalidraw-style reference PNGs; they must be present."
        )

    prompt = f"""Generate an Excalidraw / hand-drawn-style illustration with these traits:
- Loose, sketch-like strokes — natural imperfect lines, as if drawn by hand
- A CLEAN WHITE background
- Limited palette: black for main strokes, 1-2 soft accent colors (light blue, soft orange, mint green)
- Minimalist but with MANY ICONS and small drawings that visually illustrate each concept
- DO NOT INCLUDE ANY TEXT, WORDS, OR LETTERS in the image. Only drawings, icons, arrows, and lines
- Leave blank spaces where titles and labels would normally go (text will be added afterwards)
- Horizontal format {aspect}
- Include abundant small illustrations: objects, symbols, directional arrows, frames, decorative divider lines

Concept to illustrate (DRAWINGS ONLY, NO text):
{concept}

IMPORTANT: The image must be PURELY VISUAL. Zero text. Zero letters. Zero numbers. Only sketch-style drawings.
Imitate the visual style of the provided reference images faithfully."""

    parts = [
        {"text": "Visual-style reference images to imitate faithfully:"},
        {"inlineData": {"mimeType": "image/png", "data": refs[0]}},
        {"inlineData": {"mimeType": "image/png", "data": refs[1]}},
        {"text": prompt},
    ]

    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())

    for part in data["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])
        elif "text" in part:
            print(f"  Gemini says: {part['text'][:200]}", file=sys.stderr)

    raise RuntimeError("Gemini returned no image.")


def overlay_text(image_bytes: bytes, labels: list[dict], output_path: str):
    """
    Phase 2 of the two-phase fallback — overlay hand-written text labels on a
    visual-only image using Pillow.

    Each label is a dict:
      - text      : string to render
      - x, y      : position as a fraction of width/height (0.0-1.0)
      - size      : font size in pixels (default 40)
      - color     : HTML color (default "#1a1a1a")
      - anchor    : PIL anchor string ("mm" center, "lm" left, "rm" right)
      - bold      : use bold weight (default False)
      - max_width : optional wrap width as fraction of image width (0.0-1.0)
    """
    # Pillow is an optional dependency — only required for this fallback path.
    from PIL import Image, ImageDraw, ImageFont

    img = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(img)
    w, h = img.size

    for label in labels:
        text = label["text"]
        x = int(label.get("x", 0.5) * w)
        y = int(label.get("y", 0.5) * h)
        size = label.get("size", 40)
        color = label.get("color", "#1a1a1a")
        anchor = label.get("anchor", "mm")
        bold = label.get("bold", False)

        # Variable font weight: 700 for bold, 400 for regular
        font_weight = 700 if bold else 400
        try:
            font = ImageFont.truetype(str(FONT_PATH), size)
            try:
                font.set_variation_by_axes([font_weight])
            except Exception:
                pass
        except Exception:
            font = ImageFont.load_default()

        # Word-wrap when max_width is supplied
        max_width = label.get("max_width")
        if max_width:
            max_px = int(max_width * w)
            # Rough character-width estimate for Caveat ~ 0.55 * font size
            char_width = size * 0.55
            chars_per_line = max(1, int(max_px / char_width))
            lines = textwrap.wrap(text, width=chars_per_line)
            line_height = size * 1.3

            total_height = len(lines) * line_height
            start_y = y - total_height / 2

            for i, line in enumerate(lines):
                ly = int(start_y + i * line_height)
                draw.text((x, ly), line, fill=color, font=font, anchor=anchor)
        else:
            draw.text((x, y), text, fill=color, font=font, anchor=anchor)

    img.save(output_path, "PNG")
    file_size = os.path.getsize(output_path)
    print(f"Saved: {output_path} ({file_size // 1024} KB)")


def main():
    parser = argparse.ArgumentParser(description="Hybrid Excalidraw-style illustration generator")
    parser.add_argument("--concept", required=True, help="Concept to illustrate")
    parser.add_argument("--labels", help="JSON array of overlay-label specs (see module docstring)")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--model", default="flash", choices=["flash", "pro"], help="Gemini model (flash=cheap+no-text-correctness, pro=paid+text-correct)")
    parser.add_argument("--aspect", default="16:9", help="Aspect ratio hint (used only for phase 1 composition)")
    parser.add_argument("--visual-only", action="store_true", help="Generate a visual-only image with no text overlay (layout iteration only — do not ship)")
    args = parser.parse_args()

    print(f"Generating illustration via Gemini {args.model}...", file=sys.stderr)
    image_bytes = generate_visual(args.concept, model=args.model, aspect=args.aspect)

    if args.visual_only:
        with open(args.output, "wb") as f:
            f.write(image_bytes)
        print(f"Saved (visual-only): {args.output} ({len(image_bytes) // 1024} KB)")
    else:
        if not args.labels:
            sys.exit("--labels is required unless --visual-only is set")
        labels = json.loads(args.labels)
        overlay_text(image_bytes, labels, args.output)


if __name__ == "__main__":
    main()
