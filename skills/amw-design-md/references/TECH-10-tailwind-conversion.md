---
name: TECH-10-tailwind-conversion
category: extraction
source: tailwind-to-design-md-main/src/{loader,css-parser,mapper,generator}.ts
also-in: TECH-08-codebase-extraction.md, TECH-12-companion-files.md
status: stable
---

# TECH: Tailwind config + globals.css → DESIGN.md

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Inputs](#inputs)
- [How it works (4-step pipeline)](#how-it-works-4-step-pipeline)
  - [Step 1 — Loader (loader.ts equivalent)](#step-1-loader-loaderts-equivalent)
  - [Step 2 — CSS-parser (css-parser.ts equivalent)](#step-2-css-parser-css-parserts-equivalent)
  - [Step 3 — Mapper (mapper.ts equivalent)](#step-3-mapper-mapperts-equivalent)
  - [Step 4 — Generator (generator.ts equivalent)](#step-4-generator-generatorts-equivalent)
- [Component derivation](#component-derivation)
- [Worked example](#worked-example)
- [Limitations](#limitations)
- [Validation](#validation)
- [Cross-references](#cross-references)


## What it does

Documents the high-fidelity mechanical conversion path from a Tailwind project (`tailwind.config.{ts,js,mjs,cjs}` + `globals.css` with `:root` CSS variables) to a Variant 1 DESIGN.md. Unlike [TECH-08-codebase-extraction](TECH-08-codebase-extraction.md) which is regex-based, this path uses `jiti` to actually evaluate the Tailwind config — so it handles dynamic values, computed configs, and shadcn-style HSL+CSS-variable patterns correctly.

The bin script is `bin/amw-design-md-from-tailwind.mjs`. Pure-local Node.js, runtime deps `jiti` (TypeScript-config evaluator) and `picocolors` (CLI output). Both are zero-API-key, npm-installable.

The agent owner is `amw-design-md-extractor-agent`.

## When to use

- The project's primary token source is a Tailwind config + globals.css (e.g., shadcn/ui project).
- High-fidelity extraction needed (color values exact, not approximated).
- The user wants to keep Tailwind as the source-of-truth and emit DESIGN.md as a derived artifact.

## When NOT to use

- Project has no Tailwind → use [TECH-08-codebase-extraction](TECH-08-codebase-extraction.md).
  > What it does · When to use · What it scans · Inputs · Extraction heuristics · Color extraction · Typography extraction · Spacing extraction · Rounded extraction · Component extraction · Output · Failure modes · When this is the wrong tool · Cross-references
- Project has Tailwind but the actual deployed UI uses different values (drift) → use [TECH-07-url-extraction](TECH-07-url-extraction.md) to capture deployed reality.
  > What it does · When to use · Architecture · Inputs · What `dev-browser eval` returns · Heuristics for token extraction · Colors · Typography · Spacing · Radius · Components · Output structure · Failure modes and recovery · Validation gate · Cross-references
- The Tailwind config has runtime function calls or imports an unsafe module — `jiti` evaluates the config; if the config has side-effects, those run.

## Inputs

```bash
node bin/amw-design-md-from-tailwind.mjs \
  --config <path-to-tailwind.config.{ts,js,mjs,cjs}> \
  --css <path-to-globals.css> \
  [--out <output-path>] \
  [--name <design-system-name>] \
  [--desc <one-line-description>]
```

Required: `--config`, `--css`. Default output: `./DESIGN.md`.

## How it works (4-step pipeline)

The Node.js port mirrors the upstream `tailwind-to-design-md` 4-file architecture. The plugin's pure-local port lives at `bin/amw-design-md-from-tailwind.mjs`.

### Step 1 — Loader (loader.ts equivalent)

`loadTailwindConfig(configPath)` uses `jiti` to evaluate the config (TypeScript or JavaScript) and extract `theme.colors`, `theme.borderRadius`, `theme.spacing`, `theme.fontSize`, `theme.fontFamily` — including merging with `theme.extend.*`.

For shadcn-style configs, the colors look like:

```ts
colors: {
  primary: {
    DEFAULT: "hsl(var(--primary))",
    foreground: "hsl(var(--primary-foreground))",
  },
  // ...
}
```

The loader returns the structure as-is. Resolution happens in step 3.

### Step 2 — CSS-parser (css-parser.ts equivalent)

`parseCssVariables(cssPath)` reads `globals.css` and extracts:

- The `:root { ... }` block → light-mode CSS variables.
- The `.dark { ... }` block → dark-mode CSS variables (if present).

Variable values may be:

- Direct hex: `--primary: #1a1c1e;`
- HSL triplets: `--primary: 220 8% 11%;` (shadcn convention)
- Calc/rem: `--radius: 0.5rem;` or `calc(var(--radius) - 2px)`

The parser converts HSL triplets to hex via `hslToHex(h, s, l)`. Calc expressions are kept literal (resolved later if possible).

### Step 3 — Mapper (mapper.ts equivalent)

`mapTokens(tailwindTokens, cssVars)` resolves Tailwind values referencing CSS variables:

- `hsl(var(--primary))` → resolves to the `--primary` value from cssVars.light → the resolved hex.
- Direct hex passes through.
- HSL value strings are converted.

Returns `DesignTokens`:
```ts
{
  colors: Record<string, string>,        // flattened, normalized, hex values
  rounded: Record<string, string>,        // px/rem values
  spacing: Record<string, string>,        // px/rem values
  fontFamilies: Record<string, string>,
  componentSemantics: Record<string, Record<string, string>>,
}
```

The mapper also normalizes keys: `primary-DEFAULT` → `primary`, `primary-foreground` → `primary-foreground` (kept).

### Step 4 — Generator (generator.ts equivalent)

`generateDesignMd(tokens, name, description)` emits the Variant 1 DESIGN.md as a string:

1. YAML frontmatter with `version: alpha`, `name`, `description`, `colors:`, `rounded:`, `spacing:`, `components:`.
2. Markdown body with auto-generated `## Overview`, `## Colors` (grouped: surfaces / brand / states / chrome), `## Typography` (font families), `## Layout` (spacing scale), `## Shapes` (rounded scale), `## Components` (button/card semantics if detected), `## Do's and Don'ts` (default placeholder rules).

The generator annotates color pairs with WCAG-AA contrast: `- \`primary\`: \`#1a1c1e\` — contrast with pair: 7.42:1 (WCAG AAA)`.

## Component derivation

The plugin's port derives a small set of component-semantic tokens from common shadcn/Tailwind patterns:

| Component | If `colors.X` exists | Map to |
|---|---|---|
| `button-primary` | `colors.primary` | `backgroundColor: "{colors.primary}"`, `textColor: "{colors.primary-foreground}"` (if present) |
| `button-secondary` | `colors.secondary` | same pattern |
| `button-destructive` | `colors.destructive` | same pattern |
| `card` | `colors.card` | `backgroundColor: "{colors.card}"`, `textColor: "{colors.card-foreground}"` |

Components are emitted only when the underlying tokens exist. For non-shadcn projects (different naming), the user can provide `--component-map <json>` (future enhancement; currently shadcn pattern only).

## Worked example

Input `tailwind.config.ts`:
```typescript
export default {
  theme: {
    colors: {
      primary: {
        DEFAULT: "hsl(var(--primary))",
        foreground: "hsl(var(--primary-foreground))",
      },
      background: "hsl(var(--background))",
      foreground: "hsl(var(--foreground))",
    },
    borderRadius: {
      lg: "var(--radius)",
      md: "calc(var(--radius) - 2px)",
      sm: "calc(var(--radius) - 4px)",
    },
  },
};
```

Input `globals.css`:
```css
:root {
  --primary: 220 8% 11%;
  --primary-foreground: 30 22% 96%;
  --background: 30 22% 96%;
  --foreground: 220 8% 11%;
  --radius: 0.5rem;
}
```

Output frontmatter (excerpt):
```yaml
---
version: alpha
name: "My Design System"
description: "Auto-generated from Tailwind CSS configuration"

colors:
  primary: "#1A1C1E"
  primary-foreground: "#F7F5F2"
  background: "#F7F5F2"
  foreground: "#1A1C1E"

rounded:
  lg: "0.5rem"
  md: "calc(0.5rem - 2px)"
  sm: "calc(0.5rem - 4px)"

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
---
```

## Limitations

- **Variable spacing scale**: Tailwind's default spacing uses `0.25rem * N` for N from 0 to 96. The port slices the first 12 entries by default to keep the DESIGN.md spacing scale compact (`spacing.0`, `spacing.1`, `spacing.2`, ...). Configurable via `--spacing-cap N`.
- **Calc expressions**: `rounded.md = "calc(0.5rem - 2px)"` is preserved literally — the linter accepts this since it's a string. Some downstream consumers may not resolve it; `tokens.css` companion emits the literal `calc()`.
- **Custom plugin-extended values**: Tailwind plugins that inject theme values (e.g., `@tailwindcss/typography`) are evaluated by jiti and included if present in the resolved theme.
- **Pre-Tailwind-v4**: Targets Tailwind v3 syntax (`tailwind.config.ts`). For Tailwind v4 (`@theme inline { ... }` in CSS), use the codebase-extraction path which has v4 awareness.

## Validation

Output passes the standard validation chain:

```bash
bash <plugin-root>/bin/amw-design-md-lint.sh DESIGN.md
python3 <plugin-root>/bin/amw-design-md-validate.py DESIGN.md
python3 <plugin-root>/bin/amw-design-md-contrast.py DESIGN.md
```

If the project has shadcn's standard pairs (`primary` + `primary-foreground`, etc.), the contrast checker passes — shadcn picks WCAG-AA-compliant pairs by design.

## Cross-references

- [TECH-08-codebase-extraction](./TECH-08-codebase-extraction.md) — heuristic regex-based codebase extraction (fallback when jiti not available)
  > What it does · When to use · What it scans · Inputs · Extraction heuristics · Color extraction · Typography extraction · Spacing extraction · Rounded extraction · Component extraction · Output · Failure modes · When this is the wrong tool · Cross-references
- [TECH-12-companion-files](./TECH-12-companion-files.md) — emit `<tokens.css>` from the resulting DESIGN.md
  > What it does · The four companions · `tokens.css` — CSS custom properties · `tokens.json` — W3C Design Tokens format · `component-inventory.md` — human-readable component list · `usage-prompt.md` — Drop-in agent prompt · Inputs to the emitter · Resolution behavior · Synchronization rule · Cross-references
- `../../../bin/amw-design-md-from-tailwind.mjs` — the bin script
