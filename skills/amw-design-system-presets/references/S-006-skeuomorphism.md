---
id: S-006
name: Skeuomorphism
aesthetic_position: glass-soft-skeuomorphic
source_attribution: design-system-is-all-you-need-main/skeuomorphism.md; styles-B "Skeuomorphism" section
license: MIT
---

# S-006 — Skeuomorphism

**Filename:** `references/S-006-skeuomorphism.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Skeuomorphism replicates the surface properties of physical materials — leather, brushed metal, wood grain, felt — in a digital interface. Every UI element declares its materiality through surface gradients (light-from-above convention), multi-layer realistic drop-shadows, inner highlight borders, and optional texture overlays. The intended audience is anyone who benefits from tactile metaphor: early touch interfaces, audio/instrument apps, note-taking tools, and any product where physical familiarity reduces cognitive load.

## Token block

```css
/* S-006 Skeuomorphism — complete token block */
:root {
  /* Colors */
  --color-bg:          #8B7355;   /* warm leather base */
  --color-surface:     #A0896B;   /* lighter leather face */
  --color-text:        #2C1A0E;   /* dark espresso ink */
  --color-text-muted:  #5C4033;   /* mid-brown secondary */
  --color-primary:     #6B5240;   /* deep leather accent */
  --color-accent:      #C8860A;   /* brass/amber highlight */
  --color-border:      rgba(0,0,0,0.25);

  /* Surface realism */
  --surface-gradient:  linear-gradient(180deg, #A0896B 0%, #6B5240 100%);
  --highlight:         rgba(255,255,255,0.35);   /* inner top highlight */
  --shadow-ambient:    0 1px 3px rgba(0,0,0,0.20);
  --shadow-cast:       0 8px 16px rgba(0,0,0,0.40);
  --shadow-contact:    0 2px 6px rgba(0,0,0,0.30);
  --drop-shadow:       0 1px 3px rgba(0,0,0,0.20), 0 2px 6px rgba(0,0,0,0.30), 0 8px 16px rgba(0,0,0,0.40);
  --inner-highlight:   inset 0 1px 0 rgba(255,255,255,0.35);

  /* Typography */
  --font-display:      'Georgia', 'Palatino Linotype', 'Book Antiqua', serif;
  --font-body:         'Gill Sans', 'Optima', 'Trebuchet MS', sans-serif;
  --font-mono:         'Courier New', 'Courier', monospace;

  /* Spacing & shape */
  --spacing:           8px;
  --radius:            6px;   /* matches physical material rounding */

  /* Shadow composite (canonical --shadow token) */
  --shadow:            0 1px 3px rgba(0,0,0,0.20), 0 2px 6px rgba(0,0,0,0.30), 0 8px 16px rgba(0,0,0,0.40);

  /* Motion */
  --motion-duration:   200ms;
  --motion-easing:     cubic-bezier(0.34, 1.56, 0.64, 1);   /* spring — mechanical press feel */
}
```

```js
// Tailwind theme extension — S-006 Skeuomorphism
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'sku-bg':       '#8B7355',
        'sku-surface':  '#A0896B',
        'sku-text':     '#2C1A0E',
        'sku-muted':    '#5C4033',
        'sku-primary':  '#6B5240',
        'sku-accent':   '#C8860A',
        'sku-border':   'rgba(0,0,0,0.25)',
      },
      fontFamily: {
        display: ['Georgia', 'Palatino Linotype', 'Book Antiqua', 'serif'],
        body:    ['Gill Sans', 'Optima', 'Trebuchet MS', 'sans-serif'],
        mono:    ['Courier New', 'Courier', 'monospace'],
      },
      borderRadius: {
        sku: '6px',
      },
      boxShadow: {
        sku:       '0 1px 3px rgba(0,0,0,.20), 0 2px 6px rgba(0,0,0,.30), 0 8px 16px rgba(0,0,0,.40)',
        'sku-in':  'inset 0 1px 0 rgba(255,255,255,.35)',
      },
      transitionTimingFunction: {
        sku: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
      transitionDuration: {
        sku: '200ms',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if the surface background is a flat solid color with no gradient — the light-from-above gradient is the core materiality signal
- breaks if `border-radius` exceeds 12px — physical materials round gently, not pill-like
- breaks if `box-shadow` is reduced to a single layer — the ambient + contact + cast triple-layer is required to simulate real depth
- breaks if the inner top highlight (`inset 0 1px 0 rgba(255,255,255,0.35)`) is removed — without it surfaces look painted, not molded
- breaks if warm earth palette is replaced by cool or saturated digital colors — all hues must reference a named physical material (leather, brass, wood, felt, stone)
- breaks if typography switches to a geometric sans (e.g., Futura, Inter, DM Sans) — humanist serif/sans only
- breaks if motion uses a linear or generic ease — the spring cubic-bezier is required to simulate mechanical press/release

## Canonical render-test pointer

Render-test: inject tokens from `## Token block` into `references/_test-skeleton.html` (substitute `{{BG}}=#8B7355`, `{{SURFACE}}=#A0896B`, `{{TEXT}}=#2C1A0E`, `{{TEXT_MUTED}}=#5C4033`, `{{PRIMARY}}=#6B5240`, `{{ACCENT}}=#C8860A`, `{{BORDER}}=rgba(0,0,0,0.25)`, `{{FONT_DISPLAY}}='Georgia',serif`, `{{FONT_BODY}}='Gill Sans',sans-serif`, `{{FONT_MONO}}='Courier New',monospace`, `{{RADIUS}}=6px`, `{{SHADOW}}=0 1px 3px rgba(0,0,0,.20),0 2px 6px rgba(0,0,0,.30),0 8px 16px rgba(0,0,0,.40)`, `{{SPACING}}=8px`).

Upstream reference: `design-system-is-all-you-need-main/references/skeuomorphism.md` — realism levels: refined / classic / rich.

## Render-test verdict

JOD: pending

## Cross-references

- Sibling styles: S-004 Glassmorphism (also surface-depth-first, but translucent vs. opaque), S-005 Neumorphism (monochromatic extrusion instead of material texture), S-007 Claymorphism (pastel inflated 3D, not realistic material)
- Source: `design-system-is-all-you-need-main/skeuomorphism.md` (full parametric token system + realism levels). `styles-B "Skeuomorphism"` section in `reports/batch9-harvest/styles-B.md`.

## Attribution

Direct port from `design-system-is-all-you-need-main` (MIT license). Token values sourced from the `styles-B.md` "Skeuomorphism" section (`reports/batch9-harvest/`). Catalog summary and "breaks-if" invariants are original content authored for this plugin. License: MIT.
