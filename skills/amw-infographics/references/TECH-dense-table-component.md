---
name: TECH-dense-table-component
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/style-details.md
---

# `dense_table` — the designer's primary data format

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [CSS](#css)
- [The signature rules](#the-signature-rules)
- [HTML](#html)
- [Usage rules](#usage-rules)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Compact reference table with colored row accents, tight cell
padding (`6px 10px`), and 11–12px font. Tables are the #1 data
format — more common than charts in the body of work. Every
infographic with comparisons, specs, rates, tiers, or requirements
should have one.

## When to use

- Specs / rates / requirements / comparisons — **mandatory**.
- Tier comparisons (Gold / Silver / Bronze equivalents).
- Multi-chain support tables.
- Eligibility tables for airdrops (65% of airdrop-guide pieces have one).

## CSS

```css
/* source: image-generation/create-infographics/SKILL.md */
.dense-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11.5px;
}
.dense-table th {
  background: rgba(var(--primary-rgb), 0.15);
  color: var(--primary);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  padding: 6px 10px;
  text-align: left;
  border-bottom: 1.5px solid rgba(var(--primary-rgb), 0.3);
}
.dense-table td {
  padding: 5px 10px;
  color: var(--text);
  border-bottom: 1px solid rgba(255,255,255,0.05);
  line-height: 1.4;
}
.dense-table tr:nth-child(even) td {
  background: rgba(255,255,255,0.03);
}
.dense-table tr:hover td {
  background: rgba(var(--primary-rgb), 0.06);
}
.dense-table .accent {
  color: var(--primary);
  font-weight: 600;
}
```

## The signature rules

- **Cell padding 6px 10px** — NOT 12px 16px (that's frontend).
- **Font size 11-12px** — NOT 14px+ (too big).
- **Alternating row tint** — `rgba(255,255,255,0.03)` on even rows.
- **Uppercase header** — `letter-spacing: 0.07em`, color = primary.
- **Left-border accent on first cell** — for tier/chain tables.

## HTML

```html
<table class="dense-table">
  <thead>
    <tr>
      <th>TIER</th>
      <th>MIN STAKE</th>
      <th>APY</th>
      <th>LOCK</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span class="tier-badge gold">GOLD</span></td>
      <td class="accent">10,000 $TKN</td>
      <td class="accent">12%</td>
      <td>90 days</td>
    </tr>
    <tr>
      <td><span class="tier-badge silver">SILVER</span></td>
      <td class="accent">1,000 $TKN</td>
      <td>8%</td>
      <td>30 days</td>
    </tr>
  </tbody>
</table>
```

## Usage rules

- Row count: 4-10 rows optimal; 12+ rows → split.
- Always pair with a section header using `.section-pill` or
  underlined header.
- For tier tables, add colored `<span class="tier-badge gold">` in
  the first cell.
- Use `.accent` class on numeric values to color them in the brand
  primary.

## Gotchas

- Padding larger than `6px 10px` breaks the density feel —
  immediately looks frontend.
- Don't use `<th scope="col">` inside `<tbody>` — semantic but
  renders weirdly. Use `<td>` for all body cells.
- Currency columns benefit from `font-variant-numeric: tabular-nums`
  — digits align in columns.

## Cross-references

- [TECH-tier-comparison-component](TECH-tier-comparison-component.md) — the badge-specific variant.
  > What it does · When to use · CSS — the base table · CSS — the tier badges · HTML · Custom tier names and colors · Gotchas · Cross-references
- [TECH-chain-color-coding](TECH-chain-color-coding.md) — for multi-chain row accents.
  > What it does · The color table · CSS tokens · Chain badge component · Table row left-border per chain · When to use · Gotchas · Cross-references
- [TECH-copy-guide-numbers](TECH-copy-guide-numbers.md) — how to format numbers inside cells.
  > What it does · The number format table · Labeling rules · Currency · Headline formulas (ALL CAPS + verb-first OR noun phrase) · Type A — Verb-first (action, how-it-works, airdrop) · Type B — Noun phrase (token-economics, stats, reports) · Type C — Mission statement (launch, profile) · Subtitle rules · Per-component word budgets · Common mistakes to avoid · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
