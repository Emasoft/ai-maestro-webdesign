# Iteration budget — hard caps for all agent retry loops

This document is the single source of truth for maximum attempt counts in
every retry, fix, or regenerate loop across all `agents/amw-*.md` files.
When an agent cites "per `iteration-budget.md`", it means the cap it states
is governed by this file.

## Canonical caps by loop type

| Loop type | Canonical name | Hard cap | Applies to |
|-----------|---------------|----------|------------|
| ASCII validator fix loop | `ascii-validator-fix` | **5 attempts** | Any agent that runs `bin/amw-validate-ascii.py` in a render→validate→hint→re-validate cycle |
| LLM-based generator regenerate loop | `llm-generator-regen` | **3 attempts** | Any agent that calls an LLM to generate/revise an artifact, inspects the result, and re-prompts on failure |
| Lint mechanical-fix loop | `lint-mechanical-fix` | **2 attempts** | Any agent that calls `bin/amw-design-md-lint.sh` or equivalent lint gate and then attempts programmatic fixes |
| Browser per-scenario timeout | `browser-scenario-timeout` | **10 s default; 30 s on `retry_with`** | `amw-browser-tester-agent` only; time-based, not attempt-count |

Discovery / research agents (Tier 2 agents that perform one-shot analysis)
have **no retry loop** and are classified as *one-shot* — they are exempt
from this cap table.

## What "attempt" means

One **attempt** is one complete execution of the loop body:
1. Generate or transform the artifact
2. Validate or inspect the result
3. If FAIL: apply fix hints, increment attempt counter, loop to step 1
4. If PASS or cap reached: exit loop

The attempt counter starts at **1** for the first generation. A loop that
exits on the first successful pass records `attempts_count: 1`.

## `attempts_log[]` telemetry contract

Every agent with a retry loop MUST populate `attempts_log[]` in its return
header. The field is an ordered list, one entry per attempt, in execution
order:

```yaml
attempts_log:
  - attempt: 1
    failure_reason: "<one-line description, or null if this attempt succeeded>"
    duration_ms: <int>
  - attempt: 2
    failure_reason: null   # null means this attempt succeeded
    duration_ms: <int>
```

Rules:
- `attempts_log` has exactly `attempts_count` entries.
- The last entry's `failure_reason` is `null` if the loop exited with
  success (`status=ok`), or a non-null string if the loop hit the cap
  (`status=failed`).
- `duration_ms` per attempt is wall-clock time for that attempt only (not
  cumulative).
- One-shot agents (no retry loop) set `attempts_log: []` and
  `attempts_count: 1`.

## What happens when the cap is reached

When `attempts_count` equals `max_iterations` and validation still fails:

1. Set `status: failed` (never `partial` — a capped loop is an outright failure).
2. Set `next_action: escalate_to_user`.
3. Populate `blocking_issues` with a summary of the failure pattern observed
   across all attempts (e.g., "Validator consistently reports column-width
   drift at line 47; may indicate an upstream rendering bug rather than a
   fixable content error").
4. Include the full `attempts_log[]` so main-agent can surface the trace to
   the user without re-reading the body.

The fail-fast principle applies: do not attempt partial recovery, do not
lower the quality bar, do not silently succeed with a broken artifact.

## What this is NOT

- **Not a timeout cap.** Wall-clock time per attempt is not governed here
  (the `browser-scenario-timeout` entry is the one exception and is
  explicitly labelled as time-based).
- **Not a file-size or token-count limit.** Those are per-skill concerns.
- **Not a cap on how many agents main-agent may spawn.** Orchestration
  parallelism is governed by `agent-interaction-patterns.md`.

## How agents apply this

Each agent that has a retry loop MUST:

1. State the loop type and cap in **§8 (Uncertainty and Edge-Case Handling)**
   under a `### Iteration cap` sub-heading.
2. Add `max_iterations`, `attempts_count`, and `attempts_log[]` to its
   **§13 (Return Contract worked example)** YAML header.
3. Cite this file by relative path:
   `../skills/amw-design-principles/references/iteration-budget.md`

One-shot agents MUST acknowledge their one-shot status in §8 under a
`### Iteration cap (one-shot)` sub-heading and set
`max_iterations: 1, attempts_count: 1, attempts_log: []` in §13.

## Cross-references

- `sub-agent-return-contract.md` — canonical YAML schema that includes
  `max_iterations`, `attempts_count`, and `attempts_log[]`
- `agent-authoring-philosophy.md` — §8 and §13 template sections
- `authority-hierarchy.md` — veto logic that can abort a loop before cap
