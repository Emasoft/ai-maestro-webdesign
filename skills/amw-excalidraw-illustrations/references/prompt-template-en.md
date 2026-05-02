## Table of Contents

- [Example concept: "Realism vs Naturalism — art history lesson"](#example-concept-realism-vs-naturalism-art-history-lesson)
- [Notes on this shape](#notes-on-this-shape)


# Prompt template (English) — filled-in example

Worked example of the skill's prompt shape. Use it verbatim as a starting point
and replace the angle-bracket placeholders with the user's concept. The
LLM-visible prompt for Gemini is everything between the two fenced blocks
below.

## Example concept: "Realism vs Naturalism — art history lesson"

```
Generate a HIGH-QUALITY Excalidraw / hand-drawn-style illustration for educational material IN ENGLISH.

FORMAT: Widescreen 16:9.

VISUAL STYLE:
- Loose but DETAILED and expressive strokes, like a professional illustrator
- Clean white background
- Palette: black for lines, soft orange for the REALISM panel, mint green for the NATURALISM panel
- All text inside ROUNDED FRAMES, SPEECH BUBBLES, or LABELLED CALLOUTS with filled backgrounds
- Large hand-drawn arrows connecting the two panels
- Cross-hatched shading for depth

COMPOSITION:
Split the canvas vertically into two panels separated by a hand-drawn vertical line. Each panel has a rounded title frame at top, a central illustration, a speech-bubble callout, 2-3 labelled icons, and a bottom frame listing representative authors.

PANEL 1 (left — REALISM, orange palette):
- Title «REALISM» inside a rounded frame with soft-orange background, large block letters
- Central illustration: a worker in a field, drawn with loose strokes and cross-hatched shading
- Speech bubble: «Life as it is»
- Labelled icons in frames: hammer («labour»), wheat-stalk («rural»), gaslight («19th c.»)
- Bottom frame: «Courbet · Millet · Daumier»

PANEL 2 (right — NATURALISM, mint-green palette):
- Title «NATURALISM» inside a rounded frame with mint-green background, large block letters
- Central illustration: a magnifying glass over a microcosm of small creatures and plants, drawn with loose strokes
- Speech bubble: «Life as science sees it»
- Labelled icons in frames: beaker («method»), genetic-helix («heredity»), hourglass («environment»)
- Bottom frame: «Zola · Pardo Bazán · Clarín»

CONNECTIONS:
- A large hand-drawn horizontal arrow from the left panel's bottom-right to the right panel's bottom-left, labelled «evolves into»
- A dashed hand-drawn timeline band across the bottom with small date markers: «1850», «1880», «1900»

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

Imitate the visual style of the provided reference images faithfully.
```

## Notes on this shape

- **Spell-out block is non-optional.** Without the letter-by-letter spelling,
  Gemini will rename "Daumier" to "Daunier" or "Daumire" at random. The
  spelling pass is the single biggest quality lever.
- **Two accent colors, one per panel.** Three or more colors read busy. If
  there is a third concept, consider a third separate illustration.
- **Author names go in a labelled frame at the bottom.** Floating author
  attributions look like AI slop; framed ones read as a teacher's note.
- **Large hand-drawn arrows for relationships.** Small thin arrows vanish
  visually. Big wobbly ones carry the point.
