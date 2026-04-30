---
name: TECH-12-companion-files
category: emission
source: design-system-extractor-skill (companion-file family); W3C Design Tokens 2025.10
also-in: TECH-05-token-references.md, TECH-15-design-md-as-input.md
status: stable
---

# TECH: Companion files (tokens.css, tokens.json, component-inventory.md, usage-prompt.md)

## What it does

Documents the four companion files the plugin can emit alongside a DESIGN.md to serve different downstream consumers (build systems, CI, AI agents, designers). The bin script is `bin/amw-design-md-emit-companions.py`.

The four companions all derive from a single source-of-truth DESIGN.md. Editing the DESIGN.md and re-running the emitter regenerates them. Hand-editing the companions is forbidden — the next emitter run overwrites the changes.

## The four companions

### 1. `tokens.css` — CSS custom properties

A CSS file declaring every token as a `:root` custom property. Optional dark-mode `.dark` block for projects that declare dark-mode counterparts.

Format:
```css
/* Auto-generated from DESIGN.md. Do not edit by hand. */

:root {
  /* Colors */
  --primary: #1a1c1e;
  --on-primary: #f7f5f2;
  --secondary: #6c7278;
  --tertiary: #b8422e;
  --neutral: #f7f5f2;
  --surface: #ffffff;
  --on-surface: #1a1c1e;

  /* Typography */
  --font-family-display: "Public Sans", system-ui, sans-serif;
  --font-family-body: "Public Sans", system-ui, sans-serif;
  --font-family-mono: "JetBrains Mono", ui-monospace, Menlo, monospace;

  --font-size-headline-lg: 36px;
  --font-size-body-md: 16px;
  --font-weight-headline: 600;
  --line-height-body-md: 1.6;

  /* Rounded */
  --rounded-sm: 4px;
  --rounded-md: 8px;
  --rounded-lg: 12px;
  --rounded-full: 9999px;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 32px;
  --space-xl: 64px;
}
```

Consumers:
- Direct CSS / SCSS / LESS projects (use `var(--primary)` in component code).
- Tailwind v3 + shadcn projects (the CSS variables back the Tailwind utility classes).
- Any framework that expects `:root`-declared tokens.

### 2. `tokens.json` — W3C Design Tokens format

JSON formatted per the W3C Design Tokens Community Group 2025.10 specification (https://www.designtokens.org/tr/2025.10/format/). Each token has `$value` and `$type`.

Format:
```json
{
  "colors": {
    "primary": {"$value": "#1a1c1e", "$type": "color"},
    "on-primary": {"$value": "#f7f5f2", "$type": "color"},
    "secondary": {"$value": "#6c7278", "$type": "color"},
    "tertiary": {"$value": "#b8422e", "$type": "color"},
    "surface": {"$value": "#ffffff", "$type": "color"}
  },
  "typography": {
    "headline-lg": {
      "$value": {
        "fontFamily": "Public Sans",
        "fontSize": "36px",
        "fontWeight": 600,
        "lineHeight": 1.15,
        "letterSpacing": "-0.02em"
      },
      "$type": "typography"
    },
    "body-md": {
      "$value": {
        "fontFamily": "Public Sans",
        "fontSize": "16px",
        "fontWeight": 400,
        "lineHeight": 1.6
      },
      "$type": "typography"
    }
  },
  "rounded": {
    "sm": {"$value": "4px", "$type": "dimension"},
    "md": {"$value": "8px", "$type": "dimension"},
    "lg": {"$value": "12px", "$type": "dimension"},
    "full": {"$value": "9999px", "$type": "dimension"}
  },
  "spacing": {
    "xs": {"$value": "4px", "$type": "dimension"},
    "sm": {"$value": "8px", "$type": "dimension"},
    "md": {"$value": "16px", "$type": "dimension"},
    "lg": {"$value": "32px", "$type": "dimension"},
    "xl": {"$value": "64px", "$type": "dimension"}
  },
  "components": {
    "button-primary": {
      "backgroundColor": {"$value": "{colors.primary}", "$type": "color"},
      "textColor": {"$value": "{colors.on-primary}", "$type": "color"},
      "rounded": {"$value": "{rounded.md}", "$type": "dimension"},
      "padding": {"$value": "12px", "$type": "dimension"}
    }
  }
}
```

Consumers:
- Style Dictionary (build-time token transformation to multiple platforms).
- Figma Variables (direct import).
- Tokens Studio (Figma plugin).
- Custom code generators (Swift, Android, iOS).

The W3C format preserves token references (`{colors.primary}`) inside `components.*`.

### 3. `component-inventory.md` — human-readable component list

Markdown listing every component declared in `components:` frontmatter, with their resolved values, intended use, and example usage prompt. For designers and developers who want a "what components do we have" table without parsing YAML.

Format:
```markdown
# Component Inventory

Generated from DESIGN.md on <timestamp>. Do not edit by hand.

## Buttons

### `button-primary` — Primary CTA

| Property | Value (resolved) | Source token |
|---|---|---|
| backgroundColor | `#1a1c1e` | `{colors.primary}` |
| textColor | `#f7f5f2` | `{colors.on-primary}` |
| typography | Public Sans 14px / 500 / 1.4 | `{typography.label-md}` |
| rounded | `8px` | `{rounded.md}` |
| padding | `12px` | (literal) |

**Use:** Single most important action per screen.

**States:** `button-primary-hover` (lighter background), `button-primary-disabled` (neutral fill).

**Example prompt for AI agent:**
> Render a primary CTA button labeled "Sign up". Use `button-primary` token; minimum 44px height; full-width on mobile, content-width on desktop.

---

### `button-secondary` — Secondary CTA

…

---

## Inputs

### `input-default` — Text input

…

---

## Cards

### `card` — Default container

…
```

Consumers:
- Designers needing a quick reference.
- Code reviewers checking a generated component against the spec.
- AI agents when one wants a TL;DR of declared components without parsing the full DESIGN.md.

### 4. `usage-prompt.md` — Drop-in agent prompt

A standalone markdown file with system-prompt-style language an AI agent can be given alongside a generation request. It bakes in the design system's identity, the color list, the typography list, and the must-not rules in a compact form.

Format:
```markdown
# Design System Reference Prompt

You are generating UI for the {name} design system. Apply ALL of the following constraints when writing HTML, JSX, CSS, or Tailwind classes.

## Colors (use semantic names, never inline hex)

- Primary brand: `--primary` (#1a1c1e) — single most-important CTA per screen
- Secondary: `--secondary` (#6c7278) — borders, captions, metadata
- Tertiary: `--tertiary` (#b8422e) — interaction accent only
- Surface: `--surface` (#ffffff) — page and card backgrounds
- On-surface: `--on-surface` (#1a1c1e) — body text on surface

## Typography

- Display: Public Sans 36px / 600 / 1.15 — `var(--font-headline-lg)`
- Body: Public Sans 16px / 400 / 1.6 — `var(--font-body-md)`
- Label: Public Sans 14px / 500 / 1.4 — `var(--font-label-md)`

## Spacing

8px base unit. Use `--space-xs (4px)`, `--space-sm (8px)`, `--space-md (16px)`, `--space-lg (32px)`, `--space-xl (64px)`. Never use values outside this scale.

## Components

- Use `button-primary` for the single most important action per screen.
- Use `input-default` for text inputs; always pair with a visible `<label>`.
- Use `card` for grouped content with 24px internal padding.

## Rules (hard constraints)

- DO maintain WCAG AA contrast (4.5:1 normal text, 3:1 large text).
- DO use semantic token names; never inline hex values.
- DON'T mix rounded and sharp corners in the same view.
- DON'T introduce new colors without updating DESIGN.md first.
- DON'T use more than two font weights on a single screen.

If a component or token isn't defined here, stop and ask. Do not invent values.
```

Consumers:
- Agents that consume DESIGN.md as upstream context (e.g., when a coding LLM needs the spec inlined into a system prompt).
- Code-generation tools that need a compact constraint summary.

## Inputs to the emitter

```bash
python3 bin/amw-design-md-emit-companions.py <DESIGN.md> [--out-dir DIR] [--targets css,json,inventory,prompt]
```

Args:
- `<DESIGN.md>`: source-of-truth DESIGN.md path. Required.
- `--out-dir DIR`: output directory. Default: same dir as DESIGN.md.
- `--targets`: comma-separated subset of `css,json,inventory,prompt`. Default: all four.

## Resolution behavior

- Token references (`{path.to.token}`) are resolved before emission. The resolved values appear in `tokens.css` (literal CSS), `component-inventory.md` (in the "Value (resolved)" column), and `usage-prompt.md` (literal hex inline).
- Token references are PRESERVED in `tokens.json` (`{colors.primary}` stays as a reference) per W3C Design Tokens convention. Build tools using Style Dictionary expect this.

## Synchronization rule

Hard rule: companion files MUST stay in sync with DESIGN.md. The auditor agent's Pass 2 (drift) check (`X1`-`X6` of `review-rubric.md`) verifies this:

- Every color in DESIGN.md appears in `tokens.json` with matching value.
- Every CSS variable in `tokens.css` matches a DESIGN.md token.
- `component-inventory.md` lists every declared component.

Drift fails the audit. The fix is always: re-run the emitter, do not hand-edit.

## Cross-references

- `./TECH-05-token-references.md` — reference resolution
- `./TECH-15-design-md-as-input.md` — how downstream agents consume the companion files
- `./review-rubric.md` — `X1`-`X6` drift checks
- `<plugin-root>/bin/amw-design-md-emit-companions.py` — the bin script
