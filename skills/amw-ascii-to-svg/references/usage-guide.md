# amw-ascii-to-svg — Usage Guide (extended)

Routing surface and quick instructions live in the parent `SKILL.md`. This reference holds the activation rules, input-format catalogue, routing table, examples, non-negotiables, and error-handling notes that previously sat inline.

> Deprecated; prefer `../amw-diagram-convert/SKILL.md` (IR-pivot) for new work.

## Table of Contents

- [Position in flow](#position-in-flow)
- [Activation](#activation)
- [Input formats accepted](#input-formats-accepted)
- [Routing table](#routing-table)
- [Prerequisites](#prerequisites)
- [Examples](#examples)
- [Non-negotiables](#non-negotiables)
- [Error handling](#error-handling)

## Position in flow

OUTPUT (Phase B). Parses ASCII box-drawing input and routes the rendering to the best diagram sub-skill (`diagram-architecture` for layered systems, `diagram-svg` for freeform, `diagram-editorial` for sequences). This skill is the parser + router, not the renderer.

## Activation

Callable directly via the `/amw-ascii-to-svg` command (user shortcut — fast path for users with a ready ASCII diagram), or invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode. In Main-agent mode the orchestrator may apply parser-routing and format-detection techniques from this skill beyond what the `/amw-ascii-to-svg` command parameters expose.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Input formats accepted

1. **Unicode box-drawing** — corners, horizontal and vertical edges, tees, crosses with arrows (recommended).
2. **ASCII art boxes** — `+---+`, `|`, `|`, `+---+` with arrows `->`, `<-`, `v`, `^`, `|`, `-`.
3. **Mermaid-like text** — if detected, routes directly to `diagram-architecture` in mermaid-passthrough mode.

Input can be passed as:

- File path (`.txt` / `.md`)
- Inline ASCII pasted after the `/amw-ascii-to-svg` command
- Content inside a fenced code block in chat (strip the fence first)

## Routing table

| Input shape | Preferred renderer | Output |
|---|---|---|
| Layered architecture | `diagram-architecture` (layer mode) | SVG |
| Flowchart with decisions | `diagram-svg` | SVG |
| Sequence | `diagram-editorial` (sequence mode) | HTML+SVG |
| Already Mermaid text | `diagram-architecture` (mermaid to svg) | SVG |

## Prerequisites

- `python3` — runs `bin/amw-ascii-parse.py` and `bin/amw-svg-render.py`
- `cairosvg` — auto-installed by `bin/amw-svg-render.py` on first run

## Examples

**Concrete example — system architecture diagram (layered route):**

- **Input:** an ASCII layered-architecture sketch in a `.txt` file:
  ```
  ┌──────────────┐
  │   Browser    │
  └──────┬───────┘
         │ HTTPS
  ┌──────▼───────┐
  │   API server │
  └──────┬───────┘
  ```
- **Routing:** detected as a layered architecture diagram; delegates to `amw-diagram-architecture/`.
- **Output:** `architecture.svg` rendered by `bin/amw-svg-render.py` with measured node boxes, connectors, and oklch palette tokens applied. Saved to the project's design folder per the routing rules.

**Concrete example — freeform diagram:**

- **Input:** a freeform ASCII drawing with arrows but no clean layers (e.g. a flowchart describing a checkout funnel).
- **Routing:** delegates to `amw-diagram-svg/` (freeform SVG primitives from natural-language intent + ASCII anchor).
- **Output:** standalone `.svg` file with hand-tuned positioning per the source ASCII, no auto-layout.

## Non-negotiables

- Preserve EVERY text label verbatim — no auto-paraphrasing. If a label is too long for its node, flag and ask the user whether to truncate or enlarge the node.
- oklch colors from `design-principles` — no bare `#000` or `#fff`.
- Every SVG goes through `bin/amw-svg-render.py` visual-verify loop before delivery.
- No AI-drawn illustration — nodes stay geometric.
- No Framer Motion or GSAP.

## Error handling

- Ambiguous input format (mixed Unicode and ASCII markers) — ask the user to pick one and re-paste.
- Dense or overlapping lines that the tokenizer cannot disambiguate — ask the user to space the diagram out or supply an explicit edge list.
- Missing arrows — treat as a node-only cluster and route to `diagram-editorial`.
- Unsupported Unicode characters inside a node label — preserve them as inline text; warn the user if they seem accidental.
- Parser returns an empty graph — surface the raw parse error to the user, do not fabricate nodes.
- Routing mismatch (classified as layered but renderer rejects it) — fall back to `diagram-svg` once, then surface the failure.
