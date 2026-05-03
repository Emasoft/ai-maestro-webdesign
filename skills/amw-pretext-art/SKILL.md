---
name: amw-pretext-art
description: Deprecated. See ../amw-pretext/ for the unified pretext skill. This file is a redirect stub only. Use when the pretext-art trigger is invoked — redirect to amw-pretext. Trigger with explicit "pretext-art" or legacy pretext-art phrasing.
version: 0.2.0
---

# pretext-art (MOVED TO `skills/amw-pretext/`)

## Overview

Deprecated redirect stub. All pretext-art capability (kinetic typography, shaped containers, calligrams, wavy baseline, text-on-path, poster grids, typographic ASCII, and ~70 additional pretext techniques) has been consolidated into `skills/amw-pretext/`. Any request landing here is routed immediately to that skill.

## Prerequisites

Standard plugin runtime — no skill-specific prerequisites beyond the global plugin dependencies.

## Instructions

1. Recognize that this skill is a **redirect stub** — it contains no operational logic and emits no artifacts.
2. Re-route the incoming request immediately to `skills/amw-pretext/SKILL.md`.
3. In that skill, identify the matching `category: art` technique from the 78-technique catalog (kinetic typography, shaped containers, calligrams, wavy baseline, text-on-path, poster grid, typographic ASCII, and all other pretext effects).
4. Follow the TECH reference file for the selected technique (found under `skills/amw-pretext/references/`).

Route every art-focused pretext request to `skills/amw-pretext/SKILL.md` and pick the matching `category: art` technique from its catalog.

## Examples

**Concrete example — kinetic typography request:**

- **Input:** "make the heading shrink and reflow as the user resizes the window" (legacy `pretext-art` phrasing).
- **Operation:** redirect stub recognizes the request, routes immediately to `skills/amw-pretext/SKILL.md`. Decision tree there points at `TECH-33-kinetic-width-animation.md`.
- **Output:** the redirect emits no artifact itself; the chosen TECH file's "Minimal example" section produces a runnable JS module that drives the kinetic reflow.

**Concrete example — calligram request:**

- **Input:** "render the word DRAGON in the shape of a dragon" (creative-text intent that lands here by legacy trigger).
- **Operation:** redirect to `skills/amw-pretext/`; choose `TECH-38-calligram-shape.md` (or `TECH-39-glyph-mask-calligram.md` / `TECH-44-outline-calligram.md` depending on visual brief).
- **Output:** SVG calligram emitted by the destination TECH file's example pipeline. This stub itself emits nothing.

See `skills/amw-pretext/SKILL.md` for the full 78-technique catalog with minimal runnable examples in each TECH file.

## Output

This stub produces no artifacts — it redirects. All output is produced by `skills/amw-pretext/`.

## Error Handling

If this stub is invoked instead of `amw-pretext`: re-route the request to `skills/amw-pretext/SKILL.md`. This file contains no operational logic.

## Resources

- [SKILL](../amw-pretext/SKILL.md) — the unified pretext skill (all techniques)
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator

The full pretext capability — Canvas / SVG creative text effects AND all API / measurement / layout / integration / tables / 3D / workflow / consult techniques — now lives at:

**[`skills/amw-pretext/SKILL.md`](../amw-pretext/SKILL.md)**

The original 8 pretext-art effects (kinetic / shaped / wavy / tapering / poster-grid / custom / text-on-path / per-line-metrics) are catalogued as TECH files in `skills/amw-pretext/references/`, alongside ~70 other techniques:

- Kinetic typography: [TECH-33-kinetic-width-animation](../amw-pretext/references/TECH-33-kinetic-width-animation.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Shaped containers: [TECH-19-shaped-container](../amw-pretext/references/TECH-19-shaped-container.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Wavy baseline: [TECH-34-wavy-baseline](../amw-pretext/references/TECH-34-wavy-baseline.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Tapering font size: [TECH-28-tapering-font-size](../amw-pretext/references/TECH-28-tapering-font-size.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Generative poster grid: [TECH-36-generative-poster-grid](../amw-pretext/references/TECH-36-generative-poster-grid.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Text on a path: [TECH-35-text-on-path](../amw-pretext/references/TECH-35-text-on-path.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Calligrams (SDF / pixel-mask / outline): [TECH-38](../amw-pretext/references/TECH-38-calligram-shape.md), [TECH-39](../amw-pretext/references/TECH-39-glyph-mask-calligram.md), [TECH-44](../amw-pretext/references/TECH-44-outline-calligram.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- Typographic ASCII: [TECH-37-typographic-ascii](../amw-pretext/references/TECH-37-typographic-ascii.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

## Activation

No dedicated slash command and no active implementation — this skill is a **redirect stub** only. Any request landing here is routed immediately to `skills/amw-pretext/SKILL.md`, which is invoked by the `design-principles` orchestrator during **Phase B** for all creative text / kinetic typography / calligram deliverables.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Action required

Route every art-focused pretext request to **[`skills/amw-pretext/SKILL.md`](../amw-pretext/SKILL.md)** and pick the matching `category: art` technique from its catalog.
