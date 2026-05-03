---
name: TECH-53-threejs-text-wrapping
category: 3d
source: pretext-skills/amw-pretext-threejs-viral-frontend-design.zip (documented in SKILL-11)
also-in: pretext-skill-main/patterns.md (3D Text Wrapping)
---

# Three.js — text wrapping around 3D objects

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


**Category:** 3d
**Status:** demo-only

## What it does

Project a 3D object (torus, sphere, custom mesh) into a 2D silhouette per frame, convert the silhouette to per-Y line-width constraints, feed those to `layoutNextLine()`. Result: 2D text appears to flow AROUND a 3D rotating object.

## When to use

- Viral hero sections
- 3D brand showcase pages
- Interactive gallery pieces

## How it works

```js
// Source: pretext-skill-main/patterns.md — 3D Text Wrapping concept
// Each frame:
// 1. Raycast or depth-sample the 3D object into a 2D silhouette (offscreen canvas)
// 2. For each text line Y, compute available free width from silhouette pixels
// 3. Feed width to layoutNextLine(prepared, cursor, width)
// 4. Render text — appears to flow around the 3D shape
```

## Minimal example

Conceptual only — the full demo is in `pretext-threejs-viral-frontend-design.zip`.

## Gotchas

- Silhouette extraction at every frame is GPU-heavy; cache per-rotation-step if object spins slowly.
- Z-order: text should either always occlude or always be occluded by the 3D object, not mix.

## Cross-references

- Related: TECH-20-polygon-obstacle-mask, TECH-23-animated-obstacle-reflow, TECH-54-splat-editor
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
