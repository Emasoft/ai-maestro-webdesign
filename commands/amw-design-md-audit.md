---
name: amw-design-md-audit
description: "Run the 5-pass audit on an existing DESIGN.md — structural integrity, codebase drift, WCAG accessibility, section completeness, cross-token consistency. Spawns amw-design-md-auditor-agent. Returns a severity-classified findings list (BLOCKER / MAJOR / MINOR / NIT) without modifying the file."
---

# /amw-design-md-audit

Audit a DESIGN.md across five passes:

1. **Structural** — frontmatter shape, section order, type validity.
2. **Drift** (Mode B only) — DESIGN.md tokens vs codebase usage.
3. **Accessibility** — WCAG 2.1 AA contrast on every color pair.
4. **Completeness** — required sections present, no orphan token categories.
5. **Consistency** — cross-token coherence (e.g., `body-md` line-height makes sense for its font-size).

The auditor diagnoses; it does not fix. To repair, hand the file to `amw-design-md-author-agent` after surfacing the findings.

## Arguments

`$ARGUMENTS` may contain:

- `<path-to-DESIGN.md>` — required (default: `./DESIGN.md`)
- `--codebase <path>` — when present, switches to **Mode B** (file + codebase drift check)
- `--severity <BLOCKER|MAJOR|MINOR|NIT>` — filter findings to >= the given severity (default: report all)

If no path is provided, default to `./DESIGN.md`.

## Action

### 1. Spawn `amw-design-md-auditor-agent`

Pass:

```yaml
design_md_path: "<arg-1 or ./DESIGN.md>"
mode: "A | B"           # A = file-only, B = file + codebase
codebase_path: "<--codebase value or null>"
severity_filter: "<BLOCKER|MAJOR|MINOR|NIT|null>"
```

The agent runs all 5 passes (or skips Pass 2 in Mode A) and writes a `<DESIGN.md>.critique.md` adjacent to the input.

### 2. Surface the findings

After the agent returns:

- Total findings count by severity
- BLOCKER findings inline (these halt Phase B)
- Path to the full critique file
- Recommendations (e.g., "Run /amw-design-md-create with `--input-type brief` to repair the structural failures")

### 3. Hand back to the user

If BLOCKER findings exist, recommend:

- `/amw-design-md-lint` to confirm before re-running the audit after a fix
- `amw-design-md-author-agent` to repair structural failures
- Manual review for prose-section drift (no automated fix)

## Non-negotiables

- **Read-only audit.** The auditor never modifies the file. All repairs are explicit downstream commands.
- **All 5 passes run by default.** A user can filter the output, but the passes themselves are not skipped.
- **No veto power.** The auditor is advisory; only `amw-legal-expert-agent` and `amw-accessibility-auditor-agent` can block Phase B from veto-class concerns.

## Failure modes

- File not found → agent returns `status=failed`; surface and stop.
- Mode B requested but codebase path missing → agent returns `status=failed`; ask for the codebase path.
- File is not parseable (e.g., binary, not a Markdown file) → agent returns `status=failed` with the parse error.

## Cross-references

- [amw-design-md-auditor-agent](../agents/amw-design-md-auditor-agent.md)
- [audit-passes](../skills/amw-design-md-audit/references/audit-passes.md)
> [audit-passes.md] Pass 1 — Structural · Pass 2 — Drift · Pass 3 — Accessibility · Pass 4 — Completeness · Pass 5 — Consistency · Output file format · What the auditor does NOT do · Pre-flight checks · Cross-references
- [review-rubric](../skills/amw-design-md-audit/references/review-rubric.md)
> [review-rubric.md] Output schema · Structural checks (must-pass) · Token-quality checks (must-pass — both variants) · Sync checks (must-pass — when companion files exist) · Content-integrity checks (soft — affects score) · A11y checks (must-pass — both variants) · Scoring · What the rubric does NOT do · How `amw-design-md-author-agent` uses the rubric on its own output · Cross-references
- `bin/amw-design-md-lint.sh` (Pass 1 backbone)
- `bin/amw-design-md-contrast.py` (Pass 3 backbone)
