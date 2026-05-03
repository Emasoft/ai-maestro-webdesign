---
name: TECH-type-venn
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-type-venn

## What it does

Emits a **Venn diagram** — 2 or 3 overlapping circles, each representing a
set; the overlap region is called out and labelled. Editorial HTML+SVG.

## When to use

- 2 or 3 sets that overlap meaningfully, and the overlap is the point.
- Often used for positioning ("where do X, Y, Z intersect?") or feature
  comparisons ("which products cover this region?").
- NEVER use Venn for more than 3 sets — 4-circle Venns are mathematically
  ugly and visually unreadable; switch to a table or quadrant.

Do not use for: containment (nested), rank (pyramid), or two-axis
positioning (quadrant).

## How it works

2-circle Venn: two circles of equal radius (usually r=120 on a 520-wide
canvas), overlap = ~40% of each radius (`cx` centres at `(250, 260)` and
`(390, 260)`). 3-circle: centres arranged as an equilateral triangle;
each pair overlaps equally.

Circle fill: `paper-2` with `fill-opacity="0.7"` so overlaps darken
naturally. Accent one region (a single circle, or the triple intersection)
in `accent` with `fill-opacity="0.6"` so overlaps still read. Stroke:
1px `ink`.

Set labels: placed outside the circles in bold `Geist Sans` 12px. Overlap
labels: inside the overlap region, italic `Instrument Serif` 11–12px
(signalling this is the editorial take-away).

## Minimal example

2-circle Venn with accent overlap:

```html
<svg width="520" height="320" viewBox="0 0 520 320"
     font-family="Geist, system-ui, sans-serif">
  <rect width="520" height="320" fill="var(--paper)"/>

  <!-- Circle A -->
  <circle cx="200" cy="160" r="120" fill="var(--paper-2)"
          stroke="var(--ink)" stroke-width="1" fill-opacity="0.5"/>
  <text x="100" y="72" font-size="12" font-weight="600"
        fill="var(--ink)">Fast</text>

  <!-- Circle B -->
  <circle cx="320" cy="160" r="120" fill="var(--paper-2)"
          stroke="var(--ink)" stroke-width="1" fill-opacity="0.5"/>
  <text x="420" y="72" font-size="12" font-weight="600"
        fill="var(--ink)">Cheap</text>

  <!-- Overlap accent fill (clip via layered circle) -->
  <defs>
    <clipPath id="venn-clip-a">
      <circle cx="200" cy="160" r="120"/>
    </clipPath>
  </defs>
  <circle cx="320" cy="160" r="120" fill="var(--accent)"
          fill-opacity="0.35" clip-path="url(#venn-clip-a)"/>

  <!-- Overlap label -->
  <text x="260" y="164" text-anchor="middle"
        font-family="Instrument Serif, Georgia, serif"
        font-style="italic" font-size="13"
        fill="var(--ink)">Rare.</text>

  <!-- Tagline below -->
  <text x="260" y="300" text-anchor="middle" font-size="11"
        fill="var(--muted)">"Pick two" — the classic engineering trade-off</text>
</svg>
```

## Gotchas

- **Circle overlap ~40% of radius.** Too little overlap and the sets look
  disjoint; too much and they look like one blob.
- **Editorial overlap label in italic serif.** This is the signature
  "hot-take" typography cue — using `Geist Sans` in the overlap makes it
  read as a plain label instead of the essay punchline.
- **Accent the overlap or one single region.** Accenting both regions AND
  the overlap clutters. Pick the one visual focus.
- **Never more than 3 circles.** 4-set Venns require non-circular shapes
  to be mathematically correct and become unreadable in editorial
  settings.

## Cross-references

- [SKILL](../SKILL.md) — 13-type table
- [TECH-type-quadrant](TECH-type-quadrant.md) — for two-axis positioning (often a better fit
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  when users first think "Venn")
- [design-system](design-system.md) — italic serif for overlap labels
  > Grid · Typography · Loading the fonts · Type scale · Colour discipline · Rules · Focal node vs standard node · Connection styling · Density calibration · Coordinate-level checklist
- [primitive-annotation](primitive-annotation.md) — if you need an arrow pointing to a specific
  > When to use · Required SVG primitives · Canonical snippet · Parameter reference · Leader-line geometry · 4px grid still applies · Source citation
  region from outside the circles
