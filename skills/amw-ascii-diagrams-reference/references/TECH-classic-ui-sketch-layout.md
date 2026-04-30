---
name: TECH-classic-ui-sketch-layout
category: ascii-classic
source: ascii-diagrams-skill-main/references/graphs-annotations.md
also-in: ascii-diagrams-skill-main/SKILL.md
---

# TECH-classic-ui-sketch-layout — `+---+` UI wireframe mockup

## What it does

Renders a low-fidelity UI layout sketch — header, sidebar, main content,
footer — using classic `+---+`, `|`, and `-`. Used for quick interface
mockups in PRs, issues, and design docs where Figma/Sketch is overhead.

## When to use

- Initial UI sketches in GitHub issues ("here's what I'm thinking")
- Code-comment mockups explaining component layout
- ADR attachments showing the proposed UI shape
- Chat-based brainstorms where a real mockup is overkill

## How it works

- Outer frame: header bar on top, footer bar on bottom.
- Left sidebar with nav items (` - Item 1 ` etc).
- Main content area with placeholder boxes (`Card 1`, `Card 2`).
- Fixed-width columns; visual balance matters more than pixel-accurate
  proportions.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/graphs-annotations.md lines 76-90
  +------------------------------------------+
  | [Logo]    Navigation          [User Menu] |
  +------------------------------------------+
  |          |                                |
  | Sidebar  |         Main Content           |
  |          |                                |
  | - Item 1 |   +--------+  +--------+      |
  | - Item 2 |   | Card 1 |  | Card 2 |      |
  | - Item 3 |   +--------+  +--------+      |
  |          |                                |
  +----------+--------------------------------+
  | Footer                                    |
  +------------------------------------------+
```

## Gotchas

- This pattern is for ROUGH layout only; for final design deliverables,
  use `../../amw-ascii-sketch/` (plan-phase, 3 variants) then
  `/amw-ascii-to-html` to convert.
- Nested boxes inside the main content area need column alignment —
  `Card 1` / `Card 2` must share a row, with consistent widths.
- For mobile-first layouts, a narrower frame (40-50 cols) reads more
  honestly than squeezing into desktop proportions.

## Cross-references

- `../../amw-ascii-sketch/SKILL.md`
- `../../amw-ascii-creator/SKILL.md` (Mode B freeform wireframes)
- `./graphs-annotations.md` (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

