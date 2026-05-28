---
id: S-038
name: Dark Tech
aesthetic_position: developer-terminal-monospace
source_attribution: >
  blocked-B.md seed table "Dark Tech" (10-style Wave 1 Track H8 seed);
  styles-B.md "Dark Tech" developer-terminal position; frontend-design-engineer-skill-main
  visual-directions.md dark-professional category; tasteful-ui-skill-master
  catalog modern-dark-developer entry.
  LICENSE: MIT (tasteful-ui-skill, web-designer-plugin, frontend-design-engineer-skill).
license: MIT (all upstream sources)
---

# S-038 — Dark Tech

**Filename:** `skills/amw-design-system-presets/references/S-038-dark-tech.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## Identity

Dark Tech is a modern dark-developer aesthetic that occupies the territory between a terminal tool and a polished SaaS product — it is explicitly NOT retro, NOT scanlines, NOT neon-glow. Its visual fingerprint is a near-black canvas (`#0A0A0A`), Space Grotesk for all prose (its geometric-grotesque forms read as contemporary technical authority), JetBrains Mono for all code and data, and a single electric-blue or cyan accent that signals interactivity without overwhelming the dark field. Intended audience: developer tools, API documentation sites, CLI-companion dashboards, technical SaaS products, and code-heavy landing pages where density and precision signal credibility.

## Token block

```css
/* S-038 Dark Tech — CSS custom properties */
:root {
  /* Color */
  --color-bg:          #0A0A0A;   /* near-black — clean dark canvas without warm cast */
  --color-surface:     #141414;   /* panel / card surface */
  --color-surface-2:   #1E1E1E;   /* elevated surface (modal, code block bg) */
  --color-text:        #E8E8E8;   /* cool light grey — technical readability */
  --color-text-muted:  #6C6C6C;   /* desaturated mid-grey — metadata, comments */
  --color-primary:     #E8E8E8;   /* primary action = text colour */
  --color-accent:      #3B82F6;   /* electric blue — one interactive signal */
  --color-accent-dim:  #1D4ED8;   /* dimmed accent for hover/pressed */
  --color-border:      #262626;   /* hairline border — barely-visible structural edge */

  /* Typography */
  --font-display: 'Space Grotesk', 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --font-body:    'Space Grotesk', 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Courier New', monospace;

  /* Spacing */
  --spacing: 8px;   /* base unit; dense data tables use 4× = 32px row height */

  /* Shape — minimal radius, not zero (not retro terminal) */
  --radius: 2px;

  /* Shadow — cool-toned only */
  --shadow: 0 4px 16px rgba(0, 0, 0, 0.5);

  /* Motion — crisp and fast; technical tools don't dawdle */
  --motion-duration: 150ms;
  --motion-easing: cubic-bezier(0.4, 0, 0.2, 1);

  /* Tech extras */
  --border-width: 1px;
  --code-bg: #1E1E1E;        /* code block background (matches surface-2) */
  --accent-glow: 0 0 12px rgba(59, 130, 246, 0.15);   /* subtle blue ambient on focus */
}
```

```ts
// S-038 Dark Tech — Tailwind theme extension
const darkTech = {
  colors: {
    bg:          '#0A0A0A',
    surface:     '#141414',
    'surface-2': '#1E1E1E',
    text:        '#E8E8E8',
    'text-muted':'#6C6C6C',
    primary:     '#E8E8E8',
    accent:      '#3B82F6',
    'accent-dim':'#1D4ED8',
    border:      '#262626',
  },
  fontFamily: {
    display: ['"Space Grotesk"', 'Inter', '"Helvetica Neue"', 'Arial', 'sans-serif'],
    body:    ['"Space Grotesk"', 'Inter', '"Helvetica Neue"', 'Arial', 'sans-serif'],
    mono:    ['"JetBrains Mono"', '"Fira Code"', '"Cascadia Code"', '"Courier New"', 'monospace'],
  },
  spacing: { base: '8px' },
  borderRadius: { DEFAULT: '2px' },
  boxShadow: {
    DEFAULT: '0 4px 16px rgba(0,0,0,0.5)',
    glow: '0 0 12px rgba(59,130,246,0.15)',
  },
  transitionDuration: { DEFAULT: '150ms' },
  transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.4,0,0.2,1)' },
} as const;
```

## "Breaks if" invariants

- breaks if a serif or display font is used for any typographic role (display, body, heading)
- breaks if border-radius exceeds 4px on any primary UI element
- breaks if a neon or warm accent colour (green, amber, pink, red) is introduced — accent must remain in the blue/cyan/teal range
- breaks if scanlines, grain, or CRT visual effects are applied (retro is explicitly excluded from this preset)
- breaks if a second chromatic accent colour is introduced alongside the primary blue
- breaks if transitions exceed 300ms (technical tools must feel instant)
- breaks if body text uses a warm undertone background rather than the cool near-black canvas
- breaks if the accent is rendered as a glow wider than 20px on non-focus elements
- breaks if code blocks use a different font than the declared mono stack
- breaks if the design includes decorative gradients or aurora-style light effects on the page canvas

## Canonical render-test pointer

Render test: inject this file's tokens into `references/_test-skeleton.html` (substituting `{{BG}}` = `#0A0A0A`, `{{SURFACE}}` = `#141414`, `{{TEXT}}` = `#E8E8E8`, `{{TEXT_MUTED}}` = `#6C6C6C`, `{{PRIMARY}}` = `#E8E8E8`, `{{ACCENT}}` = `#3B82F6`, `{{BORDER}}` = `#262626`, `{{FONT_DISPLAY}}` = `'Space Grotesk', 'Inter', sans-serif`, `{{FONT_BODY}}` = `'Space Grotesk', 'Inter', sans-serif`, `{{FONT_MONO}}` = `'JetBrains Mono', 'Fira Code', monospace`, `{{RADIUS}}` = `2px`, `{{SHADOW}}` = `0 4px 16px rgba(0,0,0,.5)`, `{{SPACING}}` = `8px`).

Upstream parity source: `blocked-B.md` seed table "Dark Tech" + `frontend-design-engineer-skill-main/visual-directions.md` (MIT, inferred).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 81632 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- Siblings: S-012 Retro Terminal (scanlines + green-on-black retro), S-032 Retro Device (vintage hardware chrome), S-033 Win98 (95/98 UI nostalgia), S-029 Data Viz Dark (chart-first data canvas)
- Differentiators: S-038 is contemporary dark developer with NO retro elements; S-012 is deliberately CRT/terminal retro; S-032 emulates physical hardware; S-033 is Win9x nostalgia; S-029 is data-primary not dev-tool
- Source: `blocked-B.md` seed table Wave 1 Track H8 + `tasteful-ui-skill-master` catalog (MIT)
