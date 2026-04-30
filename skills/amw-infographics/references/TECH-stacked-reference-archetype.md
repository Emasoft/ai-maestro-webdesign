---
name: TECH-stacked-reference-archetype
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/layout-patterns.md
---

# Archetype 1: Stacked Reference (DEFAULT, 70%+ of work)

## What it does

Dense top-to-bottom sections, each structurally different from the
last. This is the backbone of almost every infographic in the body
of work — 70%+ of pieces use it.

## When to use

**Default unless the content clearly calls for something else.**
Always fits:
- Token-economics with 4+ topics (allocation, vesting, utility,
  roadmap)
- Game-overview with character rosters + mechanics + economy
- Whitepaper overviews with problem/solution/comparison/team
- Any dense multi-topic content

## The shape

```
┌────────────────────────────────────────┐
│  HEADER BAR (logo + chain badge)       │
├────────────────────────────────────────┤
│  HERO / TITLE + STAT STRIP             │
├────────────────────────────────────────┤
│  SECTION A (e.g. 2-col bullet panels)  │
├──────────────────────────────────── ── ┤  ← thin hr or colored border
│  SECTION B (e.g. pie chart + table)    │
├────────────────────────────────────────┤
│  SECTION C (e.g. flow diagram)         │
├────────────────────────────────────────┤
│  SECTION D (e.g. dense data table)     │
├────────────────────────────────────────┤
│  FOOTER                                │
└────────────────────────────────────────┘
```

## CSS implementation

```css
/* source: image-generation/create-infographics/resources/layout-patterns.md */
.stacked-reference-layout {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.stacked-section {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.stacked-section:last-child {
  border-bottom: none;
}

.section-header {
  font-family: var(--font-display);
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--primary);
  margin-bottom: 10px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(var(--primary-rgb), 0.3);
}

.section-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
```

## The section-variety rule still applies

Stacked Reference says "sections stack" — it doesn't say "sections
are all the same component type". Apply the section variety rule —
at least 3 different component types across 4+ sections.

## Gotchas

- The layout is simple; the density and variety make it work.
- Don't stack 6 identical feature-card sections — that's SaaS
  marketing, not editorial.
- Use horizontal rules (`border-bottom`) OR colored borders to
  separate — not generous whitespace.

## Cross-references

- `TECH-flow-poster-archetype.md` — alternative when flows dominate.
- `TECH-hub-spoke-archetype.md` — alternative for ecosystems.
- `TECH-cheat-sheet-archetype.md` — the densest, mixed-layout cousin.
- `TECH-section-variety-rule.md` — mandatory variety.
- [`../SKILL.md`](../SKILL.md) — parent skill

