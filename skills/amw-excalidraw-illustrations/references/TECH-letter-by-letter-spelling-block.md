---
name: TECH-letter-by-letter-spelling-block
category: excalidraw-prompt
source: SKILLS-TO-INTEGRATE/diagrams-skills/amw-excalidraw-illustrations-skill-main.zip
also-in: skills/amw-excalidraw-illustrations/references/prompt-template-en.md
---

# TECH-letter-by-letter-spelling-block

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Spell-out format](#spell-out-format)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Forces Gemini to render text correctly by **spelling out every key word
letter by letter in the prompt**. Gemini's image model periodically
transliterates, drops, or substitutes letters in any word longer than
5 characters — the spell-out block is the single biggest quality lever
against text errors.

## When to use

- **Every time the illustration contains text** — which is every
  invocation of this skill because [TECH-framed-text-no-floating](TECH-framed-text-no-floating.md)
  requires framed labels.
- **Every non-trivial word.** Common 3-4 letter words (IF, AND, OR,
  BUT) can be skipped; anything longer or containing accents MUST be
  spelled out.
- **Special emphasis on proper nouns** — author names, brand names,
  technical terms. These fail most often.

## How it works

Structure:

```
TEXT RULES — VERIFY LETTER BY LETTER:
- [WORD1] is spelled [W-O-R-D-1]
- [WORD2] is spelled [W-O-R-D-2]
- [WORD_WITH_ACCENT] is spelled [W-O-R-D space W-I-T-H space A-C-C-E-N-T]
  (with [ACCENT_DESCRIPTION] on the [LETTER])
- Every word must be PERFECTLY SPELLED in correct [LANG]
- The text must be LARGE and LEGIBLE
- Maximum 2-3 words per label
- Every piece of text is always inside a frame or bubble, never floating
```

### Spell-out format

| Input word | Spell-out |
|---|---|
| `REALISM` | `R-E-A-L-I-S-M` |
| `COURBET` | `C-O-U-R-B-E-T` |
| `PARDO BAZÁN` | `P-A-R-D-O space B-A-Z-Á-N (with acute accent on the A)` |
| `CLARÍN` | `C-L-A-R-Í-N (with acute accent on the I)` |

## Minimal example

Spell-out block for an art-history concept (attributed to
[prompt-template-en](prompt-template-en.md)):

```
TEXT RULES — VERIFY LETTER BY LETTER:
- REALISM is spelled R-E-A-L-I-S-M
- NATURALISM is spelled N-A-T-U-R-A-L-I-S-M
- COURBET is spelled C-O-U-R-B-E-T
- MILLET is spelled M-I-L-L-E-T
- DAUMIER is spelled D-A-U-M-I-E-R
- ZOLA is spelled Z-O-L-A
- PARDO BAZÁN is spelled P-A-R-D-O space B-A-Z-Á-N (with acute accent on the A)
- CLARÍN is spelled C-L-A-R-Í-N (with acute accent on the I)
- Every word must be PERFECTLY SPELLED in correct English (and Spanish where used for author names)
- The text must be LARGE and LEGIBLE
- Maximum 2-3 words per label
- Every piece of text is always inside a frame or bubble, never floating
```

## Gotchas

- **Without the spell-out, Gemini WILL transliterate.** "Daumier"
  becomes "Daunier" or "Daumire" roughly 1 in 3 calls. "Courbet"
  becomes "Courvet" or "Coubert". The spell-out cuts the error rate
  roughly 10×.
- **Describe accents explicitly.** "(with acute accent on the A)".
  Gemini sometimes drops the accent even with the spell-out unless
  the diacritic is called out in prose.
- **Use hyphens between letters**, not periods or spaces. Periods get
  parsed as sentence boundaries; spaces get parsed as word boundaries.
  Hyphens are unambiguous.
- **"space" between two words** inside a multi-word spelling. `P-A-R-D-O
  space B-A-Z-Á-N` tells Gemini there's a literal word boundary,
  preventing it from mashing the words together.
- **Even with the spell-out, expect ~1 in 10 calls to still mis-render
  one word.** The hybrid workflow (Phase 1 visual-only via flash +
  Phase 2 Pillow text overlay) is the fallback when the spell-out
  alone doesn't suffice — see [TECH-two-phase-visual-then-overlay](TECH-two-phase-visual-then-overlay.md).
- **Capitalise words that should render all-caps.** Gemini respects
  case; `REALISM` in the spell-out makes the output render REALISM,
  not Realism.

## Cross-references

- [SKILL](../SKILL.md) — rules section
- [prompt-template-en](prompt-template-en.md) / [prompt-template-es](prompt-template-es.md) — complete prompts
  > [prompt-template-es.md] Ejemplo de concepto: "Modernismo, Generación del 98 y Vanguardias — clase de literatura" · Notas sobre esta estructura
  > Example concept: "Realism vs Naturalism — art history lesson" · Notes on this shape
  containing the spell-out block
- [TECH-prompt-template-structure](TECH-prompt-template-structure.md) — the 7-section prompt this fits
  > What it does · When to use · How it works · Section order and purpose · Template skeleton · Minimal example · Gotchas · Cross-references
  into
- [TECH-framed-text-no-floating](TECH-framed-text-no-floating.md) — the related rule on framing
  > What it does · When to use · How it works · Rounded title frame (section headers) · Speech bubble (tag-line commentary) · Labelled callout with filled background (icon labels, attributions) · Minimal example · Gotchas · Cross-references
- [TECH-two-phase-visual-then-overlay](TECH-two-phase-visual-then-overlay.md) — the fallback when spell-out
  > What it does · When to use · How it works · Phase 1 — visual-only generation · Phase 2 — local text overlay via Pillow · Minimal example · Gotchas · Cross-references
  alone isn't enough
