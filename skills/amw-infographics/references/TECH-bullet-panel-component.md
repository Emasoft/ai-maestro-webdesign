---
name: TECH-bullet-panel-component
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [CSS](#css)
- [HTML](#html)
- [The ▸ bullet convention](#the-bullet-convention)
- [2-col grid pattern](#2-col-grid-pattern)
- [One fact per bullet (mandatory)](#one-fact-per-bullet-mandatory)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# `bullet_panel` component — DEFAULT for text content

## What it does

Bordered panel with a compact bullet list inside. This is the
**default** for text content — prefer it over `feature_cards` always.
Feature cards (icon + title + description) are the "SaaS landing
page" anti-pattern. `bullet_panel` is dense, editorial, signature.

## When to use

- Features, rules, conditions, requirements — **always**.
- Any time you'd reach for a 3-column "feature cards" grid, use this
  instead.
- Pair 2+ `bullet_panel`s side-by-side in a grid for 2-col density.

## CSS

```css
/* source: image-generation/create-infographics/SKILL.md */
.bullet-panel {
  border: 1.5px solid rgba(var(--primary-rgb), 0.35);
  border-radius: 8px;
  padding: 14px 16px;
  background: rgba(var(--primary-rgb), 0.04);
}
.bullet-panel h4 {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--primary);
  margin-bottom: 10px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(var(--primary-rgb), 0.2);
}
.bullet-panel ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.bullet-panel li {
  font-size: 12px;
  line-height: 1.45;
  color: var(--text);
  padding-left: 14px;
  position: relative;
}
.bullet-panel li::before {
  content: '▸';
  position: absolute;
  left: 0;
  color: var(--primary);
  font-size: 10px;
}
```

## HTML

```html
<div class="bullet-panel">
  <h4>STAKING REWARDS</h4>
  <ul>
    <li>Earns 8% APY on staked tokens</li>
    <li>30-day lock period after deposit</li>
    <li>Compounding every 24 hours</li>
    <li>Slashed 0.5% on early withdrawal</li>
  </ul>
</div>
```

## The ▸ bullet convention

Using `▸` (or `•`) with `content:` and absolute positioning — NOT
the default `list-style` bullet. The accent color on the bullet ties
each panel to the brand palette.

## 2-col grid pattern

```css
.bullet-panel-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}
```

## One fact per bullet (mandatory)

Each bullet = one fact, one condition, one number. Never multi-
sentence bullets. If you need to explain context, add a separate
bullet or use a table.

```
✅ One fact per bullet:
• Min stake: 500 $TKN
• Lock period: 30 days
• APY: 8% (compounding daily)

❌ Multi-sentence bullet:
• Users must stake at least 500 $TKN tokens and maintain the lock
  for 30 days to earn the 8% APY, which compounds every day.
```

## Gotchas

- If you have 3+ bullet panels in a row, you're OK — bullet panels
  are the variety-safe default. But stacking them beyond 4 rows
  starts feeling repetitive.
- Border opacity 0.35 is visible; 0.08 is invisible. Use 0.30+.
- The `h4` color uses `var(--primary)` — if you change the brand
  primary, it cascades. Don't hard-code hexes.

## Cross-references

- [TECH-dense-table-component](TECH-dense-table-component.md) — when the data is tabular.
- [TECH-section-variety-rule](TECH-section-variety-rule.md) — the rule this component satisfies.
- [TECH-copy-guide-bullets](TECH-copy-guide-bullets.md) — writing the bullet text.
- [`../SKILL.md`](../SKILL.md) — parent skill

