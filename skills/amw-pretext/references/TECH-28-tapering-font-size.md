---
name: TECH-28-tapering-font-size
category: typography
source: pretext-skills/amw-pretext-art/SKILL.md
also-in: skills/amw-pretext-art/SKILL.md, SKILL-14.md
---

# Tapering / variable font size (big first line → small tail)

**Category:** typography
**Status:** stable

## What it does

Render a text block where each line has a smaller font size than the previous — large first line (hero), smaller second (lede), fine print at the bottom. Iterate a descending font-size gradient and consume words greedily using `layoutWithLines()` at each size.

## When to use

- Stacked headline + subheadline + meta lines
- Poster-style tapering text
- Marketing display where readability should taper into detail

## How it works

```ts
// Source: pretext-art/SKILL.md — Path D
const fontSizes = [48, 36, 24, 18, 14]
let words = TEXT.split(' ')
let y = 0
for (const size of fontSizes) {
  if (words.length === 0) break
  const font = `${size}px sans-serif`
  const prepared = prepareWithSegments(words.join(' '), font)
  const { lines } = layoutWithLines(prepared, MAX_WIDTH, size * 1.3)
  const firstLine = lines[0]
  ctx.font = font
  ctx.fillText(firstLine.text, 0, y + size)
  y += size * 1.3
  words = words.slice(firstLine.text.split(' ').length)
}
```

## Minimal example

```ts
// Source: pretext-art/SKILL.md
// See How-it-works above — full runnable example is in the source
```

## Gotchas

- Each size requires its own `prepare()` — do not cache across sizes.
- Line height must scale with font size (`size * 1.3` is a reasonable ratio).
- If no words fit at a given size, the algorithm falls through with some leftover words — clamp `minFont`.

## Cross-references

- Related: TECH-04-layout-with-lines, TECH-01-prepare-basics
- API reference: [TECH-04-layout-with-lines](TECH-04-layout-with-lines.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
