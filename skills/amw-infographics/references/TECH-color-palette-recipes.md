---
name: TECH-color-palette-recipes
category: infographic-archetype
source: image-generation/create-infographics/resources/color-palettes.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [Dark palettes (99% of work)](#dark-palettes-99-of-work)
  - [1. AMBER DARK — signature](#1-amber-dark-signature)
  - [2. CYBER TEAL](#2-cyber-teal)
  - [3. GAMING RED](#3-gaming-red)
  - [4. HOT PINK WEB3](#4-hot-pink-web3)
  - [5. EMERALD GAMING](#5-emerald-gaming)
  - [6. ROYAL PURPLE GAMING](#6-royal-purple-gaming)
  - [7. NAVY CRYPTO](#7-navy-crypto)
  - [8. WARM GOLD DARK](#8-warm-gold-dark)
  - [9. RETRO PIXEL / ARCADE](#9-retro-pixel-arcade)
  - [10. LIME CYBERPUNK](#10-lime-cyberpunk)
- [Standout palettes](#standout-palettes)
  - [11. NEON ACID](#11-neon-acid)
  - [12. SUNSET HORIZON](#12-sunset-horizon)
  - [13. EARTHY TECH](#13-earthy-tech)
- [Light mode palettes (rare, <1%)](#light-mode-palettes-rare-1)
  - [L1. CLEAN WHITE + AMBER](#l1-clean-white-amber)
  - [L2. WARM EDITORIAL](#l2-warm-editorial)
  - [L3. BLUE PROFESSIONAL](#l3-blue-professional)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# 13 named palette recipes

## What it does

Complete catalog of the 13 named palette recipes extracted from the
175-piece body of work. Each is a complete CSS-variable set —
background, primary, secondary, accent, text, muted, border, and
sometimes glow.

## Dark palettes (99% of work)

### 1. AMBER DARK — signature
```
bg: #0D0D0D  primary: #E99A00  secondary: #E8943A  accent: #F0B63A
```
Mood: bold, crypto-native, premium. Use: token-economics, airdrop-guide.

### 2. CYBER TEAL
```
bg: #0D0D0F  primary: #00E5CC  secondary: #00D4FF  accent: #00FF85
```
Mood: futuristic, technical, web3. Use: ecosystem, how-it-works, DeFi.

### 3. GAMING RED
```
bg: #0A0A0A  primary: #E63946  accent: #FF2D2D  secondary: #E99A00
```
Mood: energetic, gaming, competitive. Use: game-overview, NFT showcase.

### 4. HOT PINK WEB3
```
bg: #0D0D0D  primary: #E91E8C  secondary: #FF69B4  accent: #E99A00
```
Mood: bold, community-driven, playful. Use: crypto-explainer.

### 5. EMERALD GAMING
```
bg: #0A0F0A  primary: #00E5A0  secondary: #7CFC00  accent: #00FF6A  glow: #00E5A0
```
Mood: gaming, fantasy, rewarding. Use: play-to-earn, NFT.

### 6. ROYAL PURPLE GAMING
```
bg: #0D0D12  primary: #9B5DE5  secondary: #E535AB  accent: #E99A00  glow: #9B5DE5
```
Mood: mystical, fantasy, legendary tier. Use: NFT character.

### 7. NAVY CRYPTO
```
bg: #0D1117  primary: #00D4FF  secondary: #0066FF  accent: #00FF85
```
Mood: professional, trustworthy. Use: DeFi protocol, comparison.

### 8. WARM GOLD DARK
```
bg: #0A0A0A  primary: #D4A84B  secondary: #C4A35A  accent: #F5C518
```
Mood: exclusive, premium. Use: VIP tiers, special events.

### 9. RETRO PIXEL / ARCADE
```
bg: #0A1628  primary: #00E5C7  secondary: #FF9500  accent: #E99A00  glow: #00E5C7
```
Mood: retro-gaming, nostalgic. Use: pixel art NFT, retro games.

### 10. LIME CYBERPUNK
```
bg: #0D0D0D  primary: #BFFF00  secondary: #7CFC00  accent: #FFFFFF  glow: #BFFF00
```
Mood: cyberpunk, energetic. Use: airdrop, DePIN.

## Standout palettes

### 11. NEON ACID
```
bg: #0D0D0D  primary: #DFFF00  secondary: #FF00FF  accent: #00FFFF
```
Mood: disruptive, high-energy. Use: bold announcements.

### 12. SUNSET HORIZON
```
bg: #0A0A0A  primary: #FF4D00  secondary: #FFB700  accent: #4A00E0
```
Mood: warm, premium, high-contrast. Use: luxury web3 brands.

### 13. EARTHY TECH
```
bg: #0D0D0D  primary: #A3B18A  secondary: #588157  accent: #E99A00
```
Mood: sustainable, organic. Use: DePIN, green crypto.

## Light mode palettes (rare, <1%)

### L1. CLEAN WHITE + AMBER
```
bg: #FFFFFF  surface: #F7F7F8  primary: #F5A623  text: #0D0D0D
```
Use: reports, investor decks on white.

### L2. WARM EDITORIAL
```
bg: #FAFAF8  surface: #F0F0EC  primary: #D4A84B  text: #1A1A1A
```
Use: NFT editorial, premium one-pagers.

### L3. BLUE PROFESSIONAL
```
bg: #F8FAFF  surface: #FFFFFF  primary: #2563EB  text: #111827
```
Use: DeFi reports, investment summaries, fintech.

## Gotchas

- Glow effects disabled on light backgrounds — they look wrong on
  white.
- Don't mix palettes in one piece — pick one recipe per infographic.
- Cards on light backgrounds get box-shadow instead of glow.

## Cross-references

- [TECH-signature-palette](TECH-signature-palette.md) — the default when no recipe is picked.
  > What it does · Background rules · The default accent hierarchy · Palette temperature · Other most-used accents (in order) · Named palette recipes (top 3) · AMBER DARK (signature, most used) · CYBER TEAL · HOT PINK WEB3 · Rule — brand first, signature second · Gotchas · Cross-references
- [TECH-glow-system](TECH-glow-system.md) — the glow layer on top of these palettes.
  > What it does · The glow system · Double-layer glow pattern · Top confirmed glow colors · When to use each · Light-mode override · Gotchas · Cross-references
- [TECH-per-type-signature-palettes](TECH-per-type-signature-palettes.md) — when the content type
  > What it does · The 5 major-type palettes · Why these · The full selection order · CSS variables per type · Token-Economics · Crypto-Explainer · Game-Overview · Ecosystem · Airdrop-Guide · Gotchas · Cross-references
  dictates the palette.
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

