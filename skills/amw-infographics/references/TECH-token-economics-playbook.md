---
name: TECH-token-economics-playbook
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/layout-patterns.md
---

# Token-Economics playbook — 35% of body of work (62/175)

## What it does

The playbook for token-economics infographics — the single most
common type. Overrides the generic signature palette with amber +
blue, sets standard component prevalence, and prescribes the
signature layout pattern.

## When to use

Content involves: token allocation, supply, vesting, TGE, FDV,
utility, staking — any "how does this token work" content.

## Color system

- **Primary:** amber `#E99A00`–`#F6A615` (warm, crypto-native, urgency)
- **Secondary:** blue `#29B7FF` or grey `#4C5A6A`
- **Background:** `#070707`–`#090909` solid (48%), gradient (21%),
  image-overlay (18%)
- **Temperature:** mixed warm+cool (60%), pure warm (26%)

## Typography

- **Display:** Bebas Neue (40%), Orbitron (16%), Teko (16%)
- **Body:** Montserrat (65%), Avenir Next (19%)
- **Type scale:** comfortable (large stats, medium labels)

## Standard component prevalence (across 62 pieces)

| Component | Prevalence | Notes |
|-----------|------------|-------|
| Callout box | 73% | Always for key allocation facts |
| Stats bar (3 KPIs) | 55% | Total Supply / Initial Price / FDV |
| Progress/vesting bars | 50% | Segmented horizontal unlock timeline |
| Footer | 56% | Attribution + logo strip |
| Timeline | 45% | Vesting schedule (horizontal) |
| Feature cards (outlined) | 40% | Sparingly |
| Comparison/allocation table | 27% | Allocation breakdown |

## Visual properties

- **Glow:** moderate (53%)
- **Geometric shapes:** heavy (87%)
- **Density:** compact (81%)
- **Border radius:** rounded 8-16px (39%) or slight 2-4px (32%)
- **Card style:** outlined (40%), flat (26%)

## Signature layout pattern (portrait-tall, 10+ content blocks)

```
HEADER BAR (logo + project name + chain badge)
  ↓
HERO TITLE + SUBTITLE (2 lines max)
  ↓
STATS STRIP (3-4 col: Total Supply | Price | FDV | Airdrop Pool)
  ↓
CORE FEATURES (2-col bullet panel)
  ↓
ALLOCATION SECTION (55/45 split: pie chart + allocation table)
  ↓ [arrow: "allocation → vesting"]
VESTING TIMELINE (full-width, TGE + monthly unlocks)
  ↓
ROUND DETAILS TABLE (Round | Price | Allocation | Cliff | Vest | TGE %)
  ↓
CALLOUT BOXES (key terms, staking APY, utility)
  ↓
FOOTER
```

## CSS variables

```css
--bg: #080808;
--primary: #E99A00;
--secondary: #29B7FF;
--text: #FFFFFF;
--muted: #8B8B8B;
```

## Font pair

Bebas Neue (display) + Montserrat (body).

## Reference template

`templates/token-economics.html`

## Density rule

Target 10+ content blocks on portrait-tall (1080×1920). Spacing
between sections: 24-32px; within sections: 8-12px.

## Gotchas

- Amber `#E99A00` is canonical — don't drift to `#F5A623` or
  `#F4A61A` variants.
- Vesting must be a table AND a progress bar — not one or the
  other. The table has dates, the bar shows the visual unlock.
- Always include FDV in the stat strip — it's the signature metric
  for token-economics.

## Cross-references

- [TECH-per-type-signature-palettes](TECH-per-type-signature-palettes.md) — the color system.
- [TECH-signature-palette](TECH-signature-palette.md) — the AMBER DARK recipe.
- [TECH-stacked-reference-archetype](TECH-stacked-reference-archetype.md) — the default archetype.
- [TECH-progress-bar-vesting](TECH-progress-bar-vesting.md) — the vesting component.
- [TECH-svg-pie-chart](TECH-svg-pie-chart.md) — the allocation chart.
- [`../SKILL.md`](../SKILL.md) — parent skill

