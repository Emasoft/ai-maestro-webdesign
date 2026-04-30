---
name: TECH-live-theme-switch
category: mermaid-theme
source: diagrams-skills/beautiful-mermaid-main/SKILL.md
also-in: diagrams-skills/beautiful-mermaid-main/references/themes.md
---

# Live theme switching — CSS custom properties

## What it does

The SVG that `renderMermaid()` emits declares its palette as CSS
custom properties on the root `<svg>` element. Overriding them at
runtime switches the entire diagram's colors **without re-rendering**.

## When to use

- Dark/light toggle in a website — flip one attribute on the `<html>`
  root, let child SVGs inherit.
- Interactive theme picker — update `--bg`/`--fg` on hover/click.
- Matching a user's OS preference via `prefers-color-scheme`.

## How it works

Emitted SVG carries:
```css
svg {
  --bg: #ffffff;
  --fg: #27272a;
  --line: /* derived */;
  --accent: /* derived */;
  --muted: /* derived */;
  --surface: /* derived */;
  --border: /* derived */;
}
```
All internal strokes, fills, and text references use
`color-mix(in srgb, var(--fg) N%, var(--bg))` — so overriding the
two source variables cascades through the whole SVG.

## Minimal example

```javascript
// source: diagrams-skills/beautiful-mermaid-main/SKILL.md
const svgElement = document.querySelector('svg.mermaid-diagram')

// Switch to tokyo-night
svgElement.style.setProperty('--bg', '#1a1b26')
svgElement.style.setProperty('--fg', '#a9b1d6')

// Switch to github-light
svgElement.style.setProperty('--bg', '#ffffff')
svgElement.style.setProperty('--fg', '#27272a')
```

## Gotchas

- The SVG must be inlined (`<svg>...</svg>` in the DOM). `<img src="…svg">`
  isolates the SVG's CSS scope — custom property overrides from the
  host page don't reach into it.
- If the library ever drops `color-mix()` fallback (older browsers),
  runtime switching silently fails but the SVG keeps showing the last
  computed color. Test the browser matrix.
- Switching only `--accent` (not `--bg`/`--fg`) works, but most
  derived tokens ignore it — better to re-render if you want many
  tokens to change.

## Cross-references

- `TECH-mono-mode.md` — the derivation rules the CSS custom properties implement.
- `TECH-enriched-mode.md` — which tokens exist to override.
- `TECH-svg-render-api.md` — the function that emits these properties.
- [`../SKILL.md`](../SKILL.md) — parent skill

