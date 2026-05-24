---
name: amw-excalidraw-illustrations
description: Generate hand-drawn Excalidraw-style conceptual illustrations via the Gemini API — white background, rough sketch, in-panel labels. GATED — requires `GEMINI_API_KEY` + per-call consent. Triggers on "Excalidraw-style illustration", "hand-drawn concept diagram", "whiteboard sketch". Does NOT trigger on broad design intent or other diagram formats — routes to design-principles. Use when generating a hand-drawn illustration. Trigger with /amw-create-excalidraw-like-diagram-png.
version: 0.1.0
---

# Excalidraw Illustrations

> **GATED skill.** Requires `GEMINI_API_KEY` in the environment AND explicit user consent before every Gemini call — each call costs real money on Google's Gemini Pro image tier. Do not invoke silently or in a loop.
> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is an executor. Its triggers are narrow — hand-drawn / Excalidraw / whiteboard-style educational illustration only. The orchestrator routes here for conceptual, illustration-heavy slide or document material where the deliberate rough-sketch aesthetic is the point; everything else stays outside this skill.
>
> **Documented exception to [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) item 3 ("no AI-drawn illustrations").** That rule targets AI-painted people, landscapes, and product shots rendered in photoreal or vector-illustration style. This skill is the carved-out exception **only** because its output is tightly constrained: white background, hand-drawn Excalidraw roughness, concept-diagram / whiteboard use case, integrated labelled text. The constraint itself is what keeps the output from looking like generic AI-illustration slop. Do not use this skill for anything that does not meet all four of those constraints.

## Overview

Generates hand-drawn Excalidraw-style conceptual illustrations via the
Gemini API (`gemini-3-pro-image-preview`). PNG output in 16:9, 1:1, or
4:3. Style anchor: white background, rough-sketch aesthetic, text always
inside speech bubbles or labeled frames, max 4 concept panels per image.
GATED — requires `GEMINI_API_KEY` and explicit per-call user consent.

## Activation and position in flow

Callable directly via `/amw-create-excalidraw-like-diagram-png`, or invoked
by the `design-principles` orchestrator during **Phase B** for hand-drawn /
whiteboard aesthetic. **OUTPUT skill — one Gemini call per invocation**;
no automatic iteration. Skill is autonomous: any agent can read this
SKILL.md and the `references/` files and use it directly.

## Trigger conditions

**Fires on:** "Excalidraw-style illustration of <X>", "hand-drawn concept
diagram of <X>", "sketchy educational illustration for <X>", "whiteboard
sketch", "conceptual diagram hand-drawn", "make an Excalidraw of <X>",
"pizarra / whiteboard illustration" (source skill was Spanish — both
vocabularies activate).

**Does NOT fire on:** generic design / draw / UI / landing-page / mockup
intent (those route to `../amw-design-principles/`); flowchart /
architecture / sequence diagram requests (route to the matching
`../amw-diagram-*/` skill); SVG icon / logo / technical figure (route to
`../amw-svg-creator/`); photoreal / vector-flat / character / mascot
requests — refuse and cite [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) item 3.

## Prerequisites

- **System:** `python3 ≥ 3.8` (Gemini REST call + optional Pillow overlay).
- **Python packages:** stdlib-only on the happy path (`urllib`, `json`,
  `base64`). Optional: `Pillow` for the two-phase text-overlay fallback —
  installed by `/amw-init` Section 7 on demand.
- **`GEMINI_API_KEY`** env var (from https://aistudio.google.com/). Abort
  with a clear error if unset; never prompt inline, never fall back.
- **Model:** `gemini-3-pro-image-preview` by default. Flash (`gemini-2.5-flash-image`)
  permitted only in `scripts/generate.py --visual-only` (text WILL be wrong).
- **Reference images:** `references/reference{1,2}.png` ship with the plugin;
  do not swap without explicit user opt-in.
- **Font fallback:** `fonts/Caveat-Variable.ttf` (Pillow overlay path only).

## Cost note (non-negotiable)

Every successful Pro call is billed by Google to the user's Gemini quota —
the plugin has no billing relationship with Google. The skill MUST ask
for explicit per-call consent before sending the HTTP request. Implicit
regeneration after a failed text render is not allowed — the user must
say "regenerate" before a new call goes out.

## Aspect ratio (ask before generating)

The skill asks the user which format to render **before** sending the Gemini call:

| Aspect | When to use |
|---|---|
| `16:9` | Default. Widescreen slides, presentations, video covers. |
| `1:1` | Social posts, document insets, single-icon concept frames. |
| `4:3` | Classic slide format, older decks, print handouts. |

If the user does not specify, default to `16:9` and tell them that's what will be used.

## Core call pattern + prompt template

The full happy-path Python heredoc (≈50 LOC, calls Gemini Pro with the
two reference images base64-embedded) and the canonical prompt-template
shape live in
[TECH-core-call-pattern](references/TECH-core-call-pattern.md).

Filled examples: [prompt-template-en](references/prompt-template-en.md) /
[prompt-template-es](references/prompt-template-es.md).

## Principles (load-bearing — preserve verbatim in every prompt)

1. **Text is part of the drawing**, never floating. Always inside speech
   bubbles, labelled frames, or callouts with filled backgrounds.
2. **Spell out hard words letter-by-letter** in the prompt — biggest single
   quality lever; every model misspells uncommon words without this.
3. **Fewer words, larger.** Max 2-3 words per label.
4. **Narrative composition**, not flat diagrams. Rich scenes with many
   small icons outperform a flat "title + three boxes".
5. **Many small icons.** Each concept has a visual metaphor.
6. **Frames and panels** with rounded borders; 2-3 accent colors max.
7. **Expressive arrows** — large, hand-drawn, labelled.

## Verification loop (MANDATORY)

After every Gemini call: (1) Read the PNG, (2) check every word is spelled
correctly, (3) if any misspelled — ASK whether to regenerate or simplify
(never silently regenerate), (4) show final image path to user. Do not
ship un-verified output and do not invent a text-overlay fix without asking.

## Iteration, fallback, and quality constraints

- **Simplify on stubborn misspellings.** Two Pro calls failing on the same
  word → simplify the label (fewer words, more common synonym), then retry.
- **Visual-only mode** (`scripts/generate.py --visual-only`) calls the flash
  variant for cheap composition iteration; text WILL be wrong — cannot ship.
- **Two-phase Pillow overlay** for pinpoint text corrections — see
  [TECH-two-phase-visual-then-overlay](references/TECH-two-phase-visual-then-overlay.md).
- **White background only.** Slides assume their own background.
- **Minimum font size:** 24 px in rendered slide output (1920×1080);
  print equivalent at final DPI. Regenerate with "LARGER TEXT" if too small.
- **Max 4 concept panels per image.** Beyond 4, text degrades — split.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (three hard
  rules apply; "three variants" means three concepts BEFORE any Gemini call).
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — exception
  to item 3 within stated constraints; never extend beyond Excalidraw.
- [color-system](../amw-design-principles/color-system.md) —
  [typography-system](../amw-design-principles/typography-system.md) — palette + type floors.
- [SKILL](../amw-ascii-sketch/SKILL.md) — pre-Gemini composition pass.
- Sibling routers: [SKILL](../amw-diagram-editorial/SKILL.md), [SKILL](../amw-diagram-architecture/SKILL.md),
  [SKILL](../amw-diagram-svg/SKILL.md), [SKILL](../amw-svg-creator/SKILL.md).
- `/amw-doctor` — reports `GEMINI_API_KEY` presence.
- `/amw-init` Section 7 — optional Pillow install.
- [CATALOG](references/CATALOG.md) — single entry into all `TECH-*.md`.
- [prompt-template-en](references/prompt-template-en.md) /
  [prompt-template-es](references/prompt-template-es.md) — filled examples.
- `scripts/generate.py` — two-phase fallback generator with Pillow.
- Source: Ray Amjad — narrative-prompt approach.

## Instructions

1. Confirm that `GEMINI_API_KEY` is set; this skill is gated — refuse immediately with a cost and key requirement note if absent.
2. Ask for the target aspect ratio (16:9, 1:1, or 4:3) and confirm the concept brief before generating.
3. Build the prompt using the prompt template in `## Prompt template`; fill in the concept, include framed text and icon narrative instructions, and embed the two reference images as base64 style anchors.
4. Call the Gemini API via the Python core call pattern; check for a valid image in the response.
5. Run the verification loop: load the PNG, check for framed text regions and icon density, and iterate (up to the retry budget) if the illustration lacks narrative density.
6. Save the final PNG with a descriptive English filename and report the artifact path and cost estimate.

## Technique selection and references

See [CATALOG](references/CATALOG.md) for the full decision tree (top-down,
by user-intent keyword) and the per-technique TOC index. Every technique in
this skill is documented as a single `TECH-*.md` file under `./references/`.
Read only the file whose topic matches the current need — do not load the
whole reference set.

<!-- end of references -->

## Examples

See [prompt-template-en](references/prompt-template-en.md) and
[prompt-template-es](references/prompt-template-es.md) for filled examples
(Realism vs Naturalism · Modernismo / Generación del 98 / Vanguardias).

## Completion checklist

Before reporting a job complete, verify (FAIL on any item triggers a remediation loop):

- Inputs captured verbatim — no silent paraphrasing.
- At least one `TECH-*.md` consulted and cited.
- Output passes `## Non-negotiables`.
- No AI-slop outside this skill's carved exception.
- PNG inspected for spelling + frame-discipline (verification loop).
- Cross-skill hand-offs documented.
- Filename is descriptive English (`Excalidraw — Realism vs Naturalism.png`, not `out.png`).

## Output

TWO outputs (artifact PNG + job-completion report). Full contract in
[skill-completion-and-output-contract](../amw-design-principles/references/skill-completion-and-output-contract.md)
and [project-output-routing](../amw-design-principles/references/project-output-routing.md).
Report path: `$MAIN_ROOT/reports/webdesigner/<ts>_<slug>_<hash>.md`.
Every artifact MUST be linked from the report.

## Non-negotiables

- **Require `GEMINI_API_KEY`** — abort with clear error if unset, never prompt inline, never fall back.
- **Explicit per-call user consent.** Each call costs money; ask before each one.
- **Default to `gemini-3-pro-image-preview`.** Flash permitted only in `--visual-only` (text WILL be wrong) — never ship.
- **Reference images mandatory.** They are the style anchor.
- **Verify every word** post-call. Never ship un-verified output.
- **Aspect ratio asked, never assumed.** Default `16:9` if user passes.
- **Refuse non-Excalidraw illustration intent** (photo-real / vector-flat /
  character / mascot). Cite ai-slop-avoid item 3.
- **Do not self-trigger on broad design vocabulary** — that's design-principles' territory.

## Error Handling

See [TECH-error-handling](references/TECH-error-handling.md) for the full
symptom → cause → recovery table (8 known failure modes, one canonical
recovery each).
