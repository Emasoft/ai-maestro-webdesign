---
name: TECH-core-call-pattern
category: excalidraw-illustrations
---

# TECH-core-call-pattern — Python heredoc for the Gemini call

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Reference invocation](#reference-invocation)
- [Prompt template (always use this shape)](#prompt-template-always-use-this-shape)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Documents the single happy-path Python call that produces an Excalidraw-style
PNG. The call uses `urllib`, embeds the two reference PNGs as base64 to
anchor the visual style, sends the `gemini-3-pro-image-preview` REST
request, and writes the decoded PNG to disk.

## When to use

Every successful invocation of `amw-excalidraw-illustrations`. The wrapper
script `scripts/generate.py` follows this same shape; if you replace the
script, keep the shape identical.

## How it works

- Reads `GEMINI_API_KEY` from the environment; aborts with a clear error
  message if missing (NEVER prompt for the key inline).
- Loads `references/reference{1,2}.png` from the skill's own folder as
  base64-encoded style anchors.
- Builds a single `contents` part list: reference-images header, reference
  image 1, reference image 2, then the concept prompt text.
- Sets `generationConfig.imageConfig.aspectRatio` to the user-chosen
  ratio (default `16:9`).
- POSTs to the v1beta generateContent endpoint with a 300-second timeout
  (image generation is slow).
- Iterates the response parts, writes any `inlineData` part to the output
  path, and echoes any `text` part to stderr (model's narration).

## Reference invocation

```bash
SKILL_DIR="$(dirname "$0")/.."           # or resolve relative to this skill's folder
CONCEPT="<prompt text — see 'Prompt template' below>"
OUTPUT="/path/to/output-filename.png"
ASPECT="16:9"                             # or "1:1" / "4:3"

python3 - <<'PYEOF'
import json, urllib.request, base64, os, sys
from pathlib import Path

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    sys.exit("GEMINI_API_KEY not set. Obtain one at https://aistudio.google.com/ and export it before invoking this skill.")

skill_dir = Path(os.environ["SKILL_DIR"])
model = "gemini-3-pro-image-preview"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

refs = []
for i in (1, 2):
    with open(skill_dir / "references" / f"reference{i}.png", "rb") as f:
        refs.append(base64.b64encode(f.read()).decode())

parts = [
    {"text": "Visual-style reference images to imitate faithfully:"},
    {"inlineData": {"mimeType": "image/png", "data": refs[0]}},
    {"inlineData": {"mimeType": "image/png", "data": refs[1]}},
    {"text": os.environ["CONCEPT"]},
]

payload = {
    "contents": [{"role": "user", "parts": parts}],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {"aspectRatio": os.environ["ASPECT"]},
    },
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=300) as resp:
    data = json.loads(resp.read())

output = os.environ["OUTPUT"]
for part in data["candidates"][0]["content"]["parts"]:
    if "inlineData" in part:
        img = base64.b64decode(part["inlineData"]["data"])
        with open(output, "wb") as f:
            f.write(img)
        print(f"Saved: {output} ({len(img) // 1024} KB)")
    elif "text" in part:
        print(part["text"])
PYEOF
```

The Python heredoc is the reference shape. The actual invocation should
be a small wrapper that resolves `SKILL_DIR` to this skill's folder and
passes `CONCEPT`, `OUTPUT`, `ASPECT` as environment variables.

## Prompt template (always use this shape)

Following this structure is what makes the difference between "usable for
a slide" and "visually cute but word-level broken." The prompt is always
in the same language as the output text — if the user wants Spanish
labels, write the prompt in Spanish; English, write it in English; etc.
The model copies the prompt's language verbatim into the illustration.

```
Generate a HIGH-QUALITY Excalidraw / hand-drawn-style illustration for educational material IN <LANGUAGE>.

FORMAT: <Widescreen 16:9 / Square 1:1 / Classic 4:3>.

VISUAL STYLE:
- Loose but DETAILED and expressive strokes, like a professional illustrator
- Clean white background
- Palette: black for lines, <color 1> for <section 1>, <color 2> for <section 2>, ...
- All text inside ROUNDED FRAMES, SPEECH BUBBLES, or LABELLED CALLOUTS with filled backgrounds
- Large hand-drawn arrows connecting sections
- Cross-hatched shading for depth

COMPOSITION:
<Describe layout: panels, columns, reading flow, space distribution>

<SECTION / PANEL 1>:
- Title «<TITLE>» inside a frame with <color> background, large letters
- <Central visual element described in detail>
- Speech bubble: «<Short phrase>»
- Labelled icons in frames: <icon> («<Label>»), <icon> («<Label>»)
- Bottom frame: «<Authors / data>»

<SECTION / PANEL 2>:
<Same structure ...>

<CONNECTIONS>:
- Arrows, timelines, elements linking the sections

TEXT RULES — VERIFY LETTER BY LETTER:
- <WORD1> is spelled <W-O-R-D-1>
- <WORD2> is spelled <W-O-R-D-2>
- Every word must be PERFECTLY SPELLED in correct <LANGUAGE>
- The text must be LARGE and LEGIBLE
- Maximum 2-3 words per label
- Every piece of text is always inside a frame or bubble, never floating

Imitate the visual style of the provided reference images faithfully.
```

See [prompt-template-en](prompt-template-en.md) and
[prompt-template-es](prompt-template-es.md) for filled-in examples.

## Gotchas

- Never log the URL — it contains `?key=$GEMINI_API_KEY`.
- The 300 s timeout is intentional. Pro image generation often takes 60-180 s.
- The response can include both `inlineData` (image) and `text` (model
  narration) parts; iterate, do not assume index 0.
- Two reference images is the magic number — one is not enough style
  anchor, three+ confuses the model.

## Cross-references

- [TECH-reference-image-priming](./TECH-reference-image-priming.md)
- [TECH-prompt-template-structure](./TECH-prompt-template-structure.md)
- [TECH-gemini-pro-vs-flash-model-choice](./TECH-gemini-pro-vs-flash-model-choice.md)
- [TECH-letter-by-letter-spelling-block](./TECH-letter-by-letter-spelling-block.md)
- [SKILL](../SKILL.md) — parent skill
