---
id: S-063
name: Motion (The Builder)
aesthetic_position: animation-centric-magician
source_attribution: "styles-A §Motion (Stitch Preset); design-forge-main/references/discovery-framework.md. MIT (inferred from repo)."
license: MIT (direct-port)
---

# S-063 — Motion (The Builder)

**Filename:** `skills/amw-design-system-presets/references/S-063-motion-builder.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Motion — internally nicknamed "The Builder" in the Stitch preset family — is the animation-centric preset where motion is the primary information carrier, not a decoration. The visual fingerprint pairs Space Grotesk at 700 (a geometric, slightly quirky display sans with rounded terminals) for headings with Inter at 400/500 (a workhorse UI sans optimised for screen) for body. The palette is calm and accent-driven: brand colour deployed at strategic motion-anchors on either a dark or white ground, with motion (not chroma) carrying the dynamic energy. Layout is animation-centric — sections scroll-reveal in choreographed sequence, elements settle into position rather than appear, transitions replace static shadows. The shadow register itself is replaced by smooth motion: a card "settles" with a brief opacity-and-y-translation rather than sitting on a static drop. The archetype is **magician / wonder** — the visitor is meant to feel "how did they do that?" Reach for it on product launch microsites, hero-driven SaaS, agency portfolios, interactive product tours, scrollytelling articles, and any brief where the WOW factor lives in choreography rather than ornament.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  /* Colors — brand accent on dark OR white; motion replaces chroma intensity */
  --color-bg:         #0E0E10;   /* near-black ground (swap to #FFFFFF for white variant) */
  --color-surface:    #18181B;   /* lifted card surface */
  --color-text:       #FAFAFA;   /* on dark */
  --color-text-muted: #A1A1AA;   /* secondary label */
  --color-primary:    #6366F1;   /* indigo brand accent — swap to brand value */
  --color-accent:     #6366F1;   /* same — Motion uses ONE accent + motion */
  --color-border:     #27272A;   /* subtle hairline */

  /* Typography */
  --font-display: 'Space Grotesk', 'Inter', 'Helvetica Neue', sans-serif;
  --font-body:    'Inter', 'system-ui', '-apple-system', sans-serif;
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  /* Display sizing — confident but not slammed (Kinetic's territory) */
  --font-size-display:  clamp(48px, 7.5vw, 96px);
  --font-weight-display: 700;
  --font-size-body:     16px;
  --font-weight-body:   400;
  --letter-spacing-display: -0.02em;
  --line-height-display: 1.05;
  --line-height-body:    1.6;

  /* Geometry */
  --spacing:      24px;
  --radius:       12px;            /* medium-soft radius — motion-friendly cards */
  --border-width: 1px;

  /* "Shadow" is a motion endpoint, not a static drop */
  --shadow-rest:   0 1px 3px rgba(0, 0, 0, 0.12);
  --shadow-active: 0 12px 32px rgba(0, 0, 0, 0.24);  /* applied on settle/scroll-reveal */
  --shadow:        var(--shadow-rest);

  /* Motion — the entire skin's primary expression */
  --motion-duration-fast:    180ms;
  --motion-duration-default: 320ms;
  --motion-duration-slow:    560ms;
  --motion-easing:   cubic-bezier(0.22, 1, 0.36, 1);   /* smooth-out, settles in place */
  --motion-easing-spring: cubic-bezier(0.34, 1.56, 0.64, 1);  /* slight overshoot for "appear" */
  --motion-stagger:  60ms;         /* delay between sibling reveals */

  /* Scroll-reveal y-translation amount */
  --motion-reveal-y: 24px;
}
```

```js
// tailwind.config.js — theme extension
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:          '#0E0E10',
        surface:     '#18181B',
        text:        '#FAFAFA',
        'text-muted': '#A1A1AA',
        primary:     '#6366F1',
        accent:      '#6366F1',
        border:      '#27272A',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'Inter', '"Helvetica Neue"', 'sans-serif'],
        body:    ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono:    ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      borderRadius: { DEFAULT: '12px' },
      boxShadow: {
        DEFAULT: '0 1px 3px rgba(0,0,0,0.12)',
        active:  '0 12px 32px rgba(0,0,0,0.24)',
      },
      transitionDuration: {
        fast:    '180ms',
        DEFAULT: '320ms',
        slow:    '560ms',
      },
      transitionTimingFunction: {
        DEFAULT: 'cubic-bezier(0.22, 1, 0.36, 1)',
        spring:  'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
    },
  },
};
```

**White-ground variant token override:**
```css
[data-variant="white"] {
  --color-bg:      #FFFFFF;
  --color-surface: #F4F4F5;
  --color-text:    #18181B;
  --color-text-muted: #71717A;
  --color-border:  #E4E4E7;
  --shadow-rest:   0 1px 3px rgba(0, 0, 0, 0.08);
  --shadow-active: 0 12px 32px rgba(0, 0, 0, 0.14);
}
```

**Scroll-reveal CSS skeleton (the kinetic surface itself):**
```css
[data-motion-reveal] {
  opacity: 0;
  transform: translateY(var(--motion-reveal-y));
  transition: opacity var(--motion-duration-default) var(--motion-easing),
              transform var(--motion-duration-default) var(--motion-easing);
}
[data-motion-reveal].is-visible {
  opacity: 1;
  transform: translateY(0);
}
@media (prefers-reduced-motion: reduce) {
  [data-motion-reveal],
  [data-motion-reveal].is-visible { transition: none; transform: none; opacity: 1; }
}
```

## "Breaks if" invariants

- breaks if `prefers-reduced-motion: reduce` is not respected — motion-centric skins MUST collapse to static states when the user opts out, or the preset becomes inaccessible
- breaks if no scroll-reveal / settle motion is present anywhere — Motion without motion is incoherent (it would just be a generic dark-mode preset)
- breaks if a fine serif display replaces Space Grotesk — the geometric-sans display register is structural
- breaks if more than one chromatic accent is deployed at full saturation — Motion is single-accent + motion-as-second-channel
- breaks if motion durations exceed ~800ms uniformly or are linear-eased — reveals must feel smooth-out, settling, not slow-creep
- breaks if static decorative drop shadows replace the rest→active motion shadow ramp — the shadow lives during transition, not at rest
- breaks if information density is so high (>~8 elements per fold) that staggered reveals become noise rather than choreography
- breaks if `--radius` falls below 8px or exceeds 20px — medium-soft radius is the motion-friendly band

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers; wrap hero text and card row in `<div data-motion-reveal>` and toggle `.is-visible` on scroll (or use IntersectionObserver).
Source render: no standalone upstream HTML demo — tokens direct-ported from `design-forge-main/references/discovery-framework.md` Motion preset description (Space Grotesk + Inter, animation-centric, scroll-reveal, magician archetype).
Parity threshold: A-class justified (description-only upstream; no renderable HTML demo to diff against).

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 64835 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-061 Kinetic (also motion-relevant but loud / single-event slam vs. Motion's choreographed settle), S-017 Corporate Bold (also dark-with-accent but no motion-as-skin — static enterprise feel), S-024 Tech / SaaS Modern (Inter + soft radius shared but no choreographed reveals)
- **SKILL:** [../SKILL.md](../SKILL.md) — preset skill orchestrator
- **Catalogue:** [./catalogue.md](./catalogue.md) — routing index
- **Skeleton:** [./_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- **Source attribution:** `reports/batch9-harvest/styles-A.md` §Motion (Stitch Preset); `reports_dev/batch9/extracted/design-forge-main/references/discovery-framework.md`. License MIT (inferred from source repo).

## Attribution

Token values direct-ported (Space Grotesk + Inter pairing, brand accent on dark/white, animation-centric scroll-reveal, smooth-out easing with rest→active shadow ramp, 12px medium-soft radius) from `design-forge-main/references/discovery-framework.md` Motion preset (a.k.a. "The Builder"), distilled via `reports/batch9-harvest/styles-A.md`. License MIT (inferred). Original distillation by the batch9 harvest team.
