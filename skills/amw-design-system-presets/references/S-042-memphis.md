---
id: S-042
name: Memphis / Neo-Memphis
aesthetic_position: playful-consumer-bold
source_attribution: https://github.com/atelier-main/examples/04-landing-memphis.html — "BLOB!" example (MIT, inferred)
license: MIT (inferred)
---

# S-042 — Memphis / Neo-Memphis

**Filename:** `skills/amw-design-system-presets/references/S-042-memphis.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Memphis revives the 1980s Milan design group's spirit — loud, anti-rational, aggressively decorative — and accelerates it into digital consumer product. The visual fingerprint is warm paper ground, a six-accent palette of fully saturated primaries and secondaries, thick ink borders on every container, organic blob shapes as the dominant decorative motif, and the hard offset shadow that transforms depth into a graphic gesture. Bowlby One display type adds carnival weight. Intended audience: DTC consumer brands, music festivals, streetwear shops, NFT drops, and any product whose brief includes the word "fun" twice.

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #fbf3df;   /* warm paper */
  --color-surface:    #fff8e6;   /* slightly lighter paper */
  --color-text:       #1a1610;   /* dark ink */
  --color-text-muted: #6b5e43;
  --color-primary:    #ff5189;   /* hot pink */
  --color-accent:     #2f5cff;   /* electric blue */
  --color-yellow:     #ffcd1f;
  --color-green:      #36c98a;
  --color-coral:      #ff6b3d;
  --color-lilac:      #bca8ff;
  --color-border:     #1a1610;

  /* Typography */
  --font-display: 'Bowlby One', 'Luckiest Guy', 'Impact', sans-serif;
  --font-body:    'Bricolage Grotesque', 'DM Sans', 'Inter', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;
  --font-accent:  'Caveat Brush', 'Caveat', cursive;

  /* Geometry */
  --spacing:      8px;
  --radius:       0px;           /* rectangular containers; blobs use per-element border-radius */
  --border-width: 3px;

  /* Shadow — hard offset, no blur */
  --shadow:       4px 4px 0 #1a1610;

  /* Motion */
  --motion-duration: 150ms;
  --motion-easing:   cubic-bezier(0.34, 1.56, 0.64, 1);  /* spring-like bounce */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:         '#fbf3df',
        surface:    '#fff8e6',
        text:       '#1a1610',
        'text-muted': '#6b5e43',
        primary:    '#ff5189',
        accent:     '#2f5cff',
        yellow:     '#ffcd1f',
        green:      '#36c98a',
        coral:      '#ff6b3d',
        lilac:      '#bca8ff',
        border:     '#1a1610',
      },
      fontFamily: {
        display: ['"Bowlby One"', '"Luckiest Guy"', 'Impact', 'sans-serif'],
        body:    ['"Bricolage Grotesque"', '"DM Sans"', 'Inter', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
        accent:  ['"Caveat Brush"', 'Caveat', 'cursive'],
      },
      borderRadius: { DEFAULT: '0px', blob: '60% 40% 55% 45% / 45% 55% 40% 60%' },
      boxShadow:    { DEFAULT: '4px 4px 0 #1a1610', offset: '6px 6px 0 #1a1610' },
      transitionDuration: { DEFAULT: '150ms' },
    },
  },
};
```

**Dark variant:** Memphis is intentionally light-first (warm paper); a dark variant is non-canonical and exits the preset.

## "Breaks if" invariants

- breaks if the warm paper background (`#fbf3df` or close equivalent) is replaced by white (`#FFFFFF`) or a dark color
- breaks if the 3px ink border convention is removed from containers
- breaks if the offset hard shadow (`4px 4px 0 #000` or per-accent variant) is replaced by blurred drop shadows
- breaks if a serif display typeface replaces Bowlby One (or equivalent carnival-weight display sans)
- breaks if blob/organic shapes are replaced by geometric rectangles as the primary decorative element
- breaks if the palette reduces to fewer than four distinct accent colors (Memphis is many-color by definition)
- breaks if standard `border-radius: 4–8px` replaces organic per-element blob radius on decorative elements
- breaks if corporate or cool-tone brand colors (navy, grey, forest) are introduced as primary palette members

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `atelier-main/examples/04-landing-memphis.html` — "BLOB!" landing page. LICENSE: MIT (inferred).

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling styles:** S-041 Bauhaus (geometric-primary on white, disciplined), S-027 Maximalism (5+ colors, chaos aesthetic), S-024 Candy (hot pink/candy-purple, pill radius, bouncy)
- **Source:** `atelier-main/examples/04-landing-memphis.html` (MIT, inferred); token block derived from embedded CSS in that example
