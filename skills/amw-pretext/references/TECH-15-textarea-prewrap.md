---
name: TECH-15-textarea-prewrap
category: measure
source: pretext-skills/amw-pretext-text-measurement/SKILL.md
also-in: SKILL-11.md, SKILL-13.md, SKILL-16.md, SKILL-21.md, SKILL-23.md, use-pretext/SKILL.md, pretext-docs/SKILL.md
---

# Textarea-compatible measurement (whiteSpace: pre-wrap)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** measure
**Status:** stable

## What it does

Pass `{ whiteSpace: 'pre-wrap' }` to `prepare()` / `prepareWithSegments()` so spaces, `\t` tabs, and `\n` newlines are preserved — same semantics as a `<textarea>`. Enables auto-height textareas where every keystroke re-runs `layout()` without the user seeing flicker.

## When to use

- Auto-growing textareas
- Code/poetry editors that must preserve line breaks literally
- Any input where the user controls whitespace

## How it works

Switches the internal whitespace normalizer from "collapse + break-at-boundaries" to "preserve everything". Tabs keep their width; newlines force hard line breaks.

```ts
// Source: pretext-docs/SKILL.md
const prepared = prepare(textareaValue, '16px Inter', { whiteSpace: 'pre-wrap' })
const { height } = layout(prepared, textareaWidth, 20)
textarea.style.height = `${height}px`
```

## Minimal example

```ts
// Source: pretext-integrate/SKILL.md
textarea.addEventListener('input', () => {
  const prepared = prepare(textarea.value, fontString, { whiteSpace: 'pre-wrap' })
  textarea.style.height = `${layout(prepared, textarea.clientWidth, 24).height}px`
})
```

## Gotchas

- Forgetting `{ whiteSpace: 'pre-wrap' }` collapses the user's spaces/newlines silently.
- Tabs use the Canvas-reported tab width, not the CSS `tab-size` — set `tab-size` to match.

## Cross-references

- Related: TECH-14-dom-free-height, TECH-57-svelte-islands (AutoHeightTextarea pattern)
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
  > What it does · When to use · How it works · Minimal example · Configuration options (source: pretext-skill-master/SKILL.md) · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
