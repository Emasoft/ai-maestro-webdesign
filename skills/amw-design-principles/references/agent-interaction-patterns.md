## Table of Contents

- [Topology invariants](#topology-invariants)
- [Phase A data flow](#phase-a-data-flow)
- [Phase B data flow](#phase-b-data-flow)
- [What main-agent does between sub-agent calls](#what-main-agent-does-between-sub-agent-calls)
- [Error propagation](#error-propagation)
- [Why this topology (instead of peer-to-peer)](#why-this-topology-instead-of-peer-to-peer)
- [Enforcement](#enforcement)

# Agent interaction patterns — data hand-offs across the 13-agent roster

This document specifies who talks to whom, when, and what data flows between them. It exists because an agent roster without explicit data-flow documentation forces main-agent to re-pass, re-fetch, or silently drop information between sub-agent calls.

## Topology invariants

The agent graph is a one-way tree rooted at main-agent. These invariants hold unconditionally:

1. **Only main-agent talks to the user.** Sub-agents never emit user-facing dialog. All user clarification requests route through main-agent.
2. **Sub-agents never call each other directly.** If `amw-brand-researcher-agent` produces a token set that `amw-wireframe-builder-agent` needs, main-agent is the one who reads the token set from brand-researcher's output and passes it into wireframe-builder's input contract. There is no peer-to-peer sub-agent channel.
3. **Main-agent spawns sub-agents; sub-agents return to main-agent.** Sub-agents may spawn `Task(subagent_type="general-purpose", ...)` calls for bounded internal work, but the spawned Task is not a sibling sub-agent and does not appear in the agent roster.
4. **Sub-agents are stateless across invocations.** A second call to `amw-legal-expert-agent` in the same session does not have memory of the first call. Main-agent is responsible for carrying state forward via input contracts.

## Phase A data flow

Phase A is the interactive discovery and low-fi iteration phase. Main-agent spawns discovery sub-agents as needed (not speculatively). The graph:

```
                          user
                           │
                           ▼
            ┌────── main-agent ──────┐
            │          │             │
            │   (spawn on demand)    │
            │          │             │
   ┌────────┼──────────┼─────────────┼──────────┐
   ▼        ▼          ▼             ▼          ▼
amw-brand  amw-user   amw-legal   amw-seo    amw-multi-
researcher research    expert    strategist  language
          analyst                  (A mode)  copywriter
```

Each discovery sub-agent returns a YAML-headed report. Main-agent aggregates the outputs and synthesizes three ASCII variants via the `ascii-sketch` skill (or equivalent low-fi artifact per the Phase A palette). User iterates; main-agent re-synthesizes. Satisfaction gate terminates Phase A.

**Important: as of P1-1, Phase B data hand-offs are mediated through `phase-a-frozen-spec.json` (canonical schema at [phase-a-frozen-spec](./phase-a-frozen-spec.md)).** The tables below document which Phase A agent's output ends up in which spec field; main-agent runs `bin/amw-freeze-phase-a.sh` at Phase A.5 to aggregate them, and every Phase B sub-agent receives only the spec's path (not the individual paths). The individual-path columns below are kept for reference / future plan changes, but in production every Phase B sub-agent reads the JSON and resolves only the keys it needs.
> [phase-a-frozen-spec.md] Schema · Producers · Consumers · Mutability · Path conventions · Worked example · Cross-references

The "Frozen-spec key" column applies to Phase A → Phase B carries (the rows whose downstream consumer is a Phase B agent). Phase A → Phase A carries (rows where one discovery agent feeds another within Phase A) bypass the frozen spec — main-agent passes those directly because the frozen spec is not yet emitted.

### Phase A data hand-offs (carried by main-agent between sub-agent invocations)

| From agent | Output field | To agent | Input field | When |
|---|---|---|---|---|
| brand-researcher | `competitor_urls` list | seo-strategist (A mode) | `competitor_urls` | seo-strategist runs after brand-researcher, uses competitor URLs for gap analysis |
| brand-researcher | `extracted_tokens` | main-agent | brand context for ASCII variant synthesis | brand-researcher feeds the synthesis step |
| user-research-analyst | `personas` | seo-strategist (A mode) | `audience_notes` | SEO keyword selection uses persona intent |
| user-research-analyst | `design_implications` | main-agent | IA structure for ASCII variants | e.g., "hero CTA above-fold on mobile" |
| legal-expert | `mandatory_elements` | main-agent | elements to include in every Phase A variant | cookie banner, disclaimers, age gate |
| seo-strategist (A) | `recommended_page_structure` | main-agent | H1/H2 seed for ASCII variants | IA backbone |
| multilanguage-copywriter | (Phase A only if variant-level copy needed) | main-agent | headline drafts | copywriter is usually Phase B, but can do Phase A headline drafts for locale-sensitive pages |

Main-agent is free to skip sub-agents when their domain is not in scope. A single-locale English-only site with no regulatory complexity may skip legal-expert and copywriter entirely.

## Phase B data flow

Phase B begins only after the satisfaction-gate token is emitted. Main-agent stops talking to the user, emits a short "building now" transition message, and fans out to production agents + Phase B auditors. The graph:

```
         main-agent (post-gate)
                │
      ┌─────────┼──────────────────┐
      │         │                  │
 ┌────┴────┐    │             ┌────┴─────┐
 │         │    │             │          │
 ▼         ▼    ▼             ▼          ▼
wireframe- diagram- infographic- asset-    video-
builder    producer builder      generator producer
      │         │       │         │         │
      └─────────┴───────┴─────────┴─────────┘
                      │
                      ▼
         ┌────── main-agent ──────┐
         │                        │
         ▼                        ▼
  amw-accessibility-     amw-seo-strategist
  auditor (B mode)       (B mode)
         │                        │
         └────────┬───────────────┘
                  ▼
         amw-browser-tester
                  │
                  ▼
            main-agent
                  │
                  ▼
   reports/webdesigner/<ts>-*.md
                  │
                  ▼
                user
```

### Phase B data hand-offs

The `Frozen-spec key` column shows which `phase-a-frozen-spec.json` field carries the data. Inputs sourced from earlier Phase B sub-agents (e.g. `wireframe-builder`'s `artifact_path`) are NOT in the frozen spec — main-agent threads those directly via the running artifact inventory because they are produced after Phase A.5.

| From agent | Output field | To agent | Input field | Frozen-spec key | Purpose |
|---|---|---|---|---|---|
| brand-researcher (from Phase A) | `extracted_tokens` | wireframe-builder | `brand_tokens` | `brand_tokens_path` | apply color / font / spacing in HTML output |
| user-research-analyst (from Phase A) | `IA_structure` | wireframe-builder | `section_order` | `ia_structure_path` | respect section hierarchy in HTML |
| multilanguage-copywriter (Phase B) | `copy_blocks_per_locale` | wireframe-builder | `copy_content` | `copy_blocks_path` | inject final copy into HTML slots |
| seo-strategist (Phase A) | `H1_H2_structure` | wireframe-builder | `heading_text` | `ia_structure_path` (H1/H2 seed) + `seo_head_path` (head fragments) | locked headings |
| legal-expert | `mandatory_elements` | wireframe-builder | `required_fragments` | `legal_mandatory_elements_path` | cookie banner, disclaimers must be present |
| design-md author/extractor (Phase A) | `DESIGN.md` | wireframe-builder, accessibility-auditor (B), component-library-architect | `design_md_path` | `design_md_path` | canonical token + section reference |
| user-research-analyst (Phase A) | `personas` | wireframe-builder, copywriter, form-designer | `personas` (microcopy / empty-state tuning) | `personas_path` | persona-driven content choices |
| (Phase A approved ASCII) | the approved variant | wireframe-builder | `approved_ascii` (layout source-of-truth) | `approved_ascii_path` + `approved_ascii_sha256` | wireframe-builder validates checksum then translates to HTML |
| (Phase A target / locales / wcag) | run-level config | every Phase B sub-agent | `target_stack`, `locales`, `wcag_target`, `output_dir` | `target_stack`, `locales`, `wcag_target`, `output_dir` | implementation target + accessibility level + output path |
| wireframe-builder | `artifact_path` (the final HTML) | accessibility-auditor (B) | `artifact_url` (file://…) | (not in spec — running artifact inventory) | audit target |
| wireframe-builder | `artifact_path` | seo-strategist (B) | `artifact_url` | (not in spec) | on-page SEO audit target |
| wireframe-builder | `artifact_path` | browser-tester | `artifact_url` + `scenarios` | (not in spec) | dev-browser scenario tests |
| diagram-producer | `artifact_paths` (SVG/PNG/Mermaid) | wireframe-builder | `embedded_diagrams` | (not in spec) | if diagrams are embedded in the HTML page |
| infographic-builder | `artifact_path` | accessibility-auditor (B) | `artifact_url` | (not in spec) | separate infographic page audit |
| video-producer | `artifact_path` (MP4) | main-agent | final report only | (not in spec) | videos don't need accessibility audit beyond closed captions handled by video-producer itself |
| asset-generator | `artifact_paths` (SVG icons/logos) | wireframe-builder | `asset_library` | (not in spec) | embed or link from HTML |
| **form-designer** (Tier 4) | `form_spec` (HTML structure + validation rules + error-state copy slots) | wireframe-builder | `form_blocks` | (not in spec — produced in Phase B) | wireframe-builder renders the layout; form-designer owns the form architecture |
| **motion-designer** (Tier 4) | `motion_spec` (CSS @keyframes / JS snippets + timing + reduced-motion guards) | wireframe-builder | `motion_blocks` | (not in spec — produced in Phase B) | wireframe-builder embeds the spec; motion-designer owns the animation semantics |
| **component-library-architect** (Tier 4) | `tokens.json` / `tailwind.config.ts` / `design-tokens.yaml` | wireframe-builder (Phase B) | `brand_tokens` | `brand_tokens_path` (when architect's output replaces brand-researcher's) | architect produces canonical token export; consumer agents read from it |
| **email-designer** (Tier 4) | `mjml_source` + `plain_text_fallback` + `dark_mode_variant` | main-agent | final report (separate render path — NOT routed to wireframe-builder) | (consumes spec; emits independent artifact) | email is a different artifact class; main-agent collects directly |
| brand-researcher | `extracted_tokens` (Phase A) | component-library-architect (Phase B if requested) | `brand_tokens_seed` | `brand_tokens_path` | architect derives a full token system from the seed |
| user-research-analyst | `personas + onboarding_flow` | wireframe-builder | `IA_structure` + `empty_state_specs` | `personas_path` + `ia_structure_path` | wireframe-builder embeds the empty-state guidance the analyst flagged |
| multilanguage-copywriter | `microcopy_per_context` | wireframe-builder | injected into form / button / toast / empty-state slots | `copy_blocks_path` | microcopy specialist work is part of copywriter, not a separate agent |

### Phase B sequencing rules

Production agents (wireframe-builder, diagram-producer, etc.) can run in parallel if their outputs are independent. Auditors (accessibility, SEO-B, browser-tester) run **after** the production agents they audit, never in parallel with them (you cannot audit an artifact that doesn't exist yet).

**Tier 4 specialists** typically run BEFORE the producer that consumes their output:
- `form-designer` runs before `wireframe-builder` when the artifact contains forms
- `motion-designer` runs before `wireframe-builder` when motion specs are required
- `component-library-architect` runs before `wireframe-builder` when tokens need authoring (rather than just consuming brand-researcher's extracted tokens)
- `email-designer` runs independently (separate render path, not piped into wireframe-builder)

Dependency chains main-agent must respect:

1. `wireframe-builder` → must complete before `accessibility-auditor (B)`, `seo-strategist (B)`, `browser-tester`
2. `diagram-producer` → must complete before `wireframe-builder` if diagrams are embedded in the HTML; otherwise may run in parallel
3. `asset-generator` → must complete before `wireframe-builder` if assets are embedded; otherwise parallel
4. `video-producer` → independent of wireframe-builder; may run in parallel
5. **Tier 4 specialists** (form-designer / motion-designer / component-library-architect) → must complete before `wireframe-builder` consumes them; `email-designer` is independent
6. **Specialist activation is on-demand** — main-agent only spawns Tier 4 if the artifact mix calls for the specialty (no forms = no form-designer, no motion = no motion-designer)

Main-agent's orchestration doctrine (§15 of main-agent spec) captures the exact spawn sequence.

## What main-agent does between sub-agent calls

For every sub-agent invocation, main-agent's steps are:

1. **Prepare the input** — for Phase A invocations, take relevant fields from prior sub-agents' YAML headers + report bodies. For Phase B invocations, the input contract is a single `frozen_spec_path` (per Phase A.5; see [phase-a-frozen-spec](./phase-a-frozen-spec.md)) plus any artifact paths produced by upstream Phase B sub-agents
  > Schema · Field reference · Producers · Consumers · Mutability · Path conventions · Worked example · Cross-references
2. **Spawn the sub-agent** via Task(subagent_type=<agent-name>, prompt=<input>)
3. **Parse the YAML header** — check `status`, `blocking_issues`, `next_action`
4. **Decide** — proceed / retry / escalate / stop (per the return-contract consumption pseudo-code)
5. **Record** — add the artifact paths to the running artifact inventory for the final job-completion report
6. **Aggregate** — merge any warnings into the running warning list; merge any recommendations into the running recommendations list

Main-agent does NOT re-read the full sub-agent report unless the summary in the YAML header + 2-3-sentence opener is insufficient for the next step. This is how context is preserved. The frozen spec (Phase A.5) is what makes Phase B input preparation O(1) instead of O(N) sub-agents — main-agent prepares the spec once, then every Phase B input contract is just one path.

## Error propagation

If a sub-agent returns `status=failed` or `next_action=escalate_to_user`:

- **Failure in a production agent** → main-agent stops the affected work stream, does not invoke its downstream auditors, carries the failure forward into the final job-completion report. Other parallel work streams continue if independent.
- **Failure in a discovery agent (Phase A)** → main-agent decides between (a) skip the domain and proceed with degraded context, (b) ask user for help, (c) retry with adjusted input. The decision is guided by the agent's `recommendations`.
- **Failure in an auditor (Phase B)** → main-agent flags but does not stop. The auditor's domain is reported as "unaudited" in the final job-completion report with the reason.

Veto-power failures (legal-expert, accessibility-auditor) are treated specially per [authority-hierarchy](authority-hierarchy.md) — they block forward progress on the affected work stream until user override or resolution.
> [authority-hierarchy.md] Domains and authority · Veto power — what it means · Resolution rules by conflict pattern · How main-agent applies the hierarchy · What the hierarchy does NOT do · Enforcement

## Why this topology (instead of peer-to-peer)

A tree topology is chosen over a mesh for three reasons:

1. **Debuggability.** Main-agent is the single source of truth for what happened. Logs are linear.
2. **Context isolation.** Each sub-agent sees only its own input + shared references. Cross-domain contamination (brand-researcher's aesthetic preferences leaking into legal-expert's compliance reasoning) is structurally prevented.
3. **Loop safety.** A mesh topology with sub-agents calling each other creates potential for circular dependencies (A calls B, B calls C, C calls A). A tree cannot.

The cost is that main-agent carries the data-plumbing burden: reading output from N sub-agents and assembling M input contracts. The benefit is that the entire workflow is inspectable and the agents themselves remain simple, single-purpose. Phase A.5 ([phase-a-frozen-spec](./phase-a-frozen-spec.md)) reduces the data-plumbing cost for the Phase A → Phase B hand-off from O(N) per-agent contracts to O(1) — one frozen JSON, N agents read it.

## Enforcement

- Every sub-agent spec documents the data it expects as input (§5) and what it produces as output (§13 + body). The cross-references to other agents use this document as the spec-of-specs.
- Main-agent's §15 Orchestration Doctrine cites this document.
- Smoke test: every hand-off in the table above is cross-checked against the sender's output schema and the receiver's input schema.
- Phase B input contracts are defined as `frozen_spec_path` only (per [phase-a-frozen-spec](./phase-a-frozen-spec.md)); any agent's §5 that lists individual paths instead of `frozen_spec_path` is non-compliant with P1-1.
  > Schema · Field reference · Producers · Consumers · Mutability · Path conventions · Worked example · Cross-references
