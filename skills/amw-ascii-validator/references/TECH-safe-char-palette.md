---
name: TECH-safe-char-palette
category: ascii-validate
source: ascii-diagram-validator-main/README.md
also-in: box-diagram-master/skills/amw-box-diagram/validate.py
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-safe-char-palette — the characters that always render 1-col

## What it does

A curated shortlist of box-drawing and arrow characters guaranteed to
render at exactly 1 column in every mainstream monospace font. Authoring
within this palette is the simplest way to produce diagrams that survive
both the validator and copy-paste between editors / terminals / chat.

## When to use

Before authoring any ASCII diagram. This is the palette to copy into scratch
instead of improvising. Any char outside this list should be double-checked
against [TECH-forbidden-chars-banlist](TECH-forbidden-chars-banlist.md) and [TECH-wide-character-detection](TECH-wide-character-detection.md).

## How it works

| Class | Characters | Notes |
|---|---|---|
| Single-line box | `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼` | Most common; editor-safe |
| Double-line box | `═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬` | Emphasis / strong containers |
| Heavy line | `━ ┃ ┏ ┓ ┗ ┛` | Bold borders; fewer junctions available |
| Rounded corners | `╭ ╮ ╰ ╯` | Pair with `─ │` for modern terminal look |
| Safe arrows | `→ ← ↑ ↓ ↔ ↕` | All U+2190-U+2195; all 1-col |
| ASCII fallback | `+ - = \| > < ^ v` | Lowest common denominator |

## Minimal example

```
// Source: ascii-diagram-validator-main/README.md lines 91-98 (Safe Box-Drawing Characters)
Single line:  ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼
Double line:  ═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬
Heavy line:   ━ ┃ ┏ ┓ ┗ ┛
Rounded:      ╭ ╮ ╰ ╯
Arrows:       → ← ↑ ↓ ↔ ↕
```

## Gotchas

- Mixing box-drawing classes in the same diagram usually works (e.g.
  rounded corners + single-line rules), but mixing thickness classes
  (single + heavy) often has no safe junction character — the line change
  is abrupt.
- Double-line junctions (`╠ ╣ ╦ ╩ ╬`) only exist for double-lines. Use them
  for legend boxes / emphasis regions, not for fine-grained wiring.
- The heavy-line class lacks proper T-junctions; use only for outer frames.

## Cross-references

- [TECH-forbidden-chars-banlist](./TECH-forbidden-chars-banlist.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-wide-character-detection](./TECH-wide-character-detection.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../../amw-box-diagram/SKILL.md) (character set table)
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
