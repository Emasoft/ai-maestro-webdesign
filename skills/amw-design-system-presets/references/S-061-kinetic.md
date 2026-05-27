---
id: S-061
name: Kinetic
aesthetic_position: avant-garde-motion-driven
source_attribution: "styles-A §Kinetic (Stitch Preset); design-forge-main/references/discovery-framework.md. MIT (inferred from repo)."
license: MIT (direct-port)
---

# S-061 — Kinetic

**Filename:** `skills/amw-design-system-presets/references/S-061-kinetic.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Kinetic is the "concert main-stage" preset — bold, rebellious, energetic, sized for brands that lead with attitude rather than restraint. The visual fingerprint pairs Cabinet Grotesk at 800/900 (a sharp display grotesque) with Satoshi at 400/500 (a clean working body), drops them onto either an ink-dark or pure-white ground, and lets a single high-saturation primary accent (electric magenta, traffic yellow, or cobalt) carry the emotional load. Layout is motion-driven: sections reveal on scroll, content slides in laterally, headlines slam into place. Borders are bold structural shapes — diagonal cuts, hard rectangles, full-bleed colour fields — and the "shadow" register is replaced by motion trails (short-lived offset duplicates, opacity ghosts). Reach for it on launch pages, music/event marketing, edgy startup hero sections, agency reels, and any brief that asks for "loud confidence" rather than "quiet authority."

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  /* Colors — high-saturation accent on dark or white ground */
  --color-bg:         #0A0A0A;   /* ink black ground (swap to #FFFFFF for white variant) */
  --color-surface:    #141414;   /* near-black surface — barely lifted */
  --color-text:       #FFFFFF;   /* on dark ground */
  --color-text-muted: #9A9A9A;   /* secondary label */
  --color-primary:    #FF2D55;   /* electric magenta — swap to #FFEC00 (traffic yellow) or #0066FF (cobalt) */
  --color-accent:     #FF2D55;   /* same as primary — Kinetic uses one accent, not two */
  --color-border:     #FFFFFF;   /* bold structural rule (matches text colour on dark) */

  /* Typography */
  --font-display: 'Cabinet Grotesk', 'Inter', 'Helvetica Neue', sans-serif;
  --font-body:    'Satoshi', 'Inter', 'system-ui', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  /* Display sizing — Kinetic runs hot */
  --font-size-display:  clamp(64px, 12vw, 180px);
  --font-weight-display: 900;
  --font-size-body:     16px;
  --font-weight-body:   400;
  --letter-spacing-display: -0.04em;  /* tight, slammed-together */
  --line-height-display: 0.92;

  /* Geometry */
  --spacing:      24px;
  --radius:       0px;             /* zero radius — bold structural shapes */
  --border-width: 2px;             /* heavier than minimalist 1px */

  /* "Shadows" replaced by motion trails */
  --shadow:       none;            /* no decorative drops */
  --motion-trail: 0 0 0 transparent; /* used as a transition target, not a static state */

  /* Motion — fast, velocity-driven */
  --motion-duration: 220ms;
  --motion-easing:   cubic-bezier(0.16, 1, 0.3, 1);  /* expo-out — slams into place */
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#0A0A0A',
        surface:     '#141414',
        text:        '#FFFFFF',
        'text-muted': '#9A9A9A',
        primary:     '#FF2D55',
        accent:      '#FF2D55',
        border:      '#FFFFFF',
      },
      fontFamily: {
        display: ['"Cabinet Grotesk"', 'Inter', '"Helvetica Neue"', 'sans-serif'],
        body:    ['Satoshi', 'Inter', 'system-ui', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      borderRadius: { DEFAULT: '0px' },
      borderWidth:  { DEFAULT: '2px' },
      boxShadow:    { DEFAULT: 'none' },
      transitionDuration: { DEFAULT: '220ms' },
      transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.16, 1, 0.3, 1)' },
      letterSpacing: { display: '-0.04em' },
    },
  },
};
```

**White-ground variant token override:**
```css
[data-variant="white"] {
  --color-bg:      #FFFFFF;
  --color-surface: #F4F4F4;
  --color-text:    #0A0A0A;
  --color-text-muted: #5A5A5A;
  --color-border:  #0A0A0A;
}
```

## "Breaks if" invariants

- breaks if `border-radius` exceeds 0px — Kinetic is built on hard structural rectangles and diagonals
- breaks if a serif display font replaces Cabinet Grotesk (or equivalent heavy grotesque); fine serif is the literal opposite emotional register
- breaks if more than one chromatic accent appears at full saturation on the page — Kinetic uses one
- breaks if transition durations exceed ~350ms or easing curves are linear/ease-in (motion must feel velocity-driven, decelerating)
- breaks if decorative drop shadows are introduced — the "shadow" register is reserved for motion trails / ghosts
- breaks if accent coverage drops below ~5% of visible surface — Kinetic needs at least one loud chromatic moment per fold
- breaks if display weight drops below 800 — Cabinet Grotesk 800/900 is structural, not stylistic
- breaks if quiet/restrained colour palettes (cream, dust, sage) replace the high-saturation accent on dark/white

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers; replace the hero headline weight to 900 and accent fill to `var(--color-primary)`.
Source render: no standalone upstream HTML demo — tokens direct-ported from `design-forge-main/references/discovery-framework.md` Kinetic preset description (Cabinet Grotesk + Satoshi, "The Startup" archetype, motion-driven layout).
Parity threshold: A-class justified (description-only upstream; no renderable HTML demo to diff against).

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling styles:** S-022 Minimal Pure (the opposite emotional register — quiet, single typeface, no motion), S-041 Bauhaus (also grid-heavy and 0 radius but uses primary RYB triad instead of single high-sat accent), S-063 Motion / The Builder (animation-centric but with brand-accent calm vs. Kinetic's rebel energy)
- **SKILL:** [../SKILL.md](../SKILL.md) — preset skill orchestrator
- **Catalogue:** [./catalogue.md](./catalogue.md) — routing index
- **Skeleton:** [./_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- **Source attribution:** `reports/batch9-harvest/styles-A.md` §Kinetic (Stitch Preset); `design-forge-main/references/discovery-framework.md`. License MIT (inferred from source repo).

## Attribution

Token values direct-ported (Cabinet Grotesk + Satoshi pairing, motion-driven layout, high-saturation single accent, zero radius, fast velocity-driven motion) from `design-forge-main/references/discovery-framework.md` Kinetic preset, distilled via `reports/batch9-harvest/styles-A.md`. License MIT (inferred). Original distillation by the batch9 harvest team.
