---
id: S-009
name: Aurora UI / Aurora Maximalism
aesthetic_position: dark-cinematic-cyber
source_attribution: blocked-A #12; styles-B "Aurora Maximalism"; frontend-design Anchor 4; 21st-frontend-design-main/SKILL.md
license: MIT
---

# S-009 — Aurora UI / Aurora Maximalism

**Filename:** `references/S-009-aurora.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Aurora UI is a dark-first aesthetic built on atmospheric gradient light rather than flat surfaces. The background is near-black (`#09090b`); the brand identity is a violet-to-pink-to-cyan gradient treated as a single design element — appearing as a radial wash behind hero content, as gradient text on 1-2 key words, and as glowing gradient borders on cards and containers. Type is enormous (15-25vw display), tracked tight, and set in Inter Variable or a grotesque equivalent. Glow boxes replace drop-shadows entirely — depth comes from luminance, not offset. Spring physics drive all motion. Intended for AI products, SaaS landing pages, and premium consumer-tech.

## Token block

```css
/* S-009 Aurora UI / Aurora Maximalism — complete token block */
:root {
  /* Colors */
  --color-bg:          #09090b;   /* near-black void */
  --color-surface:     #18181b;   /* raised panel */
  --color-surface-hi:  #27272a;   /* elevated surface */
  --color-text:        #fafafa;   /* bright white */
  --color-text-muted:  #a1a1aa;   /* zinc-400 */
  --color-primary:     #7c3aed;   /* violet-700 */
  --color-accent:      #06b6d4;   /* cyan-500 */
  --color-accent-2:    #ec4899;   /* pink-500 */
  --color-border:      rgba(139,92,246,0.15);   /* violet ghost border */

  /* Aurora gradient — the core brand expression */
  --aurora-gradient:   linear-gradient(135deg, #7c3aed 0%, #ec4899 50%, #06b6d4 100%);
  --aurora-wash:       radial-gradient(ellipse at 50% 0%, rgba(109,40,217,0.30), transparent 70%);
  --aurora-wash-2:     radial-gradient(ellipse at 80% 50%, rgba(236,72,153,0.15), transparent 60%);

  /* Glow system (elevation via luminance, not drop-shadow) */
  --glow-primary:      0 0 40px rgba(124,58,237,0.40);
  --glow-accent:       0 0 30px rgba(6,182,212,0.30);
  --glow-pink:         0 0 30px rgba(236,72,153,0.25);
  --glow-card:         0 0 60px rgba(124,58,237,0.15);

  /* Typography */
  --font-display:      'Inter Variable', 'Inter', system-ui, sans-serif;
  --font-body:         'Inter', system-ui, sans-serif;
  --font-mono:         'JetBrains Mono', 'Fira Code', monospace;
  --font-display-size: clamp(3rem, 15vw, 10rem);
  --tracking-display:  -0.04em;

  /* Spacing & shape */
  --spacing:           8px;
  --radius:            12px;   /* card / panel radius */
  --radius-button:     8px;

  /* Shadow — glow only, no offset */
  --shadow:            0 0 40px rgba(124,58,237,0.40);

  /* Motion — spring physics */
  --motion-duration:   500ms;
  --motion-easing:     cubic-bezier(0.34, 1.56, 0.64, 1);   /* spring */

  /* Gradient border trick (requires background-clip) */
  --gradient-border:   linear-gradient(135deg, rgba(124,58,237,0.6), rgba(236,72,153,0.4), rgba(6,182,212,0.6));
  --border-width:      1px;
}
```

```js
// Tailwind theme extension — S-009 Aurora UI
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'aurora-bg':       '#09090b',
        'aurora-surface':  '#18181b',
        'aurora-surf-hi':  '#27272a',
        'aurora-text':     '#fafafa',
        'aurora-muted':    '#a1a1aa',
        'aurora-primary':  '#7c3aed',
        'aurora-cyan':     '#06b6d4',
        'aurora-pink':     '#ec4899',
      },
      backgroundImage: {
        'aurora-grad':    'linear-gradient(135deg, #7c3aed 0%, #ec4899 50%, #06b6d4 100%)',
        'aurora-wash':    'radial-gradient(ellipse at 50% 0%, rgba(109,40,217,0.30), transparent 70%)',
      },
      boxShadow: {
        'aurora':         '0 0 40px rgba(124,58,237,0.40)',
        'aurora-card':    '0 0 60px rgba(124,58,237,0.15)',
        'aurora-cyan':    '0 0 30px rgba(6,182,212,0.30)',
      },
      fontFamily: {
        display: ['Inter Variable', 'Inter', 'system-ui', 'sans-serif'],
        body:    ['Inter', 'system-ui', 'sans-serif'],
        mono:    ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      borderRadius: {
        aurora: '12px',
      },
      transitionTimingFunction: {
        aurora: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
      transitionDuration: {
        aurora: '500ms',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if the background is replaced with a flat color, warm surface, or light-mode canvas — near-black void is non-negotiable
- breaks if the aurora gradient (violet → pink → cyan) is reduced to a single flat brand color — the gradient IS the brand identity
- breaks if depth is achieved via `box-shadow` with an x/y offset instead of centered radial glow — elevation via luminance only
- breaks if display type drops below 3rem (clamp floor) — huge oversized type is required for the aesthetic to read as Aurora, not just Dark-mode generic
- breaks if warm humanist serif or grotesque with visible stroke contrast is used — Inter Variable or equivalent neutral grotesque only
- breaks if spring-physics easing is replaced with standard ease-in-out — motion must feel alive and bouncy, not mechanical
- breaks if a flat background is placed behind hero content instead of the aurora wash gradient — the atmospheric radial wash is mandatory in the hero section
- breaks if more than three gradient stops are used simultaneously — violet/pink/cyan is the fixed triad; adding green, orange, or red breaks the aurora signature

## Canonical render-test pointer

Render-test: inject tokens into `references/_test-skeleton.html` (substitute `{{BG}}=#09090b`, `{{SURFACE}}=#18181b`, `{{TEXT}}=#fafafa`, `{{TEXT_MUTED}}=#a1a1aa`, `{{PRIMARY}}=#7c3aed`, `{{ACCENT}}=#06b6d4`, `{{BORDER}}=rgba(139,92,246,0.15)`, `{{FONT_DISPLAY}}='Inter Variable','Inter',system-ui,sans-serif`, `{{FONT_BODY}}='Inter',sans-serif`, `{{FONT_MONO}}='JetBrains Mono',monospace`, `{{RADIUS}}=12px`, `{{SHADOW}}=0 0 40px rgba(124,58,237,0.40)`, `{{SPACING}}=8px`). Apply `--aurora-wash` as `body::before` absolute background layer behind hero.

Upstream reference: `frontend-design-main/SKILL.md` Anchor 4 "Aurora Maximalism"; `21st-frontend-design-main/SKILL.md`; `styles-B.md` "Aurora Maximalism" section; `blocked-A.md` section 12.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 139020 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Sibling styles: S-010 Cyberpunk (neon-hard-cyber vs. atmospheric-gradient-soft), S-010b Neon (2-color glow vs. 3-color aurora gradient), S-035 21st.dev/Aceternity (bento/shimmer vs. full-bleed gradient brand)
- Source: `blocked-A.md` section 12; `styles-B.md` "Aurora Maximalism"; `frontend-design-main/SKILL.md` Anchor 4.

## Attribution

Direct port from `frontend-design-main` (MIT license) and `21st-frontend-design-main` (MIT license). Token values sourced from `styles-B.md` "Aurora Maximalism" in `reports/batch9-harvest/`. Catalog summary and "breaks-if" invariants are original content authored for this plugin. License: MIT.
