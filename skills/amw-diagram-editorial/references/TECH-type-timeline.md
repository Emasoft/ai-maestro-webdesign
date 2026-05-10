---
name: TECH-type-timeline
category: editorial-layout
source: SKILLS-TO-INTEGRATE/diagrams-skills/diagram-design-editorial/SKILL.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/cc-plugin-text-visualizations-main.zip
---

# TECH-type-timeline

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Emits a **timeline diagram** — events arranged in temporal order along a
horizontal or vertical axis, each event represented by a marker + date +
label. Editorial HTML+SVG. Best for historical sequences, product
roadmaps, case-study turning points.

## When to use

- Events are ordered in time and the **gap between them** matters (vs. a
  simple list where order is all that matters).
- 5–12 events. Fewer than 5 reads as a list; more than 12 becomes too
  dense and should split into eras or phases.
- Axis is time-linear (or logarithmic if the range is orders of magnitude,
  but that is rare enough to be a separate technique).

Do not use for: state transitions (state machine), unordered categories
(treat as a table), or "steps" in a recipe (that's a list).

## How it works

Horizontal axis (default): a single 1px `ink` line near the middle of the
canvas, with short tick marks at each event's x coordinate. Event
markers: filled circles on the axis (accent-coloured for the 1-2 focal
events, `ink` for the rest). Event labels alternate above and below the
axis to prevent collisions. Dates sit immediately adjacent to the marker
in `Geist Mono` muted 10px; titles in `Geist Sans` 12px; optional
one-line description below title in muted 10px.

Vertical axis variant: same primitives rotated 90°; useful when the labels
are long (more horizontal space per event).

## Minimal example

Horizontal timeline, one accent event:

```html
<svg width="640" height="240" viewBox="0 0 640 240"
     font-family="Geist, system-ui, sans-serif">
  <rect width="640" height="240" fill="var(--paper)"/>

  <!-- Axis line -->
  <line x1="40" y1="120" x2="600" y2="120"
        stroke="var(--ink)" stroke-width="1"/>

  <!-- Event 1 (below) -->
  <line x1="80" y1="116" x2="80" y2="124"
        stroke="var(--ink)" stroke-width="1"/>
  <circle cx="80" cy="120" r="4" fill="var(--ink)"/>
  <text x="80" y="148" text-anchor="middle" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">Jan 2021</text>
  <text x="80" y="166" text-anchor="middle" font-size="12"
        fill="var(--ink)">MVP launched</text>

  <!-- Event 2 (above, accent) -->
  <circle cx="240" cy="120" r="6" fill="var(--accent)"/>
  <text x="240" y="96" text-anchor="middle" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">Jun 2022</text>
  <text x="240" y="80" text-anchor="middle" font-size="12"
        font-weight="600" fill="var(--ink)">Series A</text>

  <!-- Event 3 (below) -->
  <line x1="400" y1="116" x2="400" y2="124"
        stroke="var(--ink)" stroke-width="1"/>
  <circle cx="400" cy="120" r="4" fill="var(--ink)"/>
  <text x="400" y="148" text-anchor="middle" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">Q4 2023</text>
  <text x="400" y="166" text-anchor="middle" font-size="12"
        fill="var(--ink)">10k customers</text>

  <!-- Event 4 (above) -->
  <circle cx="560" cy="120" r="4" fill="var(--ink)"/>
  <text x="560" y="96" text-anchor="middle" font-size="10"
        font-family="'Geist Mono', monospace" fill="var(--muted)">2025</text>
  <text x="560" y="80" text-anchor="middle" font-size="12"
        fill="var(--ink)">Profitable</text>
</svg>
```

## Gotchas

- **X coordinates must encode the actual gaps.** If Jun 2022 → Q4 2023 is
  18 months and Q4 2023 → 2025 is 15 months, those two gaps should be
  visually proportional. "Evenly spaced along the axis" defeats the whole
  point of a timeline — use a list instead.
- **Alternate above/below to prevent label collision.** Never stack two
  labels on the same side of the axis unless they are at least ~120px
  apart.
- **Dates in mono, titles in sans.** The mono date block is the timeline's
  signature look; sans dates make it look like a bullet list.
- **Accent one event, maybe two.** The turning point the piece is about.

## Cross-references

- [SKILL](../SKILL.md) — 13-type table
- [TECH-type-state-machine](TECH-type-state-machine.md) — if the "events" are really state
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  transitions, that's a different primitive
- [SKILL](../../amw-text-visual-retro/SKILL.md) — ASCII timeline cousin for retros
  and milestone docs
- [design-system](design-system.md) — mono-date convention
  > Grid · Typography · Loading the fonts · Type scale · Colour discipline · Rules · Focal node vs standard node · Connection styling · Density calibration · Coordinate-level checklist
