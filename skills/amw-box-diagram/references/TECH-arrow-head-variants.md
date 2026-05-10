---
name: TECH-arrow-head-variants
category: ascii-unicode
source: box-diagram-master/skills/amw-box-diagram/SKILL.md
also-in: diagram-skill-main/ASCII-STYLES.md, box-diagram-master/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-arrow-head-variants — `▸ ▾ ▴ ◂` vs banned `▶ ▼ ▲ ◀`

## What it does

Uses the SMALL-triangle variants `▸ ▾ ▴ ◂` (U+25B8 / U+25BE / U+25B4 /
U+25C2) for directional arrowheads, which are single-width in every
mainstream monospace font. Avoids the LARGE-triangle set `▶ ▼ ▲ ◀`
(U+25B6 / U+25BC / U+25B2 / U+25C0) which is variable-width in many
fonts (ambiguous east-asian-width) and breaks alignment.

## When to use

Any Unicode box diagram that needs directional cues. Also applies to
connectors inside structured diagrams — the same rule holds whenever a
human author writes the arrowhead by hand.

## How it works

| Direction | Use | Avoid |
|---|---|---|
| Right | `▸` (U+25B8) | `▶` (U+25B6) |
| Down | `▾` (U+25BE) | `▼` (U+25BC) |
| Up | `▴` (U+25B4) | `▲` (U+25B2) |
| Left | `◂` (U+25C2) | `◀` (U+25C0) |

For content inside boxes (labels), inline arrows `→ ← ↑ ↓` (U+2190-93)
are safe — they're narrow-ambiguous but consistently 1-col in all
mainstream monospace fonts used for code.

## Minimal example

```
// Source: box-diagram-master/skills/amw-box-diagram/SKILL.md lines 102-107
Horizontal:   ──────────▸     ◂──────────     ◂──────────▸
Vertical:     │               ▴
              │               │
              ▾               │
```

## Gotchas

- The difference between `▶` (U+25B6) and `▸` (U+25B8) is invisible at a
  glance — always copy from the safe-char palette, don't type by hand.
- `→` inside a content label is fine; `▸` outside (as a connector
  arrowhead) is fine; mixing them inconsistently looks messy.
- The validator rejects all four banned chars (`▶ ▼ ▲ ◀`) as
  `FORBIDDEN_CHAR_MEDIUM`.

## Cross-references

- [TECH-forbidden-chars-banlist](../../amw-ascii-validator/references/TECH-forbidden-chars-banlist.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-safe-char-palette](../../amw-ascii-validator/references/TECH-safe-char-palette.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-unicode-rounded-corner-set](./TECH-unicode-rounded-corner-set.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
