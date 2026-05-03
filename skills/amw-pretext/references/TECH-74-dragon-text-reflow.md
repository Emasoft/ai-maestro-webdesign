---
name: TECH-74-dragon-text-reflow
category: motion
source: pretext-skills/amw-pretext-skill-main/pretext/skills/amw-pretext/references/patterns.md
also-in: SKILL-11.md
---

# Dragon text reflow (text flowing around an 80-segment creature)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


**Category:** motion
**Status:** demo-only

## What it does

Classic pretext community demo: text flows around a dragon built from 80 linked body segments. Each segment is an obstacle; the ensemble moves in a follow-the-leader serpentine pattern. Pretext re-routes the body text around every segment at 60 fps using TECH-24's `carveTextLineSlots`.

## When to use

- Portfolio "wow" piece
- Demo of pretext's obstacle-routing ceiling
- Animation showcases

## How it works

Concept — Source: pretext-skill-main/patterns.md "Dragon text reflow"
- 80-segment creature follows a leader head with damped spring chain
- Per frame: project each segment to a circle obstacle in the text plane
- Call `carveTextLineSlots()` per line to get free slots around ALL 80 segments
- `layoutNextLine()` fills each slot; shared cursor carries across

## Minimal example

Not a few-line snippet. See community demos at https://chenglou.me/pretext/ and https://pretextwall.xyz/.

## Gotchas

- 80 obstacles per line means ~80 interval subtractions per band — still cheap but profile if lagging.
- Segment collision order must be stable — sort by X before carving.

## Cross-references

- Related: TECH-23-animated-obstacle-reflow, TECH-24-carve-text-line-slots
- API reference: [TECH-05-layout-next-line](TECH-05-layout-next-line.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
