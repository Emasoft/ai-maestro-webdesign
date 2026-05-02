---
name: TECH-svg-render-api
category: mermaid-render-svg
source: diagrams-skills/beautiful-mermaid-main/SKILL.md
also-in: diagrams-skills/Pretty-mermaid-skills-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# `renderMermaid()` — Mermaid → SVG

## What it does

Async function that takes a Mermaid diagram text and returns an SVG string.
The SVG carries seven CSS custom properties (`--bg`, `--fg`, `--line`,
`--accent`, `--muted`, `--surface`, `--border`) so hosts can re-theme it
without re-rendering.

## When to use

- Documentation, blog posts, MDX, static-site generators — any place an
  SVG tag can live.
- You need a themable, zoomable vector diagram — not a raster image.
- Live theme switching in the browser (toggle `--bg`/`--fg` on the node).

## How it works

Wraps the underlying `mermaid` npm package, then post-processes the
emitted SVG: strips the default white background, replaces hard-coded
hex colors with CSS custom property references, and injects an
`@import url(...)` for Inter.

## Minimal example

```typescript
// source: diagrams-skills/beautiful-mermaid-main/SKILL.md
import { renderMermaid } from 'beautiful-mermaid'

const svg = await renderMermaid(`
  graph LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
`)
```

Full option set: `bg`, `fg`, `font`, `transparent`, `line`, `accent`,
`muted`, `surface`, `border`.

## Gotchas

- Empty SVG output → Mermaid syntax invalid. Test at mermaid.live first.
- Fonts not rendering → the `@import` line fetches Inter from Google
  Fonts; strip the line for offline/CSP-strict embedding and let
  `system-ui` take over.
- `renderMermaid()` is **async** — always `await` it. The sibling
  `renderMermaidAscii()` is sync; don't mix them up.

## Cross-references

- [TECH-ascii-render-api](TECH-ascii-render-api.md) — the sync ASCII cousin.
- [TECH-mono-mode](TECH-mono-mode.md) — the 2-color theming foundation.
- `bin/amw-mermaid-render.sh` — the shell entrypoint used by every other
  plugin skill that needs Mermaid SVG.
- [`../SKILL.md`](../SKILL.md) — parent skill

