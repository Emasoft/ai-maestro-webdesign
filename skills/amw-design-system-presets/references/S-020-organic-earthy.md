---
id: S-020
name: Organic / Earthy / Blob
aesthetic_position: editorial-warm-paper
source_attribution: https://github.com/frontend-design (SKILL.md Anchor 7 Organic, full breaks-if invariants); https://github.com/frontend-design-engineer-skill (visual-directions.md Organic direction); https://github.com/design-system-is-all-you-need (organic token system)
license: MIT (inferred from source repo conventions)
---

# S-020 — Organic / Earthy / Blob

**Filename:** `skills/amw-design-system-presets/references/S-020-organic-earthy.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## Identity

Organic / Earthy / Blob encodes the visual language of hand-grown, seasonal, and material-world brands — farms, botanical studios, sustainable packaging, natural cosmetics, artisan ceramics, and slow-living platforms. The palette is pulled from land: sage (`#8B9D83`), clay (`#B08B6E`), terracotta (`#C66B3D`), ochre (`#C08E3A`), and moss (`#606C38`). The key technical signature is the blob shape: `border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%` (and its multi-value variations) creates asymmetric organic forms that cannot be faked with standard CSS; corners are not rounded, they are shaped. A grain texture overlay — SVG `feTurbulence` at 1-3% opacity — gives every surface the quality of recycled paper or linen fabric. Fraunces (display serif, optical-size aware, with ink-trap details) and Epilogue (humanist sans) are both fonts with visible organic character. Cream and warm-beige backgrounds are structurally forbidden — those belong to Heritage (S-019); this style uses a warm off-white neutral that reads as natural plaster rather than antique paper. Cold greys and pure whites are also forbidden. This style is for brands that need earthy warmth without historical or nostalgic connotations.

## Token block

```css
:root {
  /* Colors */
  --color-bg:          #F2EDE6;
  --color-surface:     #EBE4DB;
  --color-text:        #2A2520;
  --color-text-muted:  #6B6059;
  --color-primary:     #606C38;
  --color-accent:      #C66B3D;
  --color-border:      rgba(96, 108, 56, 0.18);

  /* Extended earth palette */
  --color-sage:        #8B9D83;
  --color-clay:        #B08B6E;
  --color-ochre:       #C08E3A;
  --color-moss:        #606C38;
  --color-terracotta:  #C66B3D;

  /* Typography */
  --font-display: 'Fraunces', 'Freight Text', 'Caslon', Georgia, serif;
  --font-body:    'Epilogue', 'Greycliff CF', 'Source Sans 3', 'Helvetica Neue', sans-serif;
  --font-mono:    'Courier Prime', 'Courier New', monospace;

  /* Spacing */
  --spacing: 8px;

  /* Shape — card radius */
  --radius: 20px;

  /* Blob shape (use on decorative/image elements, NOT on interactive UI) */
  --radius-blob: 30% 70% 70% 30% / 30% 30% 70% 70%;

  /* Shadow */
  --shadow: 0 4px 16px rgba(96, 108, 56, 0.12);

  /* Motion */
  --motion-duration: 400ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);

  /* Grain texture overlay (apply as ::after pseudo on surface elements) */
  --grain-opacity: 0.02;
  /* SVG feTurbulence grain snippet:
     background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg'><filter id='noise'><feTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%25' height='100%25' filter='url(%23noise)'/></svg>");
     background-repeat: repeat;
     opacity: var(--grain-opacity);
  */
}
```

```ts
// Tailwind theme extension
theme: {
  extend: {
    colors: {
      'org-bg':         '#F2EDE6',
      'org-surface':    '#EBE4DB',
      'org-text':       '#2A2520',
      'org-muted':      '#6B6059',
      'org-moss':       '#606C38',
      'org-terracotta': '#C66B3D',
      'org-sage':       '#8B9D83',
      'org-clay':       '#B08B6E',
      'org-ochre':      '#C08E3A',
    },
    fontFamily: {
      display: ['Fraunces', 'Freight Text', 'Caslon', 'Georgia', 'serif'],
      body:    ['Epilogue', 'Source Sans 3', 'Helvetica Neue', 'sans-serif'],
    },
    borderRadius: {
      DEFAULT: '20px',
      sm:      '16px',
      lg:      '32px',
    },
    boxShadow: {
      earth: '0 4px 16px rgba(96,108,56,0.12)',
    },
  },
},
```

## "Breaks if" invariants

- breaks if cream or warm-beige backgrounds (`#F5F0E8`, `#EDE6D6`) are used — those are Heritage (S-019) territory; this style's background must read as natural plaster, not antique paper; the structural marker is `--color-bg: #F2EDE6` (plaster-grey warm) not `#F5F0E8` (parchment)
- breaks if cold greys (`#9CA3AF`, `#6B7280`, any HSL hue 200-280) appear as neutrals — all neutrals must be warm-tinted; cold greys visually separate from the palette and read as corporate
- breaks if pure white (`#FFFFFF`) or pure black (`#000000`) appear — both are structural violations; white reads as clinical/digital, black reads as premium/editorial, neither reads as earthy
- breaks if the blob border-radius (`border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%`) is replaced with standard rounded corners — the asymmetric blob is the technical signature; uniform rounded rectangles read as SaaS
- breaks if grain texture is omitted entirely from surface elements — the grain at 1-3% opacity is what gives the style its handcrafted tactile quality; without it the palette reads as generic warm landing page
- breaks if a geometric sans-serif without humanist character (Inter, Roboto, DM Sans, Space Grotesk) replaces Epilogue — the body typeface must have organic letterforms; geometric sans reads as corporate or developer-tool
- breaks if `--radius` on interactive elements (buttons, cards) drops below 12px — below 12px the style reads as editorial/heritage; the softness is a feature, not a default
- breaks if the shadow uses a pure black tint (`rgba(0,0,0,...)`) — shadows must use a tinted version of the primary earth color (moss green, terracotta, or clay) to maintain chromatic unity

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers with the values above. Apply `--radius-blob` to the hero image and one feature card image. Add the grain overlay as a `::after` pseudo-element at `--grain-opacity: 0.02` on `--color-surface` panels.
Source parity: `frontend-design-main/SKILL.md` (Anchor 7 — Organic, full breaks-if invariants). Compare the feature card row and testimonial block at 1440px.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 129326 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- S-019 Heritage / Warm Editorial — close neighbor; Heritage is historically-coded (antique paper, script accents, oval masks); Organic is botanically-coded (grain texture, blob shapes, earth palette without cream)
- S-018 Understated Elegance — related warm territory but sage-green primary on different surface (`#F4F1EB`); S-018 is more lifestyle-contemporary, S-020 is more botanical-material
- S-042 Memphis / Neo-Memphis — blob shapes appear in both; differ radically in color and density; use S-020 when organic warmth is required, S-042 for chaotic playful energy
- Source: `reports_dev/batch9/extracted/frontend-design-main/SKILL.md` (Anchor 7 — Organic); `reports_dev/batch9/extracted/frontend-design-engineer-skill-main/frontend-design-engineer/references/visual-directions.md` (Organic direction); `reports_dev/batch9/extracted/design-system-is-all-you-need-main/` (organic token system)
