---
name: TECH-two-phase-visual-then-overlay
category: excalidraw-gemini
source: SKILLS-TO-INTEGRATE/diagrams-skills/amw-excalidraw-illustrations-skill-main.zip
also-in: skills/amw-excalidraw-illustrations/scripts/generate.py
---

# TECH-two-phase-visual-then-overlay

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Phase 1 — visual-only generation](#phase-1-visual-only-generation)
  - [Phase 2 — local text overlay via Pillow](#phase-2-local-text-overlay-via-pillow)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Fallback workflow for when Gemini stubbornly misspells a key word in the
illustration. Splits generation into **two phases**: Phase 1 asks
Gemini for a VISUAL-ONLY illustration (no text anywhere), Phase 2
overlays text locally using Pillow + the Caveat hand-written font. The
result is hand-drawn aesthetic with guaranteed-correct text.

## When to use

- **When 2 attempts with `gemini-3-pro-image-preview` have failed to
  spell a key word correctly** despite the letter-by-letter spell-out
  block.
- **When iterating rapidly on composition** without caring about text —
  flash is fast and cheap; run 3-4 compositional variants, pick one,
  then overlay text locally.
- **When the text has tricky characters** (accents, uncommon diacritics,
  mathematical symbols, non-Latin scripts) that Gemini doesn't reliably
  render.

Do not use as the default path — the single-call pipeline via the pro
model produces better visual-text integration when it works. Use this
only as a recovery.

## How it works

### Phase 1 — visual-only generation

Call Gemini with an explicit "NO TEXT" prompt:

```
Generate a hand-drawn Excalidraw-style illustration with these features:
- Loose sketchy lines, hand-drawn feel
- Clean WHITE background
- Limited palette: black for lines, 1-2 soft accent colours
- Minimalist but with MANY small ICONS illustrating each concept
- NO TEXT. NO WORDS. NO LETTERS. Only drawings, icons, arrows, lines
- Leave blank spaces where titles and labels would go (text added later)
- Format: [aspect ratio]
- Include abundant small illustrations: objects, symbols, directional arrows, frames, decorative divider lines

Concept to illustrate (VISUALS ONLY, NO text):
[concept]

IMPORTANT: The image must be PURELY VISUAL. Zero text. Zero letters. Zero numbers. Sketch style only.
Imitate the visual style of the provided reference images faithfully.
```

The flash model is acceptable for Phase 1 because the text-rendering
weakness doesn't matter when there IS no text.

### Phase 2 — local text overlay via Pillow

Use `scripts/generate.py`'s `overlay_text()` function. Each label is a
dict:

```python
{
  'text': 'REALISM',
  'x': 0.25,              # proportional position (0.0-1.0 of width)
  'y': 0.15,              # proportional position (0.0-1.0 of height)
  'size': 48,             # font size in px
  'color': '#1a1a1a',
  'anchor': 'mm',         # PIL anchor: mm=middle, lm=left, rm=right
  'bold': True,
  'max_width': 0.3        # max width before wrap (proportional)
}
```

Font: `fonts/Caveat-Variable.ttf` — a variable hand-written font that
ships with the skill. The variable axis lets overlay code pick any
weight from 400 (regular) to 700 (bold).

## Minimal example

Single invocation via the CLI wrapper:

```bash
python3 scripts/generate.py \
  --concept "Realism vs Naturalism — art history lesson, two panels" \
  --labels '[
    {"text":"REALISM", "x":0.25, "y":0.10, "size":56, "bold":true},
    {"text":"NATURALISM", "x":0.75, "y":0.10, "size":56, "bold":true},
    {"text":"Life as it is", "x":0.25, "y":0.45, "size":32, "max_width":0.3},
    {"text":"Life as science sees it", "x":0.75, "y":0.45, "size":32, "max_width":0.3}
  ]' \
  --output /tmp/realism-vs-naturalism.png \
  --model flash
```

Internally:

1. Loads `reference1.png` + `reference2.png` as style anchors (same as
   the single-call pipeline).
2. Calls Gemini Flash with the "NO TEXT" prompt — fast and cheap,
   accepts text-blind output.
3. Reads the returned bytes.
4. Opens with Pillow, overlays each label at the specified position in
   Caveat font.
5. Writes the final PNG.

## Gotchas

- **Phase 1 prompt must include "NO TEXT" multiple times.** Gemini
  occasionally ignores a single instance; reinforcing 2-3 times in the
  prompt reduces the text-leak rate.
- **Proportional positions (0.0-1.0) not pixels.** The aspect ratio may
  shift between calls; fixed-pixel positions get misaligned. Use
  proportions so the layout scales with the output image.
- **Caveat font must be the Variable TTF.** The skill ships
  `Caveat-Variable.ttf`; replacing with a static TTF breaks the
  weight-axis override (bold vs regular).
- **PIL anchor codes are two-letter.** `mm` middle-middle, `lm`
  left-middle, `rm` right-middle. Getting this wrong shifts the label
  off-target — usually discovered visually.
- **Word wrap uses an estimated char width** (`size * 0.55`). It's
  approximate; for long labels, pre-wrap manually and break into
  multiple label dicts at different y offsets.
- **This is a fallback, not the primary path.** The two-phase workflow
  has lower visual-text integration than the single-call path —
  hand-overlaid text sits on top of the image rather than being part
  of the hand-drawn composition. Use it only when the pro model's
  spelling fails repeatedly.

## Cross-references

- [SKILL](../SKILL.md) — iteration / fallback section
- `../scripts/generate.py` — the implementation
- [TECH-reference-image-priming](TECH-reference-image-priming.md) — Phase 1 still uses the references
  > What it does · When to use · How it works · API call shape · Minimal example · Gotchas · Cross-references
- [TECH-letter-by-letter-spelling-block](TECH-letter-by-letter-spelling-block.md) — the primary anti-error
  > What it does · When to use · How it works · Spell-out format · Minimal example · Gotchas · Cross-references
  technique that this technique falls back from
- [TECH-framed-text-no-floating](TECH-framed-text-no-floating.md) — even overlaid text should sit
  > What it does · When to use · How it works · Rounded title frame (section headers) · Speech bubble (tag-line commentary) · Labelled callout with filled background (icon labels, attributions) · Minimal example · Gotchas · Cross-references
  inside frames drawn in Phase 1
