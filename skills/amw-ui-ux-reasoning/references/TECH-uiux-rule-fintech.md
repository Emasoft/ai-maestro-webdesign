---
name: TECH-uiux-rule-fintech
category: uiux-rule
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---

# TECH: Reasoning rule — Fintech / Crypto / Banking

## What it does

Fintech is the category where the gap between "looks modern" and "erodes trust" is widest. The rule encodes the industry's specific anti-patterns and the structural choices that restore trust.

## When to use

When the fallback library is proposing candidates for a fintech, crypto, banking, payments, or trading product. This rule supersedes style and palette free choice — even if the user says "make it look fun", fintech constraints override.

## How it works

Four decisions the rule hard-codes:

- **Pattern** — Data-first hero (not testimonial-first, not illustration-first). Compliance footer (licenses, regulatory IDs, risk disclosure) visible.
- **Style priority** — `Professional Minimalism`, `Data-Dense UI`, `Swiss Minimalism`. Never `Claymorphism`, `Neumorphism`, `AI-Native UI`.
- **Color mood** — Deep blue / neutral grey / trust-green or navy-black combinations. Primary actions use cool tones, not red (red = error / loss).
- **Anti-patterns** —
  - Playful rounded fonts (use geometric sans — Inter Tight, IBM Plex Sans, Space Grotesk)
  - Neon colors (erodes institutional credibility)
  - Purple/pink AI gradients (ai-slop + "we're a crypto scam" coding)
  - Excessive motion on financial data (nauseating + untrustworthy)
  - Gamification on serious actions (confetti when you send $50k is not reassuring)
  - Emoji as primary icons (always Lucide / Heroicons / SF Symbols / Phosphor)

## Minimal example

```python
ds = gen.generate(
    description="Personal finance tracker with budgeting and investments",
    stack="react-native"
)
print(ds.anti_patterns)
# [
#   "Playful rounded fonts (use geometric sans)",
#   "Bright neon colors (erode trust)",
#   "AI purple/pink gradients",
#   "Excessive animations on financial data",
#   "Gamification elements on serious financial actions"
# ]
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- The rule is protective, not restrictive. Fintech products can still be beautiful — see Ramp, Mercury, Wise, Plaid. All share geometric sans, cool palettes, and generous whitespace.
- Crypto products sometimes ship the anti-patterns intentionally (neon + emoji to signal "fun degen"). That is a user-explicit choice — the rule still warns, user overrides.
- The "red = loss" convention inverts in some markets (Chinese exchanges use red for gains). If building for that market, override the color rule via user-explicit instruction.

## Cross-references

- `TECH-uiux-rules-catalog.md`
- `../SKILL.md`
- `../../amw-design-principles/ai-slop-avoid.md`
- `TECH-uiux-pre-delivery-checklist.md`
