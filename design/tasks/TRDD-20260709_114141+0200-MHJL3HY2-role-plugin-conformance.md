---
trdd-id: MHJL3HY2
title: Conform ai-maestro-webdesign to the role-plugin spec — dependencies + scaffolding
column: complete
created: 2026-07-09T11:41:41+0200
updated: 2026-07-13T09:39:20+0200
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

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-13

**COMPLETE.** ai-maestro#41 was ANSWERED and CLOSED (2026-07-09). Both slices of
this TRDD are resolved. The ruling ALSO surfaced a separate gap that is NOT in
this TRDD's scope — it is tracked as its own slice (see "Follow-up" below).

- **Q1 / dependencies slice — RESOLVED BY RULING, no manifest edit required.**
  The core plugin is *never* required in the manifest, so there is no
  `dependencies` field to add. `plugin.json` is correct as-is.
- **Q1b / `amw-memory-*` keep-vs-deprecate — KEEP, pending R24.** The governing
  proposal (R24 in ai-maestro#37, "plugins ship no per-plugin memory skills")
  is **UNRATIFIED** — no rule number, no governance-owner decision. The ruling
  explicitly declines to rule as if it were law and says: leave `amw-memory-*`
  in place, marked *pending R24 ratification*. **Do NOT deprecate them.** The
  live argument for KEEP is a non-AI-Maestro user installing webdesign
  standalone without the janitor.
- **Q2 / mandatory artifacts — scaffolding slice DONE.** Only two things make a
  role-plugin valid: (a) `<plugin>.agent.toml` with `compatible-titles` +
  `compatible-clients`, and (b) a main-agent `.md` **whose persona carries the
  governance rules**. `CHANGELOG` / `CONTRIBUTING` / `CODE_OF_CONDUCT` /
  `SECURITY` / `ACKNOWLEDGMENTS` are **publishing hygiene, NOT role-plugin
  validity** — shipping them was harmless and good, but none of them gate it.
- **Q3 / canonical spec** — there is no CPV role-plugin profile. The executable
  spec that actually rejects you is ai-maestro's `services/role-plugin-service.ts`.
- **Independent review @ 9afc116 — PASS on the manifest half:**
  `ai-maestro-webdesign.agent.toml` parses, all required fields present,
  `compatible-titles = ["MEMBER"]`, Fourfold Identity matches on all four points,
  the `[agent.skills].bundled` list is EXACTLY the 68 skill dirs on disk (zero
  drift), all 23 sub-agents carry the `amw-` prefix.

- **Follow-up (NOT this TRDD): main-agent governance gap → TRDD-K3N7QW82.**
  The ruling's unrequested review found `agents/ai-maestro-webdesign-main-agent.md`
  **FAILS condition (b)** — it carries ZERO governance content (no MEMBER role,
  no COS gateway, no R6 v3 communication graph). That is the one real remaining
  conformance gap. Tracked separately; do not reopen this TRDD for it.

- **Load-bearing facts:**
  - `model: opus` in the main-agent frontmatter is **CORRECT** and matches the
    ecosystem norm (autonomous pins sonnet, web-scenario-tester pins opus).
    **Do NOT "fix" it.**
  - `.agent.toml` is named `ai-maestro-webdesign.agent.toml` (the
    `<plugin>.agent.toml` convention), NOT `.agent.toml`.
- **SUPERSEDED — do NOT carry forward:**
  - "Dependencies slice is BLOCKED / `plugin.json` must declare
    `dependencies: [ai-maestro-plugin]`" — **WRONG**. The ruling says the core is
    never required in the manifest; there is nothing to add.
  - "Deprecate `amw-memory-*` if the core becomes a hard requirement" —
    **moot**; R24 is unratified and the ruling says KEEP.
  - Any claim that the scaffolding meta-files or `.agent.toml` are missing.
- **Durable artifacts:** the ai-maestro#41 ruling comment (the authoritative
  Q1/Q1b/Q2/Q3 answers + the independent review).

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
