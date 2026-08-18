---
trdd-id: NN3X00Q6
title: Wire amw-skill-trigger-collision.py into an actual gate
column: todo
created: 2026-08-18T19:52:25+0200
updated: 2026-08-18T19:52:25+0200
current-owner: webdesign-session
task-type: infra
approval-tier: 0
created-by: phase2-audit-remediation (hub dispatch, TRDD-BRRJK57P)
---

## Defect (Phase-1 audit, axis 4 / CONFIRMED-2)

`bin/amw-skill-trigger-collision.py` works (live run exits 1, summary total=105 high=37)
but is wired into NOTHING: not `.github/workflows/`, not pytest, not `commands/amw-doctor.md`
— despite `CLAUDE.md:365` calling it a "CI-time gate". It passes by never running.

## Change (ratchet, not big-bang)

37 pre-existing HIGH collisions are NOT adjudicated; a strict gate would red CI on day one
without fixing anything. Wire it as a RATCHET:
1. Add `tests/test_skill_trigger_collisions.py` that runs the tool and asserts
   `high <= BASELINE` (BASELINE = today's measured high count, stored as a constant with a
   comment explaining the ratchet). New collisions fail; existing debt is visible, frozen.
2. Add the tool to `commands/amw-doctor.md` so `/amw-doctor` surfaces the live counts.
3. Adjudicating the 37 down to 0 is FUTURE work — its own TRDD when someone owns it; this
   card only stops the count growing.

## Acceptance

- pytest runs the tool (real subprocess, no mock); a synthetic new collision (plant) raises
  `high` above baseline and fails; revert restores green.
- `/amw-doctor` doc lists the check.
