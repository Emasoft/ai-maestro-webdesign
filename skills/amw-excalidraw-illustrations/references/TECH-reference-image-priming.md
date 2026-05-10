---
name: TECH-reference-image-priming
category: excalidraw-gemini
source: SKILLS-TO-INTEGRATE/diagrams-skills/amw-excalidraw-illustrations-skill-main.zip
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-reference-image-priming

## What it does

Stabilises **visual style across invocations** by sending 2 reference
PNG images to Gemini on every call as "style anchors". Without the
reference images, Gemini's hand-drawn output drifts wildly between
calls — one invocation returns loose-line sketch, the next returns
photoreal cross-hatching. With the references, the output style stays
within a narrow Excalidraw-roughness band.

## When to use

- **Every Gemini API call** in this skill. Always.
- **When consistency across a deck of slides** matters — the illustrations
  must look like they came from the same hand.
- **Never swap the references** without user opt-in — the whole point of
  reference conditioning is stability.

## How it works

Two reference PNGs ship with the skill at:

```
skills/amw-excalidraw-illustrations/references/reference1.png
skills/amw-excalidraw-illustrations/references/reference2.png
```

Both are pre-made Excalidraw-style illustrations authored in a
consistent visual language (loose lines, limited palette, framed text,
cross-hatched shading). Gemini is instructed to "imitate the visual
style of the provided reference images faithfully".

**API call shape**

```python
parts = [
    {'text': 'Reference images of the visual style to imitate:'},
    {'inlineData': {'mimeType': 'image/png', 'data': base64_of_reference1}},
    {'inlineData': {'mimeType': 'image/png', 'data': base64_of_reference2}},
    {'text': detailed_concept_prompt}   # the user's actual request
]

payload = {
    'contents': [{'role': 'user', 'parts': parts}],
    'generationConfig': {
        'responseModalities': ['TEXT', 'IMAGE'],
        'imageConfig': {'aspectRatio': aspect}
    }
}
```

Base64-encode both references once per call, embed them as
`inlineData`, prefix with a text hint that they are style anchors.

## Minimal example

Python snippet loading and embedding the references (from the skill's
`scripts/generate.py`):

```python
REF_DIR = SKILL_DIR / "references"

def load_references():
    refs = []
    for i in [1, 2]:
        ref_path = REF_DIR / f"reference{i}.png"
        if ref_path.exists():
            with open(ref_path, "rb") as f:
                refs.append(base64.b64encode(f.read()).decode())
    return refs

refs = load_references()
parts = [
    {"text": "Reference images of the visual style to imitate:"},
    {"inlineData": {"mimeType": "image/png", "data": refs[0]}},
    {"inlineData": {"mimeType": "image/png", "data": refs[1]}},
    {"text": prompt},
]
```

## Gotchas

- **The reference images are load-bearing — do not delete or replace them
  without the user's explicit opt-in.** Replacing them would cause a
  visual-style drift across all subsequent outputs and silently break
  any deck or document that mixes old and new illustrations.
- **Two images, not one.** One reference is easily overfit (Gemini
  reproduces literal elements from the single reference rather than the
  style). Two diverse references let Gemini triangulate "style" vs
  "specific content".
- **PNG, not JPG.** PNG keeps the line crispness; JPG's lossy compression
  introduces artefacts that Gemini occasionally copies into the output.
- **Prefix with a text hint** that the images are style anchors. Without
  the hint, Gemini sometimes treats the references as content to
  combine with the user's concept — producing illustrations that
  literally merge elements of the reference with the request.
- **References are shipped with the plugin** — not downloaded at runtime.
  A runtime fetch path would introduce a network dependency and risk
  MITM-style style drift.

## Cross-references

- [SKILL](../SKILL.md) — model + reference-images requirement
- `../scripts/generate.py` — the reference-loading helper
- [TECH-prompt-template-structure](TECH-prompt-template-structure.md) — the accompanying text prompt
  > What it does · When to use · How it works · Section order and purpose · Template skeleton · Minimal example · Gotchas · Cross-references
- [TECH-letter-by-letter-spelling-block](TECH-letter-by-letter-spelling-block.md) — the spell-out technique
  > What it does · When to use · How it works · Spell-out format · Minimal example · Gotchas · Cross-references
  that makes text render correctly
- [TECH-gemini-pro-vs-flash-model-choice](TECH-gemini-pro-vs-flash-model-choice.md) — which model to call with
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  the references
