---
name: TECH-43-glyph-morphing
category: art
source: pretext-skills/SKILL-11.md
also-in: 
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Glyph morphing (interpolate letterforms A → Z)

**Category:** art
**Status:** demo-only

## What it does

Animate the CONTOUR of one letter morphing into another (A → Z) using opentype.js to extract contours and flubber's `interpolate()` to blend them over time. Pretext is used to measure position/advance so the morphing glyph sits in the correct place inside a flowing layout.

## When to use

- Loading indicators where letters transform
- Playful wordmark animations
- Character evolution reveals

## How it works

```js
// Source: SKILL-11 opentype.js + flubber section
// 1. For glyph A: opentype.font.getPath('A').toPathData()
// 2. For glyph Z: opentype.font.getPath('Z').toPathData()  
// 3. flubber.interpolate(pathA, pathZ, { maxSegmentLength: 10 })
// 4. Per-frame: call the interpolator with t and set as SVG path d=""
```

## Minimal example

```js
// Source: SKILL-11 defaults
// Morph duration 300-2000 ms (default 800)
// Flubber maxSegmentLength 5-20 (default 10)
```

## Gotchas

- 1-to-many / many-to-1 contours (B → I) need a contour strategy — flubber auto-detects but may look odd.
- Not all font pairs morph cleanly — prepare a fallback tween animation.
- CPU cost scales with `maxSegmentLength`; 10 is the SKILL-11 default sweet spot.

## Cross-references

- Related: TECH-35-text-on-path, TECH-52-glyph-path-art
- API reference: [TECH-02-prepare-with-segments](TECH-02-prepare-with-segments.md)
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
