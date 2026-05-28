---
id: S-017
name: Corporate Bold / Enterprise Solid
aesthetic_position: material-systems
source_attribution: https://github.com/frontend-design-engineer-skill (visual-directions.md #4 Corporate Bold); https://github.com/tasteful-ui-skill (catalog.md Stripe reference)
license: MIT (inferred from source repo conventions)
---

# S-017 — Corporate Bold / Enterprise Solid

**Filename:** `skills/amw-design-system-presets/references/S-017-corporate-bold.md`
**Tracked in:** this repo (design/tasks/ is git-tracked)

## Identity

Corporate Bold is the visual grammar of high-trust B2B software: deep navy as the authority anchor, a single bold accent color (Stripe-lineage purple `#635BFF`) for calls to action and interactive state, and a clean off-white surface that communicates precision and accessibility. The typeface stack (Roboto, Open Sans, Inter) is deliberately neutral — the function of type here is information transmission, not personality expression. Every design decision serves trust before aesthetics: subtle 1px borders define component edges without adding visual weight; the shadow system is three-level but extremely flat (1px offset, 0.08 opacity); border-radius is 6px — professional without being playful. This style serves CRM platforms, developer dashboards, fintech portals, enterprise SaaS, and any product that must convey institutional reliability to a skeptical B2B buyer.

## Token block

```css
:root {
  /* Colors */
  --color-bg:          #FFFFFF;
  --color-surface:     #F8FAFC;
  --color-text:        #1A202C;
  --color-text-muted:  #718096;
  --color-primary:     #0A2540;
  --color-accent:      #635BFF;
  --color-border:      #E2E8F0;

  /* Typography */
  --font-display: 'Roboto', 'Open Sans', 'Inter', 'Arial', sans-serif;
  --font-body:    'Inter', 'Open Sans', 'Roboto', 'Helvetica Neue', sans-serif;
  --font-mono:    'Roboto Mono', 'Consolas', 'Courier New', monospace;

  /* Spacing */
  --spacing: 8px;

  /* Shape */
  --radius: 6px;

  /* Shadow */
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.10);

  /* Motion */
  --motion-duration: 150ms;
  --motion-easing:   ease;

  /* Optional brand-specific */
  --border-width: 1px;
  --color-surface-hover: #EDF2F7;
  --shadow-medium: 0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-high:   0 10px 15px rgba(0, 0, 0, 0.10);
}
```

```ts
// Tailwind theme extension
theme: {
  extend: {
    colors: {
      'corp-bg':       '#FFFFFF',
      'corp-surface':  '#F8FAFC',
      'corp-text':     '#1A202C',
      'corp-muted':    '#718096',
      'corp-navy':     '#0A2540',
      'corp-accent':   '#635BFF',
      'corp-border':   '#E2E8F0',
    },
    fontFamily: {
      display: ['Roboto', 'Open Sans', 'Inter', 'Arial', 'sans-serif'],
      body:    ['Inter', 'Open Sans', 'Roboto', 'Helvetica Neue', 'sans-serif'],
      mono:    ['Roboto Mono', 'Consolas', 'Courier New', 'monospace'],
    },
    borderRadius: {
      DEFAULT: '6px',
      sm:      '4px',
      lg:      '8px',
    },
    boxShadow: {
      subtle: '0 1px 3px rgba(0,0,0,0.10)',
      card:   '0 4px 6px rgba(0,0,0,0.07)',
      lift:   '0 10px 15px rgba(0,0,0,0.10)',
    },
  },
},
```

## "Breaks if" invariants

- breaks if a decorative serif typeface is introduced — the corporate register requires neutral sans-serif throughout; serifs read as editorial or luxury rather than enterprise
- breaks if the dark mode variant uses the same accent purple on a dark navy surface — contrast degrades below AA compliance; dark variant requires `--color-accent` lightened to `#8B87FF` or similar
- breaks if `--radius` exceeds 8px — rounded corners shift the tone from enterprise to consumer SaaS; above 8px the style begins reading as Vibrant Friendly (S-023)
- breaks if backgrounds go dark without an explicit dark-mode palette — this style is light-mode first; toggling `--color-bg` to near-black without adjusting all surface/border/text tokens creates incoherence
- breaks if the accent is switched to a warm color (amber, orange, coral) — the Stripe-lineage purple is an authority signal in B2B contexts; warm accents read as lifestyle or consumer
- breaks if shadows are removed entirely — even the near-invisible `0 1px 3px` elevation is what distinguishes cards from background; flat surfaces collapse hierarchy in dense data layouts
- breaks if border-weight increases above 1px — thick borders (2px+) shift the register from systematic to aggressive/brutalist

## Canonical render-test pointer

Render-test: inject token block into `references/_test-skeleton.html` substituting all `{{TOKEN}}` markers with the values above.
Source parity: `frontend-design-engineer-skill-main/references/visual-directions.md` (direction #4, Corporate Bold). Pay particular attention to the pricing table and form — those are where corporate density invariants are most visible.

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 107472 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- S-008 Material Design 3 — sibling in material-systems position; uses HCT tonal palette and state layers rather than flat navy+accent; use for Google-adjacent products
- S-021 Pnalism / Two-Tone Minimal — adjacent minimal corporate; stricter (zero shadows, only 2 chromatic values); use when information density must drop further
- S-022 Minimal Pure — opposing anchor; pure black/white, zero radius; use for ultra-premium utility
- Source: `frontend-design-engineer-skill-main/.../visual-directions.md` (#4 Corporate Bold); `tasteful-ui-skill-master/.../catalog.md` (Stripe reference)
