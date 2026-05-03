---
name: TECH-26-balanced-headline
category: typography
source: pretext-skills/amw-pretext-typography-skill-main/SKILL.md
also-in: pretext-text-measurement/SKILL.md, SKILL-13.md, pretext-frontend-motion-main (Justification Comparison)
---

# Balanced headline (widow-free multiline titles)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


**Category:** typography
**Status:** stable

## What it does

For a multiline headline, find the width that makes the lines as even as possible — no tiny widow line at the bottom, no jagged staircase. Binary-search widths via `measureLineStats()` or `walkLineRanges()` until the line count or widest-line variance crosses a threshold. Pretext is essentially a userland `text-wrap: balance` that works in older browsers and gives you the exact pixel width.

## When to use

- Hero headlines / display text
- Pull quotes
- Card titles where visual balance matters

## How it works

```ts
// Source: pretext-text-measurement/SKILL.md
function findBalancedWidth(text, font, maxWidth) {
  const prepared = prepareWithSegments(text, font)
  const { lineCount: targetLines } = measureLineStats(prepared, maxWidth)
  let lo = 1, hi = maxWidth
  while (hi - lo > 1) {
    const mid = (lo + hi) / 2
    const { lineCount } = measureLineStats(prepared, mid)
    if (lineCount <= targetLines) hi = mid
    else lo = mid
  }
  return hi
}
```

## Minimal example

```ts
// Source: pretext-typography-skill-main/SKILL.md
const balancedW = findBalancedWidth(headline, '56px/1.1 "Playfair Display"', 720)
h1.style.maxWidth = `${balancedW}px`
```

## Gotchas

- Doesn't help for single-line headlines.
- Works on line-count-equal, not word-count-equal — for true word balance, iterate widths and score variance.
- Pair with `text-wrap: balance` as progressive enhancement.

## Cross-references

- Related: TECH-06-walk-line-ranges, TECH-25-shrinkwrap-width, TECH-49-justification-comparison
- API reference: [TECH-07-measure-line-stats](TECH-07-measure-line-stats.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
