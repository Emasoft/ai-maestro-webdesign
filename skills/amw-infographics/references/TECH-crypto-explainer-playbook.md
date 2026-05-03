---
name: TECH-crypto-explainer-playbook
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Color system](#color-system)
- [Typography](#typography)
- [Standard component prevalence (across 29 pieces)](#standard-component-prevalence-across-29-pieces)
- [Visual properties](#visual-properties)
- [Signature layout pattern](#signature-layout-pattern)
- [CSS variables (purple variant)](#css-variables-purple-variant)
- [CSS variables (pink variant)](#css-variables-pink-variant)
- [Font pair](#font-pair)
- [Reference template](#reference-template)
- [Archetype preference](#archetype-preference)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Crypto-Explainer playbook — 17% (29/175)

## What it does

The playbook for crypto-explainer infographics — educational
content about protocols, DeFi concepts, how-X-works. Pink / purple
primary, callout-heavy, highest neon-glow prevalence.

## When to use

Content explains: how a protocol works, DeFi concept breakdowns,
feature explainers for Web3 apps.

## Color system

- **Primary:** pink `#F59AC3` / `#F39AC6` OR purple `#A764F6`
- **Alternatives:** teal `#11C59A`, green `#4BF3B2`, amber `#F6A91A`
- **Secondary:** yellow/gold `#F4BC2F` or blue `#4DA0F8`
- **Background:** solid (45%), gradient (21%), image-overlay (21%)
- **Temperature:** mixed (69%), cool-dominant (21%)
- **Saturation:** vibrant (93%) — highest of all types

## Typography

- **Display:** Bebas Neue (38%), Montserrat Bold/Black (21%),
  Space Grotesk (10%), Bungee (7%)
- **Body:** Montserrat (41%), Avenir Next (24%), Inter (21%)

## Standard component prevalence (across 29 pieces)

| Component | Prevalence | Notes |
|-----------|------------|-------|
| Callout box | 83% | HIGHEST of all types — always present |
| Footer | 59% | |
| Feature cards (outlined 45%, filled 31%) | 76% combined | |
| Numbered list | 24% | Eligibility / how-to-claim |
| Timeline/steps | 31% | |
| Comparison table | 21% | |

## Visual properties

- **Glow:** heavy (69%)
- **Gradient overlays:** very heavy (72%) — highest of all types
- **Geometric shapes:** 93%
- **Border radius:** rounded 8-16px (59%)
- **Density:** compact (66%), comfortable (31%)
- **Card style:** outlined (45%), filled (31%)

## Signature layout pattern

```
BRAND HEADER (project logo + topic subtitle)
  ↓
FULL-BLEED HERO CONCEPT (large callout)
  ↓
FLOW DIAGRAM or PROCESS CARDS
  ↓  (curved arrows, neon glows on key nodes)
COMPARISON TABLE or NUMBERED STEPS (optional)
  ↓
FOOTER
```

## CSS variables (purple variant)

```css
--bg: #080808;
--primary: #A764F6;
--secondary: #F4BC2F;
--glow: rgba(167,100,246,0.3);
--text: #FFFFFF;
--muted: #8B8B8B;
```

## CSS variables (pink variant)

```css
--bg: #080808;
--primary: #F59AC3;
--secondary: #F4BC2F;
--glow: rgba(245,154,195,0.3);
--text: #FFFFFF;
--muted: #8B8B8B;
```

## Font pair

Bebas Neue (display) + Montserrat (body).

## Reference template

`templates/crypto-explainer.html`

## Archetype preference

**Flow Poster** is the default archetype for crypto-explainer — the
flow IS the explanation. Stacked Reference is the alternative for
feature-heavy explainers.

## Gotchas

- Pink / purple are type-specific — don't default to them for
  other types.
- Glow opacity 0.3 on key nodes — this is the MAX. Don't go heavier.
- Curved arrows (not straight) differentiate crypto-explainer's
  flows from token-economics'.

## Cross-references

- [TECH-per-type-signature-palettes](TECH-per-type-signature-palettes.md) — the color system.
  > What it does · The 5 major-type palettes · Why these · The full selection order · CSS variables per type · Token-Economics · Crypto-Explainer · Game-Overview · Ecosystem · Airdrop-Guide · Gotchas · Cross-references
- [TECH-flow-poster-archetype](TECH-flow-poster-archetype.md) — the default archetype.
  > What it does · When to use · The shape · CSS implementation · Label rule · Gotchas · Cross-references
- [TECH-flow-with-arrows-component](TECH-flow-with-arrows-component.md) — the flow component.
  > What it does · When to use · Horizontal flow — CSS · Vertical connector — CSS · HTML · Arrow icons — Phosphor only · Label rule — mandatory · Gotchas · Cross-references
- [TECH-glow-system](TECH-glow-system.md) — the neon glow patterns.
  > What it does · The glow system · Double-layer glow pattern · Top confirmed glow colors · When to use each · Light-mode override · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

