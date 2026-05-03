---
name: TECH-enriched-mode
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


# Enriched Mode — override specific derived tokens

## What it does

Lets you hand-pick any subset of the five derived tokens (`line`,
`accent`, `muted`, `surface`, `border`) while still using Mono Mode
for the rest. Every field is optional — whatever you don't set falls
back to the `bg/fg` derivation rules.

## When to use

- Brand integration where one token needs a specific hex (e.g. the
  brand's exact accent arrow color).
- Custom themes that derive from more than two brand colors.
- Polishing a near-final theme where Mono Mode got 90% there but the
  arrowhead color feels wrong.

## How it works

Merge-on-top semantics: the options object's explicit fields win; the
missing fields are computed via Mono Mode's blend rules against
`bg/fg`.

## Minimal example

```typescript
// source: diagrams-skills/beautiful-mermaid-main/references/themes.md
const svg = await renderMermaid(diagram, {
  bg: '#1a1b26',
  fg: '#a9b1d6',
  line: '#565f89',      // Edge/connector color
  accent: '#7aa2f7',    // Arrow heads, highlights
  muted: '#565f89',     // Secondary text, labels
  surface: '#24283b',   // Node fill tint
  border: '#414868'     // Node stroke
})
```

## Gotchas

- Overriding `accent` but leaving `muted` derived can produce a
  mismatched palette where the arrowhead pops but the secondary text
  feels faded. If you set `accent`, audit `muted` too.
- `surface` is only used by filled node shapes (`[[...]]`, `([...])`).
  Setting it does nothing for a diagram made of plain `[rect]` nodes.
- Don't try to "go partial" (pass only one token and no `bg/fg`) —
  `bg` and `fg` are always required.

## Cross-references

- [TECH-mono-mode](TECH-mono-mode.md) — the fall-through rules.
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-built-in-themes](TECH-built-in-themes.md) — pre-baked palettes that use this shape.
  > What it does · When to use · The full 15 · Recommended defaults · Minimal example · Gotchas · Cross-references
- [TECH-theme-selection-guide](TECH-theme-selection-guide.md) — when to even reach for Enriched Mode.
  > What it does · When to use · Decision tree · Context-to-theme cheat table · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

