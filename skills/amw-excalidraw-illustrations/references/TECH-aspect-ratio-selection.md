---
name: TECH-aspect-ratio-selection
category: excalidraw-gemini
source: SKILLS-TO-INTEGRATE/diagrams-skills/amw-excalidraw-illustrations-skill-main.zip
also-in:
---

# TECH-aspect-ratio-selection

## What it does

Asks the user which **aspect ratio** (16:9 widescreen, 1:1 square, 4:3
classic) they want before calling Gemini. The choice is passed through
the API's `imageConfig.aspectRatio` field, which meaningfully changes
the composition Gemini returns — a 16:9 request produces horizontal
two-panel layouts, a 1:1 produces centrally-composed single scenes.

## When to use

- **Before every Gemini call** in this skill.
- **Whenever the use case is ambiguous** ("make me an Excalidraw of X").
- **Never assume** — the skill defaults to 16:9 only after the user
  declined to specify.

## How it works

Three canonical ratios:

| Aspect | Use case | Composition effect |
|---|---|---|
| `16:9` | Slides, presentations, widescreen docs | Horizontal two-panel layouts, side-by-side composition |
| `1:1` | Social media posts, document insertions, avatars | Centrally-composed single scene |
| `4:3` | Classic print / legacy displays, balanced layouts | Compromise between 16:9 and 1:1 — works for 1-2 panels |

### Asking the user

Default prompt pattern:

```
Agent: "Which aspect ratio?
  - 16:9 (widescreen, slides — default)
  - 1:1 (square, social)
  - 4:3 (classic, balanced)
  Or tell me another — I'll pass it to Gemini."
```

If the user doesn't answer, default to 16:9.

### API wiring

The aspect ratio is passed in the API call's `generationConfig`:

```python
payload = {
    "contents": [{"role": "user", "parts": parts}],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {"aspectRatio": "16:9"}    # or "1:1", "4:3"
    }
}
```

The prompt itself should ALSO declare the ratio in the FORMAT section
— redundancy is safer than relying on the API flag alone:

```
FORMAT: Widescreen 16:9.
```

## Minimal example

Interactive invocation:

```
User: "Make me an Excalidraw of the OSI stack"
Agent: "Which aspect ratio?
  - 16:9 (widescreen, slides — default)
  - 1:1 (square, social)
  - 4:3 (classic, balanced)"
User: "1:1 for social media"
Agent: [generates with aspectRatio=1:1, prompt declares "Square 1:1"]
```

Non-interactive invocation (script):

```bash
python3 scripts/generate.py \
  --concept "OSI 7-layer stack, hand-drawn" \
  --output osi.png \
  --aspect 1:1
```

## Gotchas

- **Declare the ratio TWICE** — in the prompt's FORMAT section AND in
  the API `imageConfig.aspectRatio`. The redundancy catches edge cases
  where the prompt-level declaration wins over the API flag or vice
  versa.
- **16:9 is the default ONLY if the user declined to specify.** Silently
  defaulting without asking silently ships the wrong shape for
  non-slide use cases.
- **Non-canonical ratios are supported but unstable.** Gemini honours
  arbitrary ratios like `21:9` or `3:4`, but composition quality
  drops — the model is trained most heavily on the three canonical
  ratios.
- **Aspect ratio affects panel count.** A two-panel illustration works
  great at 16:9, cramps at 1:1, and looks wrong at 4:3. Match the
  composition to the ratio in the prompt's COMPOSITION section.
- **Aspect ratio interacts with text legibility.** At 1:1 the same text
  content has less horizontal space; bump the text sizes in the
  prompt ("large and legible") to compensate.
- **Cost scales with pixel count.** 16:9 is approximately 1920×1080;
  1:1 is 1024×1024; 4:3 is 1440×1080. Per-call costs scale roughly
  with total pixels.

## Cross-references

- `../SKILL.md` — aspect ratio section
- `TECH-gemini-pro-vs-flash-model-choice.md` — model choice interacts
  with ratio (some ratios perform differently per model)
- `TECH-prompt-template-structure.md` — FORMAT section declares ratio
- `TECH-reference-image-priming.md` — references should match the
  chosen ratio for best style transfer
