---
name: TECH-29-line-clamp-truncate-readmore
category: typography
source: pretext-skills/use-pretext/SKILL.md
also-in: SKILL-21.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Exact-line truncate with "Read more"

**Category:** typography
**Status:** stable

## What it does

Clamp text to exactly N rendered lines and show a "Read more" / ellipsis only when the original really overflows. Unlike CSS `line-clamp`, pretext knows the exact character index where line N ends, so you can insert the ellipsis at the precise grapheme boundary.

## When to use

- Card summaries that should cut to a specific line count
- Preview excerpts with a reliable "Show more" toggle
- Any truncation UI that must know WHETHER truncation happened

## How it works

```ts
// Source: use-pretext/SKILL.md — Recipe 5
const prepared = prepareWithSegments(text, font)
const { lines } = layoutWithLines(prepared, containerWidth, lineHeight)
if (lines.length > maxLines) {
  isTruncated = true
  truncatedText = lines.slice(0, maxLines).map(l => l.text).join('').trimEnd() + '…'
}
```

## Minimal example

```svelte
<!-- Source: use-pretext/SKILL.md — Recipe 5 -->
<p>{expanded ? text : truncatedText}</p>
{#if isTruncated}
  <button on:click={() => expanded = !expanded}>
    {expanded ? 'Show less' : 'Read more'}
  </button>
{/if}
```

## Gotchas

- `line.text` may include a trailing space — `trimEnd()` before appending the ellipsis.
- Joining `line.text` across lines does not preserve the original whitespace collapse decisions; fine for most cases but verify for `pre-wrap`.
- On width change, recompute — a narrower container may now fit exactly N lines without truncating.

## Cross-references

- Related: TECH-04-layout-with-lines
- API reference: [TECH-04-layout-with-lines](TECH-04-layout-with-lines.md)
  > What it does · When to use · How it works · Minimal example · Return types (source: pretext-skill-master/SKILL.md) · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
