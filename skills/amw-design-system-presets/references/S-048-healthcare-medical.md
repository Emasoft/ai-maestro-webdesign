<!--
  Clean-room transcription. Source: blocked-B harvest entry #12 (`landing-page-builder-skill-main`)
  industry x theme matrix, theme #15 "Healthcare/Medical". Upstream license is unknown;
  this file contains no source code, only the documented aesthetic intent (hue/lightness/chroma)
  and derivations consistent with generally-accepted healthcare-UI conventions.
-->
---
id: S-048
name: Healthcare / Medical
aesthetic_position: light-calm-trust
source_attribution: >
  blocked-B.md harvest entry #12 `landing-page-builder-skill-main` (industry x theme matrix,
  theme #15 "Healthcare/Medical"); Master Ledger row S-048. Clean-room transcription from
  documented hue/lightness/chroma values; no upstream code is reused.
license: clean-room (upstream license unknown; derivations from public-domain oklch color values)
---

# S-048 — Healthcare / Medical

**Filename:** `skills/amw-design-system-presets/references/S-048-healthcare-medical.md`
**Tracked in:** this repo (skills/ is git-tracked)

## Identity

Healthcare Medical is a light-mode aesthetic engineered for clinics, dental and medical practices, telemedicine platforms, patient-portal applications, and health-information products where the primary emotional brief is calm and trustworthy. Its visual fingerprint is a balanced medical teal (`oklch(0.55 0.13 195)`) on a near-white canvas — the teal is deliberately mid-chroma (`C=0.13`, lower than the energetic blues of S-047) so it reads as professional and clinical without becoming sterile. Typography is a contemporary, very legible sans (Inter, DM Sans) at slightly higher line-height than default to support older readers and long-form patient instructions. Surfaces are extremely light and layered with gentle cool grey; the radius is moderate (8-10px) which conveys approachability without playfulness; shadows are very soft and cool. The palette is strictly one-chromatic-signal: introducing red signals alarm and breaks the calm brief; introducing warm tones shifts the register toward wellness or spa (S-051) rather than clinical-trust.

## Token block

```css
/* S-048 Healthcare / Medical — CSS custom properties (oklch primary; hex fallback) */
:root {
  /* Color — oklch source of truth */
  --color-bg:           oklch(0.99 0.004 195);  /* cool near-white, slight teal undertone */
  --color-surface:      oklch(0.97 0.006 195);  /* card / panel surface */
  --color-surface-2:    oklch(0.94 0.008 195);  /* elevated surface (modal, aside) */
  --color-text:         oklch(0.22 0.02 220);   /* deep cool slate — readable for all ages */
  --color-text-muted:   oklch(0.50 0.02 220);   /* labels, secondary text */
  --color-primary:      oklch(0.55 0.13 195);   /* medical teal — primary brand */
  --color-primary-dim:  oklch(0.45 0.13 195);   /* pressed / hover state */
  --color-accent:       oklch(0.55 0.13 195);   /* one-chromatic-signal contract */
  --color-border:       oklch(0.91 0.010 195);  /* gentle cool-grey hairline */
  --color-success:      oklch(0.60 0.13 160);   /* green for confirmed appointments, lab-result-ok */
  --color-warning:      oklch(0.75 0.13 75);    /* amber — used SPARINGLY (results that need follow-up) */
  --color-danger:       oklch(0.55 0.18 25);    /* reserved exclusively for true clinical alerts */
  --color-focus-ring:   oklch(0.55 0.13 195 / 0.35);

  /* Hex fallback for older browsers (approximate sRGB) */
  --color-bg-hex:       #FBFCFC;
  --color-surface-hex:  #F4F7F8;
  --color-text-hex:     #232A36;
  --color-primary-hex:  #2A8A9C;
  --color-border-hex:   #DDE5E7;

  /* Typography — high-legibility sans */
  --font-display: 'Inter', 'DM Sans', 'Source Sans 3', 'Helvetica Neue', sans-serif;
  --font-body:    'Inter', 'Source Sans 3', 'Helvetica Neue', Arial, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Spacing — slightly generous for patient readability */
  --spacing: 8px;
  --line-height-body: 1.6;

  /* Shape — approachable without playful */
  --radius: 8px;

  /* Shadow — soft, cool, low-elevation */
  --shadow: 0 2px 8px rgba(42, 138, 156, 0.08);
  --shadow-elev: 0 8px 20px rgba(42, 138, 156, 0.10);

  /* Motion — gentle, never jarring (anxious users) */
  --motion-duration: 220ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);

  /* Healthcare extras */
  --border-width: 1px;
  --color-cta-text: oklch(0.99 0.004 195);  /* near-white text on the teal CTA */
}
```

```ts
// S-048 Healthcare / Medical — Tailwind theme extension
const healthcareMedical = {
  colors: {
    bg:           'oklch(0.99 0.004 195)',
    surface:      'oklch(0.97 0.006 195)',
    'surface-2':  'oklch(0.94 0.008 195)',
    text:         'oklch(0.22 0.02 220)',
    'text-muted': 'oklch(0.50 0.02 220)',
    primary:      'oklch(0.55 0.13 195)',
    'primary-dim':'oklch(0.45 0.13 195)',
    border:       'oklch(0.91 0.010 195)',
    success:      'oklch(0.60 0.13 160)',
    warning:      'oklch(0.75 0.13 75)',
    danger:       'oklch(0.55 0.18 25)',
  },
  fontFamily: {
    display: ['Inter', '"DM Sans"', '"Source Sans 3"', '"Helvetica Neue"', 'sans-serif'],
    body:    ['Inter', '"Source Sans 3"', '"Helvetica Neue"', 'Arial', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
  },
  spacing:      { base: '8px' },
  borderRadius: { DEFAULT: '8px' },
  boxShadow:    {
    DEFAULT: '0 2px 8px rgba(42,138,156,0.08)',
    elev:    '0 8px 20px rgba(42,138,156,0.10)',
  },
  transitionDuration:      { DEFAULT: '220ms' },
  transitionTimingFunction:{ DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if red (`oklch(0.55 0.18 25)`) is used outside of true clinical alerts — red in a healthcare context reads as immediate danger; using it for ordinary CTAs, errors, or decoration violates trust and undermines the alert semantics
- breaks if the teal chroma exceeds `C=0.18` — high-chroma teal reads as branded-consumer (think menthol gum) rather than clinical-trust; the documented `C=0.13` is the calibrated upper bound
- breaks if a warm chromatic accent (orange, coral, pink) is introduced alongside the teal — warm + cool yields wellness-spa or beauty registers (S-051) rather than clinical-medical; temperature coherence is the trust signal
- breaks if border-radius falls below 4px — sharp edges in a healthcare context read as bureaucratic or industrial-medical (lab-equipment); the brief is patient-facing, requiring approachable corners
- breaks if line-height drops below `1.5` for body — long-form patient instructions and older readers need generous vertical breathing room; tight type breaks accessibility and clinical usability
- breaks if the canvas tints warm (cream, ivory) — warm canvas shifts the register from clinical to hospitality; medical brief requires cool-leaning whites
- breaks if shadows go neutral-grey or warm — the teal-tinted soft shadow is part of the temperature-coherent palette; neutral shadows clash with the teal accent on layered surfaces
- breaks if motion-duration drops below 150ms or uses linear easing — anxious users (medical context inherently raises stress) require gentle eased transitions; snappy linear motion reads as alarming
- breaks if the teal CTA uses dark teal text on light teal surface (low contrast) — accessibility-critical contexts demand WCAG AA contrast minimum; the CTA must use near-white text on the medical teal

## Canonical render-test pointer

Render test: inject this file's tokens into `skills/amw-design-system-presets/references/_test-skeleton.html` (substituting `{{BG}}` = `oklch(0.99 0.004 195)`, `{{SURFACE}}` = `oklch(0.97 0.006 195)`, `{{TEXT}}` = `oklch(0.22 0.02 220)`, `{{TEXT_MUTED}}` = `oklch(0.50 0.02 220)`, `{{PRIMARY}}` = `oklch(0.55 0.13 195)`, `{{ACCENT}}` = `oklch(0.55 0.13 195)`, `{{BORDER}}` = `oklch(0.91 0.010 195)`, `{{FONT_DISPLAY}}` = `'Inter', 'DM Sans', sans-serif`, `{{FONT_BODY}}` = `'Inter', 'Source Sans 3', sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', monospace`, `{{RADIUS}}` = `8px`, `{{SHADOW}}` = `0 2px 8px rgba(42,138,156,0.08)`, `{{SPACING}}` = `8px`). Visual parity target: the page should read as calm and trustworthy on first glance; if any element produces a stress response (red used decoratively, jarring motion, sterile flatness), the calm-trust brief has been broken.

Upstream parity source: blocked-B.md harvest entry #12 `landing-page-builder-skill-main` (industry x theme matrix, theme #15 "Healthcare/Medical"); Master Ledger row S-048.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 105025 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Siblings: S-047 Electric Blue Modern (higher chroma, energetic prosumer rather than clinical-calm), S-049 Plumbing / Trades (deeper service-blue, trust-utility rather than clinical), S-051 Beauty / Spa (warm wellness rather than cool clinical), S-039 Warm Professional (warm-paper professional-services, not healthcare-specific)
- Differentiators: S-048 is light-mode cool-clinical-teal calibrated for calm-trust patient-facing healthcare; S-047 is energetic-residential-tech; S-049 is utility-blue for service businesses; S-051 is warm wellness-spa; S-039 is warm professional-services
- Source: `reports/batch9-harvest/blocked-B.md` harvest entry #12; `landing-page-builder-skill-main` (industry x theme matrix, theme #15)
