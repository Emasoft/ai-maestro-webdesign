---
name: TECH-chain-color-coding
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/style-details.md
---
## Table of Contents

- [What it does](#what-it-does)
- [The color table](#the-color-table)
- [CSS tokens](#css-tokens)
- [Chain badge component](#chain-badge-component)
- [Table row left-border per chain](#table-row-left-border-per-chain)
- [When to use](#when-to-use)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Blockchain chain color-coding

## What it does

When a protocol lists supported chains, each chain's identifier gets
its official brand color. Ethereum blue, Arbitrum orange, Solana
purple, etc. This is a mandatory convention for multi-chain content.

## The color table

```
Ethereum   #627EEA  blue
Arbitrum   #E87030  orange
Solana     #9945FF  purple
BNBChain   #F3BA2F  yellow
Base       #0052FF  dark blue
Polygon    #8247E5  violet
Avalanche  #E84142  red
Optimism   #FF0420  red
```

## CSS tokens

```css
/* source: image-generation/create-infographics/resources/style-details.md */
.chain-eth   { --chain-color: #627EEA; }
.chain-arb   { --chain-color: #E87030; }
.chain-sol   { --chain-color: #9945FF; }
.chain-bnb   { --chain-color: #F3BA2F; }
.chain-base  { --chain-color: #0052FF; }
.chain-poly  { --chain-color: #8247E5; }
.chain-avax  { --chain-color: #E84142; }
.chain-op    { --chain-color: #FF0420; }
```

## Chain badge component

```css
.chain-badge {
  background: rgba(var(--chain-color-rgb), 0.12);
  border: 1px solid rgba(var(--chain-color-rgb), 0.3);
  color: var(--chain-color);
  font-size: 8.5px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 2px;
}
```

HTML:
```html
<span class="chain-badge chain-eth">ETH</span>
<span class="chain-badge chain-arb">ARB</span>
<span class="chain-badge chain-sol">SOL</span>
```

## Table row left-border per chain

```css
.chain-row-eth td:first-child  { border-left: 3px solid #627EEA; }
.chain-row-arb td:first-child  { border-left: 3px solid #E87030; }
.chain-row-sol td:first-child  { border-left: 3px solid #9945FF; }
.chain-row-bnb td:first-child  { border-left: 3px solid #F3BA2F; }
.chain-row-base td:first-child { border-left: 3px solid #0052FF; }
```

HTML:
```html
<table class="dense-table">
  <tr class="chain-row-eth">
    <td><span class="chain-badge chain-eth">ETH</span></td>
    <td>Uniswap V3</td>
    <td>$1.2B TVL</td>
  </tr>
  <tr class="chain-row-arb">
    <td><span class="chain-badge chain-arb">ARB</span></td>
    <td>GMX</td>
    <td>$400M TVL</td>
  </tr>
</table>
```

## When to use

- Multi-chain DeFi protocols listing supported chains.
- Cross-chain bridge interfaces.
- Ecosystem directories spanning multiple chains.
- Any content where chain identity matters to the reader.

## Gotchas

- Use the OFFICIAL chain brand colors, not derived ones. Users
  recognize these immediately.
- `--chain-color-rgb` requires a separate RGB version for `rgba()` —
  convert each hex or use a helper.
- Don't mix chain colors with brand accent colors in the same
  section — the reader can't tell which is which.

## Cross-references

- [TECH-dense-table-component](TECH-dense-table-component.md) — the table this pattern lives in.
- [TECH-ecosystem-playbook](TECH-ecosystem-playbook.md) — multi-chain ecosystems use this
  heavily.
- [TECH-signature-palette](TECH-signature-palette.md) — brand colors (which don't override
  chain colors).
- [`../SKILL.md`](../SKILL.md) — parent skill

