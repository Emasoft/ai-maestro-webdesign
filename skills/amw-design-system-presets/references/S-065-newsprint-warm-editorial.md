---
id: S-065
name: Newsprint / Warm Editorial (The Editorial)
aesthetic_position: print-editorial-library-reading-room
source_attribution: "styles-A §Newsprint / Warm Editorial (Stitch Preset); design-forge-main/references/discovery-framework.md; atelier-main/examples/05-dashboard-magazine.html. MIT (inferred from source repos)."
license: MIT (direct-port)
---

# S-065 — Newsprint / Warm Editorial (The Editorial)

**Filename:** `skills/amw-design-system-presets/references/S-065-newsprint-warm-editorial.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Newsprint / Warm Editorial — internally nicknamed "The Editorial" in the Stitch preset family — is the "library reading room" preset: warm, editorial, trustworthy, the digital transplant of a printed quality broadsheet or literary monthly. The visual fingerprint pairs Playfair Display at 700/800 (a high-contrast display serif with strong stroke modulation and ball terminals) for headlines with Source Sans 3 at 400/500 (a quiet workhorse humanist sans with print-newspaper lineage via Adobe's Source family) for body and ancillary text. The palette is warm cream paper with dark ink and one editorial accent — claret/burgundy or muted antique gold — applied sparingly to drop caps, pull-quote rules, and section markers. Layout is column-based: two-column or three-column at desktop with hairline vertical rules, moderate-to-high information density, generous internal leading. Borders are 1px hairline horizontal rules between sections (think the rule beneath a newspaper masthead). Radius is zero — print-style sharp corners. Box shadows are forbidden — depth comes from rule weight and paper warmth. Motion is minimal: a brief opacity fade on scroll, nothing more — content is the focus, not motion. Reach for it on long-form publications, magazine websites, university journals, op-ed columns, monthly newsletters as websites, literary or culture review sites, slow-news brands, gallery monographs, and any brief that asks for "earnest editorial weight, not SaaS shine."

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  /* Colors — warm cream paper, dark ink, single editorial accent */
  --color-bg:         #F4EDDD;   /* warm cream paper */
  --color-surface:    #ECE3CF;   /* slightly darker cream for sidebars / pull-quotes */
  --color-text:       #1A1612;   /* warm dark ink */
  --color-text-muted: #5C5246;   /* muted warm brown-grey */
  --color-text-faint: #8A7E6C;   /* faint warm grey for captions */
  --color-primary:    #7C1F2C;   /* claret / burgundy — editorial accent (swap to #A1804A muted antique gold) */
  --color-accent:     #7C1F2C;   /* same — Editorial uses ONE accent */
  --color-border:     #1A1612;   /* hairline rule in same dark ink as text */
  --color-border-faint: #C4B89D; /* faint warm rule for column separators */

  /* Typography */
  --font-display: 'Playfair Display', 'Source Serif 4', 'Georgia', 'Times New Roman', serif;
  --font-body:    'Source Sans 3', 'Source Sans Pro', 'Inter', 'system-ui', sans-serif;
  --font-mono:    'Source Code Pro', 'IBM Plex Mono', 'Courier New', monospace;

  /* Display sizing — editorial weight without slamming */
  --font-size-display:  clamp(40px, 6vw, 80px);
  --font-weight-display: 800;
  --letter-spacing-display: -0.01em;
  --line-height-display: 1.08;

  /* Body — high-leading editorial column rhythm */
  --font-size-body:     17px;
  --font-weight-body:   400;
  --line-height-body:   1.65;

  /* Pull-quote / drop-cap */
  --font-size-pull:     22px;
  --font-weight-pull:   400;
  --font-style-pull:    italic;
  --font-size-dropcap:  72px;
  --font-weight-dropcap: 800;

  /* Column layout */
  --content-width:    1100px;    /* multi-column max */
  --column-count:     2;         /* two-column desktop default (3 for high-density mode) */
  --column-gap:       40px;
  --column-rule-width: 1px;

  /* Geometry — print-style sharp */
  --spacing:      24px;
  --radius:       0px;             /* zero radius — print never rounds */
  --border-width: 1px;             /* hairline rules everywhere */

  /* No box shadows — depth is rule weight and paper warmth */
  --shadow:       none;

  /* Motion — minimal */
  --motion-duration: 280ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#F4EDDD',
        surface:     '#ECE3CF',
        text:        '#1A1612',
        'text-muted': '#5C5246',
        'text-faint': '#8A7E6C',
        primary:     '#7C1F2C',
        accent:      '#7C1F2C',
        border:      '#1A1612',
        'border-faint': '#C4B89D',
      },
      fontFamily: {
        display: ['"Playfair Display"', '"Source Serif 4"', 'Georgia', '"Times New Roman"', 'serif'],
        body:    ['"Source Sans 3"', '"Source Sans Pro"', 'Inter', 'system-ui', 'sans-serif'],
        mono:    ['"Source Code Pro"', '"IBM Plex Mono"', '"Courier New"', 'monospace'],
      },
      borderRadius: { DEFAULT: '0px' },
      borderWidth:  { DEFAULT: '1px' },
      boxShadow:    { DEFAULT: 'none' },
      transitionDuration: { DEFAULT: '280ms' },
      maxWidth: { content: '1100px' },
      columns: { '2': '2', '3': '3' },
    },
  },
};
```

**Drop-cap CSS snippet (editorial flourish for the first paragraph of any long-form piece):**
```css
.editorial-body > p:first-of-type::first-letter {
  font-family: var(--font-display);
  font-size: var(--font-size-dropcap);
  font-weight: var(--font-weight-dropcap);
  line-height: 0.85;
  float: left;
  padding: 6px 10px 0 0;
  color: var(--color-primary);
}
```

**Column rule snippet (between two-column body text):**
```css
.editorial-columns {
  column-count: var(--column-count);
  column-gap: var(--column-gap);
  column-rule: var(--column-rule-width) solid var(--color-border-faint);
}
```

## "Breaks if" invariants

- breaks if `border-radius` exceeds 0px — Editorial is print-derived and always sharp-cornered
- breaks if a modern SaaS palette (saturated teal, electric blue, neon accent) replaces the claret/burgundy or antique gold editorial accent
- breaks if a sans-serif display font replaces Playfair Display (or equivalent high-contrast serif) — the serif display is structural
- breaks if the background is pure white (`#FFFFFF`) or cold grey — the warm cream paper tint is the defining skin
- breaks if any decorative drop shadow appears — depth must come from rule weight and paper warmth alone
- breaks if motion duration exceeds ~400ms or any element scroll-animates dramatically — Editorial keeps motion quiet and content-first
- breaks if column-rule width or section-rule width exceeds 1px — hairline rules only
- breaks if information density is too low (whitespace-heavy "Luxury" treatment) — Editorial expects moderate-to-high density, column-based, reading-room weight
- breaks if more than one chromatic accent is deployed at full saturation — Editorial uses ONE (claret OR antique gold, not both)

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html`, wrap body copy in `<div class="editorial-columns editorial-body">`, set the hero h1 to Playfair Display 800 with `letter-spacing: -0.01em`, and add a 1px claret horizontal rule beneath the masthead.
Source render: no standalone upstream HTML demo — tokens direct-ported from `design-forge-main/references/discovery-framework.md` Newsprint preset description (Playfair Display + Source Sans 3, warm cream, claret accent, column-based, hairline rules) cross-checked against `atelier-main/examples/05-dashboard-magazine.html` (same family) for column / hairline-rule treatment.
Parity threshold: A-class justified (description-only upstream and a sibling render reference; no exact renderable HTML demo to diff against).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 79450 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-037 Cream Editorial (also warm cream + serif but Cormorant Garamond all-serif vs. Editorial's Playfair + sans body split), S-039 Warm Professional (Source Serif 4 + Source Sans 3 shared but business-trust tone vs. editorial-magazine), S-044 Dashboard Magazine (atelier sibling — same magazine column language applied to a dashboard surface), S-062 Luxury (also serif-driven with single accent but dark-ground gallery vs. Editorial's warm-paper reading room)
- **SKILL:** [../SKILL.md](../SKILL.md) — preset skill orchestrator
- **Catalogue:** [./catalogue.md](./catalogue.md) — routing index
- **Skeleton:** [./_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- **Source attribution:** `reports/batch9-harvest/styles-A.md` §Newsprint / Warm Editorial (Stitch Preset); `reports_dev/batch9/extracted/design-forge-main/references/discovery-framework.md`; `reports_dev/batch9/extracted/atelier-main/examples/05-dashboard-magazine.html`. License MIT (inferred from source repos).

## Attribution

Token values direct-ported (Playfair Display + Source Sans 3 pairing, warm cream paper, claret/burgundy or antique gold single accent, column-based layout with hairline column-rules, zero radius, no shadows, minimal motion) from `design-forge-main/references/discovery-framework.md` Newsprint / Warm Editorial preset (a.k.a. "The Editorial") cross-checked against `atelier-main/examples/05-dashboard-magazine.html` for column treatment, distilled via `reports/batch9-harvest/styles-A.md`. License MIT (inferred). Original distillation by the batch9 harvest team.
