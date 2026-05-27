<!--
Direct-port from `amw-design-extract` / designlang (MIT). Algorithm
adapted for the DESIGN.md schema; attribution preserved.
-->

# TECH: Color-role inference — flat palette → primary / secondary / accent / surface / background

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Inputs](#inputs)
- [Algorithm](#algorithm)
  - [Step 1 — Normalize and count](#step-1--normalize-and-count)
  - [Step 2 — Compute per-color features](#step-2--compute-per-color-features)
  - [Step 3 — Score each role](#step-3--score-each-role)
  - [Step 4 — Assign by greedy-max with ties broken by usage](#step-4--assign-by-greedy-max-with-ties-broken-by-usage)
- [Pseudo-code](#pseudo-code)
- [Heuristic constants](#heuristic-constants)
- [Worked example](#worked-example)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

Documents how a flat extracted palette (from `bin/amw-design-md-from-url.sh` or `bin/amw-design-md-from-codebase.py`) is converted into the **semantic role map** the Variant 1 DESIGN.md schema expects: `colors.primary`, `colors.secondary`, `colors.tertiary`, `colors.surface`, `colors.background`, `colors.on-surface`, `colors.border-subtle`, `colors.accent`.

The flat palette captures *every distinct hex value observed*. The role-inference pass picks which of those values is the brand-defining hue (`primary`), which is the dominant page surface (`background`), which is the small-area accent (`tertiary` or `accent`), etc. Without this pass the DESIGN.md frontmatter is just a hex dump — useful for token replacement but not for token-based authoring.

The inference algorithm is a direct port from the `amw-design-extract` (designlang, MIT) project's role-classifier. The DESIGN.md emitter writes the assigned role names into the `colors:` map and records the original computed-style observation counts in the prose section.

## When to use

- After URL or codebase extraction has emitted a flat list of `[(hex, observation_count, [element_roles])]`.
- Before emitting the `colors:` block in DESIGN.md frontmatter.
- Whenever a user asks "what is the primary color of <site>?" and you have the extracted palette but no semantic labels yet.

## When NOT to use

- The site already exposes named CSS custom properties (`--color-primary: #...`) — trust those names; skip role inference.
- The site uses Material Design tonal palettes (palette of 13 stops per role) — defer to `TECH-tonal-palette-extract.md`; this skill targets flat palettes.
- Only one color was extracted — assign it to `primary` directly; the algorithm has nothing to compare against.

## Inputs

The inference takes a list of records:

```python
PaletteEntry = dict(
  hex: str,                    # "#1a1c1e"
  count: int,                  # 47 — observation count across landmarks
  roles: list[str],            # ["body", "h1"]  — element-roles observed on
  area_px2: float,             # sum of bounding-box areas of carrying elements
)
```

The bin script populates `count`, `roles`, and `area_px2` while walking the dev-browser snapshot. A color seen only on a single `<button>` has `count=1`, `roles=["button"]`, `area_px2 ≈ small`. A color used as the body background has `count` in the thousands and `area_px2` near viewport size.

## Algorithm

### Step 1 — Normalize and count

Drop entries with `count == 0` (declared CSS variables never referenced). Re-sort the palette by `area_px2` descending — large-area colors are background candidates; small-area colors are accent candidates.

### Step 2 — Compute per-color features

For every entry, compute three derived features:

| Feature | Formula | Range |
|---|---|---|
| `luminance` | WCAG relative luminance from sRGB | `0.0` (pure black) → `1.0` (pure white) |
| `chroma` | OKLCH chroma (or HSL saturation as a fallback) | `0.0` (gray) → `~0.4` (saturated) |
| `area_share` | `area_px2 / sum(area_px2)` across the palette | `0.0` → `1.0` |

These three numbers decide every role assignment. Hue is intentionally NOT used as a feature — most pages have a single brand hue and using hue would just confirm what `chroma + count` already told us.

### Step 3 — Score each role

Each role has a scoring function over `(luminance, chroma, area_share, count)`. The role is assigned to the color with the highest score; once assigned, the color is removed from the candidate pool. Scores are intentionally fuzzy — the algorithm uses ranges, not thresholds.

| Role | High score when | Why |
|---|---|---|
| `background` | `area_share > 0.5`, `chroma < 0.04` | Largest near-grayscale area = the canvas |
| `surface` | second-largest near-grayscale area, `\|luminance - background.luminance\| > 0.05` | Cards / panels sit a step away from background |
| `on-surface` | `luminance` opposite to `background` (delta > 0.7), `chroma < 0.05` | Body text contrasts hard with background |
| `border-subtle` | `chroma < 0.04`, `\|luminance - surface.luminance\| < 0.2`, `area_share < 0.05` | Faint gray, small area, low contrast |
| `primary` | `chroma > 0.10`, observed on roles `["button", "link", "h1"]`, `count` high among saturated colors | Most-used brand-colored color |
| `secondary` | `chroma > 0.08`, NOT the primary, `count` second-highest among saturated colors | Supporting brand color |
| `tertiary` / `accent` | `chroma > 0.12`, `count` low, observed on a single small element (badge, link, status pill) | Reserved for the loudest splash |

The scoring functions return floats in `[0, 1]`; tied scores break by raw `count`.

### Step 4 — Assign by greedy-max with ties broken by usage

Iterate roles in fixed order: `background → surface → on-surface → border-subtle → primary → secondary → tertiary`. For each role, pick the candidate with the highest score; remove from pool; record the score for the prose section ("`primary` assigned at confidence 0.78 — usage on 47 elements, observed on `<a>`, `<button>`, `<h1>`").

If no candidate scores above `0.5` for a role, leave the role unassigned and add a warning to the DESIGN.md prose ("No `surface` color was extracted with confidence; review live site for card backgrounds").

## Pseudo-code

```python
def assign_color_roles(palette: list[PaletteEntry]) -> dict[str, ColorAssignment]:
    palette = [p for p in palette if p["count"] > 0]
    total_area = sum(p["area_px2"] for p in palette) or 1.0
    for p in palette:
        p["luminance"] = wcag_luminance(p["hex"])
        p["chroma"] = oklch_chroma(p["hex"])
        p["area_share"] = p["area_px2"] / total_area

    assignments: dict[str, ColorAssignment] = {}
    pool = list(palette)
    role_order = [
        "background", "surface", "on-surface", "border-subtle",
        "primary", "secondary", "tertiary",
    ]

    for role in role_order:
        scorer = ROLE_SCORERS[role]
        scored = [(p, scorer(p, assignments)) for p in pool]
        scored = [(p, s) for p, s in scored if s >= 0.5]
        if not scored:
            assignments[role] = ColorAssignment(hex=None, confidence=0.0,
                                                warning=f"no candidate for {role}")
            continue
        scored.sort(key=lambda x: (x[1], x[0]["count"]), reverse=True)
        chosen, conf = scored[0]
        assignments[role] = ColorAssignment(
            hex=chosen["hex"], confidence=conf,
            usage_count=chosen["count"], element_roles=chosen["roles"],
        )
        pool.remove(chosen)
    return assignments
```

The `ROLE_SCORERS` dict maps each role to a small lambda over `(palette_entry, prior_assignments)`. The `background` scorer is the only one that does NOT consult `prior_assignments`; every other scorer subtracts a penalty if the candidate is too close (luminance / chroma) to an already-assigned role, preventing two roles from picking near-duplicate colors.

## Heuristic constants

Empirically tuned on the 60-brand corpus in `skills/amw-design-principles/brand-library/`. Do NOT change these without re-running the brand-corpus regression suite.

| Constant | Value | What it controls |
|---|---|---|
| `MIN_AREA_FOR_BACKGROUND` | `0.50` | Color must cover > 50% of total area to be `background` |
| `MIN_CHROMA_FOR_BRAND` | `0.10` | Color must be saturated to be a primary/secondary candidate |
| `MAX_CHROMA_FOR_NEUTRAL` | `0.04` | Color must be near-gray to be background/surface/border |
| `MIN_LUMINANCE_DELTA_FOR_TEXT` | `0.70` | `on-surface` must be visually opposite the background |
| `CONFIDENCE_FLOOR` | `0.50` | Below this, leave the role unassigned + warn |
| `TIEBREAKER_USAGE_BONUS` | `0.10` | Per-decile usage boost when scores within `0.05` of each other |

## Worked example

Linear.app homepage — flat extracted palette:

| Hex | count | roles | area_px2 |
|---|---|---|---|
| `#08090a` | 312 | body, html | 9.2 M |
| `#ffffff` | 287 | h1, h2, p, button | 3.1 M |
| `#1a1d23` | 64 | card, nav | 0.8 M |
| `#5e6ad2` | 18 | button-primary, link, h1-accent | 0.04 M |
| `#9b9fac` | 41 | small, footer, caption | 0.2 M |
| `#26282d` | 9 | border, divider | 0.01 M |

Role assignment:

1. `background` → `#08090a` (area_share=0.69, chroma=0.01, confidence=0.92)
2. `surface` → `#1a1d23` (area_share=0.06, chroma=0.02, |Δlum|=0.08, confidence=0.81)
3. `on-surface` → `#ffffff` (Δlum from background = 0.96, chroma=0.0, confidence=0.95)
4. `border-subtle` → `#26282d` (chroma=0.02, |Δlum from surface|=0.04, area_share=0.001, confidence=0.79)
5. `primary` → `#5e6ad2` (chroma=0.18, observed on button + link + h1, count=18, confidence=0.84)
6. `secondary` → unassigned (no second saturated color); warning recorded
7. `tertiary` → unassigned; warning recorded

The DESIGN.md emitter writes the assigned 5 roles and the prose includes "Secondary and tertiary not extracted with confidence — Linear uses a single chromatic accent. Add manually if your design extends the palette."

## Breaks if

- **Hex normalization is missing** — `#fff` and `#ffffff` are treated as different colors and split the count, dropping both below `MIN_CHROMA_FOR_BRAND` candidacy. The bin script must normalize 3-digit to 6-digit BEFORE building the palette.
- **`area_px2` is not captured** — without bounding-box area the `background` / `surface` distinction collapses. Fall back to `count` only, but mark all assignments with `confidence ≤ 0.6`.
- **The site is dark-mode-active during extraction but the user wants the light palette** — the extracted luminance polarity flips. See `TECH-extractor-dark-mode-pair-detection.md` for the two-pass strategy.
- **Multi-brand pages** (e.g., `/showcase` listing 12 partners with 12 different logos) — chroma-based scoring picks an arbitrary partner color as `primary`. Restrict extraction to landmark elements (`header`, `main`, `footer`) only, not to embedded showcase cards.
- **CSS variables declared but never referenced** (`--color-emergency: #ff0000` defined but no element uses it) — Step 1 filters these out via `count == 0`. If the bin script counts declared vars as observations the algorithm misfires; declared-only colors must not enter the palette at all.

## Cross-references

- [TECH-07-url-extraction](./TECH-07-url-extraction.md) — produces the flat palette this algorithm consumes
- [TECH-08-codebase-extraction](./TECH-08-codebase-extraction.md) — same algorithm runs on codebase-extracted palettes
- [TECH-02-color-tokens](./TECH-02-color-tokens.md) — the role vocabulary this algorithm assigns into
- [TECH-extractor-typography-role-inference](./TECH-extractor-typography-role-inference.md) — sibling inference for the typography map
- [TECH-extractor-dark-mode-pair-detection](./TECH-extractor-dark-mode-pair-detection.md) — companion algorithm for dual-palette sites
- `../../../bin/amw-design-md-from-url.sh` — bin script that hosts this classifier
- [amw-design-md-extractor-agent](../../../agents/amw-design-md-extractor-agent.md) — the agent that owns this flow
- Upstream reference: `amw-design-extract` skill (designlang, MIT) — algorithm origin
