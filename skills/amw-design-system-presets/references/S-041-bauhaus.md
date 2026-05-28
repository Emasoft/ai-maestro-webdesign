---
id: S-041
name: Bauhaus
aesthetic_position: classical-modernist geometric
source_attribution: https://github.com/design-forge-main/SKILL.md + references/discovery-framework.md (MIT, inferred); Google Stitch "Bauhaus" preset
license: MIT (inferred)
---

# S-041 — Bauhaus

**Filename:** `skills/amw-design-system-presets/references/S-041-bauhaus.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Bauhaus translates the Dessau workshop's doctrine — form follows function, geometry is the grammar — into a digital visual language. The palette is strictly primary: red, blue, yellow on a white or black ground, deployed as bold geometric blocks rather than gradients or tints. Typography pairs Cabinet Grotesk at heavy weights (display) with Satoshi (body), anchoring the "startup rebel" archetype favored by design-forge. Intended audience: creative agencies, architecture studios, design-tools marketing, and any brand that wants to telegraph disciplined avant-garde confidence.

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #FFFFFF;
  --color-surface:    #F5F5F5;
  --color-text:       #111111;
  --color-text-muted: #555555;
  --color-primary:    #E63946;   /* Bauhaus red */
  --color-accent:     #0D47A1;   /* Bauhaus blue */
  --color-yellow:     #FFC107;   /* Bauhaus yellow — decorative / highlight only */
  --color-border:     #111111;

  /* Typography */
  --font-display: 'Cabinet Grotesk', 'Satoshi', 'Arial Black', sans-serif;
  --font-body:    'Satoshi', 'Inter', 'Helvetica Neue', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  /* Geometry */
  --spacing:      8px;
  --radius:       0px;
  --border-width: 2px;

  /* Shadow — hard offset, no blur (Bauhaus rejects decoration) */
  --shadow:       none;

  /* Motion */
  --motion-duration: 200ms;
  --motion-easing:   linear;
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:         '#FFFFFF',
        surface:    '#F5F5F5',
        text:       '#111111',
        'text-muted': '#555555',
        primary:    '#E63946',
        accent:     '#0D47A1',
        yellow:     '#FFC107',
        border:     '#111111',
      },
      fontFamily: {
        display: ['"Cabinet Grotesk"', 'Satoshi', '"Arial Black"', 'sans-serif'],
        body:    ['Satoshi', 'Inter', '"Helvetica Neue"', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      borderRadius: { DEFAULT: '0px', none: '0px' },
      boxShadow:    { DEFAULT: 'none', none: 'none' },
      transitionDuration: { DEFAULT: '200ms' },
      transitionTimingFunction: { DEFAULT: 'linear' },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #111111;
  --color-surface:    #1E1E1E;
  --color-text:       #F5F5F5;
  --color-text-muted: #AAAAAA;
  --color-border:     #F5F5F5;
}
```

## "Breaks if" invariants

- breaks if `border-radius` is greater than 0px on any UI element
- breaks if gradients appear anywhere (backgrounds, buttons, or text)
- breaks if a fourth chromatic color is introduced beyond red, blue, and yellow
- breaks if body font is a serif or display-italic typeface
- breaks if `--shadow` uses blur-radius greater than 0 (hard offset only; preferably none)
- breaks if yellow (`#FFC107`) is used as a background for large text blocks (reserved for decoration/highlight only due to WCAG contrast risk on white)
- breaks if layout density drops to single-column soft-editorial mode — Bauhaus demands grid structure
- breaks if geometric shapes (circle, triangle, square) are replaced by organic blob shapes
- breaks if `--motion-easing` is changed to a spring or bounce curve — Bauhaus motion is functional, not expressive

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `atelier-main/examples/bauhaus-reference.html` (not yet ported); visual reference: Bauhaus Dessau Foundation web identity + design-forge Bauhaus Stitch preset screenshots.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 84124 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-001 Swiss (strict modernist, Helvetica-first), S-002 Brutalism (raw system fonts), S-003 Neo-Brutalism (single scream color)
- **Source:** `design-forge-main/SKILL.md` + `design-forge-main/references/discovery-framework.md` (MIT, inferred); Google Stitch "Bauhaus" preset documentation
- **Note:** Cabinet Grotesk and Satoshi are available on Google Fonts and Fontshare respectively; both are free for commercial use
