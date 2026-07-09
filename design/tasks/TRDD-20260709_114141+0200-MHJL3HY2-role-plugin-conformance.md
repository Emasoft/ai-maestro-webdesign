---
trdd-id: MHJL3HY2
title: Conform ai-maestro-webdesign to the role-plugin spec — dependencies + scaffolding
column: blocked
created: 2026-07-09T11:41:41+0200
updated: 2026-07-09T11:41:41+0200
current-owner: webdesign-claude
assignee: webdesign-claude
priority: 3
severity: MEDIUM
effort: S
task-type: infra
parent-trdd: null
npt: []
eht: []
blocked-by: []
pre-block-column: dev
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
test-requirements: [lint]
audit-requirements: []
review-requirements: []
impacts: [config-schema]
implementation-commits: [51ab529, fb6d408, 2c96a18]
external-refs: ["github.com/Emasoft/ai-maestro/issues/41"]
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-09

- **Current state:**
  - Scaffolding slice — **DONE + verified**. Present at repo root:
    `ai-maestro-webdesign.agent.toml` (51ab529, MEMBER role profile),
    `CHANGELOG.md` (pre-existing), and `CODE_OF_CONDUCT.md` /
    `CONTRIBUTING.md` / `SECURITY.md` / `ACKNOWLEDGMENTS.md`
    (fb6d408 + path-fix 2c96a18). Mirror the `ai-maestro-maintainer-agent`
    v1.7.2 reference shape, adapted to webdesign.
  - Dependencies slice — **BLOCKED on ai-maestro#41** (OPEN, 0 comments as
    of 2026-07-09). `plugin.json` still declares **no `dependencies` field**.
- **NEXT ACTION (when #41 is answered):**
  1. If the ruling says role-plugins MUST declare the core, add
     `"dependencies": [ { "name": "ai-maestro-plugin"[, "version": "<per-ruling>"] } ]`
     to `.claude-plugin/plugin.json` (Q1 decides pinned vs floating).
  2. Resolve **keep-vs-deprecate the `amw-memory-*` skills** per Q1b — current
     lean is **KEEP** (standalone-publish self-containment). Only deprecate if
     the ruling makes `ai-maestro-plugin` a hard runtime requirement that
     supersedes standalone installability.
  3. Re-run CPV validate (`remote_validation.py plugin . --strict`), bump
     version, update CHANGELOG, commit.
- **Load-bearing facts:**
  - `.agent.toml` is named `ai-maestro-webdesign.agent.toml` (the
    `<plugin>.agent.toml` convention), NOT `.agent.toml`.
  - webdesign is intentionally **self-contained for standalone marketplace
    publish** — this is the crux of Q1b.
- **SUPERSEDED — do NOT carry forward:** any earlier claim that scaffolding
  meta-files were missing (they now exist) or that `.agent.toml` was absent.
- **Durable artifacts:** ai-maestro#41 body (the 4 questions Q1/Q1b/Q2/Q3);
  reference plugin at
  `~/.claude/plugins/cache/ai-maestro-plugins/ai-maestro-maintainer-agent/1.7.2/`.

## Context

`ai-maestro-webdesign` is being prepped for publication to
`Emasoft/ai-maestro-plugins`. A pre-publish audit of its manifest + tree
against the official Claude Code plugins-reference and two shipped reference
role-plugins (`ai-maestro-maintainer-agent` v1.7.0, `ai-maestro-autonomous-agent`
v1.5.1) surfaced two conformance gaps. Both were escalated to a governance
ruling in **ai-maestro#41** rather than fixed by guesswork.

## Gap 1 — `dependencies` not declared (BLOCKED)

Reference role-plugins declare the core plugin
(`"dependencies": [ { "name": "ai-maestro-plugin", ... } ]`); webdesign's
`plugin.json` declares none. The version policy is unsettled (the two
references disagree — pinned `^2.6.0` vs unconstrained). **Q1b** couples this
to a real product decision: does requiring the core conflict with webdesign's
standalone-publish design, and therefore should the `amw-memory-*` skills be
kept (self-containment) or deprecated (defer to the janitor-hosted memory
system)? Awaiting the #41 ruling.

## Gap 2 — role-plugin structural artifacts (DONE)

The missing meta-files identified in #41 Q2 have been authored to match the
maintainer reference shape:

| Artifact | Status | Commit |
|---|---|---|
| `ai-maestro-webdesign.agent.toml` | present | 51ab529 |
| `CHANGELOG.md` | present (pre-existing) | — |
| `CODE_OF_CONDUCT.md` | added | fb6d408 |
| `CONTRIBUTING.md` | added | fb6d408 |
| `SECURITY.md` | added | fb6d408 |
| `ACKNOWLEDGMENTS.md` | added + path-fix | fb6d408, 2c96a18 |

Whether every one of these is strictly *mandatory* vs nice-to-have is #41 Q2;
authoring the full set conforms to the observed reference shape regardless of
the ruling, so this slice is safe to land ahead of the answer.

## Verification

- Commit `fb6d408` touched exactly the 4 new files (no `git add -A` leakage);
  `2c96a18` corrected one wrong path in ACKNOWLEDGMENTS caught by a
  repo-fact verification pass (the Tailwind docs-sync script lives at
  `skills/amw-tailwind-4/scripts/sync_tailwind_docs.py`, not repo-root
  `scripts/`). Every other ACKNOWLEDGMENTS claim (dev-browser, Hyperframes,
  beautiful-mermaid/lukilabs, shadcn, brand-`*`.md library, Refactoring-UI
  section, MIT react libs) was checked against the actual repo and confirmed.
- CONTRIBUTING commands (`uv run pytest tests/ -v`, `ruff`, `mypy`,
  CPV `remote_validation.py … --strict`) and SECURITY channel (GitHub
  Security Advisories on the repo) are accurate.

## Out of scope

`.agent.toml` regeneration (already present), the `dependencies` edit, and
the amw-memory keep/deprecate decision — all gated on ai-maestro#41.
