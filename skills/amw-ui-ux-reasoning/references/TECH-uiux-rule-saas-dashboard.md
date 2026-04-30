---
name: TECH-uiux-rule-saas-dashboard
category: uiux-rule
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---

# TECH: Reasoning rule — SaaS Dashboard / B2B Analytics

## What it does

SaaS dashboards are the category most over-designed into ai-slop. The rule enforces data-first hierarchy, progressive disclosure, and restrained visual language — showing the value (data, insights, actions) before decoration.

## When to use

When building analytics platforms, admin panels, B2B-tools dashboards, observability UIs, CRM home screens, or any app where the primary screen shows user data (charts, tables, metrics).

## How it works

- **Pattern** — Data-First + Progressive Disclosure: key metrics above fold (4-6 KPIs max), secondary data revealed on click/hover, filters collapsed by default, sidebar nav with 5-7 items max.
- **Style priority** — `Glassmorphism`, `Bento Grid`, `AI-Native UI` (when the product IS AI, not when every product claims AI). `Data-Dense UI` for power-user screens.
- **Color mood** — Indigo / violet / deep blue primary; dark surface backgrounds common; white surface acceptable but less defensible for long sessions.
- **Anti-patterns** —
  - Decorative animations on data (charts that wobble, KPIs that pulse for no reason)
  - Overly complex gradients (purple-to-pink, radial + linear layered — both ai-slop)
  - Stock photos (dashboards never need them)
  - Too many colors in charts (use 6 max — beyond that, switch to greyscale)
  - Marketing-site chrome (huge hero, testimonials) inside a product UI
  - Rainbow palette on status indicators (use 3-4 semantic: success / warning / error / info)

## Minimal example

```python
ds = gen.generate(
    description="B2B SaaS analytics dashboard for enterprise teams",
    stack="react",
    tech_details={"component_library": "shadcn/ui", "css": "tailwindcss"}
)
# Pattern:   "Data-First + Progressive Disclosure"
# Style:     "Glassmorphism" or "Bento Grid"
# Colors:    Primary #6366F1 (Indigo), CTA #8B5CF6 (Violet), surface rgba(255,255,255,0.05)
# Fonts:     Inter / Inter (unified, high legibility — mandatory for data)
# Effects:   Subtle card shadows, smooth data transitions 200ms
# Avoid:     Decorative animations, overly complex gradients, rainbow chart palettes
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- The "AI-Native" style is legitimate when the product surfaces AI interaction (chat, generation, agent traces). Applying it to a non-AI SaaS ("we have a recommendations engine") is ai-slop coding.
- Dark mode for dashboards is expected for power users working 8+ hour sessions — the rule does not ban dark mode; it bans unnecessary gradients and decoration.
- `Inter` is acceptable here (and only here) because data-dense numerals benefit from its tabular-nums and clear `0/O` differentiation — this is one of the few industry exceptions to the "avoid Inter" ai-slop rule.

## Cross-references

- `TECH-uiux-rules-catalog.md`
- `TECH-uiux-pre-delivery-checklist.md`
- `../SKILL.md`
- `../../amw-design-principles/ai-slop-avoid.md`
