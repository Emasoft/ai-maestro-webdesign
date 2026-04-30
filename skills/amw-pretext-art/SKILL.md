---
name: amw-pretext-art
description: Deprecated. See ../amw-pretext/ for the unified pretext skill. This file is a redirect stub only.
version: 0.2.0
---

# pretext-art (MOVED TO `skills/amw-pretext/`)

The full pretext capability — Canvas / SVG creative text effects AND all API / measurement / layout / integration / tables / 3D / workflow / consult techniques — now lives at:

**[`skills/amw-pretext/SKILL.md`](../amw-pretext/SKILL.md)**

The original 8 pretext-art effects (kinetic / shaped / wavy / tapering / poster-grid / custom / text-on-path / per-line-metrics) are catalogued as TECH files in `skills/amw-pretext/references/`, alongside ~70 other techniques:

- Kinetic typography: [TECH-33-kinetic-width-animation](../amw-pretext/references/TECH-33-kinetic-width-animation.md)
- Shaped containers: [TECH-19-shaped-container](../amw-pretext/references/TECH-19-shaped-container.md)
- Wavy baseline: [TECH-34-wavy-baseline](../amw-pretext/references/TECH-34-wavy-baseline.md)
- Tapering font size: [TECH-28-tapering-font-size](../amw-pretext/references/TECH-28-tapering-font-size.md)
- Generative poster grid: [TECH-36-generative-poster-grid](../amw-pretext/references/TECH-36-generative-poster-grid.md)
- Text on a path: [TECH-35-text-on-path](../amw-pretext/references/TECH-35-text-on-path.md)
- Calligrams (SDF / pixel-mask / outline): [TECH-38](../amw-pretext/references/TECH-38-calligram-shape.md), [TECH-39](../amw-pretext/references/TECH-39-glyph-mask-calligram.md), [TECH-44](../amw-pretext/references/TECH-44-outline-calligram.md)
- Typographic ASCII: [TECH-37-typographic-ascii](../amw-pretext/references/TECH-37-typographic-ascii.md)

## Activation

No dedicated slash command and no active implementation — this skill is a **redirect stub** only. Any request landing here is routed immediately to `skills/amw-pretext/SKILL.md`, which is invoked by the `design-principles` orchestrator during **Phase B** for all creative text / kinetic typography / calligram deliverables.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Action required

Route every art-focused pretext request to **[`skills/amw-pretext/SKILL.md`](../amw-pretext/SKILL.md)** and pick the matching `category: art` technique from its catalog.
