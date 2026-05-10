---
name: TECH-13-converting-variant2-to-1
category: conversion
source: community-9-section-spec.md, canonical-spec-google-alpha.md
also-in: TECH-04-component-tokens.md, TECH-12-companion-files.md
status: stable
---

# TECH: Converting Variant 2 (community 9-section) → Variant 1 (canonical)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Conversion overview](#conversion-overview)
- [Token extraction from V2 prose](#token-extraction-from-v2-prose)
  - [Colors](#colors)
  - [Typography](#typography)
  - [Spacing](#spacing)
  - [Rounded](#rounded)
  - [Components](#components)
  - [Mermaid state diagram](#mermaid-state-diagram)
  - [Sections 8-9 merging](#sections-8-9-merging)
- [Information that may be lost](#information-that-may-be-lost)
- [Inputs](#inputs)
- [Validation after conversion](#validation-after-conversion)
- [Round-trip notes](#round-trip-notes)
- [Cross-references](#cross-references)

## What it does

Documents the field-level conversion from a Variant 2 DESIGN.md (community 9-section format, all in prose) to a Variant 1 DESIGN.md (canonical `@google/design.md`, with YAML frontmatter). The bin script is `bin/amw-design-md-convert-v2-to-v1.py`. Pure-Python, no external deps beyond PyYAML.

## When to use

- The user provides a DESIGN.md from the public corpus (`awesome-design-md-pre-paywall`, design-swatches, etc.) and wants to use it as input to the plugin's downstream wireframe-builder, which prefers Variant 1.
- The user has authored a Variant 2 file and now wants to lint it via `npx @google/design.md` (which only understands V1).
- Companion-file emission needs Variant 1 input (the emitter is V1-only currently).

## When NOT to use

- The user explicitly wants Variant 2 output (matching an existing collection style) — keep the source Variant 2 file as-is and operate on it directly via Variant 2 path.
- The user has Variant 1 already — no conversion needed.

## Conversion overview

The script walks the Variant 2 prose and tables and produces:

1. A Variant 1 YAML frontmatter populated from the prose tokens.
2. A Variant 1 markdown body in canonical 8-section order (mapping V2's 9 sections to V1's 8).

| V2 section | V1 mapping |
|---|---|
| 1. Visual Theme & Atmosphere | → V1 `## Overview` |
| 2. Color Palette & Roles | → V1 frontmatter `colors:` + V1 `## Colors` |
| 3. Typography Rules | → V1 frontmatter `typography:` + V1 `## Typography` |
| 4. Component Stylings | → V1 frontmatter `components:` + V1 `## Components` |
| 5. Layout Principles | → V1 frontmatter `spacing:` + V1 `## Layout` |
| 6. Depth & Elevation | → V1 `## Elevation & Depth` (prose only — V1 has no shadow tokens) |
| (V2 has no separate "Shapes" section) | → V1 `## Shapes` synthesized from V2 Sec 5's "Border Radius Scale" subsection + frontmatter `rounded:` |
| 7. Do's and Don'ts | → V1 `## Do's and Don'ts` |
| 8. Responsive Behavior | → merged into V1 `## Layout` (V1 has no separate responsive section) |
| 9. Agent Prompt Guide | → either dropped (V1 has no equivalent) OR appended as a custom non-normative section "## Agent Prompt Guide" (preserved per spec.md L350: "Unknown section heading: Preserve; do not error") |

## Token extraction from V2 prose

### Colors

V2 Section 2 has bullet entries like:
```
- **Color Name** (`#rrggbb`): role description and/or CSS variable name
```

The converter regex-matches each bullet and produces:
- A `colors.<slug>` entry where slug is derived from the bold label (lowercased, hyphen-separated).
- A `## Colors` prose bullet matching the original.

```python
# Pseudo-code
for bullet in section_2.bullets:
    match = re.match(r"-\s*\*\*(.+?)\*\*\s*\(\s*`([#0-9a-fA-F]+)`\s*\)\s*:\s*(.+)", bullet)
    if match:
        descriptive_name, hex_value, role = match.groups()
        slug = slugify(descriptive_name)
        colors[slug] = hex_value
```

If V2 has subsections like `### Primary`, `### Secondary & Accent`, the converter prefixes slugs:
- `### Primary` → `primary`, `primary-hover`, `primary-light`
- `### Surface & Background` → `surface`, `surface-elevated`, `surface-inverse`

### Typography

V2 Section 3 has a 7-column table:
```
| Role | Font | Size | Weight | Line Height | Letter Spacing | Notes |
```

Each row → a typography token:

```yaml
typography:
  display-hero:
    fontFamily: <Font column>
    fontSize: <Size column with px stripped>
    fontWeight: <Weight column>
    lineHeight: <Line Height column, unitless if decimal else with unit>
    letterSpacing: <Letter Spacing column, "0em" if "normal" or "0">
```

Slug from "Role" column (lowercased, hyphenated).

### Spacing

V2 Section 5 "Spacing System":
```
- Base unit: 8px
- Scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px
```

Converter:
```yaml
spacing:
  base: 8px
  xs: 4px
  sm: 8px
  md: 16px      # the converter uses positional → semantic mapping
  lg: 32px
  xl: 64px
  2xl: 96px
```

Positional mapping is heuristic: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 → xs / sm / md / md+1 / lg-1 / lg / lg+1 / xl / 2xl. The script uses standard Tailwind-ish naming.

### Rounded

V2 Section 5 "Border Radius Scale":
```
- xs: 2px
- sm: 4px
- md: 8px
- lg: 12px
- xl: 16px
- full: 9999px
```

Direct map → V1 frontmatter `rounded:` with same keys.

### Components

V2 Section 4 component blocks:
```
**Primary**
- Background: `#1a1c1e`
- Text: `#f7f5f2`
- Padding: 12px 24px
- Radius: 8px
- ...
```

Converter:
```yaml
components:
  button-primary:
    backgroundColor: "#1a1c1e"      # or "{colors.<slug-of-#1a1c1e>}" if matched
    textColor: "#f7f5f2"
    padding: 12px
    rounded: 8px
```

If a hex value matches a token in the extracted `colors:` map, the converter emits a `{colors.X}` reference instead of literal hex (idiomatic Variant 1 style).

If the V2 component spec has multiple variants under the same component (e.g., `**Primary White**` and `**Primary Dark**`), each becomes a `<component>-<variant>` entry.

### Mermaid state diagram

V2 commonly has a `mermaid stateDiagram-v2` block under Section 4. Variant 1 has no equivalent token. The converter preserves it as a `## Components` prose subsection in V1 (since V1 prose accepts arbitrary content per spec).

### Sections 8-9 merging

V1 has no `## Responsive Behavior` section. The converter:
- Moves V2 Section 8 prose into V1 `## Layout` as a "### Responsive" subsection.
- Moves V2 Section 9 (Agent Prompt Guide) to a non-normative tail section "## Agent Prompt Guide" after V1's `## Do's and Don'ts` (the spec accepts unknown sections per L350).

## Information that may be lost

V2 has richer content than V1 in some areas. Conversion preserves data but flags where Variant 1 has no native slot:

| V2 content | V1 fate |
|---|---|
| XML boundary tags (`<context>`, `<design_tokens>`, `<constraints>`) | Stripped (V1 has no equivalent; the wrapping is preserved as "non-normative" in prose) |
| Per-component shadow rgba formulas | Kept in `## Elevation & Depth` prose (V1 has no shadow token group) |
| Example component prompts (V2 §9) | Kept as appended "## Agent Prompt Guide" |
| Z-index scale (V2 §6) | Kept in `## Elevation & Depth` prose |
| Brand-tinted shadow opacity (V2 §6 typical) | Kept in `## Elevation & Depth` prose |
| Whitespace philosophy paragraphs | Kept in `## Layout` prose |
| Iteration guide (V2 §9) | Kept in "## Agent Prompt Guide" prose |

The converter writes a warning to the converted file's header comment listing what was preserved-as-prose vs natively-mapped:

```markdown
<!--
Converted from Variant 2 (community 9-section) to Variant 1 (canonical Google) on <timestamp>.
Source: <input-file-path>
Preserved as prose (no Variant 1 token slot): shadow rgba formulas, z-index scale,
agent prompt guide content. Fully mapped: colors, typography, spacing, rounded, components.
-->
```

## Inputs

```bash
python3 bin/amw-design-md-convert-v2-to-v1.py <input-v2.md> <output-v1.md> [--name NAME]
```

- `<input-v2.md>`: source Variant 2 file. Required.
- `<output-v1.md>`: destination Variant 1 file. Required.
- `--name NAME`: design system name override. Default: extracted from `# Design System Inspired by NAME` line.

## Validation after conversion

```bash
bash bin/amw-design-md-lint.sh OUTPUT.md      # MUST pass
python3 bin/amw-design-md-validate.py OUTPUT.md
python3 bin/amw-design-md-contrast.py OUTPUT.md
```

If lint fails, the conversion has a bug — report and fix the converter, do not hand-edit the output.

## Round-trip notes

The conversion is **lossy** in one direction (V2 → V1 drops some content into prose). The reverse direction (V1 → V2) is NOT provided — users wanting Variant 2 output should author it directly from the Variant 2 template.

## Cross-references

- [community-9-section-spec](./community-9-section-spec.md) — V2 source format
  > Document head (DESIGN_MD_SPEC L13-L17) · Section count and order (DESIGN_MD_SPEC L25-L36) · No YAML frontmatter · Section specifications · Section 1 — Visual Theme & Atmosphere (DESIGN_MD_SPEC L43-L67) · Section 2 — Color Palette & Roles (DESIGN_MD_SPEC L72-L106) · Section 3 — Typography Rules (DESIGN_MD_SPEC L108-L166) · Section 4 — Component Stylings (DESIGN_MD_SPEC L169-L216) · Section 5 — Layout Principles (DESIGN_MD_SPEC L219-L246) · Section 6 — Depth & Elevation · Section 7 — Do's and Don'ts · Section 8 — Responsive Behavior · Section 9 — Agent Prompt Guide · XML boundary tags (Variant 2 enhancement) · Mermaid component-state diagram · Comparison vs Variant 1 · Cross-references
- [canonical-spec-google-alpha](./canonical-spec-google-alpha.md) — V1 target format
  > File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Top-level fields · Type definitions · Component property tokens (spec.md L312-L319) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Section content guidance · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references
- [TECH-04-component-tokens](./TECH-04-component-tokens.md) — component tokens in V1
  > What it does · Hard rules · Property whitelist (per spec.md L312-L319) · Variant naming convention · Composite token references allowed inside `components.*` · Common component patterns · Button (primary/secondary/ghost) · Input · Card · Chip / Badge · Hover-state derivation strategies · Anti-patterns · Cross-references
- [TECH-12-companion-files](./TECH-12-companion-files.md) — emit companions from the converted V1
  > What it does · The four companions · `tokens.css` — CSS custom properties · `tokens.json` — W3C Design Tokens format · `component-inventory.md` — human-readable component list · `usage-prompt.md` — Drop-in agent prompt · Inputs to the emitter · Resolution behavior · Synchronization rule · Cross-references
- `../../../bin/amw-design-md-convert-v2-to-v1.py`
