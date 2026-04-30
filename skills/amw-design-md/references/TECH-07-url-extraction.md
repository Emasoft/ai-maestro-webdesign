---
name: TECH-07-url-extraction
category: extraction
source: design-md-creator-skill, web-to-design-md, clone-design, insane-design (READMEs and SKILL.md sections)
also-in: TECH-09-multipage-extraction.md, TECH-08-codebase-extraction.md
status: stable
---

# TECH: URL → DESIGN.md extraction (delegating to dev-browser)

## What it does

Documents how to extract a Variant 1 DESIGN.md from a live URL. The plugin's URL-extraction path goes through `amw-dev-browser` (the only browser-automation primitive in this plugin). The bin script is `bin/amw-design-md-from-url.sh`. The agent that owns this flow is `amw-design-md-extractor-agent`.

## When to use

- User says: "extract DESIGN.md from <URL>"
- User says: "make a DESIGN.md from this site I like"
- Brand-researcher delegating: when the user provides a competitor URL and wants the result as a structured DESIGN.md (rather than free-form notes)

Do NOT trigger on:
- "extract design tokens from <URL>" without DESIGN.md keyword → routes to `amw-design-extract`
- "clone this site" → routes to wireframe-builder (which may consume an extracted DESIGN.md as one of its inputs)

## Architecture

```
                ┌──────────────────────────────┐
   URL ─────►   │  amw-design-md-extractor-    │
                │  agent (Tier 3)              │
                └──────────────┬───────────────┘
                               │
                               ▼
                  bin/amw-design-md-from-url.sh
                               │
                               ▼
              bin/amw-dev-browser-wrapper.sh
                               │
                               ▼
              dev-browser eval <URL>  (DOM + computed styles)
                               │
                               ▼
              JSON snapshot of:
                - rendered HTML structure
                - computed styles (color, font, spacing on key landmarks)
                - CSS custom properties from :root and .dark
                - stylesheet rules (selectors + declarations)
                - meta tags, og: data, brand name
                               │
                               ▼
              bin/amw-design-md-from-url.sh post-processor:
                - cluster colors (k-means; top 8-12)
                - extract font stacks from used computed-styles
                - infer spacing scale from common margin/padding values
                - infer radius scale from rounded values
                - emit Variant 1 DESIGN.md frontmatter + draft prose
                               │
                               ▼
                       Draft DESIGN.md
                               │
                               ▼
              bin/amw-design-md-lint.sh (validate)
              bin/amw-design-md-contrast.py (a11y check)
                               │
                               ▼
                  Final DESIGN.md (Variant 1)
```

## Inputs

`bin/amw-design-md-from-url.sh <URL> [-o <out-path>] [-n <name>]`

- `<URL>`: the page to extract from. Must be reachable via the user's network.
- `-o <out-path>`: output file path. Default: `./DESIGN.md`.
- `-n <name>`: design system name. Default: derived from `<title>` or domain name.

## What `dev-browser eval` returns

The wrapper invokes `dev-browser eval <URL>` with a JS expression that captures:

1. **DOM landmarks** — `header`, `main`, `footer`, navigation, the largest `<h1>`, the first call-to-action button, body text samples.
2. **Computed styles for landmarks** — `color`, `background-color`, `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing`, `border-radius`, `padding`, `margin` for each.
3. **CSS custom properties** — every `--X: Y` from `:root`, `.dark`, `[data-theme]`.
4. **Stylesheet rules** — for each external stylesheet, the resolved selectors and declarations.
5. **Color usage frequency** — every distinct color value seen in computed styles, with hit count.
6. **Brand metadata** — `<title>`, `og:title`, `og:description`, brand name from logo `alt`, primary CTA text.

This is a single JSON blob (typically 50-500 KB).

## Heuristics for token extraction

### Colors

1. Cluster all observed colors using k-means (k=8 typically) in CIELab space.
2. The most-used cluster centroid → `colors.primary` (typically the dark text color OR the brand accent, decided by usage on landmarks).
3. The least-used cluster centroid that appears on a single CTA → `colors.tertiary` (likely brand accent if not detected as primary).
4. The page-background cluster → `colors.surface` or `colors.neutral`.
5. Pure white / off-white → `colors.surface` if not already taken.

The heuristic is imperfect; the post-processor flags ambiguous colors in the prose (e.g., "Primary detected as #1A1C1E (used in 47% of computed styles); the alternative was #B8422E (used as accent on 3 elements)").

### Typography

1. Group font-family values from computed styles. The font-family used on most body text → body-md primary.
2. The font-family used on the largest `<h1>` → display.
3. Other observed sizes (px values from computed-style font-size) populate the typography levels.
4. Quantize sizes to a 2-px grid (round to nearest 2) to avoid `15.7px` / `16.2px` noise.

### Spacing

1. Collect all margin/padding numeric values across landmarks.
2. Sort, dedupe, find common factors (typically 4 or 8). The factor → spacing base unit.
3. Multiples of the base appearing 3+ times → spacing scale entries.

### Radius

1. Collect all `border-radius` values.
2. Cluster (typically 3-6 distinct values).
3. Map smallest → `rounded.sm`, etc.

### Components

The component extraction is harder; the bin script tries to identify a primary CTA button and an input by computed style of the most prominent matching elements, then emits `button-primary`, `input-default`, and `card` (if visible) entries.

## Output structure

The bin script emits a draft DESIGN.md with:

- Variant 1 YAML frontmatter (name, version, colors, typography, rounded, spacing, components).
- `## Overview` section with auto-generated prose: "This design system was extracted from {url} on {timestamp}. The brand projects {tone}; uses {N} primary color(s); typography is {family-summary}; layout is {grid-summary}." (This prose is starting copy; the user / agent edits it.)
- `## Colors`, `## Typography`, etc., with the extracted values + brief auto-generated philosophy notes.
- `## Do's and Don'ts` containing 5-7 default rules (color discipline, contrast, font discipline) — placeholder rules the user customizes.

The auto-generated prose is intentionally generic; the **user is expected to refine it** before treating the file as canonical. The plugin's author agent flags this in `warnings`.

## Failure modes and recovery

| Failure | Cause | Recovery |
|---|---|---|
| `dev-browser` cannot reach URL | Network, paywall, login required | Return `failed` with `blocking_issues=["URL unreachable: <error>"]`. Suggest user provide screenshots or a local HTML snapshot. |
| Page is JS-heavy SPA, content takes time | dev-browser eval runs before render complete | Add `--wait-for-selector main` or `--wait-ms 2000`. |
| Too many distinct colors (10K+) | Page uses a CSS framework with full palette declared | Filter to colors actually used in computed styles, not just declared. |
| All-image landing page | Few text elements | Extract from images via OCR is OUT OF SCOPE. Return `partial` with `warnings=["Site is image-heavy; extracted only typography from <h1> and body samples"]`. |
| Login wall | The user's path to that content is auth-gated | Out of scope for this bin script. See `TECH-09-multipage-extraction.md` for the multi-page session flow. |

## Validation gate

Every URL-extracted DESIGN.md passes the standard validation chain before delivery:

```bash
bash bin/amw-design-md-lint.sh DESIGN.md
python3 bin/amw-design-md-validate.py DESIGN.md
python3 bin/amw-design-md-contrast.py DESIGN.md
```

A draft that fails contrast (extracted colors fail WCAG-AA) is marked `partial` with the contrast failures in `warnings`. The user adjusts.

## Cross-references

- `./TECH-08-codebase-extraction.md` — extracting from a local codebase instead of URL
- `./TECH-09-multipage-extraction.md` — multi-page sessions including login
- `./TECH-10-tailwind-conversion.md` — extracting from tailwind config (different path)
- `<plugin-root>/bin/amw-design-md-from-url.sh` — the bin script
- `<plugin-root>/bin/amw-dev-browser-wrapper.sh` — browser primitive used internally
- `../../amw-dev-browser/SKILL.md` — dev-browser skill spec
- `../../../agents/amw-design-md-extractor-agent.md` — the agent
