# Audit procedure — amw-design-drift-audit

## Table of Contents

- [Phase 0 — Parse the token surface](#phase-0-parse-the-token-surface)
- [Phase 1 — Color drift (CIEDE2000 ΔE<3)](#phase-1-color-drift-ciede2000-δe3)
- [Phase 2 — Scale drift (off-step values)](#phase-2-scale-drift-off-step-values)
- [Phase 3 — Magic numbers (single-use tokens)](#phase-3-magic-numbers-single-use-tokens)
- [Phase 4 — Cross-surface conflicts](#phase-4-cross-surface-conflicts)
- [Phase 5 — Emit report](#phase-5-emit-report)

Detailed algorithm for the three drift categories. Read top-to-bottom; each phase depends on the previous.

## Phase 0 — Parse the token surface

Normalize every input into a list of tuples:

```
(token_name: str, category: str, raw_value: str, source_file: str, source_line: int)
```

`category` ∈ {`color`, `spacing`, `radius`, `font-size`, `font-weight`, `shadow`, `z-index`, `other`}.

Surface-specific parsers:

- **Tailwind v3 (`tailwind.config.{js,ts}`)** — execute the config in a Node sandbox (or `tsx --eval`) to resolve `theme.extend.colors`, `theme.extend.spacing`, `theme.extend.borderRadius`, `theme.extend.fontSize`, `theme.extend.fontWeight`, `theme.extend.boxShadow`. Flatten nested objects (`primary: { 500: '#...', 600: '#...' }` → `primary-500`, `primary-600`).
- **Tailwind v4 (`@theme` in CSS)** — regex `@theme\s*\{([^}]+)\}` then split by `;` and parse each `--<name>: <value>;` line.
- **CSS custom properties** — find every `:root` (and `[data-theme=...]`, `.dark`, etc.) block, parse declarations, dedupe by name.
- **tokens.json (W3C)** — recursively walk the JSON; a node is a token iff it has `$value`. The path becomes the token name (`color.brand.primary` → `color-brand-primary`).
- **DESIGN.md** — parse the YAML frontmatter; the `tokens:` block follows the canonical schema (`tokens.color.primary.value`, etc.).

Always preserve `source_file` + `source_line` so the report can cite exact locations.

## Phase 1 — Color drift (CIEDE2000 ΔE<3)

CIEDE2000 is the perceptually uniform color-difference metric. ΔE<1 ≈ imperceptible; ΔE<3 ≈ "very close, only a trained eye notices"; ΔE>5 ≈ obvious.

### Algorithm

1. Filter tokens where `category == 'color'`.
2. For each color, parse to RGB (hex `#rrggbb`, `#rgb`, `rgb()`, `rgba()`, `hsl()`, `hsla()`, named CSS colors). Skip `transparent`, `currentColor`, `inherit`.
3. Convert RGB → sRGB linear → CIE XYZ (D65 illuminant) → CIE LAB.
4. For every unordered pair `(token_a, token_b)`, compute CIEDE2000 ΔE.
5. Build an undirected graph: nodes = tokens, edges = pairs with ΔE<3.0.
6. Find connected components. Any component with ≥2 nodes is a **drift cluster**.
7. Within a cluster, the "canonical" token is the one with the most usage in the codebase (count grep hits across `*.{css,tsx,jsx,ts,js,html,vue,svelte}`). Recommend collapsing other cluster members into it.

### Cluster recommendation logic

- **2 tokens, ΔE<1.0** → "collapse — visually identical".
- **2 tokens, ΔE 1.0–2.0** → "review — likely the same intent".
- **3+ tokens, ΔE all <3.0** → "collapse — palette has drifted across files".
- **2 tokens, ΔE 2.0–3.0** → "review — borderline, ask the designer".

## Phase 2 — Scale drift (off-step values)

### Infer the project's declared scale

For each numeric category (`spacing`, `radius`, `font-size`):

1. Extract all values, normalize to px (`rem` → 16px assumed, `em` → 16px assumed for the audit; flag if the project's root font-size is not 16px).
2. Find the **modal step** — the GCD of values that differ from each other, restricted to "round" candidates (1, 2, 4, 6, 8, 12, 16). Common steps: spacing=4px, radius=2px, font-size=1px or 2px (typography rarely has a clean step; treat font-size as "documented" if it matches a declared type-scale ratio like 1.125 / 1.2 / 1.25 / 1.333 / 1.5).
3. If the modal step covers >80% of values, that's the declared scale. Otherwise the project has no clean scale — report as "scale-inconsistent" without flagging individual values (the whole system needs a redesign, not a single-value fix).

### Flag off-step values

A value `v` is **off-scale** iff `v % step != 0` AND `v` is not on the explicit exception list:

- Borders: `1px`, `0.5px` (hairline), `2px`, `3px`.
- Radius: `9999px` / `9999` / `50%` (pill / circle shorthand).
- Spacing: `0.5` of the step (half-step for tight UI density).
- Font-size: any value derivable from the type-scale ratio.

### Recommendation

For each off-step value, suggest the **nearest aligned value** (round to nearest step). Don't suggest a new step — that's a redesign decision the audit doesn't make.

## Phase 3 — Magic numbers (single-use tokens)

A token is a **magic number** iff its value appears exactly once in the entire codebase (token-definition site does NOT count).

### Algorithm

1. For each token, grep the codebase for the value (literal raw_value AND the token name).
2. Subtract the definition site. Count remaining occurrences.
3. If count == 1 (one usage outside the definition), flag.
4. If count == 0 (never used), separately flag as **dead token** (orthogonal finding; usually a dead-code cleanup, not a drift issue).

### Recommendation

- **Promote** — if the single usage is semantically meaningful (e.g. a specific component's shadow), rename the token to that semantic name.
- **Eliminate** — if the single usage is incidental (a one-off magic value), inline back to a parent scale token (e.g. replace `--space-7px` with the closest aligned value).

The audit MUST NOT decide between promote and eliminate automatically; it presents both options for human judgment.

## Phase 4 — Cross-surface conflicts

If the codebase has MORE THAN ONE token surface (e.g. Tailwind config AND a tokens.json), find tokens with the same semantic name but different values across surfaces.

Match by normalized name (lowercase, strip prefixes, collapse separators):
- `--color-primary` ↔ `colors.primary` ↔ `tokens.color.primary` ↔ `primary` (in a DESIGN.md `tokens:` block).

Report any value mismatch as a **cross-surface conflict** with HIGH severity — these are silent bugs waiting to manifest in production (dev sees one color in Storybook, prod renders another).

## Phase 5 — Emit report

The report path is provided by the orchestrator; default:
`$MAIN_ROOT/reports/design-drift/<YYYYMMDD_HHMMSS±HHMM>-drift-audit.md`

Section order:

1. **Header** — input surface(s) parsed, total tokens, audit timestamp.
2. **Summary verdict** — CLEAN / LOW / MEDIUM / HIGH.
3. **Color drift** — one table per cluster.
4. **Scale drift** — one table per off-scale value, grouped by category.
5. **Magic numbers** — one table per single-use token, with promote-vs-eliminate recommendation.
6. **Dead tokens** — separate table for zero-use tokens.
7. **Cross-surface conflicts** (if applicable) — one table per conflicting token name.
8. **Next steps** — human-actionable bullets ordered by impact (cross-surface conflicts first, then color clusters, then scale, then magic numbers).
9. **Appendix** — full parsed token list (for the LLM's next pass to re-audit without re-parsing).
