---
id: S-064
name: Hand-draw
aesthetic_position: organic-sketch-illustrative
source_attribution: "styles-A §Hand-draw (Stitch Preset); design-forge-main/references/discovery-framework.md. MIT (inferred from repo)."
license: MIT (direct-port)
---

# S-064 — Hand-draw

**Filename:** `skills/amw-design-system-presets/references/S-064-hand-draw.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Hand-draw is the "artist's studio" preset — sketchy, organic, informal, the visual register of a small-batch craft product or independent creator rather than a polished SaaS platform. The visual fingerprint pairs Fraunces at 700/900 (a sturdy modern serif with organic curves and varied stroke modulation) for display with Outfit at 300/400 (a clean humanist sans for body readability) — the contrast between hand-feeling display and quiet body is the entire skin's heart. The palette is soft, earthy, muted: warm sand, dusty terracotta, moss green, ink charcoal, faded cobalt — no saturated chroma. Fills are slightly uneven (a touch of grain or a subtle SVG noise overlay around 2%). Borders are irregular — sketch-style strokes drawn as inline SVG paths with `stroke-dasharray` or `<filter feTurbulence>` displacement rather than CSS `border`. Radius is organic — non-uniform corner values that vary slightly element-to-element (e.g. `border-radius: 12px 18px 9px 15px / 14px 10px 16px 11px`). Motion is gentle: spring easing with mild overshoot, and SVG path-drawing reveals where `stroke-dashoffset` animates from `pathLength` to `0`. Reach for it on illustration-driven landing pages, indie product sites, children's products, handmade goods, lifestyle / wellness brands, creator portfolios, art-school course pages, and any brief that asks for "human warmth, not polish."

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  /* Colors — soft, earthy, muted; no saturated chroma */
  --color-bg:         #F6F1E7;   /* warm sand paper */
  --color-surface:    #EDE5D2;   /* darker sand for cards */
  --color-text:       #2A2620;   /* ink charcoal */
  --color-text-muted: #6E665A;   /* muted warm brown-grey */
  --color-text-faint: #A39A89;   /* faint warm grey */
  --color-primary:    #C56A4A;   /* dusty terracotta */
  --color-accent:     #7A8F6A;   /* muted moss green — secondary */
  --color-accent-blue: #6985A3;  /* faded cobalt — tertiary */
  --color-border:     #2A2620;   /* sketch ink (used in SVG strokes, not CSS borders) */

  /* Typography */
  --font-display: 'Fraunces', 'Lora', 'Georgia', serif;
  --font-body:    'Outfit', 'Inter', 'system-ui', sans-serif;
  --font-mono:    'JetBrains Mono', 'Courier New', monospace;

  /* Display sizing */
  --font-size-display:  clamp(44px, 7vw, 88px);
  --font-weight-display: 900;          /* Fraunces 900 has the most organic curves */
  --font-variation-display: 'opsz' 144, 'SOFT' 100;  /* Fraunces variable axes — max soft */
  --font-size-body:     17px;
  --font-weight-body:   400;
  --line-height-display: 1.05;
  --line-height-body:    1.7;

  /* Geometry — organic, non-uniform */
  --spacing:      24px;
  --content-width: 720px;          /* reading-flow column */
  --radius-organic: 12px 18px 9px 15px / 14px 10px 16px 11px;   /* asymmetric per-corner */
  --radius:       14px;            /* fallback rounded value when organic isn't appropriate */
  --border-width: 1.5px;           /* slightly hand-drawn weight (used in SVG strokes) */

  /* Grain overlay — subtle texture */
  --grain-opacity: 0.02;           /* 2% — barely perceptible noise */

  /* Soft, gentle shadow — not a polished elevation */
  --shadow:       0 4px 12px rgba(42, 38, 32, 0.08);

  /* Motion — gentle spring */
  --motion-duration: 400ms;
  --motion-easing-spring: cubic-bezier(0.34, 1.56, 0.64, 1);  /* soft overshoot */
  --motion-easing:        var(--motion-easing-spring);
  --motion-path-draw-duration: 900ms;   /* SVG stroke-dashoffset draw-in */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#F6F1E7',
        surface:     '#EDE5D2',
        text:        '#2A2620',
        'text-muted': '#6E665A',
        'text-faint': '#A39A89',
        primary:     '#C56A4A',
        accent:      '#7A8F6A',
        'accent-blue': '#6985A3',
        border:      '#2A2620',
      },
      fontFamily: {
        display: ['Fraunces', 'Lora', 'Georgia', 'serif'],
        body:    ['Outfit', 'Inter', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Courier New"', 'monospace'],
      },
      borderRadius: {
        DEFAULT: '14px',
        organic: '12px 18px 9px 15px / 14px 10px 16px 11px',
      },
      borderWidth: { DEFAULT: '1.5px' },
      boxShadow: { DEFAULT: '0 4px 12px rgba(42, 38, 32, 0.08)' },
      transitionDuration: { DEFAULT: '400ms' },
      transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.34, 1.56, 0.64, 1)' },
      maxWidth: { content: '720px' },
    },
  },
};
```

**Sketch border SVG snippet (replaces CSS `border` for the sketchy stroke effect):**
```html
<!-- wrap a card in this SVG envelope; path uses turbulence for irregular wobble -->
<svg width="100%" height="100%" preserveAspectRatio="none" style="position:absolute; inset:0; pointer-events:none;">
  <defs>
    <filter id="sketch-wobble">
      <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="2"/>
    </filter>
  </defs>
  <rect x="2" y="2" width="calc(100% - 4px)" height="calc(100% - 4px)"
        fill="none" stroke="var(--color-border)" stroke-width="1.5"
        filter="url(#sketch-wobble)"
        pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"
        style="animation: sketch-draw var(--motion-path-draw-duration) var(--motion-easing) forwards;"/>
</svg>
<style>
  @keyframes sketch-draw { to { stroke-dashoffset: 0; } }
  @media (prefers-reduced-motion: reduce) {
    rect { animation: none; stroke-dashoffset: 0; }
  }
</style>
```

**Grain overlay snippet:**
```html
<div aria-hidden="true" style="position:fixed; inset:0; pointer-events:none; opacity:var(--grain-opacity);
  background-image: url('data:image/svg+xml;utf8,&lt;svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22160%22 height=%22160%22&gt;&lt;filter id=%22n%22&gt;&lt;feTurbulence type=%22fractalNoise%22 baseFrequency=%220.85%22/&gt;&lt;/filter&gt;&lt;rect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23n)%22/&gt;&lt;/svg&gt;');"></div>
```

## "Breaks if" invariants

- breaks if a rigid grid is enforced — Hand-draw layout is organic / content-led / asymmetric
- breaks if a polished sans-serif display font (Inter, Helvetica, geometric grotesque) replaces Fraunces or its serif siblings
- breaks if saturated / corporate-palette colours (electric blue, neon green, brand-saturated red) appear — Hand-draw stays muted
- breaks if borders are perfect CSS `border` rules with no irregularity — sketch wobble (SVG `<feTurbulence>` displacement or hand-drawn stroke) is structural
- breaks if uniform symmetric corner radius (`border-radius: 12px`) is used on hero/card surfaces — organic asymmetric radius is the look
- breaks if motion is linear-eased or instant — gentle spring with soft overshoot is the entire motion register
- breaks if grain opacity exceeds ~4% — texture must be felt, not seen
- breaks if `prefers-reduced-motion: reduce` is not honoured on SVG path-draw reveals — fallback to static `stroke-dashoffset: 0`

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html`, replace card `border` with the SVG sketch-envelope snippet, and add the grain-overlay snippet to `<body>`. Set hero display to Fraunces 900 with full softness axis.
Source render: no standalone upstream HTML demo — tokens direct-ported from `design-forge-main/references/discovery-framework.md` Hand-draw preset description (Fraunces + Outfit, soft earthy colours, sketch borders, SVG path-draw motion).
Parity threshold: A-class justified (description-only upstream; no renderable HTML demo to diff against).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 63680 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-007 Claymorphism (also playful but uses polished clay-volume shapes vs. flat sketch), S-020 Organic (warm shadow + blob radius shared but no SVG sketch wobble), S-026 Wabi-sabi / Imperfect (asymmetry + grain shared but darker / more contemplative palette), S-042 Memphis (also colourful and informal but bright pop colours vs. Hand-draw's earthy mutes)
- **SKILL:** [../SKILL.md](../SKILL.md) — preset skill orchestrator
- **Catalogue:** [./catalogue.md](./catalogue.md) — routing index
- **Skeleton:** [./_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- **Source attribution:** `reports/batch9-harvest/styles-A.md` §Hand-draw (Stitch Preset); `design-forge-main/references/discovery-framework.md`. License MIT (inferred from source repo).

## Attribution

Token values direct-ported (Fraunces + Outfit pairing, soft earthy muted palette, sketch-style irregular borders via SVG `<feTurbulence>` displacement, organic asymmetric radius, gentle spring motion, SVG path-draw reveals) from `design-forge-main/references/discovery-framework.md` Hand-draw preset, distilled via `reports/batch9-harvest/styles-A.md`. License MIT (inferred). Original distillation by the batch9 harvest team.
