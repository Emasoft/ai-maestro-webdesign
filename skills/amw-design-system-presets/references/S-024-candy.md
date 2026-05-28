---
id: S-024
name: Candy / Playful Consumer App
aesthetic_position: playful-consumer-bold candy-neon
source_attribution: https://github.com/generate-design-md-main/references/examples/consumer-app-playful.design.md; https://github.com/web-designer-plugin-main (README.md — Candy App archetype); https://github.com/frontend-design-engineer-skill-main (visual-directions.md — Playful Gradient direction)
license: MIT (inferred)
---

# S-024 — Candy / Playful Consumer App

**Filename:** `skills/amw-design-system-presets/references/S-024-candy.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Candy is the sweetest end of the SaaS aesthetic spectrum: hot pink, candy purple, and lime green on near-white surfaces, with fully rounded pill buttons, colored drop-shadows that glow in the primary hue, and animated interactions — confetti bursts on success, scratch-to-reveal, bouncy spring curves on every hover. The palette blends pastel softness with neon punches so nothing ever reads as aggressive, only joyful. Poppins or Nunito at bold weights keeps the copy warm and approachable; emoji accents are welcome. Intended audience: consumer apps, mobile-first products, gamified education platforms, loyalty programs, and any B2C product aimed at a non-technical, joy-seeking user.

## Token block

```css
:root {
  /* Colors — hot pink / candy purple / lime hybrid palette */
  --color-bg:         #FAFAFA;
  --color-surface:    #FFFFFF;
  --color-text:       #1A0030;
  --color-text-muted: #6B5B8E;
  --color-primary:    #7C3AED;   /* candy purple */
  --color-secondary:  #FF71CE;   /* hot pink */
  --color-accent:     #A3E635;   /* lime green */
  --color-accent-2:   #38BDF8;   /* sky blue — for states / tags */
  --color-border:     #EDE9F4;

  /* Typography */
  --font-display: 'Poppins', 'Nunito', 'DM Rounded', sans-serif;
  --font-body:    'Nunito', 'Poppins', 'Inter', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  /* Geometry — pill or large radius everywhere */
  --spacing:      8px;
  --radius:       20px;          /* 16-24px card radius; buttons use 9999px pill */
  --radius-pill:  9999px;
  --border-width: 1px;

  /* Shadow — colored, tinted to primary or secondary hue */
  --shadow:       0 4px 20px rgba(124, 58, 237, 0.18);
  --shadow-pink:  0 4px 20px rgba(255, 113, 206, 0.22);

  /* Motion — bouncy spring (overshoots then settles) */
  --motion-duration: 350ms;
  --motion-easing:   cubic-bezier(0.34, 1.56, 0.64, 1);   /* spring overshoot */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:           '#FAFAFA',
        surface:      '#FFFFFF',
        text:         '#1A0030',
        'text-muted': '#6B5B8E',
        primary:      '#7C3AED',
        secondary:    '#FF71CE',
        accent:       '#A3E635',
        'accent-2':   '#38BDF8',
        border:       '#EDE9F4',
      },
      fontFamily: {
        display: ['Poppins', 'Nunito', '"DM Rounded"', 'sans-serif'],
        body:    ['Nunito', 'Poppins', 'Inter', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '20px',
        card: '20px',
        btn:  '9999px',
        sm:   '16px',
        lg:   '24px',
        pill: '9999px',
      },
      boxShadow: {
        DEFAULT: '0 4px 20px rgba(124,58,237,0.18)',
        pink:    '0 4px 20px rgba(255,113,206,0.22)',
        hover:   '0 8px 32px rgba(124,58,237,0.28)',
      },
      transitionDuration: { DEFAULT: '350ms' },
      transitionTimingFunction: {
        DEFAULT: 'cubic-bezier(0.34,1.56,0.64,1)',
        spring: 'cubic-bezier(0.34,1.56,0.64,1)',
      },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #110022;
  --color-surface:    #1E0040;
  --color-text:       #FAF0FF;
  --color-text-muted: #C4A8E8;
  --color-border:     #3D1F6B;
  --shadow:           0 4px 20px rgba(124, 58, 237, 0.35);
}
```

## "Breaks if" invariants

- breaks if background becomes dark — Candy is a light-mode-first style; dark surfaces kill the sweetness
- breaks if `border-radius` drops below `16px` — sharp corners are antithetical to the candy register
- breaks if colored shadow is replaced by neutral black drop-shadow
- breaks if `--motion-easing` is changed to `ease` or `linear` — the spring overshoot (`cubic-bezier(0.34,1.56,0.64,1)`) is the signature kinetic gesture
- breaks if palette reduces to a single hue — the hot pink + purple + lime triad is structural, not decorative
- breaks if Poppins / Nunito is replaced by a geometric condensed or serif face
- breaks if animated interactions (confetti, bounce, scratch-to-reveal) are absent from success states
- breaks if layout uses dense data tables or information-heavy grids — low-density card UI only

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: `generate-design-md-main/references/examples/consumer-app-playful.design.md` (full token spec); `web-designer-plugin-main/README.md` (Candy App archetype — confetti, scratch-to-reveal); `frontend-design-engineer-skill-main` — visual-directions.md (Playful Gradient direction).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 117936 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-023 Vibrant Friendly (softer palette, no spring overshoot), S-025 Playful Toy-Like (primary triad, heavy Nunito), S-007 Claymorphism (pastel + inner highlight depth)
- **Source:** `generate-design-md-main` — consumer-app-playful.design.md; `web-designer-plugin-main` — README.md; `frontend-design-engineer-skill-main` — visual-directions.md
- **Note:** Poppins and Nunito are available on Google Fonts (free for commercial use). The spring cubic-bezier `(0.34,1.56,0.64,1)` overshoots the target by ~56% then settles — this is the physics signature of the style. Do not soften it.
