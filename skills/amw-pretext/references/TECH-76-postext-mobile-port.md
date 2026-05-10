---
name: TECH-76-postext-mobile-port
category: integrate
source: pretext-skills/postext-main.zip (sandbox) and packages/postext
also-in: 
---

# postext — pretext port for React Native / mobile runtimes

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

**Category:** integrate
**Status:** experimental

## What it does

`postext` is a companion package (see `packages/postext/` in `postext-main.zip`) that ports the pretext measurement model to environments where the standard Canvas API is unavailable or weak — React Native, embedded webviews, some Node runtimes. API surface mirrors pretext but the backend uses a platform-specific text measurer.

## When to use

- React Native apps that need pretext semantics
- Embedded webviews with limited Canvas support
- Cross-platform text-measurement needs where pretext itself doesn't run

## How it works

```ts
// Source: postext-main/packages/postext/README.md (concept)
import { prepare, layout } from 'postext'  // API mirrors @chenglou/pretext
const prepared = prepare(text, '16px Inter')
const { height } = layout(prepared, 320, 24)
```

## Minimal example

See `postext-main/packages/postext-sandbox/` for platform-specific sandboxes.

## Gotchas

- Experimental — measurement accuracy varies by platform.
- Native font metrics may drift from browser canvas — validate with your target fonts.
- Not a drop-in for pretext; APIs overlap but behavioral guarantees differ.

## Cross-references

- Related: TECH-62-ssr-node-canvas, TECH-01-prepare-basics
- API reference: [TECH-01-prepare-basics](TECH-01-prepare-basics.md)
  > What it does · When to use · How it works · Minimal example · Configuration options (source: pretext-skill-master/SKILL.md) · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
