---
name: infographics-tech-index
purpose: Full per-technique catalog for amw-infographics. Read this when you need the explicit one-line description of every TECH-* file. SKILL.md links here directly.
---

# Infographics — Full Technique Catalog (59 entries)

> **Routing back:** [SKILL](../SKILL.md) · [Anti-Frontend Checklist](TECH-anti-frontend-checklist.md) · [Reduction Pass](TECH-reduction-pass.md)

## Table of Contents

- Modes (3)
- Archetypes (5)
- Playbooks (5 content-type playbooks)
- Components (15)
- Charts (10)
- Color & typography (8)
- Copy (3)
- Aesthetic systems (3)
- Pre-delivery / quality (2)
- Pipeline / preview / export (3)
- Cross-references

This catalog mirrors every `TECH-*.md` file in `./` with its one-line
description. Use the decision tree in [SKILL.md](../SKILL.md) to pick the
right TECH file; this index exists for direct lookup when you already know
the slug.

All TECH files share the same TOC structure:
> What it does · When to use · How it works · CSS · HTML · Gotchas · Cross-references
(plus 1–4 technique-specific subsections — see each TECH file for the precise list)

## Modes (3)

- [TECH-interactive-builder-mode.md](TECH-interactive-builder-mode.md) — Mode A — component-by-component iteration with live preview
- [TECH-one-shot-mode.md](TECH-one-shot-mode.md) — Mode B — generate the full infographic in one pass
- [TECH-guided-creative-mode.md](TECH-guided-creative-mode.md) — Mode C — show two compositions before building

## Archetypes (5)

- [TECH-stacked-reference-archetype.md](TECH-stacked-reference-archetype.md) — Archetype 1: Stacked Reference (DEFAULT, 70%+ of work)
- [TECH-flow-poster-archetype.md](TECH-flow-poster-archetype.md) — Archetype 2: Flow Poster
- [TECH-hub-spoke-archetype.md](TECH-hub-spoke-archetype.md) — Archetype 3: Hub & Spoke
- [TECH-stat-poster-archetype.md](TECH-stat-poster-archetype.md) — Archetype 4: Stat Poster
- [TECH-cheat-sheet-archetype.md](TECH-cheat-sheet-archetype.md) — Archetype 5: Cheat Sheet

## Playbooks (5 content-type playbooks)

- [TECH-token-economics-playbook.md](TECH-token-economics-playbook.md) — Token-Economics — 35% (62/175)
- [TECH-game-overview-playbook.md](TECH-game-overview-playbook.md) — Game-Overview — 14% (25/175)
- [TECH-ecosystem-playbook.md](TECH-ecosystem-playbook.md) — Ecosystem — 13% (22/175)
- [TECH-crypto-explainer-playbook.md](TECH-crypto-explainer-playbook.md) — Crypto-Explainer — 17% (29/175)
- [TECH-airdrop-guide-playbook.md](TECH-airdrop-guide-playbook.md) — Airdrop-Guide — 10% (17/175)

## Components (15)

- [TECH-bullet-panel-component.md](TECH-bullet-panel-component.md) — `bullet_panel` — DEFAULT for text content
- [TECH-bordered-section-component.md](TECH-bordered-section-component.md) — `bordered_section` — visible-border content panel
- [TECH-stat-strip-component.md](TECH-stat-strip-component.md) — `stat_strip` — full-width KPI row with colored top borders
- [TECH-dense-table-component.md](TECH-dense-table-component.md) — `dense_table` — primary data format
- [TECH-tier-comparison-component.md](TECH-tier-comparison-component.md) — `tier_comparison` — tier badge table
- [TECH-step-process-component.md](TECH-step-process-component.md) — `step_process` — numbered steps with connector line
- [TECH-flow-with-arrows-component.md](TECH-flow-with-arrows-component.md) — `flow_with_arrows` — horizontal flow with arrow connectors
- [TECH-flywheel-loop-component.md](TECH-flywheel-loop-component.md) — `flywheel_loop` — rectangular nodes circular back to start
- [TECH-character-card-grid.md](TECH-character-card-grid.md) — Character / NFT card grid — tight 5-column
- [TECH-section-band.md](TECH-section-band.md) — Full-width section separator bands
- [TECH-section-header-pill.md](TECH-section-header-pill.md) — Section header pill badge (ecosystem signature)
- [TECH-section-variety-rule.md](TECH-section-variety-rule.md) — Section Variety Rule — MANDATORY across 4+ sections
- [TECH-outer-canvas-border.md](TECH-outer-canvas-border.md) — Outer canvas border — thin accent-colored frame
- [TECH-arrows-and-connectors.md](TECH-arrows-and-connectors.md) — Arrows & connectors — 71% of pieces
- [TECH-swim-lane-architecture.md](TECH-swim-lane-architecture.md) — Swim-lane architecture diagram

## Charts (10)

- [TECH-chart-selection-guide.md](TECH-chart-selection-guide.md) — Chart selection — decision tree for chart type
- [TECH-svg-pie-chart.md](TECH-svg-pie-chart.md) — SVG pie chart — token allocation (the #1 chart)
- [TECH-bar-chart-css.md](TECH-bar-chart-css.md) — CSS horizontal bar chart — vesting / allocation strips
- [TECH-line-chart.md](TECH-line-chart.md) — Line chart — Chart.js with designer theming
- [TECH-radar-chart.md](TECH-radar-chart.md) — Radar chart — Chart.js for game stats
- [TECH-progress-bar-vesting.md](TECH-progress-bar-vesting.md) — Progress bar — vesting timeline with milestones
- [TECH-waffle-chart.md](TECH-waffle-chart.md) — Waffle chart — 10×10 grid for % of total
- [TECH-slope-chart.md](TECH-slope-chart.md) — Slope chart — before/after comparison
- [TECH-annotated-bar-chart.md](TECH-annotated-bar-chart.md) — Annotated bar chart — SVG with callout + benchmark
- [TECH-proportional-circles.md](TECH-proportional-circles.md) — Proportional circles — area = value
- [TECH-dot-plot.md](TECH-dot-plot.md) — Dot plot — distribution + individual points
- [TECH-annotation-first.md](TECH-annotation-first.md) — Annotation-first — labels on charts, not in legends

## Color & typography (8)

- [TECH-signature-palette.md](TECH-signature-palette.md) — Signature palette — near-black + amber + teal/blue complement
- [TECH-color-palette-recipes.md](TECH-color-palette-recipes.md) — 13 named palette recipes
- [TECH-per-type-signature-palettes.md](TECH-per-type-signature-palettes.md) — Per-content-type signature palettes
- [TECH-chain-color-coding.md](TECH-chain-color-coding.md) — Blockchain chain color-coding
- [TECH-glow-system.md](TECH-glow-system.md) — Glow system — neon box-shadow + text-shadow
- [TECH-font-system.md](TECH-font-system.md) — Font system — 5-font display hierarchy
- [TECH-typography-scale.md](TECH-typography-scale.md) — Typography scale — minor third (1.25 ratio)
- [TECH-inline-token-coloring.md](TECH-inline-token-coloring.md) — Inline token coloring — `$TOKEN` names always colored

## Copy (3)

- [TECH-copy-guide-bullets.md](TECH-copy-guide-bullets.md) — Bullets over paragraphs, always
- [TECH-copy-guide-numbers.md](TECH-copy-guide-numbers.md) — Number formatting rules
- [TECH-design-brief.md](TECH-design-brief.md) — Design Brief — 3 (or 5) intake questions

## Aesthetic systems (3)

- [TECH-dense-editorial-dna.md](TECH-dense-editorial-dna.md) — Dense editorial DNA — the defining aesthetic
- [TECH-background-depth.md](TECH-background-depth.md) — Background depth — radial orbs, scanlines, paper texture
- [TECH-template-registry.md](TECH-template-registry.md) — 24 reference template registry

## Pre-delivery / quality (2)

- [TECH-anti-frontend-checklist.md](TECH-anti-frontend-checklist.md) — Anti-Frontend Checklist — pre-delivery gate
- [TECH-reduction-pass.md](TECH-reduction-pass.md) — Reduction Pass — strip everything that doesn't encode data

## Pipeline / preview / export (3)

- [TECH-platform-sizing.md](TECH-platform-sizing.md) — Platform sizing — Twitter, Instagram, LinkedIn, Pinterest
- [TECH-preview-server.md](TECH-preview-server.md) — Preview server — live reload during builder sessions
- [TECH-preview-animations.md](TECH-preview-animations.md) — Preview entrance animations — browser only
- [TECH-export-pipeline.md](TECH-export-pipeline.md) — Export pipeline — HTML to PNG + PDF + SVG

## Cross-references

- [SKILL.md](../SKILL.md) — orchestrator routing surface (decision tree, trigger phrases, completion checklist, template selection table)
- [resources/style-details.md](../resources/style-details.md) — full 1062-line design system with component CSS patterns, type playbooks, reduction-pass rules
- [resources/layout-patterns.md](../resources/layout-patterns.md) — full 842-line layout and archetype scaffold library
- [resources/design-brief.md](../resources/design-brief.md) — 5-question intake framework + aesthetic decision table
- [resources/charts.md](../resources/charts.md) — chart rules with annotation-first placement
- [resources/color-palettes.md](../resources/color-palettes.md) — full palette library by type
- [resources/font-pairings.md](../resources/font-pairings.md) — display-font prevalence table
- [resources/platform-sizes.md](../resources/platform-sizes.md) — 7 canvas sizes with per-platform layout/font adjustments
- [resources/copy-guide.md](../resources/copy-guide.md) — headline, callout, and label writing rules
