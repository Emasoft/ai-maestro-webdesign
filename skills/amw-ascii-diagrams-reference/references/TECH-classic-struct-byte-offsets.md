---
name: TECH-classic-struct-byte-offsets
category: ascii-classic
source: ascii-diagrams-skill-main/references/data-structures.md
also-in: ascii-diagrams-skill-main/SKILL.md
---

# TECH-classic-struct-byte-offsets — packet/struct layout with byte scale

## What it does

Renders a binary struct, packet header, or memory layout with byte offsets
above the box, field names inside, and field type / size labeled below.
The classic "Offset 0 / 4 / 8 / 12" header strip anchors every diagram.

## When to use

- Network packet headers (IP, TCP, UDP, application protocols)
- Binary file formats (PNG, MP4 box, ELF section headers)
- In-memory struct layouts (C `struct`, FFI ABI docs)
- Firmware register layouts with variable-length payloads

## How it works

- Top row is the byte-offset scale: `Offset  0  4  8  12  16`.
- Each field is a cell in a row of `+---+---+---+---+` separators.
- Field name goes on line 1 inside the cell; field type/size on line 2.
- Variable-length payloads render as a taller cell with `|  payload (variable)  |` spanning multiple inner lines.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/data-structures.md lines 6-16
  Offset  0         4         8        12        16
          +---------+---------+---------+---------+
          |  magic  |  version|  flags  |  length |
          | (uint32)| (uint16)| (uint16)| (uint32)|
          +---------+---------+---------+---------+
          |                                       |
          |            payload (variable)          |
          |                                       |
          +---------------------------------------+
```

## Gotchas

- Keep same-size fields at the same box width for visual comparison.
- Variable-length fields need an explicit `(variable)` label — otherwise
  the reader may assume it's fixed at the box's apparent width.
- Bit-field layouts (sub-byte fields inside a register) need a different
  pattern — see `./TECH-classic-bit-field-annotation.md`.

## Cross-references

- `./TECH-classic-bit-field-annotation.md`
- `./TECH-classic-linked-list.md`
- `./data-structures.md` (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

