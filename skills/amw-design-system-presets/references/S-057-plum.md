---
id: S-057
name: Plum (Bexa Accent)
aesthetic_position: creative-intelligent-purple
source_attribution: "styles-A §Plum (Bexa Accent); Bexa-professional-frontend-design-skills-for-ai-agents skills/bexa/SKILL.md. LICENSE: MIT."
license: MIT
---

# S-057 — Plum (Bexa Accent)

**Filename:** `skills/amw-design-system-presets/references/S-057-plum.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Plum is the Bexa accent calibrated for creative tools and ML/AI platforms — purple at high saturation reads as "depth + intelligence" without slipping into the corporate-blue trap. The visual fingerprint is a deep purple primary (`hsl(276 60% 50%)`) deployed against a near-white or warm-grey field, paired with a heavy geometric display sans (Inter Display, Plus Jakarta, or Geist at 700–800 weight). Layouts are feature-forward and card-heavy: hero plus capability grid plus benchmarks plus testimonials, with medium-to-high information density. Cards use rounded corners (12–16px) and lift via colored box-shadow on hover (`0 12px 32px hsl(276 60% 50% / 0.25)`) rather than neutral grey shadow — the purple stays present even in elevation. Motion is stagger-reveal on scroll plus spotlight border-glow on card hover. Pairing Plum with corporate blue or muted slate destroys the signal; the supporting palette is warm neutral (cream, lavender-tinted grey). Intended audience: creative SaaS (design tools, video editors), ML/AI platforms, developer-experience products positioning on intelligence rather than utility, and any interface that wants to feel "premium-clever" rather than "corporate-trusted."

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #FAFAFB;            /* near-white field */
  --color-surface:    #F5F3F8;            /* lavender-tinted lift */
  --color-text:       #14101F;            /* purple-cast near-black */
  --color-text-muted: #5A526B;            /* purple-cast muted */
  --color-primary:    hsl(276 60% 50%);   /* Plum — deep purple */
  --color-primary-hover: hsl(276 60% 44%);
  --color-accent:     hsl(276 60% 50%);   /* single-accent system */
  --color-border:     #E5E0EC;            /* lavender hairline */

  /* Typography */
  --font-display: 'Inter Display', 'Plus Jakarta Sans', Geist, 'Inter', system-ui, sans-serif;
  --font-body:    'Inter', Geist, system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Geometry */
  --spacing:        8px;
  --radius:         14px;        /* rounded card corners */
  --radius-button:  10px;
  --border-width:   1px;

  /* Shadow — colored on hover (the Plum signature) */
  --shadow:           0 2px 8px rgba(20, 16, 31, 0.06);
  --shadow-card:      0 4px 12px rgba(20, 16, 31, 0.08);
  --shadow-card-hover: 0 12px 32px hsl(276 60% 50% / 0.25);

  /* Motion — stagger + spotlight */
  --motion-duration:        220ms;
  --motion-duration-stagger: 80ms;   /* per-item delay on grid reveal */
  --motion-easing:          cubic-bezier(0.22, 1, 0.36, 1); /* expo out */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#FAFAFB',
        surface:     '#F5F3F8',
        text:        '#14101F',
        'text-muted': '#5A526B',
        primary:     'hsl(276 60% 50%)',
        'primary-hover': 'hsl(276 60% 44%)',
        accent:      'hsl(276 60% 50%)',
        border:      '#E5E0EC',
      },
      fontFamily: {
        display: ['"Inter Display"', '"Plus Jakarta Sans"', 'Geist', 'Inter', 'system-ui', 'sans-serif'],
        body:    ['Inter', 'Geist', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
      },
      borderRadius: { DEFAULT: '14px', button: '10px' },
      boxShadow: {
        DEFAULT: '0 2px 8px rgba(20, 16, 31, 0.06)',
        card:       '0 4px 12px rgba(20, 16, 31, 0.08)',
        'card-hover': '0 12px 32px hsl(276 60% 50% / 0.25)',
      },
      transitionDuration: { DEFAULT: '220ms' },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #0E0A1A;
  --color-surface:    #18112A;
  --color-text:       #F0EAFB;
  --color-text-muted: #B5A8D0;
  --color-border:     #2D2240;
  --color-primary:    hsl(276 60% 60%);
  --color-primary-hover: hsl(276 60% 66%);
  --shadow-card-hover: 0 12px 32px hsl(276 60% 60% / 0.35);
}
```

## "Breaks if" invariants

- breaks if Plum is paired with corporate-blue accents (`#0066FF`, `#635BFF`, `#3B82F6`) — the dual chromatic signal collapses the "creative intelligence" register into generic SaaS
- breaks if the supporting palette desaturates to neutral cool grey (slate, zinc) instead of lavender-tinted warm grey
- breaks if hover elevation drops to neutral grey shadow — the Plum-cast colored shadow IS the elevation signature
- breaks if a serif display replaces the bold geometric sans
- breaks if card radius drops below 12px or exceeds 20px (the 14px midpoint is canonical for the Plum register)
- breaks if motion drops the stagger-on-reveal pattern — grids must cascade, not appear instantaneously
- breaks if the Plum saturation falls below 50% (low-sat purple reads as melancholy editorial, not platform intelligence)
- breaks if any gradient introduces non-purple hues — Plum tolerates purple-to-magenta or purple-to-violet but never purple-to-blue

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` — Plum named-accent definition (`hsl(276 60% 50%)` accent, creative-tools/ML archetype).
Parity threshold: A-class (single-accent token + heavy geometric display + colored-shadow hover signature).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 111355 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling Bexa accents:** S-056 Ember (warm orange-red CTA), S-058 Rose Smoke (fashion/beauty rose-red), S-059 Sable (luxury editorial dark-first)
- **Adjacent styles:** S-009 Aurora (gradient cousin), S-010 Cyberpunk (high-energy purple-cyan opposition), S-017 Corporate Bold (blue alternative)
- **Source attribution:** `reports/batch9-harvest/styles-A.md` §Plum (Bexa Accent); upstream `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` (MIT)
