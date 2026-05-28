---
id: S-001
name: Swiss / International Style
aesthetic_position: classical-modernist
source_attribution: "styles-B (Anchor 1); styles-A Swiss Minimal (frontend-design-engineer); blocked-A #14 (claude-skill-ui-ux-pro-max). MIT per source repos."
license: MIT
---

# S-001 — Swiss / International Style

## Identity

Swiss / International Style is the direct descendant of Müller-Brockmann's grid discipline: white or near-white field, pure black typography, one carefully chosen chromatic accent (red, orange, or YKB blue), zero radius, zero shadow. It was designed for maximum information density at maximum legibility. Reach for it when the brief demands institutional authority, SaaS precision, or design-studio credibility — anywhere that earnest clarity beats personality.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  --primary: #000000;       /* the brand-defining color */
  --accent: #E4002B;        /* Swiss Red — swap to #FF4F00 (Orange) or #002FA7 (YKB Blue) */
  --bg: #FFFFFF;            /* page background */
  --surface: #F7F7F8;       /* card/elevated surface */
  --text: #000000;          /* primary text */
  --text-muted: #666666;    /* secondary/muted text */
  --border: #000000;        /* hairline rule in accent or black */
  --font-display: 'Helvetica Neue', 'Akzidenz-Grotesk', Arial, sans-serif; /* display font family with fallbacks */
  --font-body: 'Helvetica Neue', Arial, sans-serif;    /* body font family with fallbacks */
  --font-mono: 'Helvetica Neue', monospace;            /* mono fallback */
  --radius: 0px;            /* corner radius — Swiss is always 0 */
  --shadow: none;           /* Swiss uses no decorative shadows */
  --spacing: 24px;          /* base spacing unit — aligns to 12-col grid gutter */
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        primary: '#000000',
        accent: '#E4002B',
        bg: '#FFFFFF',
        surface: '#F7F7F8',
        text: '#000000',
        'text-muted': '#666666',
        border: '#000000',
      },
      fontFamily: {
        display: ['"Helvetica Neue"', '"Akzidenz-Grotesk"', 'Arial', 'sans-serif'],
        body: ['"Helvetica Neue"', 'Arial', 'sans-serif'],
      },
      borderRadius: { DEFAULT: '0px' },
      boxShadow: { DEFAULT: 'none' },
    }
  }
}
```

## "Breaks if" invariants

- Breaks if `border-radius` exceeds 0px (Swiss is always sharp-cornered).
- Breaks if more than one chromatic accent colour is present on the page.
- Breaks if the accent is used on more than ~10% of visible surface area.
- Breaks if a serif display font replaces the grotesque — type must be a clean grotesque.
- Breaks if a warm-paper or cream background replaces the pure white / near-white field.
- Breaks if any decorative shadow (drop, inner, coloured) appears.
- Breaks if centered typography replaces left-aligned composition (Swiss is always left-justified or flush-left).
- Breaks if any gradient, texture, or grain overlay is introduced.

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: no standalone upstream demo — tokens direct-ported from `frontend-design-main/SKILL.md` Anchor 1, `frontend-design-engineer-skill-main/visual-directions.md` #2, `blocked-A #14`
Parity threshold: A-class justified (no renderable upstream demo)

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 61887 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: `reports/batch9-harvest/styles-B.md` §Swiss / International Style; `reports/batch9-harvest/styles-A.md` §Swiss Minimal; `reports/batch9-harvest/blocked-A.md` §14

## Attribution

Token values direct-ported from styles-B.md §Swiss / International Style, styles-A.md §Swiss Minimal (frontend-design-engineer-skill), and blocked-A.md #14 (claude-skill-ui-ux-pro-max). All source repos carry MIT license. Original distillation by the batch9 harvest team.
