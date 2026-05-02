## Table of Contents

- [Stage 1 — Graph Validation (all formats)](#stage-1-graph-validation-all-formats)
  - [1.1 Layer count](#11-layer-count)
  - [1.2 Node count](#12-node-count)
  - [1.3 Layer balance](#13-layer-balance)
  - [1.4 Node label quality](#14-node-label-quality)
  - [1.5 Edge integrity](#15-edge-integrity)
  - [1.6 ID integrity](#16-id-integrity)
  - [1.7 Layer order sequence](#17-layer-order-sequence)
- [Stage 2 — Format Validation](#stage-2-format-validation)
  - [Format: `graph`](#format-graph)
  - [Format: `mermaid`](#format-mermaid)
  - [Format: `svg`](#format-svg)
  - [Format: `png`](#format-png)
- [Validation Summary (quick reference)](#validation-summary-quick-reference)


# Architecture Canvas — Output Validation

Validation runs in two stages. Both must pass before returning output.

- **Stage 1 — Graph validation**: structural checks on the graph JSON.
  Runs for every `output_format`, immediately after the LLM call.
- **Stage 2 — Format validation**: surface-level checks on the rendered output.
  Runs after the transform, specific to each format.

If a check fails, apply the listed fix inline. Do not surface errors to the
caller unless the fix is impossible.

---

## Stage 1 — Graph Validation (all formats)

Run these checks on the raw graph JSON before any transform.

### 1.1 Layer count

| Check | Condition | Fix |
|-------|-----------|-----|
| Too few layers | `layers.length < 2` | Re-run generation — this graph cannot be fixed by patching |
| Too many layers | `layers.length > 6` | Merge the two most similar adjacent layers into one; re-assign their nodes |
| Prefer range | `layers.length < 3 or > 5` | Warn internally; acceptable, do not auto-fix |

### 1.2 Node count

| Check | Condition | Fix |
|-------|-----------|-----|
| Too few nodes | `nodes.length < 4` | Re-run generation |
| Too many nodes | `nodes.length > 14` | Drop nodes whose descriptions most overlap with a sibling node in the same layer. Remove their edges too. |
| Prefer range | `nodes.length < 6 or > 12` | Warn internally; acceptable |

### 1.3 Layer balance

For each layer, count `nodes_in_layer = nodes.filter(n => n.layerId == layer.id).length`.

| Check | Condition | Fix |
|-------|-----------|-----|
| Empty layer | `nodes_in_layer == 0` | Remove the layer from the layers array entirely |
| Overloaded layer | `nodes_in_layer > 5` | Move the least-essential node to an adjacent layer with fewer nodes |

### 1.4 Node label quality

For each node:

| Check | Condition | Fix |
|-------|-----------|-----|
| Label too long | word count > 4 | Truncate to the first 3 meaningful words, title-case |
| Label not title-case | e.g. `"api gateway"` | Convert to title-case: `"Api Gateway"` → `"API Gateway"` using common acronym list |
| Description too long | word count > 8 | Truncate to 7 words, preserving the core verb + object |
| Description is empty | `description == ""` | Infer a 4–6 word description from the node label |

**Common acronyms to preserve uppercase**: API, UI, DB, ID, URL, HTTP, SDK,
SPA, ETL, ML, AI, S3, CDN, DNS, JWT, SSO, TLS, gRPC, REST.

### 1.5 Edge integrity

| Check | Condition | Fix |
|-------|-----------|-----|
| Dangling source | `edge.source` not in node IDs | Remove the edge |
| Dangling target | `edge.target` not in node IDs | Remove the edge |
| Self-loop | `edge.source == edge.target` | Remove the edge |
| Duplicate edge | same (source, target) pair appears twice | Remove the duplicate; keep first occurrence |
| Reverse duplicate | both A→B and B→A exist | Remove the one that goes against layer order (upward edge) |
| Edge budget exceeded | `edges.length > floor(nodes.length × 0.8)` | Remove edges greedily: prefer removing cross-layer-skip edges first, then same-layer edges, then the edge with the longest label |

### 1.6 ID integrity

| Check | Condition | Fix |
|-------|-----------|-----|
| Duplicate layer ID | two layers share the same `id` | Append `_2` to the second one; update all `layerId` references |
| Duplicate node ID | two nodes share the same `id` | Append `_b` to the second one; update all edge source/target references |
| Node references missing layer | `node.layerId` not in layer IDs | Assign node to the layer whose label is most semantically similar |

### 1.7 Layer order sequence

`order` values must be `0, 1, 2, …` with no gaps and no duplicates.

Fix: sort layers by their current `order` value, then re-assign `order = index`.

---

## Stage 2 — Format Validation

Run after the transform. Each format has its own checks.

---

### Format: `graph`

No additional checks beyond Stage 1. The validated graph JSON IS the output.

Confirm the final JSON is well-formed before returning:
- Parse it with `JSON.parse` — if this fails, re-run the repair recipe in [prompts](prompts.md)
- Confirm the top-level keys `title`, `subtitle`, `layers`, `nodes`, `edges` are all present

---

### Format: `mermaid`

After generating the Mermaid string, check:

| Check | Condition | Fix |
|-------|-----------|-----|
| Missing `flowchart TD` | First non-comment line is not `flowchart TD` | Prepend `flowchart TD` |
| Subgraph count mismatch | Number of `subgraph` blocks ≠ number of layers | Regenerate from the validated graph |
| Node count mismatch | Number of node definitions ≠ `nodes.length` | Regenerate from the validated graph |
| Edge count mismatch | Number of `-->` lines ≠ `edges.length` | Regenerate from the validated graph |
| Missing `classDef` block | `classDef layer0` not present | Append the full classDef block from [formats](formats.md) |
| Missing `class` assignments | Any layer has nodes but no `class ... layerN` line | Append missing class assignment lines |
| Special chars in node ID | Node ID contains `-`, space, or `.` | Replace with `_` in the Mermaid output only (do not change the graph JSON) |
| Label contains `"` | Unescaped double-quote inside `["…"]` | Escape as `&quot;` or replace with `'` |
| Subgraph label contains `(` or `)` | Mermaid treats these as node shape syntax | Replace with `[` and `]` in the subgraph label string |

**Structural re-generation trigger**: if more than 2 of the above checks fail
simultaneously, discard the Mermaid string and regenerate from scratch using
the validated graph rather than patching multiple issues.

---

### Format: `svg`

After generating the SVG string, check:

#### Well-formedness

| Check | Condition | Fix |
|-------|-----------|-----|
| Missing XML declaration root | Does not start with `<svg` | Prepend `<svg xmlns="http://www.w3.org/2000/svg" ...>` |
| Unclosed root element | Does not end with `</svg>` | Append `</svg>` |
| Missing `<defs>` block | No `<defs>` present | Prepend the standard defs block from [formats](formats.md) |
| Missing arrow marker | `id="arrow"` not in defs | Insert the marker element into the existing `<defs>` |
| Unescaped `&` in text | Raw `&` in a `<text>` element | Replace with `&amp;` |
| Unescaped `<` in text | Raw `<` in a `<text>` element | Replace with `&lt;` |

#### Layout sanity

| Check | Condition | Fix |
|-------|-----------|-----|
| Zero or negative height | `height` attribute ≤ 0 | Recalculate using the formula in [formats](formats.md) |
| Node count in SVG | Number of card `<rect>` elements with `fill="white"` ≠ `nodes.length` | Regenerate SVG from the validated graph |
| Layer band count | Number of layer band `<rect rx="12">` elements ≠ `layers.length` | Regenerate SVG from the validated graph |
| Node overflows layer band | Computed `node.y + NODE_H > layer_band_bottom` | Increase the layer band height and shift all lower layers down |
| Nodes overlap | Two nodes in same layer have overlapping x-ranges | Re-run the horizontal centering calculation for that layer |
| Title text missing | No `<text>` with `text-anchor="middle"` near bottom of SVG | Append the title text element |

#### Visual quality

| Check | Condition | Fix |
|-------|-----------|-----|
| No grid background | `url(#grid)` not referenced | Add the grid rect after the background rect |
| No accent bars | No `<rect width="3" ...>` elements | Regenerate — accent bars are essential visual structure |
| Edges drawn after nodes | `<path marker-end="url(#arrow)">` elements appear after node `<rect>` elements | Reorder: move all edge paths before the first node card rect |

**SVG re-generation trigger**: if any layout sanity check fails (node count
mismatch, layer band count mismatch, or node overflow), discard and regenerate
the entire SVG from the validated graph. Patching pixel coordinates is
error-prone and should be avoided.

---

### Format: `png`

`png` uses the same SVG as the `svg` format — run the full SVG validation
above first.

After SVG validation passes, additionally check:

| Check | Condition | Fix |
|-------|-----------|-----|
| Export instructions missing | The five-line instructions block is not present | Append the standard instructions block from [formats](formats.md) |
| Instructions appear before SVG | Instructions block precedes the `<svg` tag | Move instructions to after `</svg>` |

---

## Validation Summary (quick reference)

```
After LLM call:
  ✓ 2–6 layers (2–6 hard, 3–5 preferred)
  ✓ 4–14 nodes (4–14 hard, 8–10 preferred)
  ✓ No empty layers
  ✓ No layer with > 5 nodes
  ✓ Node labels ≤ 4 words, title-case
  ✓ Node descriptions ≤ 8 words
  ✓ No dangling, duplicate, self-loop, or upward-only duplicate edges
  ✓ Edge count ≤ floor(n × 0.8)
  ✓ No duplicate IDs
  ✓ All node layerIds resolve to a real layer
  ✓ Layer order = 0, 1, 2, … with no gaps

After transform (format-specific):
  graph  → JSON parses cleanly, all top-level keys present
  mermaid → flowchart TD present, subgraph/node/edge counts match,
             classDefs + class assignments present, IDs are safe
  svg    → well-formed XML, defs/arrow present, height > 0,
             node/layer counts match, edges behind nodes, title present
  png    → SVG passes svg checks + export instructions appended after SVG
```
