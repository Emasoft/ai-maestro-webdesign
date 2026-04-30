---
name: TECH-73-design-consultation-route
category: consult
source: pretext-skills/SKILL-20.md (gstack design-consultation)
also-in: SKILL-18.md, SKILL-22.md, SKILL-24.md
---

# Full-pipeline design consultation (gstack design-html)

**Category:** consult
**Status:** stable

## What it does

SKILL-20 / SKILL-22 / SKILL-24 describe a full-pipeline gstack-style design consultation that uses pretext as the HTML layout engine. Flow: `design-consultation` creates DESIGN.md → `design-shotgun` generates mockups → `design-html` finalizes pretext-native HTML/CSS (text actually reflows, heights computed, layouts dynamic). 30 KB overhead, zero deps.

## When to use

- Full-project design systems
- Teams adopting gstack as their skill framework
- Multi-step design pipelines (brand → mockup → HTML)

## How it works

The gstack design pipeline:
1. `/plan-design-review` — infer design system from existing site
2. `/design-consultation` — new project: produce DESIGN.md source of truth
3. `/design-shotgun` — generate 3-6 variant mockups
4. `/design-html` — turn the approved mockup into pretext-native HTML

Pretext sits inside step 4, handling:
- Exact height pre-measurement for hero sections
- Shrink-wrapped chat bubbles / tooltips
- Editorial-engine obstacle routing for gallery pages
- Masonry / virtualized lists in product pages

## Minimal example

Not a single snippet — it's a multi-session pipeline. Refer to SKILL-20 / SKILL-22 / SKILL-24 preambles.

## Gotchas

- The gstack pipeline (including SKILL-20 preamble) depends on `~/.claude/skills/gstack/` being installed — not bundled in this plugin.
- Voice triggers (speech-to-text): "build the design", "code the mockup", "make it real" — all route to `design-html`.

## Cross-references

- Related: TECH-72-use-pretext-decision-guide, all workflow techniques
- API reference: N/A — process-level guide
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
