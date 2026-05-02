---
name: TECH-one-shot-mode
category: infographic-builder
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [The 5 steps](#the-5-steps)
- [Classification — identify the type](#classification-identify-the-type)
- [Composition archetype — pick one](#composition-archetype-pick-one)
- [Build rules](#build-rules)
- [Head elements (required)](#head-elements-required)
- [Step 5 — export command](#step-5-export-command)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# One-Shot mode (Mode B) — generate the full infographic in one pass

## What it does

A pipeline that builds the full infographic HTML in a single
generation, without component-by-component approval. Used when the
user provides a complete brief and wants the result immediately.

## When to use

- "Create an infographic about X" (full brief provided)
- "Generate", "make me", "build this infographic"
- User says "assemble" or "finalize" after a builder session

## The 5 steps

```
Step 1 — Design Brief
  3 questions if not answered: brand, platform, key insight

Step 2 — Classify + Archetype + Layout Intent
  Content type (playbook or generic)
  Composition archetype (Stacked Reference default)
  Layout intent (archetype + dominant component + density target)

Step 3 — Build
  Single self-contained HTML file
  CSS inline, no external stylesheets
  Phosphor Icons + Google Fonts loaded via CDN

Step 4 — Quality Check
  Anti-Frontend Checklist
  Reduction Pass

Step 5 — Export
  PNG + PDF + SVG via scripts/export.py
```

## Classification — identify the type

Crypto/Web3 playbooks:
- `token-economics`, `crypto-explainer`, `game-overview`,
  `ecosystem`, `airdrop-guide`, `token-flywheel`, `staking-yield`,
  `defi-protocol`, `roadmap`, `stats-poster`, `whitepaper-overview`,
  `game-event`, `game-cheat-sheet`

Generic archetypes:
- `listicle`, `feature-roster`, `modern-timeline`, `dark-modern`,
  `data-story`, `event-schedule`, `branded-minimal`,
  `light-editorial`, `how-it-works`, `comparison`, `nft-showcase`

State the type in one sentence: *"Content type: token-economics →
applying Token-Economics Playbook."*

## Composition archetype — pick one

Default: **Stacked Reference** (70%+ of pieces). Override to
Flow Poster if flow dominates, Hub & Spoke for ecosystems, Stat
Poster for single-metric stories, Cheat Sheet for dense guides.

## Build rules

- All CSS inline — no external stylesheets
- Use CSS custom properties at `:root` for colors, fonts, spacing
- Section padding: 24-32px vertical
- Card padding: 12-16px
- Gaps: 8-12px within sections
- Charts: inline SVG for pie, Chart.js `<canvas>` for bar/line/radar
- No lorem ipsum, no placeholder text, no fabricated data
- Footer by default

## Head elements (required)

```html
<!-- source: image-generation/create-infographics/SKILL.md -->
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
<script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>
<!-- Chart.js — only if building bar/line/radar charts -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

## Step 5 — export command

```bash
pip install playwright --break-system-packages -q
playwright install chromium --with-deps
python scripts/export.py --input {html_file} --output {name} --width {W} --scale 2
```

Produces `{name}.png`, `{name}.pdf`, `{name}.svg`.

## Gotchas

- Don't skip the Quality Check — Anti-Frontend failures are the
  most common reason one-shot output looks bad.
- Don't use `.infographic/` state — this mode doesn't persist
  per-component state.
- Use the playbook's color system and component defaults, not the
  generic signature palette.

## Cross-references

- [TECH-interactive-builder-mode](TECH-interactive-builder-mode.md) — the iterative cousin.
- [TECH-guided-creative-mode](TECH-guided-creative-mode.md) — the 2-option middle path.
- [TECH-dense-editorial-dna](TECH-dense-editorial-dna.md) — the quality check rules.
- [TECH-anti-frontend-checklist](TECH-anti-frontend-checklist.md) — Step 4 details.
- [TECH-export-pipeline](TECH-export-pipeline.md) — Step 5 details.
- [`../SKILL.md`](../SKILL.md) — parent skill

