---
name: TECH-game-overview-playbook
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Color system](#color-system)
- [Typography — two sub-variants](#typography-two-sub-variants)
  - [Standard game](#standard-game)
  - [Pixel / retro game](#pixel-retro-game)
- [Standard component prevalence (across 25 pieces)](#standard-component-prevalence-across-25-pieces)
- [Visual properties](#visual-properties)
- [Signature layout pattern](#signature-layout-pattern)
- [Character card grid (signature pattern)](#character-card-grid-signature-pattern)
- [Light-mode sub-variant](#light-mode-sub-variant)
- [CSS variables (standard)](#css-variables-standard)
- [CSS variables (pixel)](#css-variables-pixel)
- [Reference template](#reference-template)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Game-Overview playbook — 14% (25/175)

## What it does

The playbook for game-overview / GameFi infographics — character
rosters, tokenomics, game mechanics, mode breakdowns. Two font
sub-variants (standard vs pixel-retro).

## When to use

Content involves: GameFi launches, character rosters, game mechanic
breakdowns, NFT game tokenomics, tournaments.

## Color system

- **Primary:** amber/gold `#F6A91A` / `#F2BC42` (55%) OR vibrant
  purple `#A94CFF` / `#C24BFF` (24%)
- **Secondary:** complementary contrast (green `#4FE112` with amber,
  or gold with purple)
- **Background:** solid (56%), image-overlay (20%) — often actual
  game art as background
- **Temperature:** mixed (100%)
- **Saturation:** vibrant (96%)

## Typography — two sub-variants

### Standard game
- **Display:** Bebas Neue (48%), Teko (12%)
- **Body:** Montserrat (52%)

### Pixel / retro game
- **Display:** Press Start 2P (20%) — pixel only
- **Body:** VT323 or IBM Plex Mono for stats
- **Border radius:** 0px (sharp), not rounded

Use pixel fonts when the game has retro/pixel/8-bit aesthetic. Never
use Bebas Neue for a pixel game.

## Standard component prevalence (across 25 pieces)

| Component | Prevalence | Notes |
|-----------|------------|-------|
| Feature cards (outlined 56%, filled 36%) | 92% combined | Very common |
| Callout box | 64% | |
| Comparison table | 40% | Character stats, rarity, items |
| Footer | 52% | |
| Progress bars | 16% | Character stats, progression |
| Timeline | 16% | |

## Visual properties

- **Glow:** 60%
- **Decorative BG (game art):** 68%
- **Geometric shapes:** 68%
- **Border radius:** rounded 8-16px (60%), sharp 0px (12% pixel games)
- **Density:** compact (76%)

## Signature layout pattern

```
GAME-ART HERO HEADER (logo lockup top-left/right)
  ↓
CHARACTER PROFILES (portrait + rarity + ability grid)
  OR GAME FEATURE SECTIONS
  ↓
STATS COMPARISON MATRIX (rarity, power, drop rate)
  ↓
MECHANICS / ECONOMY OVERVIEW (flow diagram or mode breakdown)
  ↓
FOOTER
```

## Character card grid (signature pattern)

```css
/* source: image-generation/create-infographics/SKILL.md */
.char-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 2px; }
.char-card { background: var(--bg3); border: 1px solid var(--border); overflow: hidden; }
.char-portrait { width: 100%; aspect-ratio: 1; object-fit: cover; display: block; }
.char-name { font-size: 9px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; padding: 5px 8px 4px; color: #fff; }
.char-stat-bar { flex: 1; height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; overflow: hidden; }
```

Tight 5-column grid, each card = portrait + name + 2-4 colored
horizontal stat bars.

## Light-mode sub-variant

Game event guides, quest cheat sheets, bounty pocket guides
frequently use white / `#f4f5f8` backgrounds. If content type is
event guide / quest walkthrough / bounty guide → light mode is the
right default for THAT sub-type.

## CSS variables (standard)

```css
--bg: #070707;
--primary: #F6A91A;
--secondary: #A94CFF;
--glow: rgba(246,169,26,0.25);
--text: #FFFFFF;
--muted: #8B8B8B;
```

## CSS variables (pixel)

```css
--bg: #070707;
--primary: #F6A91A;
--font-display: 'Press Start 2P', monospace;
--font-body: 'VT323', monospace;
--radius-card: 0px;
```

## Reference template

`templates/game-overview.html`

## Gotchas

- Research the game aesthetic first — pixel vs 3D vs fantasy vs
  sci-fi — and pick the font variant accordingly.
- Character card grids pack TIGHT — 2px gaps, not 10px. Density
  over breathing room.
- Light-mode game guides are a real sub-variant, not a mistake.

## Cross-references

- [TECH-per-type-signature-palettes](TECH-per-type-signature-palettes.md) — the color system.
  > What it does · The 5 major-type palettes · Why these · The full selection order · CSS variables per type · Token-Economics · Crypto-Explainer · Game-Overview · Ecosystem · Airdrop-Guide · Gotchas · Cross-references
- [TECH-character-card-grid](TECH-character-card-grid.md) — the signature component.
  > What it does · CSS · HTML · The tight-grid signature · Stat bar sizing · When to use · Gotchas · Cross-references
- [TECH-radar-chart](TECH-radar-chart.md) — for character stat comparisons.
  > What it does · When to use · HTML · The signature options · Multi-character comparison — overlay datasets · Gotchas · Cross-references
- [TECH-tier-comparison-component](TECH-tier-comparison-component.md) — rarity tables.
  > What it does · When to use · CSS — the base table · CSS — the tier badges · HTML · Custom tier names and colors · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
