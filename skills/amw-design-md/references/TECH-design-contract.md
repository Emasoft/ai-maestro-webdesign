---
name: TECH-design-contract
category: orchestration
source: design-forge-main/SKILL.md L64-L136, design-forge-main/references/contract-validator.md (MIT)
also-in: amw-design-principles/references/phase-a-frozen-spec.md, amw-design-principles/references/agent-interaction-patterns.md
status: stable
---

# TECH: Persistent Design Contract (session-spanning input contract)

## Table of Contents

- [What it does](#what-it-does)
- [How it relates to phase-a-frozen-spec.md](#how-it-relates-to-phase-a-frozen-spec-md)
- [JSON schema (version 1)](#json-schema-version-1)
  - [`meta`](#meta)
  - [`user_intent`](#user_intent)
  - [`brand_tokens`](#brand_tokens)
  - [`ia`](#ia)
  - [`legal`](#legal)
  - [`target_stack`](#target_stack)
  - [`decisions_log`](#decisions_log)
- [Lifecycle](#lifecycle)
- [Validator (BLOCK / FLAG / PASS)](#validator-block--flag--pass)
- [Storage and versioning](#storage-and-versioning)
- [Hard invariants](#hard-invariants)
- [Cross-references](#cross-references)

## What it does

The **Persistent Design Contract** is a JSON document the `ai-maestro-webdesign-main-agent` builds incrementally during a session and threads into every Phase B sub-agent call. It captures:

1. **User intent** — industry, audience, primary action, tone of voice.
2. **Locked brand tokens** — primary color, color mode, fonts, border-radius bucket.
3. **Information architecture** — pages + primary navigation.
4. **Legal mandatories** — jurisdictions + hard compliance requirements (GDPR cookie banner, ADA, etc.).
5. **Target stack** — implementation framework + CSS strategy.
6. **Decisions log** — an append-only record of every locked choice with timestamp + actor, so a later agent can audit *why* the contract looks the way it does.

The contract is the orchestrator's working memory between user turns. Without it, every Phase A turn would have to re-derive the same context, and every Phase B sub-agent would have to re-paraphrase user requirements into its own input contract (the failure mode quantified at **~30K orchestrator tokens per multi-artifact workflow** in [phase-a-frozen-spec.md](../../amw-design-principles/references/phase-a-frozen-spec.md)).

This TECH is the direct port of design-forge's "Design Contract" pattern (MIT) adapted to the AMW agent topology.

## How it relates to phase-a-frozen-spec.md

The Persistent Design Contract and the [Phase A Frozen Spec](../../amw-design-principles/references/phase-a-frozen-spec.md) are complementary, not redundant.

| Aspect | Persistent Design Contract (this TECH) | Phase A Frozen Spec |
|---|---|---|
| Lifetime | Whole session (across Phase A and Phase B; survives restarts via on-disk JSON) | Single Phase B fan-out (immutable for one run) |
| Format | JSON, dictionary-shaped, sections | JSON, flat key-value, paths |
| Producer | `main-agent` updates after every locked decision | `main-agent` writes once via `bin/amw-freeze-phase-a.sh` |
| Consumer | `main-agent` reads on every turn; Phase B agents may read for context | Every Phase B sub-agent reads at startup |
| Mutability | Append-only via `decisions_log`; sections can be edited as the contract evolves | Immutable for the duration of one Phase B run |
| What it carries | Decisions + rationale + accumulated context | Concrete file paths + SHA256s of locked artifacts |
| Schema location | `bin/amw-design-contract-validate.py` SUPPORTED_SCHEMA_VERSION | `bin/amw-freeze-phase-a.sh` |

Pipeline: orchestrator builds + updates the **contract** during Phase A. At the satisfaction gate, orchestrator emits a **frozen spec** that points to the on-disk artifacts the contract describes. Phase B agents read **both**: contract for *why*, frozen spec for *what / where*.

## JSON schema (version 1)

A canonical contract has exactly this top-level shape. Additional top-level keys are tolerated by the validator but are not enforced.

```json
{
  "meta": { ... },
  "user_intent": { ... },
  "brand_tokens": { ... },
  "ia": { ... },
  "legal": { ... },
  "target_stack": { ... },
  "decisions_log": [ ... ]
}
```

### `meta`

| Key | Type | Required | Semantic |
|---|---|---|---|
| `schema_version` | string | YES | Always `"1"` for this schema. Validator BLOCKs on mismatch. |
| `contract_id` | string | YES | Stable identifier, typically `<yyyymmdd>-<slug>`. |
| `created_at` | ISO-8601 string with TZ offset | YES | When the contract was first emitted. |
| `updated_at` | ISO-8601 string with TZ offset | YES | When the contract was last mutated. Bumped on every edit. |
| `phase` | `phase_a_discovery` \| `phase_a_lowfi` \| `phase_a_locked` \| `phase_b` | YES | Where the orchestrator is in the workflow. |

### `user_intent`

| Key | Type | Required | Semantic |
|---|---|---|---|
| `project_name` | string | YES | Human-readable name. |
| `industry` | string | YES | E.g. `b2b SaaS / devtools`, `hospitality / wellness`. |
| `primary_audience` | string | YES | Who the page is for. Specifics > demographics. |
| `primary_action` | string | YES | Single most important visitor outcome (book a stay, start a trial). |
| `tone` | string | YES | 1-3 adjectives. Drives token contradiction detection. |
| `reference_urls` | string array | advisory (FLAG when empty) | Competitor / inspiration URLs. |
| `success_metrics` | string array | advisory (FLAG when empty) | Measurable goals tied to the primary action. |

### `brand_tokens`

| Key | Type | Required | Semantic |
|---|---|---|---|
| `primary_color` | hex string (`#RGB` / `#RRGGBB` / `#RRGGBBAA`) | YES | Primary brand color. |
| `color_mode` | `LIGHT` \| `DARK` | YES | Page color mode. |
| `display_font` | string | YES | Display / headline font family. |
| `body_font` | string | YES | Body copy font family. |
| `border_radius_bucket` | one of `ROUND_FOUR` / `ROUND_EIGHT` / `ROUND_TWELVE` / `ROUND_FULL` (or lowercase / `4px` / `8px` / `12px` / `9999px` / `full`) | YES | Coarse-grain radius bucket. Matches design-forge spec. |
| `neutral_palette` | hex string array | advisory (FLAG when empty) | Neutral ramp the orchestrator gives Phase B. |
| `preset_fingerprint` | string | advisory (FLAG when empty) | Identity tag for the validator's preset check (e.g. `luxury-dark-serif`). |

### `ia`

| Key | Type | Required | Semantic |
|---|---|---|---|
| `pages` | array of `{name, slug, purpose}` objects | YES, non-empty | Every page the project covers. |
| `primary_nav` | string array | YES, non-empty | Primary nav order, by page name. |

### `legal`

| Key | Type | Required | Semantic |
|---|---|---|---|
| `jurisdictions` | string array | YES (may be empty) | ISO country / region codes that apply. |
| `mandatories` | string array | YES (may be empty) | Hard compliance items. Validator FLAGs when jurisdictions != [] but mandatories == []. |

### `target_stack`

| Key | Type | Required | Semantic |
|---|---|---|---|
| `framework` | string | YES | E.g. `shadcn+next`, `vanilla-html`, `astro`, `email-mjml`. |
| `css_strategy` | string | advisory (FLAG when empty) | E.g. `tailwind v4`, `css-modules`, `styled-components`. |

### `decisions_log`

An array of objects, append-only. Each entry:

| Key | Type | Required | Semantic |
|---|---|---|---|
| `timestamp` | ISO-8601 string with TZ offset | YES | When the decision was locked. |
| `decision` | string | YES | What was locked. One sentence. |
| `actor` | string | advisory | `user`, `main-agent`, or a sub-agent name. |

## Lifecycle

1. **Phase A discovery (`phase: "phase_a_discovery"`)** — orchestrator opens an empty contract with `meta` + a partial `user_intent`. Required `user_intent` fields are filled as the discovery questions are answered.
2. **Phase A low-fi iteration (`phase: "phase_a_lowfi"`)** — ASCII variants are proposed. `brand_tokens` start filling in. Each user decision appends a row to `decisions_log`.
3. **Phase A lock (`phase: "phase_a_locked"`)** — satisfaction gate passed. All required fields populated. Validator MUST return **PASS** or the orchestrator must elicit the missing data.
4. **Phase B (`phase: "phase_b"`)** — sub-agents read the contract for context. The contract is no longer mutated *as policy*; only `decisions_log` may grow if a sub-agent surfaces a hard constraint that requires user override. If material edits land, orchestrator bumps `meta.updated_at` and re-emits a fresh frozen spec.

## Validator (BLOCK / FLAG / PASS)

The validator lives at `bin/amw-design-contract-validate.py` and implements the design-forge severity model directly.

| Verdict | Exit code | Meaning |
|---|---|---|
| `PASS` | 0 | Contract is clean. Phase B may proceed. |
| `FLAG` | 1 | Required fields are present; one or more advisory fields warrant follow-up. Phase B may proceed but the orchestrator should ask the user about flagged items first. |
| `BLOCK` | 2 | Hard rule violated. Phase B MUST NOT proceed. |

Invocation:

```bash
python3 bin/amw-design-contract-validate.py path/to/contract.json
python3 bin/amw-design-contract-validate.py path/to/contract.json --json
python3 bin/amw-design-contract-validate.py path/to/contract.json --strict-flags
```

Output (`--json`) shape:

```json
{
  "contract": "/abs/path/to/contract.json",
  "verdict": "FLAG",
  "findings": [
    {
      "severity": "FLAG",
      "code": "F030",
      "message": "user_intent.reference_urls is empty — orchestrator should ask for ...",
      "path": "user_intent.reference_urls"
    }
  ]
}
```

BLOCK rules in summary:

- Malformed JSON → `B003`.
- Non-object top-level → `B004`.
- Missing required section → `B010`.
- Wrong section type → `B011`.
- Missing required field in `meta` / `user_intent` / `brand_tokens` / `ia` / `legal` / `target_stack` / `decisions_log` → `B02x`–`B08x`.
- `meta.schema_version` not equal to `1` → `B022`.
- `meta.phase` not in the lifecycle enum → `B023`.
- Hex color invalid → `B041`.
- Color mode invalid → `B042`.
- Border-radius bucket invalid → `B043`.
- `legal.mandatories` includes a cookie banner but `target_stack.framework` is an email stack → `B090`.

FLAG rules cover advisory fields (`reference_urls`, `success_metrics`, `neutral_palette`, `preset_fingerprint`, `css_strategy`, empty `decisions_log`, tone/color-mode inconsistencies, jurisdictions without mandatories).

## Storage and versioning

- The contract lives at `<project_root>/.amw-design-contract/contract.json` (gitignored — contains private project data).
- Old versions are archived to `<project_root>/.amw-design-contract/history/<updated_at>.json` when a section is edited. The history folder is also gitignored.
- The `decisions_log` is the canonical history *inside* the live contract; the per-version history files are for forensics when the orchestrator needs to compare a current contract against a previous lock.

These paths mirror design-forge's `.design-forge/contract/current.md` + versioned files but use JSON instead of markdown so the validator can do mechanical checks instead of LLM-based parsing.

## Hard invariants

1. **Schema-version mismatch is BLOCK.** Older / newer orchestrators MUST NOT silently parse incompatible contracts.
2. **`decisions_log` is append-only.** Removing rows is a hard policy violation. Mark superseded decisions inside the row's `decision` text (`"[SUPERSEDED 2026-05-27 — see row N]"`) instead.
3. **The validator is read-only.** It does not write anywhere except stdout/stderr. The orchestrator owns all mutations.
4. **No PyYAML, no requests.** The validator must work in any minimal environment a Phase B agent runs in.
5. **Email stacks cannot host cookie banners.** This is a hard contradiction the validator catches because design-forge's source spec is web-only and the AMW plugin also produces emails — a contract that mixes the two is malformed.

## Cross-references

- **contract-validator.md** — the design-forge upstream source (MIT) this TECH ports (original BLOCK / FLAG / PASS spec; a build-time distillation input, not shipped in the plugin).
- [phase-a-frozen-spec.md](../../amw-design-principles/references/phase-a-frozen-spec.md) — the single-run, immutable counterpart of this contract.
- [agent-interaction-patterns.md](../../amw-design-principles/references/agent-interaction-patterns.md) — how the contract flows from main-agent to sub-agents.
- [authority-hierarchy.md](../../amw-design-principles/references/authority-hierarchy.md) — who can veto a contract decision (`amw-legal-expert-agent`, `amw-accessibility-auditor-agent`).
- [sub-agent-return-contract.md](../../amw-design-principles/references/sub-agent-return-contract.md) — the YAML header shape sub-agents return; the contract is the *input* counterpart of that *output*.
- `bin/amw-design-contract-validate.py` — the validator implementation.
- `tests/test_amw_design_contract_validate.py` — the validator's test suite.
- `tests/fixtures/contract-{pass,flag,block}.json` — reference contracts for each verdict.
