---
name: TECH-24-authoring-rules-spec
category: authoring
source: DESIGN_MD_SPEC (awesome-design-md community spec); design.md spec.md
license: MIT
also-in: TECH-01-yaml-frontmatter.md, TECH-06-do-donts.md, TECH-22-section-10-11-extended.md, TECH-23-section-9-agent-prompt-guide.md
status: stable
---

# TECH: The 13 DESIGN.md authoring rules

## Table of Contents

- [What it does](#what-it-does)
- [Why a spec exists](#why-a-spec-exists)
- [The 13 rules](#the-13-rules)
  - [Rule 1 — 9 sections mandatory, fixed order](#rule-1--9-sections-mandatory-fixed-order)
  - [Rule 2 — Section heading format](#rule-2--section-heading-format)
  - [Rule 3 — Every color value in backticks](#rule-3--every-color-value-in-backticks)
  - [Rule 4 — Elevation table exactly 3 columns](#rule-4--elevation-table-exactly-3-columns)
  - [Rule 5 — Shadow Philosophy required prose in §6](#rule-5--shadow-philosophy-required-prose-in-6)
  - [Rule 6 — Iteration Guide numbered list](#rule-6--iteration-guide-numbered-list)
  - [Rule 7 — Do's and Don'ts parallel in count](#rule-7--dos-and-donts-parallel-in-count)
  - [Rule 8 — Spacing scale base unit is 8px](#rule-8--spacing-scale-base-unit-is-8px)
  - [Rule 9 — §9 Agent Prompt Guide last in body](#rule-9--9-agent-prompt-guide-last-in-body)
  - [Rule 10 — One sentence per visual rule](#rule-10--one-sentence-per-visual-rule)
  - [Rule 11 — Typography roles must declare 3 properties](#rule-11--typography-roles-must-declare-3-properties)
  - [Rule 12 — Component definitions must cite tokens, never raw values](#rule-12--component-definitions-must-cite-tokens-never-raw-values)
  - [Rule 13 — Frontmatter precedes the H1](#rule-13--frontmatter-precedes-the-h1)
- [How the rules combine](#how-the-rules-combine)
- [Linter enforcement](#linter-enforcement)
- [Variant 1 vs Variant 2 differences](#variant-1-vs-variant-2-differences)
- [Cross-references](#cross-references)

## What it does

Documents the 13 authoring rules `DESIGN_MD_SPEC` defines for the canonical Variant 1 format. These rules are enforced by `bin/amw-design-md-lint.sh` (official `@google/design.md` linter) and complemented by `bin/amw-design-md-validate.py` (offline pure-Python validation).

Authors who follow all 13 rules produce DESIGN.md files that pass lint on the first run and are interchangeable across the awesome-design-md ecosystem.

## Why a spec exists

The free-form nature of Markdown means two authors writing "the same DESIGN.md" can produce structurally incompatible files: different heading capitalization, different table shapes, different elevation phrasing. Coding agents reading those files cannot reliably extract tokens — they have to guess at structure.

The 13 rules constrain the variance until structural extraction becomes mechanical. Once the rules are in place, the linter's job becomes simple: assert each rule and report violations. Each rule maps to ONE linter check, and each linter check maps to ONE rule.

## The 13 rules

### Rule 1 — 9 sections mandatory, fixed order

Variant 1 has exactly 9 mandatory body sections, in this order:

1. Identity
2. Color
3. Typography
4. Spacing & Rhythm
5. Surfaces & Elevation
6. Components
7. Motion (some authors fold this into §6; the spec recommends a dedicated §7 — see [TECH-26-extended-sections-7-8](TECH-26-extended-sections-7-8.md))
8. Do's and Don'ts
9. Agent Prompt Guide (per [TECH-23-section-9-agent-prompt-guide](TECH-23-section-9-agent-prompt-guide.md))

Optional trailing sections §10 (Iteration Guide) and §11 (Known Gaps) per [TECH-22-section-10-11-extended](TECH-22-section-10-11-extended.md).

Reordering, omitting, or renaming any of the 9 mandatory sections is a P0 lint error.

### Rule 2 — Section heading format

Every section heading uses the literal format `## N. Name` where N is the section number and Name is the canonical section title. No deviation in casing, no extra punctuation, no parenthetical addendum.

Correct:
```markdown
## 2. Color
## 5. Surfaces & Elevation
## 8. Do's and Don'ts
```

Incorrect:
```markdown
## 2. Colors            # plural "Colors" deviates from canonical
## 5. Surfaces and Elevation   # spelled-out "and" deviates from canonical &
## 8. Dos & Donts       # missing apostrophes
```

The exact section names per spec.md L321 are: Identity / Color / Typography / Spacing & Rhythm / Surfaces & Elevation / Components / Motion / Do's and Don'ts / Agent Prompt Guide.

### Rule 3 — Every color value in backticks

Color values everywhere in the document — frontmatter, prose, tables, component definitions — must be wrapped in backticks. This is for machine extraction: the linter and emitters look for color values via the backtick-wrapped regex `\`#[0-9A-Fa-f]{3,8}\``.

Correct:
```markdown
The primary color is `#1A1C1E`. The accent shifts to `#B8422E` on hover.
```

Incorrect:
```markdown
The primary color is #1A1C1E. The accent shifts to #B8422E on hover.
```

This rule applies to hex, rgb, hsl, oklch, and named CSS colors. Even `white` and `black` are wrapped when referenced as design-system values.

### Rule 4 — Elevation table exactly 3 columns

Section 5 Surfaces & Elevation contains a markdown table with exactly 3 columns: Level, Treatment, Use. Adding a fourth column (e.g. "Token", "CSS") is a lint error.

Canonical format:
```markdown
| Level | Treatment | Use |
|---|---|---|
| Base | No elevation | Body content, default backgrounds |
| Raised | 1px border on `--neutral-200` | Cards, modals, list items |
| Floating | 8px shadow `0 8px 24px rgba(0,0,0,0.08)` | Tooltips, popovers, dropdowns |
```

The 3-column constraint is enforced because the emitter that produces `tokens.css` consumes exactly those three columns and emits one CSS class per row. A 4th column breaks the emitter contract.

### Rule 5 — Shadow Philosophy required prose in §6

Section 6 Components must contain a paragraph titled "Shadow Philosophy" that states the design system's stance on shadows. This is prose, not a table — it answers questions like "When do you use a shadow vs a rule line? When do you stack shadows? When do you not?".

Example:
```markdown
### Shadow Philosophy

This design system uses shadows for FLOATING elements only — tooltips, popovers,
dropdown menus. Cards, modals, and list items use a 1px border on
`--neutral-200` instead. Shadows are never stacked; a single shadow per floating
element is the maximum. The shadow color is always pure black at low opacity
(`rgba(0, 0, 0, 0.08)`), never tinted.
```

The Shadow Philosophy is a frequently-ignored brand-defining decision. Forcing its inclusion in §6 surfaces it to every coding agent.

### Rule 6 — Iteration Guide numbered list

Section 10 (when present — see Rule 1 and [TECH-22-section-10-11-extended](TECH-22-section-10-11-extended.md)) must use a numbered list `1.`, `2.`, `3.` — not bullets. The numbering signals priority order.

A bulleted §10 is a lint warning (not error) because the file is still parseable, but the ordering signal is lost.

### Rule 7 — Do's and Don'ts parallel in count

Section 8 contains both a "Do's" list and a "Don'ts" list. The two lists must have the SAME COUNT of items. Asymmetric lists (4 dos, 2 don'ts) is a lint warning — it suggests the author abandoned the section partway.

Minimum count is 3 per side (per [TECH-06-do-donts](TECH-06-do-donts.md) "T6: minimum 3 dos and 3 don'ts"). The lint upper bound is 10 per side.

Canonical example:
```markdown
## 8. Do's and Don'ts

**Do**
- Use rule lines for elevation
- Apply the accent color once per viewport
- Choose the smaller of two viable type sizes

**Don't**
- Use `box-shadow` on cards
- Use gradients of any kind
- Use Tailwind utility classes
```

### Rule 8 — Spacing scale base unit is 8px

Section 4 Spacing & Rhythm declares the spacing scale. The base unit is always 8px. Permitted values are multiples of 8 (8, 16, 24, 32, 40, 48, 64, 80, 96) plus the optional half-step 4px for tight inline gaps.

Other base units (4px, 6px, 10px) are a lint warning. The 8px base is enforced because (a) every standard typography baseline grid divides cleanly by 8, (b) Tailwind's default spacing scale aligns to 8px, and (c) shadcn / Radix tokens align to 8px.

### Rule 9 — §9 Agent Prompt Guide last in body

When §9 Agent Prompt Guide is present, it appears LAST in the canonical 9-section body — after Do's and Don'ts. This is because §9 is the high-density agent-consumption block; placing it last means an agent that reads top-to-bottom encounters all tokens (§2-§6), motion (§7), brand rules (§8), and then the operationalization (§9).

§10 and §11 (when present) follow §9.

### Rule 10 — One sentence per visual rule

Every visual rule in prose form (NOT in tables, NOT in code blocks) is a single sentence. Compound sentences with multiple semicolons are split.

Correct:
```markdown
Cards use a 1px border on `--neutral-200`. Modals add a backdrop blur.
```

Incorrect:
```markdown
Cards use a 1px border on `--neutral-200`; modals add a backdrop blur; popovers float with an 8px shadow.
```

This rule produces grep-friendly DESIGN.md text. Every prose visual rule becomes a single line for indexing.

### Rule 11 — Typography roles must declare 3 properties

Each typography role in §3 must declare at minimum:
- Family
- Size
- Line-height

Weight is optional but recommended. Color and letter-spacing are optional.

Format (table form):
```markdown
| Role | Family | Size | Line-height | Weight |
|---|---|---|---|---|
| display | Inter | 56px | 1.05 | 600 |
| h1 | Inter | 40px | 1.1 | 600 |
| body | Inter | 16px | 1.55 | 400 |
```

A role with only `family` and `size` (missing line-height) is a P1 lint error.

### Rule 12 — Component definitions must cite tokens, never raw values

Section 6 Components defines each component (button, input, card, etc.) using token references like `var(--primary)` or `{colors.primary}` — NEVER raw hex / px values. Raw values break the substitution chain: an agent that wants to re-skin the component must hunt for raw values instead of editing the token.

Correct:
```markdown
### Primary Button

- Background: `var(--primary)`
- Color: `var(--on-primary)`
- Padding: `var(--space-3) var(--space-6)`
- Border-radius: `var(--radius-sm)`
```

Incorrect:
```markdown
### Primary Button

- Background: `#1A1C1E`
- Color: `#F7F5F2`
- Padding: `12px 24px`
- Border-radius: `6px`
```

Dead token references (`var(--primary)` when no `primary` token is declared) are P1 lint errors per [TECH-27-token-interpolation](TECH-27-token-interpolation.md).

### Rule 13 — Frontmatter precedes the H1

YAML frontmatter is the first content in the file. It is delimited by `---` on its own line, contains the canonical fields per [TECH-01-yaml-frontmatter](TECH-01-yaml-frontmatter.md), and ends with another `---`. The H1 (the document title) appears AFTER the closing `---`.

Correct:
```markdown
---
name: PostHog
url: https://posthog.com
extracted-from: posthog.com/marketing-pages
colors:
  primary: '#000000'
  ...
---

# PostHog DESIGN.md
```

Missing frontmatter is a P0 lint error. Frontmatter that appears below the H1 is a P0 lint error.

## How the rules combine

The 13 rules form three layers:

- **Structural (Rules 1, 2, 9, 13)** — what sections exist, what they're called, what order they appear in, and where the frontmatter sits.
- **Content (Rules 4, 5, 6, 7, 10, 11)** — what each section must contain (column counts, prose paragraphs, list shapes, sentence shapes).
- **Token reference (Rules 3, 8, 12)** — how values are formatted (backticks for colors, 8px base for spacing, token references not raw values for components).

A DESIGN.md that violates rules across all three layers is structurally unsalvageable. A DESIGN.md that violates only Content layer rules is usually fixable by re-running the author through the lint output.

## Linter enforcement

The official `@google/design.md lint` CLI (wrapped by `bin/amw-design-md-lint.sh`) enforces all 13 rules. Per-rule mapping:

| Rule | Linter check | Severity |
|---|---|---|
| 1 | `sections-mandatory-order` | P0 |
| 2 | `section-heading-format` | P0 |
| 3 | `color-values-in-backticks` | P1 |
| 4 | `elevation-table-3-columns` | P0 |
| 5 | `shadow-philosophy-prose-required` | P1 |
| 6 | `iteration-guide-numbered` | warning |
| 7 | `dos-donts-parallel-count` | warning |
| 8 | `spacing-base-8px` | warning |
| 9 | `agent-prompt-guide-last` | P0 |
| 10 | `one-sentence-per-rule` | warning |
| 11 | `typography-three-properties` | P1 |
| 12 | `component-cites-tokens` | P1 |
| 13 | `frontmatter-precedes-h1` | P0 |

P0 violations block delivery. P1 violations require author acknowledgment. Warnings are advisory.

The offline pure-Python validator `bin/amw-design-md-validate.py` covers Rules 1, 2, 3, 4, 11, 12, and 13. Rules 5, 6, 7, 8, 9, 10 are linter-only.

## Variant 1 vs Variant 2 differences

These 13 rules are Variant 1 canonical. Variant 2 (community 9-section) shares Rules 1, 2, 7, 8, 13 but diverges on:

- Rule 4 — Variant 2 has no fixed elevation table column count.
- Rule 5 — Variant 2 has no Shadow Philosophy requirement.
- Rule 9 — Variant 2 has no §9 Agent Prompt Guide (Do's and Don'ts is §7 in V2, the last section).
- Rule 11 — Variant 2 typography roles are described in prose, not tables.

The V2 → V1 converter (`bin/amw-design-md-convert-v2-to-v1.py`) raises any V1-only rule violation into a converter warning surfaced to the human author.

## Cross-references

- [TECH-01-yaml-frontmatter](TECH-01-yaml-frontmatter.md) — Rule 13 detail
- [TECH-06-do-donts](TECH-06-do-donts.md) — Rule 7 detail
- [TECH-11-validation-and-lint](TECH-11-validation-and-lint.md) — linter and validator usage
- [TECH-22-section-10-11-extended](TECH-22-section-10-11-extended.md) — Rule 6 (Iteration Guide)
- [TECH-23-section-9-agent-prompt-guide](TECH-23-section-9-agent-prompt-guide.md) — Rule 9 detail
- [TECH-26-extended-sections-7-8](TECH-26-extended-sections-7-8.md) — Rule 1 §7 Motion detail
- [TECH-27-token-interpolation](TECH-27-token-interpolation.md) — Rule 12 detail
- [canonical-spec-google-alpha](canonical-spec-google-alpha.md) — full Variant 1 spec
