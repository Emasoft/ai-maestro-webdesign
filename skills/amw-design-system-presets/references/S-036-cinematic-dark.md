---
id: S-036
name: Cinematic Dark / Immersive
aesthetic_position: dark-cinematic-cyber
source_attribution: >
  styles-B.md "Cinematic Dark" (web-designer-plugin-main/README.md Immersive Scroll
  archetype; tasteful-ui-skill-master catalog; frontend-design-engineer-skill-main
  visual-directions.md); styles-A.md "Cinematic / Product Dark" (atelier-main/examples/
  02-product-cinematic.html "OPVS NO. IV"). LICENSE: MIT (atelier, web-designer-plugin,
  tasteful-ui-skill).
license: MIT (all upstream sources)
---

# S-036 — Cinematic Dark / Immersive

**Filename:** `skills/amw-design-system-presets/references/S-036-cinematic-dark.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## Identity

Cinematic Dark is a dark-canvas immersive aesthetic drawn from feature-film colour grading and architectural lighting design. Its visual fingerprint is a near-black void (`#06060A`) carrying a film-stock warmth in the shadows, large-body serif titles that occupy the full hero width, and fullscreen scroll-pinned reveals that feel like advancing frames in a projector. Intended audience: premium product launches, creative portfolios, luxury SaaS landing pages, independent film or record-label sites where every viewport is a staged scene.

## Token block

```css
/* S-036 Cinematic Dark — CSS custom properties */
:root {
  /* Color */
  --color-bg:          #06060A;   /* near-void with imperceptible warm cast */
  --color-surface:     #101018;   /* slightly lighter panel / card surface */
  --color-surface-2:   #1A1A28;   /* elevated surface (modal, tooltip) */
  --color-text:        #EDEDEA;   /* warm off-white — film highlight */
  --color-text-muted:  #8A8A8A;   /* desaturated mid-grey — negative space type */
  --color-primary:     #EDEDEA;   /* primary action matches text (inverted on dark) */
  --color-accent:      #A855F7;   /* one vivid chromatic pop: purple-violet */
  --color-accent-dim:  #7E22CE;   /* dimmed accent for hover/pressed states */
  --color-border:      #1F1F2E;   /* hairline only — barely-visible dark edge */

  /* Typography */
  --font-display: 'Playfair Display', 'Lora', 'Georgia', serif;
  --font-body:    'Inter', 'Helvetica Neue', Arial, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Spacing */
  --spacing: 8px;   /* base unit; hero padding typically 8× = 64px */

  /* Shape */
  --radius: 4px;

  /* Shadow / Glow */
  --shadow: 0 8px 40px rgba(0, 0, 0, 0.6);
  --glow-accent: 0 0 48px rgba(168, 85, 247, 0.25);   /* violet atmospheric bloom */

  /* Motion — cinematic, never snappy */
  --motion-duration: 800ms;
  --motion-easing: cubic-bezier(0.22, 1, 0.36, 1);   /* expo-out decelerate */

  /* Film-grade extras */
  --gradient-hero: linear-gradient(180deg, rgba(6, 6, 10, 0) 0%, #06060A 100%);
  --gradient-vignette: radial-gradient(ellipse at center, transparent 40%, rgba(0, 0, 0, 0.7) 100%);
}
```

```ts
// S-036 Cinematic Dark — Tailwind theme extension
const cinematicDark = {
  colors: {
    bg:          '#06060A',
    surface:     '#101018',
    'surface-2': '#1A1A28',
    text:        '#EDEDEA',
    'text-muted':'#8A8A8A',
    primary:     '#EDEDEA',
    accent:      '#A855F7',
    'accent-dim':'#7E22CE',
    border:      '#1F1F2E',
  },
  fontFamily: {
    display: ['"Playfair Display"', 'Lora', 'Georgia', 'serif'],
    body:    ['Inter', '"Helvetica Neue"', 'Arial', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
  },
  spacing: { base: '8px' },
  borderRadius: { DEFAULT: '4px' },
  boxShadow: {
    DEFAULT: '0 8px 40px rgba(0,0,0,0.6)',
    glow: '0 0 48px rgba(168,85,247,0.25)',
  },
  transitionDuration: { DEFAULT: '800ms' },
  transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.22,1,0.36,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if any background lighter than `#1A1A28` is used for the page canvas
- breaks if border-radius exceeds 8px on any primary UI element
- breaks if a second chromatic accent colour is introduced alongside the primary accent
- breaks if transitions fall below 700ms or use linear/ease-in easing
- breaks if the hero section does not occupy the full viewport height (100vh)
- breaks if a sans-serif display font replaces the serif heading stack
- breaks if the accent colour appears on more than two independent screen regions simultaneously (scarcity rule)
- breaks if drop-shadows are rendered in a colour other than near-black or the accent hue (no grey drop-shadows)
- breaks if the page colour-grading is cold/blue-white rather than slightly warm-shadow / neutral-highlight
- breaks if scroll interactions use `scrollIntoView` rather than smooth positional animation

## Canonical render-test pointer

Render test: inject this file's tokens into `references/_test-skeleton.html` (substituting `{{BG}}` = `#06060A`, `{{SURFACE}}` = `#101018`, `{{TEXT}}` = `#EDEDEA`, `{{TEXT_MUTED}}` = `#8A8A8A`, `{{PRIMARY}}` = `#EDEDEA`, `{{ACCENT}}` = `#A855F7`, `{{BORDER}}` = `#1F1F2E`, `{{FONT_DISPLAY}}` = `'Playfair Display', 'Lora', Georgia, serif`, `{{FONT_BODY}}` = `Inter, sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', monospace`, `{{RADIUS}}` = `4px`, `{{SHADOW}}` = `0 8px 40px rgba(0,0,0,.6)`, `{{SPACING}}` = `8px`).

Upstream parity source: `atelier-main/examples/02-product-cinematic.html` (MIT, inferred).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 116361 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Siblings: S-009 Aurora (gradient-heavy dark), S-010 Cyberpunk (neon-glow dark), S-016 Luxury Dark Warm (gold accent dark)
- Differentiators: S-036 is film-grade warm-shadow dark with serif titles and slow transitions; S-009 has gradient brand colour; S-010 has neon glow + all-caps + 0px radius; S-016 uses gold not violet
- Source: `styles-B.md` "Cinematic Dark" + `styles-A.md` "Cinematic / Product Dark" (atelier MIT)
