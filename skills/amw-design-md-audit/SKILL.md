---
name: amw-design-md-audit
description: Lint, validate, and audit a DESIGN.md for quality and consistency. Triggers on "lint/validate my DESIGN.md", "audit/five-pass-audit DESIGN.md", "score DESIGN.md quality", "DESIGN.md anti-patterns". Does NOT trigger on authoring or generic design. Use to gate a DESIGN.md before delivery or diagnose problems.
version: 0.1.0
---

# AMW Design.md — Audit

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Lints, validates, scores, and runs the 5-pass audit on an existing DESIGN.md — the pre-delivery quality gate. For the format itself read [spec](../amw-design-md-spec/SKILL.md); to author from a brief use [author](../amw-design-md-author/SKILL.md). DESIGN.md is one of several optional input/output formats the plugin accepts. Triggers are DESIGN.md-specific only.

## Overview

The quality gate for DESIGN.md. Lints (official `npx @google/design.md lint` + offline pure-Python), diffs revisions, runs the 5-pass audit (structural / drift / a11y / completeness / consistency), scores against a rubric, and enforces the DESIGN.md-specific ai-slop anti-pattern check before delivery. Diagnoses problems and provides validation-failure recovery flows; it does not author or repair the file itself.

## Activation

Callable when the user wants to *lint, validate, audit, or score* a DESIGN.md. Also invoked by the orchestrator in main-agent mode, which may delegate to `amw-design-md-auditor-agent` (it reads this SKILL.md and its references; the auditor runs the 5-pass audit and writes a `<file>.critique.md` adjacent to the input). This skill is **autonomous and self-contained** — any agent can read this SKILL.md and the referenced files and execute the recipes without re-routing.

## Position in flow

GATE / QA. Reads a DESIGN.md and returns pass/fail + findings + a quality score. The pre-delivery mechanical check (ai-slop) and the lint gate are what [author](../amw-design-md-author/SKILL.md) and [extract](../amw-design-md-extract/SKILL.md) call before declaring done. The auditor diagnoses, never repairs — repairs are the author's job.

## What this skill is NOT

- Not the format reference — that is [spec](../amw-design-md-spec/SKILL.md).
- Not an author or repair engine. The auditor surfaces findings; fixing them is [author](../amw-design-md-author/SKILL.md)'s job.
- Not the orchestrator. Generic "design system" requests route to `amw-design-principles`.

## Trigger conditions

Fires on: "lint / validate my DESIGN.md"; "audit / five-pass-audit DESIGN.md"; "score DESIGN.md quality"; "DESIGN.md anti-patterns / ai-slop check"; "diff two DESIGN.md files"; "why did my DESIGN.md fail validation".

Does NOT fire on "create a DESIGN.md" (→ [author](../amw-design-md-author/SKILL.md)), "extract a DESIGN.md" (→ [extract](../amw-design-md-extract/SKILL.md)), or generic "design a page" / "design system" (→ `amw-design-principles`).

## The lint / validate / audit / diff operations

- **Lint / validate:** `bin/amw-design-md-lint.sh <path>` for the official linter; `bin/amw-design-md-validate.py <path>` for offline pure-Python validation (frontmatter + section order + token-reference resolution).
- **Diff two revisions:** `bin/amw-design-md-diff.sh <a.md> <b.md>` — wrapper around `npx @google/design.md diff`.
- **5-pass audit:** spawn `amw-design-md-auditor-agent`; it runs the 5-pass audit per [audit-passes](references/audit-passes.md) and writes a `<file>.critique.md` adjacent to the input.

## The audit passes, scoring, recovery, and anti-patterns

- **5-pass audit** (structural / drift / a11y / completeness / consistency, plus the critique-file format): [audit-passes](references/audit-passes.md).
  > Pass 1 — Structural · Pass 2 — Drift · Pass 3 — Accessibility · Pass 4 — Completeness · Pass 5 — Consistency · Output file format · What the auditor does NOT do · Pre-flight checks · Cross-references
- **Quality-scoring rubric** (must-pass structural / token / sync / a11y checks + soft content-integrity checks + scoring): [review-rubric](references/review-rubric.md).
  > Output schema · Structural checks (must-pass) · Token-quality checks (must-pass — both variants) · Sync checks (must-pass — when companion files exist) · Content-integrity checks (soft — affects score) · A11y checks (must-pass — both variants) · Scoring · What the rubric does NOT do · How `amw-design-md-author-agent` uses the rubric on its own output · Cross-references
- **Validation-failure recovery** (recovery flowchart + failure categories + iteration cap + manual recovery for users): [TECH-14-validation-failure-recovery](references/TECH-14-validation-failure-recovery.md).
  > What it does · Recovery flowchart · Failure categories · Iteration cap · What recovery does NOT do · Manual recovery flow for users · Cross-references
- **DESIGN.md-specific ai-slop anti-patterns** — the mechanical pre-delivery check (token authoring / structural / prose / Variant 2 / conversion / companion-file slop): [ai-slop-avoid](references/ai-slop-avoid.md).
  > Token authoring slop · Structural slop · Prose slop · Variant 2 — community 9-section specific · Conversion slop · Companion-file slop · Final delivery gate

## Instructions

1. For a quick gate, run `bin/amw-design-md-lint.sh <path>` (official) then `bin/amw-design-md-validate.py <path>` (offline). Fail fast if either reports errors.
2. For a full audit, spawn `amw-design-md-auditor-agent`; it runs the 5-pass audit per [audit-passes](references/audit-passes.md) and writes `<file>.critique.md`.
3. Score against [review-rubric](references/review-rubric.md); must-pass checks gate delivery, soft checks affect the score.
4. Run the [ai-slop-avoid](references/ai-slop-avoid.md) check as the final pre-delivery gate.
5. On validation failure, follow the recovery flow in [TECH-14-validation-failure-recovery](references/TECH-14-validation-failure-recovery.md); hand repairs to [author](../amw-design-md-author/SKILL.md).

## Hard rules

1. Every DESIGN.md MUST pass `bin/amw-design-md-lint.sh` before being delivered. Lint failure halts delivery.
2. WCAG-AA contrast checks (via `bin/amw-design-md-contrast.py`, run by [author](../amw-design-md-author/SKILL.md)) surface failures to `warnings`, not silent omission; the audit verifies they were not silently dropped.
3. The auditor diagnoses, never repairs. Repairs route back to [author](../amw-design-md-author/SKILL.md).
4. The skill never re-emits broad design vocabulary in tool-call text — that would re-trigger the orchestrator. See [skill-invocation-protocol](../amw-design-principles/references/skill-invocation-protocol.md).

## Resources

- [audit-passes](references/audit-passes.md) — 5-pass audit (structural / drift / a11y / completeness / consistency)
- [review-rubric](references/review-rubric.md) — quality-scoring rubric
- [TECH-14-validation-failure-recovery](references/TECH-14-validation-failure-recovery.md) — validation-failure recovery flows
- [ai-slop-avoid](references/ai-slop-avoid.md) — DESIGN.md-specific anti-patterns (the pre-delivery mechanical check)
- [spec](../amw-design-md-spec/SKILL.md) · [author](../amw-design-md-author/SKILL.md) · [extract](../amw-design-md-extract/SKILL.md) · [convert](../amw-design-md-convert/SKILL.md) — sibling DESIGN.md skills
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (this skill is downstream)
- `<plugin-root>/bin/amw-design-md-lint.sh` · `amw-design-md-validate.py` · `amw-design-md-diff.sh` — the lint / validate / diff scripts
