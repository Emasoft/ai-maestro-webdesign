---
name: TECH-copy-guide-numbers
category: infographic-archetype
source: image-generation/create-infographics/resources/copy-guide.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The number format table](#the-number-format-table)
- [Labeling rules](#labeling-rules)
- [Currency](#currency)
- [Headline formulas (ALL CAPS + verb-first OR noun phrase)](#headline-formulas-all-caps-verb-first-or-noun-phrase)
  - [Type A — Verb-first (action, how-it-works, airdrop)](#type-a-verb-first-action-how-it-works-airdrop)
  - [Type B — Noun phrase (token-economics, stats, reports)](#type-b-noun-phrase-token-economics-stats-reports)
  - [Type C — Mission statement (launch, profile)](#type-c-mission-statement-launch-profile)
- [Subtitle rules](#subtitle-rules)
- [Per-component word budgets](#per-component-word-budgets)
- [Common mistakes to avoid](#common-mistakes-to-avoid)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Number formatting rules

## What it does

Numbers in infographics compete for space. **Cut 40% of what you
write first.** Lead with the number; format it for scannability;
never show raw digits.

## The number format table

| Raw value | Wrong | Right |
|-----------|-------|-------|
| 1,000,000,000 | 1000000000 | **1B** |
| 69,000,000,000 | 69000000000 | **69B** |
| 500,000,000 | 500,000,000 | **500M** |
| 1,500,000 | 1500000 | **1.5M** |
| 0.000123 | 0.000123 | **$0.0001** |
| 157,432 | 157432 | **157K** |
| 45.7% | 45.70% | **45.7%** |
| $12,000,000 | $12,000,000 | **$12M** |

## Labeling rules

- Label always UPPERCASE
- Positioned BELOW the number
- Shortest unambiguous label possible

```
✅ TOTAL SUPPLY      ❌ Total Token Supply
✅ AIRDROP POOL      ❌ Total Tokens for Airdrop
✅ TGE PRICE         ❌ Token Price at TGE Launch
✅ FDV               ❌ Fully Diluted Valuation
✅ STAKING APY       ❌ Annual Percentage Yield
```

## Currency

- Always prefix `$` for USD
- Crypto price: max 4 sig figs → `$0.0234` not `$0.023400`
- Billions: `$1.2B` | Millions: `$3.4M` | Thousands: `$56K`

## Headline formulas (ALL CAPS + verb-first OR noun phrase)

### Type A — Verb-first (action, how-it-works, airdrop)
```
HOW [PROJECT] WORKS
CLAIM YOUR [TOKEN] AIRDROP
STAKE, EARN, REPEAT
PLAY. EARN. OWN.
```

### Type B — Noun phrase (token-economics, stats, reports)
```
[PROJECT] TOKENOMICS
THE [PROJECT] ECOSYSTEM
Q4 2025 HIGHLIGHTS
[PROJECT] × [PARTNER] INTEGRATION
```

### Type C — Mission statement (launch, profile)
```
THE FUTURE OF [CATEGORY]
[PROJECT]: REDEFINING [THING]
[STAT] [UNIT]. [BOLD CLAIM].
```

## Subtitle rules

- NOT uppercase — sentence case or title case
- Max 12 words
- Complement the headline — don't repeat it

```
✅ Headline: BYBIT × AVAIL INTEGRATION
   Subtitle: Seamless cross-chain bridging, live February 2026

❌ Headline: BYBIT × AVAIL INTEGRATION
   Subtitle: THE BYBIT AND AVAIL INTEGRATION IS NOW LIVE  ← redundant, wrong case
```

## Per-component word budgets

| Component | Title | Body | Labels |
|-----------|-------|------|--------|
| **Hero title** | 3-6 words | — | — |
| **Hero subtitle** | — | 8-12 words | — |
| **Stat card** | — | — | 1-3 words UPPERCASE |
| **Feature card title** | 2-4 words | — | — |
| **Feature card body** | — | 15-25 words MAX | — |
| **Timeline node** | 2-4 words | 8-15 words | Date/quarter |
| **Comparison row** | 2-3 words | — | 1-2 words per cell |
| **Footer** | — | 5-15 words | — |
| **Callout/alert** | 2-4 words | 10-20 words | — |
| **Badge/tag** | 1-2 words | — | — |

If your feature card body exceeds 25 words, you're writing an
article. Cut it.

## Common mistakes to avoid

| Don't | Do Instead |
|-------|------------|
| "The total token supply is 1 billion" | **1B TOTAL SUPPLY** |
| "Users can earn rewards by staking" | **STAKE & EARN** |
| "TVL: $2.4M" | **$2.4M TVL** (number first) |
| "Token Allocation" | **TOKEN ALLOCATION** |
| Paragraph inside a card | Bullet list, one fact per line |
| Uncolored `$TOKEN` | `<span class="highlight">$TOKEN</span>` |

## Gotchas

- Rounding — `$1,500,000` → `$1.5M` OK. `$1,512,345` → `$1.5M` also
  OK. The precision isn't the point; scannability is.
- `$0.0234` not `$0.02`. For crypto, sub-cent matters.
- `font-variant-numeric: tabular-nums` makes formatted numbers
  align properly in tables.

## Cross-references

- [TECH-typography-scale](TECH-typography-scale.md) — size rules for hero numbers.
- [TECH-copy-guide-bullets](TECH-copy-guide-bullets.md) — bullet list rules.
- [TECH-inline-token-coloring](TECH-inline-token-coloring.md) — `$TOKEN` span styling.
- [`../SKILL.md`](../SKILL.md) — parent skill

