---
trdd-id: 8ED76GM5
title: Migrate the two v1 status TRDDs to v2 column frontmatter
column: todo
created: 2026-08-18T19:52:25+0200
updated: 2026-08-18T19:52:25+0200
current-owner: webdesign-session
task-type: docs
approval-tier: 0
created-by: phase2-audit-remediation (hub dispatch, TRDD-BRRJK57P)
---

## Defect (Phase-1 audit, axis 2 / F3)

`design/tasks/TRDD-20260525_184846+0200-6d8ffed6-batch9-integration.md:4` and
`design/tasks/TRDD-20260531_221948+0200-e4d97761-gsap-hyperframes-license-decision.md:4`
carry v1 `status: completed` with ZERO `column:` line — invisible to the kanban board
(`grep '^column:'` misses them).

## Change

In each file: replace `status: completed` with `column: completed`, bump `updated:`.
Both are terminal (`completed`) → per folder lifecycle, `git mv` to `design/archived/`.
Leave the full-UUID `trdd-id:` values as-is (grandfathered ids; rewriting them would break
existing citations — the defect is the missing `column:`, not the id).

## Acceptance

- `grep -L '^column:' design/tasks/*.md design/archived/*.md` → empty for these two files.
- Both files live in `design/archived/`.
