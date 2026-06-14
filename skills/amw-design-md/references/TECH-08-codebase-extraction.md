---
name: TECH-08-codebase-extraction
category: extraction
source: design-md-builder/scripts/scan_codebase.py
also-in: TECH-07-url-extraction.md, TECH-10-tailwind-conversion.md
status: stable
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [What it scans](#what-it-scans)
- [Inputs](#inputs)
- [Extraction heuristics](#extraction-heuristics)
  - [Color extraction](#color-extraction)
  - [Typography extraction](#typography-extraction)
  - [Spacing extraction](#spacing-extraction)
  - [Rounded extraction](#rounded-extraction)
  - [Component extraction](#component-extraction)
- [Output](#output)
- [Failure modes](#failure-modes)
- [When this is the wrong tool](#when-this-is-the-wrong-tool)
- [Cross-references](#cross-references)

# TECH: Codebase scan → DESIGN.md extraction

## What it does

Scans a project directory and extracts design tokens from existing source files (Tailwind configs, CSS variables, theme files, package.json, frequency of utility classes, font packages) to draft a Variant 1 DESIGN.md.

The bin script is `bin/amw-design-md-from-codebase.py`. Pure-Python (stdlib only — no external deps). The agent owner is `amw-design-md-extractor-agent`.

## When to use

- User says: "extract DESIGN.md from this codebase"
- User says: "make a DESIGN.md from my project's Tailwind setup and CSS"
- Auditor's drift pass (Pass 2) uses this internally to produce a current-state DESIGN.md and diffs against the existing one.

## What it scans

The script walks the project directory tree (skipping `node_modules`, `.git`, `dist`, `build`, `.next`, `.turbo`, etc.) and inspects:

| File pattern | What it extracts |
|---|---|
| `package.json` | Framework (next, vite, expo), UI libraries (shadcn, radix, mui, chakra, mantine), font packages (@fontsource, next/font), tailwind version |
| `tailwind.config.{js,ts,mjs,cjs}` | Heuristic regex extraction of `colors:`, `borderRadius:`, `spacing:`, `fontFamily:` from the theme block (cannot eval JS safely) |
| `globals.css`, `*.css`, `*.scss` | `:root { --X: Y }` blocks → CSS custom properties |
| `app.css`, `theme.css`, `tokens.css` | Same as above, prioritized for token files |
| `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.astro` | Tailwind class frequency: `text-xl`, `p-4`, `m-2`, `rounded-md`, `font-sans`, etc. |
| `tokens.json`, `design-tokens.json` | If present, treated as already-canonical |

The script is intentionally regex-based. It cannot eval JavaScript safely (no jiti dependency in pure Python), so for complex Tailwind configs with computed values, it falls back to flagging "complex config detected; review manually" in the output.

## Inputs

```bash
python3 bin/amw-design-md-from-codebase.py <project-root> [--max-files N] [--out PATH] [--name NAME]
```

- `<project-root>`: project directory to scan. Required.
- `--max-files N`: cap on number of files inspected (default 1500).
- `--out PATH`: output DESIGN.md path. Default: `<project-root>/DESIGN.md`.
- `--name NAME`: design system name. Default: from `package.json:name` or directory name.

## Extraction heuristics

### Color extraction

Three sources, in priority:

1. **CSS custom properties** in `:root` blocks. Direct mapping `--primary: #hex` → `colors.primary: "#hex"`. HSL triplets like `--primary: 220 8% 11%` are converted to hex.
2. **Tailwind config `colors:` block**. Regex pattern matches the colors object, then for each key extracts hex/rgb/hsl literals.
3. **Hex-frequency in source files** (only if 1 and 2 are absent). Top 10 most-used hex values across `*.tsx` / `*.css` files are emitted as `colors.discovered-N` placeholders for the user to rename.

Token-name normalization:
- `--primary-DEFAULT` → `primary`
- `--primary-50` → `primary-50` (kept)
- `--background` → `surface` (heuristic)
- `--foreground` → `on-surface` (heuristic)

### Typography extraction

1. **next/font imports**: `import { Inter } from "next/font/google"` → `Inter` is one font family.
2. **@fontsource packages**: `@fontsource/public-sans` → `Public Sans`.
3. **Tailwind `fontFamily:` block** in config.
4. **CSS @font-face declarations**: `font-family: 'Custom'` registered in CSS.

Typography levels are inferred from Tailwind utility class frequency:
- `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, ..., `text-9xl` map to body-sm/md/lg, headline-md/lg/display, etc.
- Used class counts inform whether to include the level (>10 occurrences → include).

### Spacing extraction

Tailwind spacing utilities (`p-`, `m-`, `gap-`, `space-x-`, etc.) are counted. The most-used 8-12 spacing values become the `spacing:` map. Tailwind's default spacing scale (`0.25rem * N`) is preserved if the project uses the default.

### Rounded extraction

`rounded`, `rounded-sm`, `rounded-md`, `rounded-lg`, `rounded-xl`, `rounded-2xl`, `rounded-3xl`, `rounded-full` class frequency. Top 4-6 → `rounded:` map.

### Component extraction

Heuristic only: looks for a Button.tsx / button.tsx / Button.vue file and extracts its className-derived background/text/padding/rounded. If shadcn is detected (`@/components/ui/button.tsx` pattern), a default shadcn-button mapping is emitted.

## Output

A draft Variant 1 DESIGN.md at the specified path:

- YAML frontmatter populated with extracted tokens.
- Markdown body sections auto-generated with extraction notes:
  - `## Overview` — "This design system was extracted from the codebase at <path> on <timestamp>. Detected: <framework>, <UI libraries>, <font sources>."
  - `## Colors` — extracted color tokens with light prose explaining their CSS variable origin.
  - `## Typography` — extracted families with usage notes.
  - `## Layout` — extracted spacing scale + grid notes.
  - `## Components` — extracted button/input/card placeholders.
  - `## Do's and Don'ts` — generic placeholder rules; user customizes.

Plus an `extraction-notes.md` adjacent file with:
- Source files inspected
- Tokens that needed manual disambiguation
- Tokens with low confidence
- Files where the regex extractor failed (for user inspection)

## Failure modes

| Failure | Cause | Recovery |
|---|---|---|
| No `package.json` found | Project is not Node-based | Try heuristic on CSS files only; emit minimal DESIGN.md with `warnings` |
| Complex Tailwind config not regex-parseable | Computed values, function calls in `colors` | Emit partial extraction; flag in `extraction-notes.md` for manual review |
| No CSS variables, no Tailwind, custom CSS only | Project rolled its own | Fall back to hex-frequency in source files; mark all tokens as `discovered-*` |
| Project uses styled-components / emotion / vanilla-extract | CSS-in-JS, regex doesn't capture | Currently out of scope; emit warning, suggest manual authoring |

## When this is the wrong tool

- The user has a Tailwind config and globals.css and wants pure mechanical conversion → use `bin/amw-design-md-from-tailwind.mjs` instead (jiti-based; can eval the config). See [TECH-10-tailwind-conversion](TECH-10-tailwind-conversion.md).
  > What it does · When to use · When NOT to use · Inputs · How it works (4-step pipeline) · Step 1 — Loader (loader.ts equivalent) · Step 2 — CSS-parser (css-parser.ts equivalent) · Step 3 — Mapper (mapper.ts equivalent) · Step 4 — Generator (generator.ts equivalent) · Component derivation · Worked example · Limitations · Validation · Cross-references
- The user wants extraction from a deployed URL → use `bin/amw-design-md-from-url.sh`. See [TECH-07-url-extraction](TECH-07-url-extraction.md).
  > What it does · When to use · Architecture · Inputs · What `dev-browser eval` returns · Heuristics for token extraction · Colors · Typography · Spacing · Radius · Components · Output structure · Failure modes and recovery · Validation gate · Cross-references
- The user has a finished DESIGN.md and wants to audit drift → use `amw-design-md-auditor-agent` Pass 2 (which calls this script under the hood).

## Cross-references

- [TECH-07-url-extraction](./TECH-07-url-extraction.md) — URL extraction
  > What it does · When to use · Architecture · Inputs · What `dev-browser eval` returns · Heuristics for token extraction · Colors · Typography · Spacing · Radius · Components · Output structure · Failure modes and recovery · Validation gate · Cross-references
- [TECH-10-tailwind-conversion](./TECH-10-tailwind-conversion.md) — Tailwind-specific extraction (more accurate for TW projects)
  > What it does · When to use · When NOT to use · Inputs · How it works (4-step pipeline) · Step 1 — Loader (loader.ts equivalent) · Step 2 — CSS-parser (css-parser.ts equivalent) · Step 3 — Mapper (mapper.ts equivalent) · Step 4 — Generator (generator.ts equivalent) · Component derivation · Worked example · Limitations · Validation · Cross-references
- [audit-passes](../../amw-design-md-audit/references/audit-passes.md) — Pass 2 (drift) uses this internally
  > Pass 1 — Structural · Pass 2 — Drift · Pass 3 — Accessibility · Pass 4 — Completeness · Pass 5 — Consistency · Output file format · What the auditor does NOT do · Pre-flight checks · Cross-references
- `../../../bin/amw-design-md-from-codebase.py` — the bin script
