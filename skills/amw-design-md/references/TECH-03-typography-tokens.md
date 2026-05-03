---
name: TECH-03-typography-tokens
category: authoring
source: design.md-main/docs/spec.md L141-L192
also-in: TECH-01-yaml-frontmatter.md, TECH-05-token-references.md, TECH-cjk-localization.md
status: stable
---

# TECH: Typography tokens authoring

## Table of Contents

- [What it does](#what-it-does)
- [Hard rules](#hard-rules)
  - [Required Typography sub-fields (per spec.md L64-L68)](#required-typography-sub-fields-per-specmd-l64-l68)
  - [fontSize units](#fontsize-units)
  - [fontWeight rules](#fontweight-rules)
  - [lineHeight conventions](#lineheight-conventions)
  - [letterSpacing](#letterspacing)
  - [fontFeature / fontVariation (OpenType)](#fontfeature-fontvariation-opentype)
- [Recommended level taxonomy](#recommended-level-taxonomy)
  - [Variable fonts and weight axis](#variable-fonts-and-weight-axis)
- [Font fallback chains](#font-fallback-chains)
- [CJK considerations](#cjk-considerations)
- [Common patterns](#common-patterns)
  - [Display + headline + body × 3 sizes (11 levels)](#display-headline-body-3-sizes-11-levels)
  - [Compact 7-level (developer tools)](#compact-7-level-developer-tools)
  - [Marketing-rich 15-level (consumer brands)](#marketing-rich-15-level-consumer-brands)
- [Worked example — full row](#worked-example-full-row)
- [Cross-references](#cross-references)


## What it does

Documents how to declare the `typography:` map in YAML frontmatter. Covers font-family selection, the level taxonomy, fontWeight rules, line-height conventions, letter-spacing best-practices, and OpenType feature settings.

## Hard rules

### Required Typography sub-fields (per spec.md L64-L68)

Every typography token must include at minimum:

- `fontFamily` (string)
- `fontSize` (Dimension — px/em/rem)
- `fontWeight` (number 100-900)
- `lineHeight` (Dimension or unitless number)

Optional but recommended:

- `letterSpacing` (Dimension — typically em for relative tracking)
- `fontFeature` (string — CSS `font-feature-settings`)
- `fontVariation` (string — CSS `font-variation-settings`)

A row missing any of the four required fields is a hard linter failure.

### fontSize units

Use `px` for the canonical value. The reader MAY add `rem` equivalents in prose for accessibility but the frontmatter is `px`. Do not mix units within a system unless intentional (e.g., a fluid system using `clamp()` is documented in prose, with one canonical px value in frontmatter).

### fontWeight rules

Integer 100-900. The official linter rejects:

- `fontWeight: bold` — string non-number
- `fontWeight: 1000` — out of range
- `fontWeight: 450` — odd; CSS allows 1-1000 but the spec restricts to 100-900 step values typically

Both `fontWeight: 600` (bare) and `fontWeight: "600"` (quoted string) are accepted as equivalent (per spec.md L66).

### lineHeight conventions

Two valid forms:

1. **Unitless number** (recommended for body): `lineHeight: 1.6`. Treated as multiplier of fontSize. CSS best practice — children inherit a multiplier, not a fixed px.
2. **Dimension**: `lineHeight: "24px"` or `lineHeight: "1.5rem"`. Use for very large display text where exact line-height is part of the visual.

Prefer unitless for body and label sizes (1.4–1.6). Use dimension for display sizes where the box height is part of the layout (1.0–1.2 px values).

### letterSpacing

Use em for relative tracking. Display sizes: negative (`-0.02em` to `-0.04em`). Body: zero or omitted. Labels and uppercase text: positive (`0.05em` to `0.15em`).

```yaml
headline-display:
  letterSpacing: "-0.03em"
body-md:
  letterSpacing: "0"        # or omit
label-caps:
  letterSpacing: "0.1em"
```

### fontFeature / fontVariation (OpenType)

Use these for advanced typography:

```yaml
body-md:
  fontFamily: "Public Sans"
  fontSize: 16px
  fontWeight: 400
  lineHeight: 1.6
  fontFeature: "'kern', 'liga', 'tnum'"   # tabular numbers for data
  fontVariation: "'wght' 400, 'opsz' 14"  # variable-font axis
```

Refer to MDN for valid feature tag list.

## Recommended level taxonomy

Per spec.md L143-L147, most systems have 9-15 levels organized in semantic categories × sizes:

| Category | sm | md | lg | xl | display |
|---|---|---|---|---|---|
| `headline-*` | headline-sm | headline-md | headline-lg | headline-xl | headline-display |
| `body-*` | body-sm | body-md | body-lg | — | — |
| `label-*` | label-sm | label-md | label-lg | — | — |
| `caption` | caption | — | — | — | — |
| `display` | — | — | — | — | display-mega |

Suggested 11-level system:
```yaml
typography:
  display-hero:        # 64-96px, weight 700
  headline-lg:         # 36-48px, weight 600
  headline-md:         # 28-32px, weight 600
  headline-sm:         # 22-24px, weight 600
  body-lg:             # 18px, weight 400
  body-md:             # 16px, weight 400
  body-sm:             # 14px, weight 400
  label-lg:            # 16px, weight 500, possibly uppercase + tracking
  label-md:            # 14px, weight 500
  label-sm:            # 12px, weight 500
  caption:             # 11-12px, weight 400
```

### Variable fonts and weight axis

Variable fonts allow continuous weight values via `font-variation-settings`. Declare the canonical weight in `fontWeight` and use `fontVariation` for axis values:

```yaml
headline-lg:
  fontFamily: "Public Sans"
  fontSize: 36px
  fontWeight: 650
  fontVariation: "'wght' 650, 'wdth' 100"
  lineHeight: 1.15
```

Note `fontWeight: 650` is valid for variable fonts even though it's between the 100-900 step values; the linter accepts integers in [100..900] inclusive.

## Font fallback chains

The frontmatter `fontFamily` is the primary family — typically a single name. Prose section `## Typography` lists the full fallback chain:

```markdown
## Typography

- **Body / UI**: `Public Sans` — fallback: `system-ui, -apple-system, BlinkMacSystemFont, sans-serif`
- **Display**: `Public Sans` (650 weight) — fallback chain same as body
- **Mono / Code**: `JetBrains Mono` — fallback: `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`
```

Companion `tokens.css` (emitted by `bin/amw-design-md-emit-companions.py`) bakes the full fallback chain into CSS custom properties.

## CJK considerations

For Japanese / Chinese / Korean locale variants, the font stack and metrics are entirely different. See [TECH-cjk-localization](TECH-cjk-localization.md). Key points:

- Add a JP/KO/ZH primary font BEFORE the Latin fallback: `"Noto Sans JP", "Hiragino Sans", "Public Sans"`.
- Reduce body font-size by 1-2 px (CJK ideographs read smaller comfortably).
- Increase line-height by 0.1-0.2 (CJK needs more vertical breathing room).
- Letter-spacing remains 0; CJK has no concept of inter-character spacing in the Latin sense.

## Common patterns

### Display + headline + body × 3 sizes (11 levels)

Standard editorial product. See template above.

### Compact 7-level (developer tools)

```yaml
typography:
  display: 32px / 700 / 1.1
  heading: 24px / 600 / 1.2
  subheading: 18px / 600 / 1.3
  body: 16px / 400 / 1.5
  body-sm: 14px / 400 / 1.5
  caption: 12px / 400 / 1.4
  code: 14px (mono) / 400 / 1.5
```

(Schematic shorthand — actual frontmatter has full Typography sub-fields per row.)

### Marketing-rich 15-level (consumer brands)

Adds: hero, mega, eyebrow (uppercase tracking), oversized callout, button-lg, button-md, button-sm, link, mono. Used by Stripe, Spotify, Apple-style brands.

## Worked example — full row

```yaml
typography:
  body-md:
    fontFamily: "Public Sans"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "0"
    fontFeature: "'kern', 'liga'"
```

## Cross-references

- [TECH-01-yaml-frontmatter](./TECH-01-yaml-frontmatter.md) — YAML rules
  > What it does · When to use · Hard rules · Delimiters · Top-level fields · Value type rules · Token references · YAML quoting rules · Common gotchas · Worked example — minimal valid frontmatter · Worked example — token reference inside components · Validation · Cross-references
- [TECH-05-token-references](./TECH-05-token-references.md) — using `{typography.X}` in components
  > What it does · Hard rules · Syntax · Where references are valid · Resolution model · Scalar groups must point to primitives · Composite references allowed inside `components` · Self-references and cycles · What a resolved DESIGN.md looks like · When NOT to use references · Common errors · Validation · Cross-references
- [TECH-cjk-localization](./TECH-cjk-localization.md) — CJK font / size / line-height adjustments
  > What it does · When to use · How it works · Typography (per language) · Layout · Punctuation + line breaking · Cultural symbolism · Microcopy patterns · Locale machinery · SEO impacts · Performance · Minimal example · Gotchas · Cross-references · Source attribution
- [canonical-spec-google-alpha](canonical-spec-google-alpha.md) — full Typography spec
  > File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Top-level fields · Type definitions · Component property tokens (spec.md L312-L319) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Section content guidance · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references
