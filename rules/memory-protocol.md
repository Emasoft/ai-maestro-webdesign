# Memory protocol — webdesign markdown memory system

The webdesign plugin carries a **markdown memory system** so its agents reuse prior
solutions instead of re-deriving them. Three parts: **authoring** (`amw-memory-write`
skill), **recall** (`amw-memory-recall` skill), and the **search engine** (`memgrep`,
with a plain-`grep` fallback) over a corpus of one-fact-per-file markdown notes. This file
is webdesign's plugin-local mirror of the fleet memory protocol (canonical cross-project
form: `~/.claude/rules/markdown-memory-recall.md`); the JANITOR plugin owns the fleet spec
(coordinated on ai-maestro-janitor#21).

## The one law: index by the QUESTION, not the answer

A memory is found from the SYMPTOM — the user's words, the error text, the thing that went
wrong — NOT the jargon of the fix. A note's `description:` (the recall-ranked surface) MUST
carry the words a future session will have when the problem RECURS. The answer lives in the
body.

## Recall BEFORE acting (the discipline)

Before debugging a recurring problem, making a design/architecture decision, or acting on a
recurring alert, **recall first** — "have we hit this before?". It is cheap and it is the
whole point of having a memory. Use the `amw-memory-recall` skill (it composes the three
scope roots and runs `memgrep recall`, degrading to `grep -rliE` when the binary is absent).

## Memory scopes (LOCAL / PROJECT / USER)

| Scope | Root | Git | Contains |
|---|---|---|---|
| **LOCAL** | `~/.claude/projects/<slug>/memory/` | never pushed | machine-private: local paths, hostnames, credential hints |
| **PROJECT** | `<git-root>/memory/` | tracked + pushed | project knowledge any contributor needs — NO sensitive data |
| **USER** | `~/.claude/memory/` | never in any repo | cross-project, machine-independent |

**Write routing:** local/secret/machine-specific → LOCAL; project knowledge any dev needs →
PROJECT; about the user across projects → USER; **UNSURE → LOCAL** (safe scope). **Recall
precedence:** when scopes conflict, the more specific wins (LOCAL > PROJECT > USER).

## Authoring (see `skills/amw-memory-write/SKILL.md`)

One fact per note; symptom-indexed `description`; flat frontmatter (`name` / `description` /
`metadata.type` ∈ user|feedback|project|reference). Optional wikimem fields
(`ocd`/`lmd`/`tier`/`globs`) are additive — write flat now, adopt opportunistically. Every
note ends with a `## Notes and lessons learned` section (the `[^N]` lesson landing zone).
After writing, add a `- [Title](FILE) — hook` line to the memdir's `MEMORY.md` index.

**Correction protocol:** when a fact is wrong, rewrite the body to the correct fact and
demote the old claim to a dated `[^N]` lesson with its WHY — never a silent deletion.

## memgrep distribution

`memgrep` is a Rust binary. Availability ladder (recall degrades, never breaks):

1. **Prebuilt release binary** — ai-maestro-janitor v0.7.1+ ships macOS arm64/x64 + Linux
   x64/arm64 assets with `SHA256SUMS`; verify the checksum and put it on `PATH`.
2. **Build from source** — `cargo install --path <janitor-checkout>/scripts/memgrep`
   (note: `tools/` → `scripts/` moved in janitor v0.7.0).
3. **Plain-grep fallback** — `grep -rliE` over the note frontmatter + bodies. Keep forever
   (covers CI containers without the binary).

Do NOT declare a hard dependency on ai-maestro-janitor — the grep fallback makes it soft.

## Read the notes whole

When you read a note, also read every `[^N]` lesson under its `## Notes and lessons
learned` — they are *why* the fact is the way it is and *what error not to repeat*.
`memgrep recall` appends them automatically.
