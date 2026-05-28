---
id: S-078
name: Crayon (Warm Beige + Handwritten)
aesthetic_position: editorial-warm-paper
source_attribution: "styles-A §Crayon (Warm Beige + Handwritten); upstream: `claude-design-mode-main/README.md` 'Crayon' design example. LICENSE: MIT."
license: MIT
---

# S-078 — Crayon (Warm Beige + Handwritten)

## Identity

Crayon is the "well-designed Notion page with personality" idiom — a warm beige paper-stock background, Inter Tight providing the structural display rhythm with tight tracking, and Caveat (a credible web-safe handwriting face) deployed strictly as annotation: callouts, sticky-note labels, highlighter underlines, single-line margin notes. The chrome wears the macOS window metaphor (three traffic-light dots, titlebar, soft 8–12px rounded panels with light warm shadows). The accent is a single muted earth tone — a clay, a sage, a soft terracotta — applied sparingly. Reach for it when the brief is a personal portfolio, a writer's blog, a small-team productivity tool, a course-notes site, an internal wiki that needs warmth, or any product where the implied promise is "human, considered, slightly playful, not corporate." Avoid for fintech, enterprise SaaS, hard-news editorial — Crayon is too soft and too informal.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  --primary:      #2B2A26;   /* warm near-black ink */
  --accent:       #C97B5A;   /* muted clay terracotta — the single accent */
  --bg:           #F5EFE3;   /* warm beige paper-stock — the defining ground */
  --surface:      #FAF6EC;   /* sticky-note / panel surface — lighter beige */
  --surface-elev: #FFFFFF;   /* macOS-window inner content (one step lighter than surface) */
  --text:         #2B2A26;   /* primary text — warm near-black */
  --text-muted:   #6B6660;   /* secondary text — warm grey */
  --text-faint:   #9C968C;   /* faint label / timestamp */
  --highlight:    #F5D682;   /* highlighter-marker yellow — used behind Caveat callouts */
  --border:       #D9CFBE;   /* soft warm hairline */
  --border-strong:#A89B85;   /* emphatic panel divider */
  --font-display: 'Inter Tight', 'Inter', system-ui, sans-serif;     /* tight tracking; structural rhythm */
  --font-body:    'Inter Tight', 'Inter', system-ui, sans-serif;
  --font-hand:    'Caveat', 'Comic Sans MS', cursive;                /* annotation / callout / margin-note only */
  --font-mono:    'JetBrains Mono', 'Menlo', monospace;
  --radius:       10px;      /* 8–12px range — 10px is canonical midpoint */
  --radius-sm:    8px;
  --radius-lg:    12px;
  --shadow:       0 1px 2px rgba(60, 50, 35, 0.06), 0 2px 8px rgba(60, 50, 35, 0.04); /* light warm shadow */
  --shadow-card:  0 4px 16px rgba(60, 50, 35, 0.08);
  --spacing:      8px;
  --motion-duration: 200ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        primary: '#2B2A26',
        accent: '#C97B5A',
        bg: '#F5EFE3',
        surface: '#FAF6EC',
        'surface-elev': '#FFFFFF',
        text: '#2B2A26',
        'text-muted': '#6B6660',
        'text-faint': '#9C968C',
        highlight: '#F5D682',
        border: '#D9CFBE',
        'border-strong': '#A89B85',
      },
      fontFamily: {
        display: ['"Inter Tight"', 'Inter', 'system-ui', 'sans-serif'],
        body:    ['"Inter Tight"', 'Inter', 'system-ui', 'sans-serif'],
        hand:    ['Caveat', '"Comic Sans MS"', 'cursive'],
        mono:    ['"JetBrains Mono"', 'Menlo', 'monospace'],
      },
      borderRadius: { DEFAULT: '10px', sm: '8px', lg: '12px' },
      boxShadow: {
        DEFAULT: '0 1px 2px rgba(60,50,35,0.06), 0 2px 8px rgba(60,50,35,0.04)',
        card:    '0 4px 16px rgba(60,50,35,0.08)',
      },
      transitionDuration: { DEFAULT: '200ms' },
    }
  }
}
```

**Dark variant token override (rare for Crayon — beige is the soul; only use when product requires it):**
```css
[data-theme="dark"] {
  --bg:          #2B2724;
  --surface:     #34302C;
  --surface-elev:#3F3A35;
  --text:        #F5EFE3;
  --text-muted:  #B8B0A2;
  --text-faint:  #7A7368;
  --border:      #4A453F;
  --border-strong:#6B6660;
  --highlight:   #8B7438;
}
```

## "Breaks if" invariants

- Breaks if the background is cold (cool grey, pure white, blue-tinted) — the warm beige is the defining skin, not negotiable.
- Breaks if a monospace face replaces Inter Tight for body or display text (mono is allowed for code only, never for general prose).
- Breaks if the handwritten face (Caveat) is used for body text — Caveat is annotation-only: callouts, margin notes, sticky-label captions. Body in Caveat destroys legibility.
- Breaks if `border-radius` drops below 8px or exceeds 12px on panel chrome (the 8–12px band is the cozy-but-still-utilitarian range).
- Breaks if hard angular Brutalist borders (≥2px black, zero radius) appear — Crayon's borders are soft and warm.
- Breaks if more than one chromatic accent is introduced at full saturation — clay terracotta OR sage OR muted ochre, never two simultaneously.
- Breaks if cold-blue or high-saturation tech-bright accents appear — Crayon's palette is strictly earth-toned.
- Breaks if shadows become opaque or grey-cast — they must be warm-tinted (small brown/beige component) at low opacity.
- Breaks if information density exceeds Notion-comfort (long uninterrupted reading flow, occasional panel break) — high-density data-grid layouts contradict the "personality" promise.

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: no standalone upstream demo — tokens derived from `styles-A.md §Crayon (Warm Beige + Handwritten)` prose; upstream `claude-design-mode-main/README.md` describes but does not ship HTML.
Parity threshold: A-class justified (no renderable upstream demo)

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 117959 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-045 Warm Minimalism / Notion (also warm off-white, but no handwritten font and no macOS chrome — Crayon adds the personality layer on top of Notion's calm), S-037 Cream Editorial (also warm paper-stock, but all-serif and editorial-formal), S-020 Organic Earthy (also earth-toned, but more textural / grain-based), S-007 Claymorphism (also soft-rounded warm, but more skeuomorphic and less editorial).
- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: `reports/batch9-harvest/styles-A.md §Crayon (Warm Beige + Handwritten)` — upstream `claude-design-mode-main/README.md`, MIT.

## Attribution

Visual description, font pairing (Inter Tight + Caveat), and macOS window chrome metaphor ported from styles-A.md §Crayon. Token hex values are clean-room interpretations of the upstream prose ("warm beige base, soft earth tones, single muted accent, 8–12px radius, light warm shadows"). Upstream source repo `claude-design-mode-main` is MIT-licensed; this reference inherits MIT.
