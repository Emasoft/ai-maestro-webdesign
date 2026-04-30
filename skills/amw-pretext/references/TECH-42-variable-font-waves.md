---
name: TECH-42-variable-font-waves
category: art
source: pretext-skills/SKILL-11.md
also-in: 
---

# Variable-font per-character waves (weight / width ripples)

**Category:** art
**Status:** demo-only

## What it does

Animate a variable font's axes (weight, width, optical size) per-character using CSS `font-variation-settings` or opentype.js `font.tables.fvar.axes`, driven by a sine / ripple / cascade function indexed by character position. Pretext measures the per-character widths so the DOM/Canvas layout still aligns as weights pulse.

## When to use

- Breathing / heartbeat marquee text
- Cascade effects (wave of weight traveling across the word)
- Interactive hover-to-embolden titles

## How it works

```js
// Concept — Source: SKILL-11 opentype.js + CSS font-variation-settings
// Per character i:
// 1. Compute phase[i] = sin(time * freq + i * stagger)
// 2. weight[i] = 400 + phase[i] * 300  // 400-700 range
// 3. Apply via inline style: `font-variation-settings: 'wght' ${weight[i]}`
// 4. Pretext must re-prepare at each weight change OR pre-measure all weights

// For Canvas, you'd re-measure each char at each weight — use per-char prepareWithSegments cache
```

## Minimal example

```js
// Per-character CSS toggling — DOM path
spans.forEach((s, i) => {
  s.style.fontVariationSettings = `"wght" ${400 + Math.sin(t + i * 0.3) * 300}`
})
```

## Gotchas

- Weight change = width change = must re-measure if layout depends on width.
- `font-variation-settings` in Canvas `ctx.font` has limited support across browsers.

## Cross-references

- Related: TECH-37-typographic-ascii, TECH-35-text-on-path
- API reference: [TECH-02-prepare-with-segments](TECH-02-prepare-with-segments.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
