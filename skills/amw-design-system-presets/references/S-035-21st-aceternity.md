---
id: S-035
name: 21st.dev / Aceternity
aesthetic_position: dark-cinematic-cyber premium-saas bento-landing
source_attribution: https://github.com/21st-frontend-design (MIT) + https://ui.aceternity.com
license: MIT (21st-frontend-design); Aceternity UI components MIT
---

# S-035 — 21st.dev / Aceternity

## Identity

21st.dev / Aceternity is the dominant visual language of premium-tier 2024–2025 SaaS landing pages: near-black zinc (`bg-zinc-950`) ground, one or two soft radial colour washes (violet, emerald, or sky) fading into the background, ONE vivid accent, gradient-border cards using `border-white/10`, bento-grid layouts with `rounded-2xl`, and motion-heavy components — shimmer, marquee, spotlight effects — rendered via Aceternity UI primitives. Display type is tightly tracked Inter Variable. Intended for developer tools, AI products, infrastructure SaaS, and any product aiming to signal technical sophistication and modern design literacy.

## Token block

```css
:root {
  /* Colors — zinc-950 ground is mandatory; NOT pure black */
  --color-bg:         oklch(10% 0.01 270);  /* ≈ #09090b — zinc-950 */
  --color-surface:    rgba(255, 255, 255, 0.02);
  --color-text:       #F4F4F5;              /* zinc-100 */
  --color-text-muted: #A1A1AA;              /* zinc-400 */
  --color-primary:    #7C3AED;              /* violet-700 — ONE vivid accent */
  --color-accent:     #7C3AED;
  --color-border:     rgba(255, 255, 255, 0.10);  /* border-white/10 */

  /* Colour washes (radial gradients, layered behind content) */
  --color-wash-1: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(124, 58, 237, 0.25) 0%, transparent 60%);
  --color-wash-2: radial-gradient(ellipse 60% 40% at 80% 80%,  rgba(16, 185, 129, 0.12) 0%, transparent 55%);

  /* Typography — Inter Variable, tight tracking */
  --font-display: 'Inter Variable', 'Inter', 'Helvetica Neue', system-ui, sans-serif;
  --font-body:    'Inter Variable', 'Inter', 'Helvetica Neue', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Courier New', monospace;

  /* Spacing */
  --spacing:           8px;
  --section-padding:   clamp(6rem, 8vw, 8rem);
  --max-width:         64rem;

  /* Shape — bento grid rounded-2xl */
  --radius: 16px;

  /* Tracking */
  --tracking-display: -0.04em;
  --tracking-body:    -0.01em;

  /* Shadow — multi-layer soft lift + rim light */
  --shadow:
    0 0 0 1px rgba(255, 255, 255, 0.06),
    0 24px 48px -12px rgba(0, 0, 0, 0.60);

  /* Motion */
  --motion-duration: 300ms;
  --motion-easing:   ease-out;

  /* Gradient border helper */
  --gradient-border: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.04) 100%);

  /* Shimmer animation (Aceternity shimmer component) */
  --shimmer-color:     rgba(255, 255, 255, 0.06);
  --shimmer-highlight: rgba(255, 255, 255, 0.12);
}
```

```ts
// tailwind.config.ts — theme extension
export default {
  theme: {
    extend: {
      colors: {
        bg:       'oklch(10% 0.01 270)',
        surface:  'rgba(255,255,255,0.02)',
        text:     '#F4F4F5',
        muted:    '#A1A1AA',
        primary:  '#7C3AED',
        accent:   '#7C3AED',
        border:   'rgba(255,255,255,0.10)',
        shimmer:  'rgba(255,255,255,0.06)',
      },
      fontFamily: {
        display: ['"Inter Variable"', 'Inter', '"Helvetica Neue"', 'system-ui', 'sans-serif'],
        body:    ['"Inter Variable"', 'Inter', '"Helvetica Neue"', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', '"Cascadia Code"', '"Courier New"', 'monospace'],
      },
      letterSpacing: {
        display: '-0.04em',
        body:    '-0.01em',
      },
      borderRadius: {
        DEFAULT: '16px',
        bento:   '16px',
        card:    '12px',
      },
      boxShadow: {
        bento: '0 0 0 1px rgba(255,255,255,0.06), 0 24px 48px -12px rgba(0,0,0,0.6)',
        glow:  '0 0 24px 0 rgba(124,58,237,0.35)',
      },
      transitionDuration: { DEFAULT: '300ms' },
      transitionTimingFunction: { DEFAULT: 'ease-out' },
      backgroundImage: {
        wash1:  'radial-gradient(ellipse 80% 50% at 50% -20%, rgba(124,58,237,0.25) 0%, transparent 60%)',
        wash2:  'radial-gradient(ellipse 60% 40% at 80% 80%, rgba(16,185,129,0.12) 0%, transparent 55%)',
        gborder: 'linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.04) 100%)',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if `--color-bg` is pure black (`#000000`) — the ground MUST be zinc-950 (`oklch(10% 0.01 270)` / `#09090b`), not pure black; the distinction is structural to the zinc material identity
- breaks if a second vivid chromatic accent is introduced alongside `--color-primary` — ONE accent colour rule is absolute
- breaks if the section padding is reduced below `4rem` — generous negative space is load-bearing for the premium feel
- breaks if `border-radius` drops below 12px on bento cards — `rounded-2xl` is the canonical bento shape
- breaks if the gradient border (`border-white/10`) is replaced with a solid opaque border — gradient-translucent borders are the card identity
- breaks if Inter Variable is replaced with a display serif or script font — tight-tracked geometric sans is structural
- breaks if `--tracking-display` is set to 0 or positive — negative letter-spacing on headings is mandatory for the dense editorial tone
- breaks if motion is disabled entirely — shimmer and marquee components require at minimum CSS `@keyframes` animations to be permitted

## Canonical render-test pointer

Render-test file: `references/render-tests/S-035-21st-aceternity-test.html` (generated from `references/_test-skeleton.html` + this file's `{{TOKEN}}` block; wash gradients injected as background-image layers on `<body>`).
Upstream source: https://github.com/21st-frontend-design (MIT) + https://ui.aceternity.com (MIT).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 110052 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- S-009 Aurora — dark aurora gradient, no bento grid, different accent language
- S-010 Cyberpunk — neon-hard cyber palette, no zinc-neutral base
- S-029 Data Viz Dark — data-dense dark surface, no landing-page bento structure
- Source: 21st-frontend-design (MIT) — https://github.com/21st-frontend-design
- Source: Aceternity UI (MIT) — https://ui.aceternity.com
