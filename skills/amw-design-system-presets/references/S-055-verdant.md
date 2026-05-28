---
id: S-055
name: Verdant (Bexa Accent — Growth / Sustainability Green)
aesthetic_position: single-hue-accent-saas
source_attribution: "Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md (MIT); styles-A.md §Verdant (Bexa Accent)"
license: MIT (direct-port with attribution)
---

# S-055 — Verdant (Bexa Accent — Growth / Sustainability Green)

**Filename:** `skills/amw-design-system-presets/references/S-055-verdant.md`
**Tracked in:** this repo (skills/amw-design-system-presets/references/ is git-tracked)

## Identity

Verdant is the growth-and-sustainability accent in the Bexa single-hue family — `hsl(158 58% 40%)`, a mid-green that sits between teal and forest, carrying enough chroma to read as alive and enough darkness to read as serious. It is the accent for fintech-forward sustainability platforms, climate-tech SaaS, plant-care products, healthy-eating brands, and any product whose audience must trust the message of long-term growth without slipping into either neon eco-cliché or institutional-finance heaviness. The accent pairs cleanly with Geist, Inter, or Plus Jakarta Sans, drops onto a feature-grid + pricing SaaS structure, takes `rounded-xl` cards (~12px radius), uses standard light elevation, and carries one signature motion cue from the Bexa source: a status-ping animation pairs naturally with a MeshGradient background variant on the hero. Reach for it when the brief is a sustainability product, fintech with a growth narrative, climate startup, agtech, plant-care commerce, or any SaaS whose category requires nature-as-trust rather than tech-blue authority.

## Token block

The Bexa source treats every accent preset as a single `--accent` token that drops onto a light or dark neutral surface; the block below provides the full surface scaffold around the Verdant accent so the preset is independently usable in `_test-skeleton.html`.

```css
/* S-055 Verdant (Bexa Accent) — token block, light surface */
:root {
  /* Colors — neutral light surface + single Verdant accent */
  --color-bg:         #FFFFFF;        /* clean light field */
  --color-surface:    #F8FAFC;        /* cool-neutral card surface (shared scaffold w/ S-054) */
  --color-text:       #0F172A;        /* near-black slate */
  --color-text-muted: #475569;        /* slate-600 */
  --color-text-faint: #94A3B8;        /* slate-400 */
  --color-primary:    hsl(158 58% 40%);   /* VERDANT — interactive + brand */
  --color-accent:     hsl(158 58% 30%);   /* VERDANT pressed / active darker shade */
  --color-border:     #E2E8F0;        /* slate-200 hairline */

  /* Typography — SaaS sans-serif */
  --font-display: 'Geist', 'Inter', 'Plus Jakarta Sans', 'system-ui', sans-serif;
  --font-body:    'Geist', 'Inter', 'Plus Jakarta Sans', 'system-ui', sans-serif;
  --font-mono:    'Geist Mono', 'JetBrains Mono', 'Fira Code', monospace;

  /* Geometry — standard SaaS card */
  --spacing:      8px;
  --radius:       12px;               /* rounded-xl */
  --border-width: 1px;

  /* Shadow — light elevation, neutral */
  --shadow:       0 1px 2px rgba(15, 23, 42, 0.06);
  --shadow-card:  0 4px 12px rgba(15, 23, 42, 0.08);

  /* Motion — status ping + MeshGradient background pair from Bexa source */
  --motion-duration: 200ms;
  --motion-easing:   cubic-bezier(0.22, 1, 0.36, 1);   /* expo easing */
  --motion-ping-duration: 1500ms;                       /* status-ping cadence */
}

/* Bexa-documented status-ping animation (companion to the accent) */
@keyframes status-ping {
  0%   { transform: scale(1);   opacity: 0.75; }
  75%  { transform: scale(1.6); opacity: 0;    }
  100% { transform: scale(1.6); opacity: 0;    }
}
.status-ping {
  background: var(--color-primary);
  animation: status-ping var(--motion-ping-duration) cubic-bezier(0, 0, 0.2, 1) infinite;
}
```

```css
/* S-055 Verdant — dark surface variant (drop on near-black) */
[data-theme="dark"] {
  --color-bg:         #0F172A;
  --color-surface:    #1E293B;
  --color-text:       #F1F5F9;
  --color-text-muted: #94A3B8;
  --color-text-faint: #64748B;
  --color-primary:    hsl(158 58% 50%);   /* VERDANT lifted ~10% L for contrast on dark */
  --color-accent:     hsl(158 58% 40%);   /* VERDANT base as accent/hover */
  --color-border:     #334155;
}
```

```js
// tailwind.config.js — theme extension (S-055)
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:           '#FFFFFF',
        surface:      '#F8FAFC',
        text:         '#0F172A',
        'text-muted': '#475569',
        'text-faint': '#94A3B8',
        primary:      'hsl(158 58% 40%)',
        accent:       'hsl(158 58% 30%)',
        border:       '#E2E8F0',
      },
      fontFamily: {
        display: ['Geist', 'Inter', '"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
        body:    ['Geist', 'Inter', '"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
        mono:    ['"Geist Mono"', '"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      borderRadius: { DEFAULT: '12px', xl: '12px' },
      boxShadow: {
        DEFAULT: '0 1px 2px rgba(15,23,42,0.06)',
        card:    '0 4px 12px rgba(15,23,42,0.08)',
        none:    'none',
      },
      transitionDuration: { DEFAULT: '200ms' },
      transitionTimingFunction: { DEFAULT: 'cubic-bezier(0.22, 1, 0.36, 1)' },
      keyframes: {
        'status-ping': {
          '0%':   { transform: 'scale(1)',   opacity: '0.75' },
          '75%':  { transform: 'scale(1.6)', opacity: '0' },
          '100%': { transform: 'scale(1.6)', opacity: '0' },
        },
      },
      animation: {
        'status-ping': 'status-ping 1500ms cubic-bezier(0, 0, 0.2, 1) infinite',
      },
    },
  },
};
```

## "Breaks if" invariants

- breaks if a cold-blue secondary accent is introduced alongside Verdant — the Bexa single-hue rule is what gives the preset its identity; pairing with blue tilts the page back into S-054 Cobalt territory and collapses the growth/sustainability signal
- breaks if Verdant chroma is lifted high enough that it reads as neon lime — Bexa explicitly warns against "neon lime that pushes into cheap territory"; chroma above ~70% saturation crosses this line
- breaks if Verdant lightness drops below 30% — becomes forest/conservative-emerald (closer to S-052 Real Estate / Stable Growth), losing the "growth-forward" cue
- breaks if Verdant lightness rises above 55% — becomes mint/pastel (consumer-wellness territory), losing the SaaS context
- breaks if motion uses spring easing or bounce — Bexa's contract is expo easing; the status-ping animation is the one approved motion cue
- breaks if border-radius exceeds 16px (over-rounded consumer feel) or falls to 0 (industrial — wrong category)
- breaks if the typography pairing flips to serif (Cormorant, Lora, Source Serif 4) — Verdant's SaaS context requires sans-serif (Geist / Inter / Plus Jakarta Sans)
- breaks if a warm secondary accent (orange, amber, rose, peach) is introduced — Bexa accent presets are single-hue by definition; introducing a warm counterpart collapses the contract

## Canonical render-test pointer

Render-test: inject the token block above into `skills/amw-design-system-presets/references/_test-skeleton.html`, substituting all `{{TOKEN}}` markers. The HSL values, the `@keyframes status-ping` block, and the motion tokens are accepted directly by every modern browser.
Upstream parity source: `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` (MIT) — the `--accent: hsl(158 58% 40%)` token is direct-ported from the source repo's Verdant accent definition, and the status-ping animation is direct-ported from the same source. The surrounding surface scaffold is reconstructed from Bexa's documented "feature-grid + pricing SaaS structure, light elevation, expo easing" guidance.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 122011 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling Bexa single-hue presets:** S-054 Cobalt (`hsl(221 70% 52%)` — technical SaaS blue), S-056 Ember (`hsl(22 90% 50%)` — energy/CTA orange), S-057 Plum (`hsl(276 60% 50%)` — creative/ML purple), S-058 Rose Smoke (`hsl(348 62% 46%)` — fashion/beauty rose), S-059 Sable (`hsl(220 12% 22%)` — luxury editorial dark-first) — same single-hue contract, different industry targeting
- **Adjacent green presets:** S-052 Real Estate / Stable Growth (oklch deep emerald `oklch(0.45 0.15 145)` — darker, narrower industry targeting, paper-warm surface); S-048 Healthcare/Medical (oklch teal `oklch(0.55 0.13 195)` — adjacent hue zone but cooler, medical context)
- **Source attribution:** `Bexa-professional-frontend-design-skills-for-ai-agents-main/skills/bexa/SKILL.md` (MIT, Bexa contributors); `reports/batch9-harvest/styles-A.md` §Verdant (Bexa Accent); `reports/batch9-analysis/MASTER-LEDGER.md` row S-055

## Attribution

The Verdant accent value (`hsl(158 58% 40%)`) and the companion `status-ping` keyframe animation are direct-ported from the Bexa skill under its MIT license, with attribution to the Bexa contributors. The surrounding surface tokens are conventional SaaS-neutral defaults reconstructed from Bexa's documented context (feature-grid + pricing SaaS, light elevation, expo easing); no other source code is copied verbatim.
