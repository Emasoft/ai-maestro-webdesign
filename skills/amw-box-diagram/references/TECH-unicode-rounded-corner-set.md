---
name: TECH-unicode-rounded-corner-set
category: ascii-unicode
source: box-diagram-master/skills/amw-box-diagram/SKILL.md
also-in: box-diagram-master/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-unicode-rounded-corner-set — `╭ ╮ ╰ ╯ │ ─` box character set

## What it does

Uses the Unicode rounded-corner box-drawing set as the default glyph
palette: `╭` (top-left) / `╮` (top-right) / `╰` (bottom-left) / `╯`
(bottom-right), with `─` for horizontal and `│` for vertical rules.
Produces a cleaner visual than the classic `+--+` set while still
rendering at exactly 1 column in every mainstream monospace font.

## When to use

Whenever the target surface is a modern terminal, GitHub-rendered code
fence, VS Code Markdown preview, Notion, or Slack code block. For older
terminals and email-client diffs (where UTF-8 may not render reliably)
fall back to the classic set — see `TECH-classic-flowchart-diamond.md`
and its siblings.

## How it works

| Position | Char | Code point |
|---|---|---|
| Top-left corner | `╭` | U+256D |
| Top-right corner | `╮` | U+256E |
| Bottom-left corner | `╰` | U+2570 |
| Bottom-right corner | `╯` | U+256F |
| Horizontal | `─` | U+2500 |
| Vertical | `│` | U+2502 |
| Right arrow | `▸` | U+25B8 |
| Down arrow | `▾` | U+25BE |
| Up arrow | `▴` | U+25B4 |
| Left arrow | `◂` | U+25C2 |

## Minimal example

```
// Source: box-diagram-master/skills/amw-box-diagram/SKILL.md lines 68-70
╭──────────────────╮
│  Content here    │
╰──────────────────╯
```

## Gotchas

- `▼ ▲ ▶ ◀` (U+25BC, U+25B2, U+25B6, U+25C0) are banned — they render at
  variable width in many fonts. Use `▾ ▴ ▸ ◂` instead.
- Mixing `╭╮╰╯` (rounded outer) with `┌┐└┘` (square inner) is an
  intentional pattern: rounded for the outer frame, square for internal
  T-junctions. Don't mix them casually.
- The character set requires UTF-8 — Windows consoles need `chcp 65001`
  or use the classic `+---+` set.

## Cross-references

- [TECH-python-helper-pattern](./TECH-python-helper-pattern.md)
- `../../amw-ascii-validator/references/TECH-safe-char-palette.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

