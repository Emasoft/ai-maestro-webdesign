---
name: TECH-classic-bit-field-annotation
category: ascii-classic
source: ascii-diagrams-skill-main/references/data-structures.md
also-in: ascii-diagrams-skill-main/references/graphs-annotations.md
---

# TECH-classic-bit-field-annotation — bit-width register layout

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Renders a register or packed bit-field with a bit-position scale on top,
individual bit cells, and grouped-field annotations below. Used for
processor status-register docs, FPU control-word layouts, and low-level
protocol fields where fewer-than-byte fields matter.

## When to use

- Processor flag registers (`N Z C V` at bits 31-28 of ARM CPSR)
- FPU control words (Flush-to-zero, rounding mode, exception masks)
- Compact binary protocol fields (QUIC short-packet header, CoAP options)

## How it works

- Top strip: bit positions scaled to columns (`31  30  29  28 | 27 ...`).
- Cell strip: each bit gets one cell; grouped bits (e.g. exception masks
  at bits 27-24) span multiple cells.
- Bottom strip: field-name labels under the bit strips, often with
  annotations pointing at specific bits with arrows.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/data-structures.md lines 37-44
  31  30  29  28 | 27  26  25  24 | 23 ... 16 | 15 ... 8 | 7 ... 0
  +---+---+---+--+---+---+---+---+-----------+----------+---------+
  | N | Z | C | V|   |   |   |   |           |          |         |
  +---+---+---+--+---+---+---+---+-----------+----------+---------+
  |    Flags     |   Reserved    |   Type    |  Length   | Opcode  |
```

With pointer-style annotation (source: graphs-annotations.md lines 23-32):

```
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

## Gotchas

- Bit positions vary by architecture — MSB-0 vs LSB-0. State the
  convention in a caption.
- Annotations with `+---` arrows eat vertical space; prefer them for
  diagrams where the annotation IS the point (register docs), not where
  the layout is the point ([TECH-classic-struct-byte-offsets](TECH-classic-struct-byte-offsets.md)).

## Cross-references

- [TECH-classic-struct-byte-offsets](./TECH-classic-struct-byte-offsets.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-annotation-pointer-arrows](./TECH-classic-annotation-pointer-arrows.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [data-structures](./data-structures.md), [graphs-annotations](./graphs-annotations.md) (legacy pattern files)
  > [graphs-annotations.md] Directed Graphs · Code Annotations · Before/After Comparisons · UI Sketches
  > Reference
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

