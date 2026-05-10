---
name: TECH-type-pyramid
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

# TECH-type-pyramid

## What it does

Emits a **pyramid or funnel diagram** — horizontal bands of decreasing (or
increasing) width stacked vertically. Classic use: Maslow-style priority
hierarchies, conversion funnels, Kano model tiers. Editorial HTML+SVG.

## When to use

- Ranked tiers where each tier is a subset / narrower than the one below
  it — either because fewer things qualify (priority tiers) or fewer
  users reach it (conversion drop-off).
- 3–6 tiers. Fewer reads as a simple list; more becomes indistinguishable
  per band.
- Orientation:
  - **Pyramid (base-wide):** ranked importance — the top tier is the
    rarefied few ("ship-blocking priorities").
  - **Funnel (top-wide):** conversion drop-off — the top is "visitors",
    the bottom is "paid users".

Do not use for: two-axis comparison (quadrant), sibling relationships
(tree), or sets that overlap (Venn).

## How it works

Each tier: a trapezoidal `<polygon>` whose width tapers toward the
apex. Start with the wide band at the correct end (top for funnel,
bottom for pyramid), reduce width by a fixed step per tier (80px inset
per band on a 540-wide base gives 5 tiers before the apex becomes
degenerate). Each slice is **48px tall**.

Tier labels: centred inside the band in `Geist Sans` 13px bold. For a
funnel, add the conversion rate on the right edge of each slice in
`Geist Mono` 11px `var(--muted)`. For a pyramid, a value annotation
on the right edge in `Geist Mono` 10px `var(--muted)` is optional.
Accent the focal tier; everything else in `paper-2`.

**Slices limit.** More than 6 levels pushes the bottom slice too wide
and the top too thin — split into two diagrams or switch to a bar chart.

## Minimal example

4-tier conversion funnel, accent on the paid tier:

```html
<svg width="560" height="360" viewBox="0 0 560 360"
     font-family="Geist, system-ui, sans-serif">
  <rect width="560" height="360" fill="var(--paper)"/>

  <!-- Tier 1: Visitors (widest) -->
  <polygon points="40,40 520,40 480,100 80,100"
           fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="280" y="76" text-anchor="middle" font-size="13"
        font-weight="600" fill="var(--ink)">Visitors</text>
  <text x="520" y="76" text-anchor="end" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">100%</text>

  <!-- Tier 2: Sign-ups -->
  <polygon points="80,100 480,100 440,160 120,160"
           fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="280" y="136" text-anchor="middle" font-size="13"
        font-weight="600" fill="var(--ink)">Sign-ups</text>
  <text x="480" y="136" text-anchor="end" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">18%</text>

  <!-- Tier 3: Activated -->
  <polygon points="120,160 440,160 400,220 160,220"
           fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1"/>
  <text x="280" y="196" text-anchor="middle" font-size="13"
        font-weight="600" fill="var(--ink)">Activated</text>
  <text x="440" y="196" text-anchor="end" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">7%</text>

  <!-- Tier 4: Paid (accent) -->
  <polygon points="160,220 400,220 360,280 200,280"
           fill="var(--accent)"/>
  <text x="280" y="256" text-anchor="middle" font-size="13"
        font-weight="600" fill="var(--accent-fg)">Paid</text>
  <text x="400" y="256" text-anchor="end" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--accent-fg)"
        opacity="0.9">2%</text>
</svg>
```

## Gotchas

- **Slope consistency.** Each band's left/right inset should be the same
  delta from the previous band (`40px` inset per tier in the example).
  Irregular slopes look like a drawing error.
- **Value annotation in mono muted, right-aligned.** Not bold, not
  centred. The tier name is the content; the value is supporting data.
- **Accent one tier only.** Funnel's job is to surface where drop-off
  matters — accent the tier the piece is about.
- **Don't stack text across multiple lines inside a tier.** If the label
  doesn't fit on one line, the tier name is too long — rename.

## Cross-references

- [SKILL](../SKILL.md) — 13-type table
- [TECH-type-tree](TECH-type-tree.md) — if the hierarchy is strictly parent-child
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-type-layers](TECH-type-layers.md) — if the bands are equal-width
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  abstraction layers, not narrowing tiers
- [design-system](design-system.md) — mono-value annotation convention
  > Grid · Typography · Loading the fonts · Type scale · Colour discipline · Rules · Focal node vs standard node · Connection styling · Density calibration · Coordinate-level checklist
