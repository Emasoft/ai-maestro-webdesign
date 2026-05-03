---
name: TECH-ux-process-ideate
category: ux-process
source: SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: UX process — Ideate & Design (Phase 3)

## What it does

The third of five phases. HIGH priority. Phase 3 converts defined problems into wireframes: low → mid → high fidelity. Multiple sketch concepts are explored before any one is committed to.

## When to use

After Phase 2 (Define) produces personas, journey maps, and problem statements. Run Phase 3 before any engineering work begins — wireframes catch flow problems before code does.

## How it works

Three fidelity rungs:

- **Low-fidelity** (paper / ASCII / box sketches) — explore 3+ concepts per problem. Cheap and fast; the point is to generate alternatives, not to refine.
- **Mid-fidelity** (greyscale wireframes) — pick 1-2 concepts from low-fi and flesh them out. No color, no brand, no real copy. Shows layout, hierarchy, content adjacency.
- **High-fidelity** (designed mockups) — apply the design system to the selected wireframe. Real copy, real imagery, real colors. Pixel-level decisions.

Responsive coverage is mandatory: 375 / 768 / 1024 / 1440 at minimum.

This phase is where the plugin's `ascii-sketch` skill lives — the ASCII-first plan phase IS low-fidelity ideation, and the user iterates on ASCII variants before any HTML is produced.

## Minimal example

For Sarah's "reorder basics in 90 seconds" problem, three low-fi concepts:

1. **Home-screen recents** — last 5 orders as big cards on home, one-tap reorder
2. **Persistent basics rail** — fixed row of 6 items (user-customized) always visible
3. **SMS reorder** — no app, a reply-with-"basics" SMS flow

Cheapest to test: #2. Build a greyscale wireframe, walk Sarah through it in a 20-min usability test.

*Attributed to the ux-designer skill — `SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md`.*

## Gotchas

- Skipping low-fi to jump straight into high-fi mockups is how teams fall in love with a bad idea. The 3-concept sketch pass exists specifically to prevent this.
- "One primary CTA per screen" is a hard rule in this phase — competing CTAs always signal unresolved hierarchy.
- Mid-fi in greyscale is deliberate: it tests layout, not brand. Adding color at this stage makes reviewers comment on color instead of structure.
- The plugin's ASCII-first workflow replaces low-fi sketches with ASCII variants — same purpose, 1% of the iteration cost.

## Cross-references

- [TECH-ux-process-define](TECH-ux-process-define.md) — upstream (Phase 2)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-ux-process-prototype](TECH-ux-process-prototype.md) — downstream (Phase 4)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../../amw-ascii-sketch/SKILL.md) — ASCII-first implementation of this phase
- [SKILL](../SKILL.md)
