---
name: TECH-validate-before-emit
category: ascii-validate
source: box-diagram-master/skills/amw-box-diagram/SKILL.md
also-in: ascii-diagram-validator-main/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-validate-before-emit — never show un-validated ASCII

## What it does

Every skill that emits ASCII (sketches, flowcharts, wireframes,
architecture diagrams) MUST run the validator before the output reaches
the user. If the validator fails, apply its `FIX:` hints, re-validate,
loop. Only present ASCII that passed.

## When to use

Any authoring flow whose final artifact is ASCII. This is the non-
negotiable contract that makes perfect-ASCII trustworthy — the user reads
exactly what they would read in production, so a 1-col-off rectangle
erodes trust in every subsequent variant.

## How it works

The canonical loop (adapted from `box-diagram-master/skills/amw-box-diagram/SKILL.md`
workflow step 4-6):

```
1. Generate the diagram
2. Write to a temp file
3. Run: python3 bin/amw-validate-ascii.py <file>
4. If PASS → present to the user FROM THE FILE (never re-typed)
5. If FAIL → apply every FIX: hint, goto 3
6. After N retries with no convergence, STOP and propose a redesign
```

Output from the validated file — never re-type the diagram. Even one lost
space between the read and the paste breaks every corner below it.

## Minimal example

```bash
# Source: box-diagram-master/skills/amw-box-diagram/SKILL.md lines 17-22 (Workflow)
python bin/amw-validate-ascii.py /tmp/diagram.txt > /tmp/validator-out.txt
if [ $? -ne 0 ]; then
  # apply FIX: hints from /tmp/validator-out.txt, retry
  :
else
  cat /tmp/diagram.txt
fi
```

## Gotchas

- "Looks good in my context window" is NOT validation. LLMs cannot count
  characters reliably; the validator is how the plugin compensates.
- Cap iteration at ~8 retries. After that, the brief is likely structurally
  impossible at the chosen frame width — propose widening or splitting.
- Never re-type from memory. Always read the file back and paste its exact
  bytes into the code fence.

## Cross-references

- [TECH-fix-hint-actionable-format](./TECH-fix-hint-actionable-format.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../../amw-ascii-creator/SKILL.md) (Mode B workflow step 4-7)
- [SKILL](../../amw-box-diagram/SKILL.md) (Workflow section)
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
