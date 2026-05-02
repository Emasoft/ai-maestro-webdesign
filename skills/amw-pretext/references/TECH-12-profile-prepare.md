---
name: TECH-12-profile-prepare
category: api
source: pretext-skills/amw-pretext-docs/SKILL.md
also-in: 
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# profilePrepare() — diagnostic timing breakdown

**Category:** api
**Status:** stable

## What it does

`profilePrepare(text, font, options?) -> PrepareProfile` runs `prepare()` and returns a timing breakdown: `{ analysisMs, measureMs, totalMs, analysisSegments, preparedSegments, breakableSegments }`. Use when a `prepare()` call is slower than expected and you need to know whether segmentation or canvas measurement is the bottleneck.

## When to use

- Debugging slow `prepare()` calls on large documents
- Comparing segmentation vs measurement cost per font
- Verifying cache hits

## How it works

Wraps `prepare()` with per-phase timestamps. Drop-in replacement while profiling — not for production.

```ts
// Source: pretext-docs/SKILL.md (PrepareProfile type)
const p = profilePrepare(text, '16px Inter')
console.log(p.analysisMs, p.measureMs, p.totalMs)
```

## Minimal example

```ts
// Source: pretext-docs/SKILL.md
import { profilePrepare } from '@chenglou/pretext'
const profile = profilePrepare(longArticle, '16px Inter')
// {analysisMs:12.4, measureMs:6.1, totalMs:18.5, analysisSegments:412, preparedSegments:389, breakableSegments:73}
```

## Gotchas

- Has extra timing overhead; do not use as a replacement for `prepare()` in production.
- Timings depend on Canvas font engine availability and fontloaders.

## Cross-references

- Related: TECH-01-prepare-basics
- API reference: this file
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
