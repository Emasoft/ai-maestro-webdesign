---
name: amw-ascii-to-svg
description: DEPRECATED — superseded by amw-diagram-convert (which uses the IR pivot for any-to-any conversion across ASCII/HTML/SVG/Mermaid/PNG). Kept as a low-level primitive for direct ASCII→SVG paths and for the /amw-ascii-to-svg slash command (backward compatibility). New code should route through amw-diagram-convert. Triggers narrowly on the legacy phrasings only.
version: 0.2.0
---

# ASCII to SVG (DEPRECATED — see amw-diagram-convert)

> **DEPRECATED:** This skill is superseded by `../amw-diagram-convert/SKILL.md`, which uses the IR-pivot to handle the full N×N format-conversion matrix (ASCII / HTML / SVG / Mermaid / PNG) without N² special cases. New code should route through `amw-diagram-convert` whenever multiple format conversions are needed. This skill remains as a low-level primitive for the direct ASCII→SVG path and for the `/amw-ascii-to-svg` slash command (backward compatibility).
>
> The `amw-diagram-convert` skill internally calls this skill's `bin/amw-ascii-parse.py` for the ASCII parsing step, so the IR-pivot path subsumes everything documented below.
>
> **Orchestrated by:** `../amw-design-principles/SKILL.md`.

## Activation

Callable directly via the `/amw-ascii-to-svg` command (user shortcut — fast path for users with a ready ASCII diagram), or invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode. In Main-agent mode the orchestrator may apply parser-routing and format-detection techniques from this skill beyond what the `/amw-ascii-to-svg` command parameters expose.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT (Phase B). Parses ASCII box-drawing input and routes the rendering to the best diagram sub-skill (`diagram-architecture` for layered systems, `diagram-svg` for freeform, `diagram-editorial` for sequences). This skill is the parser + router, not the renderer.

## Input formats accepted

1. **Unicode box-drawing** — corners, horizontal and vertical edges, tees, crosses with arrows (recommended).
2. **ASCII art boxes** — `+---+`, `|`, `|`, `+---+` with arrows `->`, `<-`, `v`, `^`, `|`, `-`.
3. **Mermaid-like text** — if detected, routes directly to `diagram-architecture` in mermaid-passthrough mode.

Input can be passed as:

- File path (`.txt` / `.md`)
- Inline ASCII pasted after the `/amw-ascii-to-svg` command
- Content inside a fenced code block in chat (strip the fence first)

## Action

1. Detect format (unicode / ASCII / mermaid). Ask user if ambiguous.
2. Invoke `../../bin/amw-ascii-parse.py --in <source> --mode diagram --out /tmp/amw-ascii-<slug>-graph.json` to tokenize into a node/edge graph.
3. Classify the content:
   - Layered system with 3-6 buckets → route to `../amw-diagram-architecture/SKILL.md`
   - Decision tree / flowchart → route to `../amw-diagram-svg/SKILL.md`
   - Sequence (user → frontend → backend) → route to `../amw-diagram-editorial/SKILL.md` in sequence mode
   - Freeform cluster → route to `../amw-diagram-svg/SKILL.md`
4. Hand the chosen renderer a concise instruction: preserve every node and edge label verbatim; use oklch colors per `design-principles`; output SVG only, no wrapper prose.
5. Save SVG to `/tmp/amw-ascii-<slug>-out.svg`.
6. Run `../../bin/amw-svg-render.py render /tmp/amw-ascii-<slug>-out.svg` to generate PNG preview.
7. Visual-verify loop: render → view → fix → render, max 3 iterations. If still broken after 3, report what failed.
8. Deliver paths to the user. Do NOT inline the SVG into chat.

## Dependencies

- `python3` — runs `bin/amw-ascii-parse.py` and `bin/amw-svg-render.py`
- `cairosvg` — auto-installed by `bin/amw-svg-render.py` on first run

## Cross-references

- `../../bin/amw-ascii-parse.py` — tokenizer
- `../../bin/amw-svg-render.py` — render-verify-finish loop
- `../amw-diagram-architecture/SKILL.md` — layered-system route
- `../amw-diagram-svg/SKILL.md` — freeform route
- `../amw-diagram-editorial/SKILL.md` — sequence route
- `../amw-design-principles/color-system.md` — oklch palette
- `../amw-design-principles/typography-system.md` — node-label type sizes
- `/amw-ascii-to-svg` — user-facing command that invokes this skill

## Routing table

| Input shape | Preferred renderer | Output |
|---|---|---|
| Layered architecture | `diagram-architecture` (layer mode) | SVG |
| Flowchart with decisions | `diagram-svg` | SVG |
| Sequence | `diagram-editorial` (sequence mode) | HTML+SVG |
| Already Mermaid text | `diagram-architecture` (mermaid to svg) | SVG |

## Non-negotiables

- Preserve EVERY text label verbatim — no auto-paraphrasing. If a label is too long for its node, flag and ask the user whether to truncate or enlarge the node.
- oklch colors from `design-principles` — no bare `#000` or `#fff`.
- Every SVG goes through `bin/amw-svg-render.py` visual-verify loop before delivery.
- No AI-drawn illustration — nodes stay geometric.
- No Framer Motion or GSAP.

## Failure modes

- Ambiguous input format (mixed Unicode and ASCII markers) — ask the user to pick one and re-paste.
- Dense or overlapping lines that the tokenizer cannot disambiguate — ask the user to space the diagram out or supply an explicit edge list.
- Missing arrows — treat as a node-only cluster and route to `diagram-editorial`.
- Unsupported Unicode characters inside a node label — preserve them as inline text; warn the user if they seem accidental.
- Parser returns an empty graph — surface the raw parse error to the user, do not fabricate nodes.
- Routing mismatch (classified as layered but renderer rejects it) — fall back to `diagram-svg` once, then surface the failure.
