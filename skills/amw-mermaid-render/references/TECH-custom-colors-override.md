---
name: TECH-custom-colors-override
category: mermaid-render-svg
source: diagrams-skills/Pretty-mermaid-skills-main/SKILL.md
also-in: diagrams-skills/Pretty-mermaid-skills-main/scripts/render.mjs
---

# CLI color overrides — per-invocation theming

## What it does

The Pretty-mermaid CLI lets you pass seven optional `--color-name` flags
that override any theme's tokens. Handy when you've picked a built-in
theme but want to tweak one or two colors without defining a new
theme object.

## When to use

- Demo-grade customization — "show the same flowchart in brand
  colors" without editing source.
- CI build step that injects brand hex values at build time.
- Transparent-background output so the same diagram works in
  dark-mode and light-mode docs.

## The seven override flags

```
--bg      Background color (hex)
--fg      Foreground color (hex)
--line    Edge/connector color
--accent  Arrow heads, highlights
--muted   Secondary text, labels
--surface Node fill tint
--border  Node stroke
--font    Font family (default: Inter)
--transparent      SVG only — strip bg, emit transparent
```

## Minimal example

```bash
# source: diagrams-skills/Pretty-mermaid-skills-main/SKILL.md
node scripts/render.mjs \
  --input diagram.mmd \
  --bg "#1a1b26" \
  --fg "#a9b1d6" \
  --accent "#7aa2f7" \
  --output custom.svg
```

```bash
# Transparent, brand font
node scripts/render.mjs \
  --input diagram.mmd \
  --transparent \
  --font "JetBrains Mono" \
  --output transparent.svg
```

## Gotchas

- Override flags **override** the theme — don't pass both
  `--theme tokyo-night` and `--bg "#000"` expecting some kind of
  merge. `--bg` wins.
- `--transparent` + `--bg` is inconsistent — `--transparent` implies
  no background, so `--bg` is ignored. Don't ship both.
- Hex values must be quoted in shells — `--bg #000000` expands `#` as a
  comment in some shells. Use `--bg "#000000"`.

## Cross-references

- `TECH-enriched-mode.md` — the programmatic equivalent for Node/TS.
- `TECH-built-in-themes.md` — when you'd rather NOT handcraft every token.
- `bin/amw-mermaid-render.sh` — the plugin-shipped shell wrapper.
- [`../SKILL.md`](../SKILL.md) — parent skill

