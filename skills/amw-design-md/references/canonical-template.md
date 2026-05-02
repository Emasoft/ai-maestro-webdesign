## Table of Contents

- [Filling guide](#filling-guide)
- [Cross-references](#cross-references)


# Canonical DESIGN.md template (Variant 1 — `@google/design.md` alpha)

Copy the block below to a new `DESIGN.md`. Fill every `<placeholder>` with a real value. Leave optional sections out entirely if not relevant — do NOT leave empty section headers. After filling, run `bin/amw-design-md-lint.sh DESIGN.md` and fix any errors.

This skeleton produces a file that passes `npx @google/design.md lint` cleanly.

---

```markdown
---
version: alpha
name: <Design system name — e.g. "Daylight Prestige">
description: <One-line description — optional but recommended>

colors:
  primary: "<#hex>"
  secondary: "<#hex>"
  tertiary: "<#hex>"      # optional
  neutral: "<#hex>"       # optional
  surface: "<#hex>"       # optional
  on-surface: "<#hex>"    # optional
  error: "<#hex>"         # optional

typography:
  headline-display:
    fontFamily: <Font family name>
    fontSize: <Npx>
    fontWeight: <100-900>
    lineHeight: <unitless or Npx>
    letterSpacing: <Nem>     # optional
  headline-lg:
    fontFamily: <Font family name>
    fontSize: <Npx>
    fontWeight: <100-900>
    lineHeight: <unitless or Npx>
  headline-md:
    fontFamily: <Font family name>
    fontSize: <Npx>
    fontWeight: <100-900>
    lineHeight: <unitless or Npx>
  body-lg:
    fontFamily: <Font family name>
    fontSize: <Npx>
    fontWeight: <100-900>
    lineHeight: <unitless or Npx>
  body-md:
    fontFamily: <Font family name>
    fontSize: <Npx>
    fontWeight: <100-900>
    lineHeight: <unitless or Npx>
  body-sm:
    fontFamily: <Font family name>
    fontSize: <Npx>
    fontWeight: <100-900>
    lineHeight: <unitless or Npx>
  label-lg:
    fontFamily: <Font family name>
    fontSize: <Npx>
    fontWeight: <100-900>
    lineHeight: <unitless or Npx>
    letterSpacing: <Nem>     # optional but recommended for labels
  label-md:
    fontFamily: <Font family name>
    fontSize: <Npx>
    fontWeight: <100-900>
    lineHeight: <unitless or Npx>
    letterSpacing: <Nem>
  label-sm:
    fontFamily: <Font family name>
    fontSize: <Npx>
    fontWeight: <100-900>
    lineHeight: <unitless or Npx>
    letterSpacing: <Nem>

rounded:
  none: 0px
  sm: <Npx>
  md: <Npx>
  lg: <Npx>
  xl: <Npx>
  full: 9999px

spacing:
  base: <Npx>      # the canonical step (typically 16px)
  xs: <Npx>
  sm: <Npx>
  md: <Npx>
  lg: <Npx>
  xl: <Npx>
  gutter: <Npx>    # optional
  margin: <Npx>    # optional

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: <Npx>
  button-primary-hover:
    backgroundColor: "{colors.secondary}"
  button-primary-disabled:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.on-surface}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: <Npx>
  input-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: <Npx>
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: <Npx>
---

# <Design system name> Design System

> <One-paragraph description of the brand and the AI-agent context. This is for human readers. The YAML frontmatter is for machine readers.>

## Overview

<One paragraph describing the holistic look-and-feel: brand personality, target audience, emotional response. Specify density (compact / balanced / airy), formality (playful / professional), and any opinionated choices that distinguish this system from others. ~80-150 words.>

## Colors

<One paragraph explaining the color philosophy. State which palette is the brand-identity driver and which is utilitarian.>

- **Primary (`<#hex>`):** <Role description — where it is used and why>
- **Secondary (`<#hex>`):** <Role description>
- **Tertiary (`<#hex>`):** <Role description — optional>
- **Neutral (`<#hex>`):** <Role description — optional>

<Optional: explicit do-not-use rules, e.g., "Never use Tertiary in dense data tables.">

## Typography

<One-paragraph explanation of the typographic strategy: what fonts, what hierarchy logic, what families work where.>

- **Display & headlines:** <Font name + weight rationale>
- **Body:** <Font name + weight + reading-rhythm note>
- **Labels:** <Font name + weight + special features like uppercase/letter-spacing>

## Layout

<One-paragraph layout philosophy: grid model (fluid / fixed-max-width), spacing-scale rationale, container behavior.>

- **Grid:** <e.g., 12-column on desktop, fluid on mobile, max content width 1200px>
- **Base unit:** <e.g., 8px>
- **Spacing scale (px):** <e.g., 4, 8, 16, 24, 32, 48, 64>

## Elevation & Depth

<Describe how visual hierarchy is conveyed. If using shadows: shadow philosophy + general formula. If flat design: alternative methods (borders, color contrast, surface tones).>

## Shapes

<Describe the corner-radius philosophy: architectural-sharp (small radii) vs friendly-soft (large radii). Specify the scale levels.>

## Components

<For each component declared in `components:` frontmatter, give a 1-2-sentence usage rule. Example:>

- **Button (primary):** <Used for the single most important action per screen. One per view maximum unless explicitly justified.>
- **Button (secondary):** <Used for supporting actions; outline variant in light contexts, filled in dark contexts.>
- **Input (default):** <Always paired with a visible label. Placeholder text supplements but never replaces.>
- **Card:** <Container for grouped content. Internal padding follows spacing.lg.>

## Do's and Don'ts

**Do:**
- Do <concrete rule 1 — e.g., "Do use the primary color for the single most important action per screen.">
- Do <concrete rule 2 — e.g., "Do maintain WCAG AA contrast ratios (4.5:1 for normal text).">
- Do <concrete rule 3 — e.g., "Do reference tokens by name; never hard-code hex values in component code.">
- Do <concrete rule 4 — e.g., "Do respect the 8px grid for every spatial value.">

**Don't:**
- Don't <concrete anti-pattern 1 — e.g., "Don't mix rounded and sharp corners in the same view.">
- Don't <concrete anti-pattern 2 — e.g., "Don't use more than two font weights on a single screen.">
- Don't <concrete anti-pattern 3 — e.g., "Don't introduce new colors outside this palette without updating this file first.">
- Don't <concrete anti-pattern 4 — e.g., "Don't use Tertiary as the dominant color of any view.">
```

---

## Filling guide

When filling this template:

1. **Every `<placeholder>` must become a real value.** Leaving any placeholder in place fails the slop checklist (`ai-slop-avoid.md` S4).
2. **Hex values must be 6-digit `#xxxxxx`.** No CSS named colors. No `rgb()` in frontmatter.
3. **`fontWeight` is a number 100–900.** Quoted or unquoted both work.
4. **Token references use `{path.to.token}` syntax** — only inside the `components:` block, and only to existing paths.
5. **Sections may be omitted but not reordered.** A file with `## Layout` before `## Typography` is rejected by the linter.
6. **The `## Overview` paragraph is the most important prose section.** It is what the AI agent reads first when scoping a design decision. Make it actionable.

After filling, validate:

```bash
bash <plugin-root>/bin/amw-design-md-lint.sh DESIGN.md
python3 <plugin-root>/bin/amw-design-md-validate.py DESIGN.md
python3 <plugin-root>/bin/amw-design-md-contrast.py DESIGN.md
```

Fix any errors before delivering.

## Cross-references

- `canonical-spec-google-alpha.md` — full spec
- `TECH-01-yaml-frontmatter.md` — YAML authoring tips
- `TECH-02-color-tokens.md` — color authoring
- `TECH-03-typography-tokens.md` — typography authoring
- `TECH-04-component-tokens.md` — component variants
- `TECH-06-do-donts.md` — actionable do/don't authoring
- `../../amw-design-principles/ai-slop-avoid.md` — what NOT to write
