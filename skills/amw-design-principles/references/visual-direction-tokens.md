# Visual Direction Tokens

Loaded by `amw-design-principles` (the orchestrator) and consumed during Phase B.

Eight named visual-direction anchors. Each anchor owns a complete CSS custom-property token
block and a hard "breaks-if" invariant — one visual property whose presence signals the anchor
was not held. Use this file to steer `amw-ascii-sketch` variant selection in Phase A and to
initialize token blocks in Phase B.

**Commit fully to one anchor.** Hybridizing ("Swiss with Brutalist edge") is a category error —
each anchor's signature excludes the others by construction.

## Table of Contents

- [I. Two-Input Derivation Note](#i-two-input-derivation-note)
- [II. Swiss](#ii-swiss)
- [III. Industrial](#iii-industrial)
- [IV. Brutalist](#iv-brutalist)
- [V. Aurora Maximalism](#v-aurora-maximalism)
- [VI. Chaotic Maximalism](#vi-chaotic-maximalism)
- [VII. Retro-Futuristic](#vii-retro-futuristic)
- [VIII. Organic](#viii-organic)
- [IX. Lo-Fi](#ix-lo-fi)

---

## I. Two-Input Derivation Note

When a user provides only a theme color and an intensity keyword, the entire token set can be
derived algorithmically. Two inputs suffice:

1. `--theme-color` — The brand's primary accent hex (e.g., `#E4002B`).
2. `--intensity` — A keyword that scales the dominant dimension of the chosen anchor
   (e.g., shadow depth, glow strength, warmth saturation, rawness level).

All remaining tokens — surface palette, typography stack, radius, shadow, spacing unit — are
derived from those two inputs according to the anchor's rules below. Do not ask the user for
derived tokens; compute them silently.

---

## II. Swiss

**For:** SaaS, DevTools, editorial, publications. Functional clarity.

```css
:root {
  --color-background:  #FFFFFF;         /* pure white or #F7F7F8 */
  --color-surface:     #F7F7F8;
  --color-text:        #000000;
  --color-secondary:   #555555;
  --color-accent:      #E4002B;         /* Swiss Red; or #FF4F00 or #002FA7 — one only */
  --font-heading:      'Akzidenz-Grotesk', 'Helvetica Neue', sans-serif;
  --font-body:         'Akzidenz-Grotesk', 'Helvetica Neue', sans-serif;
  --font-size-base:    16px;
  --border-radius:     0px;             /* or 4px max — no rounded cards */
  --spacing-unit:      8px;
  --shadow:            none;
  --border:            1px solid #000000;  /* hairline rule; visible grid */
}
```

**Breaks if:** warm paper backgrounds, serif display type, grain texture, or centered typography appear.

---

## III. Industrial

**For:** Terminals, CLIs, dashboards, security tools, developer infrastructure.

```css
:root {
  --color-background:  #000000;         /* or warm-black #0B0C0A */
  --color-surface:     #111111;
  --color-text:        #E0E0E0;
  --color-secondary:   #888888;
  --color-accent:      #00E676;         /* one semantic signal: green | red #FF3B30 | amber #FFB800 | lime #C6FF4A */
  --font-heading:      'IBM Plex Mono', 'JetBrains Mono', monospace;
  --font-body:         'IBM Plex Mono', 'JetBrains Mono', monospace;
  --font-size-base:    15px;
  --border-radius:     0px;
  --spacing-unit:      8px;
  --shadow:            none;
  --border:            1px solid #333333;
  --font-variant-numeric: tabular-nums;
}
```

**Breaks if:** serif typography, proportional fonts, warm paper, grain texture, decorative shadows, or rounded corners appear.

---

## IV. Brutalist

**For:** Disruptive startups, art projects, anti-brand statements, raw irreverence.

```css
:root {
  --color-background:  #FFE500;         /* or #FFFFFF | #000000 | #FF0000 | #0000FF — 2-3 competing */
  --color-surface:     #FFFFFF;
  --color-text:        #000000;
  --color-secondary:   #FFFFFF;
  --color-accent:      #FF00FF;         /* or any pure primary that clashes with background */
  --font-heading:      system-ui, 'Helvetica', 'Arial', sans-serif;  /* system fonts only */
  --font-body:         'Times New Roman', serif;
  --font-size-base:    16px;
  --border-radius:     0px;
  --spacing-unit:      16px;
  --shadow:            4px 4px 0px 0px #000000;  /* hard offset, zero blur */
  --border:            2px solid #000000;
}
```

**Breaks if:** web fonts, colors tuned beyond pure primaries, soft shadows, rounded corners, or a centered balanced layout appear.

---

## V. Aurora Maximalism

**For:** Consumer apps, event pages, entertainment products. Bold and vivid.

```css
:root {
  --color-background:  linear-gradient(135deg, #5D34D0, #FF006E, #00F0FF);
  --color-surface:     rgba(255, 255, 255, 0.08);  /* glass panel */
  --color-text:        #FFFFFF;
  --color-secondary:   rgba(255, 255, 255, 0.70);
  --color-accent:      #00F0FF;
  --font-heading:      'PP Neue Machina', 'Inter Variable', sans-serif;
  --font-body:         'Inter Variable', sans-serif;
  --font-size-base:    16px;
  --font-size-display: clamp(4rem, 15vw, 12rem);  /* oversized display */
  --border-radius:     16px;
  --spacing-unit:      8px;
  --shadow:            0 0 40px rgba(0, 240, 255, 0.3);  /* neon glow */
  --border:            1px solid rgba(255, 255, 255, 0.15);
}
```

**Breaks if:** flat backgrounds, warm paper tones, hairline grid rules as primary structure, or a restrained palette appear.

---

## VI. Chaotic Maximalism

**For:** Zine culture, Gen-Z brands, creative agencies that want to break every convention.

```css
:root {
  --color-background:  #FF71CE;         /* clashing palette — hot pink + acid yellow + cyan */
  --color-surface:     #DFFF00;
  --color-text:        #000000;
  --color-secondary:   #00FFFF;
  --color-accent:      #DFFF00;
  --font-heading:      /* deliberately 3+ faces colliding — e.g.: */ 'Impact', sans-serif;
  --font-body:         'Courier New', monospace;
  --font-size-base:    16px;
  --border-radius:     0px;             /* or vary wildly per element */
  --spacing-unit:      16px;
  --shadow:            none;
  --border:            2px solid #000000;
  /* Textures: SVG patterns (squiggles, dots, zigzags) on every surface */
}
```

**Breaks if:** a coherent single palette, a single typeface, whitespace-as-structure, or any 60/30/10 color dominance appears.

---

## VII. Retro-Futuristic

**For:** Synthwave, cyberpunk, terminal nostalgia, gaming UIs, period aesthetic products.

```css
:root {
  --color-background:  #0A0014;         /* pitch black or deep navy-black */
  --color-surface:     #12001E;
  --color-text:        #00FFFF;         /* or phosphor green #00FF41 */
  --color-secondary:   rgba(0, 255, 255, 0.60);
  --color-accent:      #FF006E;         /* magenta + cyan pair; or #00FF41 + #FFB000 */
  --font-heading:      'VT323', 'Orbitron', 'Space Mono', monospace;
  --font-body:         'Space Mono', 'IBM Plex Mono', monospace;
  --font-size-base:    15px;
  --border-radius:     0px;
  --spacing-unit:      8px;
  --shadow:            0 0 10px rgba(0, 255, 255, 0.40);
  --border:            1px solid rgba(0, 255, 255, 0.30);
  /* Texture: CRT scanlines via repeating-linear-gradient on ::before */
}
```

**Breaks if:** flatness, modern geometric sans-serifs (Inter, Söhne), warm paper surfaces, or the absence of glow/texture appear.

---

## VIII. Organic

**For:** Wellness, food, sustainability brands, boutique e-commerce. Tactile warmth.

```css
:root {
  --color-background:  #E8DCC7;         /* sand; or oat #D4B895 — never warm cream #F0+ range */
  --color-surface:     #D6C8AE;
  --color-text:        #2C1A0E;
  --color-secondary:   #6B4F3A;
  --color-accent:      #C66B3D;         /* terracotta; or sage #8B9D83 | ochre #C08E3A */
  --font-heading:      'Freight Display', 'EB Garamond', 'Caslon', serif;
  --font-body:         'Epilogue', 'Greycliff', sans-serif;
  --font-size-base:    17px;
  --border-radius:     24px;            /* 16–32 px; generous rounded corners */
  --spacing-unit:      12px;
  --shadow:            0 4px 24px rgba(44, 26, 14, 0.10);
  --border:            1px solid rgba(139, 90, 60, 0.20);
  /* Texture: SVG feTurbulence grain at 1–3% opacity */
}
```

**Breaks if:** cream backgrounds in the warm `#F0+` range, cold grays, pure whites, pure blacks, or hard-rectangle layouts with zero radius appear. Fraunces is restricted to this anchor; do not use it in other anchors.

---

## IX. Lo-Fi

**For:** Zines, print-inspired personal sites, indie brands, lo-fi music labels.

```css
:root {
  --color-background:  #E8E0C0;         /* paper-yellow — more saturated than cream */
  --color-surface:     #EDE4CF;
  --color-text:        #1A1208;
  --color-secondary:   #5C4A2A;
  --color-accent:      #FF006E;         /* Risograph misregistration channel */
  --color-accent-2:    #00FFCC;
  --font-heading:      'Times New Roman', serif;   /* deliberately mixed: Times + Helvetica + Courier */
  --font-body:         'Helvetica', sans-serif;
  --font-size-base:    16px;
  --border-radius:     0px;             /* but individual elements rotated 2–8° via transform */
  --spacing-unit:      8px;
  --shadow:            none;
  --border:            1px solid #1A1208;
  /* Texture: halftone dots (SVG radial-gradient tile); Risograph: text-shadow 3px 0 #FF006E, -3px 0 #00FFCC */
}
```

**Breaks if:** precision grid alignment, a single typeface, smooth motion, rectangles squared flush to the grid, or a flat paper tone (cream instead of paper-yellow) appear.

---

*Sources: frontend-design / SKILL.md — 8 anchors with breaks-if invariants (MIT); frontend-design-engineer / references / visual-directions.md — 8 token sets (MIT); design-system-is-all-you-need / SKILL.md — two-input derivation pattern (MIT).*
