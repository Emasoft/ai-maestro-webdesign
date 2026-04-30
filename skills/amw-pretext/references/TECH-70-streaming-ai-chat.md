---
name: TECH-70-streaming-ai-chat
category: workflow
source: pretext-skills/amw-pretext-skill-main/pretext/skills/amw-pretext/references/patterns.md
also-in: 
---

# Streaming AI chat (measure tokens as they arrive)

**Category:** workflow
**Status:** stable

## What it does

Compute the evolving bubble height as LLM tokens stream in. Call `layout()` on every token — at ~0.0002 ms per call, 60 fps measurement is comfortable even under rapid streaming. The bubble resizes smoothly, scrollbars behave correctly, and layout shift is eliminated.

## When to use

- LLM chat UIs (Claude, GPT, Gemini apps)
- Live captioning with growing text
- Any UI where text arrives token-by-token

## How it works

```js
// Source: pretext-skill-main/patterns.md — Streaming AI Chat
let textSoFar = ''
for await (const token of stream) {
  textSoFar += token
  const prepared = prepare(textSoFar, '16px sans-serif')
  const { height } = layout(prepared, 400, 24)
  bubble.style.height = height + 'px'
  bubble.textContent = textSoFar
}
```

## Minimal example

See How-it-works above — runnable as written for any async iterable of tokens.

## Gotchas

- `prepare()` is expensive per call; for very long streams consider preparing once per N tokens rather than every token.
- If text is huge (>10 KB chunks), `prepare()` takes 1-5 ms — enough to drop frames. Batch updates.
- Auto-scroll: check `scrollTop + clientHeight >= scrollHeight` BEFORE applying the new height to decide whether to auto-scroll.

## Cross-references

- Related: TECH-14-dom-free-height, TECH-30-layout-shift-prevention, TECH-46-chat-bubbles
- API reference: [TECH-03-layout](TECH-03-layout.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
