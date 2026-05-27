---
id: S-054
name: Cobalt (Bexa Accent — Technical SaaS Blue)
aesthetic_position: single-hue-accent-saas
source_attribution: "Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md (MIT); styles-A.md §Cobalt (Bexa Accent)"
license: MIT (direct-port with attribution)
---

# S-054 — Cobalt (Bexa Accent — Technical SaaS Blue)

**Filename:** `skills/amw-design-system-presets/references/S-054-cobalt.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Cobalt is one of six single-hue accent presets in the Bexa family — small, surgical palettes built around a single high-saturation accent that drops cleanly onto either a light or dark neutral surface. The Cobalt slot is the technical-SaaS blue: `hsl(221 70% 52%)`, a high-chroma medium-light blue that signals confidence, competence, and "enterprise default done right" without sliding into the cliché purple-to-blue gradient or the too-aggressive royal blue. It pairs with Geist or Inter for body text, sits inside a standard 12-column SaaS grid, takes moderate corner radius (`rounded-lg` to `rounded-xl`, i.e. 8–12px), and uses light elevation with neutral shadows. Motion is precise expo easing (no springs, no overshoot — those belong to consumer apps). Reach for it when the brief is a B2B SaaS product page, developer tool landing, technical-authority service site, or any tool whose audience expects competence rather than personality.

## Token block

The Bexa source treats every accent preset as a single `--accent` token that drops into either a light or dark neutral surface; below is the full surface scaffold around the single accent so the preset is independently usable in `_test-skeleton.html` without depending on a neutral-base preset.

```css
/* S-054 Cobalt (Bexa Accent) — token block, light surface */
:root {
  /* Colors — neutral light surface + single Cobalt accent */
  --color-bg:         #FFFFFF;        /* clean light field */
  --color-surface:    #F8FAFC;        /* cool-neutral card surface */
  --color-text:       #0F172A;        /* near-black slate */
  --color-text-muted: #475569;        /* slate-600 */
  --color-text-faint: #94A3B8;        /* slate-400 */
  --color-primary:    hsl(221 70% 52%);   /* COBALT — interactive + brand */
  --color-accent:     hsl(221 70% 42%);   /* COBALT pressed / active darker shade */
  --color-border:     #E2E8F0;        /* slate-200 hairline */

  /* Typography — technical SaaS */
  --font-display: 'Geist', 'Inter', 'system-ui', '-apple-system', sans-serif;
  --font-body:    'Geist', 'Inter', 'system-ui', '-apple-system', sans-serif;
  --font-mono:    'Geist Mono', 'JetBrains Mono', 'Fira Code', monospace;

  /* Geometry — standard SaaS card */
  --spacing:      8px;
  --radius:       12px;               /* rounded-xl midpoint; range 8–12px */
  --border-width: 1px;

  /* Shadow — light elevation, neutral */
  --shadow:       0 1px 2px rgba(15, 23, 42, 0.06);
  --shadow-card:  0 4px 12px rgba(15, 23, 42, 0.08);

  /* Motion — precise, no springs */
  --motion-duration: 200ms;
  --motion-easing:   cubic-bezier(0.22, 1, 0.36, 1);   /* expo easing */
}
```

```css
/* S-054 Cobalt — dark surface variant (drop on near-black) */
[data-theme="dark"] {
  --color-bg:         #0F172A;
  --color-surface:    #1E293B;
  --color-text:       #F1F5F9;
  --color-text-muted: #94A3B8;
  --color-text-faint: #64748B;
  --color-primary:    hsl(221 70% 62%);   /* COBALT lifted ~10% L for contrast on dark */
  --color-accent:     hsl(221 70% 52%);   /* COBALT base as accent/hover */
  --color-border:     #334155;
}
```

```js
// tailwind.config.js — theme extension (S-054)
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:           '#FFFFFF',
        surface:      '#F8FAFC',
        text:         '#0F172A',
        'text-muted': '#475569',
        'text-faint': '#94A3B8',
        primary:      'hsl(221 70% 52%)',
        accent:       'hsl(221 70% 42%)',
        border:       '#E2E8F0',
      },
      fontFamily: {
        display: ['Geist', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        body:    ['Geist', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono:    ['"Geist Mono"', '"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      borderRadius: { DEFAULT: '12px', lg: '8px', xl: '12px' },
      boxShadow: {
        DEFAULT: '0 1px 2px rgba(15,23,42,0.06)',
        card:    '0 4px 12px rgba(15,23,42,0.08)',
        none:    'none',
      },
      transitionDuration: { DEFAULT: '200ms' },
      transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.22, 1, 0.36, 1)' },
    },
  },
};
```

## "Breaks if" invariants

- breaks if a warm-toned secondary accent (rose, amber, peach, orange) is introduced alongside Cobalt — the Bexa single-hue rule is what gives the preset its identity; pairing with a warm accent collapses it into a generic SaaS palette
- breaks if Cobalt is deployed in a consumer / lifestyle / hospitality context — the cool-blue technical authority signal is wrong for warm-audience brands (use S-051 Beauty/Spa, S-053 Restaurant, or a Bexa warm accent like S-056 Ember instead)
- breaks if Cobalt lightness drops below 40% (becomes royal/navy — too heavy, slips toward S-017 Corporate Bold) or rises above 65% (becomes sky/baby — slips toward consumer pastel)
- breaks if Cobalt chroma falls below 55% saturation — becomes desaturated slate, which has its own visual language (often legal/finance) and dilutes the technical-SaaS-confidence signal
- breaks if motion is set to spring easing or has bounce/overshoot — the preset's motion contract is precise expo easing only; springs are a consumer-app cue and conflict with the technical-authority read
- breaks if border-radius exceeds 16px (over-rounded, consumer-app feel) or falls to 0 (industrial-stiff, wrong category)
- breaks if the typography pairing flips to serif (Cormorant, Lora, Source Serif 4) — Cobalt's technical-SaaS context requires a clean sans-serif (Geist/Inter); serif breaks the category
- breaks if the page uses the canonical AI-slop purple→blue gradient or any large background gradient on the Cobalt accent — Cobalt is a solid-fill accent by design

## Canonical render-test pointer

Render-test: inject the token block above into `skills/amw-design-system-presets/references/_test-skeleton.html`, substituting all `{{TOKEN}}` markers. The HSL values are accepted directly by every modern browser.
Upstream parity source: `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` (MIT) — the `--accent: hsl(221 70% 52%)` token is direct-ported from the source repo's Cobalt accent definition. The surface scaffold (neutral background, slate text, light elevation) is reconstructed from Bexa's documented "technical SaaS context, 12-col grid, light elevation, expo easing" guidance.

## Render-test verdict

JOD: pending

## Cross-references

- **Sibling Bexa single-hue presets:** S-055 Verdant (`hsl(158 58% 40%)` — growth/sustainability green), S-056 Ember (`hsl(22 90% 50%)` — energy/CTA orange), S-057 Plum (`hsl(276 60% 50%)` — creative/ML purple), S-058 Rose Smoke (`hsl(348 62% 46%)` — fashion/beauty rose), S-059 Sable (`hsl(220 12% 22%)` — luxury editorial dark-first) — same single-hue contract, different industry targeting
- **Adjacent blue presets:** S-017 Corporate Bold (deep navy `#0A2540` + Stripe purple accent — heavier, B2B fintech, multi-chromatic); S-047 Electric Blue Modern (`oklch(0.55 0.22 255)` — modern industry-themed sibling using oklch rather than hsl)
- **Source attribution:** `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` (MIT, Bexa contributors); `reports/batch9-harvest/styles-A.md` §Cobalt (Bexa Accent); `reports/batch9-analysis/MASTER-LEDGER.md` row S-054

## Attribution

The Cobalt accent value (`hsl(221 70% 52%)`) is direct-ported from the Bexa skill under its MIT license, with attribution to the Bexa contributors. The surrounding surface tokens are conventional SaaS-neutral defaults reconstructed from Bexa's documented context (technical SaaS, 12-col grid, light elevation, expo easing); no other source code is copied verbatim.
