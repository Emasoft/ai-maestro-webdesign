---
id: S-021
name: Pnalism / Two-Tone Minimal
aesthetic_position: classical-modernist two-tone
source_attribution: https://github.com/devPnal/design-system-is-all-you-need (pnalism.md — full parametric token system + density levels)
license: MIT (inferred)
---

# S-021 — Pnalism / Two-Tone Minimal

**Filename:** `skills/amw-design-system-presets/references/S-021-pnalism.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Pnalism is radical chromatic restraint reduced to a mathematical invariant: white background, pure black text, and exactly one accent color (plus its single tint). The name derives from "pnalism" — a design-system discipline that enforces maximum legibility through minimum palette. The system ships three density levels (compact, comfortable, spacious) with identical token blocks, differing only in spacing multipliers. Every border is 1px; every shadow is absent; radius is capped at 8px. Intended audience: developer tools, productivity apps, financial dashboards, and any product where clarity of information outranks brand expression.

## Token block

```css
:root {
  /* Colors — EXACTLY 2 chromatic values: --color-primary + --color-primary-light */
  --color-bg:            #FFFFFF;
  --color-surface:       #F8F8F8;
  --color-text:          #000000;
  --color-text-muted:    #555555;
  --color-primary:       #0070F3;   /* single accent — swap for brand color */
  --color-primary-light: #E8F4FF;   /* tint of primary — only permitted second chromatic value */
  --color-accent:        #0070F3;   /* alias — same as primary */
  --color-border:        #000000;

  /* Typography */
  --font-display: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --font-body:    'Inter', 'Helvetica Neue', Arial, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  /* Geometry */
  --spacing:      8px;
  --radius:       8px;           /* hard cap — do not exceed */
  --border-width: 1px;           /* 1px borders ONLY — never 2px or thicker */

  /* Shadow — none is the invariant */
  --shadow:       none;

  /* Motion — functional only */
  --motion-duration: 150ms;
  --motion-easing:   ease;
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:             '#FFFFFF',
        surface:        '#F8F8F8',
        text:           '#000000',
        'text-muted':   '#555555',
        primary:        '#0070F3',
        'primary-light':'#E8F4FF',
        accent:         '#0070F3',
        border:         '#000000',
      },
      fontFamily: {
        display: ['Inter', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        body:    ['Inter', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      borderRadius: { DEFAULT: '8px' },
      borderWidth:  { DEFAULT: '1px' },
      boxShadow:    { DEFAULT: 'none', none: 'none' },
      transitionDuration: { DEFAULT: '150ms' },
      transitionTimingFunction: { DEFAULT: 'ease' },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:            #000000;
  --color-surface:       #111111;
  --color-text:          #FFFFFF;
  --color-text-muted:    #AAAAAA;
  --color-border:        #FFFFFF;
  --color-primary-light: #0F1F30;
}
```

**Density level multipliers (compact / comfortable / spacious):**
```css
/* compact */   --spacing: 6px;
/* comfortable */ --spacing: 8px;  /* default */
/* spacious */  --spacing: 12px;
```

## "Breaks if" invariants

- breaks if a third chromatic color is introduced beyond `--color-primary` and `--color-primary-light`
- breaks if any `box-shadow` value other than `none` is used anywhere in the UI
- breaks if `border-width` exceeds `1px` on any element
- breaks if `border-radius` exceeds `8px` on any element
- breaks if gradients appear on backgrounds, buttons, or text
- breaks if a second accent hue is added (e.g. a warning orange that is not a tint of the primary)
- breaks if `--motion-duration` exceeds 150ms — pnalism is functional, never expressive
- breaks if typographic hierarchy relies on color variety rather than weight/size contrast

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `design-system-is-all-you-need-main/pnalism.md` (parametric token system reference).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 95158 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-022 Minimal Pure (monochrome, zero radius), S-001 Swiss (1 accent + strict grid)
- **Source:** `design-system-is-all-you-need-main` — pnalism.md; full parametric token system with density levels
- **Note:** Inter is available on Google Fonts (free for commercial use). Primary accent `#0070F3` is Vercel blue — swap for any single brand color to brand-adapt the preset.
