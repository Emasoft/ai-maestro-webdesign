<!--
Direct-port + adapt from SKILLS-TO-INTEGRATE/web-design/claude-skill-design-system (MIT,
references/component-scanning.md) and claude-design-suite/plugins/design-systems/skills/
component-spec (MIT, SKILL.md anatomy/variants/states schema). 2026-05-27.
-->

# TECH — Extractor Component Detection (T-091, T-094)

## Table of Contents

- [When the extractor runs component detection](#when-the-extractor-runs-component-detection)
- [Codebase detection — five patterns, in priority order](#codebase-detection-five-patterns-in-priority-order)
- [URL detection — DOM landmarks + ARIA roles](#url-detection-dom-landmarks-aria-roles)
- [State detection (T-094)](#state-detection-t-094)
- [shadcn / Radix specific signals](#shadcn-radix-specific-signals)
- [What the extractor skips](#what-the-extractor-skips)
- [Confidence and fallbacks](#confidence-and-fallbacks)
- [Output — what lands in DESIGN.md](#output-what-lands-in-designmd)
- [Validation gate](#validation-gate)
- [Cross-references](#cross-references)

How the codebase extractor (`bin/amw-design-md-from-codebase.py`) and the URL extractor
(`bin/amw-design-md-from-url.sh`) detect **component shapes** (buttons, cards, inputs,
modals, navigation, badges) AND **state variants** (default, hover, focus, active,
disabled, loading, error, selected). Activated by `--extract-components` and reused
implicitly when a DESIGN.md emits non-empty `## 4. Component Stylings`.

## When the extractor runs component detection

- `--extract-components` was passed to `bin/amw-design-md-from-codebase.py` or
  `bin/amw-design-md-from-url.sh`.
- Or the calling agent (`amw-design-md-extractor-agent`) determined the source is
  rich enough (≥3 colors, ≥1 typography role) AND the target DESIGN.md needs a
  populated `## 4. Component Stylings` section. An empty `## 4.` is allowed but
  every authored DESIGN.md ships better when this section is non-empty.

When the flag is absent and the source has no component signal, the extractor
emits a one-line `# TODO: component-spec` placeholder for each canonical entry
(button-primary, button-secondary, card, input) rather than fabricating tokens.

## Codebase detection — five patterns, in priority order

The codebase scanner reads each component file (`components/**/*.{tsx,jsx,vue,svelte}`)
and tries patterns in this fixed priority order. The first pattern that resolves
non-empty variant + state lists is the one whose output is recorded; later patterns
augment only the lists the prior pattern left empty.

### Pattern 1 — `cva()` call with `variants` object (class-variance-authority)

```tsx
const buttonVariants = cva('base-classes', {
  variants: {
    variant: {
      default: '...',
      secondary: '...',
      outline: '...',
      ghost: '...',
      destructive: '...',
    },
    size: {
      sm: '...',
      default: '...',
      lg: '...',
      icon: '...',
    },
  },
})
```

**Extract:** `variants = [default, secondary, outline, ghost, destructive]`,
`sizes = [sm, default, lg, icon]`. Strongest signal — `cva()` is the
shadcn/Radix idiom and the variant list is the source of truth.

### Pattern 2 — TypeScript union type

```tsx
type ButtonVariant = 'default' | 'secondary' | 'outline' | 'ghost' | 'destructive'
type ButtonSize = 'sm' | 'default' | 'lg'
```

**Extract:** variant and size union members. Used when `cva()` is absent but
the component is typed strictly.

### Pattern 3 — Prop interface

```tsx
interface ButtonProps {
  variant?: 'default' | 'secondary' | 'outline' | 'ghost' | 'destructive'
  size?: 'sm' | 'default' | 'lg'
  disabled?: boolean
  loading?: boolean
  isLoading?: boolean
  asChild?: boolean
}
```

**Extract:** variants, sizes, AND boolean state props (disabled, loading).
Pattern 3 is the primary path for surfacing **state variants** (see §State
detection below).

### Pattern 4 — Switch statement

```tsx
switch (variant) {
  case 'primary': return 'bg-primary text-white'
  case 'secondary': return 'bg-secondary text-secondary-foreground'
  case 'outline': return 'border border-input bg-background'
}
```

**Extract:** variant list from `case` literals.

### Pattern 5 — Object map

```tsx
const variantStyles = {
  default: 'bg-primary text-primary-foreground',
  secondary: 'bg-secondary text-secondary-foreground',
  destructive: 'bg-destructive text-destructive-foreground',
}
```

**Extract:** `variants = Object.keys(variantStyles)`. Weakest signal — only
used when Patterns 1–4 returned empty.

## URL detection — DOM landmarks + ARIA roles

The URL extractor delegates to `amw-dev-browser` (see
[TECH-07-url-extraction](TECH-07-url-extraction.md)) and asks the live page
for component candidates via this evaluation. Each landmark / role / pattern
in the table maps to a canonical Variant 1 component-spec entry.

| Source pattern | Canonical entry |
|---|---|
| `<button>` or `[role="button"]` with `bg-{primary,accent,brand}` class | `button-primary` |
| Second-most-frequent `<button>` style class set | `button-secondary` |
| `<button>` with `[aria-label]` but no visible text | `button-icon` |
| `<input type="text">`, `<input type="email">`, `<input type="search">` | `input` |
| `<textarea>` (if styled differently from input) | `textarea` |
| `<select>` or `[role="combobox"]` | `select` |
| `<a>` with `href`, NOT inside `<nav>`, with same color as button-primary | `link-primary` |
| `<a>` inside `<nav>` or `<header>` | `nav-link` |
| `[role="dialog"]`, `[role="alertdialog"]`, `<dialog>` | `modal` |
| `[role="tablist"]` + `[role="tab"]` | `tabs` |
| `[role="alert"]`, `[role="status"]` | `alert` (variant=success/warning/error/info per color) |
| `<article>` or `<section>` with rounded border, padding ≥16px, shadow ≠ none | `card` |
| `<span>` / `<div>` with rounded ≥9999px, padding ~ 4-8×12-16px, font-size ≤14px | `badge` / `pill` |
| `<details>` or `[role="region"]` with `[aria-expanded]` toggle | `accordion` |
| `<svg>` with no `<text>`/`<title>` describing brand chrome (header/footer logo) | `logo` (recorded separately, see [TECH-extractor-icon-asset-export](TECH-extractor-icon-asset-export.md)) |

Confidence is computed per-entry: number of matching DOM nodes × 1.0 +
ARIA role presence × 0.5 + variant token resolution × 0.3. Entries with
confidence < 1.0 are emitted with a `# UNCERTAIN:` comment rather than as
canonical tokens.

## State detection (T-094)

State variants are read from THREE sources in priority order:

### Source 1 — Boolean props on the component interface (codebase only)

Always look for these props regardless of pattern:

| Prop name | Canonical state |
|---|---|
| `disabled` | disabled |
| `loading` / `isLoading` | loading |
| `error` / `hasError` | error |
| `checked` / `defaultChecked` | checked (checkboxes, toggles) |
| `selected` / `isSelected` | selected (selectable items) |
| `open` / `defaultOpen` | open (modals, dropdowns, accordions) |
| `active` | active (nav items, tabs) |
| `pressed` | pressed (toggle buttons; matches `aria-pressed`) |

If the prop is present in the interface, the state is added to the component's
`states` list in the emitted DESIGN.md.

### Source 2 — CSS pseudo-class selectors (codebase + URL)

The extractor counts occurrences of these pseudo-classes attached to the
component's class set or its base element:

| Pseudo-class | Canonical state |
|---|---|
| `:hover` | hover |
| `:focus`, `:focus-visible` | focus |
| `:active` | active |
| `:disabled`, `[disabled]`, `[aria-disabled="true"]` | disabled |
| `[aria-busy="true"]`, `[data-loading="true"]` | loading |
| `[aria-invalid="true"]`, `[data-error="true"]` | error |
| `[aria-checked="true"]`, `:checked` | checked |
| `[aria-selected="true"]`, `[data-state="selected"]` | selected |
| `[aria-expanded="true"]`, `[data-state="open"]` | open |
| `[aria-pressed="true"]`, `[data-state="on"]` | pressed |

Each match increments a state-confidence counter. A state is emitted in the
DESIGN.md only when the counter ≥ 1. The counter value is recorded in
`<output>.extraction-notes.md`.

### Source 3 — Variant strings that name a state directly

Some codebases use a `variant` enum that includes state-like values:

```tsx
variant?: 'default' | 'disabled' | 'loading' | 'error'
```

These ALWAYS emit the corresponding state regardless of Source 1/2 signal.
The extractor records `state_via=variant_enum` in extraction-notes so the
auditor knows the state is structural, not derived.

## shadcn / Radix specific signals

For shadcn components found at `components/ui/`:

- The `cn()` utility merges classes — variants are in `cva()` or inline
  objects (Pattern 1 / Pattern 5).
- `asChild` prop uses Radix `Slot` — the component renders as whatever child
  is passed. Record `asChild: true` in the component-spec metadata so the
  downstream wireframe-builder knows it is polymorphic.
- Most components have `className` prop forwarded — extracted variants
  apply to the BASE class set, but consumer-passed `className` overrides
  win at render time. The extractor still records the base variants.

## What the extractor skips

Per claude-skill-design-system's contract, skip these even when present:

- Layout components (Header, Footer, Sidebar, Layout, Main) — they are
  composition, not components.
- Page components (`app/page.tsx`, `pages/index.tsx`).
- Context providers.
- HOCs / wrapper components with no visual output.
- Style-only utility helpers (`cn()`, `clsx()`, `cva()` itself).

Skipping rationale is logged in extraction-notes so an auditor in Mode B
can re-include a skipped file if it does carry design intent.

## Confidence and fallbacks

When variants cannot be enumerated from any of the five patterns:

1. The extractor greps the codebase for `<ButtonName>` usages and tries to
   read the `variant=` prop literal from JSX call sites. Repeated literals
   become the variant list.
2. If Storybook is present (`*.stories.{ts,tsx,mdx}`), the extractor reads
   the `argTypes.variant.options` list and uses it as the variant
   enumeration. Same for `argTypes.size.options`.
3. If still empty, the extractor emits ONLY `default` and `disabled` for
   variants and notes `confidence=low` in extraction-notes.

## Output — what lands in DESIGN.md

```yaml
components:
  button-primary:
    base:
      background: "{colors.primary}"
      foreground: "{colors.primary-foreground}"
      rounded: "{rounded.md}"
      padding: "{spacing.2} {spacing.4}"
      font: "{typography.button}"
    variants:
      size: [sm, default, lg, icon]
      tone: [default, destructive]
    states:
      hover:
        background: "{colors.primary-hover}"
      focus:
        ring: "{colors.ring}"
      disabled:
        opacity: 0.5
        cursor: not-allowed
      loading:
        opacity: 0.7
        # spinner glyph TBD
```

The `# UNCERTAIN:` and `# TODO:` markers stay in the YAML when the
extractor couldn't resolve a token — they are the explicit gap signal for
the auditor and the wireframe-builder.

## Validation gate

After component detection runs, the extractor:

1. Re-runs `bin/amw-design-md-lint.sh` to verify every component-spec entry
   references resolvable tokens (no `{colors.does-not-exist}`).
2. Records the component count, variant count, and state count in the
   `recommendations[]` of the agent's return contract: `"Found 4 components,
   12 variants, 18 state-rules. button-primary has full hover/focus/disabled/
   loading coverage; card has only base + hover."`
3. Failing token references that the codebase did not provide stay as
   `# UNCERTAIN:` and surface as P1 lint warnings (not P0 errors).

## Cross-references

- [TECH-04-component-tokens](TECH-04-component-tokens.md) — canonical
  component-token schema this extractor targets
- [TECH-07-url-extraction](TECH-07-url-extraction.md) — URL extraction
  pipeline that calls into the component-detection rules here
- [TECH-08-codebase-extraction](TECH-08-codebase-extraction.md) — codebase
  scan that calls into the five-pattern detector
- [TECH-extractor-icon-asset-export](TECH-extractor-icon-asset-export.md) —
  paired skill for icons, logos, raster assets discovered during the same
  scan
- [SKILL](../../amw-dev-browser/SKILL.md) — browser primitive used by URL
  detection
- [SKILL](../../amw-design-extract/SKILL.md) — sibling URL-extraction skill
  whose looser-format output feeds the strict DESIGN.md format here
