---
name: TECH-30-layout-shift-prevention
category: typography
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, use-pretext/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Prevent layout shift (CLS) on dynamic content

**Category:** typography
**Status:** stable

## What it does

When text loads asynchronously (fetch, stream, lazy block), measure it with pretext BEFORE inserting it into the DOM, then set the container's height first. This reserves the exact pixel height so the browser never needs to reflow around newly arrived content — eliminates Cumulative Layout Shift (CLS) for text-driven blocks.

## When to use

- Async-loaded article content / comments
- LLM streaming chat bubbles (measure each partial)
- Card grids where items arrive from different endpoints

## How it works

```ts
// Source: use-pretext/SKILL.md — Recipe 6
async function loadAndRender(width) {
  const text = await fetchText()
  const prepared = prepare(text, '16px Inter')
  const { height } = layout(prepared, width, 24)
  container.style.height = `${height}px`   // reserve
  container.textContent = text             // insert — no reflow around it
}
```

## Minimal example

```ts
// Source: pretext-text-measurement/SKILL.md
const prepared = prepare(text, '16px Inter')
const { height } = layout(prepared, width, 24)
container.style.height = `${height}px`
container.textContent = text
```

## Gotchas

- CSS padding / border around the text must be added to the reserved height.
- On the first paint, `document.fonts.ready` should have resolved — otherwise the fallback-font measurement is off.
- For streaming content, re-measure + reset height per incoming chunk.

## Cross-references

- Related: TECH-14-dom-free-height, TECH-70-streaming-ai-chat
- API reference: [TECH-03-layout](TECH-03-layout.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
