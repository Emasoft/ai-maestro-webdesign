---
id: S-044
name: Dashboard Magazine / FT-style
aesthetic_position: editorial-warm-paper
source_attribution: batch9 harvest corpus `atelier` (examples/05-dashboard-magazine.html; MIT, inferred; no public upstream URL recorded)
license: MIT (inferred)
---

# S-044 — Dashboard Magazine / FT-style

**Filename:** `skills/amw-design-system-presets/references/S-044-dashboard-magazine.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Dashboard Magazine marries the Financial Times warm-cream broadsheet aesthetic with the precision of a data dashboard. The visual fingerprint is warm cream newsprint paper, a masthead header with a 6px top border accent, three-column broadsheet grid, Newsreader variable optical-size serif for display, IBM Plex Sans for navigation and body, and IBM Plex Mono for numbers and tabular data. Accents are a tight editorial set: claret red, warm gold, and forest green — no blues, no purples. Paper grain texture (SVG `feTurbulence`, `mix-blend-mode: multiply`) ties the digital surface to the physical press. No shadows anywhere — elevation is achieved through typographic hierarchy and column rules. Intended audience: financial news products, analytics dashboards, internal reporting tools, research publications, and any platform where data credibility and typographic authority are the primary trust signals.

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #fef3e6;   /* warm cream newsprint */
  --color-surface:    #fef9f0;   /* lifted cream surface */
  --color-text:       #1a1411;   /* dark ink */
  --color-text-muted: #3a2f29;   /* secondary ink */
  --color-primary:    #7d1f3d;   /* claret */
  --color-accent:     #a8732a;   /* gold */
  --color-green:      #2f6b3f;   /* forest green */
  --color-red:        #a82418;   /* alert/negative red */
  --color-border:     #c9b89a;   /* warm rule */
  --color-rule:       #c9b89a;

  /* Typography */
  --font-display: 'Newsreader', 'Playfair Display', 'Georgia', serif;
  --font-body:    'IBM Plex Sans', 'Source Sans 3', 'Helvetica Neue', sans-serif;
  --font-mono:    'IBM Plex Mono', 'JetBrains Mono', 'Courier New', monospace;

  /* Optical-size variable font settings (Newsreader supports opsz 6–72) */
  --font-display-opsz-headline: 'opsz' 36;
  --font-display-opsz-deck:     'opsz' 18;
  --font-display-opsz-caption:  'opsz' 10;

  /* Geometry */
  --spacing:      8px;
  --radius:       0px;
  --border-width: 1px;

  /* Shadow — none (print aesthetic) */
  --shadow:       none;

  /* Masthead accent border */
  --masthead-border: 6px solid var(--color-primary);

  /* Motion — none (print) */
  --motion-duration: 0ms;
  --motion-easing:   linear;
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#fef3e6',
        surface:     '#fef9f0',
        text:        '#1a1411',
        'text-muted': '#3a2f29',
        primary:     '#7d1f3d',
        accent:      '#a8732a',
        green:       '#2f6b3f',
        red:         '#a82418',
        border:      '#c9b89a',
        rule:        '#c9b89a',
      },
      fontFamily: {
        display: ['Newsreader', '"Playfair Display"', 'Georgia', 'serif'],
        body:    ['"IBM Plex Sans"', '"Source Sans 3"', '"Helvetica Neue"', 'sans-serif'],
        mono:    ['"IBM Plex Mono"', '"JetBrains Mono"', '"Courier New"', 'monospace'],
      },
      borderRadius: { DEFAULT: '0px', none: '0px' },
      boxShadow:    { DEFAULT: 'none', none: 'none' },
      transitionDuration: { DEFAULT: '0ms' },
    },
  },
};
```

**Dark variant:** Not canonical for this preset — Dashboard Magazine is print-first, light-always.

## "Breaks if" invariants

- breaks if shadows are introduced (the entire elevation system is typographic and column-rule based)
- breaks if `border-radius` exceeds 0px on any structural element
- breaks if a sans-serif typeface replaces Newsreader in the display/headline role
- breaks if the 3-column broadsheet layout collapses to a single-column card-grid
- breaks if the masthead header structure (publication title + datestamp + 6px top border) is removed
- breaks if the warm cream background is replaced with pure white (`#FFFFFF`) or any cool-toned color
- breaks if blue or purple are introduced as accent colors (claret/gold/green are the only permitted chromatic accents)
- breaks if the paper grain texture overlay is removed
- breaks if IBM Plex Mono is replaced with a proportional font for numeric/tabular data columns

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `atelier-main/examples/05-dashboard-magazine.html`. LICENSE: MIT (inferred).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 112425 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-014 Editorial Serif (Playfair+Lora, deep-red accent, 720px column), S-037 Cream Editorial (Cormorant Garamond, 0px radius, serif-everywhere), S-039 Warm Professional (Source Serif 4, moderate radius)
- **Source:** `reports_dev/batch9/extracted/atelier-main/examples/05-dashboard-magazine.html` (MIT, inferred); `reports_dev/batch9/extracted/atelier-main/SKILL.md` tone B1 #7 "Editorial / Magazine"; `reports/batch9-harvest/styles-A.md` Dashboard Magazine entry
