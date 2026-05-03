---
name: TECH-classic-annotation-pointer-arrows
category: ascii-classic
source: ascii-diagrams-skill-main/references/graphs-annotations.md
also-in: ascii-diagrams-skill-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-classic-annotation-pointer-arrows — label-to-element connectors

## What it does

Renders pointer-style annotations where a label sits off to the side of
the diagram and connects to a specific element via `+---`, `|`, or arrow
characters. Used for call-outs, field-meaning explanations, and
clarifying specific points in a complex layout.

## When to use

- Register-field documentation (label each bit position)
- File-format annotations (point at specific bytes)
- UI-element call-outs (explain specific widgets)
- Call-outs in code-comment diagrams

## How it works

- Label text on the outside (left, right, above, or below the target).
- `+---` line from the label toward the target.
- `|` vertical segments for multi-row routing.
- Arrow head or `+` at the target.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/graphs-annotations.md lines 22-34
  Exception Masks--+          +---Exception Flags
                   |          |
  Flush-to-zero---+  +----+  +----+
                  |  |    |  |    |
                  FRRMMMMMDEEEEEE
                  ||      |
                  ++      ----Denormals-are-zero
                  |
                  +---Rounding Mode
```

File-format annotation variant (from Chromium):

```
  // +---------------------+
  // |      Header         |
  // +---------------------+
  // |      Part           |
  // +---------------------+
  // |      Part           |
  // +---------------------+
  // |      ...            |
  // +---------------------+
```

## Gotchas

- Crossing annotation arrows becomes unreadable fast; if three annotations
  need to reach the same row, stack the labels vertically and use parallel
  `+---` lines.
- Balance label density — 8+ annotations on a single diagram usually need
  splitting across multiple smaller diagrams.

## Cross-references

- [TECH-classic-bit-field-annotation](./TECH-classic-bit-field-annotation.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [graphs-annotations](./graphs-annotations.md) (legacy pattern file)
  > Directed Graphs · Code Annotations · Before/After Comparisons · UI Sketches
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

