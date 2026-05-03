---
name: TECH-design-brief
category: infographic-builder
source: image-generation/create-infographics/resources/design-brief.md
also-in: image-generation/create-infographics/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [The 3 minimum questions](#the-3-minimum-questions)
- [The 5 full-brief questions](#the-5-full-brief-questions)
- [Aesthetic direction mapping (Question 2)](#aesthetic-direction-mapping-question-2)
- [Rules](#rules)
- [Skip-brief defaults](#skip-brief-defaults)
- [Thesis extraction (from data)](#thesis-extraction-from-data)
  - [Thesis formula](#thesis-formula)
- [Tone → palette mapping](#tone-palette-mapping)
- [Audience sophistication → density](#audience-sophistication-density)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Design Brief — 3 (or 5) intake questions

## What it does

Before mode detection or design work, collect the design brief.
Minimum 3 questions (SKILL.md); richer 5-question version in
`resources/design-brief.md` maps answers to concrete design
decisions.

## The 3 minimum questions

1. **Brand** — project name, logo URL or hex color (or "none")
2. **Platform** — Twitter/X | Instagram | Default (portrait 1080×1440)
3. **Key insight** — the one number or fact viewers must remember
   (or "extract from data")

## The 5 full-brief questions

1. **Brand color** — hex code, logo URL, color name, or "none"
2. **Aesthetic direction** — A-F (see mapping below)
3. **Platform** — Twitter/X, Instagram, LinkedIn, Website, Print
4. **Hero insight** — the one number or idea
5. **Hard constraints** — colors to avoid, tone requirements

## Aesthetic direction mapping (Question 2)

| Option | Label | Background | Primary | Typography | Decoration |
|--------|-------|------------|---------|------------|------------|
| A | Editorial/Clean | `#FAFAF9` or `#111111` | Muted single | Serif + sans data | Minimal |
| B | **Bold/Cyber (default)** | `#0D0D0D` | Neon (cyan, amber, lime) | Sans-serif, tight | Glows, gradients |
| C | Premium/Luxury | `#0A0A0A` | Gold `#C9A84C` or silver | Serif + condensed sans | Thin borders, no clutter |
| D | Corporate/Trust | `#FFFFFF` or `#F4F6F8` | Brand blue/navy | Clean sans-serif | Light shadows, no glows |
| E | Playful/Loud | `#F5F0E8` or vivid | Saturated multi-color | Rounded sans | Bold shapes |
| F | Custom | User-defined | User-defined | Follow user | Follow user |

**Reduction pass strictness:**
- A, C, D → strict
- B, E → loose
- F → match user intent

## Rules

- Run before any mode detection or design work
- If user already answered in the initial message, skip — don't re-ask
- If user says "just do it", "skip", or doesn't answer, proceed with
  defaults and note the assumptions

## Skip-brief defaults

| Question skipped | Default |
|------------------|---------|
| Brand color | No brand — use aesthetic palette only |
| Aesthetic | **B (Bold/Cyber)** — the skill's native style |
| Platform | LinkedIn (1200 × 627) |
| Hero insight | Extract from data or ask one targeted question |
| Hard constraints | None — full creative latitude |

How to communicate defaults:
> "No brief provided — proceeding with: Bold/Cyber aesthetic,
> LinkedIn format, no brand color. Hero insight extracted as: [X].
> Building now."

State and proceed.

## Thesis extraction (from data)

Extract a single declarative thesis:

```
User gives: "Monthly active users: Jan 1.2M, Feb 1.4M, Mar 1.9M, Apr 2.6M"
→ Thesis: "User growth is accelerating, not just growing"
→ Hero stat: +117% growth, Jan-Apr
→ Supporting: month-over-month acceleration rate
```

### Thesis formula

```
[Subject] [verb] [insight] — proven by [hero stat].
```

Examples:
- "Remote work increases output — 23% productivity gain"
- "DeFi adoption is driven by yield — 78% of users entered during
  high-APY windows"
- "Engagement peaks early — 60% of impressions in first 6 hours"

If no clear thesis: present two candidates and ask which direction.

## Tone → palette mapping

| Tone | Signal words | Palette | Avoid |
|------|-------------|---------|-------|
| Authoritative | "proves", "data shows" | Deep navy or black | Bright neon, pastels |
| Alarming / Urgent | "crisis", "risk" | Dark + red or amber | Blues, greens |
| Optimistic / Growth | "growth", "up" | Dark + green or brand | Reds, oranges |
| Friendly | "join", "together" | Light warm | Heavy glows |
| Premium / Exclusive | "unveil", "limited" | Near-black + gold/silver | Saturated neons |
| Analytical | "breakdown", "comparison" | Dark or light + muted | Multi-color |

## Audience sophistication → density

| Audience | Density | Labels | Vocabulary |
|----------|---------|--------|------------|
| General public | Low (3-5 points) | Full descriptive | Plain, no acronyms |
| Industry-savvy | Medium (6-9) | Short + context | Industry terms |
| Expert | High (10-14) | Terse, precise | Full vocabulary |
| Executive | Very low (1-3 hero stats) | Bold callouts | Business outcomes |

## Gotchas

- Don't re-ask questions the user already answered.
- State defaults explicitly — "Skipping brand, using Bold/Cyber
  default" — so the user can course-correct.
- Extract thesis from data, don't invent it.

## Cross-references

- [TECH-interactive-builder-mode](TECH-interactive-builder-mode.md) — brief runs before A1.
  > What it does · When to use · The flow · State file — `.infographic/{project}.json` · Preview server · The approval gate (A4) · State schema per component · Why verbatim HTML · Session resume · Gotchas · Cross-references
- [TECH-one-shot-mode](TECH-one-shot-mode.md) — brief runs before Step 1.
  > What it does · When to use · The 5 steps · Classification — identify the type · Composition archetype — pick one · Build rules · Head elements (required) · Step 5 — export command · Gotchas · Cross-references
- [TECH-signature-palette](TECH-signature-palette.md) — the Bold/Cyber default palette.
  > What it does · Background rules · The default accent hierarchy · Palette temperature · Other most-used accents (in order) · Named palette recipes (top 3) · AMBER DARK (signature, most used) · CYBER TEAL · HOT PINK WEB3 · Rule — brand first, signature second · Gotchas · Cross-references
- [TECH-platform-sizing](TECH-platform-sizing.md) — Question 3 mapping.
  > What it does · The size table · Safe zones per platform · CSS — fixed-aspect platforms · Font size scaling by platform · Density by format · Watermark / attribution per platform · Export commands · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

