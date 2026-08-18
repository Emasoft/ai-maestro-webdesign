---
trdd-id: 676DDBYL
title: Document the baseline-tag-protect ruleset and record its approval
column: completed
created: 2026-08-18T19:52:25+0200
updated: 2026-08-18T20:24:00+0200
current-owner: webdesign-session
task-type: docs
approval-tier: 2
created-by: phase2-audit-remediation (hub dispatch, TRDD-BRRJK57P)
---

## Defect (Phase-1 audit, axis 2 / F9)

GitHub ruleset id 18894433 `baseline-tag-protect` (target: tag, rules: `deletion` +
`update` on `refs/tags/v*.*.*`, enforcement: active) exists beyond the ratified 2-ruleset
baseline with no TRDD/PRRD approval record. Additive (tightens tag safety) — low risk,
but per manager-approval-defaults §F an undocumented baseline deviation.

## Change

Document, do not remove (it protects release tags — removal would loosen). Add to
CLAUDE.md's conventions a one-paragraph record of the third ruleset, and record the hub's
Phase-2 dispatch as the MANAGER approval in this TRDD's Approval log.

## Approval log

- 2026-08-18T19:52:25+0200 — Tier-2 authority: hub session ai-maestro-fd, Phase-2 dispatch
  under the USER's verbatim delegation ("you are in charge. decide yourself in base of
  verified facts and tests"). This TRDD documents an EXISTING additive ruleset; it does
  not create or loosen one.
