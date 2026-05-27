---
name: TECH-orchestration-checkpoint-protocol
category: main-agent-references
source: batch9 T-163 (clean-room from orchestration patterns; general design knowledge — no specific source attribution)
also-in: two-mode-workflow.md (Phase A satisfaction gate); this doc covers mid-Phase-B checkpoints
---

# Orchestration — mid-Phase-B checkpoint protocol

## Table of Contents

- [What it does](#what-it-does)
- [When this is relevant](#when-this-is-relevant)
- [Checkpoint vs satisfaction gate](#checkpoint-vs-satisfaction-gate)
- [The four mandatory checkpoint triggers](#the-four-mandatory-checkpoint-triggers)
- [Checkpoint message format](#checkpoint-message-format)
- [Decision tree for checkpoint decisions](#decision-tree-for-checkpoint-decisions)
- [Worked example — good case](#worked-example-good-case)
- [Worked example — bad case](#worked-example-bad-case)
- [Recording the checkpoint](#recording-the-checkpoint)
- [What this protocol does NOT do](#what-this-protocol-does-not-do)
- [Cross-references](#cross-references)

## What it does

Defines when, during Phase B execution, main-agent **must pause and check in with the user** versus when it can **keep running** until Phase B completion. Phase B is the build phase: it runs after the Phase A satisfaction gate, fans sub-agents out per the parallel-dispatch rules, and assembles the final job-completion report. The user has approved the direction; mid-Phase-B is not for re-litigating Phase A choices.

But Phase B is not a sealed pipeline. Four classes of event can occur mid-flight that require the user to make a decision main-agent cannot make alone. The checkpoint protocol identifies those classes precisely, prescribes the format of the check-in, and prevents the two failure modes:

- **Under-checkpointing** — main-agent keeps running past a veto, ships a defective artifact, surfaces the issue only in the final report when it is too late for the user to redirect cheaply.
- **Over-checkpointing** — main-agent pauses for every minor warning, fragmenting the build into a stop-start dialogue that defeats the purpose of Phase A approval.

The default is **keep running**. Checkpoints fire only on the four explicit triggers.

## When this is relevant

Phase B is between the satisfaction-gate token and the final job-completion report. Specifically:

- After main-agent runs `bin/amw-freeze-phase-a.sh` and produces `phase-a-frozen-spec.json`.
- During Phase B production fan-out (wireframe-builder, diagram-producer, asset-generator, video-producer).
- During Phase B audit fan-out (accessibility-auditor B, seo-strategist B, browser-tester).
- During Tier 4 specialist work (form-designer, motion-designer, component-library-architect, email-designer).
- During post-audit legal-compliance verification (legal-expert in B mode).

Not relevant during Phase A (Phase A is conversational by definition; "checkpoints" don't apply — the entire phase is a checkpoint). Not relevant once the final job-completion report is being written (at that point the build is done; the user reviews the report, not a mid-flight checkpoint).

## Checkpoint vs satisfaction gate

These two protocols look similar but apply to different transitions:

| | Satisfaction gate (`two-mode-workflow.md`) | Checkpoint (this doc) |
|---|---|---|
| When it fires | End of Phase A, before Phase B begins | Mid-Phase-B, between sub-agent waves |
| What it checks | "Is the Phase A direction approved?" | "Is this mid-flight event something the user must decide on?" |
| Token list | `yes`, `ship it`, `that's the one`, `perfect`, `done`, `approved`, `go ahead`, `let's do it` | (no fixed tokens; main-agent presents specific options) |
| Default | Block; require an explicit positive token | Keep running; pause only on the four explicit triggers |
| User response | Approves direction or requests another iteration | Resolves a specific mid-flight decision |
| Frequency | Exactly once per project (or once per Phase A re-iteration) | Zero to N times mid-Phase-B (rare; most projects have zero checkpoints) |

A satisfaction gate is the *gate of Phase A*. A checkpoint is the *interruption of Phase B*. They are not interchangeable; phrasing a checkpoint like "is this the direction you wanted?" is wrong (that question was answered at the gate).

## The four mandatory checkpoint triggers

Main-agent MUST pause Phase B and surface the event to the user when any of these four triggers fires. Outside of these triggers, main-agent keeps running until Phase B completion.

### Trigger 1 — Veto fired

A veto-holder sub-agent (`amw-legal-expert-agent`, `amw-accessibility-auditor-agent`) returns `blocking_issues` in its veto domain. The veto cannot be resolved by re-spawning the agent with adjusted input from main-agent alone; it requires either:

- A user-accepted-risk override ("ship without the cookie banner, I'll handle consent externally").
- A direction change ("we'll redesign the form to avoid the contrast issue").
- A drop ("skip the testimonial section, it was non-essential").

Main-agent cannot pick any of these three options unilaterally. → checkpoint required.

### Trigger 2 — Sub-agent reports BLOCK

A non-veto sub-agent returns `status=failed` AND `next_action=escalate_to_user` AND its blocking issue is not resolvable by retry with adjusted input. The "escalate_to_user" flag in the return contract is the explicit signal: the agent could not produce useful output and the cause is something only the user can answer.

Examples of escalate_to_user blocks:

- Brand-researcher: "the three competitor URLs you provided are 404 / behind auth / paywalled — need usable URLs to extract tokens."
- Wireframe-builder: "the approved ASCII references a `<chart>` block but no diagram-producer artifact was provided and no diagram source is present in the input contract — clarify whether the chart should be omitted, mocked, or have its source supplied."
- Multilanguage-copywriter: "the brief lists French (Switzerland) locale but the brand voice file is single-locale French (France); these have different formal-register conventions — pick one or supply both."

→ checkpoint required.

### Trigger 3 — Budget threshold breached

Mid-flight, the running scope of changes has grown beyond what the user approved at the satisfaction gate. The threshold: **>20% of the original Phase A direction has changed** (measured by approved artifact sections, locales, target stack, or required mandatory elements).

Concrete thresholds:

- More than 1 new top-level section has been added that was not in the approved ASCII (5-section approved page now has 7+ sections).
- A new locale has been requested mid-flight (English-only project gained French requirement post-gate).
- The target stack has flipped (shadcn+next → vanilla HTML, or vice versa).
- New mandatory legal elements were introduced (project gained EU users post-gate, GDPR now applies).
- A new sub-agent class is being invoked that was not in the original Phase B fan-out plan (e.g., motion-designer wasn't on the plan but a mid-flight requirement now needs animation).

→ checkpoint required.

### Trigger 4 — Unrecoverable error

A sub-agent or build step has failed in a way that retry alone cannot fix and the failure is not classifiable as Trigger 2 (escalate_to_user). Examples:

- `bin/amw-validate-ascii.py` exits non-zero on the approved ASCII because the file got truncated on disk after Phase A approval.
- A required tool dependency (Playwright, `dev-browser` CLI, `npx mmdc`) is missing from the runtime environment and `/amw-init` has not been run.
- A frozen-spec field references a path that no longer exists on disk (file was moved or deleted).
- Two sub-agents in the same wave both return `status=failed` with conflicting recovery advice.

These cannot be resolved by main-agent re-trying the same step; they require external intervention. → checkpoint required.

## Checkpoint message format

The check-in message uses a fixed three-part structure. The structure exists to make checkpoints scannable: the user sees what happened, what their options are, and what main-agent will do absent a response, in three short blocks.

```
WHAT HAPPENED
<one-sentence factual description of the trigger event. Cite the sub-agent
that raised it and the specific blocking_issue or threshold breached.>

OPTIONS
1. <concrete option A — what main-agent will do, with the cost / consequence in one phrase>
2. <concrete option B — same shape>
3. <concrete option C, if applicable — same shape>

DEFAULT IF NO RESPONSE
<which option main-agent will pick if the user does not respond in this round. May be "stop and wait" — silence is not interpreted as approval to proceed past a veto.>
```

Three structural rules:

1. **No more than 4 options.** If the decision has 5+ branches, main-agent has not done enough framing — refine until at most 4 options remain.
2. **Every option is concrete.** "Discuss accessibility further" is not an option. "Re-design the hero with a darker primary that meets 4.5:1 contrast" is.
3. **The default is conservative.** For veto triggers (1 and 4-when-fatal), the default is "stop and wait". For non-fatal triggers (2 and 3 and 4-when-recoverable), the default may be a specific safe option, but it MUST be labeled so the user knows what main-agent does if they say nothing.

The three-part shape is the contract. Variations on wording are fine; variations on structure (e.g. burying the options in prose) are not.

## Decision tree for checkpoint decisions

```
sub-agent return arrives in main-agent
            │
            ▼
   is this a veto-holder
   returning blocking_issues
   in its veto domain?
            │
   ┌────────┴────────┐
  YES                NO
   │                  │
   ▼                  ▼
TRIGGER 1     does the return have
checkpoint    status=failed AND
              next_action=escalate_to_user?
                      │
              ┌───────┴───────┐
             YES              NO
              │                │
              ▼                ▼
        TRIGGER 2      has Phase B scope grown
        checkpoint     >20% beyond the Phase A
                       approved direction?
                              │
                      ┌───────┴───────┐
                     YES              NO
                      │                │
                      ▼                ▼
              TRIGGER 3        is the return a
              checkpoint       failure that retry
                               with adjusted input
                               cannot fix?
                                      │
                              ┌───────┴───────┐
                             YES              NO
                              │                │
                              ▼                ▼
                      TRIGGER 4         no checkpoint
                      checkpoint        keep running
```

The tree is short on purpose. Most sub-agent returns produce "keep running" (the rightmost leaf). Checkpoints are the exception.

## Worked example — good case

**Scenario:** SaaS dashboard build. After the Phase A satisfaction gate, main-agent runs Phase B. Wireframe-builder completes. Accessibility-auditor (B mode) runs against the produced HTML and returns:

```yaml
status: failed
confidence: high
blocking_issues:
  - "contrast 3.4:1 on primary CTA button text (white on #2EC4B6) — fails WCAG-AA for body-size button text (requires 4.5:1)"
  - "focus indicator on form inputs missing — fails WCAG 2.4.7"
next_action: escalate_to_user
```

**Main-agent's checkpoint message:**

```
WHAT HAPPENED
The accessibility audit returned 2 WCAG-AA hard blockers on the dashboard build:
(a) primary CTA contrast is 3.4:1 against required 4.5:1; (b) form-input focus
indicators are missing per WCAG 2.4.7.

OPTIONS
1. Re-author the affected components — darken the CTA primary to #1F8F86 and add
   `focus:ring-2 focus:ring-offset-2` to inputs. Adds ~1 sub-agent round.
2. Ship as-is with the audit failures recorded as known-issues in the final report.
   User-accepted risk; the dashboard will fail an independent WCAG audit.
3. Drop the CTA button styling and the dedicated form rows from this build, defer
   to a v2 once design tokens are reconciled. Smaller artifact, no audit failures.

DEFAULT IF NO RESPONSE
Stop and wait — these are veto-holder hard blockers; main-agent does not proceed
past them without explicit user direction.
```

**Why this is good:**

- The trigger fired correctly (Trigger 1 — veto-holder returned blocking_issues).
- The user sees the specific WCAG rules that failed, not "accessibility problems".
- The three options are concrete and span the realistic action space (fix, override, drop).
- The default is "stop and wait" because Trigger 1 is veto-class.
- Main-agent does NOT silently pick option 1 to "speed things up". The user explicitly authorizes the fix.

**User reply:** "Do option 1, and add the focus ring to buttons too while you're there."

**Main-agent's next step:** Spawn the re-author wave (Tier 4 component-library-architect updates the token to `#1F8F86`, wireframe-builder re-renders with the new token + focus rings on buttons), re-run accessibility-auditor. No second checkpoint unless a new trigger fires.

## Worked example — bad case

**Scenario (anti-pattern):** Same dashboard build. Accessibility-auditor returns the same two blocking_issues.

**Bad-case main-agent behavior:** Main-agent notices the failures, mentally classifies them as "I can fix this on my own", and silently dispatches a re-author wave that adjusts the CTA color and adds focus rings, then continues to seo-strategist (B) audit and browser-tester audit. The final job-completion report mentions both fixes in passing under "decisions arbitrated".

**Why this is wrong:**

1. **Trigger 1 was bypassed.** Veto-holder returned blocking_issues; checkpoint was mandatory. Main-agent skipped it.
2. **The user lost the option to choose.** Option 2 (ship as-is) and option 3 (drop the affected sections) were never offered. Maybe the user actually wanted option 3 because the dashboard is for an internal MVP and they don't care about accessibility for v1.
3. **The mid-flight re-author is silent work.** The user's running mental model of "what is main-agent doing" is wrong — they think the build is on track, but main-agent has actually pivoted to a fix wave. If the fix wave fails, the user is even further behind their expectation.
4. **The decisions-arbitrated entry in the final report is too late.** The user discovers the change after the build is already shipped. They cannot redirect.

**Correct fix:** Apply Trigger 1. Pause. Send the checkpoint message. Wait for user direction.

The bad case shows the failure mode the protocol exists to prevent: main-agent's bias to "keep things moving" can silently override user agency. The checkpoint is the explicit pause that returns agency.

## Recording the checkpoint

Every checkpoint produces a structured entry in the final job-completion report under a `### Checkpoints` section:

```markdown
### Checkpoint <N> — <trigger class>
- **What happened:** <one-sentence factual description>
- **Triggered by:** <sub-agent name + the specific return field that fired the trigger>
- **Options surfaced:** <list of the options main-agent presented>
- **User response:** <verbatim or paraphrased>
- **Resolution:** <what main-agent did after the response>
- **Wall-clock impact:** <approximate; e.g. "added 2 sub-agent rounds">
```

The structured form lets the user trace the build's mid-flight pivots after the fact. A run with zero checkpoints means the build went through without any of the four triggers firing — that is the normal, expected case for most projects. A run with 3+ checkpoints suggests the brief was under-specified at Phase A and may benefit from a Phase A revisit on the next iteration.

## What this protocol does NOT do

- It does not pause for warnings. A sub-agent return with `status=ok` plus a non-empty `warnings` list does not trigger a checkpoint; warnings are aggregated for the final report.
- It does not pause for low-confidence returns. A sub-agent returning `status=partial` with `confidence=low` is reported as a warning, not a checkpoint, unless its blocking issue ALSO meets one of the four triggers.
- It does not interrupt parallel batches mid-flight. A parallel-dispatched wave runs to completion; main-agent waits for all returns before evaluating triggers. The first trigger to fire in the aggregated returns is the one that produces the checkpoint.
- It does not replace the satisfaction gate. Phase A still ends with the explicit gate. The checkpoint is for mid-Phase-B events only.
- It does not generate spontaneous status updates. Main-agent does not say "now running wireframe-builder... now running accessibility-auditor..." during normal Phase B execution. Mid-flight commentary is reserved for checkpoint events.

## Cross-references

- `references/two-mode-workflow.md` — Phase A satisfaction gate (the sibling protocol that ends Phase A).
- `references/sub-agent-return-contract.md` — the `status` / `blocking_issues` / `next_action` fields that drive the trigger conditions.
- `references/authority-hierarchy.md` — the veto-holder list (the source for Trigger 1).
- `references/agent-interaction-patterns.md` — error propagation rules (what main-agent does after Trigger 2 or 4 returns).
- `references/TECH-orchestration-conflict-resolution.md` — sibling doc on how conflicts between sub-agents are resolved (orthogonal to checkpoints, but Trigger 1 commonly follows a conflict).
- `references/TECH-orchestration-parallel-dispatch.md` — sibling doc on how parallel batches feed into checkpoint evaluation.
- `references/TECH-orchestration-recovery-from-veto.md` — sibling doc on the recovery options after a Trigger 1 checkpoint.
- `agents/ai-maestro-webdesign-main-agent.md` §15 Orchestration Doctrine — the binding consumer of this checkpoint protocol.
