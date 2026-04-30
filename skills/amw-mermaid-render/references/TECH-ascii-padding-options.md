---
name: TECH-ascii-padding-options
category: mermaid-render-ascii
source: diagrams-skills/beautiful-mermaid-main/references/ascii-rendering.md
also-in: diagrams-skills/Pretty-mermaid-skills-main/SKILL.md, diagrams-skills/agent-skill-diagramming-flows-main/SKILL.md
---

# `paddingX` / `paddingY` / `boxBorderPadding`

## What it does

Three tuning knobs on `renderMermaidAscii()` that control horizontal
node spacing, vertical node spacing, and the inner padding of each
text box.

## When to use

- Compact output for inline docs (`paddingX: 2, boxBorderPadding: 0`).
- Spacious output for standalone ASCII diagrams in a terminal
  (`paddingX: 10`).
- Narrow terminal windows — tighten padding to keep diagrams under 80
  cols.

## Defaults

```
paddingX:         5   // horizontal gap between nodes
paddingY:         5   // vertical gap between nodes
boxBorderPadding: 1   // interior padding inside box borders
```

## What each one does

```
boxBorderPadding: 0 → |A|
boxBorderPadding: 1 → | A |       (default)
boxBorderPadding: 2 → |  A  |
```

```
paddingX: 2  → +---+  +---+       (compact horizontal)
               | A |--| B |
               +---+  +---+

paddingX: 10 → +---+          +---+   (spacious horizontal)
               | A |--------->| B |
               +---+          +---+
```

## Minimal example

```typescript
// source: diagrams-skills/beautiful-mermaid-main/references/ascii-rendering.md
const inline = renderMermaidAscii(diagram, {
  paddingX: 2,
  boxBorderPadding: 0
})
// Output suitable for embedding inside narrow markdown columns
```

## Gotchas

- Tight padding (`paddingX: 0`) merges nodes visually and can break
  arrow routing — the library clamps to a minimum internally, don't
  rely on zero being zero.
- Padding is in **character cells**, not pixels. A `paddingY: 2` gap
  looks huge in a terminal but tiny in a Markdown-rendered code block
  on a retina screen.
- `paddingX` + `paddingY` do NOT affect label text wrapping — long
  node labels still blow up box widths. Use `<br>` inside node labels
  if you want wrapping.

## Cross-references

- `TECH-ascii-render-api.md` — the parent function.
- `TECH-ascii-markdown-integration.md` — wrapping output for markdown
  rendering contexts.
- `bin/amw-mermaid-render.sh` — the shell CLI that accepts `--padding-x`.
- [`../SKILL.md`](../SKILL.md) — parent skill

