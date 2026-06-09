<!--
Direct-port from `amw-design-extract` / designlang (MIT). Algorithm
adapted for the DESIGN.md typography schema; attribution preserved.
-->

# TECH: Typography-role inference — font-size/weight pairs → display / heading / body / caption

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Inputs](#inputs)
- [Algorithm](#algorithm)
  - [Step 1 — Quantize and deduplicate](#step-1--quantize-and-deduplicate)
  - [Step 2 — Sort by visual prominence](#step-2--sort-by-visual-prominence)
  - [Step 3 — Cluster sizes into hierarchy bins](#step-3--cluster-sizes-into-hierarchy-bins)
  - [Step 4 — Assign roles by visual hierarchy heuristics](#step-4--assign-roles-by-visual-hierarchy-heuristics)
  - [Step 5 — Verify with element-role evidence](#step-5--verify-with-element-role-evidence)
- [Pseudo-code](#pseudo-code)
- [Heuristic constants](#heuristic-constants)
- [Worked example](#worked-example)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

Documents how a flat list of extracted `(font-family, font-size, font-weight, line-height)` tuples — with the elements they were observed on — is converted into the **semantic typography map** the Variant 1 DESIGN.md schema expects: `typography.headline-display`, `typography.headline-lg`, `typography.headline-md`, `typography.body-lg`, `typography.body-md`, `typography.body-sm`, `typography.label-md`, `typography.caption`.

The flat tuples capture *every distinct typography style observed on the page*. Without role inference, the DESIGN.md frontmatter ends up listing 30+ ad-hoc entries (`style-48-700-1.1`, `style-36-600-1.15`, …) that no one can author against. The inference pass picks the 6-8 most-meaningful styles and assigns them to the canonical roles.

The algorithm is a direct port from the `amw-design-extract` (designlang, MIT) project's typography classifier, adapted to the Variant 1 DESIGN.md role names.

## When to use

- After URL or codebase extraction has emitted a flat list of `[(font_family, font_size_px, font_weight, line_height, [element_roles], observation_count)]`.
- Before emitting the `typography:` block in DESIGN.md frontmatter.
- Whenever a user asks "what is the heading style of <site>?" and you have the extracted styles but no semantic labels yet.

## When NOT to use

- The site already exposes named CSS custom properties (`--font-size-heading: 32px`) — trust the names; skip inference.
- The site uses fluid typography (`clamp()` everywhere) — the captured size is viewport-dependent; record `warnings: ["fluid typography detected; extracted at viewport width 1440px only"]` and proceed with that viewport's snapshot.
- The site uses a single font size everywhere (rare; mostly old blog templates) — skip inference; emit one body-md style.

## Inputs

```python
TypographyStyle = dict(
  font_family: str,              # "Inter"
  font_size_px: float,           # 48.0
  font_weight: int,              # 700
  line_height: float,            # 1.1 (unitless ratio) or 52.8 (px)
  letter_spacing_em: float,      # -0.02 (negative tracking common on display)
  count: int,                    # 14 — observations of this exact style
  element_roles: list[str],      # ["h1"] — elements observed on
)
```

A site with 12 distinct headline-display variants per breakpoint produces dozens of tuples; the algorithm is robust to this because Step 1 quantizes aggressively.

## Algorithm

### Step 1 — Quantize and deduplicate

Computed-style font sizes vary by sub-pixel amounts (`15.7px` vs `16.2px` from `rem`-based scales × root-font-size rounding). Quantize to the nearest 2px to collapse this noise:

```python
def quantize(px: float) -> int:
    return int(round(px / 2.0) * 2)
```

After quantization, merge tuples that match on `(font_family, quantized_size, weight, line_height_rounded_1_decimal)` — sum their counts, union their element_roles.

A 30-entry palette typically collapses to 8-12 distinct styles after this pass.

### Step 2 — Sort by visual prominence

Compute a `prominence_score` per style:

```text
prominence_score = font_size_px × (font_weight / 400) × area_share
```

The score correlates with how loud the style appears on the page. A 48px / weight 700 / appears 14 times on the hero produces a high score; a 14px / weight 400 / appears 200 times in body text produces a moderate score; a 12px / weight 300 / appears once on a footer disclaimer produces a low score.

### Step 3 — Cluster sizes into hierarchy bins

Use a fixed bin layout, NOT k-means — typography has a known hierarchy:

| Bin | Size range (px) | Role candidates |
|---|---|---|
| `xxl` | > 56 | headline-display |
| `xl` | 36 – 56 | headline-lg, headline-display |
| `lg` | 24 – 36 | headline-md, headline-lg |
| `md` | 18 – 24 | body-lg, headline-md |
| `base` | 14 – 18 | body-md (most common) |
| `sm` | 12 – 14 | body-sm, label-md |
| `xs` | 10 – 12 | caption, label-sm |

Map each quantized size into its bin. A bin can hold multiple styles (`headline-display` and `headline-lg` may both fall into the `xl` bin if the site uses 40px and 48px both).

### Step 4 — Assign roles by visual hierarchy heuristics

Assignment proceeds top-down through the canonical role list, picking the single best candidate from each bin and removing it from the pool.

| Role | Bin preference | Tiebreaker |
|---|---|---|
| `headline-display` | `xxl` → `xl` | highest font_size_px |
| `headline-lg` | `xl` → `lg` | next-highest font_size_px below display |
| `headline-md` | `lg` → `md` | observed on `<h2>` / `<h3>` if available |
| `body-lg` | `md` | observed on `<p>` (intro paragraph) if available |
| `body-md` | `base` | highest count (most-used) |
| `body-sm` | `sm` | observed on `<p>` / `<small>` |
| `label-md` | `sm` → `base` | observed on `<button>` / `<label>` |
| `caption` | `xs` → `sm` | lowest count, observed on `<small>` / `<figcaption>` |

If a role's preferred bin has no candidates, fall back to the secondary bin. If both are empty, the role goes unassigned and the DESIGN.md prose records a warning ("No `caption` style extracted; site does not use sub-12px text").

### Step 5 — Verify with element-role evidence

Element-role observations are the **strongest signal** for any assignment — a style observed on `<h1>` is more likely `headline-display` than `headline-lg` no matter how the size falls. Boost the score of candidates whose element_roles overlap with the expected element list:

| Role | Expected element_roles | Score multiplier when matched |
|---|---|---|
| `headline-display` | `h1` | × 1.3 |
| `headline-lg` | `h1`, `h2` | × 1.2 |
| `headline-md` | `h2`, `h3` | × 1.2 |
| `body-lg` | `p` (in `<main>` or `[role="main"]`) | × 1.1 |
| `body-md` | `p`, `li`, `td` | × 1.0 (baseline; this is the default) |
| `body-sm` | `p`, `small`, `li` | × 1.1 |
| `label-md` | `button`, `label`, `[role="button"]` | × 1.3 |
| `caption` | `small`, `figcaption`, `[role="caption"]` | × 1.3 |

A `48px / 700` style observed on `<h1>` AND on `<button>` (rare but possible — a site that uses giant buttons in the hero) scores high for both `headline-display` and `label-md`. The greedy-max assignment picks the higher-scoring role first; the second-best role then picks a different candidate.

## Pseudo-code

```python
def assign_typography_roles(styles: list[TypographyStyle]) -> dict[str, TypographyAssignment]:
    quantized = quantize_and_dedupe(styles)
    for s in quantized:
        s["prominence_score"] = (
            s["font_size_px"] *
            (s["font_weight"] / 400) *
            max(s.get("area_share", 0.01), 0.01)
        )
        s["bin"] = bin_for_size(s["font_size_px"])

    role_order = [
        "headline-display", "headline-lg", "headline-md",
        "body-lg", "body-md", "body-sm",
        "label-md", "caption",
    ]
    pool = list(quantized)
    assignments = {}

    for role in role_order:
        candidates = [s for s in pool if s["bin"] in ROLE_BIN_PREFERENCE[role]]
        if not candidates:
            assignments[role] = TypographyAssignment(
                style=None, confidence=0.0,
                warning=f"no candidate for {role}",
            )
            continue
        for c in candidates:
            c["role_score"] = role_score(c, role, assignments)
        candidates.sort(key=lambda c: c["role_score"], reverse=True)
        chosen = candidates[0]
        if chosen["role_score"] < CONFIDENCE_FLOOR:
            assignments[role] = TypographyAssignment(
                style=None, confidence=chosen["role_score"],
                warning=f"low confidence ({chosen['role_score']:.2f}) for {role}",
            )
            continue
        assignments[role] = TypographyAssignment(
            font_family=chosen["font_family"],
            font_size_px=chosen["font_size_px"],
            font_weight=chosen["font_weight"],
            line_height=chosen["line_height"],
            confidence=chosen["role_score"],
            usage_count=chosen["count"],
            element_roles=chosen["element_roles"],
        )
        pool.remove(chosen)
    return assignments
```

## Heuristic constants

Empirically tuned on the upstream 60-brand extraction corpus; the ships-with-plugin snapshot of that corpus is `skills/amw-design-md/references/brand-*.md` (see `brand-catalog.md`). Do NOT change without re-running the brand-corpus regression suite.

| Constant | Value | What it controls |
|---|---|---|
| `QUANTIZE_PX_STEP` | `2` | Sub-pixel deduplication granularity |
| `LINE_HEIGHT_QUANTIZE` | `0.1` | Quantize line-height ratios to one decimal |
| `CONFIDENCE_FLOOR` | `0.40` | Below this, leave the role unassigned + warn |
| `ELEMENT_ROLE_BONUS` | `1.2` – `1.3` | Multiplier applied when element_roles match (see Step 5) |
| `MIN_OBSERVATIONS_FOR_BODY` | `3` | A style observed once is unlikely to be `body-md`; minimum count for default body roles |

## Worked example

Linear.app homepage — quantized typography palette:

| Quantized size | Weight | Family | Count | element_roles |
|---|---|---|---|---|
| 96px | 700 | Inter | 1 | h1 |
| 56px | 600 | Inter | 1 | h1 (smaller hero variant) |
| 36px | 600 | Inter | 4 | h2 |
| 24px | 600 | Inter | 6 | h3 |
| 20px | 500 | Inter | 3 | p (intro) |
| 16px | 400 | Inter | 42 | p, li, td |
| 14px | 400 | Inter | 18 | p, small |
| 14px | 500 | Inter | 12 | button, label |
| 12px | 400 | Inter | 5 | small, figcaption |

Role assignment:

1. `headline-display` → `96px / 700` (xxl bin, h1, score=2.21) ✓
2. `headline-lg` → `56px / 600` (xl bin, h1, score=1.98) ✓
3. `headline-md` → `36px / 600` (lg bin, h2, score=1.85) ✓
4. `body-lg` → `20px / 500` (md bin, p, score=1.42) ✓
5. `body-md` → `16px / 400` (base bin, p with count 42, score=1.30) ✓
6. `body-sm` → `14px / 400` (sm bin, p+small, score=1.10) ✓
7. `label-md` → `14px / 500` (sm bin, button, score=1.27) ✓ (element-role × 1.3)
8. `caption` → `12px / 400` (xs bin, small, score=0.91) ✓ (element-role × 1.3)

All 8 roles assigned with confidence ≥ 0.6. The DESIGN.md emitter writes:

```yaml
typography:
  headline-display:
    fontFamily: "Inter"
    fontSize: "96px"
    fontWeight: 700
    lineHeight: 1.05
  headline-lg:
    fontFamily: "Inter"
    fontSize: "56px"
    fontWeight: 600
    lineHeight: 1.1
  ...
```

## Breaks if

- **Site uses fluid typography (`clamp(1rem, 2vw, 1.5rem)`)** — computed-style returns whatever the current viewport produces. The extractor sees a single value (the viewport at extraction time) and the inference works, but the resulting fixed `fontSize: 24px` misrepresents intent. Record `warnings: ["fluid typography detected; extracted at 1440px viewport"]` and recommend a multi-viewport pass via re-extraction.
- **Single font-family across all sizes** (common — Inter / Roboto / system-sans) — pairing by family is impossible because there is nothing to pair against; the algorithm doesn't need family for role inference but the output `fontFamily:` field will be identical across all 8 roles. Note this in prose so the user can choose a display + body split deliberately.
- **Element-role observations are missing** — when the extractor cannot link a style back to its element_role (e.g., styles in pseudo-elements, in `::first-letter`, etc.), the element-role-bonus boost is unavailable and the assignment degrades to size-only ranking. Confidence drops; assignments may misalign (e.g., a large `button` style may get assigned to `headline-display` because it's the largest weight-700 style).
- **More than 8 visually-meaningful styles** — sites with rich typography hierarchies (Medium, NYT, editorial sites) may have 12-15 distinct prominence-score-high styles. The canonical Variant 1 has 8 slots; extra styles are dropped. Add them via `extensions.typography.extra-N` rather than overwriting canonical slots. Record `warnings: ["site uses {N} typography levels; canonical schema captures 8 — extra levels in extensions.typography"]`.
- **Display fonts present but never used on headings** (font loaded but only used decoratively) — the algorithm assigns based on observed usage, not on declared `@font-face` rules. A loaded-but-unused font correctly does not appear in any role; users who want the unused font tracked must add it manually post-extraction.
- **Line-height in mixed units (`1.5` vs `24px`)** — normalize to a unitless ratio before clustering: if line-height is in px, divide by font_size_px. Without normalization, two visually-equivalent styles (`16px / 24px line-height` and `16px / 1.5 line-height`) get treated as different and split counts.

## Cross-references

- [TECH-extractor-color-role-inference](./TECH-extractor-color-role-inference.md) — sibling inference algorithm for the color map
- [TECH-07-url-extraction](./TECH-07-url-extraction.md) — produces the flat typography tuples this algorithm consumes
- [TECH-08-codebase-extraction](./TECH-08-codebase-extraction.md) — same algorithm runs on codebase-extracted styles
- [TECH-03-typography-tokens](./TECH-03-typography-tokens.md) — the role vocabulary this algorithm assigns into
- `../../../bin/amw-design-md-from-url.sh` — bin script that hosts this classifier
- [amw-design-md-extractor-agent](../../../agents/amw-design-md-extractor-agent.md) — the agent that owns this flow
- Upstream reference: `amw-design-extract` skill (designlang, MIT) — algorithm origin
