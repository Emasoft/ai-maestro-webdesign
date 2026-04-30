---
name: TECH-uiux-pre-delivery-checklist
category: uiux-rule
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---

# TECH: Universal pre-delivery checklist

## What it does

Every design system the generator produces is accompanied by a universal pre-delivery checklist covering four axes: accessibility, responsive behavior, performance, and interaction states. The checklist is the same across industries — the industry-specific anti-patterns (from the reasoning rule) layer on top.

## When to use

As the final gate before emitting any production output. `ux-evaluator` uses this checklist as the baseline pass criteria; `design-principles` enforces it via `ai-slop-avoid.md`. The checklist runs on every variant, not just the final one.

## How it works

Four sections, each a boolean gate set. A design fails the checklist if ANY item is unchecked.

### Accessibility

- [ ] No emojis as icons — use SVG (Heroicons / Lucide / Phosphor / SF Symbols)
- [ ] `cursor: pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode: text contrast ratio ≥ 4.5:1
- [ ] Dark mode: text contrast ratio ≥ 4.5:1
- [ ] Focus states visible for keyboard navigation
- [ ] `prefers-reduced-motion` respected
- [ ] ARIA labels on icon-only buttons

### Responsive

- [ ] Mobile: 375px breakpoint tested
- [ ] Tablet: 768px breakpoint tested
- [ ] Desktop: 1024px breakpoint tested
- [ ] Wide: 1440px breakpoint tested

### Performance

- [ ] Images use next-gen formats (WebP / AVIF)
- [ ] Fonts loaded with `font-display: swap`
- [ ] No layout shift on font load (reserve space via `size-adjust` or explicit fallback metrics)
- [ ] Animations use `transform` / `opacity` only (no layout props — no `top` / `left` / `width` / `height` tweens)

### Interaction

- [ ] Loading states on all async actions
- [ ] Error states are clear and actionable
- [ ] Empty states are designed (not blank placeholders)
- [ ] Success feedback on form submissions

## Minimal example

```python
ds = gen.generate(description="Personal finance tracker")
for item in ds.checklist:
    print(item)
# ✓ WCAG AA contrast on all number displays
# ✓ Currency formatted with locale awareness
# ✓ Error states are clear and actionable
# ✓ Loading states on all async operations
# ✓ Biometric auth UI integrated
# ✓ No emojis as primary icons — use Lucide or SF Symbols
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- The checklist is necessary but not sufficient — a design can pass every item and still be ai-slop. Run `../../amw-design-principles/ai-slop-avoid.md` alongside.
- The contrast rule is AA, not AAA. AAA is 7:1 for normal text and is the correct target for legal, medical, and government content.
- "Animations use transform/opacity only" rules out layout-triggering properties (width, height, top, left, padding, margin). Scale + translate achieve the same visual result without layout recalc.

## Cross-references

- `../SKILL.md`
- `TECH-uiux-design-system-generator.md`
- `TECH-uiux-rules-catalog.md` — industry-specific anti-patterns stack on top of this baseline
- `../../amw-design-principles/ai-slop-avoid.md` — non-skippable final filter
- `../../amw-ux-evaluator/SKILL.md` — pairs with this checklist at delivery time
