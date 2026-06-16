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

**Don't panic — webdesign's own code is NOT the problem.** When `cpv ... plugin .` reports **INVALID** with ~20 CRITICAL security findings, **all 20/20 CRITICAL are inside the vendored `external/hyperframes/` git submodule** (gitlink, mode 160000, v0.4.30) — upstream heygen-com code (Dockerfiles, TS source, ffmpeg/browser-manager, package.json) that webdesign neither owns nor may edit (RULE 0 + the cross-project rule). webdesign's OWN code has **0 CRITICAL**; only a few MAJOR/MINOR/NIT. All but one were the skillaudit doc-content false-positive category tracked in cpv#83 (PATH_TRAVERSAL / CRED_ENV_SAFE / REGEX_DOS / CMD_INJECTION matching reference/example prose) — but **one was a REAL command injection** in `bin/amw-sound-analyze.mjs` (execSync interpolating `process.argv[2]` into a shell string), now FIXED (commit a5d3e11, switched to `execFileSync` arg-array).[^1]

**Root cause:** CPV's `skillaudit` SECURITY scanner is NOT gitignore-aware — unlike the "REPO LINT (gitignore-filtered)" pass, it recurses INTO the checked-out submodule working files. The `.gitignore` rule `external/hyperframes/**` (and its comment) only ever scoped the lint scanners (htmlhint/hadolint/ruff/markdownlint/absolute-path) — `skillaudit` was never in that list, so the security gate scans the 244MB submodule and flags its legitimate exec code.

**Do NOT "fix" it by:** editing the submodule (forbidden — not our code), muting a CPV rule, or relaxing `--strict` (forbidden by the no-exempt doctrine). **cpv#123 is CLOSED — CPV will NOT add a security-scan exclude, by policy** (an author-controlled security-skip list is the abusable "exempt-a-list" mechanism they removed; "vendored != trusted", so vendored content is security-scanned by design; `cpv.exclude_paths` exists but skips STYLE/STRUCTURE only, never security).[^2] So the resolution is definitively **my-side — make the submodule source not present as scannable/shippable content.** Three options, all USER/architectural decisions (they change dev/publish behavior — flagged in task #122, not yet made):

1. **`git submodule deinit external/hyperframes`** — removes the checked-out working files (keeps the gitlink); re-init with `git submodule update --init` for local video-render dev. Smallest change.
2. **Configure `cpv.strip.extract[]`** (the strip-dev-parts pattern in `plugin.json` — webdesign only has `cpv.strip.allowed_submodule_urls` today, which just whitelists the URL for the gitmodules validator; it does NOT strip/exclude anything) to extract the submodule from the published artifact.
3. **Drop the vendored submodule entirely** — the bridge runs `npx hyperframes` at RUNTIME (see `skills/amw-hyperframes-bridge/`), so the 244MB gitlink is dev-only reference. Cleanest; loses the local source reference.

Verified 2026-06-16 (CPV 2.126.26): tally CRITICAL=20 MAJOR=24 MINOR=30 NIT=42; in-submodule CRITICAL=20/20, MAJOR=20/24, MINOR=12/30, NIT=12/42. This session's own 3 commits passed `project-scope` validation cleanly (VALID, 0 findings). Governed by [[architecture-hub]].

## Notes and lessons learned

[^2]: [ocd:2026-06-16 lmd:2026-06-16] cpv#123 (requesting a `cpv.scan_exclude` honored by the security scanner) was CLOSED as completed by the CPV maintainer with a firm policy: NO author-controlled security-scan exclude will ever be added — it is precisely the "exempt a list of paths" lever they deliberately removed because a malicious author would just list their payload dir. "Vendored != trusted" → vendored/submodule content is security-scanned by design. The maintainer also announced an upcoming release that makes a tracked+gitignored file a blocking MAJOR (gitignore must imply not-shipped), deprecating webdesign's shadcn-docs gitignore-hack (retired in commit 5a05012). Lesson: do not expect CPV to let you exclude code from the SECURITY scan — the only honest path for un-editable vendored exec code is to make it genuinely absent from the scanned/shipped tree (deinit/strip/remove), not to exclude-list it.

[^1]: [ocd:2026-06-16 lmd:2026-06-16] I initially pattern-matched ALL webdesign-own skillaudit findings as the cpv#83 doc-content FP category (they mostly were — agent/skill prose, reference docs, vendored shadcn MDX). But verifying each by file:line found one genuine command injection in an *executable* `.mjs` (the ffmpeg `execSync` string). Lesson: the submodule/doc FPs are real FPs, but do NOT extend "it's all FPs" to own-code findings that sit in actual executable scripts (`bin/*.mjs|*.py|*.sh`) — read those specific findings and verify FP-vs-real individually. The tell: a finding in *prose/docs* is almost always an FP; a finding in *executable code* with string-interpolated input is almost always real.
