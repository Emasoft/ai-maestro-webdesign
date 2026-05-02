---
name: TECH-built-in-themes
category: mermaid-theme
source: diagrams-skills/beautiful-mermaid-main/references/themes.md
also-in: diagrams-skills/Pretty-mermaid-skills-main/references/THEMES.md
---

# `THEMES[...]` — 15 pre-baked theme objects

## What it does

Exports a `THEMES` dictionary keyed by theme name. Each value is a
Mono-Mode-compatible object (`bg`, `fg`, sometimes `accent`). Pick one
and pass it straight into `renderMermaid()`.

## When to use

- You don't have a brand palette and want something that "just looks
  nice" in dark mode.
- Pairing diagrams to an editor theme (tokyo-night, dracula,
  github-dark) so docs feel consistent with screenshots.
- Print-friendly output — pick `zinc-light` or `solarized-light`.

## The full 15

**Light:** `zinc-light`, `tokyo-night-light`, `catppuccin-latte`,
`nord-light`, `github-light`, `solarized-light`

**Dark:** `zinc-dark`, `tokyo-night`, `tokyo-night-storm`,
`catppuccin-mocha`, `nord`, `dracula`, `github-dark`,
`solarized-dark`, `one-dark`

## Recommended defaults

| Context | Theme |
|---------|-------|
| Dark docs | `tokyo-night` |
| Light docs | `github-light` |
| Terminal | `dracula` |
| Print | `zinc-light` |

## Minimal example

```typescript
// source: diagrams-skills/beautiful-mermaid-main/references/themes.md
import { renderMermaid, THEMES } from 'beautiful-mermaid'

const svg = await renderMermaid(diagram, THEMES['tokyo-night'])
```

## Gotchas

- Keys are case-sensitive. `THEMES['Tokyo-Night']` is `undefined`.
- Some dark themes derive `fg` automatically (`zinc-dark`, `nord`,
  `one-dark`) — you can't reliably query `THEMES['zinc-dark'].fg`
  because the library computes it on use.
- Shipping as `tokyo-night` but users asking for "tokyonight" — do a
  fuzzy lookup or normalize input before key access.

## Cross-references

- [TECH-theme-selection-guide](TECH-theme-selection-guide.md) — human-readable decision tree.
- [TECH-mono-mode](TECH-mono-mode.md) — what makes a theme work with two colors.
- [TECH-shiki-theme-import](TECH-shiki-theme-import.md) — import any VS Code theme on demand.
- [`../SKILL.md`](../SKILL.md) — parent skill

