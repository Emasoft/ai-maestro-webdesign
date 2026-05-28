---
id: S-052
name: Real Estate / Stable Growth (Deep Emerald)
aesthetic_position: industry-themed-oklch
source_attribution: "landing-page-builder-skill-main industry-themed oklch palette family (license unknown — clean-room derivation); reports/batch9-harvest/blocked-B.md #12 entry #28 + #13 industry decision matrix"
license: clean-room derivation (no verbatim copy)
---

# S-052 — Real Estate / Stable Growth (Deep Emerald)

**Filename:** `skills/amw-design-system-presets/references/S-052-real-estate-emerald.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Real Estate / Stable Growth is the deep-emerald slot in the industry-themed oklch palette family — chosen for brokerages, property-listing sites, mortgage advisors, REIT marketing pages, and any service whose customer must trust the seller with a six-or-seven-figure transaction. The visual signature is rooted in green-as-money-and-stability, but pulls the hue toward forest rather than mint: a deep emerald primary at low lightness and moderate chroma, sitting against a light warm-leaning paper field. Text is near-black, text-muted is warm-grey, and the single accent is a refined gold reserved for highlights, premium-tier badges, or hover states on listings. Corner radius is moderate (8–12px) and shadows are subtle and neutral. Typography pairs a transitional serif display (Source Serif 4, Newsreader) with a clean humanist sans body to project established-firm authority. Photography placeholders sit comfortably here — masonry gallery, property maps, filter chips — and the palette is intentionally compatible with photographic warmth. Reach for it when the brief involves real estate listings, mortgage, property management, REIT, or any high-trust transactional service that needs neither tech-SaaS nor luxury aesthetics.

## Token block

```css
/* S-052 Real Estate / Stable Growth (Deep Emerald) — token block */
:root {
  /* Colors — warm light field, deep emerald primary, gold accent */
  --color-bg:         oklch(0.98 0.008 95);    /* warm off-white paper */
  --color-surface:    oklch(0.96 0.010 95);    /* slightly warmer card surface */
  --color-text:       oklch(0.22 0.020 145);   /* near-black with green undertone */
  --color-text-muted: oklch(0.50 0.020 95);    /* warm muted grey */
  --color-text-faint: oklch(0.72 0.018 95);    /* faint label / placeholder */
  --color-primary:    oklch(0.45 0.150 145);   /* deep emerald — interactive + brand */
  --color-accent:     oklch(0.75 0.110 85);    /* refined gold — highlights, premium badges */
  --color-border:     oklch(0.90 0.010 95);    /* warm hairline */

  /* Typography — transitional serif display, humanist sans body */
  --font-display: 'Source Serif 4', 'Newsreader', 'Georgia', serif;
  --font-body:    'Inter', 'system-ui', '-apple-system', sans-serif;
  --font-mono:    'iA Writer Mono', 'Fira Code', 'Courier New', monospace;

  /* Geometry — moderate radius */
  --spacing:      8px;
  --radius:       10px;                        /* canonical midpoint 8–12px */
  --border-width: 1px;

  /* Shadow — subtle, neutral */
  --shadow:       0 1px 3px rgba(0, 0, 0, 0.06);
  --shadow-card:  0 4px 12px rgba(0, 0, 0, 0.08);

  /* Motion */
  --motion-duration: 200ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);
}
```

```js
// tailwind.config.js — theme extension (S-052)
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:           'oklch(0.98 0.008 95)',
        surface:      'oklch(0.96 0.010 95)',
        text:         'oklch(0.22 0.020 145)',
        'text-muted': 'oklch(0.50 0.020 95)',
        'text-faint': 'oklch(0.72 0.018 95)',
        primary:      'oklch(0.45 0.150 145)',
        accent:       'oklch(0.75 0.110 85)',
        border:       'oklch(0.90 0.010 95)',
      },
      fontFamily: {
        display: ['"Source Serif 4"', 'Newsreader', 'Georgia', 'serif'],
        body:    ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono:    ['"iA Writer Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
      },
      borderRadius: { DEFAULT: '10px', sm: '8px', md: '10px', lg: '12px' },
      boxShadow: {
        DEFAULT: '0 1px 3px rgba(0,0,0,0.06)',
        card:    '0 4px 12px rgba(0,0,0,0.08)',
        none:    'none',
      },
      transitionDuration: { DEFAULT: '200ms' },
    },
  },
};
```

## "Breaks if" invariants

- breaks if the green hue rotates below 130 or above 160 — drifting toward yellow-green (~120) reads as eco/sustainability rather than financial stability; drifting toward teal (~170) reads as healthcare instead
- breaks if `--color-primary` lightness exceeds 0.55 — too light and the emerald becomes mint, which signals startup-fintech or wellness, not established real estate authority
- breaks if `--color-primary` chroma exceeds 0.20 — high-saturation green pushes into neon/playful territory; the deep stability read requires restraint
- breaks if a vivid red, vivid blue, or neon accent is introduced — the gold accent is the only chromatic counterpart; introducing a third hue flips the category
- breaks if the background is set to pure white (`#FFFFFF`) — the warm paper tint is structural to the trustworthy-document feel; pure white reads clinical/tech-SaaS
- breaks if the typography pairing flips to all-sans-serif geometric (Space Grotesk, Geist) — the transitional serif display is what carries the established-firm signal
- breaks if `border-radius` falls to 0 (industrial-too-stiff) or exceeds 16px (over-rounded consumer-app)
- breaks if shadows are tinted in any chromatic hue (warm rose, cool blue, etc.) — neutral grey shadow is the constraint that keeps the document-trust character

## Canonical render-test pointer

Render-test: inject the token block above into `skills/amw-design-system-presets/references/_test-skeleton.html`, substituting all `{{TOKEN}}` markers. The oklch values are accepted directly by modern browsers (CSS Color Module 4); no conversion required.
Upstream parity source: `landing-page-builder-skill-main` industry-themed oklch palette family entry #28 (Real Estate / Stable Growth, hue 145°) — clean-room derivation from the documented "deep emerald green, growth-oriented, trust-first" description; no verbatim copy of upstream code.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 124030 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling industry-oklch presets:** S-046 Industrial/Trust Authority, S-047 Electric Blue Modern, S-048 Healthcare/Medical, S-049 Plumbing/Trades, S-050 Legal/Professional, S-051 Beauty/Spa, S-053 Restaurant/Food — same palette family, different hue rotation per industry
- **Adjacent green presets:** S-055 Verdant (Bexa single-hue `hsl(158 58% 40%)` — comparable hue zone but higher lightness and broader SaaS/fintech context, not real-estate-specific); S-014 Editorial Serif (similar typography pairing but neutral palette, no chromatic identity)
- **Source attribution:** `reports/batch9-harvest/blocked-B.md` §12 (entry #28 Real Estate / Stable Growth oklch theme) + entry #13 (9-industry decision matrix); `reports/batch9-analysis/MASTER-LEDGER.md` row S-052
