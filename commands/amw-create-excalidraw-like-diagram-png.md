---
name: amw-create-excalidraw-like-diagram-png
description: "Shortcut for users who know they want a hand-drawn Excalidraw-style PNG via Gemini API and have their GEMINI_API_KEY ready. GATED — requires explicit per-call cost consent. An agent in Main-agent mode may also invoke skills/amw-excalidraw-illustrations/ directly via the orchestrator after Phase A approval, applying the full range of scene-composition techniques the skill exposes."
---

# /amw-create-excalidraw-like-diagram-png

Thin wrapper over `skills/amw-excalidraw-illustrations/`. The skill does the actual work; this command is the entry-point, cost-consent gate, and early-refusal check.

## Preconditions (non-skippable)

### 1. API key present

```bash
[ -z "$GEMINI_API_KEY" ] && {
  echo "REFUSED: \$GEMINI_API_KEY is not set in the environment."
  echo "Obtain one at https://aistudio.google.com/ > API keys, export it, then re-run."
  exit 1
}
```

If `$GEMINI_API_KEY` is unset, refuse immediately with the message above. Do NOT prompt for the key inline. Do NOT fall back to any other image model. Do NOT swap to a local renderer.

### 2. Explicit cost consent (per call)

**Cost disclosure (shown verbatim before every Gemini call):**

> This command uses the Gemini API and costs money (~$0.01–$0.05 per image depending on resolution and prompt complexity). Each retry is a new Gemini call and a new cost. Respond `yes` or `proceed` to continue. Anything else cancels.

Wait for the user reply. Accept only `yes` or `proceed` (case-insensitive). Any other response (including `sure`, `ok`, `fine`, silence, or no reply) cancels — do NOT infer consent from context.

### 3. PNG-output-only reminder (shown once per invocation)

> Reminder: PNG is output-only. You cannot round-trip this PNG back into an editable diagram — there is no `/amw-modify-png-diagram` command, and Excalidraw scenes rasterized to PNG lose their source geometry. If you want to iterate, keep your prompt AND the Excalidraw scene JSON so you can re-author. For structural-diagram edits, use `/amw-create-or-modify-{ascii,html,svg,mermaid}-diagram` instead.

## Dispatch

1. Read `$ARGUMENTS` as the concept description (natural-language prompt for the hand-drawn illustration).
2. Invoke `skills/amw-excalidraw-illustrations/SKILL.md` with that prompt. The skill handles model selection, reference-image conditioning, Gemini REST call, optional Pillow text-overlay fallback, PNG save, and descriptive-filename conventions.
3. On return, report the saved PNG's absolute path + the Gemini call's approximate cost.
4. If the user asks to regenerate (because text is wrong or style is off), re-enter the cost-consent gate first — every retry is a new paid call.

## Optional flags

- `--aspect 16:9|4:3|1:1|3:4|9:16` — aspect ratio for the PNG (forwarded to the skill).
- `--model pro|flash` — override the default `gemini-3-pro-image-preview` with `gemini-2.5-flash-image`. `flash` is cheaper but produces more text errors — the skill documents the tradeoff.

## Output contract

Exactly one `.png` file at the user's working directory with a descriptive Title-Case filename. No round-trip support.

## Cross-references

- `skills/amw-excalidraw-illustrations/SKILL.md` — the backing skill (does the actual work, documents cost, Gemini model choice, references, Pillow fallback).
- `skills/amw-design-principles/ai-slop-avoid.md` — the generic "no AI-drawn illustrations" rule; this skill is the documented exception because of the hand-drawn-Excalidraw constraint. See the excalidraw-illustrations SKILL.md header note.
- `skills/amw-diagram-formats/references/png.md` — PNG-as-output-only rule (user directive 2026-04-22): no re-entry, no OCR, no round-trip.
- `/amw-create-or-modify-{ascii,html,svg,mermaid}-diagram` — editable-format alternatives if the user needs iteration.
