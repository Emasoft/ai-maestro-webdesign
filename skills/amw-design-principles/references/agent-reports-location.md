## Table of Contents

- [Required locations](#required-locations)
- [Why this matters](#why-this-matters)
- [Main-repo root resolution (works from worktrees and main checkout)](#main-repo-root-resolution-works-from-worktrees-and-main-checkout)
- [Timestamp format (mandatory)](#timestamp-format-mandatory)
- [Compliance table (how each surface complies)](#compliance-table-how-each-surface-complies)
- [Template: drop this block into every new agent / skill definition](#template-drop-this-block-into-every-new-agent-skill-definition)
- [Orchestrator override](#orchestrator-override)
- [Gitignore bootstrap](#gitignore-bootstrap)
- [Anti-patterns (DO NOT DO)](#anti-patterns-do-not-do)
- [Verification checklist](#verification-checklist)

# Agent Report Location

**Rule:** Every agent, skill, or tool that writes a report MUST save it under
`<main-repo-root>/reports/<component>/<timestamp>-<name>.md`.

This is a hard invariant. It applies to all agents (built-in, user-defined,
plugin-provided), all skills, all hooks, every slash command, every script,
every LLM Externalizer call, every subagent swarm — everything that emits a
report, audit, scan output, summary, handoff, or analysis file.

## Required locations

| What | Where | Gitignored |
|------|-------|------------|
| User-facing reports from agents / skills / tools | `<main-repo-root>/reports/<component>/` | Yes |
| Dev-only scratch, drafts, iteration artifacts | `<main-repo-root>/reports_dev/<component>/` | Yes |
| Final output of pipelines with internal state | `<main-repo-root>/reports/<component>/` | Yes |
| Internal operational state of a pipeline (e.g. step-to-step exchange) | Declared in the pipeline's own spec | Yes (must be) |

**Both `./reports/` AND `./reports_dev/` MUST be present in the project
`.gitignore`.** Before spawning any agent, verify both entries exist and add
them if missing.

## Why this matters

- Reports routinely contain private data: absolute paths, usernames,
  internal hostnames, excerpts of proprietary source, auth tokens that
  happened to be in logs, PII embedded in test fixtures.
- Committing a report to the repo is a data leak. Gitignoring them both is
  the seat-belt.
- Centralising them under one path (`./reports/`) makes them searchable,
  cleanable, and backup-able from a single command — instead of scattered
  across every agent's whim.
- Worktrees inherit the same `.gitignore` from the main repo, but writing
  to the worktree's own `./reports/` would split the archive across N
  branches. The main-repo root is the single source of truth.

## Main-repo root resolution (works from worktrees and main checkout)

Shell helper every agent can paste at the top of its Bash prologue:

```bash
# Resolve the main repo root — same answer whether we run in the main
# checkout or a linked worktree.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  MAIN_ROOT="$(git worktree list | head -n1 | awk '{print $1}')"
else
  MAIN_ROOT="$CLAUDE_PROJECT_DIR"   # fallback when not a git repo
fi
REPORT_DIR="$MAIN_ROOT/reports/<component>"
mkdir -p "$REPORT_DIR"
# Timestamp MUST be local time + GMT offset — see "Timestamp format" below.
REPORT_FILE="$REPORT_DIR/$(date +%Y%m%d_%H%M%S%z)-<name>.md"
```

`git worktree list` always lists the main checkout first, even when called
from a linked worktree. That is the canonical way to find the primary
working tree without parsing `.git` files by hand.

## Timestamp format (mandatory)

Every report filename MUST embed a timestamp in **local time** with the
**delta from GMT** appended in the compact `±HHMM` form.

Canonical shell:

```bash
TIMESTAMP="$(date +%Y%m%d_%H%M%S%z)"
# Examples of output:
#   20260421_183012+0200   (Rome, CEST)
#   20260421_123012-0500   (New York, EST)
#   20260421_163012+0000   (UTC)
```

- `%Y%m%d_%H%M%S` — local date and time, underscore-separated
- `%z` — GMT offset in `±HHMM` (no colon; filesystem-safe on every OS)

**Rules:**
- Never use UTC (`date -u`) — local time is required so humans can tie a
  report back to their own workday without timezone arithmetic.
- Never omit the `%z` offset — a bare `YYYYMMDD_HHMMSS` is ambiguous across
  machines, worktrees, and shared filesystems.
- Never use `:` in the offset (`+02:00`) — Windows filesystems reject it.
- Never reformat the timestamp after `date` has produced it; the compact
  form is the canonical spelling everywhere the rule is mentioned.

The same format is the default for TRDD filenames, handoff docs, and any
other dated artefact an agent emits — consistency lets `ls -t` and glob
sorting do the right thing without extra metadata.

## Compliance table (how each surface complies)

**Same rule, same folder, for everything.** No carve-outs, no per-tool
overrides — every surface below writes to
`$MAIN_ROOT/reports/<component>/<ts±tz>-<slug>.<ext>`:

| Surface | `<component>` |
|---------|---------------|
| User-defined agents in `~/.claude/agents/` | agent name |
| Plugin-shipped agents | agent name |
| Skills | skill name |
| Hooks | hook name |
| Slash commands | command name |
| MCP tools (including LLM Externalizer) | tool/server name — pass `output_dir: "$MAIN_ROOT/reports/<tool>/"` on every call; never accept a server default that points anywhere else |
| Scripts invoked from CLAUDE.md workflows | script name (e.g. `generate-reasoning`) |

If a tool's server default points somewhere else (e.g. `reports_dev/<tool>/`),
override it on every call. There are no exceptions.

## Template: drop this block into every new agent / skill definition

```markdown
## Output location

Write your final report to:
`$MAIN_ROOT/reports/<component>/{YYYYMMDD_HHMMSS±HHMM}-<summary-slug>.md`

Resolve the path with:

\`\`\`bash
MAIN_ROOT="$(git worktree list | head -n1 | awk '{print $1}')"
REPORT_DIR="$MAIN_ROOT/reports/<component>"
mkdir -p "$REPORT_DIR"
TIMESTAMP="$(date +%Y%m%d_%H%M%S%z)"   # local time + GMT offset
REPORT_FILE="$REPORT_DIR/$TIMESTAMP-<summary-slug>.md"
\`\`\`

The timestamp MUST be local time with the GMT offset appended (`%z`,
compact `±HHMM` form — never UTC, never `±HH:MM`).

Do NOT write to `reports_dev/`, `.claude/`, or any per-worktree subtree —
those are for internal scratch, not for the final artefact.
```

## Orchestrator override

If the orchestrator hands the agent an explicit `output_path` via the
prompt, honor that path verbatim. Otherwise fall back to the rule above.

## Gitignore bootstrap

If `.gitignore` is missing either entry, add both atomically:

```bash
grep -qxF '/reports/'      .gitignore 2>/dev/null || echo '/reports/'      >> .gitignore
grep -qxF '/reports_dev/'  .gitignore 2>/dev/null || echo '/reports_dev/'  >> .gitignore
```

Do this lazily (just-in-time, the first time an agent is about to write a
report), not eagerly at session start — most projects already have both
entries, and an extra `.gitignore` churn commit is noise.

## Anti-patterns (DO NOT DO)

- Writing a report to the worktree's local `./reports/` when running inside
  a linked worktree — it will live on a branch that gets deleted.
- Writing to `~/.claude/` or `~/` — those are outside the project scope and
  cannot be cleaned up per-project.
- Writing to `.claude/` inside the project — that directory is reserved for
  Claude Code spec artefacts (hooks, settings, commands), not reports.
- Letting a plugin or script default to `reports_dev/` for a final,
  user-facing report — `reports_dev/` is for drafts and iteration, the
  canonical output is `reports/`.
- Subsystem-private report directories (e.g. `.rechecker/reports/`,
  `.audit/reports/`, `.ci/artifacts/`, `llm_externalizer_output/`). These
  look "operational" but they hold the same findings/audit content as
  top-level reports — they MUST live under `$MAIN_ROOT/reports/<component>/`.
  Only pure runtime state that is not a report (progress trackers, index
  files, batch lists) may remain in a subsystem-private directory.
- Emitting the raw report content back to the orchestrator as a tool
  result: always write to disk, return only the filepath.

## Verification checklist

Before reporting a task complete, if any report was written:
- [ ] File lives under `$MAIN_ROOT/reports/<component>/`
- [ ] Filename timestamp is local time **and** includes the GMT offset
      (`%Y%m%d_%H%M%S%z` → e.g. `20260421_183012+0200`)
- [ ] `.gitignore` contains both `/reports/` and `/reports_dev/`
- [ ] The path was resolved via `git worktree list` (worktree-safe)
- [ ] The orchestrator received only the filepath, not the report body
