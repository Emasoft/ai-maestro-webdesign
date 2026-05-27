---
id: S-060
name: Beam "The Stripe" (Stitch Preset)
aesthetic_position: precision-instrument-saas
source_attribution: "styles-A §Beam (Stitch Preset); design-forge-main/references/discovery-framework.md. LICENSE: MIT (inferred from repo)."
license: MIT (inferred)
---

# S-060 — Beam "The Stripe" (Stitch Preset)

**Filename:** `skills/amw-design-system-presets/references/S-060-beam-the-stripe.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Beam is the design-forge "Stitch" archetype labeled "The Stripe" — premium, precise, modern SaaS calibrated to feel like a *precision instrument*. The visual fingerprint is a clean white or near-white base, a single chromatic accent (blue or purple at moderate saturation — `#635BFF`-class), a minimal secondary palette of cool greys, and the signature Clash Display + General Sans type pair. Clash Display (weights 600/700) provides geometric authority in headlines and section markers; General Sans (weights 400/500) carries body copy with a calmer humanist register. Layouts are structured-whitespace and content-first: medium information density, generous section gutters, deliberate type-rhythm. Geometry is restrained — 4–6px corner radius (just enough to soften, never enough to read "playful") and light box shadows (`0 1px 3px rgba(0,0,0,0.06)`) for micro-elevation. Motion is the canonical Beam signature: gentle springs with precise expo easing (`cubic-bezier(0.22, 1, 0.36, 1)`), never bouncy, never aggressive. Pairing Beam with warm tones, hand-drawn shapes, or playful color collapses the precision-instrument register. Intended audience: B2B SaaS marketing sites, developer-tools positioning, fintech product surfaces, infrastructure platforms, and any product where the design promise is "carefully engineered."

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #FFFFFF;            /* clean white base */
  --color-surface:    #FAFAFB;            /* near-white lift */
  --color-surface-2:  #F4F5F7;            /* second elevation */
  --color-text:       #0F1115;            /* near-black */
  --color-text-muted: #5A6071;            /* cool muted grey */
  --color-text-faint: #8A8F9C;            /* faint label */
  --color-primary:    #635BFF;            /* Stripe-purple class accent */
  --color-primary-hover: #524BDD;
  --color-accent:     #635BFF;            /* single-accent system */
  --color-border:     #E5E7EB;            /* cool hairline */

  /* Typography — Clash Display + General Sans pair */
  --font-display: 'Clash Display', 'Inter Display', Inter, system-ui, sans-serif;
  --font-body:    'General Sans', Inter, system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  --font-weight-display: 600;   /* Clash 600/700 canonical */
  --font-weight-body:    400;   /* General Sans 400/500 */

  /* Geometry */
  --spacing:      8px;
  --radius:       5px;           /* 4–6px range — 5px is canonical midpoint */
  --radius-button: 6px;
  --border-width: 1px;

  /* Shadow — light box shadow for micro-elevation */
  --shadow:       0 1px 3px rgba(15, 17, 21, 0.06);
  --shadow-card:  0 4px 12px rgba(15, 17, 21, 0.08);

  /* Motion — gentle spring with precise expo easing (Beam signature) */
  --motion-duration: 200ms;
  --motion-easing:   cubic-bezier(0.22, 1, 0.36, 1); /* expo out — precise, no overshoot */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#FFFFFF',
        surface:     '#FAFAFB',
        'surface-2': '#F4F5F7',
        text:        '#0F1115',
        'text-muted': '#5A6071',
        'text-faint': '#8A8F9C',
        primary:     '#635BFF',
        'primary-hover': '#524BDD',
        accent:      '#635BFF',
        border:      '#E5E7EB',
      },
      fontFamily: {
        display: ['"Clash Display"', '"Inter Display"', 'Inter', 'system-ui', 'sans-serif'],
        body:    ['"General Sans"', 'Inter', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
      },
      fontWeight: { display: '600', body: '400' },
      borderRadius: { DEFAULT: '5px', sm: '4px', md: '6px', button: '6px' },
      boxShadow: {
        DEFAULT: '0 1px 3px rgba(15, 17, 21, 0.06)',
        card:    '0 4px 12px rgba(15, 17, 21, 0.08)',
      },
      transitionDuration:       { DEFAULT: '200ms' },
      transitionTimingFunction: { expo: 'cubic-bezier(0.22, 1, 0.36, 1)' },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #0F1115;
  --color-surface:    #1A1D24;
  --color-surface-2:  #232730;
  --color-text:       #FAFAFB;
  --color-text-muted: #A5ABBA;
  --color-text-faint: #6C7280;
  --color-border:     #2A2E38;
  --color-primary:    #8A82FF;       /* lifted for dark contrast */
  --color-primary-hover: #9A93FF;
}
```

## "Breaks if" invariants

- breaks if warm tones (cream, terracotta, gold) enter any layer — Beam is cool-neutral by definition
- breaks if hand-drawn, organic, or sketchy shapes appear — the precision-instrument promise depends on geometric discipline
- breaks if color saturation exceeds the moderate-purple register — playful or vivid color collapses the SaaS-precision signal
- breaks if `border-radius` falls below 4px or exceeds 6px on cards/buttons
- breaks if motion adopts springs with overshoot (bouncy `cubic-bezier(0.34, 1.56, 0.64, 1)`) — Beam uses expo-out for precise non-bouncy gentleness
- breaks if the Clash Display + General Sans pair is substituted by a single-family stack — the display/body type contrast is structural
- breaks if shadows go heavy (`0 8px 32px rgba(0,0,0,0.2)`) — micro-elevation only
- breaks if information density jumps to data-dashboard levels — structured whitespace is the rhythm

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `design-forge-main/references/discovery-framework.md` — Stitch preset "Beam / The Stripe" archetype (Clash Display + General Sans, 4–6px radius, light shadow, expo easing).
Parity threshold: A-class (type pair + radius range + motion signature; no upstream rendered demo, justified).

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling Stitch presets:** S-061 Kinetic (Cabinet Grotesk + Satoshi, motion-driven), S-062 Luxury "The Luxury" (Cormorant + Tenor Sans, dark + gold)
- **Adjacent styles:** S-017 Corporate Bold (deep-navy SaaS cousin), S-051 Stitch "The Builder" (Space Grotesk + Inter, technical sibling)
- **Source attribution:** `reports/batch9-harvest/styles-A.md` §Beam (Stitch Preset) — "The Stripe"; upstream `design-forge-main/references/discovery-framework.md` (MIT inferred)
