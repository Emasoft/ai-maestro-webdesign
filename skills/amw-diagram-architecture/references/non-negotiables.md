# Non-negotiables — amw-diagram-architecture

## Table of Contents

- [Hard limits](#hard-limits)
- [Model & output](#model--output)
- [Palette coherence](#palette-coherence)
- [Validation](#validation)

Hard rules for every emission from this skill. Failure on any item triggers a remediation loop or regeneration; do not silently work around these.

## Hard limits

- **Never exceed the layer/node budgets.** 3–5 layers, 6–12 nodes. Visual quality over completeness — merge, drop, or simplify minor components rather than overflow a layer or crowd the canvas.
- **Layers are the spine.** Every diagram is top-down, strictly layered; nodes connect within their layer's slot first, then across layers.
- **Edges signal flow, not exhaustion.** Maximum edges = `floor(nodeCount × 0.8)`. Draw only primary data or control flow; drop the rest.

## Model & output

- **Model freshness.** Use a capable modern Claude Sonnet or Opus (e.g. `claude-sonnet-4-6` or newer). NEVER pin the legacy dated Sonnet-4 snapshot from the 2025-05 series — that snapshot is outdated and scheduled for retirement. Update the model string in [prompts](./prompts.md) whenever Anthropic ships a newer production model.
- **No prose wrapper by default.** The output IS the diagram. Add narration only when the caller explicitly asks for it.

## Palette coherence

Five non-adjacent-hue anchors form the canonical identity of this diagram family — each layer gets a distinct hue band so layers remain distinguishable at a glance. Use the oklch values as the primary spec; hex fallbacks are provided for legacy tooling only:

| Layer | Role | oklch | hex | Name |
|---|---|---|---|---|
| 1 | frontend | `oklch(30% 0.04 260)` | `#3B4252` | slate-ink |
| 2 | gateway / orchestration | `oklch(62% 0.16 45)` | `#C87341` | rust-accent |
| 3 | logic / services / agents | `oklch(65% 0.13 190)` | `#4FA9A3` | teal-accent |
| 4 | tools / integrations | `oklch(78% 0.14 85)` | `#D9A441` | amber-accent |
| 5 | data / storage | `oklch(60% 0.09 140)` | `#6E9B6A` | sage-accent |

The previous indigo-purple defaults (`#6366F1` / `#8B5CF6`) were retired because they sit in the "purple-blue gradient" band flagged by [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) item #1.

Substituting tokens from [color-system](../../amw-design-principles/color-system.md) is permitted only when the caller has supplied an explicit design-token override; silent recoloring breaks cross-diagram recognisability.

## Validation

- **Validation is mandatory, not advisory.** Every Stage 1 and Stage 2 check must pass before return. Surfacing an error to the caller is the last resort — apply the listed fixes first, regenerate if the triggers fire.
