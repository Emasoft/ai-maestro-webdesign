---
name: TECH-ux-rule-visual
category: ux-rule-visual
source: SKILLS-TO-INTEGRATE/web-design/ux-designer/rules/visual-design.md
also-in: SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md
---

# TECH: Rule — Visual Design (hierarchy + design system)

## What it does

MEDIUM-priority rule covering visual hierarchy (how the eye is guided), typography scale, color usage, layout, and the essentials of a design system. Visual design communicates hierarchy and brand without requiring users to think.

## When to use

On visual-design reviews, design-system setup, typography scale audits, color-usage audits, and layout rhythm checks. Trigger phrases: "establish hierarchy", "pick a type scale", "design-system essentials", "8-pt grid".

## How it works

### Establishing hierarchy

Six tools (applied together, not individually):

1. **Size** — larger elements attract attention first; use for headings and primary CTAs
2. **Contrast** — high contrast draws the eye; for key actions and critical info
3. **Color** — saturated/brand colors for emphasis; muted for secondary
4. **Position** — top-left scanned first in LTR; F / Z-pattern for key content
5. **Whitespace** — generous spacing isolates and elevates
6. **Typography** — weight, size, style create levels

### Typography scale

- 3-4 distinct sizes per screen (more = chaos)
- Consistent ratio between levels (1.25× or 1.333×)
- Weight (bold vs regular) differentiates within the same size
- ALL CAPS only for very short labels (buttons, tags)

### Color usage

- Primary for main CTAs and key interactive elements
- Neutrals (grays) for body text + secondary elements
- Semantic: green (success), red (error), yellow (warning), blue (info)
- Accent colors limited to 1-2 per screen

### Layout

- Align to a grid (8px base is standard)
- Tighter spacing between related elements, looser between unrelated (proximity principle)
- Group related items via shared containers + proximity

### Design-system essentials

- Color palette (primary / secondary / neutral / semantic + usage rules)
- Typography (families, size scale, weight, line heights)
- Spacing (base unit — typically 4 or 8 px — applied consistently)
- Grid (columns, gutters, margins per breakpoint)
- Elevation (shadow levels indicating depth)
- Border radius (4 subtle, 8 cards, full for pills)

### Component documentation

Every component specifies: purpose + anatomy + states (default / hover / active / focus / disabled / error), variants, responsive behavior, accessibility requirements.

## Minimal example

Typography scale at 1.25× ratio:

```css
:root {
  --fs-xs:   12px;
  --fs-sm:   14px;
  --fs-base: 16px;  /* body */
  --fs-lg:   20px;  /* lead */
  --fs-xl:   25px;  /* h3 */
  --fs-2xl:  31px;  /* h2 */
  --fs-3xl:  39px;  /* h1 */
}
```

*Attributed to the ux-designer rule file — `SKILLS-TO-INTEGRATE/web-design/ux-designer/rules/visual-design.md`.*

## Gotchas

- Making everything bold / large = nothing is emphasized. Hierarchy demands contrast.
- Competing CTAs of equal weight on the same screen means the user sees no primary action. One primary per screen.
- Design systems built before product needs are understood ossify bad decisions. Start with real components, extract patterns, generalize.
- Separate design (Figma) and code (React) component libraries inevitably drift. Single source of truth (code) is the only defensible architecture.

## Cross-references

- `TECH-ux-rule-research.md`, `TECH-ux-rule-accessibility.md`, `TECH-ux-rule-ia.md`, `TECH-ux-rule-interaction.md`
- `../../amw-design-principles/typography-system.md`
- `../../amw-design-principles/color-system.md`
- `../../amw-design-principles/spacing-rhythm.md`
- `../SKILL.md`
