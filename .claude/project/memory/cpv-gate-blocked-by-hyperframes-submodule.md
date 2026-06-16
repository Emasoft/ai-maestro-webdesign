---
name: cpv-gate-blocked-by-hyperframes-submodule
description: "CPV full plugin validation says INVALID / 20 CRITICAL / security gate fails / plugin won't pass / publishing blocked — is webdesign's own code broken? why so many critical security findings?"
ocd: 2026-06-16
lmd: 2026-06-16
metadata:
  node_type: memory
  type: project
  tier: component
  globs: ["external/hyperframes/**", ".claude-plugin/plugin.json"]
---

**Don't panic — webdesign's own code is NOT the problem.** When `cpv ... plugin .` reports **INVALID** with ~20 CRITICAL security findings, **all 20/20 CRITICAL are inside the vendored `external/hyperframes/` git submodule** (gitlink, mode 160000, v0.4.30) — upstream heygen-com code (Dockerfiles, TS source, ffmpeg/browser-manager, package.json) that webdesign neither owns nor may edit (RULE 0 + the cross-project rule). webdesign's OWN code has **0 CRITICAL**; only a few MAJOR/MINOR/NIT, mostly the skillaudit doc-content false-positive category tracked in cpv#83 (PATH_TRAVERSAL / CRED_ENV_SAFE / REGEX_DOS / CMD_INJECTION matching reference/example prose).

**Root cause:** CPV's `skillaudit` SECURITY scanner is NOT gitignore-aware — unlike the "REPO LINT (gitignore-filtered)" pass, it recurses INTO the checked-out submodule working files. The `.gitignore` rule `external/hyperframes/**` (and its comment) only ever scoped the lint scanners (htmlhint/hadolint/ruff/markdownlint/absolute-path) — `skillaudit` was never in that list, so the security gate scans the 244MB submodule and flags its legitimate exec code.

**Do NOT "fix" it by:** editing the submodule (forbidden — not our code), muting a CPV rule, or relaxing `--strict` (forbidden by the no-exempt doctrine). **Resolution is architectural, two tracks:**
1. **cpv#123** — the requested `plugin.json cpv.scan_exclude` must apply to the SECURITY scanner (not just lint), so `external/**` skips scanning. Awaiting the CPV maintainer.
2. **Publish-exclude the submodule.** The bridge runs `npx hyperframes` at RUNTIME (see `skills/amw-hyperframes-bridge/`), so the 244MB gitlink is dev-only reference and arguably should NOT ship in the published package. Excluding `external/` from the publish artifact makes the gate pass on the shipped plugin. **This is a user/architectural decision — flagged, not yet made.**

Verified 2026-06-16 (CPV 2.126.26): tally CRITICAL=20 MAJOR=24 MINOR=30 NIT=42; in-submodule CRITICAL=20/20, MAJOR=20/24, MINOR=12/30, NIT=12/42. This session's own 3 commits passed `project-scope` validation cleanly (VALID, 0 findings). Governed by [[architecture-hub]].

## Notes and lessons learned
