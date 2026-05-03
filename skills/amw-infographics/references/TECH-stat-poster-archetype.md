---
name: TECH-stat-poster-archetype
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/layout-patterns.md
---

# Archetype 4: Stat Poster

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [The shape](#the-shape)
- [CSS implementation](#css-implementation)
- [The number-first rule](#the-number-first-rule)
- [Tabular numerics mandatory](#tabular-numerics-mandatory)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Oversized numbers / stats dominate the canvas. Minimal supporting
text. Bold, immediate impact. The hero stat takes 35-40% of canvas
height; everything else orbits it.

## When to use

- Single-metric stories: "$4.2M raised in 14 days"
- Sale stats, KPI announcements, milestone posters
- Any piece where one number IS the story

Example reference: `stats.png`.

## The shape

```
┌────────────────────────────────────────┐
│  HEADER (logo + context label)         │
│                                        │
│         ████████████████               │
│              $4.2M                     │  ← hero stat (35–40% of canvas)
│         TOTAL RAISED                   │
│                                        │
│  ┌─────────┬─────────┬─────────┐       │
│  │ 1,240   │  92%    │  14 days│       │
│  │investors│ sold    │ to close│       │
│  └─────────┴─────────┴─────────┘       │
│                                        │
│  FOOTER                                │
└────────────────────────────────────────┘
```

## CSS implementation

```css
/* source: image-generation/create-infographics/resources/layout-patterns.md */
.stat-poster-layout {
  display: grid;
  grid-template-rows: auto 1fr auto auto;
  gap: 0;
  min-height: 100%;
}

.stat-stage {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  gap: 8px;
}

.hero-number {
  font-family: var(--font-display);
  font-size: clamp(4rem, 18vw, 10rem);
  font-weight: 800;
  line-height: 0.9;
  letter-spacing: -0.04em;
  color: var(--primary);
  text-align: center;
  font-variant-numeric: tabular-nums;
  text-shadow: 0 0 40px rgba(var(--primary-rgb), 0.4);
}

.hero-label {
  font-family: var(--font-display);
  font-size: 14px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
}

.supporting-stat-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1px;
  background: rgba(255,255,255,0.06);
  width: 100%;
  border-top: 1px solid rgba(255,255,255,0.08);
}

.supporting-stat {
  padding: 10px 14px;
  background: var(--bg-secondary);
  text-align: center;
}

.supporting-value {
  font-family: var(--font-display);
  font-size: 18px;
  color: var(--text-primary);
}

.supporting-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
  margin-top: 2px;
}
```

## The number-first rule

For Stat Poster, the number must come BEFORE the unit label
visually. Not "Total Raised: $4.2M" but "$4.2M / TOTAL RAISED"
stacked vertically with the number dominant.

## Tabular numerics mandatory

```css
font-variant-numeric: tabular-nums;
font-feature-settings: "tnum" 1;
```

Without this, digits jitter when animating counters.

## Gotchas

- One hero stat. Not two. If the piece has two equally important
  numbers, it's not a Stat Poster — it's a Stacked Reference with
  a prominent stat strip.
- Supporting stats should be far smaller than hero — `18px` vs
  `10rem`. Don't compete.
- Text-shadow glow at `rgba(var(--primary-rgb), 0.4)` makes the
  hero pop. Subtler glow kills the impact.

## Cross-references

- [TECH-stat-strip-component](TECH-stat-strip-component.md) — the supporting stat row.
  > What it does · When to use · CSS · HTML · The signature — colored top border · Number formatting rules · Common stat fields · Gotchas · Cross-references
- [TECH-typography-scale](TECH-typography-scale.md) — size rules for the hero number.
  > What it does · The scale · Weight-based hierarchy · Letter-spacing rules · Tabular numerics (mandatory for numbers) · Summary rules · Body font size rules (the density signature) · Gotchas · Cross-references
- [TECH-stacked-reference-archetype](TECH-stacked-reference-archetype.md) — when you have multiple equal stats.
  > What it does · When to use · The shape · CSS implementation · The section-variety rule still applies · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

