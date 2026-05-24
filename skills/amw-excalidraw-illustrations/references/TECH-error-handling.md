---
name: TECH-error-handling
category: excalidraw-illustrations
---

# TECH-error-handling — Symptom → cause → recovery table

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Symptom table](#symptom-table)
- [Cross-references](#cross-references)

## What it does

Lists every known failure mode of the Excalidraw / Gemini-Pro illustration
path with its likely cause and a single canonical recovery action. The
recovery actions are NOT improvisations — they are the only correct fixes
for each row.

## When to use

The moment a Gemini call returns something other than a clean PNG, or the
verification loop spots a defect.

## How it works

Match the observed symptom to a row in the table below. Apply the
"Recovery" action exactly as written. Do NOT chain recoveries — a single
recovery action either resolves the failure or escalates to the user.

## Symptom table

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

## Cross-references

- [TECH-core-call-pattern](./TECH-core-call-pattern.md) — the call to which
  these errors apply.
- [TECH-two-phase-visual-then-overlay](./TECH-two-phase-visual-then-overlay.md)
  — the Pillow-overlay fallback referenced in the table.
- [SKILL](../SKILL.md) — parent skill.
