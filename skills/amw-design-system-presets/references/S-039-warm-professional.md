---
id: S-039
name: Warm Professional
aesthetic_position: editorial-warm-paper
source_attribution: >
  blocked-B.md seed table "Warm Professional" (10-style Wave 1 Track H8 seed);
  styles-B.md "Warm Professional" editorial-warm-paper position; tasteful-ui-skill-master
  catalog business-trustworthy entry; frontend-design-engineer-skill-main
  visual-directions.md warm-corporate category.
  LICENSE: MIT (tasteful-ui-skill, web-designer-plugin, frontend-design-engineer-skill).
license: MIT (all upstream sources)
---

# S-039 — Warm Professional

**Filename:** `skills/amw-design-system-presets/references/S-039-warm-professional.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## Identity

Warm Professional is a business-trust aesthetic built on a warm off-white canvas (`#F9F5F0`) that projects approachability without sacrificing authority. Its visual fingerprint is a pairing of Source Serif 4 for display and headings with Source Sans 3 for body text — the Source family's internal harmony creates typographic coherence at every scale — a muted navy or forest-green accent that reads as trustworthy rather than aggressive, and moderate 6-8px radius on UI elements. Intended audience: professional services firms, law practices, financial advisory, medical and health information, B2B SaaS for regulated industries, and any context where "human" and "credible" must coexist without a corporate-cold feel.

## Token block

```css
/* S-039 Warm Professional — CSS custom properties */
:root {
  /* Color */
  --color-bg:          #F9F5F0;   /* warm off-white — approachable, not clinical */
  --color-surface:     #F2EDE6;   /* card / panel surface — slightly deeper warm */
  --color-surface-2:   #EAE3DA;   /* elevated surface (modal, aside) */
  --color-text:        #1F1A14;   /* warm near-black — authoritative but not harsh */
  --color-text-muted:  #7A6F63;   /* warm grey — captions, secondary labels */
  --color-primary:     #1F1A14;   /* primary action matches text (light bg) */
  --color-accent:      #2D5A8A;   /* muted navy — trust signal, one chromatic touch */
  --color-accent-dim:  #1E3F63;   /* pressed/hover accent */
  --color-border:      #D9D1C7;   /* soft warm-grey hairline */

  /* Typography — Source family pairing */
  --font-display: 'Source Serif 4', 'Source Serif Pro', 'Lora', Georgia, serif;
  --font-body:    'Source Sans 3', 'Source Sans Pro', 'Inter', 'Helvetica Neue', sans-serif;
  --font-mono:    'Source Code Pro', 'JetBrains Mono', 'Courier New', monospace;

  /* Spacing */
  --spacing: 8px;   /* base unit */

  /* Shape */
  --radius: 6px;

  /* Shadow — warm-toned ambient */
  --shadow: 0 2px 16px rgba(31, 26, 20, 0.08);

  /* Motion — professional pacing, not snappy, not slow */
  --motion-duration: 250ms;
  --motion-easing: cubic-bezier(0.4, 0, 0.2, 1);

  /* Professional extras */
  --border-width: 1px;
  --gradient-hero: linear-gradient(160deg, #F9F5F0 0%, #F0EAE1 100%);
}
```

```ts
// S-039 Warm Professional — Tailwind theme extension
const warmProfessional = {
  colors: {
    bg:          '#F9F5F0',
    surface:     '#F2EDE6',
    'surface-2': '#EAE3DA',
    text:        '#1F1A14',
    'text-muted':'#7A6F63',
    primary:     '#1F1A14',
    accent:      '#2D5A8A',
    'accent-dim':'#1E3F63',
    border:      '#D9D1C7',
  },
  fontFamily: {
    display: ['"Source Serif 4"', '"Source Serif Pro"', 'Lora', 'Georgia', 'serif'],
    body:    ['"Source Sans 3"', '"Source Sans Pro"', 'Inter', '"Helvetica Neue"', 'sans-serif'],
    mono:    ['"Source Code Pro"', '"JetBrains Mono"', '"Courier New"', 'monospace'],
  },
  spacing: { base: '8px' },
  borderRadius: { DEFAULT: '6px' },
  boxShadow: {
    DEFAULT: '0 2px 16px rgba(31,26,20,0.08)',
  },
  transitionDuration: { DEFAULT: '250ms' },
  transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if the canvas background becomes white (`#FFFFFF`) or cool-toned
- breaks if border-radius exceeds 10px on any primary UI element (destroys professional restraint)
- breaks if border-radius falls to 0px (the zero-radius editorial look is S-037, not S-039)
- breaks if a saturated or bright accent colour replaces the muted navy (electric blue, hot orange, vivid green all break the trust signal)
- breaks if a second chromatic accent colour is introduced alongside the navy
- breaks if display headings use a sans-serif font (Source Serif 4 provides the authority layer)
- breaks if the body font switches to a serif (Source Sans 3 pairs with the serif display stack; inverting them loses the pairing logic)
- breaks if drop-shadows use a cool grey rather than the warm near-black tint
- breaks if the accent colour is used for background fills at high saturation rather than text, borders, or CTA labels
- breaks if decorative flourishes (ornamental dividers, illustrated icons, editorial photography) are replaced by purely geometric/abstract shapes (this is a human-profession aesthetic, not a startup aesthetic)

## Canonical render-test pointer

Render test: inject this file's tokens into `references/_test-skeleton.html` (substituting `{{BG}}` = `#F9F5F0`, `{{SURFACE}}` = `#F2EDE6`, `{{TEXT}}` = `#1F1A14`, `{{TEXT_MUTED}}` = `#7A6F63`, `{{PRIMARY}}` = `#1F1A14`, `{{ACCENT}}` = `#2D5A8A`, `{{BORDER}}` = `#D9D1C7`, `{{FONT_DISPLAY}}` = `'Source Serif 4', 'Lora', Georgia, serif`, `{{FONT_BODY}}` = `'Source Sans 3', 'Inter', sans-serif`, `{{FONT_MONO}}` = `'Source Code Pro', monospace`, `{{RADIUS}}` = `6px`, `{{SHADOW}}` = `0 2px 16px rgba(31,26,20,.08)`, `{{SPACING}}` = `8px`).

Upstream parity source: `blocked-B.md` seed table "Warm Professional" + `tasteful-ui-skill-master` catalog (MIT, inferred).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 112703 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Siblings: S-017 Corporate Bold (cooler, bolder, blue-dominant), S-018 Understated Elegance (minimal, colder), S-037 Cream Editorial (serif-everywhere, 0px radius), S-020 Organic (earth-tones, rounded, nature-focused)
- Differentiators: S-039 is warm + human + moderate-radius with a serif/sans pairing; S-017 is corporate-cold dominant blue; S-018 is cooler minimal; S-037 uses a single serif font everywhere at 0px radius; S-020 is earthy/organic not professional-services
- Source: `reports/batch9-harvest/blocked-B.md` seed table Wave 1 Track H8 + `tasteful-ui-skill-master` catalog (MIT)
