---
name: TECH-uiux-rule-food-restaurant
category: uiux-rule
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---

# TECH: Reasoning rule — Food / Restaurant / Hospitality

## What it does

Food sites are photography-led. The rule enforces warm color temperature, photography-forward hero, and rigorous contrast rules so that text on food photos remains legible.

## When to use

When building for restaurants, meal-kit services, specialty grocers, food delivery, cafes, boutique hospitality, or any product where appetizing imagery is the primary conversion driver.

## How it works

- **Pattern** — Photography-forward: hero is a single large food image (no carousel). Menu/offering preview above fold. Location + hours/reservation CTA visible early.
- **Style priority** — `Warm Minimalism`, `Editorial`, `Minimalism`. Avoid `Glassmorphism` (cold + tech-forward, fights food warmth), `Cyberpunk` (obviously wrong).
- **Color mood** — Warm neutrals (cream, sand, warm off-white); appetizing reds (tomato, paprika); earthy tones (olive, rust, mustard). Cool blues as primary are wrong — read as tech/medical, not food.
- **Anti-patterns** —
  - Cold blues as primary (reads as tech, not food)
  - Low-contrast text overlaid on full-bleed food photos (legibility fail — use overlays or type-safe zones)
  - Stock photos of generic "happy diners" (erodes craft perception)
  - Emoji in copy ("our 🔥 burger" reads unserious for anything aspiring premium)
  - Multi-CTA hero ("Reserve" + "Order" + "Sign up" on one frame)
  - Overly saturated photography that reads as fast-food marketing for casual/craft brands

## Minimal example

```python
ds = gen.generate(
    description="Independent neighborhood Italian restaurant with tasting menu",
    stack="html",
    tech_details={"css": "tailwindcss"}
)
# Pattern:   "Photography-Forward"
# Style:     "Warm Minimalism + Editorial"
# Colors:    Primary #8B4513 (warm brown), CTA #C53030 (tomato), Background #FFF8F0 (cream), Text #2D2015 (deep ink)
# Fonts:     Fraunces (heading serif) / Inter Tight (body)
# Hero:      single full-bleed dish photo, title + one CTA ("Reserve a Table")
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- Fast-food / casual brands (Five Guys, Shake Shack) can break some rules — red primary, higher saturation, multi-CTA hero. The rule bends for the category.
- Vegan / clean-eating brands often use green as primary — allowed as long as temperature is warm green (sage, olive) not cold green (forest, lime).
- International cuisine sites may override the warm palette for authenticity (Japanese washi / indigo, Scandinavian monochrome). User-explicit override allowed.

## Cross-references

- `TECH-uiux-rules-catalog.md`
- `TECH-uiux-pre-delivery-checklist.md`
- `../SKILL.md`
- `../../amw-design-principles/ai-slop-avoid.md`
