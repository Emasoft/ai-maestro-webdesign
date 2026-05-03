---
name: TECH-prompt-template-structure
category: excalidraw-prompt
source: SKILLS-TO-INTEGRATE/diagrams-skills/amw-excalidraw-illustrations-skill-main.zip
also-in: skills/amw-excalidraw-illustrations/references/prompt-template-en.md
---

# TECH-prompt-template-structure

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Section order and purpose](#section-order-and-purpose)
  - [Template skeleton](#template-skeleton)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Structures every Gemini prompt into **seven mandatory sections** in a
fixed order: format declaration, visual style, composition, per-panel
descriptions, connections, text rules, closing style-matching clause.
The structure is the single biggest quality lever after the reference
images — skipping any section produces drift.

## When to use

- **Every Gemini call** in this skill.
- **When authoring new illustration concepts** — the template fills in
  mechanically from a concept outline.
- **When debugging bad output** — if the result is off, the prompt
  probably skipped or compressed one of the seven sections.

## How it works

### Section order and purpose

1. **Header / format.** One line declaring the illustration style +
   language + aspect ratio.
2. **Visual style.** 5-7 bullet points: stroke style, background, palette,
   text treatment, arrows, shading.
3. **Composition.** 1-2 sentences describing the overall layout (panels,
   columns, reading flow).
4. **Per-panel / per-section.** One block per panel, enumerating title,
   central illustration, speech bubble, labelled icons, bottom frame.
5. **Connections.** How the panels relate to each other (arrows,
   timelines, unifying elements).
6. **Text rules — verify letter by letter.** The spell-out block
   (see [TECH-letter-by-letter-spelling-block](TECH-letter-by-letter-spelling-block.md)).
   > [TECH-letter-by-letter-spelling-block.md] What it does · When to use · How it works · Spell-out format · Minimal example · Gotchas · Cross-references
7. **Closing clause.** "Imitate the visual style of the provided
   reference images faithfully."

### Template skeleton

```
Generate a HIGH-QUALITY Excalidraw / hand-drawn-style illustration for educational material IN [LANG].

FORMAT: [Widescreen 16:9 / Square 1:1 / Classic 4:3].

VISUAL STYLE:
- Loose but DETAILED and expressive strokes, like a professional illustrator
- Clean white background
- Palette: black for lines, [accent 1] for [section 1], [accent 2] for [section 2]
- All text inside ROUNDED FRAMES, SPEECH BUBBLES, or LABELLED CALLOUTS with filled backgrounds
- Large hand-drawn arrows connecting sections
- Cross-hatched shading for depth

COMPOSITION:
[Describe layout: panels, columns, flow, space distribution]

[SECTION / PANEL 1]:
- Title «[TITLE]» in framed header with [color] background, large block letters
- Central illustration: [detailed description]
- Speech bubble: «[Short phrase]»
- Labelled icons in frames: [icon1] («[Label1]»), [icon2] («[Label2]»)
- Bottom frame: «[Authors / data]»

[SECTION / PANEL 2]:
[Same structure ...]

[CONNECTIONS]:
- [Arrows / timelines / unifying elements]

TEXT RULES — VERIFY LETTER BY LETTER:
- [WORD1] is spelled [W-O-R-D-1]
- [WORD2] is spelled [W-O-R-D-2]
- Every word must be PERFECTLY SPELLED in correct [LANG]
- Text must be LARGE and LEGIBLE
- Maximum 2-3 words per label
- All text always inside a frame or bubble, never floating

Imitate the visual style of the provided reference images faithfully.
```

## Minimal example

Concept: "Realism vs Naturalism" — two-panel layout with contrasting
palettes. Attributed to
`skills/amw-excalidraw-illustrations/references/prompt-template-en.md`:

```
Generate a HIGH-QUALITY Excalidraw / hand-drawn-style illustration for educational material IN ENGLISH.

FORMAT: Widescreen 16:9.

VISUAL STYLE:
- Loose but DETAILED expressive strokes
- Clean white background
- Palette: black for lines, soft orange for REALISM panel, mint green for NATURALISM panel
- All text inside ROUNDED FRAMES, SPEECH BUBBLES, or LABELLED CALLOUTS
- Large hand-drawn arrows connecting the two panels
- Cross-hatched shading for depth

COMPOSITION:
Split canvas vertically into two panels separated by a hand-drawn line. Each panel has a rounded title frame at top, a central illustration, a speech bubble, 2-3 labelled icons, and a bottom frame with authors.

PANEL 1 (left — REALISM, orange):
- Title «REALISM» in rounded frame, large block letters
- Central illustration: worker in a field, cross-hatched
- Speech bubble: «Life as it is»
- Labelled icons in frames: hammer («labour»), wheat («rural»), gaslight («19th c.»)
- Bottom frame: «Courbet · Millet · Daumier»

PANEL 2 (right — NATURALISM, mint green):
- Title «NATURALISM» in rounded frame
- Central illustration: magnifying glass over microcosm
- Speech bubble: «Life as science sees it»
- Labelled icons: beaker («method»), DNA helix («heredity»), hourglass («environment»)
- Bottom frame: «Zola · Pardo Bazán · Clarín»

CONNECTIONS:
- Large horizontal arrow between panels labelled «evolves into»
- Dashed timeline band at bottom: «1850», «1880», «1900»

TEXT RULES — VERIFY LETTER BY LETTER:
- REALISM = R-E-A-L-I-S-M
- NATURALISM = N-A-T-U-R-A-L-I-S-M
- COURBET = C-O-U-R-B-E-T
[... rest of spell-out block ...]

Imitate the visual style of the provided reference images faithfully.
```

## Gotchas

- **Don't collapse the panels section into a single blob.** Separate
  `PANEL 1` and `PANEL 2` blocks with the same internal shape keep
  Gemini from merging them.
- **«Guillemets» for in-image text.** The double-angle quotes make it
  crystal-clear what belongs inside the illustration vs. what is
  instruction. ASCII quotes confuse Gemini on edge cases.
- **Two accent colours max per illustration.** Three+ reads busy; if
  there's a third concept, consider a separate illustration.
- **The spell-out block is non-skippable** — even for common English
  words Gemini sometimes mangles. See
  [TECH-letter-by-letter-spelling-block](TECH-letter-by-letter-spelling-block.md).
- **Close with the style-matching clause.** "Imitate the visual style
  of the provided reference images faithfully." Without it, Gemini
  sometimes ignores the references in favour of its own default style.

## Cross-references

- [SKILL](../SKILL.md) — prompt structure overview
- [prompt-template-en](prompt-template-en.md) / [prompt-template-es](prompt-template-es.md) — full worked
  > [prompt-template-es.md] Ejemplo de concepto: "Modernismo, Generación del 98 y Vanguardias — clase de literatura" · Notas sobre esta estructura
  > Example concept: "Realism vs Naturalism — art history lesson" · Notes on this shape
  examples
- [TECH-reference-image-priming](TECH-reference-image-priming.md) — the references this prompt
  > What it does · When to use · How it works · API call shape · Minimal example · Gotchas · Cross-references
  references
- [TECH-letter-by-letter-spelling-block](TECH-letter-by-letter-spelling-block.md) — the spell-out section
  > What it does · When to use · How it works · Spell-out format · Minimal example · Gotchas · Cross-references
- [TECH-framed-text-no-floating](TECH-framed-text-no-floating.md) — the text-in-frames rule
  > What it does · When to use · How it works · Rounded title frame (section headers) · Speech bubble (tag-line commentary) · Labelled callout with filled background (icon labels, attributions) · Minimal example · Gotchas · Cross-references
