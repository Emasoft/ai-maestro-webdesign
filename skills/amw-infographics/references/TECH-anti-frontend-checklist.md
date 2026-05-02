---
name: TECH-anti-frontend-checklist
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The checklist](#the-checklist)
  - [Structure](#structure)
  - [Spacing](#spacing)
  - [Visual](#visual)
  - [Density](#density)
  - [Playbook compliance (if applicable)](#playbook-compliance-if-applicable)
  - [Data integrity](#data-integrity)
  - [Export readiness](#export-readiness)
- [Common failure modes](#common-failure-modes)
  - [1. The SaaS Landing Page](#1-the-saas-landing-page)
  - [2. The Dashboard](#2-the-dashboard)
  - [3. The Slide Deck](#3-the-slide-deck)
  - [4. The Component Demo](#4-the-component-demo)
  - [5. The Floating Islands](#5-the-floating-islands)
- [After checklist → run Reduction Pass](#after-checklist-run-reduction-pass)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Anti-Frontend Checklist — pre-delivery gate

## What it does

Run this checklist on the built HTML before export. Catches the
most common failure mode: producing a piece that looks like a SaaS
landing page instead of dense editorial reference material.

## The checklist

### Structure
- [ ] **No uniform card grids** — at least 3 different component
  types used
- [ ] **No paragraph descriptions** — all body text is bullet points
- [ ] **No isolated sections** — sections connect via arrows, flow
  lines, or shared color coding

### Spacing
- [ ] **Tight spacing** — card padding 12-16px, body font 11-13px
- [ ] Within-section gaps 8-12px
- [ ] Between-section gaps 24-32px + horizontal rule or colored border

### Visual
- [ ] **Visible borders** — not ghost borders (`rgba(255,255,255,0.08)`
  fails; use 0.25+)
- [ ] **Arrows/connectors present** if content describes process or
  flow
- [ ] **At least one table** if data has comparisons, specs, rates

### Density
- [ ] **Content block count** meets target:
  - Portrait-medium (1080×1440): 8+ blocks
  - Portrait-tall (1080×1920): 12+ blocks
  - Landscape (1200×675): 4+ blocks
  - Square (1080×1080): 5+ blocks

### Playbook compliance (if applicable)
- [ ] Section variety — 3+ different component types across
  4+ sections
- [ ] If a type-specific playbook exists, it was followed (color
  system, font pair, component defaults)
- [ ] Logo present (95% of pieces — omit only if user explicitly said
  no logo)
- [ ] Token-economics → vesting timeline or allocation visual present
- [ ] Ecosystem → partner grid with category pills
- [ ] Airdrop-guide → eligibility table + step-process

### Data integrity
- [ ] **No fabricated data** — every number came from input
- [ ] No lorem ipsum, no placeholder text
- [ ] **Display font is NOT** Inter, Roboto, Arial, Helvetica
  (generic system/UI fonts — use the 5-font display hierarchy
  or an approved 2025/2026 premium alternative instead)
- [ ] **Phosphor Icons CDN included** — no emojis as icons

### Export readiness
- [ ] Canvas width matches platform (if specified)
- [ ] All input data represented — nothing omitted
- [ ] Background mode matches request (dark by default)
- [ ] Footer included (omit only if user explicitly said no)

## Common failure modes

### 1. The SaaS Landing Page
Uniform 3-col card grids, generous whitespace, paragraph descriptions,
no tables or arrows. Looks like a Next.js marketing page.
**Fix:** Replace card grids with bullet panels + dense tables.
Add arrow connectors.

### 2. The Dashboard
Clean, minimal, data-sparse. Looks like a Stripe widget. Too much
empty space.
**Fix:** Pack more content. Smaller fonts (11-13px body).

### 3. The Slide Deck
Each section is a "slide" with one big idea and whitespace.
**Fix:** Merge sparse sections. Increase within-section density.

### 4. The Component Demo
Every section uses the same component type.
**Fix:** Apply Section Variety Rule — 3+ types across 4+ sections.

### 5. The Floating Islands
Sections isolated, no visual connection to each other.
**Fix:** Add directional arrow connectors between related sections.

## After checklist → run Reduction Pass

See [TECH-reduction-pass](TECH-reduction-pass.md). Remove gridlines, redundant labels,
unjustified decoration — scaled to the aesthetic.

## Gotchas

- Run the checklist BEFORE export. Fixing issues after PNG is made
  wastes an iteration cycle.
- Failing ANY item is cause to redesign, not ship.
- Don't game the checklist — e.g. adding a token arrow just to
  satisfy the arrow rule. The arrow must serve the content.

## Cross-references

- [TECH-dense-editorial-dna](TECH-dense-editorial-dna.md) — the parent philosophy.
- [TECH-section-variety-rule](TECH-section-variety-rule.md) — the variety rule this enforces.
- [TECH-reduction-pass](TECH-reduction-pass.md) — the complementary strip-it-down pass.
- [`../SKILL.md`](../SKILL.md) — parent skill

