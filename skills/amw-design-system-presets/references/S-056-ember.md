---
id: S-056
name: Ember (Bexa Accent)
aesthetic_position: warm-energetic-cta
source_attribution: "styles-A §Ember (Bexa Accent); Bexa-professional-frontend-design-skills-for-ai-agents skills/bexa/SKILL.md. LICENSE: MIT."
license: MIT
---

# S-056 — Ember (Bexa Accent)

**Filename:** `skills/amw-design-system-presets/references/S-056-ember.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Ember is the Bexa accent system tuned for energy, urgency, and startup momentum — the palette you reach for when the page exists to drive a click. The visual fingerprint is a warm orange-red primary (`hsl(22 90% 50%)`) deployed as the dominant chromatic event, paired with a bold geometric grotesque (Space Grotesk or Plus Jakarta Sans) at heavy display weights. Layouts are marketing-heavy: hero plus feature grid plus pricing plus testimonial plus CTA rail, with prominent rounded-pill buttons and medium card radius (10–14px). Motion is spring-based and reactive — CTAs visibly respond to hover with scale, glow, or color-shift. Supporting palette stays warm (cream, ivory, deep brown) rather than cool, because pairing Ember with cool greys collapses its energetic signal. Intended audience: SaaS landing pages targeting conversion, consumer mobile-app marketing sites, fitness and creator-economy products, and any interface where the CTA must dominate.

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #FFFFFF;            /* clean white field */
  --color-surface:    #FFF7F0;            /* warm cream lift */
  --color-text:       #1A0F0A;            /* warm near-black */
  --color-text-muted: #5C4A3F;            /* warm muted */
  --color-primary:    hsl(22 90% 50%);    /* Ember — warm orange-red */
  --color-primary-hover: hsl(22 90% 44%); /* darker on hover */
  --color-accent:     hsl(22 90% 50%);    /* single-accent system */
  --color-border:     #E8DCD2;            /* warm hairline */

  /* Typography */
  --font-display: 'Space Grotesk', 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
  --font-body:    'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Geometry */
  --spacing:        8px;
  --radius:         12px;            /* medium card radius */
  --radius-pill:    9999px;          /* CTA buttons */
  --border-width:   1px;

  /* Shadow — warm cast on lift */
  --shadow:       0 2px 8px rgba(230, 90, 30, 0.10);
  --shadow-cta:   0 8px 24px rgba(230, 90, 30, 0.25);

  /* Motion — spring-driven */
  --motion-duration: 220ms;
  --motion-easing:   cubic-bezier(0.34, 1.56, 0.64, 1); /* gentle overshoot */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#FFFFFF',
        surface:     '#FFF7F0',
        text:        '#1A0F0A',
        'text-muted': '#5C4A3F',
        primary:     'hsl(22 90% 50%)',
        'primary-hover': 'hsl(22 90% 44%)',
        accent:      'hsl(22 90% 50%)',
        border:      '#E8DCD2',
      },
      fontFamily: {
        display: ['"Space Grotesk"', '"Plus Jakarta Sans"', 'Inter', 'system-ui', 'sans-serif'],
        body:    ['"Plus Jakarta Sans"', 'Inter', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
      },
      borderRadius: { DEFAULT: '12px', pill: '9999px' },
      boxShadow: {
        DEFAULT: '0 2px 8px rgba(230, 90, 30, 0.10)',
        cta:     '0 8px 24px rgba(230, 90, 30, 0.25)',
      },
      transitionDuration:       { DEFAULT: '220ms' },
      transitionTimingFunction: { spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)' },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #1A0F0A;
  --color-surface:    #2A1B12;
  --color-text:       #FFF7F0;
  --color-text-muted: #C8B5A8;
  --color-border:     #3D2A1F;
  --color-primary:    hsl(22 90% 56%);
  --color-primary-hover: hsl(22 90% 62%);
}
```

## "Breaks if" invariants

- breaks if a cool-toned secondary accent (blue, teal, slate) shares prominence with the Ember orange — the warm monolith is the signature
- breaks if the supporting palette desaturates to neutral greys instead of warm creams/browns
- breaks if CTA buttons drop the rounded-pill geometry in favor of sharp or 4px radius
- breaks if motion duration falls below 180ms or removes the spring easing — energy comes from the bounce
- breaks if card radius collapses to 0–4px (hard edges contradict the energetic, approachable register)
- breaks if the orange accent appears below ~12% of visible surface area on landing pages — Ember must dominate
- breaks if a serif display typeface replaces the bold geometric grotesque
- breaks if hover states do not visibly react (scale, glow, or color-shift) — static CTAs collapse the energy promise

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` — Ember named-accent definition (`hsl(22 90% 50%)` accent, marketing/CTA archetype).
Parity threshold: A-class (single-accent token + grotesque type-pair + spring motion).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 106934 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling Bexa accents:** S-057 Plum (creative/ML purple), S-058 Rose Smoke (fashion/beauty rose-red), S-059 Sable (luxury editorial dark-first)
- **Adjacent styles:** S-017 Corporate Bold (cool counterpart, Stripe purple), S-045 Warm Minimalism (warm-paper editorial, low-energy cousin)
- **Source attribution:** `reports/batch9-harvest/styles-A.md` §Ember (Bexa Accent); upstream `reports_dev/batch9/extracted/Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` (MIT)
