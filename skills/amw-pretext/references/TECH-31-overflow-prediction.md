---
name: TECH-31-overflow-prediction
category: typography
source: pretext-skills/amw-pretext-agent-skill-main/implementation-patterns.md
also-in: SKILL-15.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Overflow prediction (will this button's label wrap?)

**Category:** typography
**Status:** stable

## What it does

Before rendering, check whether a button / chip / label / cell's text would wrap onto a second line at the target width. If `layout(prepared, buttonWidth, lineHeight).lineCount > 1`, the label overflows — shrink the font, truncate, or widen the button.

## When to use

- Dev-time assertions that CTAs don't wrap
- Runtime adaptive sizing (shrink font if overflow)
- Design-system lint checks for labels in a grid

## How it works

```ts
// Source: pretext-agent-skill-main/implementation-patterns.md — Pattern 2
const prepared = prepare(buttonText, font)
const { lineCount } = layout(prepared, buttonInnerWidth, lineHeight)
const overflows = lineCount > 1
```

## Minimal example

```ts
// Source: pretext-agent-skill-main/implementation-patterns.md
if (layout(prepare('Get Started Now →', '14px Inter'), 80, 20).lineCount > 1) {
  console.warn('Button label wraps at 80px wide')
}
```

## Gotchas

- Include inner padding in `buttonInnerWidth`, not the full button width.
- At dev time, assert against the widest label in your translations catalog.

## Cross-references

- Related: TECH-27-auto-fit-font-size, TECH-08-measure-natural-width
- API reference: [TECH-03-layout](TECH-03-layout.md)
  > What it does · When to use · How it works · Minimal example · Return value · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
