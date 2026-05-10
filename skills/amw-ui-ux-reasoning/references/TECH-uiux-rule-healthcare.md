---
name: TECH-uiux-rule-healthcare
category: uiux-rule
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: Reasoning rule — Healthcare / Medical

## What it does

Healthcare products navigate legal + emotional constraints simultaneously. The rule enforces "clinical but warm" — institutional enough to be trustworthy, human enough not to feel like a government form.

## When to use

When building for clinics, hospitals, telemedicine, mental-health apps, medical-record systems, pharma-facing platforms, or any YMYL (your-money-your-life) medical content. This rule supersedes free style choice.

## How it works

- **Pattern** — Trust-first hero: credentials, licenses, accreditations visible above fold. Clear "What we treat / When to seek care / How to start" triad.
- **Style priority** — `Clean Minimalism`, `Soft UI`, `Warm Minimalism`. Avoid `Glassmorphism` (visually cold on medical data), `Brutalism` (anxiety-inducing).
- **Color mood** — Blues, teals, whites. Muted greens for reassurance. Warm off-white backgrounds (not pure `#FFFFFF` — clinical but not sterile).
- **Anti-patterns** —
  - Red primary buttons (emergency connotation triggers anxiety)
  - Dark mode on medical records (readability + accessibility regression for older users)
  - Stock photos of smiling patients (reads as marketing fiction, erodes trust)
  - Gamification (star ratings on health outcomes, badges for medication adherence)
  - Overly playful illustrations on serious content (cancer, mental-health crisis pages)
  - Ambiguous iconography (pill shapes that look like logos, heart icons with romance connotation)

## Minimal example

```python
ds = gen.generate(
    description="Telemedicine booking + online consultation platform",
    stack="nextjs"
)
print(ds.colors.primary)   # e.g. #2B7A9F (clinical teal)
print(ds.colors.cta)       # e.g. #0066CC (steady blue — not red)
print(ds.anti_patterns)
# [
#   "Red for primary actions",
#   "Dark mode on medical data",
#   "Stock photos of smiling patients",
#   ...
# ]
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- Mental-health products have a narrower palette — avoid bright yellows (anxiety) and pure white (clinical-hostile for depression audiences). Warm cream surfaces with sage green or dusty blue primary work better.
- Accessibility is legally required, not optional (ADA in the US, EN 301 549 in the EU). All WCAG 2.1 AA gates from the pre-delivery checklist are hard requirements, not suggestions.
- Pediatric products can loosen the anti-patterns (friendly illustrations are expected) but the core "clinical + trustworthy" layer must still be present for parent audiences.

## Cross-references

- [TECH-uiux-rules-catalog](TECH-uiux-rules-catalog.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Top 10 distinctive rules — broken out as individual TECH files · Cross-references
- [TECH-uiux-pre-delivery-checklist](TECH-uiux-pre-delivery-checklist.md)
  > What it does · When to use · How it works · Accessibility · Responsive · Performance · Interaction · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md)
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
