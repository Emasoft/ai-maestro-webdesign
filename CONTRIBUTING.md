# Contributing to ai-maestro-webdesign

Thank you for your interest in this plugin. `ai-maestro-webdesign` is a
Claude Code plugin that consolidates design judgment (the
`amw-design-principles` orchestrator), ASCII-first sketching, diagram
authoring, DESIGN.md tooling, and wireframe-to-HTML production into one
coherent skill set. Contributing here means working inside that
orchestrator/executor architecture, not adding another standalone tool.

## Two contribution paths

**Bug reports** — welcome from anyone. File an issue describing: which
skill/agent/command was involved, the exact prompt or `/amw-*` command
you ran, the expected vs. observed behaviour, and (if relevant) the
generated artifact (HTML/SVG/ASCII) that shows the problem.

**Feature requests / new skills / new agents** — open a Discussion or
an issue first. Because every skill's `description` trigger is tuned to
avoid colliding with `amw-design-principles`'s broad design vocabulary
(see the "Orchestrator priority" rule below), adding a skill is a
design decision, not just code — it needs review before implementation
starts.

## Read `CLAUDE.md` first

`CLAUDE.md` at the repo root is the canonical map of this plugin: the
`agents/` tier structure (main-agent + 19 `amw-*` sub-agents), the
`skills/` layout, the shared `bin/` scripts, and the runtime-dependency
tiers. Read it before touching `skills/`, `agents/`, `commands/`, or
`bin/` — it documents invariants that are easy to break by accident.

## The orchestrator-priority invariant (hard rule)

`amw-design-principles/SKILL.md` owns the broad design vocabulary
(*design, UI, mockup, landing page, wireframe, prototype, slide, deck,
poster, website*) so it is always the first skill Claude Code activates
on generic design intent. Every other skill's `description` is
deliberately narrowed to specific technical triggers ("extract design
tokens from URL", "render HTML as video", "architecture diagram", …).

**When adding or editing any `SKILL.md`, never widen its `description`
back into the general design vocabulary.** A skill that re-claims
"design" or "UI" as a trigger hijacks orchestration and breaks the
ASCII-first plan phase for every other user request. If you're unsure
whether your new trigger is narrow enough, ask in the issue/PR before
merging.

## Local setup

```bash
# 1. Clone and enter the repo
git clone https://github.com/Emasoft/ai-maestro-webdesign
cd ai-maestro-webdesign

# 2. Create the Python environment (uv is mandatory; the project ships
#    uv.lock for reproducibility)
uv venv --python 3.12
source .venv/bin/activate

# 3. Install dependencies + the dev extra (pytest, ruff, mypy, pyyaml)
uv sync --extra dev

# 4. Run the test suite
uv run pytest tests/ -v

# 5. Run linters before committing
uv run ruff check .
uv run mypy .
```

Node-based tooling (`bun`, `playwright`, `dev-browser`) is only needed
for the runtime-acceptance path described in `CLAUDE.md` — install it
via `/amw-init` inside a Claude Code session, not as a prerequisite for
editing skill/agent markdown.

## Plugin validation (CPV)

Before opening a PR that touches `.claude-plugin/plugin.json`,
`skills/`, `agents/`, `commands/`, or `hooks/`, run the
`claude-plugins-validation` (CPV) plugin's remote validator locally —
the same gate CI runs:

```bash
CLAUDE_PRIVATE_USERNAMES="$(whoami)" uv run --with pyyaml python \
  <path-to-cpv>/scripts/remote_validation.py plugin . --strict
```

Fix every CRITICAL/MAJOR/MINOR finding before requesting review. Common
findings on this plugin: skill `description` too long, YAML frontmatter
values starting with `[` needing quotes, agent `description` exceeding
the token budget.

## Branch convention

| Branch prefix | Meaning |
|---|---|
| `fix/<short-slug>` | Bug fix |
| `feat/<short-slug>` | New skill / agent / command |
| `docs/<slug>` | Documentation-only change |
| `chore/<slug>` | Tooling / CI / hygiene |
| `refactor/<slug>` | Behaviour-preserving restructure |
| `test/<slug>` | New tests / test fixes |

Never push to `main` directly. Open a PR against `main`; CI (`Lint` →
`Commitlint` → `Validate`) must pass before merge.

## Commit discipline — record the WHY, in two places

Every commit must explain **why**, not just what, in **both** the
commit message body and the code comments at the change site — the
commit message is the durable record a future contributor (human or
agent) reads with `git log`/`git blame`; the code comment is what a
reader sees without leaving the file. A subject line alone
(`fix bug`, `update skill`) is not enough.

```
type(scope): subject line (<= 70 chars)

A blank line, then the WHY: what problem this solves, what the
previous behaviour was, why the new shape is correct, and what
alternative was considered and rejected.

Optional: which issue / TRDD this closes.
```

`type` in `{feat, fix, docs, chore, refactor, test, perf, style, ci,
build, revert}`. `scope` is the area touched (e.g. `ascii-sketch`,
`diagram-ir`, `design-md`, `agents`, `bin`).

**Never use `git add -A`, `git add .`, or `git add --all`.** Stage
files by name (`git add path/to/file.md path/to/other.py`). This
plugin's reports live under gitignored `reports/`/`reports_dev/`
directories precisely so a wildcard `git add` cannot leak absolute
paths, local usernames, or agent-generated analysis into a commit —
don't defeat that by staging everything anyway.

## TRDDs for non-trivial design tasks

This repo tracks non-trivial feature specs and deferred design work as
TRDDs (Task Requirement Design Documents) under `design/tasks/`, with
`design/proposals/`, `design/refused/`, and `design/archived/` as the
approval-lifecycle folders, and `design/requirements/PRRD.md` as the
project's rules document. If your PR implements or depends on an
existing TRDD, cite its `TRDD-<id8>` in the PR description and, where
relevant, in the commit subject. If you're proposing new scope beyond
a small bug fix, consider authoring a TRDD first rather than opening a
large unscoped PR.

## Self-identification in GitHub posts

Every AI Maestro plugin shares a single human-owned GitHub identity.
When an AI agent (not a human) posts an issue, issue comment, PR, or PR
review on this repo, the body should begin with a one-line
self-identification, e.g.:

> This is the Claude responsible for the ai-maestro-webdesign project.

This avoids ambiguity about who (or what) authored a given comment when
several AI Maestro agents share the same `gh` authentication.

## Path redaction in PR / commit / issue text

When copying logs or paths into a PR description, issue comment, or
commit message, redact host-specific paths:

```
/Users/<anyone>/<rest>        ->  $HOME/<rest>
/home/<anyone>/<rest>         ->  $HOME/<rest>
<absolute path to this repo>  ->  $PROJECT_DIR/<rest>
```

## What we will and won't accept

We *will* review PRs that:

- Fix bugs documented in an open issue.
- Add a new executor skill whose `description` trigger is narrow and
  demonstrably non-colliding with `amw-design-principles` and every
  existing skill (run the cross-refs / skill-trigger-collision checks
  under `bin/` before opening the PR).
- Extend `bin/` with a shared utility when at least two skills would
  benefit, rather than duplicating a one-off script per skill.
- Improve accessibility, cross-platform compatibility, or test
  coverage for existing skills/agents/bin scripts.
- Improve documentation (`CLAUDE.md`, `README.md`, skill references).

We *will not* merge PRs that:

- Widen a skill's `description` back into the general design
  vocabulary the orchestrator owns (breaks first-activation routing).
- Bypass the ASCII-first plan phase / Phase A -> Phase B approval gate
  documented in `CLAUDE.md` for the main-agent workflow.
- Skip the test suite or the CPV validation gate.
- Add a new runtime dependency without updating the dependency tiers
  table in `CLAUDE.md` (system-required / installed-via-`/amw-init` /
  bundled).

## License

By contributing, you agree your work is licensed under MIT (same as
the rest of the repo — see `LICENSE`).

## Code of Conduct

This project follows the [Contributor Covenant
v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
See `CODE_OF_CONDUCT.md` for the full text.

## Reporting security issues

Do NOT open public issues for security vulnerabilities. See
`SECURITY.md` for the private disclosure channel.

## Questions?

Open a GitHub Discussion or comment on an existing issue.
