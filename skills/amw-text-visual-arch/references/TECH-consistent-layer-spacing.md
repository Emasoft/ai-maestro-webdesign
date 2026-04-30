---
name: TECH-consistent-layer-spacing
category: text-visual-arch
source: cc-plugin-text-visualizations-main/skills/tools-visual-ascii-arch/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-consistent-layer-spacing — fixed grid + 2-space layer separator

## What it does

Enforces a consistent layout grid in an ASCII architecture diagram: each
layer is a horizontal row; layers are separated by exactly 2 blank lines
(or a single line of vertical connectors plus a blank). Every node in a
layer uses the same box width.

## When to use

Always on, for every layered architecture diagram. Inconsistent spacing
makes a diagram read as if it has bugs the reader must decode.

## How it works

- **Horizontal:** every node in one layer shares one `inner_width`. If
  nodes naturally differ in label length, pick the longest and pad the
  others.
- **Vertical:** exactly 2 spaces between the bottom of one layer and the
  top of the next, OR one line of connector glyphs + 1 blank line.
- **Indent:** consistent left-margin for the whole diagram. Don't let
  a sub-layer drift right.

## Minimal example

```
// Adapted from: cc-plugin-text-visualizations-main/skills/tools-visual-ascii-arch/SKILL.md lines 22-24 (Apply layout grid)
+---------+  +---------+  +---------+    ← Layer 1: Presentation
|  Web    |  | Mobile  |  |  CLI    |
+----+----+  +----+----+  +----+----+
     |            |            |
     +------------+------------+         ← connectors
                  |
             +----v----+                  ← Layer 2: Gateway
             | API Gw  |
             +---------+
```

## Gotchas

- Pad the labels with trailing spaces to reach the chosen `inner_width`
  — "Web" must render as `| Web     |` inside a 9-char box, not
  `| Web |`.
- If one layer has 3 nodes and the next has 1, CENTER the single node
  under the 3-way fan-in — don't leave it left-justified.
- Max layer depth that fits in a terminal screen: 4-5 before the top
  scrolls out of view.

## Cross-references

- `../../amw-ascii-creator/references/TECH-render-mode-layers.md`
- `./TECH-c4-zoom-levels.md`
- `../../amw-box-diagram/references/TECH-fan-out-fan-in-junctions.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

