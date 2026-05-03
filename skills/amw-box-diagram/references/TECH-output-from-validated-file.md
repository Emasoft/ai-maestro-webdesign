---
name: TECH-output-from-validated-file
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


# TECH-output-from-validated-file — read back, never re-type

## What it does

After the validator passes, the author reads back the validated file
byte-for-byte and pastes it into the reply. Re-typing the diagram from
memory — even after the eye has just seen it pass — is the single most
common silent-corruption bug.

## When to use

Always, at the end of every authoring loop. This is a process rule, not
a visual technique, but it is the difference between "this diagram
worked in my scratch but broke in the user's chat" and "the diagram
works".

## How it works

```bash
# 1. Validate in a loop until PASS
python3 bin/amw-validate-ascii.py /tmp/diagram.txt
# exit 0 → continue

# 2. Read back
cat /tmp/diagram.txt

# 3. Paste the output into the reply INSIDE a code fence; no editing
```

Never:

```
# BAD
# "the diagram passed validation, here it is:"
# [author re-types the diagram from memory]
```

## Minimal example

```bash
# Source: box-diagram-master/skills/amw-box-diagram/SKILL.md lines 21-22, 43-45
python bin/amw-validate-ascii.py /tmp/diagram.txt   # PASS
cat /tmp/diagram.txt                       # ← read back
# paste the exact bytes of cat's output into the reply
```

## Gotchas

- Even experienced authors underestimate how easy it is to drop one
  trailing space while re-typing. That's one validator failure in the
  user's context, not in your scratch.
- Some editors / shells normalize whitespace on paste; double-check
  trailing spaces survive the round trip.
- If the reply platform strips trailing whitespace (some Markdown
  renderers do), wrap the paste in a triple-backtick code fence without
  a language tag — bare ``` preserves whitespace.

## Cross-references

- [TECH-validate-before-emit](../../amw-ascii-validator/references/TECH-validate-before-emit.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-fix-hint-actionable-format](../../amw-ascii-validator/references/TECH-fix-hint-actionable-format.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

