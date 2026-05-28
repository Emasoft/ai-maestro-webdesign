---
id: S-011
name: Retro-Futuristic / Synthwave
aesthetic_position: dark-cinematic-cyber
source_attribution: https://github.com/Emasoft/ai-maestro-webdesign (batch9 harvest, styles-B "Retro-Futuristic"; styles-A "Retro-Futuristic"; frontend-design Anchor 6)
license: original summary; upstream token values MIT where applicable
---

## Identity

Synthwave evokes the neon-drenched 1980s science-fiction imaginary as seen through a retrocomputing lens: deep-space backgrounds saturated with violet and indigo, phosphor-glow text rendered in bitmap or display-weight sans-serif (VT323, Orbitron), and the horizontal scanline texture of a CRT monitor simulated via `repeating-linear-gradient`. The palette alternates between two canonical variants — **neon** (magenta `#FF00FF` + cyan `#00FFFF`) and **phosphor** (amber `#FFB300` + warm green `#39FF14`) — against a near-black `#0D0221` deep space background. Neon glow box-shadows on every interactive surface give the UI a volumetric quality without requiring actual 3-D. Designed for creative tools, music apps, gaming dashboards, and any context where nostalgic futurism is the intended emotional register.

## Token block

```css
/* S-011 Retro-Futuristic / Synthwave — token block (neon variant) */
:root {
  /* Colors */
  --color-bg:           #0D0221;   /* deep space */
  --color-surface:      #150535;   /* elevated panel, slightly lighter */
  --color-text:         #E8D5FF;   /* soft lavender white */
  --color-text-muted:   #9966CC;   /* mid-purple muted */
  --color-primary:      #FF00FF;   /* magenta neon */
  --color-accent:       #00FFFF;   /* cyan neon */
  --color-border:       #4B0082;   /* indigo hairline */

  /* Typography */
  --font-display: 'Orbitron', 'VT323', 'Courier New', monospace;
  --font-body:    'VT323', 'Share Tech Mono', 'Courier New', monospace;
  --font-mono:    'VT323', 'Fira Code', 'Courier New', monospace;

  /* Layout */
  --spacing:       8px;
  --radius:        0px;

  /* Shadow / Glow */
  --shadow:        0 0 8px #FF00FF, 0 0 24px rgba(255,0,255,0.45), 0 0 48px rgba(255,0,255,0.2);
  --glow-primary:  0 0 6px #FF00FF, 0 0 20px #FF00FF, 0 0 40px rgba(255,0,255,0.4);
  --glow-accent:   0 0 6px #00FFFF, 0 0 20px #00FFFF, 0 0 40px rgba(0,255,255,0.4);

  /* Motion */
  --motion-duration: 200ms;
  --motion-easing:   linear;

  /* CRT scanline overlay — apply as background on a pseudo-element */
  --gradient-scanlines: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.18) 2px,
    rgba(0,0,0,0.18) 4px
  );

  /* Phosphor variant (swap these to switch palette) */
  --color-primary-phosphor: #FFB300; /* amber */
  --color-accent-phosphor:  #39FF14; /* toxic green */
}
```

```ts
// Tailwind theme extension — S-011 Synthwave
export default {
  theme: {
    extend: {
      colors: {
        synthwave: {
          bg:          '#0D0221',
          surface:     '#150535',
          text:        '#E8D5FF',
          muted:       '#9966CC',
          primary:     '#FF00FF',
          accent:      '#00FFFF',
          border:      '#4B0082',
          amber:       '#FFB300',   // phosphor alt
          green:       '#39FF14',   // phosphor alt
        },
      },
      fontFamily: {
        display: ['Orbitron', 'VT323', 'Courier New', 'monospace'],
        body:    ['VT323', 'Share Tech Mono', 'Courier New', 'monospace'],
        mono:    ['VT323', 'Fira Code', 'Courier New', 'monospace'],
      },
      borderRadius: {
        synthwave: '0px',
      },
      boxShadow: {
        'sw-primary': '0 0 8px #FF00FF, 0 0 24px rgba(255,0,255,0.45), 0 0 48px rgba(255,0,255,0.2)',
        'sw-accent':  '0 0 8px #00FFFF, 0 0 24px rgba(0,255,255,0.45), 0 0 48px rgba(0,255,255,0.2)',
      },
      transitionDuration: {
        synthwave: '200ms',
      },
    },
  },
};
```

## "Breaks if" invariants

- Breaks if `border-radius` is set above `0px` — the style is hard-edged by definition; rounded corners destroy the CRT/vector-terminal aesthetic.
- Breaks if the scanline `repeating-linear-gradient` overlay is removed — the CRT texture is load-bearing visual evidence of the retro-futurist concept.
- Breaks if a warm neutral (beige, cream, tan) replaces the deep-space `#0D0221` background — Synthwave lives in the dark; light backgrounds invert the emotional register entirely.
- Breaks if a third chromatic family is introduced (e.g. adding orange alongside magenta + cyan) — the dual-neon palette tension is the visual signature; a third color dissipates it into generic colorfulness.
- Breaks if body text is set in a proportional serif or humanist sans — the style demands bitmap or futuristic monospace fonts for all text roles.
- Breaks if box-shadows are replaced with hard offset shadows (`4px 4px 0 #000` style) — the multi-layer outward glow is what distinguishes Synthwave from Brutalism-in-dark-mode.
- Breaks if `--motion-duration` is set above `400ms` — transitions should feel like CRT phosphor decay, not the slow fade of editorial design.
- Breaks if the phosphor and neon variants are mixed in the same page — choose one palette variant per artifact; mixing defeats the internal color logic.

## Canonical render-test pointer

Render-test: inject tokens into `skills/amw-design-system-presets/references/_test-skeleton.html` with the neon variant token block above. Parity source: styles-B "Retro-Futuristic" + frontend-design Anchor 6 (batch9 harvest).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 99539 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- S-010 Cyberpunk / Dark Neo-Noir — shares deep-space background and neon glow architecture; Cyberpunk adds glitch effects and all-caps; Synthwave stays analog-retro.
- S-012 Retro Terminal / Green-on-Black — shares the monospace-only font contract; Terminal uses a single phosphor color on a near-black background rather than the dual-neon palette.
- S-010b Neon / Glow UI — shares the multi-layer glow shadow system; Neon is a contemporary dark UI; Synthwave is specifically 1980s retrocomputing aesthetic.

## Attribution

Tokens derived from batch9 harvest: `styles-B` "Retro-Futuristic", `styles-A` "Retro-Futuristic", `frontend-design` Anchor 6. Original synthesis for this plugin. Upstream open-source values (palette choices) are in the public domain as color specifications.
