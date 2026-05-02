---
name: TECH-terminal-output-ansi
category: mermaid-render-ascii
source: diagrams-skills/beautiful-mermaid-main/references/ascii-rendering.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Pattern 1: Highlight node names](#pattern-1-highlight-node-names)
- [Pattern 2: Whole-diagram color wrap](#pattern-2-whole-diagram-color-wrap)
- [Pattern 3: Per-node status colors](#pattern-3-per-node-status-colors)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Adding ANSI colors to ASCII output

## What it does

Patterns for layering ANSI 256-color or TrueColor escape codes on top
of the plain-text output from `renderMermaidAscii()`. The renderer
itself emits pure ASCII — color is an optional post-processing step.

## When to use

- CI logs where you want failed-step diagrams highlighted red.
- Developer tools that print diagrams in the terminal and want to
  match the editor's theme palette.
- Highlighting one node in a larger flow (e.g. "the step that
  errored").

## Pattern 1: Highlight node names

```typescript
// source: diagrams-skills/beautiful-mermaid-main/references/ascii-rendering.md
const ascii = renderMermaidAscii(diagram)

// Wrap text between pipes in cyan
const colored = ascii.replace(/\|([^|]+)\|/g, '|\x1b[36m$1\x1b[0m|')
console.log(colored)
```

## Pattern 2: Whole-diagram color wrap

```typescript
const ascii = renderMermaidAscii(diagram)
console.log(`\x1b[2m${ascii}\x1b[0m`) // dim the whole thing
```

## Pattern 3: Per-node status colors

```typescript
const ascii = renderMermaidAscii(diagram)
const coloredByStatus = ascii
  .replace(/\|( OK [^|]*)\|/g,   '|\x1b[32m$1\x1b[0m|') // green
  .replace(/\|( FAIL [^|]*)\|/g, '|\x1b[31m$1\x1b[0m|') // red
  .replace(/\|( WAIT [^|]*)\|/g, '|\x1b[33m$1\x1b[0m|') // yellow
```

## Gotchas

- ANSI escape codes break Markdown rendering — don't dump colored
  output into a file a reader will open. Write uncolored ASCII to
  disk, color only when printing to stdout of an interactive terminal.
- `process.stdout.isTTY` check — many CI environments pretend to be
  non-interactive; respect `NO_COLOR` env var if set.
- TrueColor (`\x1b[38;2;R;G;Bm`) isn't universal — fall back to
  256-color or standard 16 for older terminals.

## Cross-references

- [TECH-ascii-render-api](TECH-ascii-render-api.md) — produces the input text.
- [TECH-ascii-markdown-integration](TECH-ascii-markdown-integration.md) — the NO-color cousin for
  persistent Markdown output.
- [`../SKILL.md`](../SKILL.md) — parent skill

