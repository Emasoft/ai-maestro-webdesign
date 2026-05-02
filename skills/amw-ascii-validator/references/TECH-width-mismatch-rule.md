---
name: TECH-width-mismatch-rule
category: ascii-validate
source: ascii-diagram-validator-main/validate_ascii.pl
also-in: ascii-diagram-validator-main/README.md, box-diagram-master/skills/amw-box-diagram/validate.py
---

# TECH-width-mismatch-rule — every frame line shares one display width

## What it does

The validator asserts that every line in a framed ASCII diagram has the same
**display width** (accounting for wide characters). Any deviation produces a
`WIDTH_MISMATCH` finding with a precise `FIX: Add N space(s) to pad this line
to width X` hint.

## When to use

Hand-authored rectangular wireframes: dashboards, mobile frames, editorial
layouts, newspaper-column mockups. Any artifact whose visual integrity
depends on a stable right edge.

## How it works

The Perl validator picks the **globally most-common line width** as the
expected width and flags every deviation. The Python port groups consecutive
lines that share box-char column positions into one structural group and
computes the expected width per group — reducing false positives on
diagrams with multiple independent structures.

## Minimal example

```
# Source: ascii-diagram-validator-main/README.md lines 70-89 (Example output)
Status: FAIL
Lines: 3, Expected Width: 23 characters

Issues Found:
  1. Line   2, Col  23: [WIDTH_MISMATCH] Line has width 22, expected 23 (off by -1).
     FIX: Add 1 space(s) to pad this line to width 23
```

## Gotchas

- Trailing whitespace matters. A line ending at col 22 when the frame is
  width 23 requires one trailing space.
- Authors using `String.trimEnd()` on every line will silently strip the
  padding the validator expects — do NOT trim right before saving.
- Wide characters (emoji, CJK) count as 2 cols; a single emoji on one line
  requires 1 fewer trailing space than an emoji-free line to hit the same
  width.

## Cross-references

- [TECH-fix-hint-actionable-format](./TECH-fix-hint-actionable-format.md)
- [TECH-group-aware-width-detection](./TECH-group-aware-width-detection.md)
- [TECH-wide-character-detection](./TECH-wide-character-detection.md)
- [`../SKILL.md`](../SKILL.md) — parent skill

