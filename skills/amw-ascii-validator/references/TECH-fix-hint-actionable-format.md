---
name: TECH-fix-hint-actionable-format
category: ascii-validate
source: ascii-diagram-validator-main/validate_ascii.pl
also-in: ascii-diagram-validator-main/README.md
---

# TECH-fix-hint-actionable-format — every finding carries a mechanical FIX:

## What it does

The validator does not stop at "FAIL: bad". Each finding includes a
mechanical `FIX:` instruction naming the exact line, column, and action to
take ("Add 1 space", "Move `│` right by 1 position", "Substitute `⟶` with
`──→` at col 27"). An automated iteration loop can apply every FIX
verbatim without reasoning.

## When to use

Any authoring loop where a downstream skill (e.g. `ascii-sketch` /
`ascii-creator` in Mode B) applies validator findings automatically until
PASS. The FIX: contract is what makes the loop terminate without human
intervention.

## How it works

Each finding follows a uniform shape:

```
Line <L>, Col <C>: [<CODE>] <human-readable failure>. FIX: <mechanical instruction>
```

`<CODE>` is one of: `WIDTH_MISMATCH`, `VERTICAL_MISALIGNED`,
`BROKEN_BORDER`, `WIDE_CHAR`, `FORBIDDEN_CHAR_CRITICAL`,
`FORBIDDEN_CHAR_HIGH`, `FORBIDDEN_CHAR_MEDIUM`, `TAB_CHAR`.

`FIX:` is always an imperative sentence naming the precise edit.

## Minimal example

```
// Source: ascii-diagram-validator-main/README.md lines 81-83
1. Line   2, Col  23: [WIDTH_MISMATCH] Line has width 22, expected 23
   (off by -1). FIX: Add 1 space(s) to pad this line to width 23
```

An iteration loop would:

```bash
# Parse L=2, action="Add 1 space(s)" — apply, re-validate.
sed -i '2s/$/ /' /tmp/diagram.txt
python3 bin/amw-validate-ascii.py /tmp/diagram.txt
# Loop until exit 0.
```

## Gotchas

- When multiple findings on the same line conflict (e.g. "add 2 spaces" and
  "remove 1 space"), apply in the order the validator reports them — the
  validator emits them top-to-bottom left-to-right, which is the order a
  naive line-by-line re-validate will reconverge against.
- Applying all fixes in one pass is rarely safe; re-validate after each
  fix until no findings remain.

## Cross-references

- `./TECH-width-mismatch-rule.md`
- `./TECH-vertical-line-continuity.md`
- `./TECH-forbidden-chars-banlist.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

