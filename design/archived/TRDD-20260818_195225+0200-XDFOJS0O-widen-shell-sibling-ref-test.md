---
trdd-id: XDFOJS0O
title: Widen test_shell_sibling_refs_resolve to catch fully-missing siblings
column: completed
created: 2026-08-18T19:52:25+0200
updated: 2026-08-18T20:08:00+0200
current-owner: webdesign-session
task-type: bugfix
approval-tier: 0
created-by: phase2-audit-remediation (hub dispatch, TRDD-BRRJK57P)
---

## Defect (Phase-1 audit, axis 4 / CONFIRMED-1)

`tests/test_bin_delegation_paths.py:83` — `if name not in real and f"amw-{name}" in real:`.
The second clause narrows detection to the "forgot the amw- prefix" shape only. A shell ref
to a bin sibling that does not exist under ANY name passes silently. Plant-verified:
appending `$SCRIPT_DIR/amw-totally-fake-nonexistent-script-xyz.py` → 4 passed.

## Change

Flag any `$VAR/.../name` ref whose basename is absent from `real`, WITHOUT re-flagging
vendor/external refs. The vendor exemption is deliberate (docstring lines 72-76): keep it
by exempting refs whose holding variable is not a bin-dir variable, or by scoping the
missing-check to refs that are amw-prefixed or resolve inside `bin/`. Add a positive
control: a plant of a fully-nonexistent amw- sibling must FAIL the test.

## Acceptance

- Plant of a nonexistent `amw-*` sibling in any bin/*.sh → test fails.
- `$VENDOR_DIR/scripts/render.mjs`-style refs still pass.
- Full suite green.
