---
name: TECH-classic-linked-list
category: ascii-classic
source: ascii-diagrams-skill-main/references/data-structures.md
also-in: ascii-diagrams-skill-main/SKILL.md
---

# TECH-classic-linked-list — head → node → node → NULL chain

## What it does

Renders a singly- or doubly-linked-list data structure as a row of boxed
nodes with `-->` arrows between them, terminating in `NULL`. Multi-field
nodes show the `data` slot on an inner line.

## When to use

- Kernel-data-structure docs (Linux `struct list_head`)
- LeetCode / interview prep docs
- Tutorial visualizations for students learning pointer semantics

## How it works

- Each node is a 2-line box: header line + `data` line.
- `-->` between nodes (singly linked).
- `<->` between nodes for doubly linked lists.
- The final `-->NULL` anchors the terminator.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/data-structures.md lines 19-24
  +------+    +------+    +------+
  | head |--->| node |--->| node |--->NULL
  | data |    | data |    | data |
  +------+    +------+    +------+
```

Stack/queue variant (source: lines 27-35):

```
  TOP --> +-------+
          | item3 |
          +-------+
          | item2 |
          +-------+
          | item1 |     BOTTOM
          +-------+
```

## Gotchas

- For very long lists, use ellipsis mid-chain: `head --> ... --> node --> NULL`.
- Circular / cyclic lists need an arrow going back to the head — route it
  underneath the chain to avoid crossing the forward arrows.
- Pointer arithmetic diagrams (arrays of structs) are better drawn with
  `TECH-classic-struct-byte-offsets.md`.

## Cross-references

- `./TECH-classic-struct-byte-offsets.md`
- `./data-structures.md` (legacy pattern file)
- [`../SKILL.md`](../SKILL.md) — parent skill

