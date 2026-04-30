---
name: TECH-21-multi-column-handoff
category: layout
source: pretext-skills/SKILL-15.md
also-in: pretext-frontend-motion-main (demo-family-map: Editorial Engine, Dynamic Layout), pretext-skill-main/patterns.md
---

# Multi-column text handoff

**Category:** layout
**Status:** stable

## What it does

Flow a single text stream across multiple columns (magazine layout). `layoutNextLine()` returns a `LayoutLine` whose `.end` cursor is the handoff point — carry that cursor into the next column's iteration instead of re-splitting the source string.

## When to use

- Magazine / newspaper layouts
- Multi-column long-form articles
- Editorial spreads where text must flow column-by-column

## How it works

```ts
// Source: SKILL-15.md / pretext-skill-main/patterns.md
const prepared = prepareWithSegments(article, font)
let cursor = { segmentIndex: 0, graphemeIndex: 0 }
let y = 0
for (let col = 0; col < columns; col++) {
  while (y + LINE_HEIGHT <= columnBottom) {
    const line = layoutNextLine(prepared, cursor, columnWidth)
    if (!line) break  // story done
    renderLineInColumn(line, col, y)
    cursor = line.end
    y += LINE_HEIGHT
  }
  y = columnTop  // reset Y for next column
}
```

## Minimal example

```ts
// Two-column handoff
while (column1.hasRoom() && (line = layoutNextLine(prepared, cursor, w1))) { 
  column1.place(line); cursor = line.end 
}
while (column2.hasRoom() && (line = layoutNextLine(prepared, cursor, w2))) {
  column2.place(line); cursor = line.end
}
```

## Gotchas

- Never manually slice the source text to split across columns — carry the cursor.
- Columns can have DIFFERENT widths (first narrower, second wider) — per-column `maxWidth` is fine.

## Cross-references

- Related: TECH-05-layout-next-line, TECH-20-polygon-obstacle-mask, TECH-44-editorial-engine
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
