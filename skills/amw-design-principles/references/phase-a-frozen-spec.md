## Table of Contents

- [Schema](#schema)
- [Producers](#producers)
- [Consumers](#consumers)
- [Mutability](#mutability)
- [Path conventions](#path-conventions)
- [Worked example](#worked-example)
- [Cross-references](#cross-references)

# Phase A.5 Frozen Spec — canonical Phase B input contract

This document defines the `phase-a-frozen-spec.json` schema and the protocol around it. The frozen spec is the single source of truth that every Phase B sub-agent reads at startup. It exists because the prior pattern — main-agent paraphrasing N Phase A YAML headers into N Phase B input contracts — burned an estimated **~30K orchestrator tokens per multi-artifact workflow** in redundant data-plumbing (4× duplicate `ai-slop-avoid.md` reads, 3× `color-system.md` reads, 6× return-contract spec reads, plus the per-sub-agent paraphrase passes). With the frozen spec, the cost is one `bin/amw-freeze-phase-a.sh` invocation and one absolute path passed into every Phase B input contract.

The frozen spec is produced exactly once per Phase B run. It is **immutable for the duration of that run** — Phase B agents that detect drift (the `approved_ascii_sha256` no longer matches the file's current sha256) must fail fast and refuse to proceed. To incorporate fresh user input, main-agent emits a NEW frozen spec with a new timestamp and re-fans-out Phase B; the old spec stays on disk for audit trail.

## Schema

```json
{
  "frozen_at": "2026-04-30T18:30:12+0200",
  "frozen_spec_version": "1",
  "approved_ascii_path": "/abs/path/to/amw-sketch-final.txt",
  "approved_ascii_sha256": "d32a60d704a684a8313dc90ab28f800465c0e6c08a60e9274dd4ce0986751739",
  "brand_tokens_path": "/abs/path/to/tokens.json",
  "design_md_path": "/abs/path/to/DESIGN.md",
  "ia_structure_path": "/abs/path/to/ia.json",
  "copy_blocks_path": "/abs/path/to/copy-en-fr.json",
  "legal_mandatory_elements_path": "/abs/path/to/legal-fragments.html",
  "seo_head_path": "/abs/path/to/seo-head.json",
  "personas_path": "/abs/path/to/personas.md",
  "target_stack": "shadcn+next",
  "locales": ["en", "fr"],
  "output_dir": "/abs/path/to/design/mockups/",
  "wcag_target": "AA"
}
```

### Field reference

| Key | Type | Required | Semantic meaning | Fallback when null |
|---|---|---|---|---|
| `frozen_at` | string (ISO-8601 with offset, e.g. `2026-04-30T18:30:12+0200`) | YES | Local-time timestamp + GMT offset of when this spec was emitted. Used for ordering and audit. | n/a — required |
| `frozen_spec_version` | string | YES | Always `"1"` for this schema. Future schema changes bump this; consumers may refuse unknown versions. | n/a — required |
| `approved_ascii_path` | absolute path | YES | The ASCII variant the user approved at the satisfaction gate (Phase A → Phase B transition). | n/a — required |
| `approved_ascii_sha256` | 64-char hex | YES | sha256 of the file at `approved_ascii_path` at freeze time. Consumer agents recompute and refuse to proceed on mismatch. | n/a — required |
| `brand_tokens_path` | absolute path | YES | Token JSON from `amw-brand-researcher-agent` (or user-supplied). Source of color / spacing / typography. | n/a — required |
| `design_md_path` | absolute path | YES | Variant 1 / Variant 2 DESIGN.md (author / extractor / user-supplied). Canonical token + section reference. | n/a — required |
| `ia_structure_path` | absolute path | YES | Information-architecture JSON (sections, hierarchy, navigation). | n/a — required |
| `copy_blocks_path` | absolute path \| null | optional | Locale-keyed copy blocks. Skip when single-locale and copy is inline in the ASCII / IA. | consumer agents fall back to inline copy from the approved ASCII or use placeholder slots |
| `legal_mandatory_elements_path` | absolute path \| null | optional | HTML or JSON with mandatory legal fragments (cookie banner, disclaimers, age gate). Skip when no regulatory requirements. | consumer agents skip the legal-fragment injection step; legal-expert (B mode) audit will flag missing elements if any apply |
| `seo_head_path` | absolute path \| null | optional | SEO `<head>` fragments + structured-data JSON-LD. Skip when SEO is not in scope. | consumer agents emit a generic `<head>` (charset / viewport / title only) |
| `personas_path` | absolute path \| null | optional | User-research personas markdown. Skip when no user-research provided. | consumer agents proceed without persona-tuned microcopy / empty-state text |
| `target_stack` | string | YES | Implementation target. Examples: `shadcn+next`, `vanilla-html`, `astro`, `email-mjml`. | n/a — required |
| `locales` | string array | YES | BCP-47 locale codes. Single-element array `["en"]` is the single-locale case. | n/a — required |
| `output_dir` | absolute path | YES | Where Phase B agents write their final artifacts. Created if absent. | n/a — required |
| `wcag_target` | `"AA"` \| `"AAA"` | YES | Accessibility target. Drives contrast checks, focus-ring visibility, motion gating. | n/a — required |

Consumers MUST NOT add or rename keys. Schema evolution bumps `frozen_spec_version` and the new keys land in version `"2"`.

## Producers

**Only `ai-maestro-webdesign-main-agent` writes a frozen spec**, and it does so exactly once between the Phase A satisfaction gate and the Phase B fan-out. Phase A sub-agents do NOT write to the spec directly — they emit their own reports per the standard sub-agent return contract, and main-agent aggregates the relevant `report_path` / `artifact_path` values into the spec via `bin/amw-freeze-phase-a.sh`.

The freeze invocation:

```bash
bash bin/amw-freeze-phase-a.sh \
  --approved-ascii  "<abs path>" \
  --brand-tokens    "<abs path>" \
  --design-md       "<abs path>" \
  --ia              "<abs path>" \
  --copy            "<abs path | omit>" \
  --legal           "<abs path | omit>" \
  --seo-head        "<abs path | omit>" \
  --personas        "<abs path | omit>" \
  --target-stack    "shadcn+next" \
  --locales         "en,fr" \
  --output-dir      "<abs path>" \
  --wcag-target     "AA" \
  --out             "$MAIN_ROOT/reports/webdesigner/phase-a-frozen/<ts±tz>-frozen-spec.json"
```

Optional flags (`--copy`, `--legal`, `--seo-head`, `--personas`) are omitted when the corresponding domain is out of scope for the run. The script emits `null` for any optional field whose flag was not passed.

## Consumers

**Every Phase B sub-agent receives `frozen_spec_path: <abs-path>` in its input contract** and reads only the keys it needs. The agent never receives the individual artifact paths — those are resolved out of the JSON. Typical consumption matrix:

| Phase B sub-agent | Keys typically read |
|---|---|
| `amw-wireframe-builder-agent` | `approved_ascii_path`, `approved_ascii_sha256`, `brand_tokens_path`, `design_md_path`, `ia_structure_path`, `copy_blocks_path`, `legal_mandatory_elements_path`, `seo_head_path`, `target_stack`, `locales`, `output_dir`, `wcag_target` |
| `amw-diagram-producer-agent` | `design_md_path` (for color / typography tokens), `output_dir` |
| `amw-infographic-builder-agent` | `brand_tokens_path`, `design_md_path`, `output_dir` |
| `amw-asset-generator-agent` | `brand_tokens_path` (token-driven SVG), `output_dir` |
| `amw-video-producer-agent` | `brand_tokens_path`, `output_dir` |
| `amw-form-designer-agent` | `design_md_path`, `copy_blocks_path` (microcopy / errors), `wcag_target`, `locales` |
| `amw-motion-designer-agent` | `design_md_path`, `wcag_target` (reduced-motion gating) |
| `amw-email-designer-agent` | `brand_tokens_path`, `design_md_path`, `copy_blocks_path`, `output_dir`, `locales` |
| `amw-component-library-architect-agent` | `brand_tokens_path`, `design_md_path`, `output_dir` |
| `amw-accessibility-auditor-agent` (B mode) | `wcag_target`, `design_md_path` (contrast pre-flight), the artifact paths returned by upstream producers |
| `amw-seo-strategist-agent` (B mode) | `seo_head_path`, `ia_structure_path`, the artifact paths returned by upstream producers |
| `amw-browser-tester-agent` | `output_dir`, the artifact paths returned by upstream producers |
| `amw-legal-expert-agent` (B mode) | `legal_mandatory_elements_path`, the artifact paths returned by upstream producers |

Each agent decides which keys it needs; the consumption matrix above is descriptive, not prescriptive. Agents MUST treat absent (null) optional keys per the "Fallback when null" column of the schema table.

## Mutability

The frozen spec is **immutable for the duration of one Phase B run**. Specifically:

1. Once `bin/amw-freeze-phase-a.sh` writes the JSON, the spec file is read-only by convention. Phase B agents do not write to it. Main-agent does not edit it.
2. Phase B agents that read the spec MUST recompute the sha256 of `approved_ascii_path` and compare to `approved_ascii_sha256`. On mismatch, the agent emits:
   ```yaml
   status: failed
   blocking_issues:
     - "frozen spec checksum mismatch — main-agent must re-freeze before retry"
   ```
   and refuses to proceed.
3. If main-agent needs to change a hand-off (e.g. the user re-iterates on copy after Phase B has partially run), the procedure is:
   1. Cancel any in-flight Phase B work (sub-agents that haven't started skip; sub-agents in flight finish their current step and abandon).
   2. Iterate Phase A as needed (re-spawn discovery agents, re-render ASCII variants).
   3. Emit a NEW frozen spec with a new timestamp via a fresh `bin/amw-freeze-phase-a.sh` invocation — the new path goes to `<MAIN_ROOT>/reports/webdesigner/phase-a-frozen/<new-ts±tz>-frozen-spec.json`.
   4. Re-fan-out Phase B with the new `frozen_spec_path` in every sub-agent's input contract.
4. The old spec stays on disk forever (gitignored under `reports/`). Audit tools can reconstruct the chain of frozen specs by sorting filenames lexicographically.

## Path conventions

Every path inside the spec is **absolute** (resolved through `python3 -c "import os; print(os.path.realpath(...))"` for cross-platform correctness). Relative paths are forbidden — Phase B sub-agents may run with a different working directory than main-agent.

The spec file itself is written to:

```
<MAIN_ROOT>/reports/webdesigner/phase-a-frozen/<YYYYMMDD_HHMMSS±HHMM>-frozen-spec.json
```

where `<MAIN_ROOT>` is resolved via `git worktree list | head -n1 | awk '{print $1}'` per `~/.claude/rules/agent-reports-location.md`. Both `/reports/` and `/reports_dev/` are gitignored.

The `output_dir` field is the directory where Phase B's *user-facing* artifacts (HTML, SVG, MP4, MJML) land — typically inside the user's project, not under `reports/`. The spec itself is operational state, not a user-facing artifact.

## Worked example

A luxury-resort landing page with two locales (English + French), GDPR scope, full SEO, and persona-driven empty states.

**Phase A produced:**
- `amw-brand-researcher-agent` report → competitor analysis + `tokens.json` at `~/projects/serene-isles/research/brand/tokens.json`
- `amw-design-md-extractor-agent` report → `~/projects/serene-isles/DESIGN.md` (extracted from a reference URL)
- `amw-user-research-analyst-agent` report → `~/projects/serene-isles/research/personas.md` + `ia.json`
- `amw-legal-expert-agent` report → `~/projects/serene-isles/legal/cookie-banner.html`
- `amw-seo-strategist-agent` (Phase A) report → `~/projects/serene-isles/seo/head-fragments.json`
- `amw-multilanguage-copywriter-agent` report → `~/projects/serene-isles/copy/copy-en-fr.json`
- The approved ASCII variant → `/tmp/amw-sketch-serene-isles-final.txt`

**Main-agent runs:**

```bash
bash bin/amw-freeze-phase-a.sh \
  --approved-ascii "/tmp/amw-sketch-serene-isles-final.txt" \
  --brand-tokens   "${CLAUDE_PROJECT_DIR}/research/brand/tokens.json" \
  --design-md      "${CLAUDE_PROJECT_DIR}/DESIGN.md" \
  --ia             "${CLAUDE_PROJECT_DIR}/research/ia.json" \
  --copy           "${CLAUDE_PROJECT_DIR}/copy/copy-en-fr.json" \
  --legal          "${CLAUDE_PROJECT_DIR}/legal/cookie-banner.html" \
  --seo-head       "${CLAUDE_PROJECT_DIR}/seo/head-fragments.json" \
  --personas       "${CLAUDE_PROJECT_DIR}/research/personas.md" \
  --target-stack   "shadcn+next" \
  --locales        "en,fr" \
  --output-dir     "${CLAUDE_PROJECT_DIR}/design/mockups" \
  --wcag-target    "AA" \
  --out            "/path/to/Code/AI-MAESTRO-WEBDESIGN-AGENT/reports/webdesigner/phase-a-frozen/20260430_183012+0200-frozen-spec.json"
```

**Resulting spec** (abbreviated):

```json
{
  "frozen_at": "2026-04-30T18:30:12+0200",
  "frozen_spec_version": "1",
  "approved_ascii_path": "/tmp/amw-sketch-serene-isles-final.txt",
  "approved_ascii_sha256": "d32a60d704a684a8313dc90ab28f800465c0e6c08a60e9274dd4ce0986751739",
  "brand_tokens_path": "${CLAUDE_PROJECT_DIR}/research/brand/tokens.json",
  "design_md_path": "${CLAUDE_PROJECT_DIR}/DESIGN.md",
  "ia_structure_path": "${CLAUDE_PROJECT_DIR}/research/ia.json",
  "copy_blocks_path": "${CLAUDE_PROJECT_DIR}/copy/copy-en-fr.json",
  "legal_mandatory_elements_path": "${CLAUDE_PROJECT_DIR}/legal/cookie-banner.html",
  "seo_head_path": "${CLAUDE_PROJECT_DIR}/seo/head-fragments.json",
  "personas_path": "${CLAUDE_PROJECT_DIR}/research/personas.md",
  "target_stack": "shadcn+next",
  "locales": ["en", "fr"],
  "output_dir": "${CLAUDE_PROJECT_DIR}/design/mockups",
  "wcag_target": "AA"
}
```

**Main-agent then fans out Phase B**, passing only `frozen_spec_path: "/path/to/Code/AI-MAESTRO-WEBDESIGN-AGENT/reports/webdesigner/phase-a-frozen/20260430_183012+0200-frozen-spec.json"` to every sub-agent's input contract. `amw-wireframe-builder-agent` reads the spec and resolves the keys it needs; `amw-diagram-producer-agent` reads only `design_md_path` and `output_dir`; `amw-accessibility-auditor-agent` (B) reads `wcag_target` and `design_md_path`. None of them re-derives token decisions, copy decisions, or IA decisions — those are already on disk and pinned via the sha256.

## Cross-references

- [agent-interaction-patterns](./agent-interaction-patterns.md) — data hand-off table; every row maps to a key in the frozen spec.
  > Topology invariants · Phase A data flow · Phase A data hand-offs (carried by main-agent between sub-agent invocations) · Phase B data flow · Phase B data hand-offs · Phase B sequencing rules · What main-agent does between sub-agent calls · Error propagation · Why this topology (instead of peer-to-peer) · Enforcement
- [sub-agent-return-contract](./sub-agent-return-contract.md) — the YAML headers Phase A sub-agents return; main-agent harvests `report_path` / `artifact_path` values from those headers when assembling the spec.
  > Schema · Field semantics · `agent` — required, string · `phase` — required, enum `A | B` · `status` — required, enum `ok | partial | failed` · `confidence` — required, enum `high | medium | low` · `execution_time_ms` — optional, int · `max_iterations` — required, int · `attempts_count` — required, int · `attempts_log` — required, list of objects · `blocking_issues` — required (empty list ok), list of strings · `warnings` — required (empty list ok), list of strings · `artifact_paths` — required (empty list ok), list of objects · `recommendations` — required (empty list ok), list of strings · `next_action` — required, string (free-form but see conventions) · `report_path` — required, string · Markdown body structure · How main-agent consumes the contract · Contract invariants (enforced by smoke tests)
- [two-mode-workflow](./two-mode-workflow.md) — the Phase A satisfaction gate and the Phase A → Phase B transition.
  > Sub-agent delegation (Main-agent mode only) · Naming convention · One-way delegation rule · Delegation timing · Full sub-agent roster (19 amw-* agents across four tiers) · Cross-references · Mode Detection · Command mode signals (fast path — dispatch immediately) · Main-agent mode signals (requirements path — enter Phase A first) · Tie-breaking rule · Phase A — Iterative Low-Fi Loop · Inputs · Low-fi artifact types (pick the cheapest that fits) · Iteration rules · RDD (Requirements Design Document) — auto-pass Phase A · Satisfaction gate (hard stop — non-skippable) · What Phase A does NOT include · Phase B — Implementation and Spawning · Transition protocol · Sub-agent spawning rules · Non-conversation rule · Job-completion report · Scenario Testing via dev-browser (mandatory in Phase B) · What a scenario test covers · dev-browser is the ONLY input-automation primitive · Scenario test output format · Anti-Patterns · Skipping Phase A when requirements are vague · Starting Phase B before explicit approval · Spawning sub-agents during Phase A · …(+3)
- `../../../bin/amw-freeze-phase-a.sh` — the producer script (only main-agent invokes it).
- [ai-maestro-webdesign-main-agent](../../../agents/ai-maestro-webdesign-main-agent.md) §15 — the orchestration doctrine that mandates Phase A.5 between satisfaction gate and Phase B fan-out.
