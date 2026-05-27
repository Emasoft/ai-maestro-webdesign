---
id: S-062
name: Luxury (The Luxury)
aesthetic_position: gallery-opening-cinematic
source_attribution: "styles-A §Luxury (Stitch Preset); design-forge-main/references/discovery-framework.md. MIT (inferred from repo)."
license: MIT (direct-port)
---

# S-062 — Luxury (The Luxury)

**Filename:** `skills/amw-design-system-presets/references/S-062-luxury.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Luxury — internally nicknamed "The Luxury" in the Stitch preset family — is the gallery-opening preset: elegant, refined, sovereign in tone, and visually unmistakable. The visual fingerprint pairs Cormorant Garamond at 600/700 (a high-contrast didone-adjacent serif with deep stroke modulation) for display with Tenor Sans at 400 (a quiet, geometric sans with classical proportions) for body. The palette is dark-first — a deep neutral ground (true black or ink-charcoal) backing a single metallic accent: aged gold (`#C9A961`) or champagne. Maximum contrast: stark ink-on-cream or cream-on-ink, no mid-tone fillers. Borders are hairline (1px maximum) or absent entirely. Radius is zero. Box shadows are forbidden — depth is implied by negative space alone. Motion is cinematic and slow — long opacity fades, easing-in-out 600–900ms reveals. Layout is sovereign: generous whitespace, single dominant artefact per fold, low information density. Reach for it on luxury fashion landing pages, premium hospitality sites, jewellery houses, fine-wine merchants, gallery / museum surfaces, perfumeries, and any brief that wants the visitor to feel they have walked into a vernissage.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  /* Colors — dark-first, max contrast, single metallic accent */
  --color-bg:         #0B0B0B;   /* deep neutral ground — ink charcoal */
  --color-surface:    #141414;   /* barely-lifted surface */
  --color-text:       #EDE7D6;   /* warm cream ink on dark */
  --color-text-muted: #8A8474;   /* muted warm grey */
  --color-text-faint: #5C574B;   /* faint warm grey for fine print */
  --color-primary:    #C9A961;   /* aged gold accent (swap to champagne #D4BC83) */
  --color-accent:     #C9A961;   /* same — Luxury uses ONE metallic accent */
  --color-border:     #2A2620;   /* hairline near-bg with warm cast */

  /* Typography */
  --font-display: 'Cormorant Garamond', 'EB Garamond', 'Times New Roman', serif;
  --font-body:    'Tenor Sans', 'Optima', 'Avenir Next', sans-serif;
  --font-mono:    'IBM Plex Mono', 'Courier New', monospace;

  /* Display sizing — Cormorant runs large and quiet */
  --font-size-display:  clamp(56px, 9vw, 128px);
  --font-weight-display: 600;
  --font-size-body:     17px;
  --font-weight-body:   400;
  --letter-spacing-display: 0em;
  --letter-spacing-body:    0.01em;  /* Tenor Sans benefits from microscopic tracking */
  --line-height-display: 1.05;
  --line-height-body:    1.7;

  /* Geometry — sovereign whitespace */
  --spacing:      32px;            /* generous base spacing */
  --content-width: 920px;          /* sovereign single-column or 2-col gallery */
  --radius:       0px;             /* zero radius — Luxury is sharp-cornered */
  --border-width: 1px;             /* hairline borders only */

  /* No box shadows — depth is implied by whitespace */
  --shadow:       none;

  /* Motion — cinematic, slow */
  --motion-duration: 700ms;
  --motion-easing:   cubic-bezier(0.4, 0, 0.2, 1);   /* slow ease-in-out */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#0B0B0B',
        surface:     '#141414',
        text:        '#EDE7D6',
        'text-muted': '#8A8474',
        'text-faint': '#5C574B',
        primary:     '#C9A961',
        accent:      '#C9A961',
        border:      '#2A2620',
      },
      fontFamily: {
        display: ['"Cormorant Garamond"', '"EB Garamond"', '"Times New Roman"', 'serif'],
        body:    ['"Tenor Sans"', 'Optima', '"Avenir Next"', 'sans-serif'],
        mono:    ['"IBM Plex Mono"', '"Courier New"', 'monospace'],
      },
      borderRadius: { DEFAULT: '0px' },
      borderWidth:  { DEFAULT: '1px' },
      boxShadow:    { DEFAULT: 'none' },
      transitionDuration: { DEFAULT: '700ms' },
      transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.4, 0, 0.2, 1)' },
      maxWidth: { content: '920px' },
    },
  },
};
```

**Cream-ground variant token override (for surfaces that want light Luxury):**
```css
[data-variant="cream"] {
  --color-bg:      #F5F1E8;     /* warm cream paper */
  --color-surface: #EDE7D6;
  --color-text:    #1A1815;
  --color-text-muted: #4A4538;
  --color-border:  #C4BCAD;
}
```

## "Breaks if" invariants

- breaks if `border-radius` exceeds 0px — Luxury is always sharp-cornered, never rounded
- breaks if a bright chromatic accent (saturated red, blue, magenta, lime) replaces the muted metallic — Luxury reads as gold/champagne, not pop-colour
- breaks if friendly or playful display typography (rounded sans, slab serif, geometric monoline) replaces the high-contrast didone-adjacent serif
- breaks if any decorative drop shadow / coloured shadow / glow appears — depth is implied by whitespace alone
- breaks if information density rises above ~3 primary elements per fold — Luxury is sovereign / low-density
- breaks if motion durations fall below ~500ms or easing curves are bouncy/elastic — reveals must feel cinematic, not snappy
- breaks if border weight exceeds 1px — hairline rules only, or no rules at all
- breaks if surface area is filled rather than left as whitespace — empty space is structural, not residual

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers; for the hero, replace headline weight to 600 and set body copy in Tenor Sans at letter-spacing 0.01em.
Source render: no standalone upstream HTML demo — tokens direct-ported from `design-forge-main/references/discovery-framework.md` Luxury preset description (Cormorant Garamond + Tenor Sans, dark + gold, hairline borders, cinematic reveals).
Parity threshold: A-class justified (description-only upstream; no renderable HTML demo to diff against).

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling styles:** S-037 Cream Editorial (cream-first Cormorant serif but no metallic accent), S-028 Art Deco (also navy/black + gold pairing but adds geometric chevron/symmetry ornament that Luxury rejects), S-022 Minimal Pure (sovereign whitespace shared but pure black/white, no serif and no metallic), S-065 Newsprint/Warm Editorial (also serif-driven but warm cream paper not deep dark ground)
- **SKILL:** [../SKILL.md](../SKILL.md) — preset skill orchestrator
- **Catalogue:** [./catalogue.md](./catalogue.md) — routing index
- **Skeleton:** [./_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- **Source attribution:** `reports/batch9-harvest/styles-A.md` §Luxury (Stitch Preset); `design-forge-main/references/discovery-framework.md`. License MIT (inferred from source repo).

## Attribution

Token values direct-ported (Cormorant Garamond + Tenor Sans pairing, dark ground + metallic gold accent, hairline borders, zero radius, no shadows, cinematic 700ms motion) from `design-forge-main/references/discovery-framework.md` Luxury preset (a.k.a. "The Luxury"), distilled via `reports/batch9-harvest/styles-A.md`. License MIT (inferred). Original distillation by the batch9 harvest team.
