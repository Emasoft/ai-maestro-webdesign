---
name: TECH-style-presets
category: arrow-vocab
source: diagram-skill-main/ASCII-STYLES.md
also-in: diagram-skill-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-style-presets — `detallado` / `unicode` / `clasico` / `compacto`

## What it does

Defines four orthogonal style presets that control the AESTHETIC of a
rendered diagram (glyph set, label density, box shapes) independently of
the diagram's STRUCTURE (nodes + edges). A caller picks one preset to
match the target medium.

## When to use

- `detallado` — Documentation artifacts, review-ready diagrams with
  numbered steps on edges.
- `unicode` — Large diagrams where edge-label clutter would dominate.
- `clasico` — README / maximum-compatibility output; pure ASCII.
- `compacto` — Linear summaries, captions, one-line flows.

## How it works

| Preset | Glyph set | Labels on edges | Width | Use case |
|---|---|---|---|---|
| `detallado` (detailed) | Unicode box-drawing + `▶ ▼ ╭╮╰╯` + semantic shapes | Yes (numbered `1. Request`) | Widest | Review artifacts, high clarity |
| `unicode` | Unicode box-drawing | No | Medium | Large diagrams |
| `clasico` (classic) | Pure ASCII (`+ - | > < v ^`) | Optional | README compatibility |
| `compacto` (compact) | Inline one-line: `A → B → C` with `─┬─` fan-outs | No | Narrowest | Captions, linear flows |

Presets are orthogonal to mode selection:
`--style clasico` + `mode: layers` → ASCII-only layered architecture;
`--style detallado` + `mode: sequence` → Unicode sequence diagram with
labeled messages.

## Minimal example

```
// Source: diagram-skill-main/ASCII-STYLES.md lines 27-36, 71-79, 95-103, 133
detallado (sequence):
┌────────┐  1. Request   ┌──────────┐  2. Process   ┌─────────┐
│ Client │──────────────▶│ Gateway  │──────────────▶│ Service │
└────────┘               └──────────┘               └─────────┘

unicode (no edge labels):
┌────────┐     ┌──────────┐     ┌─────────┐
│ Client │────▶│ Gateway  │────▶│ Service │
└────────┘     └──────────┘     └─────────┘

clasico (pure ASCII):
+--------+     +----------+     +---------+
| Client |---->| Gateway  |---->| Service |
+--------+     +----------+     +---------+

compacto (inline):
Client → Gateway → Service → DB

compacto with fan-out:
Client → Gateway ─┬─→ Service A → DB-A
                  └─→ Service B → DB-B
```

## Gotchas

- Preset naming convention is Spanish in the source skill — `detallado` /
  `clasico` / `compacto`. The plugin preserves these names for
  continuity.
- Mixing presets in one diagram confuses the reader; pick ONE per
  diagram.
- `detallado` uses `▶` which is on the banned character list for the
  ASCII validator — it's acceptable in Unicode-first output formats
  (Mermaid, SVG) but NOT in text-only ASCII artifacts.

## Cross-references

- [TECH-arrow-vocabulary](./TECH-arrow-vocabulary.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../../amw-ascii-creator/SKILL.md) (style presets section)
- [TECH-forbidden-chars-banlist](../../amw-ascii-validator/references/TECH-forbidden-chars-banlist.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
