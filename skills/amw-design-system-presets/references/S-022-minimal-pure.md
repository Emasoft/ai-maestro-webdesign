---
id: S-022
name: Minimal Pure / Ultra-Minimal Precision
aesthetic_position: classical-modernist monochrome
source_attribution: https://github.com/DonkeyKing01/tasteful-ui-skill (catalog.md — Monochrome category); batch9 harvest corpus `frontend-design` (SKILL.md — Industrial + Swiss zero-decoration invariants; no public upstream URL recorded)
license: MIT (inferred)
---

# S-022 — Minimal Pure / Ultra-Minimal Precision

**Filename:** `skills/amw-design-system-presets/references/S-022-minimal-pure.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Minimal Pure is the absolute reduction: pure black on pure white, one typeface, weight as the only dimension of variation. No color — not even a muted grey accent. Typography is the decoration: display sizes run 80–120px, headlines carry all the visual energy, and body copy is deliberately small and restrained. Zero radius, zero shadow, zero illustration. The style lives at the intersection of Swiss rationalism and stark monochrome futurism. Intended audience: architecture studios, luxury typographic brands, editorial platforms, and developer-focused tools that want to telegraph technical seriousness without any color politics.

## Token block

```css
:root {
  /* Colors — pure black and white ONLY; grey for secondary hierarchy */
  --color-bg:         #FFFFFF;
  --color-surface:    #FAFAFA;
  --color-text:       #000000;
  --color-text-muted: #666666;
  --color-primary:    #000000;   /* black is the only "primary" */
  --color-accent:     #000000;   /* no chromatic accent permitted */
  --color-border:     #000000;

  /* Typography — single family; weight is the only axis */
  --font-display: 'Helvetica Neue', 'Inter', Arial, sans-serif;
  --font-body:    'Helvetica Neue', 'Inter', Arial, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  /* Display scale — 80-120px mandatory for hero typography */
  --font-display-size: clamp(5rem, 12vw, 7.5rem);  /* 80-120px */
  --font-body-size:    clamp(1rem, 1.125vw, 1.125rem); /* 16-18px */

  /* Geometry */
  --spacing:      8px;
  --radius:       0px;           /* zero radius is the invariant */
  --border-width: 1px;

  /* Shadow — none */
  --shadow:       none;

  /* Motion — typographic entrance only; no decorative motion */
  --motion-duration: 200ms;
  --motion-easing:   ease;
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:           '#FFFFFF',
        surface:      '#FAFAFA',
        text:         '#000000',
        'text-muted': '#666666',
        primary:      '#000000',
        accent:       '#000000',
        border:       '#000000',
      },
      fontFamily: {
        display: ['"Helvetica Neue"', 'Inter', 'Arial', 'sans-serif'],
        body:    ['"Helvetica Neue"', 'Inter', 'Arial', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      fontSize: {
        'display': ['clamp(5rem, 12vw, 7.5rem)', { lineHeight: '1.0' }],
        'body':    ['clamp(1rem, 1.125vw, 1.125rem)', { lineHeight: '1.6' }],
      },
      borderRadius: { DEFAULT: '0px', none: '0px' },
      boxShadow:    { DEFAULT: 'none', none: 'none' },
      transitionDuration: { DEFAULT: '200ms' },
      transitionTimingFunction: { DEFAULT: 'ease' },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #000000;
  --color-surface:    #111111;
  --color-text:       #FFFFFF;
  --color-text-muted: #999999;
  --color-primary:    #FFFFFF;
  --color-accent:     #FFFFFF;
  --color-border:     #FFFFFF;
}
```

## "Breaks if" invariants

- breaks if any chromatic color (hue) is introduced — grey scale only; `#000` and `#fff` are the only anchor values
- breaks if `border-radius` is greater than `0px` on any element
- breaks if any `box-shadow` value other than `none` is applied
- breaks if display typography drops below 80px (5rem) — the large scale is load-bearing for the aesthetic
- breaks if a second typeface family is introduced — single-family weight variation only
- breaks if decorative illustrations, icons with color fills, or gradient overlays appear
- breaks if body copy exceeds 18px — restrained body size is part of the contrast against the oversized display
- breaks if motion is used for anything other than typographic entrance (fades, slides on headings only)

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `tasteful-ui-skill-master/catalog.md` (Monochrome category); `frontend-design-main/SKILL.md` (Swiss/Industrial zero-decoration invariants); xAI Grok reference: "stark monochrome futuristic minimalism".

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 91134 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-021 Pnalism (2 chromatic values + 8px radius), S-001 Swiss (Helvetica-first, 1 accent permitted), S-013 Industrial (mono font + signal color)
- **Source:** `tasteful-ui-skill-master` — catalog.md; `frontend-design-main` — SKILL.md
- **Note:** The weight-only variation rule means the font stack must include a web-safe sans-serif fallback; `Helvetica Neue` is preferred over `Arial` for its tighter metrics. `Inter` is acceptable as the primary face for digital rendering.
