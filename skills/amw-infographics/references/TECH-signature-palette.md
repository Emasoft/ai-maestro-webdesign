---
name: TECH-signature-palette
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/color-palettes.md
---
## Table of Contents

- [What it does](#what-it-does)
- [Background rules](#background-rules)
- [The default accent hierarchy](#the-default-accent-hierarchy)
- [Palette temperature](#palette-temperature)
- [Other most-used accents (in order)](#other-most-used-accents-in-order)
- [Named palette recipes (top 3)](#named-palette-recipes-top-3)
  - [AMBER DARK (signature, most used)](#amber-dark-signature-most-used)
  - [CYBER TEAL](#cyber-teal)
  - [HOT PINK WEB3](#hot-pink-web3)
- [Rule — brand first, signature second](#rule-brand-first-signature-second)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Signature palette — near-black + amber + teal/blue complement

## What it does

Defines the default palette when no brand color is provided:
near-black background (`#060606`–`#090909`), amber primary
(`#E99A00`), teal or blue complement. 99% dark mode, 90% vibrant
saturation.

## Background rules

- **Default range:** `#060606`–`#090909` (closer to pure black than
  `#0A0A0A`–`#0D0D0D`)
- **Medium-dark alternative:** `#1a1a1a`–`#1d1d1d` — valid for
  strategy guides and flow-diagram-heavy pieces
- **Light mode exceptions:** game event guides, quest cheat sheets,
  bounty pocket guides use white / light-gray backgrounds — this is
  correct, not a mistake
- "Whitepaper" / "report" context does NOT override dark mode unless
  explicitly guide/educational

## The default accent hierarchy

When no brand color given:

```
Background:         #060606–#090909  (near-black)
Primary (warm):     #E99A00           (canonical amber)
Complement (cool):  #00E88A  (teal)   OR  #29B7FF  (blue)
```

**Important:** canonical amber is `#E99A00`. All of `#E79A00`,
`#E89A00`, `#E99800`, `#F4A61A`, `#F5A623`, `#F6A615` are the same
amber — standardize to `#E99A00`.

## Palette temperature

- Mixed warm+cool (75% of pieces) — amber + teal/blue together
- Pure warm (26%) — amber-only
- Pink/magenta (`#F59AC3`, `#A764F6`) is type-specific (crypto-
  explainer) — NOT a universal default

## Other most-used accents (in order)

```
#E99A00  canonical amber/gold    — #1 color (14+ uses)
#00E88A  neon mint                — ecosystem, gaming
#11C59A  emerald teal             — gaming, DeFi
#A764F6  violet purple            — web3 premium
#F29AC3  soft pink                — community
#F39AC6  rose pink                — NFT, brand
#42F3EE  cyan neon                — retro tech
#E63946  vivid red                — gaming, competitive
#9B5DE5  purple                   — NFT, fantasy
#00D4FF  electric cyan            — DeFi, blue-chip
```

## Named palette recipes (top 3)

### AMBER DARK (signature, most used)
```
background: #0D0D0D
primary:    #E99A00  (canonical amber)
secondary:  #E8943A  (warm orange)
accent:     #F0B63A  (bright amber highlight)
text:       #FFFFFF
muted:      #8B8B8B
border:     #2A2A2A
```
Use for: token-economics, airdrop-guide, crypto-explainer.

### CYBER TEAL
```
background: #0D0D0F
primary:    #00E5CC  (teal)
secondary:  #00D4FF  (electric cyan)
accent:     #00FF85  (neon green)
text:       #FFFFFF
muted:      #7A7A9A
border:     #1E1E3A
```
Use for: ecosystem, how-it-works, DeFi.

### HOT PINK WEB3
```
background: #0D0D0D
primary:    #E91E8C  (hot pink)
secondary:  #FF69B4  (soft pink)
accent:     #E99A00  (amber gold — canonical)
text:       #FFFFFF
muted:      #8B8B8B
border:     #2D1A26
```
Use for: crypto-explainer, community, playful.

## Rule — brand first, signature second

If the user provides a hex color or logo, extract the palette from
it. Signature palette is the fallback, not the first choice.

## Gotchas

- Default tech blue is overused — avoid unless the brand explicitly
  calls for it.
- Amber variants like `#F5A623`, `#F6A615` — standardize to
  `#E99A00`. Don't ship three slightly-different ambers in one
  piece.
- The near-black range (`#060606`–`#090909`) is a tight band — use
  exact values, not "approximately dark".

## Cross-references

- [TECH-dense-editorial-dna](TECH-dense-editorial-dna.md) — the parent design philosophy.
  > What it does · The success state · The failure mode · The Anti-Frontend Checklist (run before delivery) · Density targets by canvas · Spacing rules (THE signature) · Content format hierarchy (top = prefer) · Gotchas · Cross-references
- [TECH-color-palette-recipes](TECH-color-palette-recipes.md) — all 13 named palette recipes.
  > What it does · Dark palettes (99% of work) · AMBER DARK — signature · CYBER TEAL · GAMING RED · HOT PINK WEB3 · EMERALD GAMING · ROYAL PURPLE GAMING · NAVY CRYPTO · WARM GOLD DARK · RETRO PIXEL / ARCADE · LIME CYBERPUNK · Standout palettes · NEON ACID · SUNSET HORIZON · EARTHY TECH · Light mode palettes (rare, <1%) · L1. CLEAN WHITE + AMBER · L2. WARM EDITORIAL · L3. BLUE PROFESSIONAL · Gotchas · Cross-references
- [TECH-per-type-signature-palettes](TECH-per-type-signature-palettes.md) — content-type-specific palettes.
  > What it does · The 5 major-type palettes · Why these · The full selection order · CSS variables per type · Token-Economics · Crypto-Explainer · Game-Overview · Ecosystem · Airdrop-Guide · Gotchas · Cross-references
- [TECH-chain-color-coding](TECH-chain-color-coding.md) — the multi-chain blockchain palette.
  > What it does · The color table · CSS tokens · Chain badge component · Table row left-border per chain · When to use · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
