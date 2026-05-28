---
id: S-051
name: Beauty / Spa (Dusty Rose)
aesthetic_position: industry-themed-oklch
source_attribution: "landing-page-builder-skill-main industry-themed oklch palette (license unknown — clean-room derivation); reports/batch9-harvest/blocked-B.md #12 entry #24 + #13 industry decision matrix"
license: clean-room derivation (no verbatim copy)
---

# S-051 — Beauty / Spa (Dusty Rose)

**Filename:** `skills/amw-design-system-presets/references/S-051-beauty-spa.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Beauty / Spa is one slot in a 9-industry oklch-themed palette family — the visual signature for skincare, wellness studios, day spas, salons, and direct-to-consumer beauty brands where the audience expects softness and warmth rather than tech-SaaS authority. The palette pairs a near-white warm field (oklch with low chroma at a warm hue) against a dusty-rose primary at mid-lightness and mid-chroma, with a peach-toned accent reserved for highlights. There is no chromatic competition: a single rose hue carries every interactive surface, supported by warm-grey text and a soft hairline border. Corner radius is moderate (8–12px), shadows are warm-tinted rather than cool-grey, and typography leans toward humanist serif display with a clean sans body. The result reads as inviting and feminine without falling into pastel-candy territory or stock-photo-and-overlay clichés. Reach for it when the brief mentions skincare, wellness retreat, salon, beauty boutique, esthetician, or aromatherapy.

## Token block

```css
/* S-051 Beauty / Spa (Dusty Rose) — token block */
:root {
  /* Colors — warm white field, dusty rose primary, peach accent */
  --color-bg:         oklch(0.99 0.005 30);    /* warm off-white */
  --color-surface:    oklch(0.97 0.012 25);    /* peach-tinted surface for elevated cards */
  --color-text:       oklch(0.28 0.020 25);    /* warm near-black */
  --color-text-muted: oklch(0.55 0.025 25);    /* warm muted grey */
  --color-text-faint: oklch(0.75 0.020 25);    /* faint label / placeholder */
  --color-primary:    oklch(0.65 0.150 15);    /* dusty rose — interactive + brand */
  --color-accent:     oklch(0.80 0.090 50);    /* peach accent — secondary highlight */
  --color-border:     oklch(0.92 0.010 25);    /* soft warm hairline */

  /* Typography — humanist serif display, clean sans body */
  --font-display: 'Cormorant Garamond', 'Lora', 'Georgia', serif;
  --font-body:    'Inter', 'system-ui', '-apple-system', sans-serif;
  --font-mono:    'iA Writer Mono', 'Fira Code', 'Courier New', monospace;

  /* Geometry — moderate radius, warm shadow */
  --spacing:      8px;
  --radius:       10px;                        /* canonical midpoint 8–12px */
  --border-width: 1px;

  /* Shadow — warm-tinted, soft */
  --shadow:       0 1px 3px oklch(0.65 0.150 15 / 0.06);
  --shadow-card:  0 4px 16px oklch(0.65 0.150 15 / 0.08);

  /* Motion */
  --motion-duration: 250ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);
}
```

```js
// tailwind.config.js — theme extension (S-051)
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:           'oklch(0.99 0.005 30)',
        surface:      'oklch(0.97 0.012 25)',
        text:         'oklch(0.28 0.020 25)',
        'text-muted': 'oklch(0.55 0.025 25)',
        'text-faint': 'oklch(0.75 0.020 25)',
        primary:      'oklch(0.65 0.150 15)',
        accent:       'oklch(0.80 0.090 50)',
        border:       'oklch(0.92 0.010 25)',
      },
      fontFamily: {
        display: ['"Cormorant Garamond"', 'Lora', 'Georgia', 'serif'],
        body:    ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono:    ['"iA Writer Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
      },
      borderRadius: { DEFAULT: '10px', sm: '8px', md: '10px', lg: '12px' },
      boxShadow: {
        DEFAULT: '0 1px 3px oklch(0.65 0.150 15 / 0.06)',
        card:    '0 4px 16px oklch(0.65 0.150 15 / 0.08)',
        none:    'none',
      },
      transitionDuration: { DEFAULT: '250ms' },
    },
  },
};
```

## "Breaks if" invariants

- breaks if a cool-blue or cool-grey is introduced as a second accent — the palette relies on a warm-only chromatic axis (rose + peach), and adding a cool counterpart collapses the spa-warmth read
- breaks if the background is pure white (`#FFFFFF` or `oklch(1 0 0)`) — the warm tint at low chroma is the defining skin, distinguishing this preset from a neutral SaaS palette
- breaks if `--color-primary` chroma exceeds `0.20` — high-saturation rose tips into candy/Memphis territory and loses the "dusty" character
- breaks if `--color-primary` lightness falls below `0.55` — too dark and it reads as burgundy/wine (heritage editorial), not dusty rose
- breaks if a sans-serif geometric display font (Space Grotesk, Plus Jakarta Sans, Geist) replaces the humanist serif — the serif/sans split is structural to the warmth read
- breaks if `border-radius` exceeds 16px (over-rounded, candy) or falls to 0 (sharp, industrial — wrong category entirely)
- breaks if box-shadow uses neutral grey (e.g. `rgba(0,0,0,0.1)`) instead of a warm-tinted shadow — neutral shadows read as clinical, which contradicts the spa/wellness affect
- breaks if more than two chromatic colors appear on a single screen — rose primary + peach accent is the cap; a third chromatic element (e.g. blue, green, purple) flips the visual category

## Canonical render-test pointer

Render-test: inject token block above into `skills/amw-design-system-presets/references/_test-skeleton.html` substituting all `{{TOKEN}}` markers. The oklch values do not require any conversion — modern browsers accept oklch directly in CSS Color Module 4 syntax.
Upstream parity source: `landing-page-builder-skill-main` industry-themed oklch palette (license unknown — values reproduced via clean-room derivation from the documented Beauty/Spa hue + lightness + chroma description; no verbatim copy).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 111073 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling industry-oklch presets:** S-046 Industrial/Trust Authority, S-047 Electric Blue Modern, S-048 Healthcare/Medical, S-049 Plumbing/Trades, S-050 Legal/Professional, S-052 Real Estate / Stable Growth, S-053 Restaurant/Food — same palette family, different hue rotation per industry
- **Adjacent warm presets:** S-058 Rose Smoke (Bexa accent — single hue `hsl(348 62% 46%)`, comparable target audience but darker and more editorial than dusty rose); S-039 Warm Professional (warm paper + business-trust palette, no rose)
- **Source attribution:** `reports/batch9-harvest/blocked-B.md` §12 (entry #24 Beauty/Spa oklch theme) + entry #13 (9-industry decision matrix); `reports/batch9-analysis/MASTER-LEDGER.md` row S-051
