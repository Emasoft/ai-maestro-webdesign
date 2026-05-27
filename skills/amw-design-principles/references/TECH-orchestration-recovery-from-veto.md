---
name: TECH-orchestration-recovery-from-veto
category: main-agent-references
source: batch9 T-164 (clean-room from orchestration patterns; general design knowledge — no specific source attribution)
also-in: authority-hierarchy.md (defines veto power); TECH-orchestration-checkpoint-protocol.md (Trigger 1 is the entry point)
---

# Orchestration — recovery from a veto-holder block

## Table of Contents

- [What it does](#what-it-does)
- [When this is relevant](#when-this-is-relevant)
- [The three recovery options](#the-three-recovery-options)
- [Decision tree for picking a recovery path](#decision-tree-for-picking-a-recovery-path)
- [Recovery option A — user override](#recovery-option-a-user-override)
- [Recovery option B — re-author the offending element](#recovery-option-b-re-author-the-offending-element)
- [Recovery option C — drop the offending element](#recovery-option-c-drop-the-offending-element)
- [Worked example — good case](#worked-example-good-case)
- [Worked example — bad case](#worked-example-bad-case)
- [Recording the recovery](#recording-the-recovery)
- [What this protocol does NOT do](#what-this-protocol-does-not-do)
- [Cross-references](#cross-references)

## What it does

Specifies main-agent's recovery procedure after a veto-holder sub-agent (`amw-legal-expert-agent`, `amw-accessibility-auditor-agent`) blocks Phase B forward progress. This is the downstream protocol of Trigger 1 in `TECH-orchestration-checkpoint-protocol.md`: the checkpoint protocol identifies that a veto fired and surfaces the event to the user; this protocol describes the concrete option set main-agent presents and how each option resolves.

The protocol exists because "what do we do now that the audit failed" has exactly three viable answers, no more no fewer. Without a fixed option set, main-agent tends toward either (a) silent over-engineering ("I'll just fix everything myself"), or (b) paralysis ("the audit failed, I can't proceed"). Neither is correct. The user owns the choice between override, fix, and drop — main-agent's job is to present the three concretely so the user can pick.

## When this is relevant

A veto-holder sub-agent has returned `status=failed` with `blocking_issues` in its veto domain:

- `amw-legal-expert-agent` flags a missing GDPR cookie banner, a missing ADA-required accessibility statement, a copy claim that violates consumer-protection law, age-gating gaps, jurisdiction-specific disclaimer requirements, etc.
- `amw-accessibility-auditor-agent` flags a WCAG-AA hard blocker — contrast below threshold, missing alt-text on informational images, keyboard-trap, missing focus indicators, vestibular-risk motion without a `prefers-reduced-motion` guard, illegible text size below the floor for the surface type, etc.

Not relevant when:

- A non-veto sub-agent fails (use the failure rules in `agent-interaction-patterns.md`).
- A veto-holder returns warnings but no blocking_issues (warnings go to the final report; no recovery needed).
- The user has already pre-authorized a known-risk path that the veto would otherwise block (the override has been pre-applied; main-agent records the original veto and the prior authorization without re-prompting).

## The three recovery options

The recovery option set is fixed: A, B, C. Every veto checkpoint surfaces all three to the user, unless one is structurally impossible (e.g., the offending element is the page itself, so option C "drop" cannot apply).

| Option | What main-agent does | Cost class | When this is right |
|---|---|---|---|
| **A — User override** | The user accepts the risk in writing. The veto recommendation is logged in `user-accepted-risk`. Phase B proceeds with the offending element as-is. | Zero sub-agent cost; legal/accessibility risk transferred to the user. | The user has external context that the agent does not have (e.g., a separate legal team has already approved the variant, the page is internal-only, the deployment context bypasses the rule). |
| **B — Re-author the offending element** | A Tier-3 production sub-agent (typically wireframe-builder, sometimes diagram-producer or component-library-architect) re-runs against the SAME approved Phase A direction but with the veto's constraint added to its input contract. The element is regenerated to satisfy both the original spec and the veto. | One additional sub-agent round (sometimes two, if the fix needs token-architect input). | The veto identifies a real defect that can be repaired without dropping the element. This is the most common case and the right default for almost all WCAG hard blockers. |
| **C — Drop the offending element** | The element is removed from the artifact entirely. Phase B proceeds with the smaller artifact. The drop is recorded so the user can choose to add it back in a v2. | Zero sub-agent cost; the user trades scope for compliance. | The element is non-essential to the brief, repairing it would be disproportionately expensive, OR the user values the smaller artifact over the contested element. |

The user's choice between A, B, C is theirs alone. Main-agent's role is to make each option concrete enough that the user can pick.

## Decision tree for picking a recovery path

```
veto-holder returned blocking_issues
            │
            ▼
   does the element have an
   obvious mechanical fix?
   (e.g. token swap, missing alt text,
    add prefers-reduced-motion guard)
            │
   ┌────────┴────────┐
  YES                NO
   │                  │
   ▼                  ▼
option B is     does the brief require
the natural     the element? (e.g. cookie
default;        banner for EU users IS
present all 3   non-optional)
                        │
                ┌───────┴───────┐
               YES              NO
                │                │
                ▼                ▼
        option C is bad   option C is
        (cannot drop a    legitimate
        required element); (element is
        present A + B     decorative or
        only              optional);
                          present all 3
```

The tree determines which options are STRUCTURALLY available; the user still picks among the available options.

## Recovery option A — user override

**Mechanics:**

1. Main-agent presents the override as a concrete option in the checkpoint message (per `TECH-orchestration-checkpoint-protocol.md`'s message format).
2. The user emits an explicit acknowledgement that they accept the risk. Acceptable phrasings: "yes, ship without it", "I'll handle it externally", "accept the legal risk", "override the audit". Ambiguous phrasings ("ok", "fine", "whatever") DO NOT count — main-agent asks once more for explicit acknowledgement.
3. Main-agent logs the override in the final job-completion report under `## User-accepted risks`:
   ```markdown
   ### Risk: <one-sentence summary>
   - **Veto source:** <agent name>
   - **Blocking issue:** <verbatim from agent's return>
   - **User override:** <verbatim or paraphrased user acknowledgement>
   - **Recommended mitigation:** <what the veto-holder suggested as the fix; the user may want this for v2>
   ```
4. Phase B proceeds with the offending element unchanged.

**When this is right:**

- The user has external context: separate legal team approval, internal-only deployment, an existing waiver document, etc.
- The veto is geographically narrow: GDPR applies to EU visitors, but the user is shipping a US-only beta and will hard-block EU traffic at the edge.
- The veto is severity-mismatched for the deployment: a marketing landing page draft that will be revised in a week does not need WCAG-AAA, but the auditor flagged AAA-grade items as AA.

**When this is wrong:**

- The user is overriding because they are tired of the conversation, not because they have external context. Main-agent should not encourage this; the override format is intentionally explicit (requires verbatim acknowledgement) to discourage rubber-stamping.
- The user is overriding a regulatory rule they cannot legally waive (e.g., a US public-sector site must comply with ADA per federal law; a private user cannot "accept the risk" of violating it). The veto-holder's recommendation typically flags non-waivable rules; main-agent reads the recommendation and refuses the override path if applicable, presenting only options B and C.

## Recovery option B — re-author the offending element

**Mechanics:**

1. Main-agent identifies the Tier-3 producer responsible for the offending element (usually wireframe-builder; sometimes diagram-producer if the element is a diagram; sometimes component-library-architect if the issue is a token-level violation).
2. Main-agent adds the veto's constraint as an explicit field to the producer's input contract. For example:
   - Accessibility blocker on CTA contrast → wireframe-builder input gains `contrast_constraints: {primary_text_on_primary_bg: ">=4.5"}`.
   - Missing GDPR cookie banner → wireframe-builder input gains `required_fragments: ["gdpr_cookie_banner"]` plus the banner spec from legal-expert's return body.
   - Vestibular-risk motion → motion-designer input gains `motion_constraints: {prefers_reduced_motion: required, scroll_animation_max_velocity: 200px_per_sec}`.
3. Main-agent re-spawns the producer with the augmented input contract. The producer regenerates the element.
4. Main-agent re-spawns the veto-holder against the regenerated artifact. If the veto-holder signs off, recovery succeeds; if it still returns blocking_issues, main-agent surfaces the second-round failure as a new checkpoint (which may resolve to A or C this time).

**When this is right:**

- Almost always for WCAG hard blockers with mechanical fixes (contrast, alt-text, focus indicators, motion guards).
- For legal mandatory-element omissions where the missing element is well-specified (cookie banner, accessibility statement, age gate, disclaimer block).
- For any veto where the veto-holder's recommendation includes a concrete "do this instead" pattern that the producer can act on.

**When this is wrong:**

- The producer cannot generate a compliant version (e.g., the brand-required color is fundamentally below contrast threshold and the user has refused all alternatives). The fix loop will never converge; main-agent escalates back to a Trigger 1 checkpoint and surfaces only options A and C.
- The fix is disproportionately expensive: adding a single GDPR cookie banner to satisfy the veto would require redesigning the layout to accommodate a banner area that breaks the entire grid. In this case main-agent may surface a hybrid ("re-author with banner + minor layout shift, or drop the layout-conflicting section to make room") and let the user choose.

**Sub-agent rounds budget:** Recovery option B typically costs 2 additional rounds — one for the producer, one for the veto-holder to re-audit. If the second round still fails, that is a NEW checkpoint, not an automatic third attempt. Main-agent does not loop indefinitely.

## Recovery option C — drop the offending element

**Mechanics:**

1. Main-agent identifies the boundary of the offending element. The boundary is at the LARGEST level where the element can be cleanly excised — a button is one element, a hero is another, a footer is another. The boundary should not split a coherent component into a broken half.
2. Main-agent removes the element from the wireframe artifact, regenerates only the affected page region (typically a single sub-agent round with wireframe-builder), and re-runs the veto-holder against the regenerated page. The expectation is the veto disappears (the offending element no longer exists).
3. Main-agent logs the drop in the final job-completion report under `## Decisions arbitrated`:
   ```markdown
   ### Drop: <element name>
   - **Why dropped:** <veto-holder + blocking_issue>
   - **What was removed:** <concrete description of the removed component>
   - **Suggested for v2:** <the producer's recommendation for how to add it back compliantly>
   ```
4. Phase B proceeds with the smaller artifact.

**When this is right:**

- The element was decorative or optional (e.g., a testimonial carousel, an animated background, a marketing banner).
- The element was a stretch goal the user mentioned in Phase A but did not insist on.
- The cost of repair (option B) is high and the value of the element is low — drop saves more than re-author costs.
- The user explicitly prefers the smaller artifact (some users value compliance over feature parity).

**When this is wrong:**

- The element is structurally required by the brief (a contact form is the page's call-to-action; dropping it makes the page incoherent).
- The element is legally required (a cookie banner cannot be dropped to satisfy a contrast veto; main-agent must offer A or B instead).
- The element is part of the user's approved Phase A direction at a level the user emphasized. Main-agent should not silently drop something the user spent Phase A iterations refining.

## Worked example — good case

**Scenario:** Multi-locale (English + French) marketing site for a French consumer-finance product. Phase B fan-out completes; wireframe-builder produces the homepage; legal-expert (B mode) audits the French version and returns:

```yaml
status: failed
confidence: high
blocking_issues:
  - "French headline 'Garanti 100%' violates French consumer law L. 121-1 — 'garanti' as an unconditional claim requires explicit supporting language (warranty term, exclusions, contact details)"
  - "Missing legal mention block at footer per French law for finance products — must include APR disclosure, regulator notice, and registered office address"
next_action: escalate_to_user
```

**Main-agent's checkpoint message (per `TECH-orchestration-checkpoint-protocol.md`):**

```
WHAT HAPPENED
The French legal audit returned 2 mandatory-element blockers on the French homepage:
(a) the headline "Garanti 100%" violates French consumer-protection law without
supporting warranty terms; (b) the footer is missing the regulator-mandated finance
legal mention block.

OPTIONS
1. Re-author both elements — copywriter softens the headline to "Garanti avec
   conditions, voir bas de page" (French legal-compliant phrasing); wireframe-builder
   adds the legal mention block to the footer. Adds ~2 sub-agent rounds.
2. Ship as-is with the legal failures recorded as user-accepted-risk. NOT
   recommended — both are non-waivable French regulatory requirements; the site
   would be exposed to consumer-protection enforcement.
3. Drop the French version entirely; ship English-only. The French translation
   files remain on disk for a future locale-compliant v2.

DEFAULT IF NO RESPONSE
Stop and wait — these are veto-holder hard blockers in the legal/regulatory
domain; main-agent does not proceed past them without explicit user direction.
```

**User reply:** "Do option 1, and double-check the headline with copywriter for tone — I don't want it to feel disclaimer-heavy."

**Main-agent's recovery (option B):**

1. Re-spawn copywriter (Phase B mode) with input contract: `current_french_headline = "Garanti 100%"`, `legal_constraint = "L. 121-1 — unconditional 'garanti' needs supporting language; recommended phrasing 'Garanti avec conditions, voir bas de page'"`, `tone_target = "not disclaimer-heavy"`. Copywriter returns "Garantie sous conditions — détails au bas de page" (slightly more natural French than the legal-expert's literal recommendation).
2. Re-spawn wireframe-builder with input contract: `headline_text = "Garantie sous conditions — détails au bas de page"`, `required_fragments = ["french_finance_legal_mention_block"]`, plus the legal-expert's mention-block spec.
3. Re-spawn legal-expert (B mode) against the regenerated French homepage. Returns `status=ok, warnings=[]`.
4. Recovery complete. Phase B continues with the remaining audit waves.

**Final job-completion report decisions-arbitrated entry:**

```markdown
### Decision: French homepage headline + footer legal mention
- **Veto source:** amw-legal-expert-agent (B mode)
- **Blocking issues:** L. 121-1 "garanti" unconditional claim; missing finance regulator mention block
- **Recovery option chosen:** B — re-author
- **What was changed:** Headline copy updated; footer legal mention block added
- **Sub-agent rounds added:** 2 (copywriter + wireframe-builder + re-audit)
```

**Why this is good:**

- The veto fired; main-agent paused (Trigger 1 checkpoint).
- All three recovery options were presented concretely.
- The user picked option B; main-agent executed it cleanly with a re-author wave.
- The final report records what changed and why.
- The user retained agency throughout — main-agent did not silently fix or silently drop.

## Worked example — bad case

**Scenario (anti-pattern):** Same French finance site. Legal-expert returns the same two blocking_issues.

**Bad-case main-agent behavior:** Main-agent classifies "Garanti 100%" as "stylistic", overrides the legal-expert verdict on its own ("the user said they want a punchy headline"), silently leaves the legal mention block out because "the user didn't ask for it specifically", and proceeds to the next audit wave. The final report mentions "headline kept, legal mention deferred" in a footnote.

**Why this is wrong:**

1. **The veto was bypassed.** Legal-expert has veto power per `authority-hierarchy.md`. Main-agent overrode without user consent.
2. **No recovery option was offered.** A, B, and C were never presented. The user lost the choice.
3. **The override format was not used.** A user-accepted-risk override requires the user's explicit acknowledgement. Main-agent self-approving an override is structurally invalid.
4. **The dropped legal mention block was non-waivable.** French regulatory law on finance products is not something the user can opt out of. Main-agent's "deferred" was actually a regulatory violation.
5. **The "footnote" in the final report is too low-priority.** Veto overrides go in `User-accepted risks`, not in a footnote. The structure exists precisely to make the user see the risk transfer.

**Correct fix:** Apply Trigger 1. Present options A, B, C. If option A is presented and the user picks it, refuse on the grounds that the rule is non-waivable, and explain why. Only B and C remain. Let the user pick. Execute. Record.

The bad case is the failure mode this protocol exists to prevent: main-agent's helpfulness instinct can mask a regulatory violation. The three-option structure forces the conversation into the open.

## Recording the recovery

Every veto recovery produces an entry in the final job-completion report. Two cases:

- **Recovery via option A** → entry under `## User-accepted risks` (per the section structure in main-agent's §13 Return Contract).
- **Recovery via option B or C** → entry under `## Decisions arbitrated`.

The entries are structured; format examples appear in the relevant subsections above. The structural rule: every veto produces exactly one entry in exactly one of those two sections. Vetoes do not generate footnotes, do not appear inline in the artifact list, and do not disappear silently.

## What this protocol does NOT do

- It does not authorize main-agent to override a veto unilaterally. The override always requires user acknowledgement.
- It does not collapse the three options into one "best path". The user picks; main-agent presents.
- It does not retry option B more than twice. If two re-author rounds both fail to satisfy the veto, the next event is a NEW checkpoint with only options A and C surfaced (B has been exhausted).
- It does not handle non-veto failures. Those follow the failure rules in `agent-interaction-patterns.md`, which are similar in shape but not identical (no veto-class blocking; no user-accepted-risk concept).
- It does not retroactively un-drop. Once option C has been applied and the artifact has been re-rendered without the element, that decision is final for the current run. To add the element back, the user requests a new build iteration (which re-runs Phase A or re-enters Phase B with an updated approved direction).

## Cross-references

- `references/authority-hierarchy.md` — defines veto power and the veto-holder list.
- `references/TECH-orchestration-checkpoint-protocol.md` — Trigger 1 is the entry point into this protocol.
- `references/TECH-orchestration-conflict-resolution.md` — vetoes are the top of the conflict tiebreak hierarchy.
- `references/TECH-orchestration-parallel-dispatch.md` — veto-holders are dispatched in priority waves to surface their blocking_issues early.
- `references/agent-interaction-patterns.md` — failure propagation rules for non-veto failures.
- `references/sub-agent-return-contract.md` — the `blocking_issues` and `next_action` fields that signal a veto.
- `agents/ai-maestro-webdesign-main-agent.md` §15 Orchestration Doctrine — the binding consumer of this recovery protocol.
