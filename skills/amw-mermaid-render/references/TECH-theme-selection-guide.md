---
name: TECH-theme-selection-guide
category: mermaid-theme
source: diagrams-skills/beautiful-mermaid-main/references/themes.md
also-in: diagrams-skills/Pretty-mermaid-skills-main/references/THEMES.md
---

# Theme selection decision tree

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Decision tree](#decision-tree)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

A short decision tree that maps user context to one of the 15 built-in
themes. Use it when the caller says "pick a good one" instead of
naming a theme.

## When to use

- First-time users who don't know the 15 theme names.
- Batch rendering — picking one theme for 20 diagrams in a folder.
- Generating documentation — you need a default that works across
  readers' device themes.

## Decision tree

```
Dark or light mode?
├── Light
│   ├── General purpose       → zinc-light ⭐
│   ├── GitHub README feel    → github-light
│   ├── Solarized feel        → solarized-light
│   ├── Ice-blue mood         → nord-light
│   ├── Violet/purple mood    → catppuccin-latte
│   └── Soft Japanese mood    → tokyo-night-light
│
└── Dark
    ├── Universal default     → tokyo-night ⭐
    ├── Classic retro dark    → dracula ⭐
    ├── Minimal / pure        → zinc-dark
    ├── Nordic / cool         → nord
    ├── Warm / comforting     → catppuccin-mocha
    ├── GitHub feel           → github-dark
    ├── OLED-friendly very    → tokyo-night-storm
    │   dark
    ├── Academic precision    → solarized-dark
    └── Atom One Dark         → one-dark
```

**Context-to-theme cheat table**

| Context | Recommended |
|---------|-------------|
| Light documentation | `zinc-light`, `github-light` |
| Dark documentation | `github-dark`, `zinc-dark` |
| Terminal output | `tokyo-night`, `dracula` |
| Print-friendly | `zinc-light`, `solarized-light` |
| High contrast | Custom with increased `fg/bg` difference |
| Brand matching | Custom theme with brand colors |

## Minimal example

```bash
# source: diagrams-skills/Pretty-mermaid-skills-main/SKILL.md
# When the user says "dark docs"
node scripts/render.mjs -i diagram.mmd -o out.svg -t tokyo-night

# When the user says "print this"
node scripts/render.mjs -i diagram.mmd -o out.svg -t zinc-light
```

## Gotchas

- "Bright" is not a theme choice — it biases the user toward
  `dracula`, but `dracula` is dark. Re-read the user's mood word:
  "bright" often means "high contrast light" → `zinc-light`.
- Some themes render arrows almost invisible on first impression
  (`nord`, `catppuccin-mocha`) — if the user asks for "legible
  arrows", boost `accent` via Enriched Mode instead of switching
  themes.

## Cross-references

- [TECH-built-in-themes](TECH-built-in-themes.md) — the full catalog.
  > What it does · When to use · The full 15 · Recommended defaults · Minimal example · Gotchas · Cross-references
- [TECH-enriched-mode](TECH-enriched-mode.md) — when the chosen theme is 80% right and
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  needs one tweak.
- [TECH-mono-mode](TECH-mono-mode.md) — when no pre-baked theme fits at all.
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

