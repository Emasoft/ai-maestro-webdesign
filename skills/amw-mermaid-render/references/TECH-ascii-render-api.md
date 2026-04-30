---
name: TECH-ascii-render-api
category: mermaid-render-ascii
source: diagrams-skills/beautiful-mermaid-main/references/ascii-rendering.md
also-in: diagrams-skills/Pretty-mermaid-skills-main/SKILL.md, diagrams-skills/agent-skill-diagramming-flows-main/SKILL.md
---

# `renderMermaidAscii()` — Mermaid → ASCII / Unicode

## What it does

Synchronous function that renders Mermaid source as plain-text box-drawing
art — `+---+`, `|`, `>`. Output is terminal-safe, markdown-safe, and works
in any environment that can print UTF-8 or ASCII.

## When to use

- Terminal output, CI logs, READMEs, CHANGELOGs.
- Environments without graphics (email, plain text files, screen
  readers).
- Quick previews during iterative authoring — 10× faster than spawning a
  browser to render SVG.

## How it works

Walks the same parsed Mermaid AST that `renderMermaid()` uses, then
packs nodes into a character grid using width/height hints. All five
Mermaid grammar types (flowchart, sequence, state, class, ER) are
supported.

## Minimal example

```typescript
// source: diagrams-skills/beautiful-mermaid-main/references/ascii-rendering.md
import { renderMermaidAscii } from 'beautiful-mermaid'

const ascii = renderMermaidAscii(`graph LR; A --> B --> C`)
// +-----+     +-----+     +-----+
// |  A  |---->|  B  |---->|  C  |
// +-----+     +-----+     +-----+
```

Options: `useAscii` (default `false` — Unicode), `paddingX` (5),
`paddingY` (5), `boxBorderPadding` (1).

## Gotchas

- `useAscii: false` and `useAscii: true` look near-identical in the
  current library — both use ASCII-compatible characters. The flag is
  forward-compatible for a future Unicode-only mode.
- Output width is **not** clamped to 78 cols — wide diagrams overflow
  the terminal. Use tight `paddingX: 2, boxBorderPadding: 0` when
  rendering for narrow contexts.
- Not a substitute for perfect-ASCII (`bin/amw-ascii-render.py`) — that
  tool renders from structured JSON and guarantees alignment; this
  renders from Mermaid grammar and prioritizes shape fidelity.

## Cross-references

- `TECH-ascii-padding-options.md` — tuning horizontal/vertical spacing.
- `TECH-svg-render-api.md` — the async SVG cousin.
- `TECH-ascii-markdown-integration.md` — wrapping output in fenced code blocks.
- [`../SKILL.md`](../SKILL.md) — parent skill

