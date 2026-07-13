---
trdd-id: K3N7QW82
title: Add the MEMBER governance graph to the webdesign main-agent persona
column: todo
created: 2026-07-13T09:39:20+0200
updated: 2026-07-13T09:39:20+0200
current-owner: webdesign-claude
assignee: webdesign-claude
priority: 2
severity: MEDIUM
effort: S
task-type: infra
parent-trdd: MHJL3HY2
npt: []
eht: []
blocked-by: []
relevant-rules: []
release-via: publish
delivery: direct-push
target-branch: main
test-requirements: [lint]
audit-requirements: []
review-requirements: []
impacts: [agent-persona]
implementation-commits: []
external-refs: ["github.com/Emasoft/ai-maestro/issues/41"]
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-13

- **Current state:** NOT STARTED. Awaiting USER go-ahead (this edits the
  main-agent persona, which governs how the whole plugin behaves inside AI
  Maestro — not a drive-by change).
- **The gap (from the ai-maestro#41 ruling's independent review @ 9afc116):**
  `agents/ai-maestro-webdesign-main-agent.md` **FAILS condition (b)** of the
  role-plugin definition — a main-agent whose persona *carries the governance
  rules*. It is an excellent design orchestrator and a correct quad-match entry
  point, but a case-insensitive search for
  `governance|communication graph|chief-of-staff|amp-send|team-governance|MEMBER`
  returns **ZERO matches in its body**. Frontmatter carries no `skills:`
  reference; `rules/` holds only `memory-protocol.md` — no governance rule-file
  link. (Comparison on the same search: `ai-maestro-autonomous-agent` main-agent
  → **44** hits.)
- **Why it matters:** an agent running this persona does not know it holds
  MEMBER, does not know CHIEF-OF-STAFF is its sole inbound/outbound gateway
  (R6 v3), and does not know it may not message MANAGER, peers, or the user
  directly. At runtime the seeded DEP rules (`.claude/rules/aimaestro-*.md`) and
  the core's `team-governance` skill land in the agent's workdir, so it is **not
  inoperable** — but the plugin is leaning on the environment for something the
  spec puts on the persona.
- **NEXT ACTION (one concrete step, runnable as written):**
  Add a `## Communication (MEMBER governance graph)` section to
  `agents/ai-maestro-webdesign-main-agent.md`, modeled on the peer MEMBER
  plugin's section at
  `~/Code/ai-maestro-web-scenario-tester/agents/web-scenario-tester-main-agent.md:181-191`
  (READ-ONLY reference — never edit that repo). It must state: webdesign holds
  **MEMBER**; its only outbound governance edge is its team's **CHIEF-OF-STAFF**;
  it does **not** directly message MANAGER / ARCHITECT / ORCHESTRATOR /
  INTEGRATOR / MAINTAINER / other teams; the human user drives it directly via
  chat (respond when contacted, never initiate); and the `amw-*` sub-agents it
  spawns have **no messaging identity** and must never send inter-agent messages.
  Optionally ALSO add `skills:` frontmatter pointing at the core's
  `team-governance`. Then: CPV `--strict` → `publish.py --patch`.
- **Load-bearing facts / do NOT "fix" these:**
  - `model: opus` in the main-agent frontmatter is **CORRECT** (ecosystem norm:
    autonomous pins sonnet, web-scenario-tester pins opus). Leave it.
  - The delegation topology is **intentionally one-way** (main-agent →
    sub-agent → main-agent). The new section must not imply sub-agents may
    message anyone — it must say the opposite.
  - This is the **last** real role-plugin conformance gap. The manifest half
    already PASSES (see [[TRDD-MHJL3HY2]]): `.agent.toml` valid, Fourfold
    Identity matches, bundled-skills list exactly matches the 68 dirs on disk.
- **SUPERSEDED — do NOT carry forward:** nothing yet (new TRDD).
- **Durable artifacts:** the ai-maestro#41 ruling comment; the WST reference
  section cited above.

## Context

ai-maestro#41 asked four governance questions about webdesign's role-plugin
conformance. The ruling answered all four (see the parent TRDD-MHJL3HY2, now
`complete`) and then volunteered an **unrequested independent review** of the
repo at `9afc116`. That review PASSED the manifest half outright and found
exactly one genuine failure: the main-agent persona carries no governance
content, which is condition (b) of the two-condition role-plugin definition.

This TRDD is that one slice, kept separate per the ruling's own disposition
("open a new slice for the main-agent governance section, which is the one gap
that actually matters").

## Out of scope

- The `dependencies` manifest field — **resolved by ruling: no edit required**
  (the core is never required in the manifest).
- Keep-vs-deprecate the `amw-memory-*` skills — **KEEP**, pending ratification
  of R24 in ai-maestro#37 (currently an unratified proposal). Do not deprecate.
- The publishing-hygiene meta-files (CHANGELOG / CONTRIBUTING / CODE_OF_CONDUCT
  / SECURITY / ACKNOWLEDGMENTS) — already shipped; they never gated role-plugin
  validity anyway.
