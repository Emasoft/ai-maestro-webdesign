---
name: amw-skill-drift-audit
description: Plugin-maintenance audit — pins every skill to a source commit via `source` / `source_version` frontmatter, detects DRIFT when the upstream source has moved since the pin, and emits a re-distill PLAN classifying each skill as CLEAN / PIN-ONLY / STALE. Read-only — never rewrites skills or bumps pins. Triggers on "audit skill drift", "check skill pins against upstream", "re-distill plan", "skill source-version drift", "is my plugin in sync with the source skills". Does NOT trigger on generic "audit my plugin" — those go to plugin-validation; this is specifically for distilled-from-upstream skill content.
version: 0.1.0
---

# Skill Drift Audit

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is an executor. Triggers are skill-distillation-drift-specific only.

## Overview

A plugin like `ai-maestro-webdesign` is built by **distilling** content from upstream sources (read-only `SKILLS-TO-INTEGRATE/` repos, scaffold projects, official documentation). The distilled skill in `skills/<name>/SKILL.md` carries `source:` and `source_version:` frontmatter identifying *what* it was distilled from and *which commit*. This skill audits those pins against the current state of the upstream sources and emits a per-skill drift verdict.

**Three verdicts** per skill:

- **CLEAN** — upstream `HEAD == source_version`. No drift, nothing to do.
- **PIN-ONLY** — upstream `HEAD != source_version` but no `source:` file changed in the diff. Mechanical `source_version` bump suffices; content stays correct.
- **STALE** — upstream `source:` file(s) actually changed between pin and HEAD. Content may now be wrong; needs human re-distillation (judgment call about which idiom changed and how the skill should read).

**Read-only.** This skill diagnoses; it never rewrites skill content or bumps version pins. The output is a markdown PLAN a human (or follow-up workflow) acts on.

## Activation

Callable directly via the `/amw-audit-skill-drift` command (when added), or invoked as a maintenance pass before a plugin release / version bump. Pairs naturally with `cpv-batch-validate` (structural validation) and `amw-design-drift-audit` (token-level drift) for a full plugin-health sweep.

This skill is **autonomous and self-contained** — any agent (main-agent, sub-agent, external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

GOVERNANCE / META. Sits outside the design workflow proper — it audits the PLUGIN ITSELF (the skills directory), not the user's design artifacts. Use cases:

- Quarterly plugin-health pass before a release.
- After a major upstream-source update (e.g. shadcn ships v2.x, Tailwind v5 lands, the official `@google/design.md` schema changes).
- During plugin extraction — confirm every newly-distilled skill carries pins and the pins resolve.

For STRUCTURAL plugin validation (manifest correctness, frontmatter validity, file-tree shape), prefer **`cpv-batch-validate`** from claude-plugins-validation. This skill is the orthogonal CONTENT-drift detector — it answers "is the distilled CONTENT still current?", which structural validators cannot answer.

## Trigger conditions

Fires on these specific phrasings:

- "audit skill drift"
- "check skill pins against upstream"
- "re-distill plan for plugin"
- "skill source-version drift"
- "is my plugin in sync with the source skills"
- "which skills need re-distillation"
- "find STALE skills"
- "scan skills for pin drift"

Do NOT fire on: "validate my plugin", "lint my plugin", "is my plugin marketplace-ready". Those route to claude-plugins-validation (structural / marketplace checks). Drift audit is content-level, not structure-level.

## Inputs (required)

- **Plugin root** — directory containing `.claude-plugin/plugin.json` and `skills/<name>/SKILL.md` files. Default: `$PWD`.
- **Source map** (one of):
  - The skill frontmatter itself — `source:` lists paths, `source_version:` is a commit SHA in the upstream repo.
  - An optional `_meta/source-map.yaml` at the plugin root that overrides per-skill — useful if the upstream layout changed.
- **Upstream location** — for each `source:` entry, a path to the upstream repo on disk (must be a git repo). Resolved via:
  1. CLI argument (`--source-root <path>` if invoked from a command).
  2. `_meta/source-map.yaml` `upstream:` field.
  3. Fallback to `SKILLS-TO-INTEGRATE/` (read-only inventory in `ai-maestro-webdesign`).
  4. If none found → degrade to a frontmatter-only report (list pins, report "cannot diff — upstream not found", stop).

## Audit procedure

See `references/drift-procedure.md` for the detailed step-by-step. Summary:

1. **Collect pins.** For every `skills/<name>/SKILL.md` in the plugin, read frontmatter `source:` (list of upstream paths) and `source_version:` (commit SHA). Flag skills missing pins as **UNPINNED** (separate finding — these can never be drift-audited).
2. **Resolve upstream.** For each unique upstream repo, get `git -C <upstream> rev-parse --short HEAD`. If equal to the pin → mark all skills using this upstream as CLEAN candidates.
3. **Diff sources.** `git -C <upstream> diff --name-only <pin> HEAD -- <union of source paths>`. Cache the changed-file set per upstream.
4. **Map changed files → skills.** A skill is affected iff at least one of its `source:` entries appears in the changed-file set.
5. **Classify per skill** — CLEAN / PIN-ONLY / STALE (see verdict definitions above).
6. **Emit plan** — write to `$MAIN_ROOT/reports/skill-drift/<timestamp>-skill-drift-audit.md`. Sections: summary verdict, STALE skills (with diff snippets + "what to re-check"), PIN-ONLY skills (mechanical bump list), UNPINNED skills (need pins added before next audit), CLEAN skills (count only).

## What this skill MUST NOT do

- **Never edit a skill.** No content rewrites, no frontmatter mutations, no version bumps. The PLAN describes what to change; humans (or a follow-up `/wavefront-plan`-style command) apply it.
- **Never commit or push.** Read-only inspection only.
- **Never assume which idiom changed.** STALE means "a `source:` file moved; review by hand". The skill does not auto-summarize the upstream diff into "the idiom is now X" — that's the re-distillation judgment call and it's a human gate.
- **Never propose new pins for unpinned skills.** Mark them UNPINNED and stop; adding pins requires reading the skill and identifying the canonical upstream source, which is authoring work, not auditing.

## Output contract

Single markdown file at the path the orchestrator specifies (default: `$MAIN_ROOT/reports/skill-drift/<YYYYMMDD_HHMMSS±HHMM>-skill-drift-audit.md`). Sections:

1. **Header** — plugin name + version, audit timestamp, upstream(s) resolved.
2. **Summary verdict** — top-line counts (CLEAN / PIN-ONLY / STALE / UNPINNED).
3. **STALE skills** — one block per skill: pin → HEAD, changed files with one-line diff summary, "re-check" pointer to the specific idiom that may have shifted.
4. **PIN-ONLY skills** — flat list with old-pin → new-pin pairs; no diff because no content changed.
5. **UNPINNED skills** — flat list with a "needs pin" note.
6. **CLEAN skills** — count only (no detail unless a skill consumes them).
7. **Next steps** — ordered: (a) author pins for UNPINNED, (b) re-distill STALE by hand, (c) bulk-bump PIN-ONLY. Each step is a single human-actionable directive.

## Examples

CLEAN:
```
amw-skill-drift-audit — ai-maestro-webdesign v0.1.0
Upstream: SKILLS-TO-INTEGRATE/web-design/ @ a1b2c3d
CLEAN: 47 skills (all pins == HEAD). Nothing to do.
```

DRIFT:
```
amw-skill-drift-audit — ai-maestro-webdesign v0.1.0
Upstream: SKILLS-TO-INTEGRATE/web-design/ @ 9f3c1d2 (pinned at 8edaa0b)

STALE (re-distill):
  amw-shadcn-ui            ← components/ui/button.tsx changed
     diff: variant API changed (added `subtle` variant; renamed `link` → `text`)
     re-check: button-variants references + the variant matrix in component-inventory.md
  amw-tailwind-4           ← tailwind/v4-migration.md changed
     diff: @theme syntax simplified; new --color-* prefix recommendation

PIN-ONLY (bump only):
  amw-design-extract       8edaa0b → 9f3c1d2 (no source change)
  amw-ascii-sketch         8edaa0b → 9f3c1d2 (no source change)
  ... 38 others

UNPINNED (needs pin):
  amw-design-system-presets (no `source:` in frontmatter)

Verdict: 2 STALE → re-distill by hand; 40 PIN-ONLY → bulk bump; 1 UNPINNED → add pin.
(No skills modified — read-only.)
```

## References

- `references/drift-procedure.md` — detailed step-by-step drift-detection algorithm, source-map resolution, diff interpretation.

## Provenance

Direct port of the `scaffold-sync` agent from **wavefront** (MIT, © 2026 pavp, [github.com/pavp/wavefront](https://github.com)) reframed as a self-contained Claude Code skill (not an agent) and generalized from "scaffold-nextjs-app + wavefront" to "any plugin's source-pinned skills". Original implementation: `wavefront/agents/scaffold-sync.md` and the companion `wavefront/skills/sync-audit/SKILL.md`. Algorithm is unchanged; the framing (skill-not-agent, plugin-not-framework, generic-upstream-not-scaffold-only) is the adaptation.
