---
name: TECH-ascii-markdown-integration
category: mermaid-render-ascii
source: diagrams-skills/beautiful-mermaid-main/references/ascii-rendering.md
also-in: diagrams-skills/beautiful-mermaid-main/SKILL.md
---

# Wrapping ASCII output for Markdown

## What it does

Patterns for embedding `renderMermaidAscii()` output into Markdown,
READMEs, CHANGELOGs — anywhere the fenced code block semantics apply.

## When to use

- Generating a README's architecture section from a `.mmd` source.
- Writing CHANGELOG entries that include "before/after" diagrams.
- Shipping documentation that must remain readable on npm's package
  page (which renders plain text from the README with limited CSS).

## Pattern 1: plain fenced block

```typescript
// source: diagrams-skills/beautiful-mermaid-main/references/ascii-rendering.md
const ascii = renderMermaidAscii(diagram)
const markdown = `## System Architecture

\`\`\`
${ascii}
\`\`\`
`
```

The three-backtick fence with no language tag keeps the ASCII art
monospaced across every Markdown renderer.

## Pattern 2: inline compact diagram

For small flows, skip the fenced block and use a tight-padding call:

```typescript
// source: diagrams-skills/beautiful-mermaid-main/references/ascii-rendering.md
const simple = renderMermaidAscii('graph LR; A --> B', {
  paddingX: 2,
  boxBorderPadding: 0
})
```

Embed inline inside a prose paragraph wrapped in `<pre>`.

## Pattern 3: ASCII mode for email / plain text

```typescript
const ascii = renderMermaidAscii(diagram, { useAscii: true })
// Maximum terminal compatibility — no Unicode risk.
```

## Gotchas

- npm's package-page README renderer strips some Unicode box-drawing
  characters on older CDN caches — use `useAscii: true` when
  publishing to npm.
- GitHub renders fenced blocks with syntax highlighting; a `mermaid`
  language tag would try to *render the source*, not show the ASCII
  art. Use no language tag, or `text`.
- Long ASCII diagrams wrap on mobile — cap your rendered width to
  60-70 cols by tightening `paddingX`.

## Cross-references

- [TECH-ascii-render-api](TECH-ascii-render-api.md) — the renderer function.
- [TECH-ascii-padding-options](TECH-ascii-padding-options.md) — tuning for width-constrained output.
- [TECH-terminal-output-ansi](TECH-terminal-output-ansi.md) — ANSI color escape codes on top of
  plain ASCII.
- [`../SKILL.md`](../SKILL.md) — parent skill

