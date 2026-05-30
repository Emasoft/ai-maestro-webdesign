---
id: S-037
name: Cream Editorial
aesthetic_position: editorial-warm-paper
source_attribution: >
  blocked-B.md seed table "Cream Editorial" (10-style Wave 1 Track H8 seed);
  styles-B.md "Editorial Serif" warm-paper position; tasteful-ui-skill-master
  catalog "cream background with serif-everywhere discipline".
  LICENSE: MIT (tasteful-ui-skill, web-designer-plugin).
license: MIT (all upstream sources)
---

# S-037 — Cream Editorial

**Filename:** `skills/amw-design-system-presets/references/S-037-cream-editorial.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## Identity

Cream Editorial is a serif-everywhere book-publisher aesthetic built on a warm cream canvas (`#FAF8F4`) that reads like an off-white art-paper stock. Its visual fingerprint is zero border-radius on all UI elements, Cormorant Garamond for every typographic role (display, body, captions), and a single muted terracotta or ink-brown accent that never competes with the text. Intended audience: upscale literary publishers, independent booksellers, long-form journalism platforms, fine-art galleries, and premium essay or essay-magazine sites where reading density and typographic authority are the only currency.

## Token block

```css
/* S-037 Cream Editorial — CSS custom properties */
:root {
  /* Color */
  --color-bg:          #FAF8F4;   /* warm cream — art-paper stock */
  --color-surface:     #F4F0EA;   /* slightly deeper cream for cards / aside blocks */
  --color-surface-2:   #EDE8DF;   /* elevated surface (modal, inset quote) */
  --color-text:        #1C1814;   /* near-black with warm undertone */
  --color-text-muted:  #6B6055;   /* desaturated warm brown — captions, metadata */
  --color-primary:     #1C1814;   /* primary action = text colour (minimal, typographic) */
  --color-accent:      #8B3A2F;   /* muted terracotta — one chromatic touch */
  --color-accent-dim:  #6A2B22;   /* pressed/hover state for accent */
  --color-border:      #D8D2C8;   /* hairline in warm grey — barely visible ruling */

  /* Typography — serif everywhere */
  --font-display: 'Cormorant Garamond', 'Cormorant', 'EB Garamond', Georgia, serif;
  --font-body:    'Cormorant Garamond', 'Cormorant', 'EB Garamond', Georgia, serif;
  --font-mono:    'Courier Prime', 'Courier New', Courier, monospace;

  /* Spacing */
  --spacing: 8px;   /* base unit; editorial column typically 6–8× */

  /* Shape — zero radius is the style's identity */
  --radius: 0px;

  /* Shadow — soft, warm-toned; never cold grey */
  --shadow: 0 2px 12px rgba(28, 24, 20, 0.08);

  /* Motion — deliberate, unhurried */
  --motion-duration: 400ms;
  --motion-easing: cubic-bezier(0.4, 0, 0.2, 1);   /* standard ease */

  /* Editorial extras */
  --border-width: 1px;   /* ruling lines for section dividers */
  --line-height-body: 1.7;   /* generous leading for long-form reading */
  --indent-para: 1.5em;      /* traditional first-paragraph text indent */
}
```

```ts
// S-037 Cream Editorial — Tailwind theme extension
const creamEditorial = {
  colors: {
    bg:          '#FAF8F4',
    surface:     '#F4F0EA',
    'surface-2': '#EDE8DF',
    text:        '#1C1814',
    'text-muted':'#6B6055',
    primary:     '#1C1814',
    accent:      '#8B3A2F',
    'accent-dim':'#6A2B22',
    border:      '#D8D2C8',
  },
  fontFamily: {
    display: ['"Cormorant Garamond"', 'Cormorant', '"EB Garamond"', 'Georgia', 'serif'],
    body:    ['"Cormorant Garamond"', 'Cormorant', '"EB Garamond"', 'Georgia', 'serif'],
    mono:    ['"Courier Prime"', '"Courier New"', 'Courier', 'monospace'],
  },
  spacing: { base: '8px' },
  borderRadius: { DEFAULT: '0px' },
  boxShadow: {
    DEFAULT: '0 2px 12px rgba(28,24,20,0.08)',
  },
  transitionDuration: { DEFAULT: '400ms' },
  transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if any border-radius greater than 0px is applied to cards, buttons, images, or form inputs
- breaks if a sans-serif font is used for any typographic role (display, body, caption, label)
- breaks if a second chromatic accent colour is introduced alongside the terracotta accent
- breaks if the page canvas is white (`#FFFFFF`) or cool-toned rather than warm cream
- breaks if the accent colour is used on more than one independent screen region simultaneously
- breaks if body text line-height falls below 1.6 (reading density rule for long-form)
- breaks if drop-shadows use a cool grey rather than the warm near-black tint
- breaks if a bold sans-serif heading replaces the serif display stack at any hierarchy level
- breaks if the accent is used at full saturation for background fills rather than text or hairline rules
- breaks if section dividers use decorative graphical elements instead of a single hairline border

## Canonical render-test pointer

Render test: inject this file's tokens into `references/_test-skeleton.html` (substituting `{{BG}}` = `#FAF8F4`, `{{SURFACE}}` = `#F4F0EA`, `{{TEXT}}` = `#1C1814`, `{{TEXT_MUTED}}` = `#6B6055`, `{{PRIMARY}}` = `#1C1814`, `{{ACCENT}}` = `#8B3A2F`, `{{BORDER}}` = `#D8D2C8`, `{{FONT_DISPLAY}}` = `'Cormorant Garamond', 'Cormorant', 'EB Garamond', Georgia, serif`, `{{FONT_BODY}}` = `'Cormorant Garamond', Georgia, serif`, `{{FONT_MONO}}` = `'Courier Prime', monospace`, `{{RADIUS}}` = `0px`, `{{SHADOW}}` = `0 2px 12px rgba(28,24,20,.08)`, `{{SPACING}}` = `8px`).

Upstream parity source: `blocked-B.md` seed table "Cream Editorial" + `tasteful-ui-skill-master` catalog (MIT, inferred).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 91973 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Siblings: S-014 Editorial Serif (cooler paper), S-018 Understated Elegance (minimal sans body), S-030 Lo-Fi Paper (rougher texture), S-031 Paper Collage (cut-and-paste layered)
- Differentiators: S-037 is serif-only zero-radius cream; S-014 allows sans body font; S-018 uses sans-serif body; S-030 has hand-drawn scan texture; S-031 is layered collage not clean editorial
- Source: `reports/batch9-harvest/blocked-B.md` seed table Wave 1 Track H8 + `tasteful-ui-skill-master` catalog (MIT)
