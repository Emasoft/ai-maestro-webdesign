---
name: TECH-78-column-cap
category: ascii-render
source: perfect-ascii-main/server.py
also-in: perfect-ascii-main/README.md
---

# TECH-78-column-cap — hard 78-col rule and its consequences

## What it does

The renderer enforces a hard 78-column ceiling on every rendered diagram and
errors out (non-zero exit) when exceeded. This is the reason the renderer
can be trusted — the caller knows up-front whether a diagram fits, instead
of discovering truncation after paste.

## When to use

Always. This is an invariant, not a technique you opt into. The authoring
implication is: keep labels short, split wide architectures into multiple
diagrams, and prefer vertical (more rows) over horizontal (more columns).

## How it works

Before emitting the final buffer, the renderer computes `max(len(row) for
row in output_lines)`. If that value exceeds 78, the script writes an error
to stderr and exits non-zero. No truncation, no silent clipping.

## Minimal example

```bash
# Source: perfect-ascii-main/README.md lines 63-64 ("78-column max width")
# This call will succeed:
echo '{"diagram":{"boxes":[{"id":"a","label":"Hi"}],"grid":[["a"]],"connectors":[]}}' | python3 bin/amw-ascii-render.py

# This call errors — the label is longer than the usable width in a 3-column layer:
echo '{"layers":{"levels":[{"label":"L","boxes":["A very long label that will not fit","B","C"]}],"connections":"between_layers"}}' | python3 bin/amw-ascii-render.py
```

## Gotchas

- 78 is chosen for terminal-paste safety (classic `$COLUMNS=80` minus 2-col
  safety margin). GitHub allows wider but the cap protects the lowest
  common denominator.
- Wide tables auto-split at 78, BUT other modes error out — you must
  redesign.
- Layer labels on the left margin count toward the 78-col cap.

## Cross-references

- `./TECH-json-render-four-modes.md`
- `../../amw-ascii-validator/references/TECH-width-mismatch-rule.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

