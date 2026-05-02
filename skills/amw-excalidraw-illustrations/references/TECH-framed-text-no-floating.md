---
name: TECH-framed-text-no-floating
category: excalidraw-prompt
source: SKILLS-TO-INTEGRATE/diagrams-skills/amw-excalidraw-illustrations-skill-main.zip
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [1. Rounded title frame (section headers)](#1-rounded-title-frame-section-headers)
  - [2. Speech bubble (tag-line commentary)](#2-speech-bubble-tag-line-commentary)
  - [3. Labelled callout with filled background (icon labels, attributions)](#3-labelled-callout-with-filled-background-icon-labels-attributions)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-framed-text-no-floating

## What it does

Requires every piece of text in an Excalidraw illustration to live
**inside a visible frame, speech bubble, or labelled callout with a
filled background** — never floating freely on the white canvas. The
rule turns AI-generated scattered-label slop into composed editorial
illustrations.

## When to use

- **Every illustration** emitted by this skill. Non-negotiable.
- **Every label in the prompt** — write `«Label text»` inside a
  described frame or bubble.
- **Every section title** — always in a rounded frame with a colored
  fill, never as plain text.

Do not allow floating labels even for "pragmatic" short text (dates,
attributions, subtitles). Everything gets framed.

## How it works

Three frame types, each with a specific use:

### 1. Rounded title frame (section headers)

```
Title «SECTION TITLE» in rounded frame with [accent color] background,
large block letters
```

Used for the big section/panel titles. Always accent-colored
background; always block letters; always large.

### 2. Speech bubble (tag-line commentary)

```
Speech bubble: «Life as it is»
```

Speech bubbles are the "hot-take" / quotable element of the
illustration. One per section at most. Short (3-6 words). The tail of
the bubble points at the central illustration of that section.

### 3. Labelled callout with filled background (icon labels, attributions)

```
Labelled icons in frames: hammer («labour»), wheat («rural»)
Bottom frame: «Courbet · Millet · Daumier»
```

The callout frame is smaller than the title frame, rectangular with
rounded corners, soft-fill background (often the accent colour at low
opacity). Icons sit next to their labels inside the same container.

## Minimal example

Prompt excerpt showing all three types:

```
PANEL 1 (left — REALISM, orange palette):
- Title «REALISM» inside a rounded frame with soft-orange background, large block letters
- Central illustration: a worker in a field, drawn with loose strokes
- Speech bubble: «Life as it is»
- Labelled icons in frames: hammer («labour»), wheat («rural»), gaslight («19th c.»)
- Bottom frame: «Courbet · Millet · Daumier»
```

The instruction includes:

- 1 rounded title frame (REALISM title, orange bg)
- 1 speech bubble (Life as it is)
- 3 small labelled-icon frames (hammer, wheat, gaslight)
- 1 bottom attribution frame (authors)

No text floats without a container.

## Gotchas

- **«Guillemets» vs. ASCII quotes.** Use `«…»` to mark in-image text;
  Gemini parses guillemets as "this is the literal text to draw"
  unambiguously. ASCII quotes are sometimes parsed as part of the
  instruction language.
- **Frame backgrounds must have fill, not just outline.** An outline-
  only frame is nearly as bad as no frame — the text still reads as
  floating. Use soft accent colour fills at ~20-40% opacity.
- **Small labels use smaller frames.** A 3-word icon label in a huge
  frame looks wrong; match frame size to text length.
- **Icons go OUTSIDE their label frames**, not inside. Icon (hammer) +
  labelled frame ("labour") as a pair — the icon is drawn free, the
  label is framed.
- **Cohesive palette across frames.** Each panel's frames share the
  panel's accent colour. Mixing orange frames with mint frames inside
  a single panel breaks the two-panel contrast.
- **No text on white alone.** Even a single-word label must have a
  background. If you find yourself tempted to skip the frame "for
  minimalism", that's the AI-slop reflex — frame it anyway.

## Cross-references

- `../SKILL.md` — key principles #1 and #6
- [TECH-prompt-template-structure](TECH-prompt-template-structure.md) — this rule is wired into every
  panel description
- [TECH-reference-image-priming](TECH-reference-image-priming.md) — the reference images demonstrate
  framed-text convention
- [TECH-letter-by-letter-spelling-block](TECH-letter-by-letter-spelling-block.md) — spell-out rules keep the
  framed text readable
- [TECH-two-phase-visual-then-overlay](TECH-two-phase-visual-then-overlay.md) — even Pillow-overlaid text
  sits inside frames drawn by Gemini in Phase 1
