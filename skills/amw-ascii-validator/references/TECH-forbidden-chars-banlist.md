---
name: TECH-forbidden-chars-banlist
category: ascii-validate
source: ascii-diagram-validator-main/validate_ascii.pl
also-in: ascii-diagram-validator-main/README.md, box-diagram-master/README.md
---

# TECH-forbidden-chars-banlist — ban long/double arrows + filled triangles

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

The validator maintains a curated ban list of arrow glyphs and filled
triangles that render at variable (non-1.0x) width in mainstream
monospaced fonts. Each ban entry includes a severity tier and a
recommended substitution.

## When to use

Any ASCII diagram. These characters slip into LLM-authored diagrams because
they look more "designed" — but they render 1.5x / 2x / 3x in popular fonts
like SF Mono, JetBrains Mono, and Consolas, and shift the entire rest of
the line right by a fractional column.

## How it works

| Severity | Banned | Approx. width | Replace with |
|---|---|---|---|
| CRITICAL | `⟶ ⟵ ⟹ ⟸ ⟷ ⟺` | 3-5x | `──→ ←── ══→ ←══ ←─→ ←═→` or `--> <-- ==> <== <-> <=>` |
| HIGH | `⇒ ⇐ ⇔ ⇑ ⇓ ⇕` | 1.5-2x | `=> <= <=> ^ v ↕` |
| MEDIUM | `▶ ◀ ▲ ▼ ⇆ ⇄` | 1.2-1.5x | `> < ^ v <> ><` or `→ ← ↑ ↓` |

Additional hard bans: emoji (2-col), CJK chars (2-col), tabs (variable).

## Minimal example

```
Bad:  A ──⟶ B       ← U+27F6 renders 3-4x wide; alignment drifts 2-3 cols
Good: A ──→ B       ← U+2192 is single-width in standard monospace
```

## Gotchas

- `→` (U+2192) is 1-col in every standard monospace font and is NOT on the
  ban list — only the longer forms (`⟶` U+27F6, `⇒` U+21D2) are banned.
- `▸` (U+25B8) is allowed (single-width); `▶` (U+25B6) is banned because
  it's classified as "Ambiguous" east-asian-width and renders wide in CJK
  locales.
- Some terminals (Terminal.app on macOS) render `▼` as 1-col; don't trust
  your own eyeballing — the validator is authoritative.

## Cross-references

- [TECH-wide-character-detection](./TECH-wide-character-detection.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../../amw-ascii-creator/SKILL.md) (banned-characters table)
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

