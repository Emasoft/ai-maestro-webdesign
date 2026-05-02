---
name: TECH-layer-palette-5-colors
category: architecture-layer
source: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/prompts.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/formats.md
---

# TECH-layer-palette-5-colors

## What it does

Assigns one of **five fixed layer colours** to each layer of a layered
architecture diagram, in canonical order from top (user-facing) to bottom
(data). The colours are meaning-encoded: indigo = user-facing, violet =
gateway, cyan = logic, emerald = tools, amber = data.

## When to use

- **Every layered architecture diagram.** Always.
- **Mermaid's `classDef`** and **SVG's layer band + accent bar + node top
  bar** all reference the same 5-colour palette.
- **Do not substitute** other colours unless the user has explicitly run
  a brand-onboarding flow analogous to the editorial one — default
  architecture stays on this canonical palette.

## How it works

Canonical mapping from layer semantics to hex:

| Layer `order` | Semantics | Hex | Name |
|---|---|---|---|
| 0 | User-facing / frontend | `#6366F1` | Indigo |
| 1 | Gateway / orchestration / routing | `#8B5CF6` | Violet |
| 2 | Logic / services / agents | `#06B6D4` | Cyan |
| 3 | Tools / integrations | `#10B981` | Emerald |
| 4 | Data / storage | `#F59E0B` | Amber |

If a diagram has only 3 or 4 layers, pick the subset that best matches
the semantics — skip layer 3 if there's no tooling layer, skip layer 0
if the diagram is backend-only, etc.

## Minimal example

3-layer backend-focused diagram (skipping the user-facing and tools
layers):

```json
{
  "layers": [
    { "id": "gateway",  "color": "#8B5CF6", "order": 0 },
    { "id": "services", "color": "#06B6D4", "order": 1 },
    { "id": "storage",  "color": "#F59E0B", "order": 2 }
  ]
}
```

Mermaid classDef block derived from this palette:

```
classDef layer0 fill:#8B5CF6,color:#fff,stroke:#7C3AED
classDef layer1 fill:#06B6D4,color:#fff,stroke:#0891B2
classDef layer2 fill:#F59E0B,color:#fff,stroke:#D97706
```

Note: the `classDef` layer numbers are re-indexed to 0, 1, 2 once layers
are re-ordered. The hex values track the semantic layer, not the
`classDef` index.

## Gotchas

- **Use in order, not arbitrarily.** If the diagram has a user-facing
  layer AND a services layer, use indigo for frontend and cyan for
  services — don't swap because you like cyan better.
- **The `classDef` uses `color:#fff`** — white text on every coloured
  layer. Keep that default; overriding it silently fails WCAG on cyan
  and amber.
- **SVG stroke is the darker shade of each colour** (see `classDef`
  stroke values). Use the stroke only if the layer band has a visible
  border; the default SVG layout uses `stroke-opacity="0.2"` so the
  stroke is near-invisible and the fill-rgba is what carries the
  colour-coding.
- **Layer `order` determines the vertical position.** Frontend at the top
  (order 0), storage at the bottom (order 4). Reversing this confuses
  readers who learned the convention from every architecture doc.

## Cross-references

- [prompts](prompts.md) — the palette is baked into the LLM system prompt
- [formats](formats.md) — Mermaid `classDef` + SVG layer band use this palette
- [TECH-graph-json-schema](TECH-graph-json-schema.md) — layers carry the `color` field from here
- [TECH-mermaid-subgraph-transform](TECH-mermaid-subgraph-transform.md) — Mermaid applies the palette via
  `classDef`
- [TECH-svg-layered-layout](TECH-svg-layered-layout.md) — SVG uses it for band + accent bar + dot
- [`../SKILL.md`](../SKILL.md) — parent skill

