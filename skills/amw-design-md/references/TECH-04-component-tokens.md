---
name: TECH-04-component-tokens
category: authoring
source: design.md-main/docs/spec.md L277-L319
also-in: TECH-01-yaml-frontmatter.md, TECH-05-token-references.md, TECH-15-design-md-as-input.md
status: stable
---

# TECH: Component tokens authoring

## What it does

Documents the `components:` frontmatter map. Covers naming, variants, properties, and the special permission for composite token references inside component values.

## Hard rules

### Property whitelist (per spec.md L312-L319)

Each component property is one of:

- `backgroundColor` — Color (or `{colors.X}`)
- `textColor` — Color (or `{colors.X}`)
- `typography` — Typography object reference (`{typography.X}`)
- `rounded` — Dimension (or `{rounded.X}`)
- `padding` — Dimension
- `size` — Dimension
- `height` — Dimension
- `width` — Dimension

Other properties are accepted with warning. Common community-extended properties:

- `border` — `"1px solid {colors.border-subtle}"`
- `borderColor` — Color
- `borderWidth` — Dimension
- `boxShadow` — string
- `gap` — Dimension

The linter warns but does not reject these. The plugin's authoring tools (`amw-design-md-author-agent`) emit only the whitelist by default; community extensions are emitted only when the source DESIGN.md (V2 → V1 conversion) had them.

### Variant naming convention

Variants use suffixed keys (per spec.md L295):

```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary-light}"
  button-primary-pressed:
    backgroundColor: "{colors.primary-dark}"
  button-primary-disabled:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.on-surface-disabled}"
```

The convention is `<component-name>-<variant>` where variant is one of:

- State variants: `-hover`, `-active`, `-pressed`, `-focus`, `-disabled`, `-error`
- Size variants: `-sm`, `-md`, `-lg`
- Visual variants: `-primary`, `-secondary`, `-tertiary`, `-ghost`, `-outline`, `-destructive`
- Compound: `button-primary-hover`, `button-secondary-disabled`

The reader expects ONE base entry per component (no suffix) and zero or more variant entries. Variants partially override base — they SHOULD only declare the changed properties:

```yaml
button-primary:
  backgroundColor: "{colors.primary}"
  textColor: "{colors.on-primary}"
  rounded: "{rounded.md}"
  padding: 12px
button-primary-hover:
  backgroundColor: "{colors.primary-hover}"   # only the changed prop
```

This keeps the file scanable. A variant that re-declares all base properties is verbose but accepted.

### Composite token references allowed inside `components.*`

Per spec.md L76: "Within the `components` section, references to composite values (e.g., `{typography.label-md}`) are permitted."

This is a special exception. In `colors.*`, `typography.*`, `rounded.*`, `spacing.*`, references must point to primitives. In `components.*`, references to whole sub-objects (like a typography row) are allowed:

```yaml
components:
  button-primary:
    typography: "{typography.label-md}"   # OK — whole Typography object
    # Reader applies all of label-md's font-family, size, weight, etc.
```

This means a button's typography is whatever `typography.label-md` is, in full. The reader uses the resolved object directly.

## Common component patterns

### Button (primary/secondary/ghost)

```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  button-primary-disabled:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.on-neutral-disabled}"

  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    border: "1px solid {colors.primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  button-secondary-hover:
    backgroundColor: "{colors.surface-elevated}"

  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
```

### Input

```yaml
components:
  input-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    border: "1px solid {colors.border-subtle}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 12px
    height: 44px
  input-focus:
    border: "2px solid {colors.primary}"
  input-error:
    border: "1px solid {colors.error}"
  input-disabled:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.on-neutral-disabled}"
```

### Card

```yaml
components:
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    border: "1px solid {colors.border-subtle}"
    rounded: "{rounded.lg}"
    padding: 24px
  card-elevated:
    boxShadow: "rgba(26, 28, 30, 0.08) 0px 4px 8px -2px"
```

### Chip / Badge

```yaml
components:
  chip-default:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 4px 8px
  chip-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
```

## Hover-state derivation strategies

If declaring full state matrix is too verbose, an alternative is to declare only base components and document the state derivation in the prose section:

```markdown
## Components

State derivation: hover lightens background by 8%, pressed darkens by 8%, focus adds a 2-px primary-color outline outside the rounded boundary, disabled drops opacity to 50%.
```

This is accepted; the AI agent reads the prose and applies the derivation to the rendered HTML/CSS. Trade-off: less explicit; more flexible.

## Anti-patterns

- Declaring `button-primary-hover.backgroundColor` as the same value as `button-primary.backgroundColor` (no actual hover effect).
- Declaring 14 size variants when 3 (sm/md/lg) suffice.
- Declaring `button-primary-disabled.backgroundColor` with poor contrast vs disabled text (still 4.5:1 needed for legibility per WCAG-AA-large).
- Mixing component-property names — using both `backgroundColor` and `bg` across different components.

## Cross-references

- [TECH-01-yaml-frontmatter](./TECH-01-yaml-frontmatter.md) — YAML rules
- [TECH-05-token-references](./TECH-05-token-references.md) — `{path.to.token}` syntax
- [TECH-15-design-md-as-input](./TECH-15-design-md-as-input.md) — how wireframe-builder consumes these tokens
- `../canonical-spec-google-alpha.md` — full Components spec
