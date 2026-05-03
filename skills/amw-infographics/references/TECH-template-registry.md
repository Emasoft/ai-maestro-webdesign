---
name: TECH-template-registry
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/templates/
---
## Table of Contents

- [What it does](#what-it-does)
- [The shared V4 standards](#the-shared-v4-standards)
- [Crypto / Web3 templates (13)](#crypto-web3-templates-13)
- [Generic templates (11)](#generic-templates-11)
- [Template selection by user intent](#template-selection-by-user-intent)
- [Usage](#usage)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Template registry — 24 reference templates

## What it does

24 pre-built V4 Dense Editorial templates in `templates/`. Each is a
fully-built example with `{{PLACEHOLDER}}` variables. Start from
the matching template and substitute real content rather than
building from scratch.

## The shared V4 standards

Every template uses:
- 12px dense tables with 6px/10px cell padding
- `▸` bullet panels with 14px/16px padding
- Arrow connectors between sections
- Stat strips with 2px top-border accents
- Bebas Neue + Montserrat font pairing

## Crypto / Web3 templates (13)

| Template | File | Primary | Best for |
|----------|------|---------|----------|
| **Token Economics** | `token-economics.html` | Amber `#E99A00` | Allocation pie, vesting, supply |
| **Crypto Explainer** | `crypto-explainer.html` | Purple `#A764F6` | Protocol explainers, DeFi concepts |
| **Game Overview** | `game-overview.html` | Gold `#F6A91A` | GameFi launches, character rosters |
| **Ecosystem Map** | `ecosystem.html` | Green `#00E88A` | Partner directories, integrations |
| **Airdrop Guide** | `airdrop-guide.html` | Amber `#E79A00` | Eligibility, claim steps, vesting |
| **Token Flywheel** | `token-flywheel.html` | Green `#00E88A` | Value loops, buyback/burn cycles |
| **Staking & Yield** | `staking-yield.html` | Blue `#00C9FF` | APY breakdown, staking tiers |
| **DeFi Protocol** | `defi-protocol.html` | Cyan `#4ECBFF` | Mechanics, fee structures, risk |
| **Project Roadmap** | `roadmap.html` | Purple `#B98AFF` | Phase cards, milestone tables |
| **Stats Poster** | `stats-poster.html` | Amber `#E79A00` | Single-stat hero, period tables |
| **Whitepaper Overview** | `whitepaper-overview.html` | Cyan `#4ECBFF` | Technical summaries, problem/solution |
| **Game Event** | `game-event.html` | Red `#FF6B6B` | Tournament schedules, prizes |
| **Game Cheat Sheet** | `game-cheat-sheet.html` | Green `#00E88A` | Class/resource refs, combat tips |

## Generic templates (11)

| Template | File | Primary | Best for |
|----------|------|---------|----------|
| **NFT Showcase** | `nft-showcase.html` | Teal `#1AA8B8` | Rarity tiers, trait distribution |
| **How It Works** | `how-it-works.html` | Amber `#E99A00` | Step-flow explainers |
| **Comparison** | `comparison.html` | Cyan + Red | A vs B head-to-head |
| **Listicle** | `listicle.html` | Amber `#FFD166` | Ranked lists, top-N formats |
| **Feature Roster** | `feature-roster.html` | Green `#00E88A` | Feature cards, pricing tiers |
| **Modern Timeline** | `modern-timeline.html` | Purple `#B98AFF` | History/roadmap with tracks |
| **Dark Modern** | `dark-modern.html` | Cyan `#4ECBFF` | General dark overview |
| **Data Story** | `data-story.html` | Green `#00E88A` | KPI-dominant with bar charts |
| **Event Schedule** | `event-schedule.html` | Red `#FF6B6B` | Conference day columns |
| **Branded Minimal** | `branded-minimal.html` | Amber `#E99A00` | Brand-forward with pullquote |
| **Light Editorial** | `light-editorial.html` | Blue `#1A4FD6` | Light-mode reports |

## Template selection by user intent

| User says | Template |
|-----------|----------|
| "tokenomics", "vesting", "allocation" | `token-economics.html` |
| "how does X protocol work", "explainer" | `crypto-explainer.html` |
| "game overview", "NFT game" | `game-overview.html` |
| "ecosystem", "partner map" | `ecosystem.html` |
| "airdrop", "claim guide" | `airdrop-guide.html` |
| "flywheel", "value loop" | `token-flywheel.html` |
| "staking", "APY", "rewards" | `staking-yield.html` |
| "DeFi protocol", "AMM" | `defi-protocol.html` |
| "roadmap", "Q1/Q2" | `roadmap.html` or `modern-timeline.html` |
| "stats", "metrics poster" | `stats-poster.html` or `data-story.html` |
| "whitepaper" | `whitepaper-overview.html` |
| "tournament", "prizes" | `game-event.html` |
| "cheat sheet", "quick reference" | `game-cheat-sheet.html` |
| "NFT collection", "rarity" | `nft-showcase.html` |
| "compare X vs Y" | `comparison.html` |
| "top 10", "ranked list" | `listicle.html` |
| "product features", "pricing" | `feature-roster.html` |
| "timeline", "history" | `modern-timeline.html` |
| "data story", "dashboard" | `dark-modern.html` or `data-story.html` |
| "event", "conference" | `event-schedule.html` |
| "brand", "one-pager" | `branded-minimal.html` |
| "light mode", "editorial" | `light-editorial.html` |

## Usage

1. User request maps to template (see selection table).
2. Copy template to working file.
3. Replace `{{PLACEHOLDER}}` variables with user data.
4. Run Anti-Frontend Checklist.
5. Run Reduction Pass.
6. Export.

## Gotchas

- Don't modify the template's CSS structure — swap content only.
  The CSS is tuned for V4 density.
- `{{PLACEHOLDER}}` syntax isn't real templating — just string
  replacement. Use `sed`, search/replace, or a templating library.
- Templates are starting points, not rigid — if the user's data
  doesn't fit the archetype, switch templates.

## Cross-references

- [TECH-per-type-signature-palettes](TECH-per-type-signature-palettes.md) — palette defaults per type.
  > What it does · The 5 major-type palettes · Why these · The full selection order · CSS variables per type · Token-Economics · Crypto-Explainer · Game-Overview · Ecosystem · Airdrop-Guide · Gotchas · Cross-references
- [TECH-token-economics-playbook](TECH-token-economics-playbook.md) — the playbook each template implements.
  > What it does · When to use · Color system · Typography · Standard component prevalence (across 62 pieces) · Visual properties · Signature layout pattern (portrait-tall, 10+ content blocks) · CSS variables · Font pair · Reference template · Density rule · Gotchas · Cross-references
- [TECH-one-shot-mode](TECH-one-shot-mode.md) — the mode that uses templates.
  > What it does · When to use · The 5 steps · Classification — identify the type · Composition archetype — pick one · Build rules · Head elements (required) · Step 5 — export command · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

