---
id: S-005
name: Neumorphism / Soft UI
aesthetic_position: glass-soft-skeuomorphic
source_attribution: "styles-B §Neumorphism/Soft UI (DSIAYN, claude-remix); blocked-A #13 (claude-skill-ui-ux-pro-max); styles-A §Neumorphism Stitch Preset (design-forge MIT). MIT per source repos."
license: MIT
---

# S-005 — Neumorphism / Soft UI

## Identity

Neumorphism creates the illusion of elements extruded from or pressed into the background by exploiting a single rule: the same hue, dramatically lighter on one side, dramatically darker on the other. The dual shadow is the entire design — it replaces borders, elevation, and colour contrast simultaneously. The style is physically satisfying but poses a hard WCAG-AA contrast challenge; body text must be tested carefully. Reach for it when the brief demands a tactile, premium-product feel, particularly for audio/music apps, smart-home interfaces, or lifestyle apps where the low-contrast softness is a deliberate brand signal.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  --primary: #a0aabc;              /* the brand-defining color — muted cool-grey primary */
  --accent: #6b7a99;               /* secondary accent — slightly darker tonal shift */
  --bg: #e0e5ec;                   /* page background — 88-92% L single desaturated base */
  --surface: #e0e5ec;              /* card/elevated surface — identical to bg (elements emerge from it) */
  --text: #3a4660;                 /* primary text — darkened variant of bg hue for AA contrast */
  --text-muted: #6b7a99;           /* secondary/muted text */
  --border: transparent;           /* border color — no visible border; shadow IS the border */
  --font-display: 'General Sans', 'Inter', system-ui, sans-serif; /* display font family with fallbacks */
  --font-body: 'General Sans', 'Inter', system-ui, sans-serif;    /* body font family with fallbacks */
  --font-mono: 'Fira Code', 'Courier New', monospace;             /* mono */
  --radius: 16px;                  /* corner radius — 12-16px for convex/concave feel */
  --shadow: 6px 6px 12px #b8bec7, -6px -6px 12px #ffffff; /* dual outset shadow (convex) */
  --spacing: 24px;                 /* base spacing unit */
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        primary: '#a0aabc',
        accent: '#6b7a99',
        bg: '#e0e5ec',
        surface: '#e0e5ec',
        text: '#3a4660',
        'text-muted': '#6b7a99',
        border: 'transparent',
      },
      fontFamily: {
        display: ['"General Sans"', 'Inter', 'system-ui', 'sans-serif'],
        body: ['"General Sans"', 'Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: { DEFAULT: '16px' },
      boxShadow: {
        DEFAULT: '6px 6px 12px #b8bec7, -6px -6px 12px #ffffff',
        concave: 'inset 6px 6px 12px #b8bec7, inset -6px -6px 12px #ffffff',
      },
    }
  }
}
```

## "Breaks if" invariants

- Breaks if coloured shadows are used — both shadow hues must be achromatic (lighter and darker variants of the same base hue only).
- Breaks if only a single shadow is used — the dual-shadow (bright top-left + dark bottom-right) is the defining structural element.
- Breaks if the background is dark — the style requires 88-92% lightness; dark backgrounds collapse the illusion entirely.
- Breaks if a strong chromatic accent colour is introduced — any vivid colour destroys the monochromatic surface language.
- Breaks if visible border lines appear alongside the shadow (shadow IS the border; borders are redundant and style-breaking).
- Breaks if `border-radius` drops below 8px — sharp corners conflict with the soft-extrusion metaphor.
- Breaks if body text contrast falls below WCAG AA 4.5:1 — the low-contrast palette makes this a live risk that must be verified.

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: no standalone upstream demo — tokens direct-ported from `design-system-is-all-you-need-main/neumorphism.md`, `blocked-A #13`, `design-forge-main/references/discovery-framework.md`
Parity threshold: A-class justified (no renderable upstream demo)

## Render-test verdict

JOD: pending

## Cross-references

- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: `reports/batch9-harvest/styles-B.md` §Neumorphism / Soft UI; `reports/batch9-harvest/blocked-A.md` §13; `reports/batch9-harvest/styles-A.md` §Neumorphism / Soft UI (Stitch Preset)

## Attribution

Token values direct-ported from styles-B.md §Neumorphism / Soft UI (design-system-is-all-you-need, claude-remix), blocked-A.md #13 (claude-skill-ui-ux-pro-max), and styles-A.md §Neumorphism Stitch Preset (design-forge). All source repos carry MIT license. Original distillation by the batch9 harvest team.
