---
name: TECH-67-masonry-grid
category: workflow
source: pretext-skills/amw-pretext-frontend-motion-main/core/bundle/references/demo-family-map.md
also-in: SKILL-15.md (masonry/index.ts), use-pretext/SKILL.md Recipe 1, pretext-integrate/SKILL.md Path A
---

# Masonry grid (Pinterest-style variable card heights)

**Category:** workflow
**Status:** stable

## What it does

Pinterest-style card grid where card heights depend on the text content. Pre-measure every item's height at the column width with `prepare()` + `layout()`, then use a shortest-column-first packing algorithm to place cards. `layout()` is cheap enough to re-run on every resize.

## When to use

- Portfolio galleries with text cards
- Blog / article grids with previews of variable length
- Product listings with description text

## How it works

```ts
// Source: use-pretext/SKILL.md — Recipe 1 condensed
function computeLayout(width) {
  const colWidth = (width - (colCount - 1) * gap) / colCount
  const textWidth = colWidth - 32
  const colHeights = new Array(colCount).fill(0)
  const result = []
  for (const item of items) {
    const prepared = prepare(item.text, font)
    const { height } = layout(prepared, textWidth, lineHeight)
    const totalH = height + cardPadding
    let shortest = 0
    for (let c = 1; c < colCount; c++) if (colHeights[c] < colHeights[shortest]) shortest = c
    result.push({ ...item, x: shortest * (colWidth + gap), y: colHeights[shortest], w: colWidth, h: totalH })
    colHeights[shortest] += totalH + gap
  }
  return result
}
```

## Minimal example

```svelte
{#each positioned as card}
  <div style="left:{card.x}px; top:{card.y}px; width:{card.w}px; height:{card.h}px">{card.text}</div>
{/each}
```

## Gotchas

- Cache the prepared handles across resizes — only re-layout.
- `colCount` changes with breakpoints; re-compute.
- Account for card border in `totalH`.

## Cross-references

- Related: TECH-14-dom-free-height, TECH-36-generative-poster-grid
- API reference: [TECH-03-layout](TECH-03-layout.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
