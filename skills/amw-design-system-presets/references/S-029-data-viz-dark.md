---
id: S-029
name: Data Visualization Dark
aesthetic_position: developer-terminal-monospace
source_attribution: blocked-A styles.csv #19 (claude-skill-ui-ux-pro-max); reports/batch9-harvest/blocked-A.md
license: MIT
---

# S-029 — Data Visualization Dark

**Filename:** `references/S-029-data-viz-dark.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Data Visualization Dark is an analytics-first dark-canvas style optimized for the data-ink ratio: a deep indigo-navy background (`#1a1a2e`), desaturated categorical series colors (20–30% below full HSL saturation), monospaced tabular numerals, and dotted gridlines with no chart shadows. Every token choice serves legibility of quantitative content — the background is dark to make glowing chart lines pop, the series palette uses distinct hues (not tints) to avoid false grouping, and `font-variant-numeric: tabular-nums` aligns decimal columns. The intended audience is analytics dashboards, developer tooling, BI portals, financial reporting, and scientific visualization platforms.

## Token block

```css
/* S-029 Data Visualization Dark — complete token block */
:root {
  /* Canvas */
  --color-bg:          #1A1A2E;   /* deep indigo-navy */
  --color-surface:     #16213E;   /* slightly lighter navy card */
  --color-surface-2:   #0F3460;   /* elevated surface / selected state */
  --color-text:        #E2E8F0;   /* cool near-white for prose */
  --color-text-muted:  #94A3B8;   /* cool slate muted */
  --color-primary:     #5E8FDE;   /* muted blue — hsl(218,60%,62%) effective sat ~40% */
  --color-accent:      #5EC98E;   /* muted green — hsl(150,50%,58%) effective sat ~35% */
  --color-border:      rgba(255,255,255,0.08);   /* faint white rule */

  /* Categorical series palette — 6 distinct hues, each desaturated 20-30% below full */
  /* Rule: each series MUST be a different hue; no tinting the same hue */
  --series-1:          #5E8FDE;   /* muted blue    — primary axis */
  --series-2:          #5EC98E;   /* muted green */
  --series-3:          #E8835A;   /* muted orange */
  --series-4:          #A87FD4;   /* muted purple */
  --series-5:          #E8C35A;   /* muted yellow */
  --series-6:          #5ECDE8;   /* muted cyan */

  /* Chart structure */
  --chart-bg:          transparent;
  --chart-grid:        rgba(255,255,255,0.08);
  --gridline:          1px dashed rgba(255,255,255,0.08);   /* dotted gridlines signature */
  --axis-text:         #94A3B8;

  /* Typography — tabular numerals mandatory */
  --font-display:      'JetBrains Mono', 'Fira Code', 'IBM Plex Mono', monospace;
  --font-body:         'JetBrains Mono', 'Fira Code', 'IBM Plex Mono', monospace;
  --font-mono:         'JetBrains Mono', 'Fira Code', 'IBM Plex Mono', monospace;
  --font-feature-number: 'tnum';   /* tabular-nums OpenType feature — MANDATORY */

  /* Spacing & shape */
  --spacing:           8px;
  --radius:            4px;   /* functional minimal rounding; 0-4px range */

  /* Shadow — NONE on chart elements (data-ink ratio) */
  --shadow:            none;
  --chart-shadow:      none;   /* explicit — never apply drop-shadow to chart elements */

  /* Borders */
  --border-width:      1px;

  /* Motion — enter animations for data only */
  --motion-duration:   600ms;
  --motion-easing:     cubic-bezier(0.22, 1, 0.36, 1);   /* ease-out for data draw-on */
}
```

```js
// Tailwind theme extension — S-029 Data Visualization Dark
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        'dv-bg':         '#1A1A2E',
        'dv-surface':    '#16213E',
        'dv-surface-2':  '#0F3460',
        'dv-text':       '#E2E8F0',
        'dv-muted':      '#94A3B8',
        'dv-primary':    '#5E8FDE',
        'dv-accent':     '#5EC98E',
        'dv-border':     'rgba(255,255,255,0.08)',
        'dv-s1':         '#5E8FDE',
        'dv-s2':         '#5EC98E',
        'dv-s3':         '#E8835A',
        'dv-s4':         '#A87FD4',
        'dv-s5':         '#E8C35A',
        'dv-s6':         '#5ECDE8',
      },
      fontFamily: {
        display: ['JetBrains Mono', 'Fira Code', 'IBM Plex Mono', 'monospace'],
        body:    ['JetBrains Mono', 'Fira Code', 'IBM Plex Mono', 'monospace'],
        mono:    ['JetBrains Mono', 'Fira Code', 'IBM Plex Mono', 'monospace'],
      },
      borderRadius: {
        dv: '4px',
      },
      boxShadow: {
        dv: 'none',
      },
      transitionTimingFunction: {
        dv: 'cubic-bezier(0.22, 1, 0.36, 1)',
      },
      transitionDuration: {
        dv: '600ms',
      },
    },
  },
}
```

## "Breaks if" invariants

- breaks if any series color uses a tint of the same base hue as another series (e.g., two blues at different lightness) — the categorical palette requires distinct hues so each series is independently legible without a legend
- breaks if `font-variant-numeric: tabular-nums` is absent from any numeric display — column alignment is a functional requirement, not aesthetic preference
- breaks if `box-shadow` or `drop-shadow` is applied to chart elements — the data-ink ratio principle forbids shadows on visual encodings; shadows may only appear on UI chrome (modals, dropdown panels)
- breaks if gridlines are solid instead of dashed/dotted — the dotted gridline is the canonical data-viz-dark separator; solid gridlines create competing visual weight with data series
- breaks if the background is replaced by a warm dark (e.g., near-black with brown undertone) — the cool indigo-navy base is identity-defining; warm darks shift the aesthetic toward cinematic or editorial
- breaks if a proportional serif or display font replaces the monospaced body — all text must be monospaced; proportional fonts destroy tabular alignment
- breaks if saturated (full HSL) accent colors are introduced — series colors must remain 20–30% below full saturation; vivid colors blind the eye to data differences at the dense scan required by dashboards
- breaks if divergent color scales (red-to-green, blue-to-red) replace the categorical palette — divergent scales imply ordinal/continuous data; the preset is categorical; use sequential blues for ordered data as a separate configuration

## Canonical render-test pointer

Render-test: inject tokens from `## Token block` into `references/_test-skeleton.html` (substitute `{{BG}}=#1A1A2E`, `{{SURFACE}}=#16213E`, `{{TEXT}}=#E2E8F0`, `{{TEXT_MUTED}}=#94A3B8`, `{{PRIMARY}}=#5E8FDE`, `{{ACCENT}}=#5EC98E`, `{{BORDER}}=rgba(255,255,255,0.08)`, `{{FONT_DISPLAY}}='JetBrains Mono',monospace`, `{{FONT_BODY}}='JetBrains Mono',monospace`, `{{FONT_MONO}}='JetBrains Mono',monospace`, `{{RADIUS}}=4px`, `{{SHADOW}}=none`, `{{SPACING}}=8px`).

Upstream reference: `reports/batch9-harvest/blocked-A.md` #19 "Data Visualization Dark" token block; `claude-skill-ui-ux-pro-max styles.csv`.

## Render-test verdict

JOD: pending

## Cross-references

- Sibling styles: S-012 Retro Terminal (green-on-black mono, 0 radius — same monospace heritage, different purpose), S-038 Dark Tech (dark canvas + JetBrains Mono but proportional + 2px radius; no data-ink constraints), S-036 Cinematic Dark (dark canvas but serif headlines and atmospheric styling)
- Source: `reports/batch9-harvest/blocked-A.md` #19 (MIT — claude-skill-ui-ux-pro-max); `reports/batch9-harvest/styles-A.md` "Data Visualization" entry.

## Attribution

Direct port from `blocked-A.md` #19 token block (MIT license via claude-skill-ui-ux-pro-max). Extended series palette and Tailwind extension are original authoring for this plugin. Catalog summary and "breaks-if" invariants are original content. License: MIT.
