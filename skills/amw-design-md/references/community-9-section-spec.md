# Community 9-section DESIGN.md spec — Variant 2 (VoltAgent / getdesign.md style)

**Source:** `docs_dev/extracted/google-labs/design-md-creator-skill-main/design-md-creator-skill-main/.claude/skills/design-md-creator/DESIGN_MD_SPEC.md`. The author of that skill reverse-engineered the format from analysis of 58 brand DESIGN.md files in the public corpus (`docs_dev/extracted/google-labs/awesome-design-md-pre-paywall-main/`).

This is the **Variant 2** format. It dominates real-world DESIGN.md files in the wild (the 58-brand pre-paywall corpus and the parallel 98-brand `design-swatches` corpus). When a user provides a Variant 2 file, the plugin accepts it and converts to Variant 1 (canonical) via `bin/amw-design-md-convert-v2-to-v1.py`.

When the user explicitly asks for Variant 2 output (because they are matching an existing collection), the plugin can author Variant 2 directly using `references/templates/community-9-section-template.md`.

---

## Document head (DESIGN_MD_SPEC L13-L17)

Every Variant 2 file begins with a single H1 on line 1:

```
# Design System Inspired by {BrandName}
```

`{BrandName}` is the brand's common name (e.g., "Stripe", "Apple", "Wise"), not a slug.

## Section count and order (DESIGN_MD_SPEC L25-L36)

Exactly 9 numbered sections, all `##` headings, pattern `## N. Section Name`:

| # | Section name |
|---|---|
| 1 | Visual Theme & Atmosphere |
| 2 | Color Palette & Roles |
| 3 | Typography Rules |
| 4 | Component Stylings |
| 5 | Layout Principles |
| 6 | Depth & Elevation |
| 7 | Do's and Don'ts |
| 8 | Responsive Behavior |
| 9 | Agent Prompt Guide |

Three exceptional files in the corpus contain a 10th section. Plugin treats those as accepted-but-non-standard.

## No YAML frontmatter

Variant 2 has NO YAML frontmatter. All tokens are encoded in prose and tables in the body. This is the primary distinction from Variant 1 and the reason the converter must extract tokens from prose patterns.

---

## Section specifications

### Section 1 — Visual Theme & Atmosphere (DESIGN_MD_SPEC L43-L67)

Structure:
1. One-to-two long prose paragraphs (atmosphere + emotional tone + brand identity).
2. A third paragraph (sometimes merged) describing typography and spacing philosophy.
3. Closes with `**Key Characteristics:**` bold label + bullet list.

Key Characteristics list: typically 6–9 bullets, each in form `{element} — {value or descriptor}`.

```markdown
## 1. Visual Theme & Atmosphere

{Two to three paragraphs of prose}

**Key Characteristics:**
- Accent color: `#hex` — descriptor
- Background: descriptor
- Font family at size/weight — descriptor
- Interaction or animation pattern
- Border radius philosophy
- Design philosophy statement
```

### Section 2 — Color Palette & Roles (DESIGN_MD_SPEC L72-L106)

Multiple `###` subsections grouping colors by role:

1. `### Primary` or `### Primary Brand`
2. `### Secondary & Accent` or `### Interactive`
3. `### Surface & Background` or `### Surface & Borders`
4. `### Neutrals & Text` or `### Text & Neutrals`
5. `### Semantic` or `### Semantic & Status`
6. `### Gradient System` or `### Shadows` (optional)

Color entry format:
```
- **Color Name** (`#rrggbb`): role description and/or CSS variable name
```

Variants:
- `rgba()`: `- **Name** (\`rgba(r, g, b, a)\`): description`
- Multiple formats: `- **Name** (\`#hex\` / \`hsl(...)\`): description`
- CSS variable association: `- **Name** (\`#hex\`): \`--css-var\`, role`

Pure black `#000000` and pure white `#ffffff` are rarely used; near-black and off-white are standard.

### Section 3 — Typography Rules (DESIGN_MD_SPEC L108-L166)

Structure:
1. `### Font Family` (or Families) — prose font list
2. `### Hierarchy` — markdown table
3. `### Principles` — bullet list

Font Family subsection:
```markdown
### Font Family

- **Display**: `FontName`, fallback: `system-ui, sans-serif`
- **Body / UI**: `FontName`, fallbacks: `Helvetica, Arial`
```

Hierarchy table — standard 7-column schema:

```markdown
| Role | Font | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|------|--------|-------------|----------------|-------|
```

- **Role**: e.g., "Display Hero", "Body", "Button", "Caption"
- **Font**: family name
- **Size**: px with rem in parentheses, e.g., `96px (6.00rem)`
- **Weight**: numeric 100–900, occasionally named
- **Line Height**: decimal or descriptor
- **Letter Spacing**: px or `normal` or `0`
- **Notes**: OpenType features, transformation, brand-specific

Principles subsection: 3–6 bullets, each `- **Label**: explanation`.

### Section 4 — Component Stylings (DESIGN_MD_SPEC L169-L216)

Multiple `###` subsections per component type. Standard subsections:

1. `### Buttons`
2. `### Cards & Containers`
3. `### Navigation`
4. `### Inputs & Forms`

Optional/brand-specific:
5. `### Image Treatment`
6. `### Badges / Tags`
7. `### Links`
8. `### Distinctive Components`

Variant format inside each component:

```markdown
### Buttons

**Primary {Adjective}**
- Background: `#hex`
- Text: `#hex`
- Padding: top-bottom left-right
- Radius: value
- Font: descriptor
- Hover: description
- Active: description (sometimes)
- Focus: description (sometimes)
- Use: context note

**Secondary {Adjective}**
- ...
```

Variant names use bold `**Name**` inline (NOT `####`).

Common button variants: Primary / Secondary / Ghost / Outlined / Tertiary / Text Link / Destructive / Danger.

### Section 5 — Layout Principles (DESIGN_MD_SPEC L219-L246)

Structure:
1. `### Spacing System`
2. `### Grid & Container`
3. `### Whitespace Philosophy`
4. `### Border Radius Scale`

Universal rule: **every Variant 2 file states "Base unit: 8px"** under Spacing System.

```markdown
### Spacing System
- Base unit: 8px
- Scale: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px
```

Grid & Container — prose: max content width (typically 1200–1440 px), column count, gutter, container padding.

### Section 6 — Depth & Elevation

Standard: an elevation-level table (5 levels: 0/1/2/3/4) with shadow formulas using rgba and explicit px offsets.

```markdown
| Level | Use | Shadow formula |
|---|---|---|
| 0 | Flush, flat | none |
| 1 | Resting card | rgba(0,0,0,0.05) 0px 1px 2px 0px |
| 2 | Hover, dropdown | rgba(0,0,0,0.08) 0px 4px 8px -2px |
| 3 | Modal, popover | rgba(0,0,0,0.12) 0px 12px 24px -6px |
| 4 | Toast, overlay top | rgba(0,0,0,0.16) 0px 24px 48px -12px |
```

Plus: z-index scale (numeric values for `base / dropdown / sticky / overlay / modal / toast`).

### Section 7 — Do's and Don'ts

`### Do` and `### Don't` subsections, each a bullet list. Minimum 3 of each (rubric `T6`).

### Section 8 — Responsive Behavior

```markdown
### Breakpoints

| Name | Min width | Typical device |
|---|---|---|
| sm  | 640px  | Small phone |
| md  | 768px  | Tablet portrait |
| lg  | 1024px | Tablet landscape / small laptop |
| xl  | 1280px | Desktop |
| 2xl | 1536px | Large desktop |

### Collapsing Strategy
- Typography scales: h1 drops from {desktop px} to {mobile px} below md.
- Multi-column layouts collapse to single column below md.
- Touch targets must be ≥ 44×44 px on touch devices.
```

### Section 9 — Agent Prompt Guide

The TL;DR for AI agents at the bottom of the file (LLM attention bias toward recent context). Required content:

1. `### Quick Color Reference` — bullet list of the 5–7 most-used colors with hex.
2. `### Quick Type Reference` — display + body shorthand.
3. `### Example Component Prompts` — minimum 3 prompt patterns.
4. `### Iteration Guide` — 4–6 numbered step rules ("Read this entire file before writing any component", "Only reference tokens defined here", etc.).

The Variant 2 format puts these LAST because LLMs attend strongly to recent context.

---

## XML boundary tags (Variant 2 enhancement)

The `design-md-builder` skill's 9-section template wraps the 9 sections with three XML boundary tags:

- `<context>` — wraps the document Overview block (above Section 1)
- `<design_tokens>` — wraps Sections 1 through 8
- `<constraints>` — wraps Section 9 (Agent Prompt Guide)

This is a Variant 2 enhancement, not in the original 58-file corpus but recommended by the design-md-builder critic rubric (`S2`–`S4`). The plugin's Variant 2 template includes it for quality-gate compliance; the converter strips it when going Variant 2 → Variant 1.

---

## Mermaid component-state diagram

The 9-section template includes a `mermaid` block under Section 4 (Component Stylings) showing the state machine: `Default / Hover / Focus / Active / Disabled / Loading / Error`. Reviewers expect at least one valid Mermaid block per the rubric (`S5/S6`).

---

## Comparison vs Variant 1

| Aspect | Variant 1 (canonical) | Variant 2 (community) |
|---|---|---|
| YAML frontmatter | Yes, machine-readable tokens | No, all in prose/tables |
| Section count | 8 | 9 (+ optional 10–14 from extensions) |
| Token reference syntax | `{path.to.token}` curly braces | None — by-name in prose |
| Linter | `npx @google/design.md lint` | Custom rubric (`review-rubric.md`) |
| Section ordering | Fixed; reorder = error | Fixed; numbered |
| Best for | Machine consumption, AI agent input | Human-first reference, brand handoff |

The plugin's default canonical output is Variant 1. Variant 2 is accepted as input and produced on explicit request.

---

## Cross-references

- `./canonical-spec-google-alpha.md` — Variant 1 spec
- `./extension-sections-10-14.md` — optional Variant 2 extensions
- `./templates/community-9-section-template.md` — fillable Variant 2 skeleton
- `./review-rubric.md` — Variant 2 quality scoring
- `./TECH-13-converting-variant2-to-1.md` — V2 → V1 conversion details
- `<plugin-root>/bin/amw-design-md-convert-v2-to-v1.py` — conversion bin script
