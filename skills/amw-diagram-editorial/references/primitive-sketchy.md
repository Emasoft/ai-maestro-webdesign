## Table of Contents

- [When to use](#when-to-use)
- [Required SVG primitives](#required-svg-primitives)
- [Canonical snippet](#canonical-snippet)
- [Parameter reference](#parameter-reference)
- [4px grid still applies](#4px-grid-still-applies)
- [Accessibility caveat](#accessibility-caveat)
- [Source citation](#source-citation)


# Primitive — Sketchy filter (hand-drawn variant)

> **Cross-type primitive.** Applies to any of the 13 editorial diagram types
> when the output context is an essay or informal post, not a technical doc.

## When to use

- **Use:** personal essays, narrative posts, talks, op-eds — anywhere the
  reader expects a hand-drawn, zine-like feel.
- **Do NOT use:** API docs, runbooks, architecture ADRs, anything a user
  might ship to a customer. The sketchy filter is deliberately imperfect;
  it corrodes credibility in contexts that demand precision.
- **Do NOT mix:** never apply the sketchy filter to SOME elements and leave
  OTHERS pristine inside the same diagram. Either the whole diagram is
  sketchy or none of it is. Mixing reads as a bug, not a style.

## Required SVG primitives

Two SVG filter nodes, always used together:

1. `<feTurbulence>` — generates fractal noise as the displacement source.
2. `<feDisplacementMap>` — maps that noise onto the source graphic's x/y
   coordinates, producing the jittered "hand-drawn" look.

## Canonical snippet

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

## Parameter reference

| Attribute | Value | Rationale |
|---|---|---|
| `baseFrequency` | `0.04` | Low frequency = large smooth wobble, not a grainy static. At `0.1+` the filter reads as noise, not hand-drawn. |
| `numOctaves` | `3` | More octaves = more fractal detail. 3 is the sweet spot — 1 is too smooth, 5+ is too busy. |
| `seed` | `2` (or any small integer) | Deterministic noise. Changing the seed produces a different "handwriting sample". Keep constant per-diagram so the look is stable. |
| `scale` (displacement) | `2.5` | The jitter magnitude in SVG user units. At 1 the effect is barely visible. At 5+ shapes tear apart. |
| `stroke-width` on nodes | `1.5` | Crisp 1px strokes become invisible under the filter; 1.5px reads correctly. The rest of the editorial diagram family uses `1px` — only sketchy nodes bump to 1.5. |
| Filter region padding (`x/y/width/height`) | `-5% / -5% / 110% / 110%` | The displacement moves pixels outside the node's bounding box; the extra 5% padding on each side prevents clipping. |

## 4px grid still applies

Even under the sketchy filter, coordinates must still snap to multiples of
4. The filter adds jitter on **render**, not on **layout**. If the source
geometry is off-grid, the filter makes that non-alignment obvious — it does
not hide it.

## Accessibility caveat

The sketchy filter degrades legibility slightly. If the diagram contains
fine detail (thin arrows, small labels, closely-spaced nodes), the filter
can push it below comfortable readability. Either:

- Increase stroke widths to 1.5–2px on filtered elements.
- Lift font sizes by 1-2pt on labels inside filtered regions.
- Drop the filter on pure-text labels even if the enclosing shapes use it.

## Source citation

Ported from `diagram-design-editorial/SKILL.md` lines 441-455 (source SKILL.md
on disk at `SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/`).
