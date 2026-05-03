---
name: TECH-section-variety-rule
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [Acceptable section variety](#acceptable-section-variety)
- [Anti-patterns (reject and redesign)](#anti-patterns-reject-and-redesign)
- [The enforcement routine](#the-enforcement-routine)
- [The available component types (pick 3+)](#the-available-component-types-pick-3)
- [Rule of thumb](#rule-of-thumb)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Section Variety Rule — MANDATORY across 4+ sections

## What it does

Every infographic with 4+ sections MUST use at least **3 different
component types** across its sections. This single rule prevents the
"uniform card grid" anti-pattern — the #1 failure mode that makes
infographics look like marketing websites.

## Acceptable section variety

```
✅ Hero stat strip → Bullet panel → Flow diagram with arrows →
   Dense table → Callout boxes

✅ Hero → Pie chart + allocation list → Vesting timeline →
   Dense table → Footer

✅ Hero → 2-col bullet panels → Full-width comparison table →
   Step process → Footer
```

## Anti-patterns (reject and redesign)

```
❌ Hero → 3-col feature cards → 3-col feature cards →
   3-col feature cards → Footer

❌ Hero → Callout boxes → Callout boxes → Callout boxes → Footer
```

## The enforcement routine

If you catch yourself repeating the same component type 3+ times in
a row, STOP and redesign those sections. Replace one with:
- A dense table (if the content can be tabulated)
- A bullet panel with borders
- A flow diagram with arrows
- A stat callout

## The available component types (pick 3+)

From the primary component vocabulary:
- `bullet_panel`
- `dense_table`
- `flow_with_arrows`
- `stat_strip`
- `bordered_section`
- `step_process`
- `tier_comparison`
- `labeled_diagram`

Supporting (don't let dominate):
- `flywheel_loop`, `stat_callout`, `bar_chart`, `line_chart`,
  `pie_chart`, `radar_chart`, `timeline`, `comparison_table`,
  `ecosystem_map`, `progress_bars`, `icon_list`

## Rule of thumb

- 4 sections → 3 different component types minimum
- 5-6 sections → 4 different component types
- 7+ sections → 5+ different component types

## Gotchas

- "Feature cards" used 3+ times is the #1 offender — if you're
  reaching for it a third time, stop. Use `bullet_panel` or
  `dense_table` instead.
- Don't count supporting components toward variety — a hero stat
  strip + footer + 3 identical feature-card sections is still a
  variety violation.
- Variety within a single section (a table with different cell
  styles) does NOT count. This rule is about section-to-section
  structural variety.

## Cross-references

- [TECH-dense-editorial-dna](TECH-dense-editorial-dna.md) — the parent design philosophy.
  > What it does · The success state · The failure mode · The Anti-Frontend Checklist (run before delivery) · Density targets by canvas · Spacing rules (THE signature) · Content format hierarchy (top = prefer) · Gotchas · Cross-references
- [TECH-bullet-panel-component](TECH-bullet-panel-component.md) — the default text-content primary.
  > What it does · When to use · CSS · HTML · The ▸ bullet convention · 2-col grid pattern · One fact per bullet (mandatory) · Gotchas · Cross-references
- [TECH-arrows-and-connectors](TECH-arrows-and-connectors.md) — often the missing variety.
  > What it does · When arrows are MANDATORY · Rule · Horizontal arrow connector · Vertical connector line between sections · Flow diagram row · Phosphor Icons CDN · Labels on arrows (for flow diagrams) · Gotchas · Cross-references
- [TECH-stacked-reference-archetype](TECH-stacked-reference-archetype.md) — where variety lives.
  > What it does · When to use · The shape · CSS implementation · The section-variety rule still applies · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

