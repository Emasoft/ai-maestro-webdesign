---
name: TECH-per-type-signature-palettes
category: infographic-archetype
source: image-generation/create-infographics/resources/color-palettes.md
also-in: image-generation/create-infographics/SKILL.md
---

# Per-content-type signature palettes

## What it does

When the content type is known — token-economics, crypto-explainer,
game-overview, ecosystem, airdrop-guide — use the type's signature
palette as the starting point. Only deviate if the user's brand
overrides it.

## The 5 major-type palettes

| Type | Primary | Secondary | Background |
|------|---------|-----------|------------|
| **token-economics** | amber `#E99A00` | blue `#29B7FF` | `#080808` |
| **crypto-explainer** | pink `#F59AC3` or purple `#A764F6` | gold `#F4BC2F` | `#080808` |
| **game-overview** | amber `#F6A91A` or purple `#A94CFF` | complementary | `#070707` |
| **ecosystem** | teal `#00E88A` | purple `#B98AFF` | `#080808` |
| **airdrop-guide** | amber `#E79A00` | blue `#61B8FF` | `#080808` |

## Why these

Each emerged from analyzing 175 pieces:
- token-economics: 62 pieces, amber dominant — crypto-native urgency
- crypto-explainer: 29 pieces, pink/purple dominant — playful educational
- game-overview: 25 pieces, amber-or-purple split — action or mystical
- ecosystem: 22 pieces, teal dominant — freshness and growth
- airdrop-guide: 17 pieces, amber + blue split — earned vs locked values

## The full selection order

1. If user provides a brand color (hex or logo) → extract palette
   from it.
2. Else if content type maps to one of 5 playbooks → use that
   type's signature palette.
3. Else → fall back to AMBER DARK signature palette.

## CSS variables per type

### Token-Economics
```css
--bg: #080808;
--primary: #E99A00;
--secondary: #29B7FF;
--text: #FFFFFF;
--muted: #8B8B8B;
```

### Crypto-Explainer
```css
--bg: #080808;
--primary: #A764F6;
--secondary: #F4BC2F;
--glow: rgba(167,100,246,0.3);
--text: #FFFFFF;
--muted: #8B8B8B;
```

### Game-Overview
```css
--bg: #070707;
--primary: #F6A91A;
--secondary: #A94CFF;
--glow: rgba(246,169,26,0.25);
--text: #FFFFFF;
--muted: #8B8B8B;
```

### Ecosystem
```css
--bg: #080808;
--primary: #00E88A;
--secondary: #B98AFF;
--glow: rgba(0,232,138,0.2);
--text: #FFFFFF;
--muted: #8B8B8B;
```

### Airdrop-Guide
```css
--bg: #080808;
--primary: #E79A00;
--secondary: #61B8FF;
--text: #FFFFFF;
--muted: #8B8B8B;
```

## Gotchas

- These are defaults. Always defer to user-provided brand colors.
- Type detection should happen EARLY — state the type in the plan so
  the palette choice is explicit.
- The amber+blue split in airdrop-guides is the type signature —
  amber for earned/unlocked, blue for locked/future.

## Cross-references

- [TECH-signature-palette](TECH-signature-palette.md) — the universal default.
- [TECH-color-palette-recipes](TECH-color-palette-recipes.md) — named alternative palettes.
- [TECH-token-economics-playbook](TECH-token-economics-playbook.md) — the token-economics type rules.
- [TECH-crypto-explainer-playbook](TECH-crypto-explainer-playbook.md) — crypto-explainer type rules.
- [TECH-game-overview-playbook](TECH-game-overview-playbook.md) — game-overview type rules.
- [TECH-ecosystem-playbook](TECH-ecosystem-playbook.md) — ecosystem type rules.
- [TECH-airdrop-guide-playbook](TECH-airdrop-guide-playbook.md) — airdrop-guide type rules.
- [`../SKILL.md`](../SKILL.md) — parent skill

