---
name: TECH-mono-mode
category: mermaid-theme
source: diagrams-skills/beautiful-mermaid-main/references/themes.md
also-in: diagrams-skills/Pretty-mermaid-skills-main/references/THEMES.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Mono Mode — 2-color theme foundation

## What it does

Derives every diagram color from only `bg` (background) and `fg`
(foreground). The other five tokens — line, accent, muted, surface,
border — are computed via `color-mix()` blends, ensuring visual
harmony with zero manual tuning.

## When to use

- **Default** for every theme unless you explicitly need finer control.
- Brand integrations where you only know the two primary colors.
- Pairing with a VS Code theme via `fromShikiTheme()` — that helper
  emits the same 2-color shape.

## How it works

```
Text (primary)  = fg @ 100%
Text (secondary)= fg @ 60% into bg
Edge labels     = fg @ 40% into bg
Connectors      = fg @ 30% into bg
Arrow heads     = fg @ 50% into bg
Node fill       = fg @  3% into bg
Node stroke     = fg @ 20% into bg
```

Blending uses CSS `color-mix(in srgb, var(--fg) X%, var(--bg))`.

## Minimal example

```typescript
// source: diagrams-skills/beautiful-mermaid-main/references/themes.md
const svg = await renderMermaid(diagram, {
  bg: '#1a1b26',  // Background
  fg: '#a9b1d6'   // Foreground
})
// Everything else auto-derives.
```

## Gotchas

- Contrast — if `fg` and `bg` are too close in luminance, secondary
  text vanishes. Aim for >= 4:1 contrast between the two.
- `color-mix()` is CSS 5 — IE11 and very old mobile Safari don't
  support it; the library's fallbacks substitute fixed hex values, but
  live theme switching stops working in those browsers.
- Mono Mode overrides a theme only if you pass `bg` AND `fg`. Passing
  only `bg` (or only `fg`) is an error shape — don't do it.

## Cross-references

- [TECH-enriched-mode](TECH-enriched-mode.md) — override specific derived tokens.
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-built-in-themes](TECH-built-in-themes.md) — the 15 pre-baked background/foreground color pairs.
  > What it does · When to use · The full 15 · Recommended defaults · Minimal example · Gotchas · Cross-references
- [TECH-shiki-theme-import](TECH-shiki-theme-import.md) — map a VS Code theme to a Mono Mode pair.
  > What it does · When to use · Shiki → diagram token mapping · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
