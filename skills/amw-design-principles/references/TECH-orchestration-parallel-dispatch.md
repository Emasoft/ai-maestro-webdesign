---
name: TECH-orchestration-parallel-dispatch
category: main-agent-references
source: batch9 T-162 (clean-room from orchestration patterns; general design knowledge — no specific source attribution)
also-in: agent-interaction-patterns.md (Phase B sequencing rules); this doc tightens the parallel-vs-sequential decision
---

# Orchestration — parallel vs sequential dispatch

## Table of Contents

- [What it does](#what-it-does)
- [When this is relevant](#when-this-is-relevant)
- [The dispatch decision](#the-dispatch-decision)
- [Three-question algorithm](#three-question-algorithm)
- [Parallel-eligible patterns](#parallel-eligible-patterns)
- [Sequential-required patterns](#sequential-required-patterns)
- [Worked example — good case](#worked-example-good-case)
- [Worked example — bad case](#worked-example-bad-case)
- [Concurrency budget](#concurrency-budget)
- [Failure handling in parallel batches](#failure-handling-in-parallel-batches)
- [What this protocol does NOT do](#what-this-protocol-does-not-do)
- [Cross-references](#cross-references)

## What it does

Defines when main-agent dispatches sub-agents in **parallel** (one Task call per agent, all spawned in a single message, results collected together) versus **sequentially** (one Task call, wait for output, prepare next input from previous output, then spawn the next Task call).

The wrong dispatch choice has two cost classes:

- **Parallel when sequential was required** — sub-agent B runs without sub-agent A's output, produces work against stale or guessed inputs, and either fails outright or produces output that has to be discarded and re-run after A finishes. Net cost: 2× sub-agent runs, 2× sub-agent tokens, plus the wasted main-agent context that held the bad output.
- **Sequential when parallel was eligible** — main-agent serializes independent work, doubling or tripling wall-clock time on a multi-agent batch. The user waits 4× longer for an answer that could have arrived in one round.

The default bias is **parallel-first**: main-agent looks for reasons to serialize, and absent a reason, dispatches in parallel.

## When this is relevant

Whenever main-agent is about to spawn two or more sub-agents in a Phase A or Phase B fan-out. Specifically:

- **Phase A discovery fan-outs** — brand-researcher + legal-expert + seo-strategist on a new brief.
- **Phase B production fan-outs** — wireframe-builder + diagram-producer + asset-generator after the satisfaction gate.
- **Phase B audit fan-outs** — accessibility-auditor + seo-strategist (B mode) + browser-tester after wireframe-builder completes.
- **Tier 4 specialist activations** — form-designer + motion-designer when both are needed for the same artifact.

Not relevant when:

- Only one sub-agent is involved (no parallelism decision to make).
- The work is happening inside a single sub-agent's body (the sub-agent itself may parallelize internal Task calls; that is its concern, not main-agent's).

## The dispatch decision

The decision is binary at each dispatch step: **parallel** or **sequential**. There is no partial-parallel: either all the candidate sub-agents in a step go out in one batch, or they go out one at a time.

Two definitions:

- **Independent domains** — the sub-agents read disjoint slices of the available inputs and produce outputs that do not feed each other within the current step. Example: legal-expert reads `jurisdiction + business_type + processed_data_categories`; accessibility-auditor reads `wcag_target + locale`; SEO-strategist reads `target_keywords + competitor_urls`. None of the three needs another's output to function. → parallel.
- **Dependent chain** — the sub-agents form a producer/consumer chain where the downstream agent's input contract includes a field that the upstream agent emits. Example: design-md-extractor produces `design_md_path`; design-md-author consumes `design_md_path` to lint and refine; design-md-auditor consumes the refined output. → sequential.

The cleanest test: write each sub-agent's input contract and check whether any field of agent B requires an artifact path or value emitted by agent A in the same step. If yes → sequential. If no → parallel.

## Three-question algorithm

For each pair (A, B) of candidate sub-agents in a dispatch step, main-agent asks:

1. **Does B's input contract include a field produced by A in this step?**
   - Yes → B is sequential after A.
   - No → continue.
2. **Does A's output transformation change the user-facing direction such that B's work would be premature?** (E.g., a Phase A.5 frozen spec re-emission cancels in-flight Phase B work — see `phase-a-frozen-spec.md`.)
   - Yes → B is sequential after A.
   - No → continue.
3. **Is A a veto-holder whose blocking_issues, if present, would invalidate B's work?**
   - Yes — and the veto domain plausibly affects B → sequential (run A first, only dispatch B if A's veto is clear).
   - Yes — but A's veto is in a domain unrelated to B → parallel.
   - No → parallel.

If all three answers are "no", A and B are independent → parallel. If any answer is "yes", they are dependent → sequential, with A first.

Generalized to N agents: build a dependency graph by running the algorithm on every pair. The graph's transitive closure tells main-agent the dispatch waves: agents with no incoming edges go in wave 1 (parallel), agents with incoming edges only from wave-1 agents go in wave 2 (parallel within wave 2, after wave 1), and so on.

## Parallel-eligible patterns

These dispatch shapes are SAFE to parallelize. Main-agent's default bias is to use them.

**Phase A discovery (canonical parallel fan-out):**
- `amw-brand-researcher-agent` reads competitor URLs.
- `amw-legal-expert-agent` reads jurisdiction + business_type.
- `amw-seo-strategist-agent` (A mode) reads target keywords + competitor URLs.
- `amw-user-research-analyst-agent` reads interview notes + personas.
- All four have disjoint input slices. → dispatch in parallel; main-agent aggregates their YAML headers when all four return.

**Phase B production (canonical parallel fan-out, after Phase A.5):**
- `amw-asset-generator-agent` reads `frozen_spec_path` (uses brand_tokens and target_stack only).
- `amw-diagram-producer-agent` reads `frozen_spec_path` (uses approved_ascii_path's diagram regions only).
- `amw-video-producer-agent` reads `frozen_spec_path` and an HTML scene path (uses target_stack and locales only).
- All three produce independent artifacts. → dispatch in parallel.

**Phase B audit (canonical parallel fan-out, after wireframe-builder completes):**
- `amw-accessibility-auditor-agent` audits the produced HTML artifact_path.
- `amw-seo-strategist-agent` (B mode) audits the same HTML for on-page SEO.
- `amw-browser-tester-agent` runs scenario tests against the same HTML.
- All three read the same wireframe-builder output but do not feed each other. → dispatch in parallel after wireframe-builder returns.

**Tier 4 specialists pre-production (parallel within wave):**
- `amw-form-designer-agent` produces a form spec.
- `amw-motion-designer-agent` produces a motion spec.
- `amw-component-library-architect-agent` produces tokens.
- All three feed wireframe-builder, but they do not feed each other. → dispatch in parallel; wireframe-builder waits for all three before running.

## Sequential-required patterns

These dispatch shapes are SAFE only when run in order. Main-agent must serialize.

**Design-md extractor → author → auditor:**
- Extractor produces a candidate `DESIGN.md` from a URL / Tailwind config / codebase.
- Author refines it (lint pass + WCAG contrast pre-flight + 5-Q gap closure).
- Auditor performs the 5-pass review of the refined output.
- Each agent's input is the previous agent's output. → strict sequence; no parallelism possible.

**Phase B production → audit:**
- Wireframe-builder produces `artifact_path` (the rendered HTML).
- Accessibility-auditor / seo-strategist (B) / browser-tester all read that path.
- The auditors literally cannot run before the artifact exists. → wireframe-builder strictly precedes the audit wave.

**Tier 4 specialist → wireframe-builder:**
- Form-designer / motion-designer / component-library-architect emit specs that wireframe-builder embeds.
- Wireframe-builder cannot embed a spec that has not been emitted yet. → Tier 4 strictly precedes wireframe-builder.

**Iterative re-extraction → re-author:**
- When user re-iterates Phase A (changes a requirement after Phase B has partially run), main-agent re-emits the frozen spec and re-fans out Phase B. In-flight Phase B Task calls must be cancelled before the re-fan-out. → sequential with explicit cancellation step between the iterations.

## Worked example — good case

**Scenario:** New brief — "Build me a SaaS dashboard for HR teams, GDPR-compliant, English + German locales, WCAG-AA target, shadcn+next stack." User provides three competitor URLs and a one-page persona sketch.

**Main-agent's dispatch waves:**

```
WAVE 1 (parallel — independent discovery domains):
├── amw-brand-researcher-agent ← reads competitor URLs
├── amw-legal-expert-agent ← reads jurisdiction=EU + business_type=SaaS + data_categories=HR
├── amw-seo-strategist-agent (A mode) ← reads target keywords + competitor URLs
└── amw-user-research-analyst-agent ← reads persona sketch

(all four spawned in one Task batch; main-agent collects all four YAML headers when they return)
                                ↓
WAVE 2 (sequential — copywriter needs personas + brand tone):
└── amw-multilanguage-copywriter-agent ← consumes personas + brand-tone from wave 1

(spawned only after wave 1 returns; uses wave 1 outputs as input)
                                ↓
                       (ASCII iteration, user approval)
                                ↓
                          PHASE A.5 freeze
                                ↓
WAVE 3 (parallel — production agents, independent artifacts):
├── amw-asset-generator-agent ← reads frozen_spec_path
├── amw-diagram-producer-agent ← reads frozen_spec_path (no diagrams in this brief, skipped)
└── (pre-production complete)
                                ↓
WAVE 4 (single — wireframe-builder waits for wave 3 specialists):
└── amw-wireframe-builder-agent ← reads frozen_spec_path + wave 3 outputs
                                ↓
WAVE 5 (parallel — audit, independent reviews of the same artifact):
├── amw-accessibility-auditor-agent ← reads wireframe artifact_path
├── amw-seo-strategist-agent (B mode) ← reads wireframe artifact_path
└── amw-browser-tester-agent ← reads wireframe artifact_path + scenarios

(all three spawned in one Task batch; main-agent collects all three when they return)
```

Five waves total. Three are parallel batches (waves 1, 3, 5). Two are single-agent (waves 2, 4). Total wall-clock time: roughly 5 sub-agent latencies, not 9 (which is what serial dispatch of all 9 would cost).

The user sees a single transition message at each wave boundary ("running discovery on 4 specialists in parallel...", "building artifact...", "auditing on 3 specialists in parallel..."). No mid-wave commentary; main-agent does not narrate per-agent progress within a wave.

## Worked example — bad case

**Scenario (anti-pattern):** Same brief as above. Main-agent decides to run everything sequentially "to be safe".

**Bad-case dispatch:**

```
1. brand-researcher (wait)
2. legal-expert (wait)
3. seo-strategist (wait)
4. user-research-analyst (wait)
5. multilanguage-copywriter (wait)
6. (ASCII iteration)
7. freeze
8. asset-generator (wait)
9. wireframe-builder (wait)
10. accessibility-auditor (wait)
11. seo-strategist B (wait)
12. browser-tester (wait)
```

**Why this is wrong:**

1. **Wall-clock cost.** Steps 1-4 are independent — they could run as one parallel batch. Serializing them quadruples the wait time for nothing.
2. **Token cost.** Main-agent keeps the running brief in context across 4 serial waits in steps 1-4, holding the same context for 4× the duration vs one parallel batch.
3. **User-facing cost.** The user watches "spawning brand-researcher... done. spawning legal-expert... done. spawning seo-strategist... done." — four transition messages where one parallel transition would do.
4. **No technical benefit.** Sequential dispatch is justified ONLY when there is a producer/consumer chain. Steps 1-4 have no such chain. Serializing them is pure waste.

**Correct fix:** Run the three-question algorithm on every pair in steps 1-4. All answers are "no". → parallel batch. Then run on step 5 against steps 1-4 — copywriter's input contract includes personas from user-research-analyst → step 5 is sequential after step 4 (and waits for the wave 1 batch). And so on.

The bad case is fixed by NOT defaulting to "sequential to be safe". Main-agent's bias is parallel-first; sequential is the justified exception, not the default.

## Concurrency budget

There is a soft cap on how many sub-agents main-agent dispatches in a single parallel batch. The cap exists because:

1. The host Task system has its own concurrency limits; oversubscribing produces queueing rather than true parallelism.
2. Main-agent context accumulates one YAML header per sub-agent return. Twelve-agent batches produce twelve return headers in close succession, which can spike orchestrator context past a useful aggregation window.
3. Tier 1 user-facing latency feels worse when ALL sub-agents fail in the same batch — single-batch failures look like total stalls.

Soft cap: **5 sub-agents per parallel wave**. If a wave would have more than 5, split into sub-waves of 5 in priority order:

- Veto-holders first (legal-expert, accessibility-auditor) — they may block downstream work, so getting their blocking_issues early is valuable.
- Discovery agents that feed Tier 4 specialists next.
- Production agents whose artifacts feed audit agents next.
- Audit agents last.

The cap is soft, not hard. If 6 sub-agents are clearly independent and total wall-clock time matters, dispatch all 6. The cap is a default to prevent reflexive "spawn everything" patterns.

## Failure handling in parallel batches

When 5 sub-agents run in parallel and one returns `status=failed`:

1. The other 4 sub-agents still complete (parallel work is not cancelled mid-flight; the cost was already paid).
2. Main-agent aggregates all 5 returns including the failure.
3. The failure is handled per the failure rules in `agent-interaction-patterns.md` — production failure stops the work stream, discovery failure may be skipped with degraded context, veto failure stops forward progress.
4. The 4 successful returns are NOT discarded just because one peer failed. They are recorded and folded into the running inventory.

The exception: when the failed sub-agent's output was a hard prerequisite for a NEXT wave. In that case main-agent does not dispatch the next wave until the failure is resolved (re-spawn the failed agent with corrected input, or escalate to user).

## What this protocol does NOT do

- It does not parallelize sub-agents that share state. The plugin's sub-agents are stateless across invocations, so this is rarely a concern, but if a future sub-agent introduces shared mutable state (e.g., a shared lock file), main-agent must serialize accesses regardless of independence in the input contract.
- It does not parallelize Tier 1 user-facing dialog. There is exactly one main-agent talking to the user; that is the topology invariant. Parallel sub-agent dispatch happens silently from the user's perspective.
- It does not parallelize Phase A iteration. The ASCII iteration loop is conversational and serial (user emits feedback → main-agent updates → user emits feedback). Parallel dispatch is for the sub-agent layer below Phase A, not for the Phase A conversation itself.
- It does not retry a failed parallel sub-agent automatically. Retries are governed by `agent-interaction-patterns.md`'s error propagation rules; main-agent decides whether retry is warranted.

## Cross-references

- `references/agent-interaction-patterns.md` — Phase B sequencing rules (the source for the wave structures above).
- `references/phase-a-frozen-spec.md` — the data hand-off mechanism that makes Phase B parallelism cheap (one path, N readers).
- `references/sub-agent-return-contract.md` — what main-agent reads from each returned YAML header to aggregate parallel batches.
- `references/TECH-orchestration-conflict-resolution.md` — what main-agent does when parallel returns conflict.
- `references/TECH-orchestration-checkpoint-protocol.md` — when a parallel-batch return triggers a user check-in.
- `agents/ai-maestro-webdesign-main-agent.md` §15 Orchestration Doctrine — the binding consumer of this dispatch protocol.
