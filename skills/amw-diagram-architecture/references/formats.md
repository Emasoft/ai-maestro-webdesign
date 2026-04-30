# Architecture Canvas — Output Format Transforms

All four formats start from the same graph JSON produced by the LLM call.
Each section below describes the transform for one format.

---

## Format 1: `graph` (default)

**Return the graph JSON as-is.** No transform needed.

### Schema

```jsonc
{
  "title": "string (3–5 words, title-case)",
  "subtitle": "string (≤12 words, one sentence)",
  "layers": [
    {
      "id": "string (snake_case, unique)",
      "label": "string (displayed in layer header)",
      "color": "string (#hex)",
      "order": "integer (0 = topmost, increments by 1)"
    }
  ],
  "nodes": [
    {
      "id": "string (snake_case, unique)",
      "label": "string (1–3 words, title-case)",
      "description": "string (≤8 words, plain English)",
      "layerId": "string (must match a layer id)"
    }
  ],
  "edges": [
    {
      "id": "string (unique, e.g. 'e1' or 'e_src_tgt')",
      "source": "string (must be a valid node id)",
      "target": "string (must be a valid node id)",
      "label": "string (optional, empty string if unused)"
    }
  ]
}
```

### Constraints

| Field | Min | Max | Preferred |
|-------|-----|-----|-----------|
| layers | 2 | 6 | 3–5 |
| nodes total | 4 | 14 | 8–10 |
| nodes per layer | 1 | 5 | 2–4 |
| edges total | 0 | floor(n×0.8) | essential paths only |

---

## Format 2: `mermaid`

Transform the graph into a **Mermaid flowchart** using subgraphs for layers.

### Transform Rules

1. Open with `flowchart TD` (top-down flow)
2. For each layer (in `order` ascending), emit a `subgraph` block:
   ```
   subgraph LAYER_LABEL
     node_id["Node Label\ndescription"]
   end
   ```
3. After all subgraphs, emit edges:
   ```
   source_id --> target_id
   ```
   If the edge has a non-empty label:
   ```
   source_id -->|label text| target_id
   ```
4. Add `%%` comments for the title and subtitle at the top
5. Apply styling using `classDef` and `class` to color nodes by layer

### Layer Color Mapping

```
classDef layer0 fill:#6366F1,color:#fff,stroke:#4F46E5
classDef layer1 fill:#8B5CF6,color:#fff,stroke:#7C3AED
classDef layer2 fill:#06B6D4,color:#fff,stroke:#0891B2
classDef layer3 fill:#10B981,color:#fff,stroke:#059669
classDef layer4 fill:#F59E0B,color:#fff,stroke:#D97706
```

Assign each node to the `classDef` matching its layer's `order`.

### Mermaid Output Template

```
%% {title}
%% {subtitle}
flowchart TD
  subgraph {layer0.label}
    {node_id}["{node_label}\n{node_description}"]
    ...
  end
  subgraph {layer1.label}
    ...
  end
  ...
  {source} --> {target}
  {source} -->|{label}| {target}
  ...
  classDef layer0 fill:#6366F1,color:#fff,stroke:#4F46E5
  classDef layer1 fill:#8B5CF6,color:#fff,stroke:#7C3AED
  classDef layer2 fill:#06B6D4,color:#fff,stroke:#0891B2
  classDef layer3 fill:#10B981,color:#fff,stroke:#059669
  classDef layer4 fill:#F59E0B,color:#fff,stroke:#D97706
  class {layer0_node_ids} layer0
  class {layer1_node_ids} layer1
  ...
```

### Mermaid ID Safety

Mermaid node IDs must not contain spaces or hyphens in raw form.
Snake_case IDs from the graph format are safe as-is.
If a label contains special characters, wrap it in quotes inside `["…"]`.

---

## Format 3: `svg`

Render the graph as a **self-contained SVG** (~820px wide, auto height).

### Layout Algorithm

```
CONSTANTS:
  CANVAS_W     = 820
  PAD          = 40          // canvas padding
  GROUP_PAD_X  = 24          // horizontal padding inside layer band
  GROUP_PAD_TOP = 36         // space for layer label
  GROUP_PAD_BOT = 20
  GROUP_V_GAP  = 20          // vertical gap between layers
  NODE_W       = 160
  NODE_H       = 64
  NODE_H_GAP   = 16          // horizontal gap between nodes in same layer
  NODE_R       = 10          // border-radius

LAYER BAND WIDTH = CANVAS_W - PAD * 2

For each layer (top to bottom):
  nodes_in_layer = nodes where layerId == layer.id  (preserving graph order)
  row_width      = len(nodes) * NODE_W + (len(nodes)-1) * NODE_H_GAP
  start_x        = PAD + GROUP_PAD_X + (LAYER_BAND_WIDTH - 2*GROUP_PAD_X - row_width) / 2
  node_y         = current_y + GROUP_PAD_TOP + (NODE_H_max - NODE_H) / 2  // vertically centered

EDGES:
  source point: (node.cx, node.y + NODE_H)   // bottom-center
  target point: (node.cx, node.y)             // top-center
  path: cubic bezier  C sx sy+ctrl, tx ty-ctrl, tx ty
  ctrl = min(abs(ty - sy) * 0.45, 56)
```

### SVG Structure

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="820" height="{total_h}"
     font-family="system-ui, -apple-system, sans-serif">
  <defs>
    <!-- Grid pattern -->
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#D8DBE2" stroke-width="0.6"/>
    </pattern>
    <!-- Arrowhead marker -->
    <marker id="arrow" markerWidth="9" markerHeight="9"
            refX="8" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M 0 0 L 9 4.5 L 0 9 L 2.7 4.5 Z" fill="#C7CBD4"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="820" height="{total_h}" fill="#ECEEF2"/>
  <rect width="820" height="{total_h}" fill="url(#grid)"/>

  <!-- For each layer: band + label -->
  <rect x="{gx}" y="{gy}" width="{gw}" height="{gh}"
        rx="12" fill="rgba(255,255,255,0.5)"
        stroke="{layer.color}" stroke-width="1" stroke-opacity="0.2"/>
  <!-- Left accent bar -->
  <rect x="{gx}" y="{gy+12}" width="3" height="{gh-24}"
        rx="1.5" fill="{layer.color}" opacity="0.7"/>
  <!-- Layer label pill -->
  <rect x="{gx+12}" y="{gy+10}" width="{pill_w}" height="18"
        rx="9" fill="{layer.color}" opacity="0.15"/>
  <text x="{gx+20}" y="{gy+23}" font-size="10" font-weight="700"
        fill="{layer.color}" letter-spacing="0.06em"
        text-transform="uppercase">{LAYER LABEL}</text>

  <!-- Edges (drawn before nodes so they appear behind) -->
  <path d="M {x1} {y1} C {x1} {y1+ctrl} {x2} {y2-ctrl} {x2} {y2}"
        fill="none" stroke="#C7CBD4" stroke-width="1.5"
        marker-end="url(#arrow)" opacity="0.6"/>

  <!-- For each node: card -->
  <!-- Drop shadow -->
  <rect x="{nx+2}" y="{ny+4}" width="{NODE_W}" height="{NODE_H}"
        rx="{NODE_R}" fill="black" opacity="0.04"/>
  <!-- Card body -->
  <rect x="{nx}" y="{ny}" width="{NODE_W}" height="{NODE_H}"
        rx="{NODE_R}" fill="white" stroke="#E4E7ED" stroke-width="1"/>
  <!-- Top accent bar -->
  <rect x="{nx}" y="{ny}" width="{NODE_W}" height="3"
        rx="1.5" fill="{layer.color}" opacity="0.8"/>
  <!-- Node label -->
  <text x="{nx+12}" y="{ny+22}" font-size="13" font-weight="600"
        fill="#111318">{node.label}</text>
  <!-- Node description -->
  <text x="{nx+12}" y="{ny+40}" font-size="10.5"
        fill="#6B7280">{node.description}</text>
  <!-- Color dot -->
  <circle cx="{nx+NODE_W-12}" cy="{ny+NODE_H-12}" r="3.5"
          fill="{layer.color}" opacity="0.55"/>

  <!-- Title block (below diagram) -->
  <text x="410" y="{total_h - 18}" text-anchor="middle"
        font-size="12" font-weight="600" fill="#6B7280">{graph.title}</text>
</svg>
```

### SVG Height Calculation

```
layer_height(layer) = GROUP_PAD_TOP + NODE_H + GROUP_PAD_BOT
total_content_h     = sum(layer_heights) + (n_layers - 1) * GROUP_V_GAP
total_svg_h         = PAD + total_content_h + PAD + 32  // +32 for title row
```

---

## Format 4: `png`

`png` output is identical to `svg` output — return the same SVG string —
with the following addition at the end of the response:

```
---
To save as PNG:
1. Copy the SVG above into a file named architecture.svg
2. Open it in any browser — it renders immediately
3. Right-click the image → "Save image as…" → choose PNG
   OR use the browser's print dialog → Save as PDF, then convert

For programmatic conversion:
  • Node.js: sharp('architecture.svg').png().toFile('architecture.png')
  • Python:  cairosvg.svg2png(url='architecture.svg', write_to='architecture.png')
  • CLI:     inkscape architecture.svg --export-png=architecture.png
  • Online:  https://svgtopng.com
```

This approach works reliably across all environments without requiring
canvas or blob APIs.
