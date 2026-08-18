---
trdd-id: LR5ERAXT
title: Give R22 self-ID byline a mechanical enforcement surface
column: completed
created: 2026-08-18T19:52:25+0200
updated: 2026-08-18T20:20:00+0200
current-owner: webdesign-session
task-type: infra
approval-tier: 0
created-by: phase2-audit-remediation (hub dispatch, TRDD-BRRJK57P)
---

## Defect (Phase-1 audit, axis 2 / F7)

R22 (every GitHub write opens with the self-ID line) is documented at `CLAUDE.md:287-292`
and as PRRD `G1.1`, but has ZERO enforcement surface — no test, script, hook, or CI step.
Contrast: R23 has `tests/test_no_bare_handles.py`.

## Change (scoped — full automation is impossible)

The byline is prose written at gh-write time, so a repo artifact cannot gate it fully.
What CAN be enforced mechanically: any TEMPLATE the repo ships for GitHub-bound text
must carry the self-ID line. Add `tests/test_r22_selfid_templates.py`:
- scan `.github/` issue/PR templates (if any) and any repo file that declares itself a
  GitHub-comment/PR template, assert the self-ID line is present;
- positive control: a fixture template WITHOUT the line must be caught.
If no such templates exist, the test asserts that fact and guards future ones (fails the
moment a template is added without the byline).

## Acceptance

- New test collected by `uv run pytest tests/` (CI already runs it).
- Positive-control test proves the scanner fires.
