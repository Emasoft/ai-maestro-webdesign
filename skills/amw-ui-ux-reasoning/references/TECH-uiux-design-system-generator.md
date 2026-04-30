---
name: TECH-uiux-design-system-generator
category: uiux-rule
source: SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md
also-in:
---

# TECH: Design System Generator (end-to-end composition)

## What it does

The ui-ux-pro-max skill's core flow. Given a product description, it runs a multi-domain search across the 161 rules + 67 styles + 161 palettes + 57 font pairings + 24 LP patterns and returns a complete, internally-consistent design system: pattern + style + colors + typography + effects + anti-patterns + pre-delivery checklist.

## When to use

When `ui-ux-reasoning` is activated and must produce the full three-candidate fallback output — each candidate is a full design-system triple (style + palette + fonts), not just one dimension.

## How it works

Input: a one-line product description + optional `stack` (React / Next.js / Astro / Vue / HTML / SwiftUI / Flutter / etc.) + optional `mode` (light / dark / auto).

Pipeline:

1. BM25 search across the 161 reasoning rules → top industry match
2. Pull the rule's `pattern`, `style_priority`, `color_mood`, `anti_patterns`
3. Filter style catalog by `style_priority`, filter palette catalog by `color_mood`, filter font-pairings catalog by mood tag
4. Produce three candidate triples, each internally coherent (style ↔ palette ↔ fonts harmonious)
5. Annotate each with the rule's anti-patterns and the universal pre-delivery checklist
6. Export as CSS variables, Tailwind config, TypeScript theme, and a Markdown rationale

Every candidate includes:

- **Pattern** — which of the 24 LP structures applies
- **Style** — one of the 67 named visual languages
- **Colors** — primary / secondary / CTA / background / text
- **Typography** — heading + body from the 57-pair catalog + Google Fonts import URL
- **Key effects** — signature animations, hover deltas, rest motion
- **Anti-patterns** — industry-specific vetoes
- **Pre-delivery checklist** — accessibility, responsive, performance, interaction gates

## Minimal example

```python
from uiuxpro import DesignSystemGenerator

gen = DesignSystemGenerator()
ds = gen.generate(
    description="A landing page for a luxury beauty spa",
    stack="react",
    mode="light"
)

ds.pattern         # Landing page structure
ds.style           # UI style recommendation
ds.colors          # Color palette dict
ds.typography      # Font pairing + import URL
ds.effects         # Animations and interactions
ds.anti_patterns   # What to avoid
ds.checklist       # Pre-delivery gates
ds.css_variables   # Ready-to-paste :root block
ds.tailwind_config # Ready-to-merge theme extension
```

*Attributed to ui-ux-pro-max-skill — `SKILLS-TO-INTEGRATE/web-design/ui-ux-pro-max-skill/SKILL.md`.*

## Gotchas

- The generator is a single-pick composition by default — for the plugin's fallback flow, wrap it with three invocations (three different product angles or three different style-priority biases) so the output satisfies design-principles Rule 2 (three variants).
- Outputs from the upstream API include ai-slop candidates. The plugin wraps the generator with a post-filter against `../../amw-design-principles/ai-slop-avoid.md`.
- The generator works best with specific descriptions. `"a website"` returns generic; `"a SaaS landing page for a B2B project management tool targeting remote engineering teams"` returns a targeted, useful design system.

## Cross-references

- `TECH-uiux-rules-catalog.md`, `TECH-uiux-styles-catalog.md`, `TECH-uiux-palettes-catalog.md`, `TECH-uiux-font-pairings-catalog.md`, `TECH-uiux-lp-patterns-catalog.md`
- `TECH-uiux-pre-delivery-checklist.md`
- `../SKILL.md`
