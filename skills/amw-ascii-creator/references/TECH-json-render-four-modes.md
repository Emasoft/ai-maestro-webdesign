---
name: TECH-json-render-four-modes
category: ascii-render
source: perfect-ascii-main/server.py
also-in: perfect-ascii-main/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-json-render-four-modes — JSON → ASCII, four exclusive modes

## What it does

Accepts a JSON object with exactly one top-level key selecting the rendering
mode, and produces pixel-perfect ASCII art. The four modes cover the common
diagram shapes without asking the LLM to hand-align characters.

| Top-level key | Shape it emits |
|---|---|
| `diagram` | Flowcharts, ER diagrams, state machines, block diagrams |
| `table` | Data grids, comparison matrices (auto-splits at 78 chars) |
| `layers` | Layered architecture diagrams with bus connectors |
| `sequence` | Sequence diagrams with lifelines and message arrows |

## When to use

When the diagram has a clear structural shape (nodes+edges / rows+columns /
tiers / actors+messages). The renderer guarantees alignment by construction,
so alignment is not an iteration concern — the author only picks a mode and
fills in content.

## How it works

The caller pipes a JSON string into `bin/amw-ascii-render.py`. The script validates
the JSON has exactly one of the four mode keys, then dispatches to the
corresponding renderer. On invalid input or a width overflow, it exits
non-zero with a readable error; on success, it writes the ASCII to stdout.

## Minimal example

```bash
# Source: perfect-ascii-main/README.md lines 73-76
cat <<'EOF' | python3 bin/amw-ascii-render.py
{"diagram": {"boxes": [{"id": "a", "label": "Hello"}, {"id": "b", "label": "World"}], "grid": [["a"], ["b"]], "connectors": [{"from": "a", "to": "b"}]}}
EOF
```

Output (2-box vertical flowchart):

```
+-------+
| Hello |
+---+---+
    |
    v
+-------+
| World |
+-------+
```

## Gotchas

- Exactly ONE mode key per JSON object; two or more raises an error.
- 78-column hard cap on total width; oversize labels fail with an explicit
  error rather than silently truncating.
- Labels are soft-capped at ~15 chars; longer labels often force width
  overflow in multi-column layouts.

## Cross-references

- [TECH-render-mode-diagram](./TECH-render-mode-diagram.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-render-mode-table](./TECH-render-mode-table.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-render-mode-layers](./TECH-render-mode-layers.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-render-mode-sequence](./TECH-render-mode-sequence.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../../amw-ascii-validator/SKILL.md)
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

