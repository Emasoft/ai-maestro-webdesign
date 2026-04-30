---
name: TECH-27-auto-fit-font-size
category: typography
source: pretext-skills/amw-pretext-skill-main/SKILL.md
also-in: pretext-skill-main/patterns.md, SKILL-17 (SmartPage)
---

# Auto-fit font size (largest font that stays within N lines)

**Category:** typography
**Status:** stable

## What it does

Binary-search the largest font size that keeps a text block within a target line count at a given container width. CSS has no equivalent — this is often called "pretext's killer feature" (source: pretext-skill-main/SKILL.md). Use for hero headlines, card titles, quote displays where the text varies but the visual block size should be consistent.

## When to use

- Hero headlines that must stay within 2 / 3 lines
- Card titles (different titles, consistent block height)
- Quote displays / testimonials
- Auto-fit a slide title to one line

## How it works

```js
// Source: pretext-skill-main/pretext/skills/amw-pretext/references/patterns.md
function autoFitFontSize(text, fontFamily, maxWidth, lineHeight, targetMaxLines, minFont, maxFont) {
  let lo = minFont || 14, hi = maxFont || 34, bestSize = lo
  for (let i = 0; i < 20; i++) {  // 20 iterations = sub-pixel precision
    const mid = (lo + hi) / 2
    const prepared = prepare(text, `${mid}px ${fontFamily}`)
    const { lineCount } = layout(prepared, maxWidth, mid * lineHeight)
    if (lineCount <= targetMaxLines) { bestSize = mid; lo = mid }
    else hi = mid
  }
  return Math.round(bestSize * 10) / 10
}
```

## Minimal example

```js
const bestSize = autoFitFontSize(headline, 'Georgia, serif', 500, 1.5, 3, 14, 40)
h1.style.fontSize = bestSize + 'px'
```

## Gotchas

- **lineHeight must be in absolute px** (`fontSize * 1.5`), NOT a multiplier — pretext's top gotcha.
- 20 iterations gives sub-pixel precision; 10 is usually enough.
- Short text hits `maxFont` and stays 1 line — fine.
- Paying `prepare()` once per candidate size; cache by size if called often.

## Cross-references

- Related: TECH-03-layout, TECH-71-smartpage-a4-autofit
- API reference: [TECH-03-layout](TECH-03-layout.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
