---
name: TECH-66-resize-observer-pattern
category: integrate
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-21.md, use-pretext/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# ResizeObserver pattern (re-layout, not re-prepare)

**Category:** integrate
**Status:** stable

## What it does

On container resize, ONLY call `layout()` (or `layoutWithLines`, etc.) — NEVER call `prepare()`. The canonical resize handler pattern: `ResizeObserver` → `layout()` → apply new height/width. Re-preparing on every resize defeats the main pretext performance win.

## When to use

- Every project using pretext — this is how you handle reflow

## How it works

```ts
// Source: pretext-text-measurement/SKILL.md — Resize Handler Pattern
let prepared = prepareWithSegments(text, '16px Inter')
function onResize(containerWidth) {
  const { lines } = layoutWithLines(prepared, containerWidth, 24)
  renderLines(lines)
}
new ResizeObserver(e => onResize(e[0].contentRect.width)).observe(container)
function onTextChange(newText) {
  prepared = prepareWithSegments(newText, '16px Inter')
  onResize(currentWidth)
}
```

## Minimal example

```ts
// Source: use-pretext/SKILL.md — Masonry recipe
const ro = new ResizeObserver(entries => {
  positioned = computeLayout(entries[0].contentRect.width)
})
ro.observe(containerEl)
```

## Gotchas

- `ResizeObserver` fires async; first layout may be stale by one frame (acceptable).
- Disconnect the observer in cleanup to prevent leaks.

## Cross-references

- Related: TECH-03-layout, TECH-59-react-hooks-integration
- API reference: [TECH-03-layout](TECH-03-layout.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
