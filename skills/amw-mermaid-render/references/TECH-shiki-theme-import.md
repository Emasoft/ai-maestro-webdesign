---
name: TECH-shiki-theme-import
category: mermaid-theme
source: diagrams-skills/beautiful-mermaid-main/references/themes.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Shiki → diagram token mapping](#shiki-diagram-token-mapping)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# `fromShikiTheme()` — import any VS Code theme

## What it does

Takes a loaded Shiki theme object and maps its token colors onto the
Mono Mode / Enriched Mode shape. The returned object plugs straight
into `renderMermaid()`.

## When to use

- You want diagrams to match your actual editor theme 1:1.
- Pairing diagram output with Shiki-highlighted code blocks on the
  same page — both renderers share the same palette.
- Shipping a UI that already bundles Shiki — no extra theme catalog
  needed.

## Shiki → diagram token mapping

| VS Code token | Diagram role |
|---------------|--------------|
| `editor.background` | `bg` |
| `editor.foreground` | `fg` |
| `editorLineNumber.foreground` | `muted` |
| `focusBorder` | `accent` |
| `editorWidget.background` | `surface` |
| `editorWidget.border` | `border` |

## Minimal example

```typescript
// source: diagrams-skills/beautiful-mermaid-main/references/themes.md
import { getSingletonHighlighter } from 'shiki'
import { renderMermaid, fromShikiTheme } from 'beautiful-mermaid'

const highlighter = await getSingletonHighlighter({
  themes: ['vitesse-dark']
})
const colors = fromShikiTheme(highlighter.getTheme('vitesse-dark'))
const svg = await renderMermaid(diagram, colors)
```

## Gotchas

- Shiki themes don't always define every token — `editorWidget.*` is
  optional. Missing tokens fall through to Mono Mode derivation.
- Theme file format matters — JSON themes work; TMLanguage `.tmTheme`
  needs Shiki's converter first.
- `getSingletonHighlighter()` is async and expensive — cache the
  highlighter if rendering many diagrams.

## Cross-references

- [TECH-built-in-themes](TECH-built-in-themes.md) — pre-baked alternatives when Shiki is overkill.
  > What it does · When to use · The full 15 · Recommended defaults · Minimal example · Gotchas · Cross-references
- [TECH-enriched-mode](TECH-enriched-mode.md) — the option shape Shiki's output conforms to.
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-live-theme-switch](TECH-live-theme-switch.md) — runtime theme changes without re-rendering.
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
