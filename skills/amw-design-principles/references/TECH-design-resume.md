---
name: TECH-design-resume
category: orchestration
status: stable
---

# TECH: Design-workflow resume protocol

## Table of Contents

- [What it does](#what-it-does)
- [Where the resume artifact lives](#where-the-resume-artifact-lives)
- [Mandatory contract keys for a resumable session](#mandatory-contract-keys-for-a-resumable-session)
- [The resume protocol (load → diff → resume)](#the-resume-protocol-load--diff--resume)
- [Conflict-resolution rules when the contract drifts from the codebase](#conflict-resolution-rules-when-the-contract-drifts-from-the-codebase)
- [The recommendation schema returned by `amw-design-resume-agent`](#the-recommendation-schema-returned-by-amw-design-resume-agent)
- [Hard invariants](#hard-invariants)
- [Cross-references](#cross-references)

## What it does

This TECH describes the **resume protocol** the AMW webdesign workflow uses to recover from an interrupted session — `/exit` mid-Phase-A, a crash mid-Phase-B, a context wipe between days, or any other case where the orchestrator's in-memory state evaporates but on-disk artifacts (the Persistent Design Contract, the Phase A frozen spec, sub-agent reports) survive.

The protocol is implemented by two collaborating elements:

1. **`bin/amw-design-contract-validate.py --check-resumable`** — a CLI flag that returns a binary resumable / not-resumable verdict by inspecting only the contract.
2. **`agents/amw-design-resume-agent.md`** — a Tier-3 specialist that diffs the contract against on-disk artifacts and emits a structured `resume-plan` JSON that `ai-maestro-webdesign-main-agent` consumes to continue without re-elicitation.

Without this protocol, every interruption forces a full Phase A restart — wasting the locked decisions the contract was supposed to preserve. The protocol is the operational counterpart of the persistent contract's *intent*: the contract says *what was decided*, the protocol says *how to act on that decision now that the orchestrator has lost session memory*.

## Where the resume artifact lives

The orchestrator's working contract lives at:

```
<project_root>/.amw-design-contract/contract.json
```

This is the canonical, mutable session contract. The filename is **`contract.json`** (JSON, not YAML) — the `.design-contract.yaml` phrasing in the user-prompt vocabulary is a convenience label for the conceptual artifact, not the filesystem name. When a user says "resume from `.design-contract.yaml`", the resume-agent reads `.amw-design-contract/contract.json`.

History snapshots (forensic, read-only):

```
<project_root>/.amw-design-contract/history/<updated_at>.json
```

Both directories are gitignored — they contain private project state.

The frozen-spec hand-off artifact (see [phase-a-frozen-spec](phase-a-frozen-spec.md)) lives at:
> [phase-a-frozen-spec.md] Schema · Producers · Consumers · Mutability · Path conventions · Worked example · Cross-references

```
<project_root>/reports/webdesigner/phase-a-frozen/<YYYYMMDD_HHMMSS±HHMM>-frozen-spec.json
```

Sub-agent reports (Phase A discovery, Phase B production / audit / scenario):

```
<project_root>/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>-<agent-name>-<slug>.md
```

Together these three locations form the full on-disk state the resume protocol inspects.

## Mandatory contract keys for a resumable session

`amw-design-contract-validate.py --check-resumable` exits 0 (resumable) iff **all** the following keys are present and non-empty in the contract JSON. Anything missing exits 1 (needs more elicitation) without claiming the contract is broken — a sparse contract is still a legitimate Phase A seed.

| Section | Keys required for resumability | Why each is mandatory |
|---|---|---|
| `meta` | `schema_version`, `contract_id`, `created_at`, `updated_at`, `phase` | The phase marker tells the resume-agent which decision branch to take. Timestamps tell it whether the on-disk artifacts are newer or older than the contract. The schema_version must match `SUPPORTED_SCHEMA_VERSION` or resume is unsafe. |
| `user_intent` | `project_name`, `industry`, `primary_audience`, `primary_action`, `tone` | Without these, Phase B sub-agents have no anchor for what they are building. A resume that cannot prove these are present must fall back to Phase A. |
| `brand_tokens` | `primary_color`, `color_mode`, `display_font`, `body_font`, `border_radius_bucket` | The minimal brand contract every Phase B production agent reads. Missing any of them means resume cannot route into Phase B. |
| `target_stack` | `framework` | The fan-out roster depends on framework; without it, the resume-agent cannot enumerate the expected Phase B sub-agents. |
| `decisions_log` | non-empty (at least one entry) | The lock decision that ended Phase A or any later locked decision. An empty decisions_log means no decision was ever recorded — there is nothing to resume *from*. |

These five blocks define **mandatory keys**: `user_intent.project_name`, `user_intent.industry`, `user_intent.primary_audience`, `user_intent.primary_action`, `user_intent.tone`, `brand_tokens.primary_color`, `brand_tokens.color_mode`, `brand_tokens.display_font`, `brand_tokens.body_font`, `brand_tokens.border_radius_bucket`, `target_stack.framework`, `decisions_log` (non-empty list), `meta.phase`, `meta.created_at`, `meta.updated_at`, `meta.schema_version`, `meta.contract_id`.

Notes on the table above:

- The `--check-resumable` flag is a stricter superset of the regular validator's PASS rule. The regular validator allows `phase: "phase_a_discovery"` with an empty decisions_log (it's the legitimate starting state); `--check-resumable` does NOT — discovery from scratch is not "resumable", it's just "start fresh".
- Advisory FLAG-only fields (`reference_urls`, `success_metrics`, `neutral_palette`, `preset_fingerprint`, `css_strategy`) do NOT block resumability. They are nice-to-have, not mandatory.
- The check is over the **contract** only — it does not inspect on-disk reports. The resume-agent does the contract-vs-disk diff.

## The resume protocol (load → diff → resume)

The full protocol runs in three steps:

### Step 1 — Load

1. The orchestrator (or main-agent) detects a chat starts in a project with `.amw-design-contract/contract.json` present.
2. Main-agent spawns `amw-design-resume-agent` with the contract path.
3. The resume-agent first runs `bin/amw-design-contract-validate.py <contract_path> --check-resumable`:
   - exit 0 → contract is resumable; proceed to Step 2.
   - exit 1 → contract is too sparse; recommend "treat as Phase A seed — pre-fill from existing fields and re-elicit the missing ones." End protocol here.
   - exit 2 → contract is BLOCK-malformed; recommend "invoke `amw-design-contract-validator-agent` to surface and repair the BLOCKs before retrying resume." End protocol here.
4. The resume-agent reads the contract JSON in full and captures `meta.phase`, `meta.updated_at`, every mandatory key, and the `decisions_log`.

### Step 2 — Diff against current repo state

The resume-agent enumerates on-disk artifacts:

- `reports/webdesigner/phase-a-frozen/*.json` — Phase A frozen specs. The newest one's timestamp tells the resume-agent when Phase B was last fanned out.
- `reports/webdesigner/<ts>-<agent>-*.md` — sub-agent reports. The resume-agent buckets them by sub-agent name and reads only the **latest** report's YAML header per bucket.

The diff produces three sets:

1. **`completed_subagents`** — sub-agents whose latest report exists and `status: ok`.
2. **`pending_subagents`** — sub-agents the workflow expects but whose reports are missing or whose latest report is `failed` / `partial`. Ordered per [agent-interaction-patterns](phase-a-frozen-spec.md) sequencing rules.
3. **`drift_findings`** — discrepancies between contract intent and on-disk state. Examples:
   - report present for a sub-agent whose name never appears in `decisions_log[].actor`
   - `meta.updated_at` is older than the latest on-disk report
   - frozen spec exists but contract is still `phase_a_locked` (never updated to `phase_b`)

### Step 3 — Recommend a resume point

The resume-agent applies the decision table in `agents/amw-design-resume-agent.md` §7 step 7 (Operations) and emits one of these recommendations:

| Recommended phase | Meaning | What main-agent does next |
|---|---|---|
| `phase_a_discovery` | Contract was empty or near-empty | Run Phase A resource discovery, pre-fill from contract |
| `phase_a_lowfi` | Phase A iteration was mid-flight | Re-propose the latest variant the contract describes |
| `phase_a_locked` | Lock decision exists but the contract is still in lowfi | Update `meta.phase` to `phase_a_locked` and proceed to freeze |
| `phase_a_freeze` | Lock recorded but no frozen spec on disk | Run `bin/amw-freeze-phase-a.sh` next |
| `phase_b` (with `pending_subagents`) | Phase B fan-out was partial | Spawn the pending sub-agents in sequencing order |
| `phase_b_complete` | Every expected Phase B report present and `status=ok` | Emit the final job-completion report |
| `escalate` | Drift cannot be silently bridged | Surface the diff to the user and ask for resolution |

The full `resume-plan` JSON shape is documented in the recommendation-schema section below.

## Conflict-resolution rules when the contract drifts from the codebase

Drift between the contract (intent) and the codebase (actual state on disk) is the entire reason this protocol exists. The resolution rules are priority-ordered:

### Rule 1 — On-disk artifact existence over contract claims

If the contract claims `phase: "phase_b"` but no frozen-spec file exists on disk, the contract is **wrong about progress**. Trust the disk: treat the phase as `phase_a_locked`, recommend "emit frozen spec next". The contract `meta.phase` was set optimistically and the freeze step never ran.

Inverse: if a frozen spec exists but the contract is still `phase_a_locked`, the freeze ran but the contract update was interrupted. Recommend "append a back-dated decisions_log entry to bump phase to `phase_b`, then fan out". No user re-elicitation.

### Rule 2 — Contract intent over orchestrator memory

When `meta.phase` (durable on disk) and the user's verbal "I think we were at X" (volatile session memory) disagree, **the contract wins**. The protocol exists because session memory is unreliable across days/restarts; the contract is the durable substitute.

### Rule 3 — Resume the next un-run sub-agent, never a completed one

A sub-agent report whose latest YAML header says `status: ok` is **done**. Re-spawning it would either no-op (if the agent is idempotent) or — worse — overwrite a good artifact with a fresh one. The resume protocol skips any sub-agent whose latest report is `ok` and resumes at the next pending sub-agent in the sequence.

A report with `status: failed` is **not** completed — recommend re-spawning that sub-agent. A report with `status: partial` is a judgment call — surface to main-agent as a FLAG; main-agent decides whether the partial output is good enough.

### Rule 4 — Drift signals require escalation, never silent bridging

When the contract and disk disagree in a way Rule 1 and Rule 3 do not cover — e.g. a report exists from a sub-agent whose name never appears in `decisions_log[].actor`, or two reports from the same sub-agent have inconsistent statuses — the resume-agent returns `status=partial`, `next_action=escalate_to_user`. It does NOT pick a side. The user (via main-agent) decides whether to trust the report and back-date a decisions_log entry, or discard the report and re-run the sub-agent.

### Rule 5 — Stale Phase B reports vs. re-iterated Phase A

If Phase A was re-iterated mid-Phase-B (a new frozen spec emitted with a newer timestamp than the previous one), every Phase B report whose timestamp is **older** than the latest frozen spec is **stale**. Recommend re-running those sub-agents with the new frozen-spec path. The old reports stay on disk for audit trail but are no longer authoritative.

### Rule 6 — Multiple contracts

Only the canonical `<project_root>/.amw-design-contract/contract.json` is authoritative. History snapshots at `<project_root>/.amw-design-contract/history/<ts>.json` are forensic — never resume from a history file. If main-agent (or a user) passes a history path as `contract_path`, the resume-agent returns `status=failed` with `blocking_issues=["history file passed; pass the canonical contract.json instead"]`.

### Rule 7 — `--check-resumable` exit 1 is not a BLOCK

A sparse contract (e.g. `phase_a_discovery` with `user_intent.project_name` empty) is not "broken" — it's "interrupted before useful state accumulated". Recommend "treat as Phase A seed and re-elicit", not "halt". Distinct from `--check-resumable` exit 2, which corresponds to the regular validator's BLOCK verdict (malformed JSON, missing required sections, schema-version mismatch) — that IS unsafe to resume from and must be repaired first.

## The recommendation schema returned by `amw-design-resume-agent`

The resume-agent writes a structured JSON artifact at `<output_dir>/contract-resume-<YYYYMMDD_HHMMSS±HHMM>.json` with this shape:

```json
{
  "resumable": true,
  "recommended_phase": "phase_b",
  "next_step_label": "Resume Phase B fan-out at accessibility-auditor, seo-strategist, browser-tester",
  "completed_subagents": [
    "amw-wireframe-builder-agent"
  ],
  "pending_subagents": [
    "amw-accessibility-auditor-agent",
    "amw-seo-strategist-agent",
    "amw-browser-tester-agent"
  ],
  "last_artifact_path": "/abs/path/to/reports/webdesigner/20260527_101842+0200-amw-wireframe-builder-aurora-spa-home.md",
  "drift_findings": [],
  "contract_excerpt": {
    "meta": {
      "phase": "phase_a_locked",
      "schema_version": "1",
      "updated_at": "2026-05-27T11:42:18+02:00"
    },
    "decisions_log_count": 4,
    "decisions_log_last_entry": {
      "timestamp": "2026-05-27T11:42:18+02:00",
      "decision": "Locked Cormorant Garamond + Inter pairing after brand-researcher report.",
      "actor": "main-agent"
    }
  }
}
```

Field semantics:

- `resumable` — boolean. `true` iff `--check-resumable` exited 0 and no drift requires escalation.
- `recommended_phase` — one of `phase_a_discovery | phase_a_lowfi | phase_a_locked | phase_a_freeze | phase_b | phase_b_complete | escalate`.
- `next_step_label` — single line human-readable label main-agent can paraphrase to the user.
- `completed_subagents`, `pending_subagents` — arrays of sub-agent names. Phase B only; empty arrays when `recommended_phase` is a Phase A state.
- `last_artifact_path` — absolute path to the most recent useful on-disk artifact (the latest sub-agent report when Phase B is partial; the frozen spec when Phase B has not started; the contract itself otherwise).
- `drift_findings` — array of single-line strings. Empty when there is no drift; non-empty when Rule 4 triggers.
- `contract_excerpt` — minimum context main-agent needs to act on the recommendation without re-reading the full contract.

Main-agent consumes the JSON, paraphrases `next_step_label` to the user (when user-facing dialog is appropriate), and runs the recommended next step.

## Hard invariants

1. **The contract file is never auto-edited by the resume protocol.** The resume-agent is read-only. Repairs flow through main-agent and (if needed) `amw-design-contract-validator-agent`.
2. **`--check-resumable` exit codes:** 0 = resumable, 1 = sparse (treat as Phase A seed), 2 = BLOCK (repair before retry), 64 = invocation error (bad path).
3. **A sparse contract is not a broken contract.** Exit 1 means "not enough state to skip Phase A", not "the contract is bad".
4. **Drift between contract and disk is escalation territory.** Rule 4 forbids silent bridging.
5. **Phase A frozen specs are the canonical Phase A → Phase B hand-off** — their presence/absence is the single most reliable signal of whether Phase B was reached.
6. **Stale Phase B reports (older than the latest frozen spec) must be re-run, not re-trusted.** Rule 5.
7. **Only `<project_root>/.amw-design-contract/contract.json` is authoritative** — history snapshots are forensic. Rule 6.

## Cross-references

- [agent-authoring-philosophy](agent-authoring-philosophy.md) — judgment vs recipe layer that `amw-design-resume-agent` follows
  > Skills and agents are not the same kind of thing · What an agent actually needs · Recipe layer (deterministic floor) · Judgment layer (non-deterministic surface) · Why the judgment layer matters in this plugin specifically · The 14-section canonical template · What this document is NOT · Cross-references
- [phase-a-frozen-spec](phase-a-frozen-spec.md) — the freeze artifact this protocol diffs the contract against
  > Schema · Producers · Consumers · Mutability · Path conventions · Worked example · Cross-references
- [agent-interaction-patterns](agent-interaction-patterns.md) — Phase B sequencing rules that order `pending_subagents`
  > Topology invariants · Phase A data flow · Phase B data flow · What main-agent does between sub-agent calls · Error propagation · Why this topology (instead of peer-to-peer) · Enforcement
- [sub-agent-return-contract](sub-agent-return-contract.md) — the YAML header shape every sub-agent's report uses
  > Schema · Field semantics · Markdown body structure · How main-agent consumes the contract · Contract invariants
- [iteration-budget](iteration-budget.md) — one-shot diagnosis cap for the resume agent
  > Canonical caps by loop type · What "attempt" means · `attempts_log[]` telemetry contract · What happens when the cap is reached · What this is NOT · How agents apply this · Cross-references
- [TECH-design-contract](../../amw-design-md/references/TECH-design-contract.md) — canonical schema for the contract this protocol resumes from
  > What it does · How it relates to phase-a-frozen-spec.md · JSON schema (version 1) · `meta` · `user_intent` · `brand_tokens` · `ia` · `legal` · `target_stack` · `decisions_log` · Lifecycle · Validator (BLOCK / FLAG / PASS) · Storage and versioning · Hard invariants · Cross-references
- `../../../bin/amw-design-contract-validate.py` — implements `--check-resumable`
- `../../../agents/amw-design-resume-agent.md` — the resume-agent that follows this protocol
- `../../../agents/amw-design-contract-validator-agent.md` — peer validator the resume-agent recommends invoking on BLOCK contracts
