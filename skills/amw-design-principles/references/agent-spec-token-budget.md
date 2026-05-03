# Agent spec token budget — known future optimization

## Table of Contents

- [What was identified](#what-was-identified)
- [Why this is deferred (not applied in 2026-04-27 fix pass)](#why-this-is-deferred-not-applied-in-2026-04-27-fix-pass)
- [Conditions to apply this optimization later](#conditions-to-apply-this-optimization-later)
- [What was applied in the 2026-04-27 fix pass](#what-was-applied-in-the-2026-04-27-fix-pass)
- [See also](#see-also)


**Status:** Deferred (verified-safe trim deferred to a separate, focused pass)
**Identified:** 2026-04-27 capability audit
**Affected:** All 17 agents under `agents/`

## What was identified

The capability audit (Lens 5 — token efficiency) found that §13 worked-example YAML blocks across 16 of 17 agents range ~80 LOC each. The auditor estimated ~10K tokens of total savings if §13 examples were trimmed to ~40 LOC.

Random sample cited: `amw-wireframe-builder-agent` §13 = 87 LOC for status=ok worked example + 25 LOC for status=failed = 112 LOC of example markdown.

## Why this is deferred (not applied in 2026-04-27 fix pass)

1. **The 14-section template ([agent-authoring-philosophy](agent-authoring-philosophy.md)) is canonical** and every agent references the §13 worked-example structure as part of the contract. Trimming worked examples without an updated philosophy doc would produce inconsistency.
  > Skills and agents are not the same kind of thing · What an agent actually needs · Recipe layer (deterministic floor) · Judgment layer (non-deterministic surface) · Why the judgment layer matters in this plugin specifically · The 14-section canonical template · What this document is NOT · Cross-references

2. **The worked examples document the YAML schema** (per [sub-agent-return-contract](sub-agent-return-contract.md)). They're not just illustrations — they are the second-level contract the orchestrator parses when validating sub-agent outputs. Trimming risks losing schema-fidelity examples.
  > Schema · Field semantics · `agent` — required, string · `phase` — required, enum `A | B` · `status` — required, enum `ok | partial | failed` · `confidence` — required, enum `high | medium | low` · `execution_time_ms` — optional, int · `max_iterations` — required, int · `attempts_count` — required, int · `attempts_log` — required, list of objects · `blocking_issues` — required (empty list ok), list of strings · `warnings` — required (empty list ok), list of strings · `artifact_paths` — required (empty list ok), list of objects · `recommendations` — required (empty list ok), list of strings · `next_action` — required, string (free-form but see conventions) · `report_path` — required, string · Markdown body structure · How main-agent consumes the contract · Contract invariants (enforced by smoke tests)

3. **Two-status-branch examples (status=ok with warnings, status=failed)** are pedagogically necessary. Collapsing into a single example loses the distinction between "happy path with deviations" and "blocking failure".

4. **Token estimates are rough.** The auditor flagged confidence as LOW for L5 token-efficiency claims. Empirical token accounting (count tokens before / after on a representative agent) is needed before committing to a 50% trim.

## Conditions to apply this optimization later

A future pass should:
1. Update [agent-authoring-philosophy](agent-authoring-philosophy.md) to define a new "compact §13" pattern explicitly (e.g., one combined example showing both branches in a single YAML block).
  > Skills and agents are not the same kind of thing · What an agent actually needs · Recipe layer (deterministic floor) · Judgment layer (non-deterministic surface) · Why the judgment layer matters in this plugin specifically · The 14-section canonical template · What this document is NOT · Cross-references
2. Update [sub-agent-return-contract](sub-agent-return-contract.md) to host the canonical schema separately from any agent's §13 — so the schema reference becomes cross-cutting, not duplicated.
  > Schema · Field semantics · `agent` — required, string · `phase` — required, enum `A | B` · `status` — required, enum `ok | partial | failed` · `confidence` — required, enum `high | medium | low` · `execution_time_ms` — optional, int · `max_iterations` — required, int · `attempts_count` — required, int · `attempts_log` — required, list of objects · `blocking_issues` — required (empty list ok), list of strings · `warnings` — required (empty list ok), list of strings · `artifact_paths` — required (empty list ok), list of objects · `recommendations` — required (empty list ok), list of strings · `next_action` — required, string (free-form but see conventions) · `report_path` — required, string · Markdown body structure · How main-agent consumes the contract · Contract invariants (enforced by smoke tests)
3. Apply the trim atomically across all 17 agents in one commit (not piecemeal), with the new [agent-authoring-philosophy](agent-authoring-philosophy.md) and [sub-agent-return-contract](sub-agent-return-contract.md) updates.
  > Skills and agents are not the same kind of thing · What an agent actually needs · Recipe layer (deterministic floor) · Judgment layer (non-deterministic surface) · Why the judgment layer matters in this plugin specifically · The 14-section canonical template · What this document is NOT · Cross-references
4. Empirically measure token usage before / after on at least 3 agents to validate the savings claim.

## What was applied in the 2026-04-27 fix pass

Nothing — this optimization is documented here for a future pass that has its own scope and verification budget.

## See also

- [agent-authoring-philosophy](agent-authoring-philosophy.md) — canonical 14-section template
  > Skills and agents are not the same kind of thing · What an agent actually needs · Recipe layer (deterministic floor) · Judgment layer (non-deterministic surface) · Why the judgment layer matters in this plugin specifically · The 14-section canonical template · What this document is NOT · Cross-references
- [sub-agent-return-contract](sub-agent-return-contract.md) — YAML schema definition
  > Schema · Field semantics · `agent` — required, string · `phase` — required, enum `A | B` · `status` — required, enum `ok | partial | failed` · `confidence` — required, enum `high | medium | low` · `execution_time_ms` — optional, int · `max_iterations` — required, int · `attempts_count` — required, int · `attempts_log` — required, list of objects · `blocking_issues` — required (empty list ok), list of strings · `warnings` — required (empty list ok), list of strings · `artifact_paths` — required (empty list ok), list of objects · `recommendations` — required (empty list ok), list of strings · `next_action` — required, string (free-form but see conventions) · `report_path` — required, string · Markdown body structure · How main-agent consumes the contract · Contract invariants (enforced by smoke tests)
- `~/.claude/rules/agent-token-budget.md` — global token-budget rules (different scope: orchestrator → agent prompts, not agent self-spec size)
