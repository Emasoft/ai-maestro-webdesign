---
name: TECH-50-cycling-text-autofit
category: motion
source: pretext-skills/amw-pretext-skill-main/patterns.md
also-in: 
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Cycling text with auto-fit (rotating headline reveals)

**Category:** motion
**Status:** stable

## What it does

Rotate through a list of headlines, auto-fitting each (TECH-27) so all cycle members occupy the same visual block while keeping readable size. Fade/slide between entries with a double-rAF pattern so transitions are visible.

## When to use

- Hero sections that rotate value props
- Loading messages that cycle while loading
- Playful product taglines

## How it works

```ts
// Source: pretext-skill-main/patterns.md — Cycling Text with Auto-Fit
setInterval(() => {
  const nextText = texts[(i = (i + 1) % texts.length)]
  const newSize = autoFitFontSize(nextText, family, maxWidth, 1.5, 2)
  el.style.transition = 'opacity 500ms, transform 500ms'
  el.style.opacity = '0'
  el.style.transform = 'translateY(-30px)'
  setTimeout(() => {
    el.textContent = nextText
    el.style.fontSize = newSize + 'px'
    el.style.transition = 'none'
    el.style.transform = 'translateY(30px)'
    requestAnimationFrame(() => requestAnimationFrame(() => {
      el.style.transition = 'opacity 500ms, transform 500ms'
      el.style.opacity = '1'
      el.style.transform = 'translateY(0)'
    }))
  }, FADE_DURATION)
}, CYCLE_INTERVAL)
```

## Minimal example

See How-it-works above — full pattern is in pretext-skill-main/patterns.md.

## Gotchas

- **Double-rAF is essential.** Without it, browser batches the reset + new position + restored transition into one frame, producing no visible animation (source: pretext-skill-main/patterns.md).
- Keep `autoFitFontSize` iterations low (10) for frequent cycling.

## Cross-references

- Related: TECH-27-auto-fit-font-size
- API reference: [TECH-27-auto-fit-font-size](TECH-27-auto-fit-font-size.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
