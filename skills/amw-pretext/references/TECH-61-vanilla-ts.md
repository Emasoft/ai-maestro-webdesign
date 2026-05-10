---
name: TECH-61-vanilla-ts
category: integrate
source: pretext-skills/amw-pretext-frontend-motion-main/references/capabilities.md
also-in: SKILL-15.md, SKILL-17.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Vanilla TypeScript integration (no framework)

**Category:** integrate
**Status:** stable

## What it does

Pretext's cleanest integration path: vanilla TS + Canvas for demos / one-offs / editorial pages / showcase pieces. No framework overhead, no re-render cost, `prepare()` at module scope, `layout()` in a `requestAnimationFrame` loop or `ResizeObserver` callback. Pretext-frontend-motion's "Default Technical Shape" recommends this for all new demos.

## When to use

- Standalone interactive pages
- Editorial one-offs
- Canvas-heavy experiments
- Teaching / learning pretext patterns

## How it works

```ts
// Source: pretext-frontend-motion-main/references/capabilities.md Default Technical Shape
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'
const FONT = '18px Georgia'
const LINE_HEIGHT = 28
let prepared = null  // module-scope cache
async function init() {
  await document.fonts.ready
  prepared = prepareWithSegments(document.querySelector('#source').textContent, FONT)
  new ResizeObserver(() => render(canvas.width)).observe(canvas)
  render(canvas.width)
}
function render(w) {
  const { lines } = layoutWithLines(prepared, w, LINE_HEIGHT)
  ctx.clearRect(0, 0, w, canvas.height)
  lines.forEach((l, i) => ctx.fillText(l.text, 0, i * LINE_HEIGHT))
}
```

## Minimal example

```html
<canvas id="c"></canvas>
<script type="module">
  import { prepare, layout } from 'https://esm.sh/@chenglou/pretext'
  // ... simple page code
</script>
```

## Gotchas

- `type="module"` is a natural progressive-enhancement gate.
- No framework = no re-render — place event listeners/observers directly on the DOM elements.

## Cross-references

- Related: TECH-59-react-hooks-integration, TECH-60-svelte-islands-integration, TECH-63-progressive-enhancement
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
  > What it does · When to use · How it works · Minimal example · Configuration options (source: pretext-skill-master/SKILL.md) · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
