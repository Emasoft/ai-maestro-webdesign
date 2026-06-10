---
id: S-008
name: Material Design 3
aesthetic_position: material-systems
source_attribution: styles-B "Material Design 3 (M3)"; design-system-is-all-you-need-main/material-design.md; material-3-skill-master/
license: MIT
---

# S-008 — Material Design 3

## Table of Contents

- [Identity](#identity)
- [Token block](#token-block)
- ["Breaks if" invariants](#breaks-if-invariants)
- [Canonical render-test pointer](#canonical-render-test-pointer)
- [Render-test verdict](#render-test-verdict)
- [Cross-references](#cross-references)
- [Attribution](#attribution)

**Filename:** `references/S-008-material-3.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Material Design 3 (M3) is Google's systematic design language grounded in HCT (Hue–Chroma–Tone) color science, a 7-step shape scale, 15 type roles, tonal surface elevation (no drop-shadows), and a 4dp spatial grid. Unlike earlier Material versions, M3 uses tonal palette shifts instead of shadows for depth — a surface at elevation level 3 is tinted with the primary color at 11% opacity. The intended audience is any product targeting Android, web, or cross-platform consistency where component predictability and accessibility compliance (WCAG AA mandatory) are non-negotiable.

## Token block

```css
/* S-008 Material Design 3 — complete token block */
/* Default seed: #6750A4 (M3 baseline purple) */
:root {
  /* M3 role-based color system */
  --color-bg:                    #FFFBFE;   /* md-sys-color-background */
  --color-surface:               #FEF7FF;   /* md-sys-color-surface */
  --color-surface-container:     #F3EDF7;   /* md-sys-color-surface-container */
  --color-surface-container-hi:  #ECE6F0;   /* surface-container-high */
  --color-text:                  #1C1B1F;   /* md-sys-color-on-surface */
  --color-text-muted:            #49454F;   /* md-sys-color-on-surface-variant */
  --color-primary:               #6750A4;   /* md-sys-color-primary (seed) */
  --color-on-primary:            #FFFFFF;   /* md-sys-color-on-primary */
  --color-primary-container:     #EADDFF;   /* md-sys-color-primary-container */
  --color-accent:                #7965AF;   /* md-sys-color-secondary */
  --color-border:                #79747E;   /* md-sys-color-outline */
  --color-border-variant:        #CAC4D0;   /* md-sys-color-outline-variant */

  /* M3 state layers (applied as overlay on the base color) */
  --state-hover:    rgba(103,80,164,0.08);   /* primary at 8% */
  --state-pressed:  rgba(103,80,164,0.12);   /* primary at 12% (focused) */
  --state-dragged:  rgba(103,80,164,0.16);   /* primary at 16% */

  /* M3 tonal elevation (no drop-shadow; tint primary color at each level) */
  --elevation-0:    #FFFBFE;   /* surface (no tint) */
  --elevation-1:    rgba(103,80,164,0.05);   /* +5% primary tint */
  --elevation-2:    rgba(103,80,164,0.08);   /* +8% */
  --elevation-3:    rgba(103,80,164,0.11);   /* +11% */
  --elevation-4:    rgba(103,80,164,0.12);   /* +12% */
  --elevation-5:    rgba(103,80,164,0.14);   /* +14% */

  /* Typography — M3 type scale (Roboto) */
  --font-display:   'Roboto', system-ui, sans-serif;
  --font-body:      'Roboto', system-ui, sans-serif;
  --font-mono:      'Roboto Mono', 'Courier New', monospace;

  /* M3 type scale sizes */
  --type-display-lg:   57px;
  --type-display-md:   45px;
  --type-display-sm:   36px;
  --type-headline-lg:  32px;
  --type-headline-md:  28px;
  --type-headline-sm:  24px;
  --type-body-lg:      16px;
  --type-body-md:      14px;
  --type-body-sm:      12px;
  --type-label-lg:     14px;
  --type-label-sm:     11px;

  /* M3 shape scale (7 steps) */
  --spacing:        4px;   /* 4dp base grid */
  --radius:         12px;  /* md-sys-shape-corner-medium (default for cards) */
  --shape-xs:       4px;   /* ExtraSmall */
  --shape-sm:       8px;   /* Small */
  --shape-md:       12px;  /* Medium */
  --shape-lg:       16px;  /* Large */
  --shape-xl:       28px;  /* ExtraLarge */
  --shape-full:     9999px; /* Full / pill */

  /* Shadow — M3 uses NO drop-shadow; tonal elevation only */
  --shadow:         none;

  /* Motion — M3 standard / emphasized / expressive */
  --motion-duration:        300ms;   /* standard */
  --motion-duration-emph:   500ms;   /* emphasized */
  --motion-duration-expr:   600ms;   /* expressive (spring) */
  --motion-easing:          cubic-bezier(0.2, 0, 0, 1);   /* decelerate */
  --motion-easing-accel:    cubic-bezier(0.3, 0, 1, 1);   /* accelerate */
}
```

```js
// Tailwind theme extension — S-008 Material Design 3
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'm3-bg':               '#FFFBFE',
        'm3-surface':          '#FEF7FF',
        'm3-surface-cont':     '#F3EDF7',
        'm3-text':             '#1C1B1F',
        'm3-text-muted':       '#49454F',
        'm3-primary':          '#6750A4',
        'm3-on-primary':       '#FFFFFF',
        'm3-primary-cont':     '#EADDFF',
        'm3-accent':           '#7965AF',
        'm3-outline':          '#79747E',
        'm3-outline-variant':  '#CAC4D0',
      },
      fontFamily: {
        display: ['Roboto', 'system-ui', 'sans-serif'],
        body:    ['Roboto', 'system-ui', 'sans-serif'],
        mono:    ['Roboto Mono', 'Courier New', 'monospace'],
      },
      borderRadius: {
        'm3-xs':   '4px',
        'm3-sm':   '8px',
        'm3-md':   '12px',
        'm3-lg':   '16px',
        'm3-xl':   '28px',
        'm3-full': '9999px',
      },
      spacing: {
        'm3-4': '4px',
      },
      transitionTimingFunction: {
        'm3-decel': 'cubic-bezier(0.2, 0, 0, 1)',
        'm3-accel': 'cubic-bezier(0.3, 0, 1, 1)',
      },
      transitionDuration: {
        'm3-std':  '300ms',
        'm3-emph': '500ms',
        'm3-expr': '600ms',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if non-tonal flat hex colors are used instead of the M3 role system — the primary/on-primary/primary-container triplet is load-bearing for accessibility
- breaks if `border-radius` deviates from the 7-step shape scale — arbitrary radius values exit the shape system
- breaks if spatial values are not multiples of 4dp — padding, margin, and gap must be 4/8/12/16/24/32px etc.
- breaks if drop-shadows replace tonal elevation — M3 uses no `box-shadow` for depth; only the tonal surface tints signal z-level
- breaks if state layers (hover 8%, pressed 12%, dragged 16%) are omitted from interactive elements — state feedback is system-level, not component-level
- breaks if more than one font family is introduced — M3 uses a single typeface (Roboto or one brand substitute) across all 15 type roles

## Canonical render-test pointer

Render-test: inject tokens into `references/_test-skeleton.html` (substitute `{{BG}}=#FFFBFE`, `{{SURFACE}}=#FEF7FF`, `{{TEXT}}=#1C1B1F`, `{{TEXT_MUTED}}=#49454F`, `{{PRIMARY}}=#6750A4`, `{{ACCENT}}=#7965AF`, `{{BORDER}}=#79747E`, `{{FONT_DISPLAY}}='Roboto',system-ui,sans-serif`, `{{FONT_BODY}}='Roboto',sans-serif`, `{{FONT_MONO}}='Roboto Mono',monospace`, `{{RADIUS}}=12px`, `{{SHADOW}}=none`, `{{SPACING}}=4px`).

Upstream reference: `design-system-is-all-you-need-main/references/material-design.md`; `material-3-skill-master/` full M3 reference; `styles-B.md` "Material Design 3 (M3)" section.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 123929 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Sibling styles: S-017 Corporate Bold (commercial enterprise, not HCT), S-021 Pnalism (ultra-minimal two-tone), S-035 21st.dev/Aceternity (dark-first, glow-based elevation)
- Source: `reports/batch9-harvest/styles-B.md` "Material Design 3"; `reports_dev/batch9/extracted/design-system-is-all-you-need-main/design-system-is-all-you-need/references/material-design.md`; `reports_dev/batch9/extracted/material-3-skill-master/`.

## Attribution

Direct port from `design-system-is-all-you-need-main` (MIT license) and `material-3-skill-master` (MIT license). Primary seed `#6750A4` is the M3 baseline default per Google's Material Design 3 specification. Catalog summary and "breaks-if" invariants are original content authored for this plugin. License: MIT.
