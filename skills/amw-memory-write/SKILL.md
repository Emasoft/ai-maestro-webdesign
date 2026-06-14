---
name: amw-memory-write
description: Capture a durable lesson into the project's markdown memory AFTER solving a non-obvious problem, receiving a correction, or learning a project gotcha. One fact per note, a SYMPTOM-indexed description, scoped LOCAL / PROJECT / USER. Use when something was learned the hard way and a future session would waste time re-learning it.
---

# amw-memory-write — capture one symptom-indexed lesson

This is the webdesign plugin's WRITE half of the markdown memory system (the RECALL half is
`amw-memory-recall`; the full protocol is `rules/memory-protocol.md`). It records ONE fact
per note so a future session can RECALL it from the symptom.

## The one law: index the DESCRIPTION by the QUESTION, not the answer

The `description:` (plus `title`/tags) is the load-bearing recall surface — `memgrep recall`
ranks on it. It MUST carry the words a future session will have when the problem RECURS: the
user's words, the error text, the symptom — NOT the jargon of the fix. Put the symptom in
`description`; put the answer in the BODY. Two-hop recall: a symptom query lands the note;
the body gives the answer.

- WRONG `description`: "OAuth creds live in the macOS keychain."
- RIGHT `description`: "rotator failed, had to log in manually — where are the creds / why
  did the swap fail" (+ the keychain fact in the body).

## Scope routing (decide BEFORE writing)

| Signal in the fact | Scope | Root |
|---|---|---|
| local path / username / hostname / secret / machine-specific | **LOCAL** | `~/.claude/projects/<slug>/memory/` (never pushed) |
| project knowledge any contributor needs (architecture, gotcha, lesson) | **PROJECT** | `<repo>/.claude/project/memory/` (git-tracked in-repo, namespaced under `.claude/` — NO sensitive data) |
| about the user, machine-independent, cross-project | **USER** | `~/.claude/plugins/data/ai-maestro-janitor-ai-maestro-plugins/memory/` (janitor's FIXED data dir, hard-coded — NOT `${CLAUDE_PLUGIN_DATA}`) |

UNSURE → **LOCAL** (the safe scope; promotion to PROJECT is a deliberate later act).

## Note format

```markdown
---
name: <kebab-slug>                 # == filename stem
description: "<symptom surface — the load-bearing recall field>"
metadata:
  type: user | feedback | project | reference
---

<the one fact. For feedback/project, follow with **Why:** and **How to apply:** lines.
Link related notes with [[their-name]].>

## Notes and lessons learned
```

Optional wikimem fields (`ocd`/`lmd` dates, `tier: hub|aspect|component`, `globs`) are
ADDITIVE — a flat note without them is treated as a component page, so write flat now and
adopt them opportunistically. The `## Notes and lessons learned` section is mandatory (even
empty) — it is the landing zone for `[^N]` correction lessons.

## After writing

Add a one-line pointer to `MEMORY.md` in the same memdir — a bullet of the form
`- [Title]` linking the note filename `— hook` — the index loaded each session. Before
saving, recall first (`amw-memory-recall`) to UPDATE an existing note rather than
duplicate it.

## Correction protocol (don't delete — demote)

When a fact turns out wrong: rewrite the body to the CORRECT current fact, and move the old
(wrong) claim into a dated `[^N]` lesson under `## Notes and lessons learned` with its WHY.
Superseded facts become lessons, never silent deletions.

## When to use

- Just solved a non-obvious problem that cost real time → capture the symptom + fix.
- Got a correction from the user on how to work → capture it (type: feedback, with Why).
- Learned a project constraint not derivable from the code → capture it (type: project).
- NOT for what the repo already records (code structure, git history, CLAUDE.md).
