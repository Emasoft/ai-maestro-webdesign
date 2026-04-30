---
name: amw-ascii-to-svg
description: "Shortcut for users who have a ready ASCII diagram and want a clean SVG output directly — parses Unicode box-drawing into a node/edge graph and renders via diagram-architecture. An agent in Main-agent mode may also invoke skills/amw-ascii-to-svg/ directly via the orchestrator, with access to parser and routing techniques beyond what this command exposes."
---

# /amw-ascii-to-svg

Take ASCII art using Unicode box-drawing characters (`┌─┐│└┘├┤┬┴┼→↓←↑`) and produce a clean SVG diagram. Routes through the `ascii-to-svg` skill for parsing, then through `diagram-architecture` or `diagram-svg` for the render — whichever better fits the content.

## Arguments

One of:

- `$ARGUMENTS` is a path to a `.txt` or `.md` file containing the ASCII art (possibly inside a fenced code block the command should strip).
- `$ARGUMENTS` is inline ASCII pasted after the command — detect by presence of `┌─` or `│` or `┤` in the text.
- `$ARGUMENTS` is empty → ask the user to paste the ASCII or pass a file path.

## Input format expected

The command accepts any of the three standards the `ascii-parse.py` helper (Phase B2) recognizes:

1. **Unicode box-drawing** (recommended): `┌─┐│└┘├┤┬┴┼`. Arrows: `→↓←↑` or `-->`, `<--`.
2. **ASCII ASCII-art boxes**: `+---+ | | +---+`. Arrows: `->`, `<-`, `|`, `v`, `^`.
3. **Mermaid-like text** (if the input happens to be a Mermaid flowchart block, route directly to `diagram-architecture` in `mermaid` output mode instead of re-parsing).

Label text inside boxes is preserved verbatim. Edge labels between arrows are preserved.

## Action

### 1. Detect format and extract

- If input is a file, read it and strip any Markdown code-fence wrappers.
- Detect which of the three input formats is used.
- If mixed or ambiguous, ask the user for clarification.

### 2. Parse to graph JSON

Invoke `bin/amw-ascii-parse.py --format <detected> --out /tmp/amw-ascii-<slug>-graph.json` (once Phase B2 lands). Until then, perform the parse in-skill following the `ascii-to-svg` SKILL.md instructions.

Graph JSON schema:

```json
{
  "nodes": [{"id": "n1", "label": "API Gateway", "x": 120, "y": 60, "w": 200, "h": 60}],
  "edges": [{"from": "n1", "to": "n2", "label": "authenticates"}],
  "grid": {"cols": 60, "rows": 20}
}
```

### 3. Classify the content

Look at the node labels and edge density:

- Layered system with 3-6 buckets (API, DB, Cache, Queue…) → **route to `diagram-architecture`** (it does layer-aware layout).
- Decision tree / flowchart with yes/no branches → **route to `diagram-svg`** (general flowchart style).
- Sequence (user → frontend → backend) → **route to `diagram-editorial`** in sequence mode.
- Single freeform cluster → **route to `diagram-svg`**.

### 4. Render

Hand the graph JSON + chosen skill a concise instruction:

> "Render this graph as a clean SVG. Preserve every node label and edge label verbatim. Use oklch colors per skills/amw-design-principles/color-system.md. Output only the SVG, no wrapper prose."

Save the SVG to `/tmp/amw-ascii-<slug>-out.svg`. If the user asked for PNG or PDF, also run `bin/amw-svg-render.py <svg> --out <png>` (Phase B1).

### 5. Visual verify loop

Per the mandatory loop in `skills/amw-svg-creator/SKILL.md` (which the shared `bin/amw-svg-render.py` borrows), render PNG, visually inspect, fix the SVG if anything is mis-aligned or text overflows. Max 3 iterations; if still broken after 3, report what failed.

### 6. Deliver

Return the SVG path and a one-line summary: *"Parsed N nodes and M edges → /tmp/amw-ascii-<slug>-out.svg (SVG) + /tmp/amw-ascii-<slug>-out.png (preview)."*

Do not inline the SVG into chat — it pollutes context and the user already has the path.

## Non-negotiables

- **Preserve every text label.** No auto-paraphrasing. If a label is too long for its node, flag it to the user and ask whether to truncate or enlarge the node.
- **oklch colors** per design-principles. Do not use `#000` or `#fff` directly.
- **No Framer Motion / GSAP** — SVG can have SMIL animations if the input ASCII includes motion hints (rare), otherwise static.
- **No AI-drawn illustration** — this command is structural only. Nodes stay as geometric primitives.

## Routing table (quick reference)

| Input shape | Preferred renderer | Output |
|---|---|---|
| Layered architecture | `diagram-architecture` (layer mode) | SVG |
| Flowchart with decisions | `diagram-svg` | SVG |
| Sequence | `diagram-editorial` (sequence mode) | HTML+SVG |
| Already Mermaid text | `diagram-architecture` (mermaid → svg) | SVG |

## Failure modes

- ASCII contains Unicode characters outside the box-drawing set → parser will keep them as text inside the nearest node; if unexpected, warn the user.
- Grid is too dense to parse (overlapping lines, ambiguous intersections) → ask the user to space the diagram out or pass it as a list of edges.
- No arrows detected → treat as node-only diagram (Venn / pyramid / cluster) and pick the `diagram-editorial` renderer.
