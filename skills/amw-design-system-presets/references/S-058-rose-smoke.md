---
id: S-058
name: Rose Smoke (Bexa Accent)
aesthetic_position: fashion-beauty-editorial-rose
source_attribution: "styles-A §Rose Smoke (Bexa Accent); Bexa-professional-frontend-design-skills-for-ai-agents skills/bexa/SKILL.md. LICENSE: MIT."
license: MIT
---

# S-058 — Rose Smoke (Bexa Accent)

**Filename:** `skills/amw-design-system-presets/references/S-058-rose-smoke.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Rose Smoke is the Bexa accent tuned for brand-expressive fashion, beauty, and lifestyle products — soft premium with a confident edge. The visual fingerprint is a warm rose-red primary (`hsl(348 62% 46%)`) that stays desaturated on surfaces (used at 8–15% alpha for tinted backgrounds) and only goes vivid as a punctual accent — CTAs, link underlines, decorative rules. Typography pairs an elegant serif display (Fraunces variable, Cormorant Garamond) with either a complementary humanist sans (Inter Tight, DM Sans) or stays serif-only for full editorial register. Layouts are editorial-first: generous margins, low-medium density, asymmetric image-to-text rhythms reminiscent of glossy magazine spreads. Soft radius (8–12px) and minimal elevation — shadows, when present, are warm-cast (`0 4px 16px rgba(170, 60, 80, 0.08)`) rather than neutral grey. Motion is soft fade and stagger reveal; no springs, no aggressive easing. Pairing Rose Smoke with cold tech neutrals (slate, cyan) flattens the warmth signal; the supporting palette is cream, dusty rose, and warm sand. Intended audience: fashion e-commerce, beauty brands, lifestyle publications, wellness products, boutique hospitality, and creator portfolios in the "premium-feminine" register without overt cliché.

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #FBF6F4;            /* warm cream-rose field */
  --color-surface:    #F5ECE8;            /* dusty rose surface */
  --color-text:       #1F1418;            /* warm near-black */
  --color-text-muted: #6B5A5F;            /* warm muted */
  --color-primary:    hsl(348 62% 46%);   /* Rose Smoke — warm rose-red */
  --color-primary-hover: hsl(348 62% 40%);
  --color-primary-soft: hsl(348 62% 46% / 0.12); /* tinted-surface use */
  --color-accent:     hsl(348 62% 46%);   /* single-accent system */
  --color-border:     #E8D8D4;            /* warm rose hairline */

  /* Typography */
  --font-display: 'Fraunces', 'Cormorant Garamond', 'Playfair Display', Georgia, serif;
  --font-body:    'Inter Tight', 'DM Sans', 'Inter', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

  /* Optical-size variable font (Fraunces supports opsz 9–144 + SOFT 0–100) */
  --font-display-opsz-headline: 'opsz' 96, 'SOFT' 50;
  --font-display-opsz-deck:     'opsz' 36, 'SOFT' 70;
  --font-display-opsz-body:     'opsz' 14, 'SOFT' 100;

  /* Geometry */
  --spacing:      8px;
  --radius:       10px;            /* soft radius 8–12px range, midpoint */
  --border-width: 1px;

  /* Shadow — warm-cast, minimal */
  --shadow:       0 1px 4px rgba(170, 60, 80, 0.04);
  --shadow-card:  0 4px 16px rgba(170, 60, 80, 0.08);

  /* Motion — soft fades, no spring */
  --motion-duration:        320ms;
  --motion-duration-stagger: 60ms;
  --motion-easing:          cubic-bezier(0.4, 0, 0.2, 1); /* gentle */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#FBF6F4',
        surface:     '#F5ECE8',
        text:        '#1F1418',
        'text-muted': '#6B5A5F',
        primary:     'hsl(348 62% 46%)',
        'primary-hover': 'hsl(348 62% 40%)',
        'primary-soft': 'hsl(348 62% 46% / 0.12)',
        accent:      'hsl(348 62% 46%)',
        border:      '#E8D8D4',
      },
      fontFamily: {
        display: ['Fraunces', '"Cormorant Garamond"', '"Playfair Display"', 'Georgia', 'serif'],
        body:    ['"Inter Tight"', '"DM Sans"', 'Inter', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
      },
      borderRadius: { DEFAULT: '10px', sm: '8px', md: '12px' },
      boxShadow: {
        DEFAULT: '0 1px 4px rgba(170, 60, 80, 0.04)',
        card:    '0 4px 16px rgba(170, 60, 80, 0.08)',
      },
      transitionDuration: { DEFAULT: '320ms' },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #1F1418;
  --color-surface:    #2E1F25;
  --color-text:       #F5ECE8;
  --color-text-muted: #C8B5BA;
  --color-border:     #3D2A30;
  --color-primary:    hsl(348 62% 56%);
  --color-primary-hover: hsl(348 62% 62%);
  --color-primary-soft: hsl(348 62% 56% / 0.15);
}
```

## "Breaks if" invariants

- breaks if Rose Smoke is paired with cold-tech neutrals (slate, cyan, electric blue) — the supporting palette must stay warm
- breaks if a heavy grotesque display (Space Grotesk 800, Cabinet 900) replaces the elegant serif — the editorial register depends on type contrast
- breaks if the rose-red goes vivid as a tinted surface background (saturation must drop to ~12% alpha for surface use)
- breaks if radius drops below 8px or exceeds 12px on cards
- breaks if motion adopts springs or bounces — Rose Smoke is fade and stagger only
- breaks if shadows go neutral grey instead of warm rose-cast
- breaks if density jumps to data-dashboard levels — editorial generous margins are structural
- breaks if multiple chromatic accents share weight with the rose — the single-accent monolith is the signature

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` — Rose Smoke named-accent definition (`hsl(348 62% 46%)` accent, fashion/beauty archetype).
Parity threshold: A-class (single-accent token + serif/sans editorial pair + warm-cast shadow + soft fade motion).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 122460 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling Bexa accents:** S-056 Ember (warm energy CTA), S-057 Plum (creative purple), S-059 Sable (luxury editorial dark-first)
- **Adjacent styles:** S-014 Editorial Serif (display-serif cousin), S-015 Fashion Luxury Editorial (boutique-grade sibling), S-045 Warm Minimalism (Notion-warm low-energy cousin)
- **Source attribution:** `reports/batch9-harvest/styles-A.md` §Rose Smoke (Bexa Accent); upstream `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` (MIT)
