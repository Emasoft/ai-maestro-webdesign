---
id: S-031
name: Paper Collage
aesthetic_position: tactile handcraft editorial warm
source_attribution: https://github.com/MickeyAlton33/web-designer-plugin (MIT)
license: MIT
---

# S-031 — Paper Collage

## Identity

Paper Collage simulates a physical scrapbook assembled from cream paper stock, torn-edge clippings, adhesive tape renders, and hand-lettered or typewriter type. The visual language is derived from analogue craft: off-white ground, warm sepia ink, irregular silhouettes from CSS clip-path, and Polaroid-frame card containers. Intended for journaling apps, handmade-goods brands, and editorial portfolios seeking warmth and authenticity over polish.

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #FAF7F0;
  --color-surface:    #F5EFE0;
  --color-text:       #1A1208;
  --color-text-muted: #6B5744;
  --color-primary:    #2C2416;
  --color-accent:     #B85C3A;
  --color-border:     #D4C5A9;

  /* Typography */
  --font-display: 'Caveat', 'Patrick Hand', 'Comic Sans MS', cursive;
  --font-body:    'Special Elite', 'Courier New', 'Courier', monospace;
  --font-mono:    'Courier New', 'Courier', monospace;

  /* Spacing */
  --spacing: 8px;

  /* Shape */
  --radius: 2px;

  /* Shadow — paper-lift physical feel */
  --shadow: 2px 3px 6px rgba(0, 0, 0, 0.18), 0 1px 2px rgba(0, 0, 0, 0.10);

  /* Motion — snap with slow return (analogue feel) */
  --motion-duration: 400ms;
  --motion-easing:   linear;

  /* Optional — torn-edge clip path helper (override per element) */
  --torn-edge-top: polygon(0% 4%, 3% 0%, 6% 3%, 9% 0%, 12% 2%, 15% 0%, 18% 3%, 21% 0%, 25% 2%, 28% 0%, 32% 3%, 36% 0%, 40% 2%, 44% 0%, 48% 3%, 52% 1%, 56% 0%, 60% 2%, 64% 0%, 68% 3%, 72% 0%, 76% 2%, 80% 0%, 84% 3%, 88% 0%, 92% 2%, 96% 0%, 100% 3%, 100% 100%, 0% 100%);

  /* Optional — adhesive tape pseudo-element color */
  --tape-color: rgba(255, 235, 150, 0.55);
}
```

```ts
// tailwind.config.ts — theme extension
export default {
  theme: {
    extend: {
      colors: {
        bg:        '#FAF7F0',
        surface:   '#F5EFE0',
        text:      '#1A1208',
        muted:     '#6B5744',
        primary:   '#2C2416',
        accent:    '#B85C3A',
        border:    '#D4C5A9',
        tape:      'rgba(255,235,150,0.55)',
      },
      fontFamily: {
        display: ['Caveat', 'Patrick Hand', 'Comic Sans MS', 'cursive'],
        body:    ['Special Elite', 'Courier New', 'Courier', 'monospace'],
        mono:    ['Courier New', 'Courier', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '2px',
        polaroid: '4px',
      },
      boxShadow: {
        paper: '2px 3px 6px rgba(0,0,0,0.18), 0 1px 2px rgba(0,0,0,0.10)',
        lift:  '4px 6px 12px rgba(0,0,0,0.22), 0 2px 4px rgba(0,0,0,0.14)',
      },
      transitionDuration: { DEFAULT: '400ms' },
      transitionTimingFunction: { DEFAULT: 'linear' },
    },
  },
}
```

## "Breaks if" invariants

- breaks if background is pure white (`#FFFFFF`) — the warmth comes from the off-white cream ground
- breaks if a sans-serif face replaces the display font — hand-lettered or typewriter faces are structural to the identity
- breaks if border-radius exceeds 6px on card containers — Polaroid-style straight-edge silhouettes are required
- breaks if a drop-shadow uses a coloured tint — shadows must remain greyscale-brown neutrals only
- breaks if torn-edge clip-paths are replaced with smooth curves — physical irregularity is the brand signal
- breaks if a second chromatic accent colour is introduced alongside `--color-accent`
- breaks if motion uses an easing curve other than `linear` — analogue physicality demands non-interpolated feels

## Canonical render-test pointer

Render-test file: `references/render-tests/S-031-paper-collage-test.html` (generated from `references/_test-skeleton.html` + this file's `{{TOKEN}}` block).
Upstream source: web-designer-plugin paper-collage demo (MIT).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 128129 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- S-030 Lo-Fi Paper — lighter paper grain, warmer palette, no torn edges
- S-037 Cream Editorial — cleaner typographic system, no craft textures
- S-019 Heritage — heritage brand warmth but refined serif typography, no physical collage elements
- Source: web-designer-plugin (MIT) — https://github.com/MickeyAlton33/web-designer-plugin
