---
name: TECH-typography-scale
category: infographic-archetype
source: image-generation/create-infographics/resources/style-details.md
also-in: image-generation/create-infographics/resources/font-pairings.md
---

# Typography scale — minor third (1.25 ratio)

## Table of Contents

- [What it does](#what-it-does)
- [The scale](#the-scale)
- [Weight-based hierarchy](#weight-based-hierarchy)
- [Letter-spacing rules](#letter-spacing-rules)
- [Tabular numerics (mandatory for numbers)](#tabular-numerics-mandatory-for-numbers)
- [Summary rules](#summary-rules)
- [Body font size rules (the density signature)](#body-font-size-rules-the-density-signature)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Harmonious size progression based on the minor-third ratio (1.25).
Pick a base (12-14px for dense layouts, 16px for spacious), derive
the rest.

## The scale

```css
/* source: image-generation/create-infographics/resources/style-details.md */
:root {
  --text-base: 13px;             /* base for compact infographics */

  --text-xs:   10px;             /* base × 0.79 — footnotes, data labels */
  --text-sm:   11px;             /* base × 0.87 — secondary labels */
  --text-md:   13px;             /* base — body, table cells */
  --text-lg:   16px;             /* base × 1.25 — section headers */
  --text-xl:   20px;             /* base × 1.56 — card titles */
  --text-2xl:  25px;             /* base × 1.95 — subsection hero */
  --text-3xl:  32px;             /* base × 2.44 — section hero stat */
  --text-hero: 56px;             /* base × 4.3  — primary hero stat */
}
```

## Weight-based hierarchy

Size alone is weak. Pair size changes with weight changes for clear
signal:

```css
.text-context { font-weight: 300; opacity: 0.6; }  /* Context / supporting */
.text-data    { font-weight: 400; }                 /* Data values */
.text-label   { font-weight: 500; text-transform: uppercase; }  /* Labels */
.text-header  { font-weight: 700; }                 /* Headers */
.text-hero    { font-weight: 800; }                 /* Hero stat */
```

## Letter-spacing rules

```css
/* Large numbers — tighten for mass, presence */
.stat-number, .text-hero {
  letter-spacing: -0.02em;
}

/* Small caps labels — open up for legibility */
.text-label, .category-label {
  letter-spacing: 0.06em;
  text-transform: uppercase;
  font-size: var(--text-xs);
  font-weight: 600;
}

/* Body text — natural tracking */
.text-body {
  letter-spacing: 0;
}

/* Subtitle / descriptor */
.text-descriptor {
  letter-spacing: 0.02em;
  font-weight: 400;
  opacity: 0.65;
}
```

## Tabular numerics (mandatory for numbers)

```css
.stat-number, .table-cell, .bar-value, .chart-label {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum" 1;  /* fallback for older browsers */
}
```

Prevents column jitter when numbers change or animate.

## Summary rules

- Hero stats and large numbers: `letter-spacing: -0.02em`
- All-caps small labels: `0.04em` to `0.08em`
- Body text: `0` (never touch)
- Tabular-nums on all numeric elements

## Body font size rules (the density signature)

```
Dense content:  11-13px
Max body:       14px (never more)
Table cells:    11-12px
Labels (caps):  10px
Footnotes:      10px
```

Never 14-16px body — that's frontend spacing, not editorial.

## Gotchas

- `clamp()` for responsive scaling — but keep the middle value tuned
  for the canvas width (1080 or 1200).
- Don't use variable fonts at non-standard weights (e.g. 450) —
  Google Fonts sometimes strips them; stick to 400/500/600/700/800.

## Cross-references

- [TECH-font-system](TECH-font-system.md) — which fonts to use.
  > What it does · The 5 display fonts (authoritative hierarchy) · Generic fallback-only fonts (never as display) · Premium alternative pairings (2025/2026) · The body font hierarchy · Rules (non-negotiable) · Tested font pairings (top 5) · Bebas Neue + Montserrat (signature — 40%+) · Teko + Inter (esports) · Orbitron + Inter (sci-fi / DeFi) · Press Start 2P + VT323 (pixel games) · Bungee + Inter (arcade / meme) · Typography constants · Gotchas · Cross-references
- [TECH-dense-editorial-dna](TECH-dense-editorial-dna.md) — spacing and density signature.
  > What it does · The success state · The failure mode · The Anti-Frontend Checklist (run before delivery) · Density targets by canvas · Spacing rules (THE signature) · Content format hierarchy (top = prefer) · Gotchas · Cross-references
- [TECH-copy-guide-numbers](TECH-copy-guide-numbers.md) — formatting numbers for the scale.
  > What it does · The number format table · Labeling rules · Currency · Headline formulas (ALL CAPS + verb-first OR noun phrase) · Type A — Verb-first (action, how-it-works, airdrop) · Type B — Noun phrase (token-economics, stats, reports) · Type C — Mission statement (launch, profile) · Subtitle rules · Per-component word budgets · Common mistakes to avoid · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
