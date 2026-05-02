---
name: TECH-airdrop-guide-playbook
category: infographic-archetype
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Color system](#color-system)
- [Typography](#typography)
- [Standard component prevalence (across 17 pieces)](#standard-component-prevalence-across-17-pieces)
- [Visual properties](#visual-properties)
- [Signature layout pattern](#signature-layout-pattern)
- [The amber+blue value split (signature)](#the-amberblue-value-split-signature)
- [The claim-steps horizontal flow](#the-claim-steps-horizontal-flow)
- [CSS variables](#css-variables)
- [Reference template](#reference-template)
- [Archetype preference](#archetype-preference)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Airdrop-Guide playbook — 10% (17/175)

## What it does

The playbook for airdrop-guide infographics — how-to-claim tokens,
eligibility tables, vesting schedules, step-by-step claim flows.
Amber + blue split signature (earned vs locked values).

## When to use

Content involves: airdrop eligibility, how to claim, eligibility
tiers, claim steps, post-claim vesting.

## Color system

- **Primary:** amber `#E79A00`–`#F0A11A` (dominant, high urgency)
- **Secondary:** blue `#61B8FF` / `#4DA5F0` / `#10D7F4`
- **The signature split:** amber = earned/unlocked values, blue =
  locked/future values
- **Background:** solid (71%), image-overlay (24%)
- **Temperature:** mixed (94%)
- **Saturation:** vibrant (94%)

## Typography

- **Display:** Bebas Neue (47%), Montserrat Bold/Black (24%), Teko (18%)
- **Body:** Montserrat (41%), Avenir Next (29%), Inter (18%)

## Standard component prevalence (across 17 pieces)

| Component | Prevalence | Notes |
|-----------|------------|-------|
| Footer | **82%** | Near-universal |
| **Comparison / eligibility table** | **65%** | THE primary data structure |
| Stats bar | 41% | |
| Callout box | 41% | |
| Timeline (horizontal steps) | 35% | Numbered claim steps |
| Progress bars | 24% | Vesting unlock |
| Numbered list | 24% | Eligibility steps |

## Visual properties

- **Glow:** moderate (41%)
- **Geometric shapes:** 71%
- **Border radius:** mixed (35%), rounded 8-16px (35%), slight (29%)
- **Card style:** outlined (41%), none (24%)
- **Density:** compact (76%)

## Signature layout pattern

```
BRAND HEADER (logo + project name + "AIRDROP GUIDE" label)
  ↓
HERO with KEY STATS
  Headline: "HOW TO CLAIM YOUR [TOKEN] AIRDROP"
  Stat strip: Total Allocation | TGE % | Snapshot Date | Deadline
  ↓
OVERVIEW (bordered_section with 4-6 bullets)
  What, who qualifies, when, how much
  ↓
ELIGIBILITY TABLE (dense_table — THE main content)
  Tier | Requirement | Allocation | % of Pool
  Color-coded tier badges (Gold/Silver/Bronze)
  ↓ [arrow: "eligibility → claim steps"]
CLAIM STEPS (step_process, full-width)
  1 → 2 → 3 → 4 numbered steps with arrows
  Connect Wallet → Check Eligibility → Claim → Stake
  ↓
VESTING SCHEDULE TABLE (dense_table)
  Phase | Date | % Unlock | Cumulative %
  ↓ [vesting progress bar below]
PLAYER REQUIREMENTS (bullet_panel)
  What to hold/do before snapshot
  ↓
REWARD BREAKDOWN TABLE
  Reward type | Amount | Condition | Lock period
  ↓
FOOTER (warning / disclaimer)
```

## The amber+blue value split (signature)

Apply the split to the eligibility / reward tables:

```css
.tier-badge.earned    { background: rgba(231,154,0,0.2); color: #E79A00; border: 1px solid rgba(231,154,0,0.4); }
.tier-badge.locked    { background: rgba(97,184,255,0.2); color: #61B8FF; border: 1px solid rgba(97,184,255,0.4); }
/* Example:                                                                                                                  */
/* TGE 10% unlocked     → amber text                                                                                          */
/* Remaining 90% locked → blue text                                                                                           */
```

## The claim-steps horizontal flow

The step-process must be horizontal with arrows for this playbook —
not vertical. Creates the "1 → 2 → 3 → 4" action feel.

## CSS variables

```css
--bg: #080808;
--primary: #E79A00;
--secondary: #61B8FF;
--text: #FFFFFF;
--muted: #8B8B8B;
```

## Reference template

`templates/airdrop-guide.html`

## Archetype preference

**Cheat Sheet** is the default archetype — airdrop guides are the
most "pocket guide" type. Stacked Reference is the alternative for
simpler guides.

## Gotchas

- Eligibility table is MANDATORY (65% prevalence). Don't ship an
  airdrop guide without one.
- Amber+blue split is the type signature — use it consistently for
  earned/locked throughout the piece.
- Footer must include disclaimer: "Not financial advice. DYOR."

## Cross-references

- [TECH-per-type-signature-palettes](TECH-per-type-signature-palettes.md) — the color system.
- [TECH-cheat-sheet-archetype](TECH-cheat-sheet-archetype.md) — the default archetype.
- [TECH-step-process-component](TECH-step-process-component.md) — the claim steps.
- [TECH-dense-table-component](TECH-dense-table-component.md) — the eligibility table.
- [TECH-progress-bar-vesting](TECH-progress-bar-vesting.md) — the vesting bar.
- [`../SKILL.md`](../SKILL.md) — parent skill

