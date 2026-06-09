---
id: S-043
name: Japanese Dark Editorial (Zutomayo)
aesthetic_position: editorial-warm-paper
source_attribution: batch9 harvest corpus `atelier` (examples/01-resume-zutomayo.html — "FUJITA KURO" resume example; MIT, inferred; no public upstream URL recorded)
license: MIT (inferred)
---

# S-043 — Japanese Dark Editorial (Zutomayo)

**Filename:** `skills/amw-design-system-presets/references/S-043-japanese-dark-editorial.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Japanese Dark Editorial takes its name and aesthetic from the Zutomayo atelier example — a night-time creative portfolio that fuses void-black depths with aged cream type and sparse acid accents. The visual fingerprint is near-total darkness punctuated by small explosions of acid yellow, hot pink, and cyan, set in Shippori Mincho (a Japanese-origin serif available on Google Fonts; the font name is a Latin transliteration) for display and Cormorant Garamond italic for Latin sub-headings. Extreme whitespace signals confidence; paper grain texture (SVG `feTurbulence`, `mix-blend-mode: screen`) adds analogue warmth to the digital void. Intended audience: indie music artists, creative portfolios, night-economy brands, fashion editorials, and dark-mode cultural platforms.

**CJK font note:** Shippori Mincho, Cormorant, and Yomogi are Latin-script font names (transliterations); they are permitted in this file. No actual CJK character text is included.

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #0e0d12;   /* void dark */
  --color-surface:    #17151e;   /* slightly lifted dark surface */
  --color-text:       #e8e2d0;   /* aged cream */
  --color-text-muted: #8a8478;   /* dimmed cream */
  --color-primary:    #e8e2d0;   /* cream as "primary" for type/borders */
  --color-accent:     #f4e54a;   /* acid yellow — use sparingly */
  --color-accent-2:   #ff4d8d;   /* hot pink — secondary accent */
  --color-accent-3:   #5dd6ff;   /* cyan — tertiary accent */
  --color-violet:     #a89cd6;   /* atmospheric wash */
  --color-border:     rgba(232, 226, 208, 0.10);

  /* Typography */
  --font-display: 'Shippori Mincho', 'Cormorant Garamond', 'Georgia', serif;
  --font-body:    'Cormorant Garamond', 'Georgia', 'Times New Roman', serif;
  --font-mono:    'Yomogi', 'Klee One', 'Courier New', cursive;

  /* Geometry */
  --spacing:      8px;
  --radius:       0px;
  --border-width: 1px;

  /* Shadow — none; depth via layered atmospheric gradients */
  --shadow:       none;

  /* Motion */
  --motion-duration: 600ms;
  --motion-easing:   cubic-bezier(0.16, 1, 0.3, 1);

  /* Texture overlay (apply as ::before on body or .page-wrapper) */
  --gradient-atmosphere: radial-gradient(ellipse 80% 60% at 30% 20%, rgba(168,156,214,0.12) 0%, transparent 70%),
                         radial-gradient(ellipse 60% 40% at 70% 80%, rgba(244,229,74,0.06) 0%, transparent 60%);
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#0e0d12',
        surface:     '#17151e',
        text:        '#e8e2d0',
        'text-muted': '#8a8478',
        primary:     '#e8e2d0',
        accent:      '#f4e54a',
        'accent-2':  '#ff4d8d',
        'accent-3':  '#5dd6ff',
        violet:      '#a89cd6',
        border:      'rgba(232,226,208,0.10)',
      },
      fontFamily: {
        display: ['"Shippori Mincho"', '"Cormorant Garamond"', 'Georgia', 'serif'],
        body:    ['"Cormorant Garamond"', 'Georgia', '"Times New Roman"', 'serif'],
        mono:    ['Yomogi', '"Klee One"', '"Courier New"', 'cursive'],
      },
      borderRadius: { DEFAULT: '0px', none: '0px' },
      boxShadow:    { DEFAULT: 'none', none: 'none' },
      transitionDuration: { DEFAULT: '600ms' },
    },
  },
};
```

**Light variant:** Not canonical — this preset is intentionally dark-only. A light variant exits the style.

## "Breaks if" invariants

- breaks if the background is white or any light value (the void dark is the defining structural choice)
- breaks if a sans-serif typeface is used as the body font (the all-serif stack is non-negotiable)
- breaks if more than two accent colors appear prominently on the same screen (acid yellow, hot pink, and cyan are a spectrum — deploy one at a time with extreme restraint)
- breaks if `border-radius` exceeds 2px on any element (0px preferred)
- breaks if blurred drop shadows replace atmospheric gradient depth
- breaks if spacing density increases to card-grid or dashboard mode — extreme whitespace is structural
- breaks if paper grain texture overlay is removed (either SVG `feTurbulence` or CSS noise; `mix-blend-mode: screen` on dark bg)
- breaks if violet atmospheric gradient wash is removed from the page background
- breaks if motion speed drops below 400ms or uses a bounce/spring easing (cinematic slow reveals only)

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `atelier-main/examples/01-resume-zutomayo.html` — "FUJITA KURO / night memoir" resume example. LICENSE: MIT (inferred).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 105040 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-036 Cinematic Dark (film color-grade, large serif, fullscreen hero), S-016 Luxury Dark Warm (gold on near-black, Cinzel+Montserrat), S-015 Fashion Luxury (Didot/Bodoni, museum-frame gallery)
- **Source:** `reports_dev/batch9/extracted/atelier-main/examples/01-resume-zutomayo.html` (MIT, inferred); token block derived from embedded CSS and the harvest entry in `reports/batch9-harvest/styles-A.md`
