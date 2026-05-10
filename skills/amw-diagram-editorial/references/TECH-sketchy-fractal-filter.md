---
name: TECH-sketchy-fractal-filter
category: editorial-noise
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Browser-support caveat](#browser-support-caveat)
- [Cross-references](#cross-references)

# TECH-sketchy-fractal-filter

## What it does

Applies a **hand-drawn / sketchy** appearance to any editorial diagram
using two SVG filter primitives — `<feTurbulence>` for fractal noise,
`<feDisplacementMap>` to jitter pixel positions per that noise. The
effect is uniform wobble applied to every stroke and fill inside the
filtered region, reading as "sketchbook" rather than "Photoshop rough".

## When to use

- **Personal essays, narrative posts, talks, op-eds.** Anywhere the
  reader expects a hand-drawn, zine-like feel.
- **Informal docs** — retros, personal blog diagrams.
- **Never** apply to API docs, runbooks, ADRs, or customer-shippable
  artifacts. The sketchy filter is deliberately imperfect; it corrodes
  credibility in contexts that demand precision.
- **Never mix** — either the whole diagram is sketchy or none of it is.
  Applying the filter to some elements and leaving others pristine reads
  as a bug, not a style.

## How it works

Two SVG filter nodes always used together:

1. `<feTurbulence type="fractalNoise">` — generates fractal noise as
   displacement source. Fixed `seed` keeps the "handwriting sample"
   stable per diagram.
2. `<feDisplacementMap>` — maps that noise onto the source graphic's
   x/y coordinates, producing the jittered hand-drawn look.

Parameters (from [primitive-sketchy](primitive-sketchy.md)):

| Attribute | Value | Rationale |
|---|---|---|
| `baseFrequency` | `0.04` | Low frequency = large smooth wobble, not grainy static |
| `numOctaves` | `3` | Sweet spot between too smooth (1) and too busy (5+) |
| `seed` | `2` (or any small int) | Deterministic noise per diagram |
| `scale` | `2.5` | Jitter magnitude in SVG user units |
| stroke-width on filtered | `1.5` | Crisp 1px disappears under the filter |
| filter region padding | `-5% / -5% / 110% / 110%` | Prevents edge clipping |

## Minimal example

Attributed to `diagram-design-editorial/SKILL.md` lines 441-455:

```html
<defs>
  <filter id="sketchy" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.04"
                  numOctaves="3" seed="2" result="noise"/>
    <feDisplacementMap in="SourceGraphic" in2="noise"
                       scale="2.5" xChannelSelector="R"
                       yChannelSelector="G"/>
  </filter>
</defs>

<!-- Apply to any element -->
<rect x="100" y="100" width="160" height="48" rx="6"
      fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1.5"
      filter="url(#sketchy)"/>
```

## Gotchas

- **4px grid still applies.** The filter adds jitter on render, not on
  layout. Off-grid source geometry becomes MORE obvious, not less.
- **Bump stroke-width to 1.5px** on filtered elements. 1px strokes become
  invisible under the filter; the rest of the editorial family uses 1px,
  so this is a local exception.
- **Fix the `seed`.** Randomising the seed between diagrams looks
  unintentional; each diagram gets one consistent "handwriting sample".
- **Accessibility degrades.** The filter pushes small labels and thin
  arrows below comfortable readability. Either:
  - Increase stroke widths to 1.5–2px on filtered elements
  - Lift font sizes by 1-2pt on labels inside filtered regions
  - Drop the filter on pure-text labels even inside filtered shapes
- **No half-measures.** Mixing sketchy with pristine in the same diagram
  reads as a bug. All-or-nothing per diagram.

## Browser-support caveat

The filter primitives are SVG 1.1 standard and render correctly in every
modern browser. Some aggressive ad-blockers or accessibility tools strip
SVG filters — if a diagram renders pristine in such a context, that is a
graceful degradation, not a failure.

## Cross-references

- [SKILL](../SKILL.md) — Primitives section
- [primitive-sketchy](primitive-sketchy.md) — full primitive spec with browser-support notes
  > When to use · Required SVG primitives · Canonical snippet · Parameter reference · 4px grid still applies · Accessibility caveat · Source citation
- [TECH-four-px-grid-snap](TECH-four-px-grid-snap.md) — grid rule that still applies
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [design-system](design-system.md) — standard 1px stroke convention (this primitive
  > Grid · Typography · Loading the fonts · Type scale · Colour discipline · Rules · Focal node vs standard node · Connection styling · Density calibration · Coordinate-level checklist
  overrides to 1.5px locally)
- [SKILL](../../amw-ascii-diagrams-reference/SKILL.md) — ASCII alternative for
  contexts that need to look even more casual
