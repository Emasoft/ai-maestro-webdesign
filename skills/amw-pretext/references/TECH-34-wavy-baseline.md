---
name: TECH-34-wavy-baseline
category: art
source: pretext-skills/amw-pretext-art/SKILL.md
also-in: skills/amw-pretext-art/SKILL.md, SKILL-14.md
---

# Wavy / curved baseline

**Category:** art
**Status:** stable

## What it does

Render each line with a sinusoidal (or path-based) Y offset so the text appears to wave. Use `layoutWithLines()` to get per-line positions, then add `sin(i * frequency + phase) * amplitude` per line. Animate `phase` for continuous motion.

## When to use

- Playful / editorial poster visuals
- Seaside / water / music themes
- Text-heavy loading or transition states

## How it works

```ts
// Source: pretext-art/SKILL.md — Path C
function renderWavy(x, baseY, maxWidth, amplitude = 8, frequency = 0.04, phase = 0) {
  const { lines } = layoutWithLines(prepared, maxWidth, LINE_HEIGHT)
  ctx.font = FONT
  lines.forEach((line, i) => {
    const waveOffset = Math.sin(i * frequency * 10 + phase) * amplitude
    ctx.fillText(line.text, x, baseY + i * LINE_HEIGHT + waveOffset)
  })
}
let phase = 0
function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  renderWavy(40, 80, canvas.width - 80, 10, 0.05, phase)
  phase += 0.04
  requestAnimationFrame(animate)
}
```

## Minimal example

```ts
// Source: skills/amw-pretext-art/SKILL.md (plugin)
const waveY = Math.sin(i * frequency + phase) * amplitude
ctx.fillText(line.text, x, baseY + i * LINE_HEIGHT + waveY)
```

## Gotchas

- Amplitude too high at large line heights = readability loss. Keep amplitude ≤ 0.5 × LINE_HEIGHT.
- For per-glyph wave, do NOT use this technique — measure each grapheme separately and animate per glyph.

## Cross-references

- Related: TECH-04-layout-with-lines, TECH-35-text-on-path
- API reference: [TECH-04-layout-with-lines](TECH-04-layout-with-lines.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
