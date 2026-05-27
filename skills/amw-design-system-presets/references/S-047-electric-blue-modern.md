<!--
  Clean-room transcription. Source: blocked-B harvest entry #12 (`landing-page-builder-skill-main`)
  industry x theme matrix, theme #14 "Electric Blue Modern". Upstream license is unknown;
  this file contains no source code, only the documented aesthetic intent (hue/lightness/chroma)
  and derivations consistent with generally-accepted light-UI conventions.
-->
---
id: S-047
name: Electric Blue Modern
aesthetic_position: light-energetic-tech
source_attribution: >
  blocked-B.md harvest entry #12 `landing-page-builder-skill-main` (industry x theme matrix,
  theme #14 "Electric Blue Modern"); Master Ledger row S-047. Clean-room transcription from
  documented hue/lightness/chroma values; no upstream code is reused.
license: clean-room (upstream license unknown; derivations from public-domain oklch color values)
---

# S-047 — Electric Blue Modern

**Filename:** `skills/amw-design-system-presets/references/S-047-electric-blue-modern.md`
**Tracked in:** this repo (skills/ is git-tracked)

## Identity

Electric Blue Modern is a light-mode aesthetic engineered for residential-tech, smart-home, IoT consumer-facing brands, energetic prosumer products, and any landing page that must read as both technically capable and emotionally upbeat. Its visual fingerprint is an electric blue primary (`oklch(0.55 0.22 255)`) sitting on a clean cool-tinted white canvas, with deliberately high chroma (`C=0.22`) so the blue reads as charged rather than corporate. Typography is a contemporary geometric sans (Inter or DM Sans) at standard weights — the energy comes from the colour, not from typographic personality. Surfaces are layered in subtle cool-grey tones; the radius is generous (8-12px) which together with soft cool shadows pushes the register toward "consumer technology that is friendly" rather than "enterprise software that is reliable". One chromatic accent is the rule (electric blue), and complementary cool greys do the secondary work; introducing a warm accent breaks the temperature-coherence that gives this style its signature freshness.

## Token block

```css
/* S-047 Electric Blue Modern — CSS custom properties (oklch primary; hex fallback) */
:root {
  /* Color — oklch source of truth */
  --color-bg:           oklch(0.99 0.005 255);  /* cool-tinted near-white */
  --color-surface:      oklch(0.97 0.008 255);  /* card / panel surface */
  --color-surface-2:    oklch(0.94 0.010 255);  /* elevated surface (modal, aside) */
  --color-text:         oklch(0.20 0.02 255);   /* near-black, cool-leaning */
  --color-text-muted:   oklch(0.50 0.02 255);   /* muted cool grey */
  --color-primary:      oklch(0.55 0.22 255);   /* electric blue — primary brand */
  --color-primary-dim:  oklch(0.45 0.22 255);   /* pressed / hover state */
  --color-accent:       oklch(0.55 0.22 255);   /* one-chromatic-signal contract */
  --color-border:       oklch(0.90 0.012 255);  /* soft cool-grey hairline */
  --color-focus-ring:   oklch(0.55 0.22 255 / 0.35);

  /* Hex fallback for older browsers (approximate sRGB) */
  --color-bg-hex:       #FBFCFE;
  --color-surface-hex:  #F4F6FA;
  --color-text-hex:     #1F2538;
  --color-primary-hex:  #2563EB;
  --color-border-hex:   #DCE2EE;

  /* Typography — geometric sans, energetic but neutral */
  --font-display: 'Inter', 'DM Sans', 'Space Grotesk', 'Helvetica Neue', sans-serif;
  --font-body:    'Inter', 'DM Sans', 'Helvetica Neue', Arial, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Spacing */
  --spacing: 8px;

  /* Shape — generous radius reads as consumer-friendly */
  --radius: 10px;

  /* Shadow — cool-tinted, soft */
  --shadow: 0 4px 14px rgba(37, 99, 235, 0.10);
  --shadow-elev: 0 12px 28px rgba(37, 99, 235, 0.14);

  /* Motion — quick and confident */
  --motion-duration: 180ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);

  /* Energetic extras */
  --border-width: 1px;
  --glow-primary: 0 0 0 4px oklch(0.55 0.22 255 / 0.20);  /* focus ring on CTAs */
  --gradient-hero: linear-gradient(135deg, oklch(0.55 0.22 255), oklch(0.65 0.18 245));
}
```

```ts
// S-047 Electric Blue Modern — Tailwind theme extension
const electricBlueModern = {
  colors: {
    bg:           'oklch(0.99 0.005 255)',
    surface:      'oklch(0.97 0.008 255)',
    'surface-2':  'oklch(0.94 0.010 255)',
    text:         'oklch(0.20 0.02 255)',
    'text-muted': 'oklch(0.50 0.02 255)',
    primary:      'oklch(0.55 0.22 255)',
    'primary-dim':'oklch(0.45 0.22 255)',
    border:       'oklch(0.90 0.012 255)',
  },
  fontFamily: {
    display: ['Inter', '"DM Sans"', '"Space Grotesk"', '"Helvetica Neue"', 'sans-serif'],
    body:    ['Inter', '"DM Sans"', '"Helvetica Neue"', 'Arial', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
  },
  spacing:      { base: '8px' },
  borderRadius: { DEFAULT: '10px' },
  boxShadow:    {
    DEFAULT: '0 4px 14px rgba(37,99,235,0.10)',
    elev:    '0 12px 28px rgba(37,99,235,0.14)',
  },
  transitionDuration:      { DEFAULT: '180ms' },
  transitionTimingFunction:{ DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if a warm chromatic accent (orange, red, amber) is introduced alongside the electric blue — the temperature-coherent palette is what produces the signature freshness; warm + cool yields generic-startup chroma
- breaks if the canvas shifts to a warm-tinted off-white (cream, beige) — the cool-leaning bg is what frames the electric blue as charged rather than corporate; warm bg neutralises the energy
- breaks if the primary blue chroma drops below `C=0.16` — the high chroma is what produces the "electric" reading; a muted blue at `C<0.16` reads as standard corporate or Material default
- breaks if border-radius falls below 6px on primary UI elements — the consumer-friendly tone requires generous corners; sharp edges shift the register toward Industrial Trust (S-046) or Corporate Bold (S-017)
- breaks if the primary blue is used on more than 30% of the screen surface area — even a high-energy palette needs neutral breathing room; flooding with blue produces a single-block poster, not a usable product UI
- breaks if shadows go neutral-grey (`rgba(0,0,0,...)`) rather than blue-tinted — the cool-tinted shadow is part of the temperature-coherent palette; neutral shadows clash with the blue accent
- breaks if a serif display font is introduced — the energetic-modern register requires a geometric sans throughout; a serif headline signals editorial or professional-services, not residential tech
- breaks if the dark-mode variant inverts to pure black (`oklch(0 0 0)`) — the dark-mode variant should remain cool-tinted (`oklch(0.16 0.02 255)`) to preserve the temperature-coherent palette; pure black breaks the chromatic continuity

## Canonical render-test pointer

Render test: inject this file's tokens into `skills/amw-design-system-presets/references/_test-skeleton.html` (substituting `{{BG}}` = `oklch(0.99 0.005 255)`, `{{SURFACE}}` = `oklch(0.97 0.008 255)`, `{{TEXT}}` = `oklch(0.20 0.02 255)`, `{{TEXT_MUTED}}` = `oklch(0.50 0.02 255)`, `{{PRIMARY}}` = `oklch(0.55 0.22 255)`, `{{ACCENT}}` = `oklch(0.55 0.22 255)`, `{{BORDER}}` = `oklch(0.90 0.012 255)`, `{{FONT_DISPLAY}}` = `'Inter', 'DM Sans', sans-serif`, `{{FONT_BODY}}` = `'Inter', 'DM Sans', sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', monospace`, `{{RADIUS}}` = `10px`, `{{SHADOW}}` = `0 4px 14px rgba(37,99,235,0.10)`, `{{SPACING}}` = `8px`). Visual parity target: the hero CTA should read as charged and inviting against the cool-near-white field; if the page looks tepid or corporate-flat, the primary chroma has likely been dropped below `C=0.16`.

Upstream parity source: blocked-B.md harvest entry #12 `landing-page-builder-skill-main` (industry x theme matrix, theme #14 "Electric Blue Modern"); Master Ledger row S-047.

## Render-test verdict

JOD: pending

## Cross-references

- Siblings: S-017 Corporate Bold / Enterprise Solid (cooler navy + muted purple — corporate, not energetic), S-038 Dark Tech (dark canvas + electric blue accent — developer tools rather than consumer prosumer), S-023 Vibrant Friendly / Playful SaaS (multi-color rather than one-chromatic, playful rather than energetic-modern), S-049 Plumbing / Trades (deeper water-blue + service-trust framing, not high-energy)
- Differentiators: S-047 is light-mode energetic-modern with one electric-blue primary calibrated for residential tech / smart-home / IoT; S-017 is dim-corporate B2B; S-038 is dark developer-tool; S-049 is service-utility trust-blue (lower chroma, different hue band)
- Source: `blocked-B.md` harvest entry #12; `landing-page-builder-skill-main` (industry x theme matrix, theme #14)
