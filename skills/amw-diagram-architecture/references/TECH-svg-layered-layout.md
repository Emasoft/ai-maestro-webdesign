---
name: TECH-svg-layered-layout
category: architecture-graph
source: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/formats.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-svg-layered-layout

## What it does

Renders the validated graph JSON as a **self-contained SVG** (~820px
wide, auto height) using a deterministic layered layout algorithm. Each
layer becomes a horizontal band; each node a rounded card with a
colour-coded accent bar; edges drawn as cubic Bézier curves behind the
cards.

## When to use

- **`output_format: "svg"`** or `"png"` — this is the render step for
  both.
- **Offline / self-contained output** — the SVG is standalone, no
  external fonts or images needed.

Do not use for Markdown-rendered docs where the consumer renders Mermaid
directly — that is cheaper; reserve SVG for embedded artifacts that
need to look identical across renderers.

## How it works

### Canvas constants

```
CANVAS_W       = 820
PAD            = 40         canvas padding
GROUP_PAD_X    = 24         horizontal padding inside layer band
GROUP_PAD_TOP  = 36         space for layer label
GROUP_PAD_BOT  = 20
GROUP_V_GAP    = 20         vertical gap between layers
NODE_W         = 160
NODE_H         = 64
NODE_H_GAP     = 16         horizontal gap between nodes
NODE_R         = 10         border-radius
```

### Algorithm

1. For each layer (top to bottom):
   - Compute `nodes_in_layer = nodes where layerId == layer.id`.
   - `row_width = n × NODE_W + (n-1) × NODE_H_GAP`.
   - `start_x = PAD + GROUP_PAD_X + (LAYER_BAND_WIDTH - 2×GROUP_PAD_X - row_width) / 2`.
   - Centre the row horizontally inside the layer band.
2. For each node, render a card (see structure below).
3. For each edge:
   - source point: `(src.cx, src.y + NODE_H)` (bottom-center)
   - target point: `(tgt.cx, tgt.y)` (top-center)
   - path: cubic Bézier with control points vertically offset by
     `min(|ty - sy| × 0.45, 56)`.
4. Draw edges BEFORE nodes so they appear behind the cards.

### Height calculation

```
layer_height = GROUP_PAD_TOP + NODE_H + GROUP_PAD_BOT
total_content_h = sum(layer_heights) + (n_layers - 1) × GROUP_V_GAP
total_svg_h = PAD + total_content_h + PAD + 32   // +32 for title row
```

### Node card structure

```xml
<!-- Drop shadow (offset +2,+4) -->
<rect x="nx+2" y="ny+4" width="NODE_W" height="NODE_H"
      rx="NODE_R" fill="black" opacity="0.04"/>
<!-- Card body -->
<rect x="nx" y="ny" width="NODE_W" height="NODE_H"
      rx="NODE_R" fill="white" stroke="#E4E7ED" stroke-width="1"/>
<!-- Top accent bar (3px tall, layer colour) -->
<rect x="nx" y="ny" width="NODE_W" height="3"
      rx="1.5" fill="{layer.color}" opacity="0.8"/>
<!-- Labels -->
<text x="nx+12" y="ny+22" font-size="13" font-weight="600"
      fill="#111318">{node.label}</text>
<text x="nx+12" y="ny+40" font-size="10.5"
      fill="#6B7280">{node.description}</text>
<!-- Corner dot (bottom-right, layer colour) -->
<circle cx="nx+NODE_W-12" cy="ny+NODE_H-12" r="3.5"
        fill="{layer.color}" opacity="0.55"/>
```

### Layer band structure

```xml
<rect x="40" y="layerY" width="740" height="gh"
      rx="12" fill="rgba(255,255,255,0.5)"
      stroke="{layer.color}" stroke-width="1" stroke-opacity="0.2"/>
<!-- Left accent bar -->
<rect x="40" y="layerY+12" width="3" height="gh-24"
      rx="1.5" fill="{layer.color}" opacity="0.7"/>
<!-- Layer label pill -->
<rect x="52" y="layerY+10" width="pill_w" height="18"
      rx="9" fill="{layer.color}" opacity="0.15"/>
<text x="60" y="layerY+23" font-size="10" font-weight="700"
      fill="{layer.color}" letter-spacing="0.06em"
      text-transform="uppercase">{LAYER LABEL}</text>
```

## Minimal example

2-layer simplified output:

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="820" height="280"
     font-family="system-ui, -apple-system, sans-serif">
  <defs>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#D8DBE2" stroke-width="0.6"/>
    </pattern>
    <marker id="arrow" markerWidth="9" markerHeight="9"
            refX="8" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M 0 0 L 9 4.5 L 0 9 L 2.7 4.5 Z" fill="#C7CBD4"/>
    </marker>
  </defs>

  <rect width="820" height="280" fill="#ECEEF2"/>
  <rect width="820" height="280" fill="url(#grid)"/>

  <!-- Layer 0: Frontend -->
  <rect x="40" y="40" width="740" height="120" rx="12"
        fill="rgba(255,255,255,0.5)" stroke="#6366F1" stroke-opacity="0.2"/>
  <!-- ... node cards here ... -->
</svg>
```

## Gotchas

- **Draw order matters.** Edges must be drawn BEFORE node cards so the
  arrows terminate behind the card visually. Reversing produces arrows
  painted on top of nodes.
- **Grid background is part of the signature look.** Dropping it to save
  bytes makes the diagram feel floaty.
- **Control-point offset capped at 56px.** Larger offsets make the
  Bézier loop back on itself for short edges; 56 is the empirical
  sweet spot.
- **Drop shadow offset `+2,+4`, not centred.** The light-from-above
  convention; centred shadows look like haloing.
- **Re-generate rather than patch** if the Stage 2 layout checks (node
  count mismatch, overflow, overlap) fail. Patching pixel coordinates
  is error-prone; re-rendering from a validated graph is deterministic.

## Cross-references

- [formats](formats.md) — full format transform
  > Format 1: `graph` (default) · Schema · Constraints · Format 2: `mermaid` · Transform Rules · Layer Color Mapping · Mermaid Output Template · Mermaid ID Safety · Format 3: `svg` · Layout Algorithm · SVG Structure · SVG Height Calculation · Format 4: `png`
- [validation](validation.md) — Stage 2 SVG checks (well-formedness, layout sanity)
  > Stage 1 — Graph Validation (all formats) · 1 Layer count · 2 Node count · 3 Layer balance · 4 Node label quality · 5 Edge integrity · 6 ID integrity · 7 Layer order sequence · Stage 2 — Format Validation · Format: `graph` · Format: `mermaid` · Format: `svg` · Format: `png` · Validation Summary (quick reference) · **Stage 1 — Graph validation**: structural checks on the graph JSON. · **Stage 2 — Format validation**: surface-level checks on the rendered output.
- [TECH-graph-json-schema](TECH-graph-json-schema.md) — source schema
  > What it does · When to use · How it works · Constraints · Minimal example · Gotchas · Cross-references
- [TECH-layer-palette-5-colors](TECH-layer-palette-5-colors.md) — palette for band + accent bar + dot
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-mermaid-subgraph-transform](TECH-mermaid-subgraph-transform.md) — sibling transform for Mermaid
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

