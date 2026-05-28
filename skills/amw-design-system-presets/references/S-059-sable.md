---
id: S-059
name: Sable (Bexa Accent / Dark-First)
aesthetic_position: luxury-editorial-dark-first
source_attribution: "styles-A §Sable (Bexa Accent / Dark-First Style); Bexa-professional-frontend-design-skills-for-ai-agents skills/bexa/SKILL.md. LICENSE: MIT."
license: MIT
---

# S-059 — Sable (Bexa Accent / Dark-First)

**Filename:** `skills/amw-design-system-presets/references/S-059-sable.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Sable is the dark-first cousin of warm minimalism — luxury editorial restraint at near-black with a subtle cool cast. The defining accent `hsl(220 12% 22%)` is intentionally low-chroma and low-luminance: on a dark background it acts as the deepest neutral text/surface; on a light background it reads as a refined sophisticated near-black. Either deployment is correct because Sable is a *register*, not a chromatic punch. The visual fingerprint is a deep cool-cast field (charcoal `#14171C` or near-black) paired with light-weight serif display (Cormorant Garamond at weight 300, Playfair Display Light) and light-weight humanist sans (Lato Light, Inter Light) body. Layouts are low-density, generously spaced, slow-rhythm editorial. Borders are hairline (1px at low-alpha) or absent entirely; surfaces are flat — no shadows, no decorative gradients. Motion is glacial: slow dissolves, no springs, no parallax kinetic. Pairing Sable with warm-toned backgrounds, saturated accents, or bold display grotesques destroys the entire register. Intended audience: luxury fashion houses, premium hospitality, art galleries, high-end editorial publications, fine-jewelry e-commerce, and any product where the brand promise is restraint and discernment rather than energy or accessibility.

## Token block

```css
:root {
  /* Colors — dark-first canonical */
  --color-bg:         #14171C;            /* deep cool-cast near-black */
  --color-surface:    #1C2027;            /* lifted surface */
  --color-surface-2:  #232830;            /* second elevation */
  --color-text:       #E6E4DE;            /* pale warm-tinted ivory */
  --color-text-muted: #8A8B8F;            /* cool muted */
  --color-text-faint: #5A5B60;            /* faint label */
  --color-primary:    hsl(220 12% 22%);   /* Sable — accent (here acts as deep surface) */
  --color-accent:     hsl(220 12% 22%);   /* single-accent system */
  --color-border:     rgba(230, 228, 222, 0.08); /* hairline at low alpha */

  /* Typography — light-weight everywhere */
  --font-display: 'Cormorant Garamond', 'Playfair Display', 'GFS Didot', Georgia, serif;
  --font-body:    'Lato', 'Inter Tight', Inter, system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  --font-weight-display: 300;   /* Cormorant 300 is canonical */
  --font-weight-body:    300;   /* Lato 300 */

  /* Geometry */
  --spacing:      12px;          /* roomier than default to support low-density rhythm */
  --radius:       0px;           /* hairline or none, flat */
  --border-width: 1px;

  /* Shadow — none */
  --shadow:       none;

  /* Motion — glacial dissolve */
  --motion-duration: 600ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.6, 1); /* gentle linear-ish */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#14171C',
        surface:     '#1C2027',
        'surface-2': '#232830',
        text:        '#E6E4DE',
        'text-muted': '#8A8B8F',
        'text-faint': '#5A5B60',
        primary:     'hsl(220 12% 22%)',
        accent:      'hsl(220 12% 22%)',
        border:      'rgba(230, 228, 222, 0.08)',
      },
      fontFamily: {
        display: ['"Cormorant Garamond"', '"Playfair Display"', '"GFS Didot"', 'Georgia', 'serif'],
        body:    ['Lato', '"Inter Tight"', 'Inter', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
      },
      fontWeight:    { display: '300', body: '300' },
      borderRadius:  { DEFAULT: '0px', none: '0px' },
      boxShadow:     { DEFAULT: 'none', none: 'none' },
      transitionDuration: { DEFAULT: '600ms' },
    },
  },
};
```

**Light variant token override (Sable as deep-neutral on light field):**
```css
[data-theme="light"] {
  --color-bg:         #F5F4F1;
  --color-surface:    #FFFFFF;
  --color-surface-2:  #ECEAE4;
  --color-text:       hsl(220 12% 22%);   /* Sable as text */
  --color-text-muted: hsl(220 12% 38%);
  --color-text-faint: hsl(220 12% 56%);
  --color-border:     rgba(20, 23, 28, 0.10);
  --color-primary:    hsl(220 12% 22%);
}
```

## "Breaks if" invariants

- breaks if any background goes warm-toned (cream, ivory, beige) — Sable's cool-cast neutrality is the signature
- breaks if a saturated chromatic accent (warm orange, vivid blue, rose) appears anywhere — Sable is achromatic by definition
- breaks if a bold-weight display (Cormorant 700, Playfair 900, Space Grotesk 800) replaces light-weight serif — light weight IS the luxury signal
- breaks if any `border-radius` exceeds 0px on structural elements (cards, buttons, sections)
- breaks if any drop shadow or decorative elevation appears — Sable is rigorously flat
- breaks if motion duration falls below 400ms or adopts springs/bounces — slow dissolve is the only motion vocabulary
- breaks if information density jumps to data-dashboard levels — the rhythm requires generous whitespace
- breaks if the border-system uses solid lines at full opacity rather than hairlines at 6–10% alpha

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` — Sable named-accent / dark-first style (`hsl(220 12% 22%)` accent, luxury editorial archetype).
Parity threshold: A-class (single-accent token + light-weight serif/sans pair + zero-radius zero-shadow flat surface + glacial motion).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 79417 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling Bexa accents:** S-056 Ember (warm energy CTA), S-057 Plum (creative purple), S-058 Rose Smoke (fashion/beauty rose-red)
- **Adjacent styles:** S-015 Fashion Luxury Editorial (light-mode editorial cousin), S-016 Luxury Dark Warm (warm dark sibling), S-043 Japanese Dark Editorial (atmospheric dark cousin)
- **Source attribution:** `reports/batch9-harvest/styles-A.md` §Sable (Bexa Accent / Dark-First Style); upstream `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` (MIT)
