---
id: S-007
name: Claymorphism
aesthetic_position: glass-soft-skeuomorphic
source_attribution: blocked-A #11 (claude-skill-ui-ux-pro-max styles.csv); styles-B section 11
license: MIT
---

# S-007 — Claymorphism

**Filename:** `references/S-007-claymorphism.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Claymorphism renders UI elements as if they were inflated clay or rubber objects, lit uniformly and floating off the canvas. The signature is a triple-layer shadow: a soft outer drop-shadow for lift, a bright inner highlight at the top simulating rounded plastic, and a darkening inner shadow at the bottom deepening the illusion of thickness. Large radius (20-40px), pastel fills, rounded typefaces (Nunito, Poppins), and bounce easing complete the system. Intended for children's apps, consumer wellness tools, playful SaaS, and any product where friendliness is the primary signal.

## Token block

```css
/* S-007 Claymorphism — complete token block */
:root {
  /* Colors — pastel palette */
  --color-bg:          #F0F4FF;   /* soft periwinkle canvas */
  --color-surface:     #FFFFFF;   /* inflated white clay element */
  --color-text:        #1A1A2E;   /* deep navy for contrast */
  --color-text-muted:  #6B7280;   /* gray-blue secondary */
  --color-primary:     #7C6FF7;   /* soft violet */
  --color-accent:      #F97066;   /* coral-red accent */
  --color-border:      rgba(0,0,0,0.06);   /* near-invisible seam */

  /* Claymorphism shadow — the triple-layer signature */
  --clay-shadow:       0 8px 20px rgba(0,0,0,0.15),
                       inset 0 -4px 8px rgba(0,0,0,0.10),
                       inset 0 4px 8px rgba(255,255,255,0.70);

  /* Typography */
  --font-display:      'Nunito', 'Poppins', 'Varela Round', sans-serif;
  --font-body:         'Nunito', 'Poppins', system-ui, sans-serif;
  --font-mono:         'JetBrains Mono', 'Fira Code', monospace;

  /* Spacing & shape */
  --spacing:           8px;
  --radius:            24px;   /* clay inflates generously */

  /* Shadow (canonical --shadow token — the full triple-layer) */
  --shadow:            0 8px 20px rgba(0,0,0,0.15),
                       inset 0 -4px 8px rgba(0,0,0,0.10),
                       inset 0 4px 8px rgba(255,255,255,0.70);

  /* Motion — bounce easing is required */
  --motion-duration:   350ms;
  --motion-easing:     cubic-bezier(0.34, 1.56, 0.64, 1);   /* spring/bounce */
}
```

```js
// Tailwind theme extension — S-007 Claymorphism
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'clay-bg':      '#F0F4FF',
        'clay-surface': '#FFFFFF',
        'clay-text':    '#1A1A2E',
        'clay-muted':   '#6B7280',
        'clay-primary': '#7C6FF7',
        'clay-accent':  '#F97066',
      },
      fontFamily: {
        display: ['Nunito', 'Poppins', 'Varela Round', 'sans-serif'],
        body:    ['Nunito', 'Poppins', 'system-ui', 'sans-serif'],
        mono:    ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      borderRadius: {
        clay: '24px',
      },
      boxShadow: {
        clay: '0 8px 20px rgba(0,0,0,.15), inset 0 -4px 8px rgba(0,0,0,.10), inset 0 4px 8px rgba(255,255,255,.70)',
      },
      transitionTimingFunction: {
        clay: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
      transitionDuration: {
        clay: '350ms',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if `border-radius` drops below 20px — the inflated roundness is the style's primary identity signal
- breaks if the inner top highlight (`inset 0 4px 8px rgba(255,255,255,0.70)`) is removed — without it the element looks flat-pastel rather than 3D-inflated
- breaks if the inner bottom darkening (`inset 0 -4px 8px rgba(0,0,0,0.10)`) is removed — required to close the 3D illusion of thickness
- breaks if color palette uses fully saturated or dark tones — all fills must be pastels (HSL saturation 30-65%, lightness 70-90%)
- breaks if motion easing is linear or sine — bounce/spring cubic-bezier is mandatory; clay must squash and stretch
- breaks if typography switches to a geometric sans with sharp stroke contrast (e.g., Futura, Didot) — rounded letterforms only
- breaks if the outer drop-shadow is replaced with a hard-offset no-blur shadow — clay is soft, not brutalist

## Canonical render-test pointer

Render-test: inject tokens into `references/_test-skeleton.html` (substitute `{{BG}}=#F0F4FF`, `{{SURFACE}}=#FFFFFF`, `{{TEXT}}=#1A1A2E`, `{{TEXT_MUTED}}=#6B7280`, `{{PRIMARY}}=#7C6FF7`, `{{ACCENT}}=#F97066`, `{{BORDER}}=rgba(0,0,0,0.06)`, `{{FONT_DISPLAY}}='Nunito','Poppins',sans-serif`, `{{FONT_BODY}}='Nunito',sans-serif`, `{{FONT_MONO}}='JetBrains Mono',monospace`, `{{RADIUS}}=24px`, `{{SHADOW}}=0 8px 20px rgba(0,0,0,.15),inset 0 -4px 8px rgba(0,0,0,.10),inset 0 4px 8px rgba(255,255,255,.70)`, `{{SPACING}}=8px`).

Upstream reference: `claude-skill-ui-ux-pro-max-main/data/styles.csv` entry "Claymorphism"; `styles-B.md` section 11.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 113398 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Sibling styles: S-006 Skeuomorphism (realistic material vs. inflated clay), S-005 Neumorphism (monochromatic extrusion vs. colorful clay), S-025 Playful Toy-Like (bright primaries vs. soft pastels), S-026 Soft Pastel (flat pastel vs. 3D-inflated pastel)
- Source: `blocked-A.md` section 11 "Claymorphism"; `styles-B.md` section 11.

## Attribution

Direct port from `claude-skill-ui-ux-pro-max-main` styles.csv "Claymorphism" entry (MIT license). Token values cross-referenced with `styles-B.md` section 11 (`reports/batch9-harvest/`). Catalog summary and "breaks-if" invariants are original content authored for this plugin. License: MIT.
