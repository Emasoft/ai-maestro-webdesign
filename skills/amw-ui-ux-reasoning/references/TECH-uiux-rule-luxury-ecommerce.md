---
name: TECH-uiux-rule-luxury-ecommerce
category: uiux-rule
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---

# TECH: Reasoning rule — Luxury E-commerce

## What it does

Luxury is the industry where "more" is wrong and "less + better" is the entire strategy. The rule enforces editorial restraint — whitespace, type scale, and photography over animation, gradients, and grid density.

## When to use

When building for fashion, jewelry, haute couture, niche perfumery, boutique hospitality, premium spirits, high-end homeware, or any brand whose price point is the signal. This rule supersedes free style choice.

## How it works

- **Pattern** — Editorial long-form: full-bleed hero image, limited navigation, collections grid (not product grid), brand story section, newsletter capture (not sign-up-to-unlock).
- **Style priority** — `Minimalism`, `Editorial`, `Warm Minimalism`, `Swiss Minimalism`. Avoid `Claymorphism`, `Bento Grid` (both read as consumer, not luxury).
- **Color mood** — Black + gold, off-white + warm ink, deep ivory + muted metallic. Never primary bright colors; luxury speaks in tone, not hue.
- **Anti-patterns** —
  - Cluttered layouts (3+ hero CTAs = deal-of-the-day feel)
  - Too many CTAs ("Buy now" + "Add to cart" + "Save for later" on one screen = discount site)
  - Comic-Sans-adjacent fonts, playful scripts (use Didot / Cormorant / Playfair for headings)
  - Rainbow gradients, neon, overly saturated photography
  - Emoji as primary icons, emoji in copy
  - Badge overload (NEW / SALE / HOT — all of these erode luxury)

## Minimal example

```python
ds = gen.generate(
    description="Boutique Italian leather goods ecommerce",
    stack="nextjs"
)
# Pattern:   "Editorial Long-form"
# Style:     "Minimalism + Editorial"
# Colors:    Primary #0D0D0D, Background #FFFFFF, CTA #B8860B (gold), Text #1A1A1A
# Fonts:     Playfair Display / Source Sans 3
# Hero:      full-bleed product photo, minimal copy, one CTA ("Discover" / "Explore")
# Avoid:     bento grids, gradient CTAs, rainbow badges, emoji
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- "Luxury" is not "premium". Premium (SaaS enterprise, premium ecom like Apple) can use bento grids and richer palettes. True luxury (Hermès, Loro Piana, boutique jewelry) stays minimal.
- Photography is the lead — the design is a frame around the photography. If the product photography is weak, no design system will rescue the brand.
- Casual luxury (Aesop, Glossier) inverts some rules (rounded type, warm pastels) but still obeys the anti-patterns (no neon, no badge overload, generous whitespace).

## Cross-references

- `TECH-uiux-rules-catalog.md`
- `TECH-uiux-pre-delivery-checklist.md`
- `../SKILL.md`
- `../../amw-design-principles/ai-slop-avoid.md`
