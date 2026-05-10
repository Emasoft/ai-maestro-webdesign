---
name: TECH-gemini-pro-vs-flash-model-choice
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

# TECH-gemini-pro-vs-flash-model-choice

## What it does

Chooses between Gemini's **pro** and **flash** image-generation models
based on whether text correctness matters. `gemini-3-pro-image-preview`
is the default — higher-quality hand-drawn rendering with stronger text
accuracy. `gemini-2.5-flash-image` is reserved for the two-phase
fallback (visual-only generation with no text), where speed matters and
text correctness is overlaid locally.

## When to use

- **Default: `gemini-3-pro-image-preview`** — use for every
  production illustration where text legibility matters (educational
  material, slides with labels, documentation illustrations).
- **Fallback: `gemini-2.5-flash-image`** — ONLY for the two-phase
  workflow (Phase 1 visual-only, Phase 2 Pillow text overlay), and
  ONLY when compositional iteration speed matters more than
  first-class text.
- **Never** use flash as the primary model for illustrations with
  labels — flash produces too many text errors for educational
  material where the words have to be right.

## How it works

Model mapping in `scripts/generate.py`:

```python
MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro":   "gemini-3-pro-image-preview",
}
```

API selection based on use case:

| Use case | Model | Rationale |
|---|---|---|
| Educational illustration with labels | pro | Text accuracy is paramount |
| Slide illustration with call-outs | pro | Labels must be legible |
| Compositional variants (pick one, overlay text later) | flash | Fast iteration, text doesn't matter yet |
| Complete illustration with text | pro | First-class text rendering |
| Single-call happy path | pro | Quality over speed for a one-shot |

## Minimal example

Normal invocation (pro, single-call path):

```python
model_name = "gemini-3-pro-image-preview"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
# ... single API call with reference images + concept prompt + spell-out block
```

Two-phase fallback (flash, visual-only then overlay):

```python
# Phase 1: flash, NO TEXT prompt
image_bytes = generate_visual(concept, model="flash", aspect="16:9")

# Phase 2: Pillow overlay with Caveat font
overlay_text(image_bytes, labels, output_path)
```

## Gotchas

- **Pro costs more per call.** The Gemini pricing tier for
  `gemini-3-pro-image-preview` is higher than flash. The skill's
  gated-consent model (each call requires user authorisation) is
  specifically because of this cost.
- **Flash is NOT banned** — it's reserved for the two-phase fallback
  path. Don't interpret "use pro by default" as "flash is forbidden";
  flash is the right tool for visual-only iteration.
- **The model name is the full API slug**, not an alias. Gemini API
  rejects `"pro"` — must pass the full
  `"gemini-3-pro-image-preview"` identifier.
- **Different models may handle aspect ratios differently.** When
  switching models, re-validate that composition quality is acceptable
  at the chosen aspect ratio — there are edge cases where flash
  handles 4:3 better than pro or vice versa.
- **No automatic fallback.** The skill must not silently fall back
  from pro to flash on rate-limit or error. The cost difference
  matters — surface the error, let the user decide.
- **Gemini models update frequently.** When a new preview model ships,
  re-benchmark it against the references before swapping the default.
  The skill's reference-image conditioning is sensitive to model
  changes.

## Cross-references

- [SKILL](../SKILL.md) — model selection section
- [TECH-two-phase-visual-then-overlay](TECH-two-phase-visual-then-overlay.md) — the fallback workflow that
  > What it does · When to use · How it works · Phase 1 — visual-only generation · Phase 2 — local text overlay via Pillow · Minimal example · Gotchas · Cross-references
  uses flash
- [TECH-letter-by-letter-spelling-block](TECH-letter-by-letter-spelling-block.md) — the technique that pushes
  > What it does · When to use · How it works · Spell-out format · Minimal example · Gotchas · Cross-references
  pro's text accuracy to acceptable
- [TECH-aspect-ratio-selection](TECH-aspect-ratio-selection.md) — ratio choice interacts with model
  > What it does · When to use · How it works · Asking the user · API wiring · Minimal example · Gotchas · Cross-references
- [TECH-reference-image-priming](TECH-reference-image-priming.md) — references work with both models
  > What it does · When to use · How it works · API call shape · Minimal example · Gotchas · Cross-references
