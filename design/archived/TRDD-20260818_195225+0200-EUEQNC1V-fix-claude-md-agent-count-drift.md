---
trdd-id: EUEQNC1V
title: Fix CLAUDE.md agent-count drift (says 20, repo has 24)
column: completed
created: 2026-08-18T19:52:25+0200
updated: 2026-08-18T20:02:00+0200
current-owner: webdesign-session
task-type: docs
approval-tier: 0
created-by: phase2-audit-remediation (hub dispatch, TRDD-BRRJK57P)
---

## Defect (Phase-1 audit, doc drift found outside the four axes)

`CLAUDE.md:346` states "20 agents"; `ls agents/*.md | wc -l` → 24. Four agents are absent
from the Tier tables: `amw-design-contract-validator-agent`, `amw-design-resume-agent`,
`amw-slop-verifier-agent`, `amw-sound-designer-agent`.

## Change

Update the inventory count to 24 and add the four missing agents to the appropriate Tier
table rows (read each agent's frontmatter/role to place it correctly — do not guess tiers).
Also check the sibling counts in the same sentence (skill dirs, bin scripts, commands)
against the tree while there, since the sentence is one inventory claim.

## Acceptance

- Every number in the touched inventory sentence matches a fresh `find`/`ls` count.
- All 24 agents appear in exactly one Tier table.
