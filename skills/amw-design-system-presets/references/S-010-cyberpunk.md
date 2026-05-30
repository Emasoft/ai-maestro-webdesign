---
id: S-010
name: Cyberpunk / Dark Neo-Noir
aesthetic_position: dark-cinematic-cyber
source_attribution: blocked-A #16 (claude-skill-ui-ux-pro-max styles.csv "Dark Neo-Noir/Cyberpunk"); styles-B "Neon / Glow UI"; blocked-B "Cyberpunk seed"
license: MIT
---

# S-010 — Cyberpunk / Dark Neo-Noir

**Filename:** `references/S-010-cyberpunk.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Cyberpunk / Dark Neo-Noir is a dystopian aesthetic rooted in 1980s science-fiction visual culture: rain-slicked void-black backgrounds, neon cyan and magenta phosphorescence, angular zero-radius geometry, all-caps data-dense labels, and multi-layer neon glow (`0 0 5px / 20px / 40px`) that simulates light bleeding through darkness. Orbitron and Rajdhani handle display and body respectively. Optional glitch animations, CRT scanline overlays, and clipping-path diagonal cuts amplify the high-tech-low-life aesthetic. Intended for gaming sites, cyberpunk genre products, entertainment tech, and any product where menace and energy are brand signals.

## Token block

```css
/* S-010 Cyberpunk / Dark Neo-Noir — complete token block */
:root {
  /* Colors */
  --color-bg:           #0a0a12;   /* void-black with a blue cast */
  --color-surface:      #12121e;   /* raised panel */
  --color-surface-hi:   #1a1a2e;   /* elevated surface */
  --color-text:         #e0e0ff;   /* cold white with blue tint */
  --color-text-muted:   #7878aa;   /* muted blue-purple */
  --color-primary:      #00FFFF;   /* neon cyan */
  --color-accent:       #FF00FF;   /* neon magenta */
  --color-accent-2:     #00FF41;   /* toxic green (tertiary) */
  --color-border:       rgba(0,255,255,0.25);   /* cyan ghost border */

  /* Neon glow system — triple-layer */
  --glow-cyan:    0 0 5px #00FFFF, 0 0 20px #00FFFF, 0 0 40px #00FFFF;
  --glow-magenta: 0 0 5px #FF00FF, 0 0 20px #FF00FF, 0 0 40px #FF00FF;
  --glow-green:   0 0 5px #00FF41, 0 0 20px #00FF41, 0 0 40px #00FF41;
  --glow-current: 0 0 5px currentColor, 0 0 20px currentColor, 0 0 40px currentColor;

  /* Scanline overlay (apply as body::after or section::after) */
  --scanlines: repeating-linear-gradient(
    to bottom,
    transparent 0px,
    transparent 2px,
    rgba(0,0,0,0.15) 2px,
    rgba(0,0,0,0.15) 4px
  );

  /* Typography — display: Orbitron; body: Rajdhani */
  --font-display: 'Orbitron', 'Rajdhani', monospace;
  --font-body:    'Rajdhani', 'Share Tech Mono', monospace;
  --font-mono:    'Share Tech Mono', 'Fira Code', 'Courier New', monospace;
  --tracking-ui:  0.10em;   /* all-caps spacing */
  --text-transform-ui: uppercase;

  /* Spacing & shape */
  --spacing:    8px;
  --radius:     0px;   /* angular zero-radius — no softness */

  /* Border */
  --border-width: 1px;
  --border-style: solid;

  /* Shadow — neon glow (primary color, cyan) */
  --shadow: 0 0 5px #00FFFF, 0 0 20px #00FFFF, 0 0 40px #00FFFF;

  /* Motion — glitch-fast */
  --motion-duration: 150ms;
  --motion-easing:   steps(4, end);   /* glitch step-timing */
  --motion-smooth:   cubic-bezier(0.4, 0, 0.2, 1);   /* for non-glitch transitions */
}
```

```js
// Tailwind theme extension — S-010 Cyberpunk
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'cp-bg':        '#0a0a12',
        'cp-surface':   '#12121e',
        'cp-surf-hi':   '#1a1a2e',
        'cp-text':      '#e0e0ff',
        'cp-muted':     '#7878aa',
        'cp-cyan':      '#00FFFF',
        'cp-magenta':   '#FF00FF',
        'cp-green':     '#00FF41',
      },
      fontFamily: {
        display: ['Orbitron', 'Rajdhani', 'monospace'],
        body:    ['Rajdhani', 'Share Tech Mono', 'monospace'],
        mono:    ['Share Tech Mono', 'Fira Code', 'Courier New', 'monospace'],
      },
      borderRadius: {
        cp: '0px',
      },
      boxShadow: {
        'cp-cyan':    '0 0 5px #00FFFF, 0 0 20px #00FFFF, 0 0 40px #00FFFF',
        'cp-magenta': '0 0 5px #FF00FF, 0 0 20px #FF00FF, 0 0 40px #FF00FF',
        'cp-green':   '0 0 5px #00FF41, 0 0 20px #00FF41, 0 0 40px #00FF41',
      },
      letterSpacing: {
        'cp-ui': '0.10em',
      },
      transitionTimingFunction: {
        'cp-glitch': 'steps(4, end)',
      },
      transitionDuration: {
        cp: '150ms',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if `border-radius` exceeds 2px — cyberpunk geometry is strictly angular; rounded forms exit the aesthetic
- breaks if background uses a warm hue or gray value above `#1a1a2e` lightness — the deep void-black with blue cast is non-negotiable
- breaks if neon glow is reduced to a single `box-shadow` layer — the triple-layer (5px / 20px / 40px spread) defines the neon bleed; a single layer reads as plain glow, not neon phosphorescence
- breaks if display font changes to a humanist sans, serif, or rounded typeface — Orbitron (display) or Rajdhani (body) only; the condensed technical letterform is the style's typographic voice
- breaks if UI label text is set in sentence-case or mixed case — all-caps is required for UI chrome; body prose may be normal case
- breaks if warm colors (orange, red, gold, amber) are used as accent — the palette is cold-neon only: cyan, magenta, and toxic green; no warm accents
- breaks if motion uses ease-in-out instead of step or fast easing — glitch transitions require step-timing; smooth motion breaks the digital-artifact aesthetic
- breaks if the scanline overlay is removed on dark sections — the repeating scanline is part of the CRT materiality; removing it collapses into generic dark-mode

## Canonical render-test pointer

Render-test: inject tokens into `references/_test-skeleton.html` (substitute `{{BG}}=#0a0a12`, `{{SURFACE}}=#12121e`, `{{TEXT}}=#e0e0ff`, `{{TEXT_MUTED}}=#7878aa`, `{{PRIMARY}}=#00FFFF`, `{{ACCENT}}=#FF00FF`, `{{BORDER}}=rgba(0,255,255,0.25)`, `{{FONT_DISPLAY}}='Orbitron','Rajdhani',monospace`, `{{FONT_BODY}}='Rajdhani',monospace`, `{{FONT_MONO}}='Share Tech Mono',monospace`, `{{RADIUS}}=0px`, `{{SHADOW}}=0 0 5px #00FFFF,0 0 20px #00FFFF,0 0 40px #00FFFF`, `{{SPACING}}=8px`). Apply `--scanlines` as `body::after` fixed overlay at 0.4 opacity.

Upstream reference: `claude-skill-ui-ux-pro-max-main/data/styles.csv` entry "Dark Neo-Noir/Cyberpunk" (blocked-A #16); `styles-B.md` "Neon / Glow UI" section; `blocked-B.md` "Cyberpunk seed".

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 110491 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Sibling styles: S-009 Aurora (atmospheric gradient vs. neon point-sources), S-010b Neon (2-color glow subset, no scanlines/angular), S-011 Synthwave (CRT aesthetic with warm retro palette vs. cold cyberpunk neon)
- Source: `reports/batch9-harvest/blocked-A.md` section 16 "Dark Neo-Noir/Cyberpunk"; `reports/batch9-harvest/styles-B.md` "Neon / Glow UI"; `reports/batch9-harvest/blocked-B.md` "Cyberpunk seed".

## Attribution

Direct port from `claude-skill-ui-ux-pro-max-main` (MIT license) styles.csv "Dark Neo-Noir/Cyberpunk" entry. Background `#0a0a12` and neon triple-glow system sourced from `styles-B.md` "Neon / Glow UI" and `blocked-A.md` section 16. Catalog summary and "breaks-if" invariants are original content authored for this plugin. License: MIT.
