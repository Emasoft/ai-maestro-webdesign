---
id: S-053
name: Restaurant / Food (Warm Orange)
aesthetic_position: industry-themed-oklch
source_attribution: "landing-page-builder-skill-main industry-themed oklch palette family (license unknown — clean-room derivation); reports/batch9-harvest/blocked-B.md #12 entry #29 + #13 industry decision matrix"
license: clean-room derivation (no verbatim copy)
---

# S-053 — Restaurant / Food (Warm Orange)

**Filename:** `skills/amw-design-system-presets/references/S-053-restaurant-food.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Restaurant / Food is the warm-orange slot in the industry-themed oklch palette family — designed for independent restaurants, cafes, bakeries, delivery brands, and food-and-beverage marketing pages where the visual goal is appetite and welcome. The hue centre is roughly 25° (between pure orange at ~40° and rosy red at ~10°), positioned at mid-lightness and high-but-not-neon chroma so the colour reads "warm-cooked-food" rather than "construction-cone safety orange." The background is a cream-paper field with a faint warm tint (no clinical white), text is near-black with a warm undertone, and a soft warm brown is reserved as a secondary accent for footer rules, badges, or hover states. Typography pairs a humanist serif display (Lora, Source Serif 4, or a friendly contemporary serif like Fraunces) with a clean humanist sans body to project hospitality and warmth without slipping into Memphis-style maximalism. The Google-Maps-iframe pattern is at home here — the palette is built to coexist with photographic content. Reach for it when the brief mentions restaurant, cafe, bakery, food-delivery, menu page, or hospitality.

## Token block

```css
/* S-053 Restaurant / Food (Warm Orange) — token block */
:root {
  /* Colors — warm cream field, appetising orange primary, warm brown accent */
  --color-bg:         oklch(0.98 0.012 70);    /* warm cream paper */
  --color-surface:    oklch(0.96 0.015 60);    /* slightly warmer card surface */
  --color-text:       oklch(0.25 0.025 40);    /* warm near-black */
  --color-text-muted: oklch(0.50 0.020 50);    /* warm muted grey */
  --color-text-faint: oklch(0.72 0.018 50);    /* faint label / placeholder */
  --color-primary:    oklch(0.65 0.180 25);    /* warm appetite orange */
  --color-accent:     oklch(0.42 0.080 50);    /* warm brown — secondary, footer, badges */
  --color-border:     oklch(0.90 0.012 50);    /* warm hairline */

  /* Typography — humanist serif display, humanist sans body */
  --font-display: 'Lora', 'Fraunces', 'Source Serif 4', 'Georgia', serif;
  --font-body:    'Inter', 'system-ui', '-apple-system', sans-serif;
  --font-mono:    'iA Writer Mono', 'Fira Code', 'Courier New', monospace;

  /* Geometry — soft moderate radius */
  --spacing:      8px;
  --radius:       12px;                        /* slightly softer than emerald/spa siblings */
  --border-width: 1px;

  /* Shadow — warm-tinted, soft */
  --shadow:       0 1px 3px oklch(0.65 0.180 25 / 0.06);
  --shadow-card:  0 4px 16px oklch(0.65 0.180 25 / 0.08);

  /* Motion */
  --motion-duration: 220ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);
}
```

```js
// tailwind.config.js — theme extension (S-053)
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:           'oklch(0.98 0.012 70)',
        surface:      'oklch(0.96 0.015 60)',
        text:         'oklch(0.25 0.025 40)',
        'text-muted': 'oklch(0.50 0.020 50)',
        'text-faint': 'oklch(0.72 0.018 50)',
        primary:      'oklch(0.65 0.180 25)',
        accent:       'oklch(0.42 0.080 50)',
        border:       'oklch(0.90 0.012 50)',
      },
      fontFamily: {
        display: ['Lora', 'Fraunces', '"Source Serif 4"', 'Georgia', 'serif'],
        body:    ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono:    ['"iA Writer Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
      },
      borderRadius: { DEFAULT: '12px', sm: '8px', md: '12px', lg: '16px' },
      boxShadow: {
        DEFAULT: '0 1px 3px oklch(0.65 0.180 25 / 0.06)',
        card:    '0 4px 16px oklch(0.65 0.180 25 / 0.08)',
        none:    'none',
      },
      transitionDuration: { DEFAULT: '220ms' },
    },
  },
};
```

## "Breaks if" invariants

- breaks if the orange hue rotates below 10° (becomes rosy red — beauty/spa territory) or above 45° (becomes yellow — sustainability/eco territory)
- breaks if `--color-primary` chroma exceeds 0.22 — the orange tips into neon traffic-cone territory and reads as warning rather than appetite
- breaks if `--color-primary` chroma falls below 0.12 — too desaturated, the orange becomes a warm beige and loses its appetite-cueing function entirely
- breaks if a cool blue, cool green, or neutral grey is introduced as a second accent — the warmth axis is structural; cool accents collapse the hospitality read
- breaks if the background is pure white (`#FFFFFF`) — the cream paper tint is what carries the warmth; clinical white feels like a generic SaaS landing instead of a restaurant page
- breaks if the typography pairing flips to all-sans-serif geometric (Space Grotesk, Geist, Inter for display) — the humanist serif display carries the hospitality signal
- breaks if `border-radius` falls to 0 (industrial-cold) or exceeds 24px (consumer-app-bubbly, wrong category)
- breaks if shadows are pure neutral grey — the warm-tinted shadow keeps the page from reading as a SaaS card; flipping to grey shadows breaks the warmth read at the elevation layer

## Canonical render-test pointer

Render-test: inject the token block above into `skills/amw-design-system-presets/references/_test-skeleton.html`, substituting all `{{TOKEN}}` markers. The oklch values are accepted directly by modern browsers (CSS Color Module 4); no conversion required.
Upstream parity source: `landing-page-builder-skill-main` industry-themed oklch palette family entry #29 (Restaurant/Food, warm orange hue ~25°) — clean-room derivation from the documented "appetising, welcoming" description; no verbatim copy of upstream code.

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling industry-oklch presets:** S-046 Industrial/Trust Authority, S-047 Electric Blue Modern, S-048 Healthcare/Medical, S-049 Plumbing/Trades, S-050 Legal/Professional, S-051 Beauty/Spa, S-052 Real Estate / Stable Growth — same palette family, different hue rotation per industry
- **Adjacent warm presets:** S-056 Ember (Bexa single-hue `hsl(22 90% 50%)` — adjacent hue zone with much higher chroma, used for energy/CTA SaaS rather than restaurant hospitality); S-014 Editorial Serif (shared serif-display + sans-body pairing but neutral palette and editorial framing)
- **Source attribution:** `reports/batch9-harvest/blocked-B.md` §12 (entry #29 Restaurant/Food oklch theme) + entry #13 (9-industry decision matrix); `reports/batch9-analysis/MASTER-LEDGER.md` row S-053
