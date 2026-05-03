---
name: TECH-cheat-sheet-archetype
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/layout-patterns.md
---

# Archetype 5: Cheat Sheet

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [The shape](#the-shape)
- [CSS implementation](#css-implementation)
- [The mixed-layout rule](#the-mixed-layout-rule)
- [Flow connector between sections](#flow-connector-between-sections)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Maximum density. Multiple section types mixed freely — tables,
bullets, flow diagrams, images — all on one canvas. Reads like a
reference document you'd screenshot and save.

## When to use

- Pocket guides, game guides, airdrop guides
- Comprehensive overviews with 5+ distinct topics
- The densest of all archetypes — 12-20 content blocks

Example references: `pocket_guide.png`,
`farming_game_mode_mechanic_overview.png`.

## The shape

```
┌────────────────────────────────────────┐
│  HEADER                                │
├──────────────────────┬─────────────────┤
│  SECTION A           │  SECTION B      │
│  (pill tags grid)    │  (bullet list)  │
├──────────────────────┴─────────────────┤
│  ↓ FLOW CONNECTOR (labeled arrow)      │
├────────────────────────────────────────┤
│  SECTION C  │  SECTION D  │ SECTION E  │
│  (tier badges)│ (criteria) │ (process) │
├─────────────┴─────────────┴────────────┤
│  SECTION F (full-width tier table)     │
├────────────────────────────────────────┤
│  FOOTER / CTA                          │
└────────────────────────────────────────┘
```

## CSS implementation

```css
/* source: image-generation/create-infographics/resources/layout-patterns.md */
.cheat-sheet-layout {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.cheat-row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.cheat-row-3col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.cheat-row-full {
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.section-connector {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 0;
  gap: 8px;
  color: var(--muted);
  font-size: 11px;
}

.section-connector::before,
.section-connector::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(var(--primary-rgb), 0.2);
}

.pill-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.content-pill {
  padding: 4px 10px;
  border: 1px solid rgba(var(--primary-rgb), 0.4);
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-secondary);
  background: rgba(var(--primary-rgb), 0.06);
}
```

## The mixed-layout rule

Alternate between 2-col, 3-col, and full-width rows. Don't stack 5
identical 3-col rows — that's a SaaS landing page, not a cheat
sheet.

## Flow connector between sections

The `.section-connector` styled with `::before`/`::after` horizontal
lines creates a "↓ NEXT SECTION" visual. Use between related but
distinct sections to show flow.

## Gotchas

- The highest density archetype — violating the anti-frontend
  checklist here is very easy. Run the checklist twice.
- Don't mix archetypes — if the canvas has 4+ sections and you're
  using cheat-sheet layouts, stay in Cheat Sheet mode.
- Full-width rows should only be tables or hero sections — use
  multi-col for everything else.

## Cross-references

- [TECH-stacked-reference-archetype](TECH-stacked-reference-archetype.md) — less dense alternative.
  > What it does · When to use · The shape · CSS implementation · The section-variety rule still applies · Gotchas · Cross-references
- [TECH-flow-poster-archetype](TECH-flow-poster-archetype.md) — when flow is the main story.
  > What it does · When to use · The shape · CSS implementation · Label rule · Gotchas · Cross-references
- [TECH-section-variety-rule](TECH-section-variety-rule.md) — mandatory here.
  > What it does · Acceptable section variety · Anti-patterns (reject and redesign) · The enforcement routine · The available component types (pick 3+) · Rule of thumb · Gotchas · Cross-references
- [TECH-airdrop-guide-playbook](TECH-airdrop-guide-playbook.md) — airdrop guides often use this.
  > What it does · When to use · Color system · Typography · Standard component prevalence (across 17 pieces) · Visual properties · Signature layout pattern · The amber+blue value split (signature) · The claim-steps horizontal flow · CSS variables · Reference template · Archetype preference · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

