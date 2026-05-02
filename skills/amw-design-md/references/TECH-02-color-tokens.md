---
name: TECH-02-color-tokens
category: authoring
source: design.md-main/docs/spec.md L101-L139
also-in: TECH-01-yaml-frontmatter.md, TECH-05-token-references.md, TECH-11-validation-and-lint.md
status: stable
---

# TECH: Color tokens authoring

## What it does

Documents how to declare the `colors:` map in YAML frontmatter and how to write the `## Colors` prose section. Covers required tokens, recommended naming, contrast checking, and tonal-scale conventions.

## When to use

- Authoring a fresh DESIGN.md.
- Extracting tokens from a URL or codebase (the extractor produces these — but the post-extraction edit pass uses these rules).
- Auditing an existing DESIGN.md for color-token completeness.

## Hard rules

### At least primary required

Per spec.md L105: "At least the `primary` color palette must be defined."

A DESIGN.md without `colors.primary` is incomplete. The linter accepts it (the `colors:` map itself is optional) but the file fails the plugin's authoring rubric.

### Hex format

Every value MUST be `^#[0-9a-fA-F]{6}$` (6-digit) or `^#[0-9a-fA-F]{3}$` (3-digit short-form). The linter rejects:

- `rgb(26, 28, 30)` — not a hex
- `hsl(220, 8%, 11%)` — not a hex
- `slate-900` — Tailwind class, not a value
- `var(--primary)` — CSS variable, not a value
- `Midnight Forest Green` — descriptive name, not a value

Even though the prose may use descriptive names ("Midnight Forest Green"), the frontmatter must use hex.

### Recommended semantic names (non-normative)

Per spec.md L338:

| Name | Typical role |
|---|---|
| `primary` | Brand-identity color, primary CTAs |
| `secondary` | Supporting accent, secondary CTAs |
| `tertiary` | Optional third color, used sparingly |
| `neutral` | Page background, large surfaces |
| `surface` | Card / elevated-element backgrounds |
| `on-surface` | Text/icons on surfaces |
| `error` | Destructive states, error messaging |

Custom names are allowed. Common patterns:

- **Pair-based**: `primary` + `on-primary` (color + text-on-color pair)
- **Tonal scale**: `primary-10` / `primary-30` / `primary-60` / `primary-90` (lightness levels)
- **Semantic + state**: `primary` / `primary-hover` / `primary-pressed`

### Tonal-scale convention

If using tonal-scale naming, the suffix is a 0-100 lightness number where 0=darkest and 100=lightest. Common steps: 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99. Tokens reference like `{colors.primary-60}`.

The semantic-pair convention (`primary` + `on-primary`) is simpler and widely used; the tonal convention is Material 3-style and gives more flexibility. Pick one per design system; do not mix.

## Prose section authoring

The `## Colors` section in the markdown body explains the philosophy behind the tokens. Per spec.md L113-L124, it is bullet-list-style with descriptive names matching the frontmatter:

```markdown
## Colors

The palette is rooted in high-contrast neutrals and a single, evocative accent color.

- **Primary (#1A1C1E):** A deep ink used for headlines and core text to provide
  maximum readability and a sense of permanence.
- **Secondary (#6C7278):** A sophisticated slate used primarily for utilitarian
  elements like borders, captions, and metadata.
- **Tertiary (#B8422E):** A vibrant earthy red as the sole driver for
  interaction, used exclusively for primary actions and critical highlights.
- **Neutral (#F7F5F2):** A warm limestone that serves as the foundation for all
  pages.
```

Pattern: `- **<Descriptive Name> (<#hex>):** <Role explanation>`.

The descriptive name is for human readers; the hex value cross-references the frontmatter; the role explanation tells the AI agent when to use this color.

## Contrast checking

Every text-on-surface color pair must achieve WCAG-AA contrast (4.5:1 for body text, 3:1 for large text):

```bash
python3 <plugin-root>/bin/amw-design-md-contrast.py DESIGN.md
```

Output reports each declared pair's ratio. Pairs failing 4.5:1 should be:
1. Adjusted (darken/lighten one of the pair) until they pass, OR
2. Restricted to large-text-only use (and stated so in the prose), OR
3. Documented in `## Do's and Don'ts` as "do not pair these for body text".

## Common patterns

### Light + dark mode token pairs

If the design supports both light and dark modes, declare separate tokens:

```yaml
colors:
  surface-light: "#F7F5F2"
  surface-dark: "#1A1C1E"
  text-on-surface-light: "#1A1C1E"
  text-on-surface-dark: "#F7F5F2"
```

The `## Do's and Don'ts` or `## Components` prose explains which pair to use in which mode.

### Brand-tinted shadows

Variant 2 commonly uses brand-tinted shadow rgba like `rgba(26, 28, 30, 0.08)`. Variant 1 has no shadow token group; document brand-tinted shadow formulas in the `## Elevation & Depth` prose.

## Anti-patterns (from `ai-slop-avoid.md`)

- **S1**: Color name without hex — fail.
- **S2**: Token name in frontmatter mismatches hex in prose — fail.
- **S5**: Tokens named `red` / `blue` / `green` instead of semantic — fail (or redesign).

## Worked example

```yaml
colors:
  primary: "#1A1C1E"
  on-primary: "#F7F5F2"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
  surface: "#FFFFFF"
  on-surface: "#1A1C1E"
  surface-elevated: "#F7F5F2"
  border-subtle: "#E5E2DD"
  border-strong: "#1A1C1E"
  error: "#B8422E"
  success: "#1A7F37"
  warning: "#9B7B17"
```

Prose paired:

```markdown
## Colors

A high-contrast neutral palette anchored by a single earthy red accent.

- **Primary (#1A1C1E):** Deep charcoal — headlines, primary text, primary CTA fill.
- **On-primary (#F7F5F2):** Limestone — text on primary surfaces.
- **Secondary (#6C7278):** Slate — borders, metadata, captions.
- **Tertiary (#B8422E):** Earthy red — sole interaction driver.
- **Neutral (#F7F5F2):** Warm limestone — page background.
- **Surface (#FFFFFF):** Card / elevated-element background.
- **Border-subtle (#E5E2DD):** Default hairline.
- **Error (#B8422E):** Same hue as tertiary; restrict to error context, not promotion.
```

## Cross-references

- [TECH-01-yaml-frontmatter](./TECH-01-yaml-frontmatter.md) — YAML rules
- [TECH-05-token-references](./TECH-05-token-references.md) — using `{colors.X}` in components
- [TECH-11-validation-and-lint](./TECH-11-validation-and-lint.md) — running the contrast checker
- `../ai-slop-avoid.md` — color-token anti-patterns
