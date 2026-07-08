# TECH-91: Shadow + elevation extraction from a live URL

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Architecture](#architecture)
- [What dev-browser captures](#what-dev-browser-captures)
- [Elevation classification](#elevation-classification)
- [Normalization rules](#normalization-rules)
- [Output schema](#output-schema)
- [Worked example](#worked-example)
- [Edge cases](#edge-cases)
- [Failure modes](#failure-modes)
- [Cross-references](#cross-references)

## What it does

Documents how `amw-design-md-extractor-agent` reads computed `box-shadow` values from a live URL, clusters them by **elevation depth**, and emits a standardized `shadows.depth-1..depth-5` block in the DESIGN.md frontmatter. Variant 1 DESIGN.md does not include shadows in its core schema, so this technique writes to the **extension namespace** `extensions.shadows` per [extension-sections-10-14](../../amw-design-md-spec/references/extension-sections-10-14.md) — the elevation system becomes an optional extension token group.

The base flow (DOM walk + computed-style sampling) is shared with [TECH-07-url-extraction](TECH-07-url-extraction.md); this TECH focuses on the **classification + normalization** layer specific to shadows.

## When to use

- User says: "extract DESIGN.md from <URL> including shadows / elevations"
- User says: "I need the elevation system from this Material-flavored site"
- Brand-researcher: extracting a design system where shadows are a meaningful brand signal (Stripe, Linear, Vercel-style sites)

## When NOT to use

- User explicitly only wants Variant 1 core tokens (colors/type/space/radius) → skip; do not pollute frontmatter with unused extension namespace
- Site uses no shadows (flat design) → return empty `shadows: {}` block + a prose note; do not invent shadows
- Site uses CSS `filter: drop-shadow()` instead of `box-shadow` → out of scope for v1; record in `warnings`

## Architecture

```
        URL ─────► dev-browser eval ────► JSON snapshot
                                          (computed styles)
                          │
                          ▼
        For each element with non-`none` box-shadow:
          {selector, shadow_value, element_role, area_px²}
                          │
                          ▼
        Parse shadow_value into shadow_layers:
          { offsetX, offsetY, blurRadius, spreadRadius, color, inset }
                          │
                          ▼
        Compute elevation_score per shadow:
          blurRadius + (offsetY × 1.5) + (spreadRadius × 0.5)
                          │
                          ▼
        Cluster by elevation_score (k-means, k=5 default):
          depth-1 (lowest) → depth-5 (highest)
                          │
                          ▼
        Normalize each cluster centroid to canonical form
                          │
                          ▼
        Emit extensions.shadows.depth-N entries
```

## What dev-browser captures

The extraction extends the standard JSON snapshot with a `shadows` array:

```js
// dev-browser eval injects:
function captureShadows() {
  const all = document.querySelectorAll('*');
  const shadows = [];
  for (const el of all) {
    const s = getComputedStyle(el).boxShadow;
    if (s && s !== 'none') {
      const rect = el.getBoundingClientRect();
      shadows.push({
        selector: el.tagName + (el.className ? '.' + el.className.split(' ')[0] : ''),
        raw: s,
        area: rect.width * rect.height,
        role: el.matches('button, [role="button"]') ? 'button'
            : el.matches('[role="dialog"], .modal') ? 'modal'
            : el.matches('article, .card, [class*="card"]') ? 'card'
            : 'other',
      });
    }
  }
  return shadows;
}
```

Multi-layer shadows (`0 1px 2px rgba(0,0,0,0.05), 0 2px 8px rgba(0,0,0,0.1)`) are kept as a single entry with the layers preserved — they are common in modern systems and dropping the second layer loses the realistic look.

## Elevation classification

After capture, the post-processor in `bin/amw-design-md-from-url.sh` parses each `raw` value and computes an `elevation_score`:

```python
def elevation_score(shadow_layers):
    # Sum a simple visual-prominence score across all layers.
    score = 0
    for layer in shadow_layers:
        if layer.inset:
            continue  # inset shadows are not elevation; treated separately
        score += layer.blurRadius
        score += abs(layer.offsetY) * 1.5     # downward offset = perceived height
        score += layer.spreadRadius * 0.5
    return score
```

The score correlates with perceived depth: small + tight blur = low elevation (a button hover); large + diffuse blur = high elevation (a modal). The classifier runs k-means (k=5) on the scores; cluster centroids define `depth-1` through `depth-5`.

If the page uses fewer than 3 distinct shadow patterns, the classifier produces fewer depth levels (e.g., `depth-1`, `depth-2`, `depth-3` only). Do NOT pad with synthetic entries — empty depth levels signal a flat / minimal-shadow design.

## Normalization rules

The extracted raw shadow value (`rgba(0, 0, 0, 0.0784314) 0px 4px 6px -1px`) is rewritten to canonical form:

1. **Color first**, in `rgba(r, g, b, alpha)` with 3-decimal alpha precision.
2. **Offsets in `0px` form** even when the value is 0 (avoids ambiguity).
3. **Spread radius omitted when 0** (CSS allows; keeps the value compact).
4. **No `inset` keyword in elevation tokens** — inset shadows belong to a separate `extensions.shadows.inset.*` namespace.

The normalized form for `depth-2` example:

```yaml
extensions:
  shadows:
    depth-2:
      value: "0px 2px 4px 0px rgba(0, 0, 0, 0.080), 0px 4px 8px 0px rgba(0, 0, 0, 0.060)"
      usage: "card resting state; subtle hover lift"
```

## Output schema

The extension block in DESIGN.md frontmatter:

```yaml
extensions:
  shadows:
    depth-1:
      value: "0px 1px 2px 0px rgba(0, 0, 0, 0.050)"
      usage: "button resting; input field"
    depth-2:
      value: "0px 2px 4px 0px rgba(0, 0, 0, 0.080), 0px 4px 8px 0px rgba(0, 0, 0, 0.060)"
      usage: "card resting; dropdown menu"
    depth-3:
      value: "0px 4px 8px 0px rgba(0, 0, 0, 0.100), 0px 8px 16px 0px rgba(0, 0, 0, 0.080)"
      usage: "card hover; popover"
    depth-4:
      value: "0px 8px 16px 0px rgba(0, 0, 0, 0.120), 0px 16px 32px 0px rgba(0, 0, 0, 0.100)"
      usage: "modal; floating action"
    depth-5:
      value: "0px 16px 32px 0px rgba(0, 0, 0, 0.150), 0px 32px 64px 0px rgba(0, 0, 0, 0.120)"
      usage: "command palette; full-screen sheet"
```

The `usage:` field is auto-generated from the `role` metadata captured by dev-browser (button/card/modal/popover) — it is starting copy the user refines.

## Worked example

Input: Linear.app homepage.

dev-browser captures 17 elements with non-`none` box-shadow:
- 8 buttons with `0 1px 2px rgba(0,0,0,0.05)`
- 6 cards with `0 2px 4px rgba(0,0,0,0.08), 0 4px 8px rgba(0,0,0,0.06)`
- 2 popovers with `0 4px 16px rgba(0,0,0,0.12)`
- 1 modal with `0 16px 48px rgba(0,0,0,0.16)`

Classifier emits 4 depth levels (1, 2, 3, 4); `depth-5` is empty (no full-screen sheet on the landing page). The output extension block lists only the 4 populated levels; the prose section notes "depth-5 not present on this page".

## Edge cases

- **Inset shadows on inputs** (`inset 0 1px 2px ...`) — captured into `extensions.shadows.inset.input` namespace, not in `depth-N`.
- **`filter: drop-shadow()`** — captured separately; recorded in `warnings` because the extractor cannot reliably normalize them yet.
- **Tailwind shadow utilities** (`shadow-sm`, `shadow-md`, etc.) — the computed-style approach catches these regardless; no special handling needed.
- **Multi-color shadows** (`0 4px 8px hsl(220 30% 10% / 0.1)`) — the parser converts to `rgba()` form for normalization.
- **Color-mixed shadows** (`color-mix(...)` in modern browsers) — fall back to the computed RGBA value the browser produces.

## Failure modes

| Failure | Cause | Recovery |
|---|---|---|
| Page has no shadows at all | Flat-design site | Emit empty `extensions.shadows: {}` + prose note; do NOT invent shadows |
| Shadows use exotic units (`em`, `rem`) | Unusual but valid CSS | The browser converts to `px` in computed styles; capture should still work |
| Cluster centroids overlap (very narrow elevation range) | Subtle design system | Reduce k; emit only the populated levels |
| User wants 7+ depth levels | Material Design 3 (24 levels) | Override with `--shadow-levels N`; default k=5 |
| Multi-layer shadow with conflicting layer scores | Layers added for legibility, not depth | Use total score across layers (already does this); flag if user-suspect |

## Cross-references

- [TECH-07-url-extraction](./TECH-07-url-extraction.md) — base URL extraction flow
  > What it does · When to use · Architecture · Inputs · What `dev-browser eval` returns · Heuristics for token extraction · Colors · Typography · Spacing · Radius · Components · Output structure · Failure modes and recovery · Validation gate · Cross-references
- [TECH-86-multi-page-extract](./TECH-86-multi-page-extract.md) — when shadows differ across pages, multi-page merge applies
- [TECH-94-animation-extract](./TECH-94-animation-extract.md) — shadows often participate in hover transitions; extract together
- [extension-sections-10-14](../../amw-design-md-spec/references/extension-sections-10-14.md) — where extension namespaces live in Variant 1 DESIGN.md
- `../../../bin/amw-design-md-from-url.sh` — bin script that hosts this classifier
- `../../../bin/amw-dev-browser-wrapper.sh` — browser primitive used internally
- [amw-design-md-extractor-agent](../../../agents/amw-design-md-extractor-agent.md) — the agent that owns this flow
