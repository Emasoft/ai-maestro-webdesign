---
name: TECH-tier-comparison-component
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [CSS — the base table](#css-the-base-table)
- [CSS — the tier badges](#css-the-tier-badges)
- [HTML](#html)
- [Custom tier names and colors](#custom-tier-names-and-colors)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# `tier_comparison` — tier badge table

## What it does

Multi-column table with tier badges (Gold / Silver / Bronze or
equivalent) for reward tiers, rarity levels, subscription levels.
The badges are the signature — colored pills identifying each tier.

## When to use

- Reward tiers (Gold / Silver / Bronze stake levels)
- NFT rarity (Common / Rare / Epic / Legendary)
- Subscription plans (Free / Pro / Enterprise)
- Any 3-4 level hierarchy where the levels need visual identity

## CSS — the base table

```css
/* source: image-generation/create-infographics/SKILL.md */
.tier-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11.5px;
}
```

## CSS — the tier badges

```css
.tier-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.05em;
}
.tier-badge.gold   { background: rgba(255,215,0,0.2);   color: #FFD700; border: 1px solid rgba(255,215,0,0.4); }
.tier-badge.silver { background: rgba(192,192,192,0.2); color: #C0C0C0; border: 1px solid rgba(192,192,192,0.4); }
.tier-badge.bronze { background: rgba(205,127,50,0.2);  color: #CD7F32; border: 1px solid rgba(205,127,50,0.4); }
```

## HTML

```html
<table class="dense-table tier-table">
  <thead>
    <tr><th>TIER</th><th>STAKE</th><th>APY</th><th>DAILY REWARD</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><span class="tier-badge gold">GOLD</span></td>
      <td>10,000+ $TKN</td>
      <td>12%</td>
      <td>33 $TKN</td>
    </tr>
    <tr>
      <td><span class="tier-badge silver">SILVER</span></td>
      <td>1,000–10k $TKN</td>
      <td>8%</td>
      <td>3 $TKN</td>
    </tr>
    <tr>
      <td><span class="tier-badge bronze">BRONZE</span></td>
      <td>100–1k $TKN</td>
      <td>5%</td>
      <td>0.2 $TKN</td>
    </tr>
  </tbody>
</table>
```

## Custom tier names and colors

Swap `gold` / `silver` / `bronze` for project-specific tier names
(Diamond / Platinum / Gold, or Common / Rare / Epic / Legendary).
Match the badge color to the tier meaning:

```css
.tier-badge.diamond    { background: rgba(85,206,250,0.2);  color: #55CEFA; border: 1px solid rgba(85,206,250,0.4); }
.tier-badge.platinum   { background: rgba(229,228,226,0.2); color: #E5E4E2; border: 1px solid rgba(229,228,226,0.4); }
.tier-badge.legendary  { background: rgba(255,69,0,0.2);    color: #FF4500; border: 1px solid rgba(255,69,0,0.4); }
```

## Gotchas

- Badge colors should read on the dark background — light colors
  (gold, silver, diamond) work. Dark colors (black, navy) don't.
- Consistent badge styling — same padding, border-radius, font-size
  for all tiers.
- Don't mix tier-badge with other badge styles on one page —
  confuses visual hierarchy.

## Cross-references

- [TECH-dense-table-component](TECH-dense-table-component.md) — the base table pattern.
  > What it does · When to use · CSS · The signature rules · HTML · Usage rules · Gotchas · Cross-references
- [TECH-game-overview-playbook](TECH-game-overview-playbook.md) — rarity tiers in game content.
  > What it does · When to use · Color system · Typography — two sub-variants · Standard game · Pixel / retro game · Standard component prevalence (across 25 pieces) · Visual properties · Signature layout pattern · Character card grid (signature pattern) · Light-mode sub-variant · CSS variables (standard) · CSS variables (pixel) · Reference template · Gotchas · Cross-references
- [TECH-signature-palette](TECH-signature-palette.md) — how tiers relate to brand colors.
  > What it does · Background rules · The default accent hierarchy · Palette temperature · Other most-used accents (in order) · Named palette recipes (top 3) · AMBER DARK (signature, most used) · CYBER TEAL · HOT PINK WEB3 · Rule — brand first, signature second · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

