## Table of Contents

- [File structure (spec.md L6-L8)](#file-structure-specmd-l6-l8)
- [YAML frontmatter schema (spec.md L17-L40, L43-L58)](#yaml-frontmatter-schema-specmd-l17-l40-l43-l58)
- [Markdown body — the 8 fixed sections (spec.md L82-L92)](#markdown-body-the-8-fixed-sections-specmd-l82-l92)
- [Recommended token names (non-normative) (spec.md L334-L342)](#recommended-token-names-non-normative-specmd-l334-l342)
- [Consumer behavior for unknown content (spec.md L344-L356)](#consumer-behavior-for-unknown-content-specmd-l344-l356)
- [Validation rules (per the official linter)](#validation-rules-per-the-official-linter)
- [Worked example (full file)](#worked-example-full-file)
- [Cross-references](#cross-references)


# Canonical DESIGN.md spec — Variant 1 (official `@google/design.md` alpha)

**Source:** `docs_dev/extracted/google-labs/design.md-main/design.md-main/docs/spec.md` (Google Labs `design.md` repository, v0.1.1, version literal `alpha`).

This document distills that spec for plugin use. All quoted material is verbatim from the source; line numbers refer to the source file. The official linter is `npx @google/design.md lint <file>`.

This is the **PRIMARY** format for the plugin. New DESIGN.md files authored by `amw-design-md-author-agent` use this format. Variant 2 (community 9-section) is accepted as input via `bin/amw-design-md-convert-v2-to-v1.py` and documented in [community-9-section-spec](community-9-section-spec.md).
> [community-9-section-spec.md] Document head (DESIGN_MD_SPEC L13-L17) · Section count and order (DESIGN_MD_SPEC L25-L36) · No YAML frontmatter · Section specifications · Section 1 — Visual Theme & Atmosphere (DESIGN_MD_SPEC L43-L67) · Section 2 — Color Palette & Roles (DESIGN_MD_SPEC L72-L106) · Section 3 — Typography Rules (DESIGN_MD_SPEC L108-L166) · Section 4 — Component Stylings (DESIGN_MD_SPEC L169-L216) · Section 5 — Layout Principles (DESIGN_MD_SPEC L219-L246) · Section 6 — Depth & Elevation · Section 7 — Do's and Don'ts · Section 8 — Responsive Behavior · Section 9 — Agent Prompt Guide · XML boundary tags (Variant 2 enhancement) · Mermaid component-state diagram · Comparison vs Variant 1 · Cross-references

---

## File structure (spec.md L6-L8)

> "A DESIGN.md file contains two parts: An optional YAML frontmatter, and a markdown body. The YAML front matter contains machine-readable design tokens. The markdown body sections provide human-readable design rationale and guidance."

A complete DESIGN.md is therefore:

1. YAML frontmatter (delimited by exactly `---` lines at top and bottom of the block)
2. Markdown body with `<h2>` sections in fixed order (L82-L92 of spec.md)

---

## YAML frontmatter schema (spec.md L17-L40, L43-L58)

The frontmatter MUST start at line 1 with exactly `---` and end with a line containing exactly `---`. Content between is parsed as YAML.

### Top-level fields

```yaml
version: <string>          # optional, current literal: "alpha"
name: <string>             # REQUIRED — design system name
description: <string>      # optional
colors:                    # optional but at least primary recommended
  <token-name>: <Color>
typography:                # optional
  <token-name>: <Typography>
rounded:                   # optional
  <scale-level>: <Dimension>
spacing:                   # optional
  <scale-level>: <Dimension | number>
components:                # optional
  <component-name>:
    <token-name>: <string|token-reference>
```

`<scale-level>` (spec.md L60): "represents a named level in a sizing or spacing scale. Common level names include `xs`, `sm`, `md`, `lg`, `xl`, and `full`. Any descriptive string key is valid."

### Type definitions

**Color** (spec.md L62):
> "A color value must start with `#` followed by a hex color code in the SRGB color space."

**Typography** sub-fields (spec.md L64-L72):
- `fontFamily` (string)
- `fontSize` (Dimension)
- `fontWeight` (number) — "A numeric font weight value (e.g., `400`, `700`). In YAML, this may be expressed as either a bare number or a quoted string; both are equivalent."
- `lineHeight` (Dimension | number) — "A unitless number represents a multiplier of the element's `fontSize`, which is the recommended CSS practice."
- `letterSpacing` (Dimension)
- `fontFeature` (string) — configures `font-feature-settings`
- `fontVariation` (string) — configures `font-variation-settings`

**Dimension** (spec.md L74):
> "A dimension value is a string with a unit suffix. Valid units are: px, em, rem."

**Token References** (spec.md L76):
> "A token reference must be wrapped in curly braces, and contain an object path to another value in the YAML tree. For most token groups, the reference must point to a primitive value (e.g., `colors.primary-60`), not a group (e.g., `colors`). Within the `components` section, references to composite values (e.g., `{typography.label-md}`) are permitted."

### Component property tokens (spec.md L312-L319)

Each `components.<name>.<property>` may be one of:

- `backgroundColor: <Color>`
- `textColor: <Color>`
- `typography: <Typography>` (or `{typography.<key>}` reference)
- `rounded: <Dimension>` (or `{rounded.<key>}` reference)
- `padding: <Dimension>`
- `size: <Dimension>`
- `height: <Dimension>`
- `width: <Dimension>`

Variants (spec.md L295) are encoded as related keys:

```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary-60}"
    textColor: "{colors.primary-20}"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary-70}"
```

---

## Markdown body — the 8 fixed sections (spec.md L82-L92)

Sections may be omitted if not relevant. Sections present MUST appear in this order. All section headers are `<h2>` (`##`). An optional `<h1>` may appear for document title (NOT parsed as a section).

```
1. Overview          (also: "Brand & Style")
2. Colors
3. Typography
4. Layout            (also: "Layout & Spacing")
5. Elevation & Depth (also: "Elevation")
6. Shapes
7. Components
8. Do's and Don'ts
```

### Section content guidance

**1. Overview** (spec.md L97-L99):
> "A holistic description of a product's look and feel. It defines the brand personality, target audience, and the emotional response the UI should evoke, such as whether it should feel playful or professional, dense or spacious. It serves as foundational context for guiding the agent's high-level stylistic decisions when a specific rule or token isn't explicitly defined."

**2. Colors** (spec.md L103-L107):
> "At least the `primary` color palette must be defined, and additional color palettes may be defined as needed. When there are multiple color palettes, the design system may assign a semantic role for each palette. A common convention is to name the palettes in this order: `primary`, `secondary`, `tertiary`, and `neutral`."

Tokens go in the YAML frontmatter; prose explains the philosophy.

**3. Typography** (spec.md L143-L147):
> "Most design systems have 9 - 15 typography levels... A common naming convention for typography levels is to use semantic categories such as `headline`, `display`, `body`, `label`, `caption`. Each category may further be divided into different sizes, such as `small`, `medium`, and `large`."

**4. Layout** (spec.md L196-L210):
Grid model (fluid vs fixed-max-width), spacing scale, gutters, margins. Tokens go in `spacing:` frontmatter.

**5. Elevation & Depth** (spec.md L233-L245):
> "If elevation is used, it defines the required styling (spread, blur, color). For flat designs, this section explains the alternative methods used to convey visual hierarchy (e.g., borders, color contrast)."

Note: spec defines no frontmatter token group for elevation. It is prose-only.

**6. Shapes** (spec.md L249-L259):
> "The shape language is defined by **Architectural Sharpness**..." (example). Tokens go in `rounded:` frontmatter.

**7. Components** (spec.md L279-L289):
Style guidance for atoms. Common atoms listed:
- Buttons (primary, secondary, tertiary variants)
- Chips (selection, filter, action)
- Lists (items, dividers, leading/trailing)
- Tooltips
- Checkboxes (checked, unchecked, indeterminate)
- Radio buttons
- Input fields (text inputs, text areas, labels, helper text, error states)

**Important spec note (L289):** "The components specification is actively evolving. The current structure provides intentional flexibility for domain-specific component definitions while the spec matures."

**8. Do's and Don'ts** (spec.md L321-L325):
Practical guidelines. Concrete rules. Example from spec:
- "Do use the primary color only for the single most important action per screen"
- "Don't mix rounded and sharp corners in the same view"
- "Do maintain WCAG AA contrast ratios (4.5:1 for normal text)"
- "Don't use more than two font weights on a single screen"

---

## Recommended token names (non-normative) (spec.md L334-L342)

These names are not required but are commonly used:

| Group | Common names |
|---|---|
| Colors | `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error` |
| Typography | `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm` |
| Rounded | `none`, `sm`, `md`, `lg`, `xl`, `full` |

A DESIGN.md is free to use other names. The official linter does NOT reject custom names.

---

## Consumer behavior for unknown content (spec.md L344-L356)

| Scenario | Behavior | Example |
|---|---|---|
| Unknown section heading | Preserve; do not error | `## Iconography` |
| Unknown color token name | Accept if value valid | `surface-container-high: '#ede7dd'` |
| Unknown typography token name | Accept as valid typography | `telemetry-data` |
| Unknown spacing value | Accept; store as string if not a valid dimension | `grid-columns: '5'` |
| Unknown component property | Accept with warning | `borderColor` |
| Duplicate section heading | **Error; reject the file** | Two `## Colors` headings |

**The single hard validation failure is duplicate section heading.** All other unknowns are tolerated.

---

## Validation rules (per the official linter)

The `npx @google/design.md lint` CLI enforces:

1. Frontmatter starts at line 1 with exactly `---`.
2. YAML between `---` delimiters is well-formed.
3. Section headings follow the fixed order (missing OK, reordered NOT OK).
4. Duplicate section heading = ERROR.
5. `colors.*` values match `^#[0-9a-fA-F]{6}$` or short-form `^#[0-9a-fA-F]{3}$` (sRGB hex).
6. `Dimension` values match `^[0-9.]+(px|em|rem)$`.
7. `fontWeight` values are integers in [100..900].
8. Token references match `^\{[a-zA-Z0-9._-]+\}$` and resolve to an existing path in the YAML tree.
9. Component-property references to composite values are allowed only inside `components.*`.
10. WCAG-AA contrast checks (4.5:1 for normal text, 3:1 for large text) are warned about, not errored.

---

## Worked example (full file)

```markdown
---
version: alpha
name: Daylight Prestige
description: A clinical-minimalist editorial design system.
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.1em
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px
spacing:
  base: 16px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.md}"
    padding: 12px
---

# Daylight Prestige Design System

## Overview

This design system pairs editorial restraint with a single, evocative accent.
The product targets a professional readership; the UI should feel calm,
authoritative, and unhurried.

## Colors

The palette is rooted in high-contrast neutrals and a single, evocative accent color.

- **Primary (#1A1C1E):** A deep ink used for headlines and core text.
- **Secondary (#6C7278):** A sophisticated slate for borders, captions, metadata.
- **Tertiary (#B8422E):** A vibrant earthy red used exclusively for primary actions.
- **Neutral (#F7F5F2):** A warm limestone foundation for all pages.

## Typography

The typography strategy leverages two distinct weights of **Public Sans** for narrative
content and **Space Grotesk** for technical data.

## Layout

A strict 8 px spacing scale (with a 4 px half-step) maintains rhythm.
Components are grouped into cards with 24 px internal padding.

## Elevation & Depth

Depth is achieved through tonal layers rather than heavy shadows.

## Shapes

The shape language is defined by architectural sharpness — a 4 px corner radius
for all interactive elements.

## Components

Buttons, chips, lists, tooltips, checkboxes, radios, input fields all follow
the rounded-md scale and the primary/secondary/tertiary color hierarchy.

## Do's and Don'ts

- Do use the primary color only for the single most important action per screen.
- Do maintain WCAG AA contrast ratios.
- Don't mix rounded and sharp corners in the same view.
- Don't use more than two font weights on a single screen.
```

---

## Cross-references

- [community-9-section-spec](./community-9-section-spec.md) — Variant 2 (parallel community format)
  > Document head (DESIGN_MD_SPEC L13-L17) · Section count and order (DESIGN_MD_SPEC L25-L36) · No YAML frontmatter · Section specifications · Section 1 — Visual Theme & Atmosphere (DESIGN_MD_SPEC L43-L67) · Section 2 — Color Palette & Roles (DESIGN_MD_SPEC L72-L106) · Section 3 — Typography Rules (DESIGN_MD_SPEC L108-L166) · Section 4 — Component Stylings (DESIGN_MD_SPEC L169-L216) · Section 5 — Layout Principles (DESIGN_MD_SPEC L219-L246) · Section 6 — Depth & Elevation · Section 7 — Do's and Don'ts · Section 8 — Responsive Behavior · Section 9 — Agent Prompt Guide · XML boundary tags (Variant 2 enhancement) · Mermaid component-state diagram · Comparison vs Variant 1 · Cross-references
- [extension-sections-10-14](./extension-sections-10-14.md) — optional extensions (Naming / Page Specs / Composite Components / Token Mapping / i18n)
  > Section 10 — Naming Convention (Page > Section > Block > Element) · Section 11 — Page Specifications · Section 12 — Composite Components · Section 13 — Token Mapping · Section 14 — i18n References · When to use these extensions · Cross-references · "What to build" (page-level specs, requirements) · Component composition (LoginPage as a unit, not just Button + Input) · Token-to-Tailwind / token-to-CSS-var mapping table · i18n string-resource mapping
- [canonical-template](./canonical-template.md) — fillable Variant 1 skeleton
  > Filling guide · Cross-references
- [TECH-01-yaml-frontmatter](./TECH-01-yaml-frontmatter.md) — authoring the YAML frontmatter
  > What it does · When to use · Hard rules · Delimiters · Top-level fields · Value type rules · Token references · YAML quoting rules · Common gotchas · Worked example — minimal valid frontmatter · Worked example — token reference inside components · Validation · Cross-references
- [TECH-11-validation-and-lint](./TECH-11-validation-and-lint.md) — running the linter and pure-Python validator
  > What it does · The three validators · Official linter (`bin/amw-design-md-lint.sh`) · Pure-Python offline validator (`bin/amw-design-md-validate.py`) · Contrast checker (`bin/amw-design-md-contrast.py`) · Standard validation chain · Lint failure → recovery · Diff between two DESIGN.md files · CI integration suggestion (out-of-scope but documented) · Cross-references
- `../../../bin/amw-design-md-lint.sh` — wrapper around the official @google design.md npm linter (invoked via npx)
- `../../../bin/amw-design-md-validate.py` — pure-Python offline validator
