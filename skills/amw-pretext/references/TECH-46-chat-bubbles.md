---
name: TECH-46-chat-bubbles
category: motion
source: pretext-skills/amw-pretext-frontend-motion-main/core/bundle/references/demo-family-map.md
also-in: use-pretext/SKILL.md Recipe 2, SKILL-13, SKILL-15, pretext-skill-main/patterns.md (Shrink-Wrap Chat Bubbles)
---

# Tight multiline chat bubbles (Bubbles demo family)

**Category:** motion
**Status:** stable

## What it does

Message bubbles whose width tracks the widest line of their content, not the full container. Built on the shrink-wrap technique (TECH-25) with `walkLineRanges()` + a binary-search to preserve the original line count.

## When to use

- Any chat / comment / DM UI
- Notification toasts with variable copy
- Tooltips with multiline content

## How it works

```ts
// Source: use-pretext/SKILL.md — Recipe 2 — condensed
const prepared = prepareWithSegments(text, font)
const initial = layout(prepared, maxWidth, lineHeight)
let lo = 1, hi = maxWidth
while (lo < hi) {
  const mid = Math.floor((lo + hi) / 2)
  if (layout(prepared, mid, lineHeight).lineCount <= initial.lineCount) hi = mid
  else lo = mid + 1
}
let maxLineW = 0
walkLineRanges(prepared, lo, line => { if (line.width > maxLineW) maxLineW = line.width })
bubble.style.width = `${Math.ceil(maxLineW) + paddingH * 2}px`
```

## Minimal example

```ts
// Source: pretext-skill-main/patterns.md
function getBubbleWidth(text, font, maxWidth) {
  const prepared = prepareWithSegments(text, font)
  let widestLine = 0
  walkLineRanges(prepared, maxWidth, l => { widestLine = Math.max(widestLine, l.width) })
  return Math.ceil(widestLine) + padding * 2
}
```

## Gotchas

- Emoji / ZWJ sequences widen the bubble unexpectedly — always test with emoji corpora.
- For streaming chats, re-measure on each token arrival (TECH-70).

## Cross-references

- Related: TECH-25-shrinkwrap-width, TECH-70-streaming-ai-chat
- API reference: [TECH-06-walk-line-ranges](TECH-06-walk-line-ranges.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
