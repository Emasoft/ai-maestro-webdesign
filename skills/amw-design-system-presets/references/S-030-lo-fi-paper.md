---
id: S-030
name: Lo-Fi / Paper / Zine
aesthetic_position: editorial-warm-paper
source_attribution: frontend-design-main/SKILL.md (Anchor 8); reports/batch9-harvest/styles-B.md "Lo-Fi / Paper / Zine"
license: MIT
---

# S-030 — Lo-Fi / Paper / Zine

**Filename:** `references/S-030-lo-fi-paper.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Lo-Fi / Paper / Zine is a deliberate anti-digital aesthetic: a paper-yellow ground (`#E8E0C0`), mixed system fonts deployed simultaneously on the same page (Times + Helvetica + Courier), elements rotated 2–8° with `transform: rotate()`, and a halftone/Risograph misregistration effect (text-shadow offset in the accent color) that simulates imperfect photocopied or screen-printed output. Hard ink-like borders replace any soft shadow; smooth CSS transitions are banned. The intended audience is independent music labels, zine publishers, cultural magazines, counter-culture brands, and any product that signals authenticity through visible imperfection.

## Token block

```css
/* S-030 Lo-Fi / Paper / Zine — complete token block */
:root {
  /* Paper ground — the mandatory base */
  --color-bg:          #E8E0C0;   /* paper yellow — canonical */
  --color-surface:     #EDE4CF;   /* slightly warmer card stock */
  --color-text:        #1A1008;   /* dark ink — warm near-black */
  --color-text-muted:  #5C4A2A;   /* mid-ink brown */
  --color-primary:     #1A1008;   /* ink itself IS the primary */
  --color-accent:      #FF006E;   /* off-register pink — Risograph accent */
  --color-border:      #1A1008;   /* hard ink border — no softness */

  /* Risograph off-register palette */
  --color-riso-pink:   #FF006E;
  --color-riso-teal:   #00CCCC;
  --color-riso-yellow: #FFD700;

  /* Misregistration effect — apply as text-shadow to display headings */
  --misreg:            text-shadow: 3px 0 #FF006E, -3px 0 #00CCCC;

  /* Typography — three distinct system fonts simultaneously, all mandatory */
  --font-display:      'Times New Roman', 'Times', Georgia, serif;
  --font-body:         'Helvetica Neue', 'Helvetica', Arial, sans-serif;
  --font-mono:         'Courier New', 'Courier', monospace;
  --font-handwritten:  'Comic Sans MS', 'Chalkboard SE', cursive;   /* annotation layer */

  /* Spacing & shape */
  --spacing:           8px;
  --radius:            0px;   /* squared rectangles — rounded corners are forbidden */

  /* Shadow — hard ink offset shadow only; NO soft diffusion */
  --shadow:            2px 2px 0 #1A1008;   /* stamp / sticker hard drop */

  /* Rotation — applied inline via style="" or utility class */
  --rotate-cw:         rotate(3deg);    /* clockwise tilt — for cards/stickers */
  --rotate-ccw:        rotate(-2deg);   /* counter-clockwise — for labels */
  /* Use CSS: transform: var(--rotate-cw) or rotate(calc(2deg + var(--tilt, 0deg))) */

  /* Motion — NO smooth motion; static or jump-cut only */
  --motion-duration:   0ms;      /* disable all transitions */
  --motion-easing:     steps(1); /* if motion is used, it must jump-cut */
}
```

```js
// Tailwind theme extension — S-030 Lo-Fi / Paper / Zine
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'lf-bg':        '#E8E0C0',
        'lf-surface':   '#EDE4CF',
        'lf-text':      '#1A1008',
        'lf-muted':     '#5C4A2A',
        'lf-primary':   '#1A1008',
        'lf-accent':    '#FF006E',
        'lf-border':    '#1A1008',
        'lf-riso-pink': '#FF006E',
        'lf-riso-teal': '#00CCCC',
      },
      fontFamily: {
        display:     ['Times New Roman', 'Times', 'Georgia', 'serif'],
        body:        ['Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
        mono:        ['Courier New', 'Courier', 'monospace'],
        handwritten: ['Comic Sans MS', 'Chalkboard SE', 'cursive'],
      },
      borderRadius: {
        lf: '0px',
      },
      boxShadow: {
        lf: '2px 2px 0 #1A1008',
      },
      rotate: {
        'lf-cw':  '3',
        'lf-ccw': '-2',
      },
      transitionDuration: {
        lf: '0ms',
      },
      transitionTimingFunction: {
        lf: 'steps(1)',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if smooth CSS transitions or animations are applied — `transition-duration` must be 0ms or `steps()` only; any `ease`, `linear`, or bezier motion exits the preset
- breaks if `border-radius` exceeds 0px (hard edge only) — the "squared rectangles" constraint is canonical; stamp/sticker shapes may use clip-path, never border-radius
- breaks if a single typeface is used consistently throughout — the mixed-system-font rule requires Times (display) + Helvetica/Arial (body) + Courier (mono) deployed together on the same page; consistent single-font design contradicts the zine aesthetic
- breaks if the background is replaced by a clean white or a cool neutral — the warm paper-yellow `#E8E0C0` is the identity anchor; white backgrounds eliminate the photocopied-paper register
- breaks if soft box-shadows (any `rgba(0,0,0,x)` gaussian blur) replace the hard 2px solid offset shadow — the ink-stamp hard drop is required; gaussian blur reads as digital, not printed
- breaks if elements are precisely aligned with consistent even spacing — visible misalignment, rotation (2–8°), and intentional placement collisions are structural; a precision grid exits the aesthetic
- breaks if the Risograph misregistration text-shadow is removed from display headings — the chromatic aberration effect (`text-shadow: 3px 0 #FF006E, -3px 0 #00CCCC`) is the primary print-artifact signal
- breaks if a custom digital typeface (Google Fonts, variable fonts) replaces the system fonts — only system fonts (Times, Helvetica/Arial, Courier, Comic Sans) are valid; the constraint enforces "what was available on every machine, always"

## Canonical render-test pointer

Render-test: inject tokens from `## Token block` into `references/_test-skeleton.html` (substitute `{{BG}}=#E8E0C0`, `{{SURFACE}}=#EDE4CF`, `{{TEXT}}=#1A1008`, `{{TEXT_MUTED}}=#5C4A2A`, `{{PRIMARY}}=#1A1008`, `{{ACCENT}}=#FF006E`, `{{BORDER}}=#1A1008`, `{{FONT_DISPLAY}}='Times New Roman',serif`, `{{FONT_BODY}}='Helvetica Neue',sans-serif`, `{{FONT_MONO}}='Courier New',monospace`, `{{RADIUS}}=0px`, `{{SHADOW}}=2px 2px 0 #1A1008`, `{{SPACING}}=8px`). Add `transform: rotate(3deg)` to feature cards and `text-shadow: 3px 0 #FF006E, -3px 0 #00CCCC` to the hero heading.

Upstream reference: `frontend-design-main/SKILL.md` Anchor 8 "Lo-Fi / Paper / Zine"; `reports/batch9-harvest/styles-B.md` "Lo-Fi / Paper / Zine" section (ready-to-paste tokens included).

## Render-test verdict

JOD: pending

## Cross-references

- Sibling styles: S-031 Paper Collage (handcraft + torn edges + polaroid, more three-dimensional materiality), S-002 Brutalism (also system fonts + 0 radius + hard shadow, but structured grid and no rotation/misregistration), S-019 Heritage / Warm Editorial (warm cream/sand but smooth motion + organic oval masks), S-014 Editorial Serif (serif-first but precision layout and no rotation)
- Source: `frontend-design-main/SKILL.md` Anchor 8 (MIT); `reports/batch9-harvest/styles-B.md` "Lo-Fi / Paper / Zine" token block.

## Attribution

Direct port from `frontend-design-main` (MIT license). Token values sourced verbatim from `reports/batch9-harvest/styles-B.md` "Lo-Fi / Paper / Zine" ready-to-paste tokens, extended with display/motion tokens. Catalog summary and "breaks-if" invariants are original content authored for this plugin. License: MIT.
