---
trdd-id: 0TBHW83S
title: Adjudicate the 37 frozen HIGH skill-trigger collisions
column: completed
created: 2026-08-18T23:35:11+0200
updated: 2026-08-19T10:40:00+0200
current-owner: webdesign-session
task-type: audit
approval-tier: 0
created-by: TRDD-NN3X00Q6 follow-up (ratchet froze the debt, this card pays it down)
---

## Context

`tests/test_skill_trigger_collisions.py` ratchets `bin/amw-skill-trigger-collision.py`'s
HIGH count at the frozen baseline **37** (measured 2026-08-18; total=105 high=37 low=68).
The ratchet stops growth; this card is the pay-down. Unknown split between real
orchestrator-routing ambiguities (two skills claiming one trigger phrase, e.g.
"architecture flowchart sequence" → amw-diagram-editorial vs amw-html-diagram) and
detector noise.

## Work

Per HIGH collision: read both SKILL.md descriptions, decide REAL (narrow one
description per the CLAUDE.md "orchestrator priority" invariant) or NOISE (justify;
consider the tool's `--exclude` for structural false positives). Lower `HIGH_BASELINE`
in the test as debt is paid; each drop must come with the fix that earned it.

## Acceptance

- Every one of the 37 has a written REAL/NOISE verdict (report in reports/).
- `HIGH_BASELINE` lowered to the residual justified-noise count, test green.
- No skill description re-claims the broad design vocabulary owned by
  amw-design-principles.

## Approval log

- 2026-08-19T10:40:00+0200 — COMPLETED by webdesign-session (Tier 0). All 37 HIGHs adjudicated (17 REAL fixed, 19 NOISE via principled detector corrections, 1 justified residual); HIGH_BASELINE 37 -> 1; suite 245 passed/6 skipped. Verdicts: reports/trigger-collision-adjudication/. Commit 68fe6a2.
