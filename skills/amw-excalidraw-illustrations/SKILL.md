---
name: amw-excalidraw-illustrations
description: Generate hand-drawn Excalidraw-style conceptual illustrations via the Gemini API — white background, rough-sketch aesthetic, integrated in-panel text (speech bubbles, labelled frames) for educational material, slides, and concept diagrams. GATED — requires a user-provided `GEMINI_API_KEY` and explicit per-call consent because each call incurs a cost on Google's Gemini quota. Triggers on narrow phrasings only — "Excalidraw-style illustration of X", "hand-drawn concept diagram", "sketchy educational illustration", "whiteboard sketch of this concept for my slide". Does NOT trigger on broad design intent ("design a page", "UI", "landing page", "mockup") or on other diagram intents (flowchart, architecture, SVG diagram) — those route to design-principles, diagram-architecture, or diagram-svg.
version: 0.1.0
---

# Excalidraw Illustrations

> **GATED skill.** Requires `GEMINI_API_KEY` in the environment AND explicit user consent before every Gemini call — each call costs real money on Google's Gemini Pro image tier. Do not invoke silently or in a loop.
> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> This skill is an executor. Its triggers are narrow — hand-drawn / Excalidraw / whiteboard-style educational illustration only. The orchestrator routes here for conceptual, illustration-heavy slide or document material where the deliberate rough-sketch aesthetic is the point; everything else stays outside this skill.
>
> **Documented exception to `../amw-design-principles/ai-slop-avoid.md` item 3 ("no AI-drawn illustrations").** That rule targets AI-painted people, landscapes, and product shots rendered in photoreal or vector-illustration style — all of which have stiff lines, wrong proportions, and visibly degrade the whole piece. This skill is the carved-out exception **only** because its output is tightly constrained: white background, hand-drawn Excalidraw roughness, concept-diagram / whiteboard use case, integrated labelled text. The constraint itself is what keeps the output from looking like generic AI-illustration slop. Do not use this skill for anything that does not meet all four of those constraints.

## Activation

Callable directly via the `/amw-create-excalidraw-like-diagram-png` command (user shortcut for users who want a hand-drawn Excalidraw-style illustration and have `GEMINI_API_KEY` set), or invoked by the `design-principles` orchestrator during **Phase B** when the approved design calls for a hand-drawn / whiteboard-aesthetic conceptual illustration. **GATED:** explicit cost consent required before every invocation in both modes.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**OUTPUT.** One Gemini call per invocation. Input: a concept description plus an aspect-ratio choice; output: a single PNG file on disk rendered in Excalidraw hand-drawn style, with text integrated into the illustration as part of the drawing (speech bubbles, rounded frames, labelled icons — never floating raw labels).

This skill does not iterate automatically. If the first attempt has bad text (the #1 failure mode of generative image models), the user is asked whether to regenerate — the user is told the next call will cost another Gemini quota hit.

## Trigger conditions

Fires on these specific phrasings:

- "Excalidraw-style illustration of <concept>"
- "hand-drawn concept diagram of <topic>"
- "sketchy educational illustration for <slide / lesson>"
- "whiteboard sketch of <concept>"
- "conceptual diagram hand-drawn"
- "make an Excalidraw of <topic>"
- "pizarra / whiteboard illustration for <topic>" (the source skill was originally Spanish; both vocabularies should activate)

Do NOT fire on:

- generic "design X", "draw X", "illustrate this page", "UI", "landing page", "mockup" — `../amw-design-principles/` owns those
- flowchart / architecture / sequence / ER diagram requests — `../amw-diagram-editorial/`, `../amw-diagram-architecture/`, `../amw-diagram-svg/` own those
- SVG icon / logo / technical-figure requests — `../amw-svg-creator/` owns those (gated differently)
- photoreal or vector-illustration requests — refuse and refer back to design-principles' ai-slop-avoid item 3: ask the user for a real asset, do not generate

## Dependencies

- **runtime_binaries (system):** `python3 ≥ 3.8` — used to call the Gemini REST endpoint directly and (optionally) overlay fallback text via Pillow.
- **python_packages:**
  - **Required:** none — the primary call path uses only `urllib`, `json`, `base64`, `os` from the Python stdlib. No pip install is needed for the happy path.
  - **Optional fallback:** `Pillow` — only needed for the two-phase "visual-only first, text-overlay second" recovery path in `scripts/generate.py` when Gemini keeps misspelling a key word and the user wants to manually pin the text. Install via `/amw-init` Section 7 when the user says they will use this skill.
- **API access:** `GEMINI_API_KEY` environment variable. Obtain from https://aistudio.google.com/ > API keys. The skill **must** abort and surface a clear error if the variable is unset — do not prompt for the key inline, do not fall back to any other image model, do not swap to a local-rendering path.
- **Model:** `gemini-3-pro-image-preview` by default. The flash variant (`gemini-2.5-flash-image`) is disabled in this skill except for the explicit visual-only sketch path inside `scripts/generate.py`, because flash produces too many text errors for educational material where the words have to be right.
- **Reference images:** `references/reference1.png` and `references/reference2.png` inside this skill folder. These are shipped with the plugin and provide the visual-style anchor for the Gemini call. Do not swap them without the user's explicit opt-in — the whole point of the reference-conditioning is style stability across invocations.
- **Font fallback:** `fonts/Caveat-Variable.ttf` — ships with the plugin; used only by the Pillow overlay path.

## Cost note (non-negotiable)

Every successful call to `gemini-3-pro-image-preview` is **billed by Google to the user's own Gemini quota** — the plugin has no billing relationship with Google. Per-call cost depends on the user's pricing tier and the aspect ratio chosen; the skill assumes each call is non-trivial and MUST ask the user to explicitly authorize each generation before the HTTP request is sent. Implicit regeneration after a failed text render is not allowed — the user must say "regenerate" before a new call goes out.

## Aspect ratio (ask before generating)

The skill asks the user which format to render **before** sending the Gemini call:

| Aspect | When to use |
|---|---|
| `16:9` | Default. Widescreen slides, presentations, video covers. |
| `1:1` | Social posts, document insets, single-icon concept frames. |
| `4:3` | Classic slide format, older decks, print handouts. |

If the user does not specify, default to `16:9` and tell them that's what will be used.

## Core call pattern

The happy path is a single Python call with `urllib`, embedding the two reference images as base64 alongside the concept prompt. The reference images are the style anchor — Gemini imitates them faithfully enough to produce consistent hand-drawn output across separate invocations.

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

The Python heredoc is the reference shape. The actual invocation should be a small wrapper that resolves `SKILL_DIR` to this skill's folder and passes `CONCEPT`, `OUTPUT`, `ASPECT` as environment variables.

## Prompt template (always use this shape)

Following this structure is what makes the difference between "usable for a slide" and "visually cute but word-level broken." The prompt is always in the same language as the output text — if the user wants Spanish labels, write the prompt in Spanish; English, write it in English; etc. The model copies the prompt's language verbatim into the illustration.

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

See `references/prompt-template-en.md` and `references/prompt-template-es.md` for filled-in examples.

## Principles (keep these, they are load-bearing)

1. **Text is part of the drawing, not floating.** Always inside speech bubbles, labelled frames, or callouts with a filled background. Floating raw labels look generative-AI-slop; framed labels look hand-drawn and intentional.
2. **Spell out the hard words letter-by-letter in the prompt.** Every model will misspell uncommon words without this. Including the spelling is not overkill — it is the single biggest quality lever.
3. **Fewer words, larger.** Two legible words beat five cramped ones. Max 2–3 words per label.
4. **Narrative composition, not flat diagrams.** Rich scenes with many small icons and labelled vignettes outperform a flat "title + three boxes" every time.
5. **Many small icons.** Each concept should have a visual metaphor. Icon-heavy scenes read as Excalidraw; icon-sparse scenes read as AI-illustration.
6. **Frames and panels.** Separate sections with rounded borders in different accent colors. Two or three accent colors max.
7. **Expressive arrows.** Large, hand-drawn, labelled. Arrows communicate relationships — not just direction.

## Verification loop (MANDATORY every time)

After every Gemini call:

1. Read the generated PNG with the Read tool (or open it via `open <path>` on macOS / `xdg-open <path>` on Linux) to inspect it.
2. Check **every word** in the image is spelled correctly.
3. If any word is misspelled: ask the user whether to regenerate (another Gemini call) or drop that word / simplify the label in a regeneration prompt.
4. Show the final image path to the user and open it at full size.

Do not silently regenerate. Do not silently ship a broken image. Do not invent a text-overlay fix without asking.

## Iteration and fallback paths

- If two Pro calls in a row have the same word wrong, **simplify** that label (fewer words, more common synonym) and try once more.
- For cheap iteration on the **composition only** (without caring about text), the script `scripts/generate.py` has a `--visual-only` mode that calls the flash variant and produces a text-free illustration. Use this for fast layout experiments only — cost per call is lower but text will not render correctly, so it cannot be shipped as-is.
- For pinpoint text corrections (one stubborn label Gemini keeps getting wrong), the same `scripts/generate.py` supports a two-phase hybrid: phase 1 generates a visual-only image with flash, phase 2 overlays Pillow-rendered text in `fonts/Caveat-Variable.ttf` at user-specified coordinates. This path requires Pillow installed via `/amw-init` Section 7. Use only when regeneration has failed twice on the same word.

## Dimensional and quality constraints

- **White background only.** Do not let the model pick a colored background — educational-material context assumes the image will be placed on a slide with its own background.
- **Minimum font size inside the illustration.** The generated text must be readable at the target surface size (slide: 1920×1080 minimum font 24px in the rendered output; print: equivalent of 14px at final print DPI). If the image is going into a slide and the preview shows tiny text, regenerate with a "LARGER TEXT" emphasis in the prompt rather than shipping as-is.
- **Maximum number of concept panels per image.** Four. Beyond four, the text gets too small and the model's spelling starts failing. Split into multiple images.

## Cross-references

- `../amw-design-principles/SKILL.md` — orchestrator. The three hard rules (context before designing, at least three variants, reject AI slop) apply here — except that the "three variants" rule in a single Gemini session is expensive, so for this skill the variants step means three different *concepts / compositions* offered to the user **before** any call is made, not three separate Gemini calls.
- `../amw-design-principles/ai-slop-avoid.md` — this skill is a **documented exception** to item 3 (AI-drawn illustrations), **only** within the strict constraints stated at the top of this file. Do not extend to non-Excalidraw illustration requests.
- `../amw-design-principles/color-system.md` — palette discipline: if the user has supplied design tokens (rust accent, sage accent, etc.) prefer those colors over arbitrary ones when writing the prompt. Do not emit raw `#000` / `#fff` as palette instructions — use named color roles from design-principles when available.
- `../amw-design-principles/typography-system.md` — target font-size floors inside the generated image must respect the slide / body / mobile minimums named there.
- `../amw-ascii-sketch/SKILL.md` — when the user has not committed to an illustration yet and just wants concept ideas, route through `ascii-sketch` first to pick a composition cheaply before paying the Gemini cost.
- `../amw-diagram-editorial/SKILL.md`, `../amw-diagram-architecture/SKILL.md`, `../amw-diagram-svg/SKILL.md` — route to these instead when the user actually wants a structured diagram (flowchart, architecture, sequence) rather than a hand-drawn illustration. Excalidraw-style is for concept / teaching / whiteboard feel, not for structured system diagrams.
- `../amw-svg-creator/SKILL.md` — route there for icons, logos, and purely technical SVG geometry (gated in its own way).
- `/amw-doctor` — reports `GEMINI_API_KEY` presence alongside `ANTHROPIC_API_KEY`.
- `/amw-init` Section 7 — optional Pillow install for the two-phase overlay fallback.
- `references/prompt-template-en.md` / `references/prompt-template-es.md` — filled-in prompt examples.
- `scripts/generate.py` — the two-phase (visual-first, text-overlay-second) fallback generator with Pillow.
- Source inspiration: [Ray Amjad](https://github.com/theramjad) — the AI-generated Excalidraw-style illustrations and the narrative-prompt approach that the original source skill was modelled on; the in-prompt "text in frames, many icons, narrative scenes" pattern comes from that work.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `excalidraw-illustrations` is the user asking about?
  - **aspect** (1 techniques)
    - [TECH-aspect-ratio-selection](./references/TECH-aspect-ratio-selection.md) — TECH-aspect-ratio-selection
  - **framed** (1 techniques)
    - [TECH-framed-text-no-floating](./references/TECH-framed-text-no-floating.md) — TECH-framed-text-no-floating
  - **gemini** (1 techniques)
    - [TECH-gemini-pro-vs-flash-model-choice](./references/TECH-gemini-pro-vs-flash-model-choice.md) — TECH-gemini-pro-vs-flash-model-choice
  - **letter** (1 techniques)
    - [TECH-letter-by-letter-spelling-block](./references/TECH-letter-by-letter-spelling-block.md) — TECH-letter-by-letter-spelling-block
  - **prompt** (1 techniques)
    - [TECH-prompt-template-structure](./references/TECH-prompt-template-structure.md) — TECH-prompt-template-structure
  - **reference** (1 techniques)
    - [TECH-reference-image-priming](./references/TECH-reference-image-priming.md) — TECH-reference-image-priming
  - **two** (1 techniques)
    - [TECH-two-phase-visual-then-overlay](./references/TECH-two-phase-visual-then-overlay.md) — TECH-two-phase-visual-then-overlay

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-aspect-ratio-selection.md](./references/TECH-aspect-ratio-selection.md)**
  - Description: TECH-aspect-ratio-selection
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-framed-text-no-floating.md](./references/TECH-framed-text-no-floating.md)**
  - Description: TECH-framed-text-no-floating
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-gemini-pro-vs-flash-model-choice.md](./references/TECH-gemini-pro-vs-flash-model-choice.md)**
  - Description: TECH-gemini-pro-vs-flash-model-choice
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-letter-by-letter-spelling-block.md](./references/TECH-letter-by-letter-spelling-block.md)**
  - Description: TECH-letter-by-letter-spelling-block
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-prompt-template-structure.md](./references/TECH-prompt-template-structure.md)**
  - Description: TECH-prompt-template-structure
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-reference-image-priming.md](./references/TECH-reference-image-priming.md)**
  - Description: TECH-reference-image-priming
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-two-phase-visual-then-overlay.md](./references/TECH-two-phase-visual-then-overlay.md)**
  - Description: TECH-two-phase-visual-then-overlay
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-excalidraw-illustrations/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per `../amw-design-principles/ai-slop-avoid.md` (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.pl`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. Excalidraw-style PNG/SVG illustrations from Gemini API). The output path is determined by **project inference**, NOT hardcoded. See [`../amw-design-principles/references/project-output-routing.md`](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/illustrations/` created fresh)
   - Last-resort scratch: `/tmp/amw-excalidraw-illustrations-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- [path/to/artifact.ext](./path/to/artifact.ext) — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## Non-negotiables

- **Require `GEMINI_API_KEY`.** If the environment variable is unset, abort with a clear error message pointing at https://aistudio.google.com/. Do not fall back to another model; do not prompt the user for the key inline.
- **Require explicit per-call user consent.** Every Gemini call costs money. Ask before each call, not in a loop, not as part of a multi-step script. A single invocation produces a single image.
- **Default to `gemini-3-pro-image-preview`.** Flash is permitted only inside `scripts/generate.py --visual-only` for layout iteration that does not need correct text; never ship a flash image as a final deliverable.
- **Reference images are mandatory.** Do not skip the reference-image block of the prompt — it is what keeps the output style stable across calls.
- **Verify every word.** After every call, read the image back and check spelling. Do not ship un-verified output.
- **Aspect ratio is asked, never assumed silently.** If the user doesn't answer, default to `16:9` and tell them that's what you used.
- **Do not use this skill for non-Excalidraw illustration intent.** Photo-realistic, vector-flat, logo-style, character-illustration — all of those are refused and routed back to `design-principles` with ai-slop-avoid item 3 cited.
- **Do not self-trigger on broad design vocabulary.** `design`, `UI`, `landing page`, `mockup`, `prototype`, `make a picture` — those are `design-principles`' territory and it routes here only when the specific illustration-style constraint is in scope.

## Failure modes

| Symptom | Likely cause | Recovery |
|---|---|---|
| `GEMINI_API_KEY not set` | The user did not export the env var in this shell. | Abort. Tell the user to export `GEMINI_API_KEY` and re-invoke. Do not prompt for the key in chat — the user should control it via their shell / `.env`. |
| HTTP 403 / 429 from Gemini | Quota exceeded or key invalid. | Abort. Surface the raw error to the user. Do not retry — this is a billing / auth issue the user owns. |
| Image generated but text misspelled | Model limitation. | Ask the user whether to regenerate (new paid call) or simplify the label. Never silently regenerate. |
| Text is rendered floating, not in frames | Prompt omitted the "text always in frames / bubbles" rule. | Regenerate with the prompt-template block explicitly included — the rule is load-bearing. |
| Output has a colored background | Prompt allowed color background or didn't specify white. | Regenerate with an explicit "clean white background" line — do NOT try to mask the color in post-processing. |
| Font too small for slide use | Concept had too many panels or too many words per label. | Simplify — fewer panels, fewer words per label — and regenerate. |
| User wanted photorealistic / vector-flat / logo | Wrong skill. | Refuse. Cite ai-slop-avoid item 3. Route back to `design-principles` for a human-asset path or `svg-creator` for icons / logos. |
| `Pillow` missing when using `scripts/generate.py` overlay path | User never ran `/amw-init` Section 7. | Tell the user to run the Pillow install step and re-invoke. Do not bundle Pillow into the hot path; it is only for the fallback. |
