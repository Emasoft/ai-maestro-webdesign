---
name: TECH-wide-character-detection
category: ascii-validate
source: box-diagram-master/skills/amw-box-diagram/validate.py
also-in: ascii-diagram-validator-main/validate_ascii.pl, ascii-diagram-validator-main/README.md
---

# TECH-wide-character-detection — flag CJK/emoji double-width chars

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

The validator walks every character in every line, computes its display
width via `unicodedata.east_asian_width`, and flags any char whose category
is `W` (Wide) or `F` (Fullwidth) — all CJK ideographs and all emoji. A
single wide char on a line in a fixed-width-font grid pushes every
subsequent char one column to the right, breaking alignment of the frame.

## When to use

Always on. Emoji crept into "ASCII" diagrams is the second-most-common
alignment bug after width mismatches. Any diagram whose content includes
user-supplied strings (quotes, comments, labels pulled from a DB) needs
this check even if the author ran it on a clean template.

## How it works

```python
# Source: box-diagram-master/skills/amw-box-diagram/validate.py lines 33-41
def char_width(ch):
    if ord(ch) < 32:
        return 0
    cat = unicodedata.east_asian_width(ch)
    if cat in ("W", "F"):
        return 2
    return 1
```

If `char_width(ch) > 1`, a finding is added: `Line N, char M: double-width
character '<ch>' (U+NNNN) breaks monospace alignment`.

## Minimal example

```
Bad:  │ Hello 🔴 World │       ← emoji = 2 cols, frame right-edge drifts
Good: │ Hello [!] World │      ← bracket marker = 1 col, frame stays aligned
```

## Gotchas

- The check uses the Unicode database; it correctly flags emoji with ZWJ
  joiners (`👨‍👩‍👧‍👦` is treated as the composing chars, each of which is wide).
- Variation selectors (U+FE0F) that force emoji-presentation don't render
  as wide chars in all fonts, but the validator flags the base char.
- Combining characters (diacritics) have category `N` (neutral), not `W`,
  and are allowed — but they visually overlay the previous char, which can
  still confuse alignment. Use plain ASCII labels.

## Cross-references

- [TECH-78-column-cap](../../amw-ascii-creator/references/TECH-78-column-cap.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-forbidden-chars-banlist](./TECH-forbidden-chars-banlist.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

