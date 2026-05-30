---
id: S-028
name: Art Deco / Geometric
aesthetic_position: classical-modernist
source_attribution: atelier-main/SKILL.md (tone B1 #9); styles-A "Art Deco / Geometric"; styles-B "Art Deco"
license: MIT
---

# S-028 — Art Deco / Geometric

**Filename:** `references/S-028-art-deco.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Art Deco transposes the 1920s glamour of Chrysler Building ornament and Lalique glass into a digital surface: deep navy or near-black backgrounds, gold (`#D4AF37`) accents, aged cream text, and absolute symmetry. Geometric display serifs (Cinzel, Cormorant) provide the historical weight; thin hairline borders and chevron or sunburst motifs reinforce the period grammar. Zero box-shadows — depth is conveyed entirely through color contrast and layered gold rules, never soft diffusion. The intended audience is luxury fashion, hospitality, fine-dining, theatre, and any product where heritage and opulence are equity, not nostalgia.

## Token block

```css
/* S-028 Art Deco / Geometric — complete token block */
:root {
  /* Colors — the obligatory triad: navy/black + gold + cream */
  --color-bg:          #0D0B1A;   /* deep midnight navy */
  --color-surface:     #16132B;   /* slightly lighter navy card */
  --color-text:        #F5ECD4;   /* aged cream */
  --color-text-muted:  #C2A97A;   /* gold-toned secondary text */
  --color-primary:     #D4AF37;   /* classic art-deco gold */
  --color-accent:      #E8C97A;   /* pale gold highlight */
  --color-border:      #D4AF37;   /* gold hairline — thin and deliberate */

  /* Ornament palette */
  --color-cream:       #F5ECD4;   /* cream — primary text alias */
  --color-navy:        #0D0B1A;   /* deep navy — bg alias */
  --color-gold-dim:    #8A6F25;   /* dark gold for pressed/disabled states */

  /* Border & ornament widths */
  --border-width:      1px;       /* hairline — never thicker than 2px */
  --border-width-rule: 2px;       /* separator rule width */

  /* Typography — geometric serif display mandatory */
  --font-display:      'Cinzel', 'Cormorant Garamond', 'Playfair Display', serif;
  --font-body:         'Cormorant Garamond', 'Lato', 'Montserrat', sans-serif;
  --font-mono:         'Courier New', 'Courier', monospace;

  /* Spacing & shape */
  --spacing:           8px;
  --radius:            1px;   /* 0-2px only; near-sharp edges */

  /* Shadow — none; depth via color contrast only */
  --shadow:            none;

  /* Motion — scroll-reveal stagger; no bounce */
  --motion-duration:   500ms;
  --motion-easing:     cubic-bezier(0.25, 0.46, 0.45, 0.94);   /* ease-out-quad: dignified settle */
}
```

```js
// Tailwind theme extension — S-028 Art Deco / Geometric
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'ad-bg':        '#0D0B1A',
        'ad-surface':   '#16132B',
        'ad-text':      '#F5ECD4',
        'ad-muted':     '#C2A97A',
        'ad-primary':   '#D4AF37',
        'ad-accent':    '#E8C97A',
        'ad-border':    '#D4AF37',
        'ad-gold-dim':  '#8A6F25',
      },
      fontFamily: {
        display: ['Cinzel', 'Cormorant Garamond', 'Playfair Display', 'serif'],
        body:    ['Cormorant Garamond', 'Lato', 'Montserrat', 'sans-serif'],
        mono:    ['Courier New', 'Courier', 'monospace'],
      },
      borderRadius: {
        ad: '1px',
      },
      boxShadow: {
        ad: 'none',
      },
      borderWidth: {
        ad:      '1px',
        'ad-lg': '2px',
      },
      transitionTimingFunction: {
        ad: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
      },
      transitionDuration: {
        ad: '500ms',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if `border-radius` exceeds 4px — geometric period architecture uses sharp right-angle corners; rounded corners are anachronistic to the 1920s vocabulary
- breaks if `box-shadow` is applied (any non-zero shadow value) — the period aesthetic communicates depth through contrast and gold rules, never soft diffusion
- breaks if the gold is replaced by a different chromatic accent (e.g., red, blue, silver) — gold `#D4AF37` ±10 HSL lightness is the defining anchor; silver is an Art Nouveau marker, not Art Deco
- breaks if a sans-serif is used for display text — the period geometric serif (Cinzel or Cormorant) is mandatory for headlines; sans may appear only at caption scale
- breaks if the background is warm (amber, cream, tan base) without the deep navy anchor — the triad requires navy/black as the primary field; Art Deco is not warm by default
- breaks if horizontal rules and symmetric dividers are removed — the structural ornament (hairline gold rules, symmetry axis markers) is load-bearing visual grammar, not decoration
- breaks if motion uses bounce or spring easing — the dignified ease-out-quad is required; playful physics contradict the period formality

## Canonical render-test pointer

Render-test: inject tokens from `## Token block` into `references/_test-skeleton.html` (substitute `{{BG}}=#0D0B1A`, `{{SURFACE}}=#16132B`, `{{TEXT}}=#F5ECD4`, `{{TEXT_MUTED}}=#C2A97A`, `{{PRIMARY}}=#D4AF37`, `{{ACCENT}}=#E8C97A`, `{{BORDER}}=#D4AF37`, `{{FONT_DISPLAY}}='Cinzel',serif`, `{{FONT_BODY}}='Cormorant Garamond',serif`, `{{FONT_MONO}}='Courier New',monospace`, `{{RADIUS}}=1px`, `{{SHADOW}}=none`, `{{SPACING}}=8px`).

Upstream reference: `atelier-main/SKILL.md` tone B1 #9 "Art Deco / Geometric"; `reports/batch9-harvest/styles-A.md` "Art Deco / Geometric" section; `reports/batch9-harvest/styles-B.md` "Art Deco" section.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 103420 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Sibling styles: S-016 Luxury Dark Warm (gold on near-black but with soft 2px radius and subtle shadow — warmer, less geometric), S-015 Fashion Luxury Editorial (museum-frame gallery, Didot/Bodoni, near-white bg), S-001 Swiss (strict geometry but monochrome, no gold), S-041 Bauhaus (geometric shapes but primary palette, no gold)
- Source: `reports_dev/batch9/extracted/atelier-main/SKILL.md` tone B1 #9 (MIT); `reports/batch9-harvest/styles-A.md` "Art Deco / Geometric"; `reports/batch9-harvest/styles-B.md` "Art Deco".

## Attribution

Direct port from `atelier-main` (MIT license). Token values synthesized from the `styles-A.md` "Art Deco / Geometric" section and the task brief token notes. Catalog summary and "breaks-if" invariants are original content authored for this plugin. License: MIT.
