---
name: amw-ascii-to-svg
description: Deprecated. See ../amw-diagram-convert/ for the IR-pivot conversion path. This file remains as a low-level primitive callable from /amw-ascii-to-svg only — it has no auto-trigger phrases. Use when the /amw-ascii-to-svg command is explicitly invoked. Trigger with /amw-ascii-to-svg.
version: 0.1.0
---

# ASCII to SVG (DEPRECATED — see amw-diagram-convert)

> **DEPRECATED:** Superseded by [SKILL](../amw-diagram-convert/SKILL.md) (IR-pivot covers the full ASCII / HTML / SVG / Mermaid / PNG matrix). Retained only as a low-level primitive for the `/amw-ascii-to-svg` slash command.
>
> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Deprecated direct ASCII→SVG parser and router. Parses ASCII box-drawing input, classifies the diagram type, and routes rendering to the correct diagram sub-skill. Retained for backward compatibility with the `/amw-ascii-to-svg` command; new workflows should use `amw-diagram-convert`.

## Instructions

1. Detect format (unicode / ASCII / mermaid). Ask user if ambiguous.
2. Invoke `../../bin/amw-ascii-parse.py --in <source> --mode diagram --out /tmp/amw-ascii-<slug>-graph.json` to tokenize into a node/edge graph.
3. Classify the content:
   - Layered system with 3-6 buckets → route to [SKILL](../amw-diagram-architecture/SKILL.md)
   - Decision tree / flowchart → route to [SKILL](../amw-diagram-svg/SKILL.md)
   - Sequence (user → frontend → backend) → route to [SKILL](../amw-diagram-editorial/SKILL.md) in sequence mode
   - Freeform cluster → route to [SKILL](../amw-diagram-svg/SKILL.md)
4. Hand the chosen renderer a concise instruction: preserve every node and edge label verbatim; use oklch colors per `design-principles`; output SVG only, no wrapper prose.
5. Save SVG to `/tmp/amw-ascii-<slug>-out.svg`.
6. Run `../../bin/amw-svg-render.py render /tmp/amw-ascii-<slug>-out.svg` to generate PNG preview.
7. Visual-verify loop: render → view → fix → render, max 3 iterations. If still broken after 3, report what failed.
8. Deliver paths to the user. Do NOT inline the SVG into chat.

Full activation rules, accepted input formats, routing table, worked examples, non-negotiables, error-handling notes: see [usage-guide](./references/usage-guide.md).
> Position in flow · Activation · Input formats accepted · Routing table · Prerequisites · Examples · Non-negotiables · Error handling

## Prerequisites

- `python3` — runs `bin/amw-ascii-parse.py` and `bin/amw-svg-render.py`
- `cairosvg` — auto-installed by `bin/amw-svg-render.py` on first run
- Companion skill: [SKILL](../amw-diagram-convert/SKILL.md) — preferred replacement (IR-pivot)

## Output

Produces a single artifact at the path specified in §Instructions — an SVG file rendered by the target diagram sub-skill.

## Examples

- **Input:** ASCII layered-architecture sketch (`Browser → API server`). **Routing:** layered → `amw-diagram-architecture/`. **Output:** `architecture.svg` rendered with measured boxes + oklch tokens.
- **Input:** freeform ASCII flowchart with arrows but no layers. **Routing:** freeform → `amw-diagram-svg/`. **Output:** hand-positioned `.svg`, no auto-layout.

See the extended usage guide (Resources) for full worked examples.

## Error Handling

Common failure modes and remediation are listed in the extended usage guide (see Resources). Summary: ambiguous input format → ask user to pick one; dense overlapping lines → ask user to space out; missing arrows → route as node-only cluster to `diagram-editorial`; parser returns empty graph → surface raw parse error (never fabricate nodes).

## Resources

- `../../bin/amw-ascii-parse.py` — tokenizer
- `../../bin/amw-svg-render.py` — render-verify-finish loop
- [SKILL](../amw-diagram-architecture/SKILL.md) — layered-system route
- [SKILL](../amw-diagram-svg/SKILL.md) — freeform route
- [SKILL](../amw-diagram-editorial/SKILL.md) — sequence route
- [color-system](../amw-design-principles/color-system.md) — oklch palette
  > I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — node-label type sizes
  > I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax · VIII. Forbidden AI-giveaway fonts (T-043)
- [usage-guide](./references/usage-guide.md) — extended usage notes
  > Position in flow · Activation · Input formats accepted · Routing table · Prerequisites · Examples · Non-negotiables · Error handling
- `/amw-ascii-to-svg` — user-facing command that invokes this skill
