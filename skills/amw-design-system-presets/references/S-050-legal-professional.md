<!--
  Clean-room transcription. Source: blocked-B harvest entry #12 (`landing-page-builder-skill-main`)
  industry x theme matrix, theme #26 "Legal/Professional". Upstream license is unknown;
  this file contains no source code, only the documented aesthetic intent (hue/lightness/chroma)
  and derivations consistent with generally-accepted legal/professional-services UI conventions.
-->
---
id: S-050
name: Legal / Professional
aesthetic_position: light-conservative-authority
source_attribution: >
  blocked-B.md harvest entry #12 `landing-page-builder-skill-main` (industry x theme matrix,
  theme #26 "Legal/Professional"); Master Ledger row S-050. Clean-room transcription from
  documented hue/lightness/chroma values; no upstream code is reused.
license: clean-room (upstream license unknown; derivations from public-domain oklch color values)
---

# S-050 — Legal / Professional

**Filename:** `skills/amw-design-system-presets/references/S-050-legal-professional.md`
**Tracked in:** this repo (skills/ is git-tracked)

## Identity

Legal Professional is a light-mode aesthetic engineered for law firms, accounting and tax practices, financial advisory, notaries, immigration consultancies, expert-witness services, and any professional-services brand where the client brief is conservative authority with subtle warmth. Its visual fingerprint is a near-white canvas (`oklch(0.98 0 0)`) — almost pure white but neutralized so it does not feel sterile — with a deep purple-blue primary (`oklch(0.30 0.08 270)`) that reads as judicial and considered rather than corporate-cold, paired with a restrained warm gold accent for hairline rules, monogram emblems, and one quiet decorative touch. The two-chromatic contract here is intentional and traditional: purple-blue + gold is a centuries-old visual language of jurisprudence and academic professions. Typography is a serif/sans pairing in the editorial-professional register (Source Serif 4 or Lora for display, Inter or Source Sans 3 for body) — a serif headline carries weight; a sans body keeps long-form contracts and explanatory pages readable. Border-radius is restrained (2-4px); shadows are very soft and warm-toned; motion is unhurried. Decorative elements are minimal — at most one hairline gold rule per section. Density is moderate; whitespace is generous but never lush. The whole composition must read like an embossed business card sitting on dark walnut, not like a startup landing page.

## Token block

```css
/* S-050 Legal / Professional — CSS custom properties (oklch primary; hex fallback) */
:root {
  /* Color — oklch source of truth */
  --color-bg:           oklch(0.98 0 0);        /* neutral near-white, no chroma cast */
  --color-surface:      oklch(0.96 0.003 270);  /* card / panel — barely-cool */
  --color-surface-2:    oklch(0.93 0.005 270);  /* elevated surface (modal, aside) */
  --color-text:         oklch(0.20 0.02 270);   /* deep cool slate, almost-black */
  --color-text-muted:   oklch(0.48 0.02 270);   /* labels, secondary text */
  --color-primary:      oklch(0.30 0.08 270);   /* deep purple-blue — judicial authority */
  --color-primary-dim:  oklch(0.22 0.08 270);   /* pressed / hover state */
  --color-accent:       oklch(0.72 0.13 80);    /* warm gold — hairline rules, emblems */
  --color-accent-dim:   oklch(0.62 0.12 80);    /* pressed accent */
  --color-border:       oklch(0.88 0.006 270);  /* soft cool-grey hairline */
  --color-rule-gold:    oklch(0.72 0.13 80);    /* dedicated gold for section rules */
  --color-focus-ring:   oklch(0.30 0.08 270 / 0.35);

  /* Hex fallback for older browsers (approximate sRGB) */
  --color-bg-hex:       #F9F9F9;
  --color-surface-hex:  #F1F1F4;
  --color-text-hex:     #25232E;
  --color-primary-hex:  #3D365E;
  --color-accent-hex:   #BE9A3F;
  --color-border-hex:   #DCD9DF;

  /* Typography — serif display + sans body, traditional professional pairing */
  --font-display: 'Source Serif 4', 'Source Serif Pro', 'Lora', Georgia, serif;
  --font-body:    'Inter', 'Source Sans 3', 'Source Sans Pro', 'Helvetica Neue', sans-serif;
  --font-mono:    'Source Code Pro', 'JetBrains Mono', 'Courier New', monospace;

  /* Spacing — moderate, never cramped (long-form readability) */
  --spacing: 8px;
  --line-height-body: 1.6;
  --measure-body: 65ch;          /* optimal line length for long-form legal prose */

  /* Shape — restrained, judicial */
  --radius: 3px;

  /* Shadow — very soft, warm-tinted to harmonize with gold */
  --shadow: 0 1px 3px rgba(61, 54, 94, 0.06);
  --shadow-elev: 0 4px 16px rgba(61, 54, 94, 0.08);

  /* Motion — unhurried, considered */
  --motion-duration: 280ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);

  /* Legal extras */
  --border-width: 1px;
  --border-width-rule: 1px;       /* gold rule = exactly 1px, never thicker */
  --color-cta-text: oklch(0.98 0 0);  /* near-white text on deep-purple CTA */
}
```

```ts
// S-050 Legal / Professional — Tailwind theme extension
const legalProfessional = {
  colors: {
    bg:           'oklch(0.98 0 0)',
    surface:      'oklch(0.96 0.003 270)',
    'surface-2':  'oklch(0.93 0.005 270)',
    text:         'oklch(0.20 0.02 270)',
    'text-muted': 'oklch(0.48 0.02 270)',
    primary:      'oklch(0.30 0.08 270)',
    'primary-dim':'oklch(0.22 0.08 270)',
    accent:       'oklch(0.72 0.13 80)',
    'accent-dim': 'oklch(0.62 0.12 80)',
    border:       'oklch(0.88 0.006 270)',
  },
  fontFamily: {
    display: ['"Source Serif 4"', '"Source Serif Pro"', 'Lora', 'Georgia', 'serif'],
    body:    ['Inter', '"Source Sans 3"', '"Source Sans Pro"', '"Helvetica Neue"', 'sans-serif'],
    mono:    ['"Source Code Pro"', '"JetBrains Mono"', '"Courier New"', 'monospace'],
  },
  spacing:      { base: '8px' },
  borderRadius: { DEFAULT: '3px' },
  boxShadow:    {
    DEFAULT: '0 1px 3px rgba(61,54,94,0.06)',
    elev:    '0 4px 16px rgba(61,54,94,0.08)',
  },
  transitionDuration:      { DEFAULT: '280ms' },
  transitionTimingFunction:{ DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if a third chromatic color is introduced beyond the documented purple-blue + warm gold pair — the two-chromatic contract is the traditional jurisprudential signature; adding a third color violates the centuries-old visual register and dilutes authority
- breaks if the purple-blue primary chroma exceeds `C=0.12` — high-chroma purple reads as branded-creative (think a design studio) rather than judicial; the documented `C=0.08` is the calibrated upper bound
- breaks if the gold accent is used for large surface fills rather than hairline rules / emblems / single-letter monograms — gold must be scarce and decorative; flooding with gold produces a luxury-restaurant or wedding-invitation register, not a legal-professional one
- breaks if border-radius exceeds 6px on primary UI elements — the conservative-authority brief requires restrained corners; rounded corners shift the tone toward consumer or creative-professional services
- breaks if the body typeface switches to a serif (matching the display) — solid serif everywhere reads as editorial (S-014, S-037) rather than legal-professional; the serif/sans pairing is the legibility contract for long-form contracts
- breaks if motion-duration drops below 200ms or uses snappy easing — unhurried timing supports the considered/deliberate brand reading; quick motion undermines the authority signal
- breaks if shadows go cool-toned (pure-grey rgba) rather than warm-tinted — the warm-tinted shadow matches the gold accent and produces palette coherence; cool shadows clash with the gold
- breaks if gold rule weight exceeds 1px — the hairline rule is the entire decorative budget; thicker rules read as decorative-magazine rather than restrained-professional
- breaks if the canvas tints chromatically (warm cream, cool blue) — neutral near-white is what allows the deep purple-blue and warm gold to read clearly; a chromatic canvas muddles the two-color contract
- breaks if the body text measure exceeds `75ch` — long-form legal content requires tight measure for readability; wide-measure prose breaks the prose-quality contract for the use case

## Canonical render-test pointer

Render test: inject this file's tokens into `skills/amw-design-system-presets/references/_test-skeleton.html` (substituting `{{BG}}` = `oklch(0.98 0 0)`, `{{SURFACE}}` = `oklch(0.96 0.003 270)`, `{{TEXT}}` = `oklch(0.20 0.02 270)`, `{{TEXT_MUTED}}` = `oklch(0.48 0.02 270)`, `{{PRIMARY}}` = `oklch(0.30 0.08 270)`, `{{ACCENT}}` = `oklch(0.72 0.13 80)`, `{{BORDER}}` = `oklch(0.88 0.006 270)`, `{{FONT_DISPLAY}}` = `'Source Serif 4', 'Lora', Georgia, serif`, `{{FONT_BODY}}` = `Inter, 'Source Sans 3', sans-serif`, `{{FONT_MONO}}` = `'Source Code Pro', monospace`, `{{RADIUS}}` = `3px`, `{{SHADOW}}` = `0 1px 3px rgba(61,54,94,0.06)`, `{{SPACING}}` = `8px`). Visual parity target: the composition should read like a high-quality embossed business card or a law-firm letterhead; if the page looks startup-modern, the deep purple-blue chroma is likely too high or the gold is being used as a fill rather than a hairline accent.

Upstream parity source: blocked-B.md harvest entry #12 `landing-page-builder-skill-main` (industry x theme matrix, theme #26 "Legal/Professional"); Master Ledger row S-050.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 109940 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Siblings: S-039 Warm Professional (warm-paper bg + muted navy — warmer and less judicial), S-017 Corporate Bold (light navy + purple — corporate-SaaS rather than legal-services), S-028 Art Deco / Geometric (dark + gold + cream — decorative-geometric rather than restrained-judicial), S-014 Editorial Serif (serif-everywhere editorial — long-form publication rather than professional services)
- Differentiators: S-050 is light-mode conservative-authority with the traditional purple-blue + warm gold pair, calibrated for law / accounting / advisory; S-039 is warm-paper professional-services; S-017 is corporate B2B SaaS; S-028 is decorative-deco; S-014 is editorial publication
- Source: `blocked-B.md` harvest entry #12; `landing-page-builder-skill-main` (industry x theme matrix, theme #26)
