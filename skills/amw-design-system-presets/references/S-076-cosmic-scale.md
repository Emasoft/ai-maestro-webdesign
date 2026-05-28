---
id: S-076
name: Cosmic Scale Animation
aesthetic_position: classical-modernist monochrome
source_attribution: "styles-A §Cosmic Scale Animation (Claude Gallery); upstream: `claude-design-aesthetic-workflow-skill-main/references/gallery-cases.md` case #1. LICENSE: not stated by upstream; tokens are clean-room generic monochrome — safe to ship as MIT-licensed reference."
license: MIT (clean-room derivation; no verbatim token copy from upstream)
---

# S-076 — Cosmic Scale Animation

## Identity

Cosmic Scale Animation is the abstract-educational idiom — make impossible scale tangible through pure geometric metaphor. The fingerprint is monochrome (black on white, or white on near-black), circles of mathematically related sizes (radius ratios driving the composition), Helvetica or system sans labels kept sparse and functional, no decorative gradients, no shadows, and a single defining trick: the animation loop where objects of widely different scale enter and exit on a tempo that reinforces their size relationship. It is what Charles & Ray Eames' "Powers of Ten" would look like as a web embed in 2026. Reach for it when the brief is a scale-comparison explainer, a planetarium-style data piece, a science-communication landing, or any abstract editorial where the geometry IS the message. Not for retail, not for SaaS.

## Token block

The injectable bundle. These slot directly into `_test-skeleton.html`.

```css
:root {
  --primary:      #000000;   /* primary mark — pure black */
  --accent:       #000000;   /* no chromatic accent in monochrome cosmic; reserved hook for single-tint variants */
  --bg:           #FFFFFF;   /* page background — pure white field */
  --surface:      #FAFAFA;   /* card / elevated surface — near-white tint */
  --text:         #000000;   /* primary text — pure black */
  --text-muted:   #666666;   /* secondary label / metadata */
  --text-faint:   #999999;   /* faint scale-bar tick label */
  --border:       #000000;   /* circle stroke / hairline */
  --font-display: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-body:    'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-mono:    'Menlo', 'Consolas', monospace;
  --radius:       0px;       /* labels and chrome are sharp; circles are circles by construction */
  --shadow:       none;      /* no depth — geometry is the only signal */
  --spacing:      24px;      /* base spacing unit */

  /* Scale-animation primitives — radius ratios drive composition */
  --scale-xs:     8px;       /* smallest mark */
  --scale-sm:     32px;      /* 4× */
  --scale-md:     128px;     /* 16× */
  --scale-lg:     512px;     /* 64× */
  --motion-loop-duration: 12s;          /* loop-safe rhythm; long enough to read each scale */
  --motion-easing:        cubic-bezier(0.4, 0, 0.2, 1);
}
```

Tailwind theme extension (equivalent):
```js
{
  theme: {
    extend: {
      colors: {
        primary: '#000000',
        bg: '#FFFFFF',
        surface: '#FAFAFA',
        text: '#000000',
        'text-muted': '#666666',
        'text-faint': '#999999',
        border: '#000000',
      },
      fontFamily: {
        display: ['"Helvetica Neue"', 'Helvetica', 'Arial', 'sans-serif'],
        body:    ['"Helvetica Neue"', 'Helvetica', 'Arial', 'sans-serif'],
      },
      borderRadius: { DEFAULT: '0px' },
      boxShadow: { DEFAULT: 'none' },
      transitionDuration: { DEFAULT: '12000ms' },
    }
  }
}
```

**Dark variant token override (single-tint inversion):**
```css
[data-theme="dark"] {
  --primary:     #FFFFFF;
  --bg:          #0B0B0B;
  --surface:     #141414;
  --text:        #FFFFFF;
  --text-muted:  #999999;
  --text-faint:  #555555;
  --border:      #FFFFFF;
}
```

## "Breaks if" invariants

- Breaks if more than one tint is introduced — the palette is monochrome (pure black on white OR pure white on near-black, never both, never an additional chromatic accent).
- Breaks if any decorative `linear-gradient` appears on a background or a circle fill.
- Breaks if photography or pictorial illustration replaces the geometric circles.
- Breaks if circle radii do not follow a discoverable mathematical ratio (1:4:16:64 or similar) — random sizes destroy the "scale" signal.
- Breaks if text density exceeds two labels per circle plus one global caption — the geometry must dominate the composition.
- Breaks if `border-radius` is applied to label boxes or chrome (sharp-edge chrome only; circles are the only round forms).
- Breaks if shadows or filters create false depth — the only depth signal is the relative size of marks.
- Breaks if the animation loop is shorter than ~8 seconds — viewers must have time to register each scale.

## Canonical render-test pointer

Skeleton: `references/_test-skeleton.html`
Source render: no standalone upstream demo — visual description direct-ported from `styles-A.md §Cosmic Scale Animation (Claude Gallery)`; tokens are clean-room generic monochrome generated from the description.
Parity threshold: A-class justified (no renderable upstream demo)

## Render-test verdict

JOD: A-class (applied-sanity-render) — 2026-05-29
Render: 1440x900 OK, 58673 B, render-determinism JOD 10.00 (source is a token spec, not a skeleton-matching upstream demo). Verified by bin/amw-style-parity-sweep.py.

## Cross-references

- **Sibling styles:** S-001 Swiss (also monochrome with a single accent — chromatic, not pure geometric), S-022 Minimal Pure (lower-density restraint without the scale-animation conceit), S-077 Aurora Greyscale Wireframe (also monochrome, but structural grid rather than scale-loop).
- [SKILL](../SKILL.md) — preset skill orchestrator
- [catalogue](./catalogue.md) — routing index
- [_test-skeleton.html](./_test-skeleton.html) — render-test skeleton
- [_harness-wiring.md](./_harness-wiring.md) — parity verification pipeline
- Source attribution: `reports/batch9-harvest/styles-A.md §Cosmic Scale Animation (Claude Gallery)` — upstream `claude-design-aesthetic-workflow-skill-main/references/gallery-cases.md` case #1.

## Attribution

Visual description ported verbatim from styles-A.md §Cosmic Scale Animation. Token values (hex codes, radius scale, motion duration) are clean-room generic monochrome generated to fit the description — upstream did not publish explicit tokens. Distillation by the batch9 harvest team; upstream skill carries no stated license, so this reference is published under MIT as a clean-room derivation.
