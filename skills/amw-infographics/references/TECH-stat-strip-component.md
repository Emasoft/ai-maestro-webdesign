---
name: TECH-stat-strip-component
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/layout-patterns.md
---

# `stat_strip` — full-width KPI row with colored top borders

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [CSS](#css)
- [HTML](#html)
- [The signature — colored top border](#the-signature-colored-top-border)
- [Number formatting rules](#number-formatting-rules)
- [Common stat fields](#common-stat-fields)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Full-width row of 3-4 KPIs with colored top borders. Placed at the
top of an infographic (under the hero), immediately conveys the key
metrics. Present in 42% of pieces (74/175).

## When to use

- Hero stat bar under the title — Total Supply / Price / FDV / Airdrop.
- KPI summaries — anywhere 3-4 metrics need equal prominence.
- Sale stats, launch metrics, milestone counters.

## CSS

```css
/* source: image-generation/create-infographics/SKILL.md */
.stat-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* or repeat(3, 1fr) */
  gap: 10px;
  margin-bottom: 24px;
}
.stat-item {
  border-top: 3px solid var(--primary);
  background: rgba(var(--primary-rgb), 0.07);
  border-radius: 0 0 6px 6px;
  padding: 12px 14px;
  text-align: center;
}
.stat-item .number {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 28px;
  color: var(--primary);
  line-height: 1;
}
.stat-item .label {
  font-size: 10px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 4px;
}
```

## HTML

```html
<div class="stat-strip">
  <div class="stat-item">
    <div class="number">69B</div>
    <div class="label">TOTAL SUPPLY</div>
  </div>
  <div class="stat-item">
    <div class="number">$0.0001</div>
    <div class="label">TGE PRICE</div>
  </div>
  <div class="stat-item">
    <div class="number">$6.9M</div>
    <div class="label">FDV</div>
  </div>
  <div class="stat-item">
    <div class="number">15%</div>
    <div class="label">AIRDROP POOL</div>
  </div>
</div>
```

## The signature — colored top border

The `border-top: 3px solid var(--primary)` is THE distinguishing
feature. Makes each stat feel like a tab or marker.

## Number formatting rules

```
✅ 69B           ❌ 69000000000
✅ $0.0001       ❌ 0.000100 USD
✅ $6.9M FDV     ❌ $6,900,000 Fully Diluted Valuation
✅ 15%           ❌ 15.00%
```

Always format for scannability. See [TECH-copy-guide-numbers](TECH-copy-guide-numbers.md).

## Common stat fields

- Token supply / max supply
- Token price (TGE or current)
- FDV / market cap
- Airdrop pool size
- Player count / active wallets
- Staking APY

## Gotchas

- 3 stats (`repeat(3, 1fr)`) works on landscape; 4 stats works on
  portrait. 5+ gets crowded.
- Number size 28px scales down on narrow canvases — use `clamp()`
  for responsive.
- `font-variant-numeric: tabular-nums` if you animate counters.

## Cross-references

- [TECH-stat-poster-archetype](TECH-stat-poster-archetype.md) — when one stat dominates the whole canvas.
  > What it does · When to use · The shape · CSS implementation · The number-first rule · Tabular numerics mandatory · Gotchas · Cross-references
- [TECH-typography-scale](TECH-typography-scale.md) — sizing rules for stat numbers.
  > What it does · The scale · Weight-based hierarchy · Letter-spacing rules · Tabular numerics (mandatory for numbers) · Summary rules · Body font size rules (the density signature) · Gotchas · Cross-references
- [TECH-copy-guide-numbers](TECH-copy-guide-numbers.md) — number formatting rules.
  > What it does · The number format table · Labeling rules · Currency · Headline formulas (ALL CAPS + verb-first OR noun phrase) · Type A — Verb-first (action, how-it-works, airdrop) · Type B — Noun phrase (token-economics, stats, reports) · Type C — Mission statement (launch, profile) · Subtitle rules · Per-component word budgets · Common mistakes to avoid · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
