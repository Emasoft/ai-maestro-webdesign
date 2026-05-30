---
id: S-027
name: Maximalism / Chaotic Maximalism
aesthetic_position: playful-consumer-bold
source_attribution: frontend-design-main/SKILL.md (Anchor 5); atelier-main/SKILL.md (tone B1 #2); blocked-A styles.csv #17
license: MIT
---

# S-027 — Maximalism / Chaotic Maximalism

**Filename:** `references/S-027-maximalism.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Maximalism inverts every principle of restraint: 5+ clashing colors, 3+ typefaces in deliberate collision, extreme element density, overlapping layers, and a sticker-dump compositional logic that rejects whitespace as structure. Two variants coexist — the bright-chaos version (hot pink/acid yellow/cyan on white, Y2K heritage) and the deep-warm-black variant (deep jewel tones + old gold + crimson on a near-black base, more opulent fashion energy). Both share the core invariant: coherence is the enemy. The intended audience is fashion brands, Y2K-revival consumer apps, music/culture properties, and any context where maximalist exuberance signals authenticity.

## Token block

```css
/* S-027 Maximalism — complete token block */
/* Two variant sets; either may be used. Both satisfy the style. */

/* --- Variant A: Bright Chaos (Y2K / neon-pastel clash) --- */
:root[data-variant="bright"] {
  --color-bg:          #F8F4FF;   /* soft off-white base — not pure white */
  --color-surface:     #FFFFFF;
  --color-text:        #0A0A0A;
  --color-text-muted:  #444444;
  --color-primary:     #FF71CE;   /* hot pink */
  --color-accent:      #DFFF00;   /* acid yellow */
  --color-border:      #0A0A0A;   /* hard ink border */

  /* Extended palette — all must be present simultaneously */
  --color-cyan:        #00FFFF;
  --color-violet:      #8B5CF6;
  --color-coral:       #FF6B6B;
  --color-lime:        #BFFF00;

  --font-display:      'Bowlby One', 'Black Han Sans', 'Impact', fantasy;
  --font-body:         'Courier New', 'VT323', monospace;   /* Y2K mono secondary */
  --font-alt:          'Comic Sans MS', 'Chalkboard SE', cursive; /* deliberate clash */
  --font-mono:         'Courier New', 'Courier', monospace;

  --spacing:           8px;
  --radius:            0px;   /* elements with 0 radius */
  --radius-alt:        9999px; /* some elements pill — deliberate inconsistency */
  --shadow:            4px 4px 0 #0A0A0A;   /* hard offset shadow */

  --motion-duration:   120ms;   /* fast, jarring */
  --motion-easing:     steps(4, end);   /* blink/frame-skip motion */
}

/* --- Variant B: Deep Warm Black (jewel-toned opulent) --- */
:root, :root[data-variant="dark"] {
  --color-bg:          #1A0A00;   /* deep warm black */
  --color-surface:     #2A1500;   /* dark warm brown surface */
  --color-text:        #F5F0E8;   /* aged parchment */
  --color-text-muted:  #C4A882;   /* warm gold-adjacent muted */
  --color-primary:     #C9A96E;   /* old gold */
  --color-accent:      #8B0000;   /* deep crimson */
  --color-border:      #C9A96E;   /* gold hairline */

  /* Extended palette — jewel tones layered */
  --color-jewel-1:     #1B4332;   /* dark forest green */
  --color-jewel-2:     #1E3A5F;   /* deep navy */
  --color-jewel-3:     #4A0E4E;   /* deep plum */
  --color-gold-light:  #E8D5A3;   /* lighter parchment gold */

  --font-display:      'Cormorant Garamond', 'Playfair Display', serif;
  --font-body:         'EB Garamond', 'Garamond', Georgia, serif;
  --font-alt:          'Cinzel', 'Trajan Pro', serif;   /* ornate title clash */
  --font-mono:         'Courier New', 'Courier', monospace;

  --spacing:           8px;
  --radius:            0px;   /* sharp edges — ornament, not radius */
  --radius-alt:        2px;
  --shadow:            4px 4px 12px rgba(201,169,110,0.30), 0 0 32px rgba(139,0,0,0.20);

  --motion-duration:   180ms;
  --motion-easing:     cubic-bezier(0.55, 0, 0.45, 1);   /* theatrical snap */
}
```

```js
// Tailwind theme extension — S-027 Maximalism (Variant B / dark — primary registration)
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'max-bg':        '#1A0A00',
        'max-surface':   '#2A1500',
        'max-text':      '#F5F0E8',
        'max-muted':     '#C4A882',
        'max-primary':   '#C9A96E',
        'max-accent':    '#8B0000',
        'max-border':    '#C9A96E',
        /* Variant A extras */
        'max-pink':      '#FF71CE',
        'max-acid':      '#DFFF00',
        'max-cyan':      '#00FFFF',
        'max-violet':    '#8B5CF6',
      },
      fontFamily: {
        display: ['Cormorant Garamond', 'Playfair Display', 'serif'],
        body:    ['EB Garamond', 'Garamond', 'Georgia', 'serif'],
        mono:    ['Courier New', 'Courier', 'monospace'],
      },
      borderRadius: {
        max: '0px',
        'max-pill': '9999px',
      },
      boxShadow: {
        'max-dark':   '4px 4px 12px rgba(201,169,110,.30), 0 0 32px rgba(139,0,0,.20)',
        'max-bright': '4px 4px 0 #0A0A0A',
      },
      transitionTimingFunction: {
        max: 'cubic-bezier(0.55, 0, 0.45, 1)',
      },
      transitionDuration: {
        max: '180ms',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if the palette is reduced to fewer than 4 distinct chromatic hues — the clash requires at minimum 4 colors pulling in different directions; 3 or fewer reads as curated, not maximalist
- breaks if a single typeface is used throughout — 3+ faces are required; the display/body/accent triplet must span at least two font categories (serif + sans, or sans + mono + cursive)
- breaks if elements are evenly spaced and aligned to a consistent grid — visible grid collisions, overlapping layers, and deliberate misalignment are structural, not optional
- breaks if motion uses gentle easing — either fast/jarring steps (Variant A) or theatrical snap (Variant B) is required; ease-in-out kills the chaos register
- breaks if whitespace is used to create breathing room — density IS the aesthetic; open space reads as a different style entirely
- breaks if only one radius value is used across all elements — the deliberate inconsistency (0px on some, pill on others) is an invariant of the chaotic maximalism variant
- breaks if the color palette is harmonized to an analogous or complementary scheme — competing hue vectors are required

## Canonical render-test pointer

Render-test: inject tokens from `## Token block` (Variant B / dark) into `references/_test-skeleton.html` (substitute `{{BG}}=#1A0A00`, `{{SURFACE}}=#2A1500`, `{{TEXT}}=#F5F0E8`, `{{TEXT_MUTED}}=#C4A882`, `{{PRIMARY}}=#C9A96E`, `{{ACCENT}}=#8B0000`, `{{BORDER}}=#C9A96E`, `{{FONT_DISPLAY}}='Cormorant Garamond',serif`, `{{FONT_BODY}}='EB Garamond',serif`, `{{FONT_MONO}}='Courier New',monospace`, `{{RADIUS}}=0px`, `{{SHADOW}}=4px 4px 12px rgba(201,169,110,.30)`, `{{SPACING}}=8px`).

Upstream reference: `frontend-design-main/SKILL.md` Anchor 5 "Chaotic Maximalism"; `reports/batch9-harvest/styles-B.md` "Chaotic Maximalism" section; `reports/batch9-harvest/blocked-A.md` #17 "Maximalism / Dense-Rich".

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 110702 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Sibling styles: S-025 Playful Toy-Like (high-chroma but controlled grid, single typeface), S-024 Candy (controlled chaos with pill radius + bouncy physics), S-028 Art Deco (structured opulent, NOT chaotic), S-042 Memphis (maximalist but with a grid and consistent border convention)
- Source: `reports_dev/batch9/extracted/frontend-design-main/SKILL.md` Anchor 5 (MIT); `reports_dev/batch9/extracted/atelier-main/SKILL.md` tone B1 #2 (MIT); `reports/batch9-harvest/blocked-A.md` #17 token block.

## Attribution

Direct port from `frontend-design-main` (MIT license). Deep-warm-black variant token values sourced from `reports/batch9-harvest/blocked-A.md` #17 "Maximalism / Dense-Rich". Catalog summary and "breaks-if" invariants are original content authored for this plugin. License: MIT.
