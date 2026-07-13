---
trdd-id: K3N7QW82
title: Add the MEMBER governance graph to the webdesign main-agent persona
column: complete
created: 2026-07-13T09:39:20+0200
updated: 2026-07-13T10:02:23+0200
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
implementation-commits: [f904efc7e11a205ba38414e8ce47ff6b4ef5d5c3]
external-refs: ["github.com/Emasoft/ai-maestro/issues/41"]
---

## ⏵ STATE — READ THIS FIRST ON RESUME (authoritative; supersedes the body) — 2026-07-13

- **Current state:** IMPLEMENTED at `f904efc` (2026-07-13 10:02 +0200), under a
  MAESTRO mandate to decide autonomously. `column: complete`; awaiting only the
  `publish` leg (`release-via: publish`).
- **What landed:** an UNNUMBERED `## Communication (MEMBER governance graph)`
  section in `agents/ai-maestro-webdesign-main-agent.md`, between §15 and
  `## Cross-references` (unnumbered on purpose — a numbered §16 would renumber
  nothing today but invites drift against the canonical 1–15 template, and the
  WST reference is itself unnumbered). File 786 → 805 lines.
- **VERIFIED, not assumed:** the gap-defining search
  (`governance|communication graph|chief-of-staff|amp-send|team-governance|MEMBER`,
  case-insensitive) went **0 → 5** hits. §1–15 headings unchanged. Gates:
  CPV `--strict` CRITICAL=0 MAJOR=0 MINOR=0 NIT=0 (67 advisory WARNINGs);
  `ruff check scripts/` clean; `mypy scripts/` clean.
- **DECIDED AGAINST (and why) — do not "finish" this:** the optional
  `skills: [team-governance]` frontmatter proposed in the original NEXT ACTION
  was **rejected on evidence**. webdesign is dual-use (standalone design plugin
  AND AI-Maestro role-plugin), so a hard frontmatter dep on a core skill would
  dangle on standalone installs. Checked the ecosystem norm rather than guessing:
  the WST main-agent's `skills:` field lists `the-skills-menu`, **not**
  `team-governance` — governance is carried in PROSE there too. The new section
  therefore ends with an explicit standalone clause.
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
  `uv run scripts/publish.py --patch` → v0.1.7. That is the ONLY step left. It
  also carries the two docs commits already sitting unpushed on `main`
  (`3269491` wikimem page, `dc59b72` TRDD bookkeeping). On success set
  `column: published`.
- **Load-bearing facts / do NOT "fix" these:**
  - `model: opus` in the main-agent frontmatter is **CORRECT** (ecosystem norm:
    autonomous pins sonnet, web-scenario-tester pins opus). Leave it.
  - The delegation topology is **intentionally one-way** (main-agent →
    sub-agent → main-agent). The new section must not imply sub-agents may
    message anyone — it must say the opposite.
  - This is the **last** real role-plugin conformance gap. The manifest half
    already PASSES (see [[TRDD-MHJL3HY2]]): `.agent.toml` valid, Fourfold
    Identity matches, bundled-skills list exactly matches the 68 dirs on disk.
- **SUPERSEDED — do NOT carry forward:**
  - The `skills: [team-governance]` frontmatter option — REJECTED, see above.
  - "the role profile is at `.agent.toml`" — WRONG FILENAME, and it cost a
    detour. The file is **`ai-maestro-webdesign.agent.toml`** at the repo root
    (the `<plugin-name>.agent.toml` convention, added at `51ab529`). A bare
    `ls .agent.toml` returns "No such file" and looks exactly like the file is
    missing. It is not. Search by `*agent.toml`, never by the bare dotfile name.
  - The MEMORY.md note `webdesign-role-plugin-conformance-gaps` claiming
    "plugin.json missing `dependencies`" and "missing .agent.toml" — BOTH now
    FALSE (`plugin.json` carries
    `dependencies: [{name: dev-browser, marketplace: dev-browser-marketplace}]`;
    the role profile exists under the name above). The note is stale and is
    corrected in the same session as this TRDD.
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
