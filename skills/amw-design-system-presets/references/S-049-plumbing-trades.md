---
id: S-049
name: Plumbing / Trades
aesthetic_position: light-service-utility-trust
source_attribution: >
  blocked-B.md harvest entry #12 `landing-page-builder-skill-main` (industry x theme matrix,
  theme #16 "Plumbing/Trades"); Master Ledger row S-049. Clean-room transcription from
  documented hue/lightness/chroma values; no upstream code is reused.
license: clean-room (upstream license unknown; derivations from public-domain oklch color values)
---

<!--
  Clean-room transcription. Source: blocked-B harvest entry #12 (`landing-page-builder-skill-main`)
  industry x theme matrix, theme #16 "Plumbing/Trades". Upstream license is unknown;
  this file contains no source code, only the documented aesthetic intent (hue/lightness/chroma)
  and derivations consistent with generally-accepted service-utility-UI conventions.
-->

# S-049 — Plumbing / Trades

**Filename:** `skills/amw-design-system-presets/references/S-049-plumbing-trades.md`
**Tracked in:** this repo (skills/ is git-tracked)

## Identity

Plumbing Trades is a light-mode aesthetic engineered for residential and small-business service brands: plumbers, electricians, HVAC, roofing, landscaping, locksmiths, garage-door companies, and any local-services brand whose customer pages must communicate "reliable, established, will-show-up-when-promised". Its visual fingerprint is a deeper water blue (`oklch(0.50 0.18 240)`) on a clean light canvas — the blue is darker and slightly bluer than the teal of healthcare (S-048) and less electric than S-047, calibrated to read as utilitarian-trustworthy rather than clinical or energetic. Typography is a sturdy, slightly condensed sans (Inter or Barlow) — the kind of typography that a service-truck or business-card uses without irony. Surfaces are flat with low elevation; the radius is moderate (6-8px); shadows are minimal and cool. A single contrasting CTA color (often a warm yellow or orange) may be used for "Call Now" or "Book a Service" buttons — this is the only permissible departure from the one-chromatic-signal rule, because phone-call conversion is the page's primary job and the contrast is the conversion mechanism. Information hierarchy follows the trade-services brief: prominent phone number, prominent service area, prominent "available now / next-day", customer reviews near the top.

## Token block

```css
/* S-049 Plumbing / Trades — CSS custom properties (oklch primary; hex fallback) */
:root {
  /* Color — oklch source of truth */
  --color-bg:           oklch(0.99 0.005 240);  /* clean near-white, slight cool tint */
  --color-surface:      oklch(0.96 0.008 240);  /* card / panel surface */
  --color-surface-2:    oklch(0.93 0.010 240);  /* elevated surface (modal, aside) */
  --color-text:         oklch(0.22 0.03 240);   /* deep cool slate */
  --color-text-muted:   oklch(0.50 0.02 240);   /* labels, secondary text */
  --color-primary:      oklch(0.50 0.18 240);   /* water blue — primary brand */
  --color-primary-dim:  oklch(0.40 0.18 240);   /* pressed / hover state */
  --color-accent:       oklch(0.50 0.18 240);   /* matches primary by default */
  --color-cta:          oklch(0.78 0.17 65);    /* warm yellow-orange — "Call Now" only */
  --color-cta-dim:      oklch(0.70 0.17 65);    /* pressed / hover CTA */
  --color-border:       oklch(0.90 0.012 240);  /* soft cool-grey hairline */
  --color-success:      oklch(0.60 0.15 145);   /* "Available now" badge */
  --color-focus-ring:   oklch(0.50 0.18 240 / 0.35);

  /* Hex fallback for older browsers (approximate sRGB) */
  --color-bg-hex:       #FAFCFE;
  --color-surface-hex:  #F0F4F9;
  --color-text-hex:     #1F2638;
  --color-primary-hex:  #1F5BD1;
  --color-cta-hex:      #E2A03A;
  --color-border-hex:   #D8DFEB;

  /* Typography — sturdy, slightly condensed sans */
  --font-display: 'Barlow', 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --font-body:    'Inter', 'Barlow', 'Helvetica Neue', Arial, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Spacing — readable for older customers, mobile-first */
  --spacing: 8px;
  --line-height-body: 1.55;

  /* Shape — utilitarian without playful */
  --radius: 6px;

  /* Shadow — minimal, cool, low-elevation */
  --shadow: 0 2px 6px rgba(31, 91, 209, 0.08);
  --shadow-elev: 0 6px 18px rgba(31, 91, 209, 0.12);

  /* Motion — quick and direct (utility, not theatrical) */
  --motion-duration: 160ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);

  /* Trades extras */
  --border-width: 1px;
  --color-cta-text: oklch(0.18 0.03 240);   /* dark text on warm CTA for AA contrast */
  --color-phone-text: oklch(0.50 0.18 240); /* phone numbers styled in primary blue */
}
```

```ts
// S-049 Plumbing / Trades — Tailwind theme extension
const plumbingTrades = {
  colors: {
    bg:           'oklch(0.99 0.005 240)',
    surface:      'oklch(0.96 0.008 240)',
    'surface-2':  'oklch(0.93 0.010 240)',
    text:         'oklch(0.22 0.03 240)',
    'text-muted': 'oklch(0.50 0.02 240)',
    primary:      'oklch(0.50 0.18 240)',
    'primary-dim':'oklch(0.40 0.18 240)',
    cta:          'oklch(0.78 0.17 65)',
    'cta-dim':    'oklch(0.70 0.17 65)',
    border:       'oklch(0.90 0.012 240)',
    success:      'oklch(0.60 0.15 145)',
  },
  fontFamily: {
    display: ['Barlow', 'Inter', '"Helvetica Neue"', 'Arial', 'sans-serif'],
    body:    ['Inter', 'Barlow', '"Helvetica Neue"', 'Arial', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
  },
  spacing:      { base: '8px' },
  borderRadius: { DEFAULT: '6px' },
  boxShadow:    {
    DEFAULT: '0 2px 6px rgba(31,91,209,0.08)',
    elev:    '0 6px 18px rgba(31,91,209,0.12)',
  },
  transitionDuration:      { DEFAULT: '160ms' },
  transitionTimingFunction:{ DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if the warm CTA color appears on anything other than primary phone-call / book-service buttons — the contrast-pair (cool blue brand + warm CTA) only works as a conversion mechanism when the warm color is scarce; using it for general accent or decoration dissolves the signal
- breaks if the primary blue hue shifts below 220 (cyan-leaning) or above 250 (purple-leaning) — the 240 hue is the documented water-blue band; cyan reads as healthcare (S-048), purple reads as legal (S-050)
- breaks if the primary blue chroma drops below `C=0.14` — a muted blue at low chroma reads as generic corporate (S-017) rather than service-trust-utility
- breaks if border-radius exceeds 10px — service-utility brief requires utilitarian corners; rounded corners shift the tone toward consumer-app or hospitality
- breaks if the typography becomes a delicate serif or a thin geometric — service brands need sturdy, "readable from a service-truck door at 20 feet" type; thin or decorative type undermines the trust signal
- breaks if shadows go warm-toned — the cool palette is temperature-coherent; warm shadows produce visible clash on the cool blue surfaces
- breaks if the page omits a prominent phone number above the fold — the conversion brief for trades is phone-call first; design without prominent phone is a different style entirely
- breaks if motion uses bounce or elastic easing — utility brief requires direct, confident transitions; playful motion undermines the established-and-reliable framing
- breaks if a second cool chromatic color is introduced (teal, green, cyan) — the single-cool + single-warm CTA contract is what makes the design legible at glance; multiplying cools muddles the brand

## Canonical render-test pointer

Render test: inject this file's tokens into `skills/amw-design-system-presets/references/_test-skeleton.html` (substituting `{{BG}}` = `oklch(0.99 0.005 240)`, `{{SURFACE}}` = `oklch(0.96 0.008 240)`, `{{TEXT}}` = `oklch(0.22 0.03 240)`, `{{TEXT_MUTED}}` = `oklch(0.50 0.02 240)`, `{{PRIMARY}}` = `oklch(0.50 0.18 240)`, `{{ACCENT}}` = `oklch(0.78 0.17 65)`, `{{BORDER}}` = `oklch(0.90 0.012 240)`, `{{FONT_DISPLAY}}` = `Barlow, Inter, sans-serif`, `{{FONT_BODY}}` = `Inter, Barlow, sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', monospace`, `{{RADIUS}}` = `6px`, `{{SHADOW}}` = `0 2px 6px rgba(31,91,209,0.08)`, `{{SPACING}}` = `8px`). Visual parity target: the warm CTA button should pop against the cool blue brand surface as the single most attention-grabbing element on the page; if a customer's eye doesn't go straight to "Call Now" within one second, the contrast pair has been misapplied.

Upstream parity source: blocked-B.md harvest entry #12 `landing-page-builder-skill-main` (industry x theme matrix, theme #16 "Plumbing/Trades"); Master Ledger row S-049.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 102445 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Siblings: S-047 Electric Blue Modern (higher-chroma electric blue, residential-tech rather than service-trades), S-048 Healthcare / Medical (lower-chroma teal, clinical-calm rather than service-utility), S-046 Industrial / Trust Authority (dark-mode B2B rather than light-mode local-services), S-017 Corporate Bold (corporate B2B SaaS rather than local-services)
- Differentiators: S-049 is light-mode water-blue with a deliberate warm CTA contrast pair calibrated for phone-call conversion in residential service trades; S-047 is energetic-prosumer; S-048 is clinical-calm; S-046 is dark-mode B2B industrial; S-017 is corporate SaaS
- Source: `reports/batch9-harvest/blocked-B.md` harvest entry #12; `landing-page-builder-skill-main` (industry x theme matrix, theme #16)
