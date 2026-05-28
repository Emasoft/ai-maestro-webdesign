---
id: S-019
name: Heritage / Warm Editorial
aesthetic_position: editorial-warm-paper
source_attribution: https://github.com/design-system-is-all-you-need (heritage.md full parametric token system + warmth levels); https://github.com/tasteful-ui-skill (catalog.md Warm/Editorial routing)
license: MIT (inferred from source repo conventions)
---

# S-019 — Heritage / Warm Editorial

**Filename:** `skills/amw-design-system-presets/references/S-019-heritage-warm-editorial.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## Identity

Heritage / Warm Editorial translates the aesthetic of aged paper, wax seals, and hand-composed letterpress into contemporary digital surfaces. The color system is built from three background layers — cream (`#F5F0E8`), sand (`#E8DCC8`), and tan (`#D4C4A8`) — that describe a range from fresh linen to aged parchment. The typographic pairing is deliberately dual-mode: Playfair Display or Cormorant Garamond for display type evokes historical bookmaking, while Dancing Script used sparingly as an accent creates the handwritten flourish that anchors the heritage feeling. Image treatments (organic oval and circle masks rather than rectangles) reinforce the artisan-object quality of photography. The terracotta/sienna accent reads as a heat-fired pigment rather than a digital hue. Pure white and pure black are structurally forbidden — they belong to the digital present, not the material past. This style serves artisan food and beverage, heritage craft brands, travel and cultural editorial, ceremony and event design, antique and collectibles, and any brand whose proposition is rooted in provenance.

## Token block

```css
:root {
  /* Colors */
  --color-bg:          #F5F0E8;
  --color-surface:     #EDE6D6;
  --color-text:        #3D2B1F;
  --color-text-muted:  #7A6456;
  --color-primary:     #5C3D2E;
  --color-accent:      #8B4513;
  --color-border:      #C8B89A;

  /* Background scale (warmth levels) */
  --bg-cream: #F5F0E8;
  --bg-sand:  #E8DCC8;
  --bg-tan:   #D4C4A8;

  /* Typography */
  --font-display: 'Playfair Display', 'Cormorant Garamond', 'EB Garamond', Georgia, serif;
  --font-body:    'Lora', 'Georgia', 'Times New Roman', serif;
  --font-mono:    'Courier Prime', 'Courier New', monospace;

  /* Accent script (use sparingly — labels, pull-quotes, decorative callouts only) */
  --font-script: 'Dancing Script', 'Pacifico', cursive;

  /* Spacing */
  --spacing: 8px;

  /* Shape */
  --radius: 4px;

  /* Shadow */
  --shadow: none;

  /* Motion */
  --motion-duration: 400ms;
  --motion-easing:   ease;

  /* Optional brand-specific */
  --border-divider: 1px solid #C8B89A;
  --color-surface-hover: #E0D6C4;
}
```

```ts
// Tailwind theme extension
theme: {
  extend: {
    colors: {
      'her-bg':     '#F5F0E8',
      'her-surface': '#EDE6D6',
      'her-text':   '#3D2B1F',
      'her-muted':  '#7A6456',
      'her-brown':  '#5C3D2E',
      'her-sienna': '#8B4513',
      'her-border': '#C8B89A',
      'her-sand':   '#E8DCC8',
      'her-tan':    '#D4C4A8',
    },
    fontFamily: {
      display: ['Playfair Display', 'Cormorant Garamond', 'EB Garamond', 'Georgia', 'serif'],
      body:    ['Lora', 'Georgia', 'Times New Roman', 'serif'],
      script:  ['Dancing Script', 'Pacifico', 'cursive'],
    },
    borderRadius: {
      DEFAULT: '4px',
      sm:      '0px',
      oval:    '50%',
    },
    boxShadow: {
      none: 'none',
    },
  },
},
```

## "Breaks if" invariants

- breaks if pure white (`#FFFFFF`) or pure black (`#000000`) appear anywhere in the palette — these are structural violations; the style's entire warmth depends on the absence of digital primaries
- breaks if a sans-serif typeface is used as the body font — the all-serif body stack (Lora/Georgia) is non-negotiable for the heritage register; sans-serif body immediately reads as contemporary/corporate
- breaks if the script accent font (Dancing Script) is used for headings or body text — it must be reserved for labels, callouts, and decorative short strings; more than ~4 words in script becomes illegible
- breaks if drop shadows with opacity above 0.04 are added — the style uses flat warm surfaces; any visible shadow introduces a digital-elevation hierarchy that conflicts with the material aesthetic
- breaks if image masks are rectangular — oval, circle, or organic masks are the visual signature; rectangular images read as contemporary grid layouts
- breaks if cool greys (hsl 200-280) are introduced as neutrals — all neutrals must be warm-tinted; even `#9CA3AF` reads as foreign in this palette
- breaks if `--radius` is raised above 4px for card components — larger radius shifts toward contemporary wellness brands; the heritage register favors near-zero radius or the specific oval-mask idiom
- breaks if motion uses spring/bounce physics — the style's era reference predates spring physics; ease and linear transitions are period-appropriate; bounce reads as anachronistic

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers with the values above. For warmth-level testing, render three variants: cream (`--color-bg: #F5F0E8`), sand (`--color-bg: #E8DCC8`), and tan (`--color-bg: #D4C4A8`).
Source parity: `design-system-is-all-you-need-main/references/heritage.md` (full parametric token system + warmth levels). Compare the testimonial block and header nav for the warm-tone coherence test.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 108469 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- S-018 Understated Elegance — sibling; uses sage green primary rather than warm brown primary; lighter surface; more contemporary; S-019 is more antique
- S-014 Editorial Serif — related editorial register but colder palette (near-black/white with red accent); use S-014 for publications and journalism, S-019 for artisan brands
- S-020 Organic / Earthy — adjacent earthy palette but no cream backgrounds (organic uses sage/moss/ochre); S-019 is more historical, S-020 is more botanical-contemporary
- Source: `design-system-is-all-you-need-main/.../heritage.md`; `tasteful-ui-skill-master/.../catalog.md` (Warm/Editorial routing category)
