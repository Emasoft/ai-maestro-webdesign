---
name: TECH-59-react-hooks-integration
category: integrate
source: pretext-skills/amw-pretext-integrate/SKILL.md
also-in: use-pretext/SKILL.md, SKILL-21.md, pretext-frontend-motion-main/references/react-migration.md, pretext-ui-claude-skills-main/SKILL.md
---

# React hook integration (useMemo prepared handles)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** integrate
**Status:** stable

## What it does

Wrap `prepare()` / `prepareWithSegments()` in `useMemo` keyed by `[text, font, options]` so the prepared handle survives re-renders and is only recomputed when measurement inputs actually change. Call `layout()` in the render body — it's pure arithmetic and safe to run every render.

## When to use

- Any React component measuring text
- Virtualized lists / masonry grids / chat bubbles

## How it works

```tsx
// Source: pretext-integrate/SKILL.md Path A
const prepared = useMemo(
  () => items.map(item => prepare(item.text, FONT)),
  [items]
)
// In render:
function getItemHeight(index, containerWidth) {
  return layout(prepared[index], containerWidth, LINE_HEIGHT).height
}
```

## Minimal example

```tsx
// Source: pretext-frontend-motion-main/references/react-migration.md
const preparedRef = useRef(null)
useEffect(() => {
  preparedRef.current = prepareWithSegments(text, font)
}, [text, font])
const height = useMemo(
  () => preparedRef.current ? layout(preparedRef.current, width, lh).height : 0,
  [width, lh, preparedRef.current]
)
```

## Gotchas

- `prepare()` inside `useEffect` runs AFTER render — first paint uses stale heights. Reserve space via placeholder or `key` tricks.
- Do NOT measure rendered text nodes with `getBoundingClientRect` — that defeats the purpose.
- For SSR / Next.js, gate the prepare call with `typeof document !== 'undefined'`.

## Cross-references

- Related: TECH-01-prepare-basics, TECH-60-svelte-islands-integration
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
  > What it does · When to use · How it works · Minimal example · Configuration options (source: pretext-skill-master/SKILL.md) · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
