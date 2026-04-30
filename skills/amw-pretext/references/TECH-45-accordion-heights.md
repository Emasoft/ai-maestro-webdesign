---
name: TECH-45-accordion-heights
category: motion
source: pretext-skills/amw-pretext-frontend-motion-main/core/bundle/references/demo-family-map.md
also-in: SKILL-15.md (accordion.ts demo), pretext-frontend-motion-main (Accordion family)
---

# Accordion panel height (expand/collapse with known height)

**Category:** motion
**Status:** stable

## What it does

Expand/collapse text panels where the expanded height is KNOWN before paint. `prepare()` + `layout()` compute the target height; CSS transitions from `0` (collapsed) to that exact px value — no `height: auto` flicker, no scrollHeight read that triggers reflow.

## When to use

- FAQ accordions
- Settings panels with long help text
- Collapsible card body

## How it works

```ts
// Source: pretext-frontend-motion-main demo-family-map.md — Accordion family
const prepared = prepare(panelText, font)
const { height } = layout(prepared, panelWidth, lineHeight)
panel.style.setProperty('--expanded-height', `${height}px`)
// CSS: .panel { max-height: 0 } .panel.open { max-height: var(--expanded-height) }
```

## Minimal example

```css
.panel { max-height: 0; transition: max-height 0.3s ease-out; overflow: hidden }
.panel.open { max-height: var(--expanded-height) }
```

## Gotchas

- Account for internal padding/gap in the target height.
- Re-compute on viewport width change — `ResizeObserver` + re-run `layout()`.
- Prefer `max-height` over `height` transitions for easier animate-in.

## Cross-references

- Related: TECH-03-layout, TECH-30-layout-shift-prevention
- API reference: [TECH-03-layout](TECH-03-layout.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
