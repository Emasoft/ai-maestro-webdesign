---
id: S-045
name: Warm Minimalism (Notion)
aesthetic_position: editorial-warm-paper
source_attribution: Notion.so design language (clean-room derivation); atelier-main Organic/Natural tone B1 #4 (MIT, inferred); frontend-design-engineer visual-directions.md (not stated)
license: clean-room derivation (no verbatim copy)
---

# S-045 — Warm Minimalism (Notion)

**Filename:** `skills/amw-design-system-presets/references/S-045-warm-minimalism.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Warm Minimalism captures the Notion aesthetic — an off-white, cream-toned workspace that feels like premium paper stock, not a clinical white screen. The visual fingerprint is restrained: serif headings (Georgia or Lora) sitting above sans-serif body text, a 4-5 level grey hierarchy that avoids harsh contrast, a single muted accent (terracotta `#D97757` or sage `#6B8F71`) deployed sparingly, and 4–6px corner radius on all interactive elements. Shadows are almost imperceptible — `0 1px 2px rgba(0,0,0,0.04)` — signaling elevation without weight. The layout is single-column reading flow with generous line-height. Intended audience: productivity tools, note-taking apps, internal wikis, personal portfolios, documentation sites, and editorial products targeting knowledge workers.

## Token block

```css
:root {
  /* Colors */
  --color-bg:         #FAF8F2;   /* warm off-white / cream */
  --color-surface:    #F5F2EA;   /* card / elevated surface */
  --color-text:       #1F1E1B;   /* near-black warm ink */
  --color-text-muted: #6B6860;   /* muted warm grey */
  --color-text-faint: #9E9B93;   /* faint secondary label */
  --color-primary:    #D97757;   /* terracotta accent */
  --color-accent:     #6B8F71;   /* sage — secondary accent; use one OR the other */
  --color-border:     #E8E4D9;   /* soft warm hairline */

  /* Typography */
  --font-display: 'Lora', 'Georgia', 'Times New Roman', serif;
  --font-body:    'Inter', 'system-ui', '-apple-system', sans-serif;
  --font-mono:    'iA Writer Mono', 'Fira Code', 'Courier New', monospace;

  /* Reading layout */
  --content-width:    680px;
  --line-height-body: 1.75;
  --font-size-body:   17px;

  /* Geometry */
  --spacing:      8px;
  --radius:       5px;           /* 4–6px per invariant; 5px is canonical midpoint */
  --border-width: 1px;

  /* Shadow — almost imperceptible */
  --shadow:       0 1px 2px rgba(0, 0, 0, 0.04);
  --shadow-card:  0 2px 8px rgba(0, 0, 0, 0.06);

  /* Motion */
  --motion-duration: 150ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#FAF8F2',
        surface:     '#F5F2EA',
        text:        '#1F1E1B',
        'text-muted': '#6B6860',
        'text-faint': '#9E9B93',
        primary:     '#D97757',
        accent:      '#6B8F71',
        border:      '#E8E4D9',
      },
      fontFamily: {
        display: ['Lora', 'Georgia', '"Times New Roman"', 'serif'],
        body:    ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono:    ['"iA Writer Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
      },
      borderRadius: { DEFAULT: '5px', sm: '4px', md: '6px' },
      boxShadow: {
        DEFAULT: '0 1px 2px rgba(0,0,0,0.04)',
        card:    '0 2px 8px rgba(0,0,0,0.06)',
        none:    'none',
      },
      transitionDuration: { DEFAULT: '150ms' },
      maxWidth: { content: '680px' },
    },
  },
};
```

**Dark variant token override:**
```css
[data-theme="dark"] {
  --color-bg:         #1F1E1B;
  --color-surface:    #2A2926;
  --color-text:       #F0EDE5;
  --color-text-muted: #9E9B93;
  --color-text-faint: #6B6860;
  --color-border:     #38352E;
}
```

## "Breaks if" invariants

- breaks if `border-radius` falls below 4px or exceeds 6px on interactive elements
- breaks if the background is pure white (`#FFFFFF`) — the warm off-white tint is the defining skin
- breaks if shadows exceed `0 4px 16px rgba(0,0,0,0.08)` — shadows must remain near-imperceptible
- breaks if a second chromatic accent is introduced at full saturation alongside the primary (terracotta OR sage; not both simultaneously at equal weight)
- breaks if body text is set in a serif font — the display/body split (serif heading / sans body) is structural
- breaks if line-height drops below 1.65 or the content column exceeds 760px (single-column reading rhythm)
- breaks if high-chroma colors (saturated blue, vivid red, neon) appear anywhere in the palette
- breaks if dense card-grid or multi-column data layouts replace the single-column reading flow

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers.
Upstream parity source: Notion.so (live, as of 2026) — clean-room derivation, no verbatim copy of Notion source. Visual reference only.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 115869 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-037 Cream Editorial (Cormorant Garamond, all-serif, 0px radius), S-039 Warm Professional (Source Serif 4 + Source Sans 3, business-trust), S-020 Organic (blob radius, grain 1–3%, warm shadow)
- **Source attribution:** Notion.so design language (visual reference, clean-room); `reports_dev/batch9/extracted/atelier-main/SKILL.md` tone B1 #4 Organic/Natural (MIT, inferred); `reports_dev/batch9/extracted/frontend-design-engineer-skill-main/frontend-design-engineer/references/visual-directions.md` Understated Elegance entry
