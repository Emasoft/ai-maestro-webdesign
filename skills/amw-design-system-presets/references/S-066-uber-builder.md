---
id: S-066
name: Uber Builder
aesthetic_position: technical-product-systematic
source_attribution: >
  styles-A.md "Stitch Uber Design System Preset — The Builder"
  (design-forge-main/references/discovery-framework.md).
  LICENSE: MIT (inferred, design-forge-main).
license: MIT (design-forge-main)
---

# S-066 — Uber Builder

**Filename:** `skills/amw-design-system-presets/references/S-066-uber-builder.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Uber Builder is a research-laboratory aesthetic — technical, clean, and systematic. It is product-forward, not marketing-forward: the visual register is closer to a control panel than a campaign page. The fingerprint is a tight neutral palette (black/white/grey) with a single technical accent, Space Grotesk for display headings (700 weight) and Inter for body (400/500), high information density (data tables, structured lists, dense cards), 4px corner radius across all interactive elements, and functional elevation rather than decorative shadow. Motion is functional only — no decorative animation, no scroll choreography. Intended audience: operational dashboards, B2B platform consoles, fleet/logistics tools, API metrics interfaces, internal admin UIs, and any product where data density and systematic structure signal credibility over warmth.

## Token block

```css
/* S-066 Uber Builder — CSS custom properties */
:root {
  /* Colors — neutral functional base + single technical accent */
  --color-bg:          #FFFFFF;   /* white canvas (or #0A0A0A for dark variant) */
  --color-surface:     #F7F7F7;   /* card / panel surface (warm-neutral grey) */
  --color-surface-2:   #EEEEEE;   /* elevated surface, table header row */
  --color-text:        #0A0A0A;   /* near-black ink — maximum reading contrast */
  --color-text-muted:  #5C5C5C;   /* mid-grey for metadata + secondary rows */
  --color-text-faint:  #9A9A9A;   /* faint label / placeholder */
  --color-primary:     #0A0A0A;   /* primary action = ink colour */
  --color-accent:      #276EF1;   /* Uber blue — single technical accent */
  --color-accent-dim:  #1E54B7;   /* pressed / hover-dim variant */
  --color-border:      #E2E2E2;   /* hairline border — 1px structural edge */
  --color-success:     #05A357;   /* status only — never decorative */
  --color-warning:     #FFC043;
  --color-error:       #E11900;

  /* Typography */
  --font-display: 'Space Grotesk', 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --font-body:    'Inter', 'Helvetica Neue', 'system-ui', '-apple-system', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'SF Mono', 'Courier New', monospace;

  /* Type scale — high information density */
  --font-size-body:    14px;
  --font-size-label:   12px;
  --line-height-body:  1.5;

  /* Geometry — dense, structured */
  --spacing:      8px;     /* base unit; data rows 4× = 32px row height */
  --radius:       4px;     /* canonical — applies to buttons, inputs, cards */
  --border-width: 1px;

  /* Shadow — functional elevation only, NOT decorative */
  --shadow:       0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-card:  0 1px 3px rgba(0, 0, 0, 0.08);
  --shadow-modal: 0 8px 24px rgba(0, 0, 0, 0.12);

  /* Motion — functional, fast, no decoration */
  --motion-duration: 120ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);
}
```

```ts
// S-066 Uber Builder — Tailwind theme extension
const uberBuilder = {
  colors: {
    bg:           '#FFFFFF',
    surface:      '#F7F7F7',
    'surface-2':  '#EEEEEE',
    text:         '#0A0A0A',
    'text-muted': '#5C5C5C',
    'text-faint': '#9A9A9A',
    primary:      '#0A0A0A',
    accent:       '#276EF1',
    'accent-dim': '#1E54B7',
    border:       '#E2E2E2',
    success:      '#05A357',
    warning:      '#FFC043',
    error:        '#E11900',
  },
  fontFamily: {
    display: ['"Space Grotesk"', 'Inter', '"Helvetica Neue"', 'Arial', 'sans-serif'],
    body:    ['Inter', '"Helvetica Neue"', 'system-ui', '-apple-system', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"Fira Code"', '"SF Mono"', '"Courier New"', 'monospace'],
  },
  fontSize: {
    body:  ['14px', { lineHeight: '1.5' }],
    label: ['12px', { lineHeight: '1.4' }],
  },
  spacing: { base: '8px' },
  borderRadius: { DEFAULT: '4px' },
  boxShadow: {
    DEFAULT: '0 1px 2px rgba(0,0,0,0.06)',
    card:    '0 1px 3px rgba(0,0,0,0.08)',
    modal:   '0 8px 24px rgba(0,0,0,0.12)',
  },
  transitionDuration: { DEFAULT: '120ms' },
  transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #0A0A0A;
  --color-surface:    #161616;
  --color-surface-2:  #1F1F1F;
  --color-text:       #F2F2F2;
  --color-text-muted: #9A9A9A;
  --color-text-faint: #6C6C6C;
  --color-primary:    #F2F2F2;
  --color-border:     #2A2A2A;
}
```

## "Breaks if" invariants

- breaks if border-radius exceeds 6px on any primary UI element (4px is canonical, 0–6px tolerated)
- breaks if a second chromatic accent is added alongside the technical blue (single-accent rule is structural)
- breaks if Space Grotesk is replaced on display headings with a serif or geometric-rounded font (Space Grotesk's mechanical-grotesque silhouette IS the brand)
- breaks if body text uses any font other than Inter or a near-identical neo-grotesque (no humanist serif, no rounded sans)
- breaks if shadows exceed `0 4px 12px rgba(0,0,0,0.15)` — elevation must remain functional, never decorative
- breaks if decorative animation, scroll-driven parallax, or hover-flourish is introduced (motion is functional-only: state transitions, focus rings, dropdowns)
- breaks if the palette adopts warm undertones (cream backgrounds, amber accents, terracotta) — the canvas is cool-neutral
- breaks if line-height exceeds 1.65 on body text (high density requires tight rhythm)
- breaks if gradient fills appear anywhere outside chart data visualisation
- breaks if data tables use zebra striping in a chromatic hue rather than `--color-surface` grey alternation

## Canonical render-test pointer

Render test: inject this file's tokens into `references/_test-skeleton.html` (substituting `{{BG}}` = `#FFFFFF`, `{{SURFACE}}` = `#F7F7F7`, `{{TEXT}}` = `#0A0A0A`, `{{TEXT_MUTED}}` = `#5C5C5C`, `{{PRIMARY}}` = `#0A0A0A`, `{{ACCENT}}` = `#276EF1`, `{{BORDER}}` = `#E2E2E2`, `{{FONT_DISPLAY}}` = `'Space Grotesk', 'Inter', sans-serif`, `{{FONT_BODY}}` = `'Inter', sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', monospace`, `{{RADIUS}}` = `4px`, `{{SHADOW}}` = `0 1px 2px rgba(0,0,0,0.06)`, `{{SPACING}}` = `8px`).

Upstream parity source: `design-forge-main/references/discovery-framework.md` "Stitch Uber Design System Preset — The Builder" (MIT, inferred).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 84477 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-001 Swiss (Inter-only, electric blue, ultra-strict grid), S-017 Corporate Bold (high-density product UI with warmer palette), S-029 Data Viz Dark (chart-first dashboard), S-044 Dashboard Magazine (FT-style data with cream paper)
- **Differentiators:** S-066 is product-system (operational console), not marketing-clean (S-001) nor data-as-decoration (S-029); the Space Grotesk display / Inter body split is structural and distinguishes it from S-001's Inter-only stack
- **Source:** styles-A.md "Stitch Uber Design System Preset — The Builder" (`design-forge-main/references/discovery-framework.md`, MIT inferred)
