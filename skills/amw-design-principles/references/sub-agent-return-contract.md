## Table of Contents

- [Schema](#schema)
- [Field semantics](#field-semantics)
  - [`agent` — required, string](#agent-required-string)
  - [`phase` — required, enum `A | B`](#phase-required-enum-a-b)
  - [`status` — required, enum `ok | partial | failed`](#status-required-enum-ok-partial-failed)
  - [`confidence` — required, enum `high | medium | low`](#confidence-required-enum-high-medium-low)
  - [`execution_time_ms` — optional, int](#execution_time_ms-optional-int)
  - [`max_iterations` — required, int](#max_iterations-required-int)
  - [`attempts_count` — required, int](#attempts_count-required-int)
  - [`attempts_log` — required, list of objects](#attempts_log-required-list-of-objects)
  - [`blocking_issues` — required (empty list ok), list of strings](#blocking_issues-required-empty-list-ok-list-of-strings)
  - [`warnings` — required (empty list ok), list of strings](#warnings-required-empty-list-ok-list-of-strings)
  - [`artifact_paths` — required (empty list ok), list of objects](#artifact_paths-required-empty-list-ok-list-of-objects)
  - [`recommendations` — required (empty list ok), list of strings](#recommendations-required-empty-list-ok-list-of-strings)
  - [`next_action` — required, string (free-form but see conventions)](#next_action-required-string-free-form-but-see-conventions)
  - [`report_path` — required, string](#report_path-required-string)
- [Markdown body structure](#markdown-body-structure)
- [How main-agent consumes the contract](#how-main-agent-consumes-the-contract)
- [Contract invariants (enforced by smoke tests)](#contract-invariants-enforced-by-smoke-tests)


# Sub-agent return contract — canonical YAML schema

Every sub-agent under `agents/amw-*.md` returns a report to main-agent in the shape below. The first block is a YAML frontmatter header the main-agent parses mechanically. The rest is free-form markdown for human readers and for main-agent's prose synthesis.

This schema is mandatory. Without it, main-agent has no way to decide mechanically whether to proceed, retry, escalate to user, or stop. Free-form markdown alone forces main-agent to re-read every report in full, which destroys its context and makes orchestration unreliable.

## Schema

```yaml
---
agent: amw-<name>-agent
phase: A | B
status: ok | partial | failed
confidence: high | medium | low
execution_time_ms: <int>
max_iterations: <int>        # hard cap for this agent's retry loop; 1 for one-shot agents
attempts_count: <int>        # number of attempts actually made (1…max_iterations)
attempts_log:                # one entry per attempt in execution order
  - attempt: 1
    failure_reason: "<one-line description, or null if this attempt succeeded>"
    duration_ms: <int>
blocking_issues:
  - "<single-line description of an issue that prevents main-agent from proceeding>"
warnings:
  - "<non-blocking concern main-agent should be aware of>"
artifact_paths:
  - path: "<absolute path>"
    type: html | svg | png | mp4 | ascii | mermaid | json | report
    purpose: "<one-line description>"
recommendations:
  - "<actionable suggestion for main-agent>"
next_action: proceed | retry_with:<param> | escalate_to_user | stop
report_path: "<absolute path to full markdown report under reports/webdesigner/>"
---

# <Agent name> — <phase> summary

<2–3 sentence plain-language summary that main-agent can paraphrase to the user without having to read the full report>

<then the full structured report — sections vary by agent>
```

## Field semantics

### `agent` — required, string
The agent name as declared in the agent file's frontmatter. Used by main-agent to route the output to the correct downstream consumer (e.g., brand-researcher output flows to wireframe-builder's input).

### `phase` — required, enum `A | B`
Which phase of the workflow produced this output. Many agents (accessibility-auditor, SEO-strategist) run in both phases with different input contracts and different output emphasis; the phase field disambiguates.

### `status` — required, enum `ok | partial | failed`
Binary intent, but with a partial state for the common case where some parts of the job succeeded and others did not.
- `ok` — every operation completed as expected; all declared artifacts are on disk; no blocking issues.
- `partial` — some operations completed, others did not. The report must explain which. Main-agent uses `recommendations` and `next_action` to decide what to do.
- `failed` — the agent could not complete its core job. `blocking_issues` must be populated. `artifact_paths` may still contain partial outputs (e.g., a draft report) if they are useful for retry.

### `confidence` — required, enum `high | medium | low`
Self-assessed confidence in the agent's output. An agent with high expertise in its domain and complete input returns `high`. An agent working from thin input, guessing at locale nuance, or operating outside its trained domain returns `low`. Main-agent uses this to decide whether to cross-check with another agent or escalate to the user.

### `execution_time_ms` — optional, int
Wall-clock time the agent spent on the job. Useful for main-agent to detect runaway sub-agents and for post-hoc performance tuning.

### `max_iterations` — required, int
The hard cap on retry/fix/regenerate loop attempts for this agent, as declared in
[iteration-budget](iteration-budget.md). One-shot agents that have no internal retry loop set this to `1`.

### `attempts_count` — required, int
The number of attempts actually made during this invocation (`1 … max_iterations`).
An agent that succeeds on the first pass sets `attempts_count: 1`.

### `attempts_log` — required, list of objects
Telemetry for each attempt, in execution order. One entry per attempt:
- `attempt` — 1-indexed attempt number
- `failure_reason` — one-line description of why the attempt failed, or `null` if it succeeded
- `duration_ms` — wall-clock time for that attempt only (not cumulative)

The last entry's `failure_reason` is `null` when `status=ok`, or a non-null string when
`status=failed` (cap was hit). One-shot agents set `attempts_log: []`.

See [iteration-budget](iteration-budget.md) for the full contract, cap table, and fail-fast rules.

### `blocking_issues` — required (empty list ok), list of strings
Issues that prevent main-agent from proceeding without intervention. Examples:
- "Legal expert cannot identify applicable jurisdiction — user must specify operating countries"
- "Brand-researcher dev-browser timeout on all three competitor URLs — network unreachable"
- "Wireframe-builder ASCII input has column-width drift at line 47, validator refuses"

Each entry is a single line. The full detail goes in the report body. Main-agent treats a non-empty `blocking_issues` list as "do not proceed to next step without resolving these".

### `warnings` — required (empty list ok), list of strings
Non-blocking concerns. Main-agent notes them, surfaces them in the final job-completion report, but does not stall on them. Examples:
- "Copywriter's Arabic translation needs native review before shipping to production"
- "SEO-strategist's keyword-volume estimates are projected, not measured"
- "Accessibility audit found 2 AAA issues (non-blocking under AA target)"

### `artifact_paths` — required (empty list ok), list of objects
Every file the agent produced. Each entry has:
- `path` — absolute path on disk. Must exist when `status=ok`. May exist when `status=partial`. Usually absent when `status=failed`.
- `type` — one of `html | svg | png | mp4 | ascii | mermaid | json | report`. `report` means a markdown document (audit reports, analysis writeups).
- `purpose` — one-line description for main-agent's job-completion summary.

Artifacts always land at project-inferred paths per [project-output-routing](project-output-routing.md), or at the path main-agent explicitly requested. Reports always land under `$MAIN_ROOT/reports/webdesigner/`.

### `recommendations` — required (empty list ok), list of strings
Actionable suggestions for main-agent's next step. Differs from `warnings` in that these are forward-looking ("consider invoking X", "pair with Y next") rather than descriptive ("Z was observed").

### `next_action` — required, string (free-form but see conventions)
Main-agent's recommended next step, phrased as one of:
- `proceed` — continue with the planned workflow
- `retry_with:<param>` — retry the same agent with altered parameters (e.g., `retry_with:fallback_locale=en`, `retry_with:reduced_depth`)
- `escalate_to_user` — the agent needs a user decision before anything else can happen
- `stop` — the workflow cannot continue; main-agent should emit a failure summary to the user

The colon-separated form for `retry_with` is the convention; main-agent parses the parameter string and adjusts its next sub-agent invocation accordingly.

### `report_path` — required, string
Absolute path to the full markdown report. Lives under `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>-<agent-name>-<slug>.md` per [agent-reports-location](agent-reports-location.md). Main-agent never inlines the report body in its own reply; it always cites the path.

## Markdown body structure

After the YAML header, the report body has a flexible structure per agent. Minimum content:

1. **Short summary** (2–3 sentences) that main-agent can paraphrase to the user without reading further
2. **Findings / output** — the agent's actual work product
3. **Limitations** — what the agent could not do, what required assumptions, what confidence gaps exist
4. **Next steps** — if not already covered in `recommendations` header field

Per-agent extensions are welcome (legal-expert adds an "applicable frameworks" table; brand-researcher adds an "extracted tokens per site" table; accessibility-auditor adds a per-WCAG-criterion pass/fail table). The schema gives structure; the body provides depth.

## How main-agent consumes the contract

Pseudo-code for main-agent's parsing loop:

```
result = await spawn_sub_agent(agent_name, input)
yaml_header = parse_yaml_frontmatter(result)

if yaml_header.status == "failed":
    if yaml_header.next_action == "escalate_to_user":
        surface_to_user(yaml_header.blocking_issues)
    elif yaml_header.next_action == "retry_with:X":
        retry_sub_agent(agent_name, input + X)
    else:
        abort_workflow(yaml_header.blocking_issues)

if yaml_header.status == "partial":
    log_warnings(yaml_header.warnings)
    decide_retry_or_continue(yaml_header.recommendations, yaml_header.next_action)

if yaml_header.status == "ok":
    record_artifacts(yaml_header.artifact_paths)
    record_warnings(yaml_header.warnings)
    proceed_with_next_step()
```

In practice main-agent is a language model, not a parser — but it treats the YAML header as structured data and the markdown body as supplementary detail. Sub-agents that skip the YAML header force main-agent to read the entire body, which is what the contract is designed to prevent.

## Contract invariants (enforced by smoke tests)

- Every sub-agent's spec contains a `## Return Contract` section that cites this document
- Every example output in a sub-agent's spec contains a valid YAML header with all required fields
- A report with `status=ok` must list at least one entry in `artifact_paths` (even if it's the report itself)
- A report with `status=failed` must list at least one entry in `blocking_issues`
- `report_path` is always populated and always under `$MAIN_ROOT/reports/webdesigner/`
