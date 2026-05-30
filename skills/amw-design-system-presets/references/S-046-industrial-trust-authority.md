<!--
  Clean-room transcription. Source: blocked-B harvest entry #12 (`landing-page-builder-skill-main`)
  industry x theme matrix, theme #9 "Industrial/Trust Authority Dark". Upstream license is unknown;
  this file contains no source code, only the documented aesthetic intent (hue/lightness/chroma) and
  derivations that follow generally-accepted dark-UI conventions.
-->
---
id: S-046
name: Industrial / Trust Authority
aesthetic_position: dark-authority-signal
source_attribution: >
  blocked-B.md harvest entry #12 `landing-page-builder-skill-main` (industry x theme matrix,
  theme #9 "Industrial/Trust Authority Dark"); Master Ledger row S-046. Clean-room
  transcription from documented hue/lightness/chroma values; no upstream code is reused.
license: clean-room (upstream license unknown; derivations from public-domain oklch color values)
---

# S-046 — Industrial / Trust Authority

**Filename:** `skills/amw-design-system-presets/references/S-046-industrial-trust-authority.md`
**Tracked in:** this repo (skills/ is git-tracked)

## Identity

Industrial Trust Authority is a dark-mode aesthetic engineered for industrial B2B platforms, security and surveillance vendors, premium home-services brands, and any product that must communicate institutional weight, on-site competence, and operator-grade reliability. Its visual fingerprint is a deep navy canvas (`oklch(0.18 0.05 260)`) which reads as serious and grounded rather than neutral or playful, paired with a single high-luminance golden yellow signal (`oklch(0.82 0.16 86)`) reserved for primary calls to action and brand-mark accents. Body type is a neutral grotesque (Inter or Source Sans 3) at slightly elevated line-height for readability against the dark field; display type may shift to a condensed sans for industrial signage flavour. Information density is moderate to high (this is not a hospitality landing page), border-radius is restrained (4-6px), and shadows are deep but contained. The golden yellow functions as a scarce visual resource: only one or two elements per screen may use it, which is how the "signal" reads as such instead of fading into decorative noise.

## Token block

```css
/* S-046 Industrial / Trust Authority — CSS custom properties (oklch primary; hex fallback) */
:root {
  /* Color — oklch source of truth */
  --color-bg:           oklch(0.18 0.05 260);   /* deep navy canvas */
  --color-surface:      oklch(0.22 0.04 260);   /* card / panel one step lighter */
  --color-surface-2:    oklch(0.26 0.04 260);   /* elevated surface (modal, aside) */
  --color-text:         oklch(0.94 0.01 260);   /* near-white, cool-leaning for contrast */
  --color-text-muted:   oklch(0.70 0.02 260);   /* secondary labels, captions */
  --color-primary:      oklch(0.82 0.16 86);    /* golden yellow signal — CTAs only */
  --color-primary-dim:  oklch(0.72 0.14 86);    /* pressed / hover state */
  --color-accent:       oklch(0.82 0.16 86);    /* same as primary; one-signal contract */
  --color-border:       oklch(0.32 0.04 260);   /* hairline divider on dark navy */
  --color-brand-navy:   oklch(0.18 0.05 260);   /* logo / OG-image fixed brand value */
  --color-brand-gold:   oklch(0.82 0.16 86);    /* logo / OG-image fixed brand value */

  /* Hex fallback for older browsers (approximate sRGB) */
  --color-bg-hex:       #11192B;
  --color-surface-hex:  #1A2438;
  --color-text-hex:     #EAEEF5;
  --color-primary-hex:  #E5B324;
  --color-border-hex:   #2D3A55;

  /* Typography — grotesque for body, condensed for industrial signage flavour */
  --font-display: 'Barlow Condensed', 'Oswald', 'Inter', 'Helvetica Neue', sans-serif;
  --font-body:    'Inter', 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif;
  --font-mono:    'JetBrains Mono', 'IBM Plex Mono', 'Fira Code', 'Courier New', monospace;

  /* Spacing — moderate base; B2B density target */
  --spacing: 8px;

  /* Shape — restrained radius reads as engineered, not decorative */
  --radius: 4px;

  /* Shadow — deep but contained, cool-toned for dark canvas */
  --shadow: 0 8px 24px rgba(0, 0, 0, 0.45);

  /* Motion — confident, not flashy */
  --motion-duration: 200ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);

  /* Industrial extras */
  --border-width: 1px;
  --color-cta-text: oklch(0.18 0.05 260);       /* dark text ON the gold CTA */
  --glow-cta: 0 0 0 3px oklch(0.82 0.16 86 / 0.25);  /* focus ring on yellow CTA */
}
```

```ts
// S-046 Industrial / Trust Authority — Tailwind theme extension
const industrialTrustAuthority = {
  colors: {
    bg:           'oklch(0.18 0.05 260)',
    surface:      'oklch(0.22 0.04 260)',
    'surface-2':  'oklch(0.26 0.04 260)',
    text:         'oklch(0.94 0.01 260)',
    'text-muted': 'oklch(0.70 0.02 260)',
    primary:      'oklch(0.82 0.16 86)',
    'primary-dim':'oklch(0.72 0.14 86)',
    border:       'oklch(0.32 0.04 260)',
    'brand-navy': 'oklch(0.18 0.05 260)',
    'brand-gold': 'oklch(0.82 0.16 86)',
  },
  fontFamily: {
    display: ['"Barlow Condensed"', 'Oswald', 'Inter', '"Helvetica Neue"', 'sans-serif'],
    body:    ['Inter', '"Source Sans 3"', '"Helvetica Neue"', 'Arial', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"IBM Plex Mono"', '"Fira Code"', 'monospace'],
  },
  spacing:      { base: '8px' },
  borderRadius: { DEFAULT: '4px' },
  boxShadow:    { DEFAULT: '0 8px 24px rgba(0,0,0,0.45)' },
  transitionDuration:      { DEFAULT: '200ms' },
  transitionTimingFunction:{ DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if the golden yellow signal appears on more than two elements per screen — the trust-signal effect depends on scarcity; multiplying the signal turns institutional into decorative
- breaks if a second chromatic accent is introduced alongside the gold (red, green, cyan) — the one-signal contract is what makes the gold legible as the authority colour
- breaks if the canvas lightens past `oklch(0.30 0.05 260)` — once the navy reads as mid-tone rather than deep, the industrial gravitas collapses into generic SaaS-blue
- breaks if border-radius exceeds 8px on primary UI elements — the engineered, signage-adjacent register requires restrained corners; rounded corners shift the tone toward consumer or hospitality
- breaks if the body typeface switches to a serif or to a handwritten / display font — body type must read as neutral grotesque (Inter, Source Sans 3) to support the B2B information density
- breaks if shadows go warm-toned (rgba with non-zero red) — the canvas is cool navy; warm shadows produce visible chromatic clash on dark surfaces
- breaks if the gold CTA uses light text rather than dark text on its surface — the high-luminance gold (`L=0.82`) demands a dark foreground for WCAG AA contrast; light-on-gold fails contrast and reads as a child-toy palette
- breaks if the navy is desaturated to grey (`chroma < 0.02`) — the small navy chroma (`0.05`) is what distinguishes Industrial Trust from generic Dark Tech (S-038); removing it produces a different style entirely
- breaks if the gold is shifted past hue 100 (toward green) or below hue 70 (toward orange) — the `86` hue is the documented golden-yellow band; greenish-gold reads as chartreuse, orange-gold reads as warehouse-warning

## Canonical render-test pointer

Render test: inject this file's tokens into `skills/amw-design-system-presets/references/_test-skeleton.html` (substituting `{{BG}}` = `oklch(0.18 0.05 260)`, `{{SURFACE}}` = `oklch(0.22 0.04 260)`, `{{TEXT}}` = `oklch(0.94 0.01 260)`, `{{TEXT_MUTED}}` = `oklch(0.70 0.02 260)`, `{{PRIMARY}}` = `oklch(0.82 0.16 86)`, `{{ACCENT}}` = `oklch(0.82 0.16 86)`, `{{BORDER}}` = `oklch(0.32 0.04 260)`, `{{FONT_DISPLAY}}` = `'Barlow Condensed', 'Oswald', 'Inter', sans-serif`, `{{FONT_BODY}}` = `'Inter', 'Source Sans 3', sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', monospace`, `{{RADIUS}}` = `4px`, `{{SHADOW}}` = `0 8px 24px rgba(0,0,0,0.45)`, `{{SPACING}}` = `8px`). Visual parity target: the gold CTA must read as a singular focal point against the navy field; if the eye is pulled in multiple directions, the scarcity rule has been violated.

Upstream parity source: blocked-B.md harvest entry #12 `landing-page-builder-skill-main` (industry x theme matrix, theme #9 "Industrial/Trust Authority Dark"); Master Ledger row S-046.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 105781 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Siblings: S-013 Industrial / Utilitarian (mono-only, 0-radius, no shadow — Industrial Trust is the polished B2B counterpart), S-017 Corporate Bold (light navy + purple — corporate-cold rather than industrial-warm), S-038 Dark Tech (dark with electric-blue accent — developer-focused rather than B2B-services)
- Differentiators: S-046 is dark-mode-first navy with a single high-luminance gold signal calibrated for security / industrial / premium-home-services trust; S-017 is light-mode B2B SaaS; S-038 is dark developer-tool; S-013 is uncompromised utilitarian without polish
- Source: `reports/batch9-harvest/blocked-B.md` harvest entry #12; `landing-page-builder-skill-main` (industry x theme matrix, theme #9)
