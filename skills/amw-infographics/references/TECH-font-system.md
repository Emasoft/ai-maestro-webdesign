---
name: TECH-font-system
category: infographic-archetype
source: image-generation/create-infographics/resources/font-pairings.md
also-in: image-generation/create-infographics/SKILL.md
---

# Font system — the 5-font display hierarchy

## What it does

The display-font hierarchy based on 175-piece analysis: 100% of
pieces use UPPERCASE labels; the display font is one of 5 specific
condensed / techno / pixel sans-serifs; body is Montserrat by
default.

## The 5 display fonts (authoritative hierarchy)

| Font | Usage | Category | Best for |
|------|-------|----------|----------|
| **Bebas Neue** | 76x / 43% | Condensed sans | Token-economics, all-purpose — **the signature** |
| **Teko** | 23x / 13% | Condensed sans | Tokenomics, esports, compact headings |
| **Orbitron** | 13x / 7% | Sci-fi display | Token-economics, game-overview |
| **Press Start 2P** | 8x / 5% | Pixel / retro | Pixel games ONLY |
| **Bungee** | 6x / 3% | Bold block | Bold, wide, high-energy |

## Generic fallback-only fonts (never as display)

**Never** use these as the display/heading font — they are body/UI
fonts, not editorial display fonts:
- Inter, Roboto, Arial, Helvetica (generic system/UI fonts)

## Premium alternative pairings (2025/2026)

These are valid display/heading choices for specific aesthetics —
**not banned**:

| Font | Category | Best for |
|------|----------|----------|
| **Space Grotesk** | Modern Geometric | Modern Web3, DeFi, tech startups (#10) |
| **Syne** | Geometric Display | Ultra-modern Web3, DeFi, tech startups (#11) |
| **Plus Jakarta Sans** | Premium Humanist Sans | Reports, ecosystem overviews, premium brands (#12) |
| **Outfit** | Clean Geometric Sans | Contemporary general use, accessible designs (#13) |

Use these when the project brief calls for a "modern," "premium," or
"approachable" aesthetic that the 5 core display fonts don't serve.
The 5-font hierarchy above is the **default**; these are opt-in
alternatives with full Google Fonts support.

## The body font hierarchy

| Font | Usage | Notes |
|------|-------|-------|
| **Montserrat** | 57% | Default workhorse |
| Avenir Next | 15% | Premium alternative |
| Inter | 13% | Clean fallback |
| Poppins | 9% | Community / friendly |

## Rules (non-negotiable)

1. ALWAYS UPPERCASE for section labels, stat labels, category tags
2. Bebas Neue is the default display font
3. Montserrat is the default body font
4. Uppercase headings are the signature

## Tested font pairings (top 5)

### Bebas Neue + Montserrat (signature — 40%+)
```css
--font-display: 'Bebas Neue', sans-serif;
--font-body: 'Montserrat', sans-serif;
```
Load: `Bebas+Neue:wght@400&family=Montserrat:wght@400;500;600;700`
Use: token-economics, airdrop-guide, crypto-explainer.

### Teko + Inter (esports)
```css
--font-display: 'Teko', sans-serif;
--font-body: 'Inter', sans-serif;
```
Use: token-economics, airdrop-guide — any layout needing a wide
uppercase headline that's more compact than Bebas Neue.

### Orbitron + Inter (sci-fi / DeFi)
```css
--font-display: 'Orbitron', sans-serif;
--font-body: 'Inter', sans-serif;
```
Use: blockchain infrastructure, DeFi, technical protocols.

### Press Start 2P + VT323 (pixel games)
```css
--font-display: 'Press Start 2P', monospace;
--font-body: 'Inter', sans-serif;
--font-mono: 'VT323', monospace;
```
Use: NFT gaming, arcade-style, pixel art projects. **Mandatory for
pixel games; never for standard games.**

### Bungee + Inter (arcade / meme)
```css
--font-display: 'Bungee', sans-serif;
--font-body: 'Inter', sans-serif;
```
Use: meme tokens, community airdrop guides, arcade energy.

## Typography constants

```css
/* source: image-generation/create-infographics/resources/font-pairings.md */
:root {
  --text-transform-label: uppercase;
  --letter-spacing-label: 0.08em;
  --letter-spacing-hero: 0.02em;

  --text-hero: clamp(36px, 5vw, 64px);    /* Main title — Bebas Neue */
  --text-h1: clamp(22px, 3vw, 36px);      /* Section headers */
  --text-h2: clamp(16px, 2vw, 22px);      /* Card titles */
  --text-body: clamp(13px, 1.4vw, 15px);  /* Body — Montserrat */
  --text-caption: clamp(10px, 1vw, 12px); /* Labels — UPPERCASE */
  --text-stat: clamp(28px, 4vw, 48px);    /* Big numbers — Bebas Neue */
  --text-mono: clamp(11px, 1.2vw, 13px);  /* Data/addresses — mono */
}
```

## Gotchas

- Pixel font for a 3D/fantasy game is wrong — research aesthetic
  first.
- Bebas Neue for a pixel game breaks the type signature — use
  Press Start 2P.
- Space Grotesk / Syne / Plus Jakarta Sans / Outfit are valid premium
  alternatives for modern/approachable aesthetics — but default to
  the 5-font hierarchy unless the brief specifically calls for them.

## Cross-references

- `TECH-typography-scale.md` — type scale and sizing rules.
- `TECH-copy-guide-numbers.md` — number formatting in headlines.
- `TECH-per-type-signature-palettes.md` — type-specific font choices.
- [`../SKILL.md`](../SKILL.md) — parent skill

