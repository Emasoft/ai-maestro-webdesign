---
name: TECH-72-use-pretext-decision-guide
category: consult
source: pretext-skills/use-pretext/SKILL.md
also-in: SKILL-11.md, SKILL-16.md, SKILL-21.md, pretext-skill-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Decision guide — when to use pretext (and when NOT)

**Category:** consult
**Status:** stable

## What it does

Before reaching for pretext, consult this decision table. Pretext is NOT a general CSS replacement — it's a precision tool for cases where CSS layout is insufficient or where you need metrics before rendering. Using it where CSS suffices just adds a dependency.

## When to use

- Any triage decision at the START of a feature
- Before writing `prepare()` the first time in a codebase
- To justify pretext to a reviewer or team lead

## How it works

**USE pretext when** (from use-pretext/SKILL.md):
1. Virtualized / occlusion-culled lists
2. Masonry / column-balanced layouts
3. Canvas / SVG text rendering
4. Shrink-wrap / tight-fit containers
5. Preventing layout shift
6. Text truncation with exact line control
7. Responsive text-aware layouts
8. Performance-critical resize handlers

**Do NOT use pretext when**:
1. Static rendered text (Astro build-time)
2. CSS solves it: `line-clamp`, `text-overflow: ellipsis`, `min-height`, Grid/Flex
3. Server-side only (pretext needs Canvas + Intl.Segmenter)
4. Single-line text (`canvas.measureText` is enough)
5. HTML content (not plain text)
6. TanStack Virtual + height estimation (fragile per pretext-skill-main/SKILL.md)
7. Accordion content with HTML structure (use off-screen DOM measurement instead)

## Minimal example

Apply the table to your feature before writing any code.

## Gotchas

- "CSS can handle it" is the #1 reason to skip pretext — check line-clamp first.
- Tanstack Virtual warning is specific; other virtualization libs may work.

## Cross-references

- Related: ALL pretext techniques (this is the routing layer)
- API reference: [skills/amw-pretext/SKILL.md](../SKILL.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
