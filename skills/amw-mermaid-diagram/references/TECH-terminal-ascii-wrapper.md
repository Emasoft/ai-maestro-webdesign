---
name: TECH-terminal-ascii-wrapper
category: mermaid-grammar
source: diagrams-skills/agent-skill-diagramming-flows-main/SKILL.md
also-in: diagrams-skills/agent-skill-diagramming-flows-main/render.ts
---

# Terminal ASCII authoring — Bun-style one-liner

## What it does

A minimal Bun/TypeScript CLI that accepts a Mermaid source string and
prints ASCII directly to stdout. Zero build step, no flags to
configure — meant to be invoked inside agent conversations when the
user wants a diagram in the terminal *now*.

## When to use

- Planning-mode diagrams during agent conversations.
- One-shot terminal visualization without writing a `.mmd` file.
- Piping Mermaid source through a shell pipeline.

## The minimal wrapper

```typescript
// source: diagrams-skills/agent-skill-diagramming-flows-main/render.ts
#!/usr/bin/env bun

import { renderMermaidAscii } from "beautiful-mermaid";

async function readStdin(): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of Bun.stdin.stream()) {
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString("utf-8").trim();
}

async function main() {
  const args = process.argv.slice(2);
  let diagram = args.find(a => !a.startsWith("--")) || "";

  if (!diagram) {
    const isTTY = process.stdin.isTTY;
    if (!isTTY) diagram = await readStdin();
  }

  try {
    const output = renderMermaidAscii(diagram, { paddingX: 5, paddingY: 5 });
    console.log(output);
  } catch (err) {
    console.error("render error:", err instanceof Error ? err.message : err);
    process.exit(1);
  }
}
main();
```

## Usage patterns

```bash
# source: diagrams-skills/agent-skill-diagramming-flows-main/SKILL.md

# Pass as argument
bun run render.ts "graph LR
A --> B --> C"

# Pipe from stdin
echo "graph LR; A --> B" | bun run render.ts

# With padding override
bun run render.ts --padding-x 3 "graph TD; A --> B"
```

## The key convention — newlines not semicolons

```
✓ "graph LR\nA --> B\nB --> C"        Newlines — reliable across all grammars
✗ "graph LR; A --> B; B --> C"         Semicolons — works in flowcharts only
```

## Gotchas

- Requires Bun (`bun >= 1.0`) — Node.js doesn't have `Bun.stdin.stream()`.
  Port to Node with `process.stdin.on('data', ...)`.
- Single-argument mode only reads one positional — extra args are
  ignored silently.
- Piping through shells can mangle escape sequences — use a heredoc:
  `cat <<EOF | bun run render.ts` ... `EOF`.

## Cross-references

- `../../amw-mermaid-render/references/TECH-ascii-render-api.md` — the
  library function this wraps.
- `../../amw-mermaid-render/references/TECH-ascii-padding-options.md` —
  why the defaults (5, 5) were chosen.
- `../../amw-mermaid-render/` — the full-featured plugin skill with batch
  support and more flags.
- [`../SKILL.md`](../SKILL.md) — parent skill

