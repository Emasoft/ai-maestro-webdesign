---
name: TECH-orchestration-conflict-resolution
category: main-agent-references
source: batch9 T-161 (clean-room from orchestration patterns; general design knowledge — no specific source attribution)
also-in: authority-hierarchy.md (broad domain table); this doc tightens the tiebreak procedure
---

# Orchestration — conflict resolution tiebreak hierarchy

## Table of Contents

- [What it does](#what-it-does)
- [When this is relevant](#when-this-is-relevant)
- [The tiebreak hierarchy](#the-tiebreak-hierarchy)
- [Decision tree](#decision-tree)
- [Confidence-score interpretation](#confidence-score-interpretation)
- [Worked example — good case](#worked-example-good-case)
- [Worked example — bad case](#worked-example-bad-case)
- [Recording the decision](#recording-the-decision)
- [What this protocol does NOT do](#what-this-protocol-does-not-do)
- [Cross-references](#cross-references)

## What it does

Defines the deterministic tiebreak hierarchy main-agent applies when two or more sub-agent outputs disagree on a single decision point. The hierarchy resolves conflicts in a fixed order — no ad-hoc weighting, no silent preference, no main-agent guessing inside a specialist's domain.

The hierarchy answers one question: **when sub-agent A and sub-agent B return contradictory recommendations for the same artifact decision, whose recommendation does main-agent apply, and how does it record the losing recommendation so the user can see the trade-off?**

The broad domain-to-authority table lives in `authority-hierarchy.md`. This doc adds the procedural layer: the exact ordered list main-agent walks, the confidence-score rules, and the failure modes when the hierarchy cannot resolve the conflict.

## When this is relevant

Whenever main-agent aggregates outputs from two or more sub-agents and notices contradictory recommendations on the same decision point. Common triggers:

- Brand-researcher returns a primary color; accessibility-auditor flags that color as failing WCAG-AA contrast on the proposed background.
- SEO-strategist wants a keyword-loaded H1; user-research-analyst wants an emotional H1.
- Multilanguage-copywriter produces a French headline; legal-expert says the headline phrasing violates French consumer-protection law.
- Two discovery agents disagree on the same input data (brand-researcher reads competitor URLs as "minimalist trend"; user-research-analyst reads user interviews as "users want density").
- Component-library-architect emits a token; brand-researcher's extracted reference uses a different value.

Not relevant when:

- One sub-agent has no opinion on the decision (single-agent output → no conflict).
- The disagreement is in orthogonal domains with no shared decision point (SEO meta-description length vs legal disclaimer wording — both can be satisfied independently).
- The user has already stated a direct preference that pre-empts the conflict.

## The tiebreak hierarchy

Walk this list top-to-bottom. The first rule that fires resolves the conflict. Stop at the first applied rule.

| Order | Rule | Wins when |
|---|---|---|
| 1 | **Legal-expert veto** | `amw-legal-expert-agent` returns `blocking_issues` in the mandatory-element / regulatory-compliance category. Nothing below this rule can override the veto without user-accepted-risk acknowledgement. |
| 2 | **Accessibility-auditor veto** | `amw-accessibility-auditor-agent` returns `blocking_issues` in the WCAG-AA hard-blocker category (contrast below threshold, missing alt-text, keyboard-trap, motion-induced vestibular risk). Same override rules as legal. |
| 3 | **User direction** | The user has stated a direct preference on this exact decision in Phase A or earlier in Phase B. The user's word wins for their own project (subject to rules 1 and 2). |
| 4 | **Domain authority per `authority-hierarchy.md`** | One of the conflicting agents is the named authority for the decision's domain (e.g. brand-researcher owns visual direction, user-research-analyst owns IA / section order, etc.). |
| 5 | **Sub-agent confidence score** | When two non-authority agents conflict OR two equally-authoritative agents conflict, the one with the higher `confidence` field in its YAML return contract wins. |
| 6 | **Main-agent best-judgment** | When all five rules above fail (no veto, no user direction, no domain authority owns the decision, confidence scores are equal or absent), main-agent applies a documented default per `§6 Universal Decision Criteria` of the main-agent spec — but ALSO surfaces the conflict to the user with both options for explicit confirmation. |

Two invariants hold across the whole hierarchy:

1. **The losing recommendation is never silently discarded.** Whichever rule fires, the recommendation that lost goes into the final job-completion report's `warnings` or `decisions arbitrated` section so the user sees both sides.
2. **Veto rules (1 and 2) cannot be overridden by lower rules.** A user override requires explicit acknowledgement ("ship without the cookie banner, I accept the legal risk"); it is logged as `user-accepted-risk` and never re-bound silently.

## Decision tree

```
sub-agent A and sub-agent B return contradictory outputs on decision D
                    │
                    ▼
            is A or B a veto-holder
        (legal-expert or accessibility)
            with blocking_issues
            in their veto domain?
                    │
        ┌───────────┴───────────┐
       YES                      NO
        │                        │
        ▼                        ▼
   apply veto             has user already
   recommendation         stated a direct
   write losing rec       preference on D?
   to warnings            │
                ┌─────────┴─────────┐
               YES                  NO
                │                    │
                ▼                    ▼
       apply user direction    does authority-hierarchy.md
       write conflict to       name an authority for D's
       decisions-arbitrated    domain?
                                    │
                            ┌───────┴───────┐
                           YES              NO
                            │                │
                            ▼                ▼
                    apply authority's   compare confidence
                    recommendation       scores in YAML
                    write losing to     headers
                    warnings                 │
                                    ┌────────┴────────┐
                                   A>B               equal/absent
                                    │                 │
                                    ▼                 ▼
                            apply higher       apply main-agent
                            confidence rec     default per §6
                            write losing       AND surface to user
                            to warnings        with both options
```

## Confidence-score interpretation

The `confidence` field in a sub-agent's YAML return contract is one of `high` / `medium` / `low` / `partial`. It is not a numeric score; the agent emits the value based on its own knowledge of its inputs.

Tiebreak interpretation:

- **high vs medium** → high wins. Difference of one step is meaningful.
- **high vs low** → high wins, AND main-agent surfaces the conflict to the user (the gap suggests one of the agents has significantly stronger grounding).
- **medium vs medium** → cannot resolve on confidence alone. Fall through to rule 6 (main-agent best-judgment + user surfacing).
- **partial** → treat as "suggestive, not authoritative". Falls behind any non-partial recommendation regardless of label.
- **absent confidence field** → treat as `medium`. Do not infer high confidence from a missing field.

Two agents both returning `high` is the most common cause of falling through to rule 6 — both believe they are right. That is exactly the case where main-agent must surface the conflict, not silently pick.

## Worked example — good case

**Scenario:** Bora Bora resort landing page. Brand-researcher returns extracted token `--primary: #2EC4B6` (a teal pulled from luxury-resort competitors). Accessibility-auditor audits the proposed hero with white text on the teal and returns `blocking_issues: ["contrast ratio 3.2 against #FFFFFF fails WCAG-AA for body text (requires 4.5)"]`, confidence `high`.

**Hierarchy walk:**

1. Rule 1 (legal-expert veto) — N/A; no legal-expert involvement on this color choice.
2. Rule 2 (accessibility-auditor veto) — **fires**. Accessibility-auditor returned a WCAG-AA hard blocker in its veto domain.

**Resolution:** Main-agent applies the accessibility-auditor recommendation. Concretely:

- Reject the proposed `--primary: #2EC4B6` for body-text-on-primary surfaces.
- Re-prompt brand-researcher with `extracted_tokens` plus the contrast constraint: "Need a darker variant of the brand teal that meets 4.5:1 contrast against white text, or accept that white text on `#2EC4B6` is reserved for display-size headlines (≥24px) only where the AA threshold drops to 3:1."
- Brand-researcher returns a darker variant `#1F8F86` plus a usage note ("`#2EC4B6` reserved for large headings and decorative blocks").
- Both agents sign off.

**Decisions arbitrated entry in final report:**

```
Decision: primary brand color
- Initial: #2EC4B6 from brand-researcher (luxury-resort competitor extraction)
- Conflict: accessibility-auditor flagged 3.2:1 contrast against #FFFFFF body text
- Resolution: split primary into #1F8F86 (body-text surfaces) + #2EC4B6 (display headings, decorative)
- Why: accessibility-auditor veto on WCAG-AA contrast
```

The user sees the trade-off ("we used a darker teal so the body text meets contrast; the original lighter teal is still used on display headings"). Nothing is silently dropped.

## Worked example — bad case

**Scenario (anti-pattern):** Same Bora Bora landing page. Brand-researcher returns extracted token `--primary: #2EC4B6`. Accessibility-auditor flags the contrast blocker.

**Bad-case main-agent behavior:** Main-agent decides "brand-researcher is closer to the user's stated aesthetic intent (luxury resort), so I'll keep the teal", silently lowers the body text size from 16px to 14px to "compensate", and ships.

**Why this is wrong:**

1. **The veto was silently overridden.** Accessibility-auditor returned a hard blocker; main-agent's lowering body text from 16px to 14px does not actually resolve the contrast issue (contrast is independent of size; the WCAG-AA threshold at 4.5 applies to body text at any size below 24px / 18.66px-bold). Main-agent introduced a SECOND blocker (sub-16px body text triggers a reflow concern) on top of the unresolved first.
2. **The user never saw the conflict.** No "decisions arbitrated" entry. No warning. The shipped page fails WCAG-AA silently. When the user runs a 3rd-party accessibility audit two weeks later, they find a defect they were never told about.
3. **The hierarchy was bypassed.** Rule 2 (accessibility veto) was not applied. Main-agent jumped to "I'll handle it myself", which is rule 6 (best-judgment) — but rule 6 only fires AFTER rules 1-5 have been walked, AND rule 6 requires surfacing the conflict to the user, not silent handling.

**Correct fix path:** Walk the hierarchy in order. Rule 2 fires. Apply the accessibility recommendation. Record the trade-off. Tell the user.

The bad case is the failure mode this document exists to prevent. Main-agent's job is NOT to "balance" specialists' opinions by silently mixing them — it is to apply the hierarchy deterministically and surface every tiebreak decision to the user.

## Recording the decision

Every conflict resolution produces a structured entry in the final job-completion report. Format:

```markdown
### Conflict: <decision-domain — short>
- **Initial recommendation:** <agent-A's output, with confidence>
- **Conflicting recommendation:** <agent-B's output, with confidence>
- **Hierarchy rule applied:** <rule 1-6 + which agent / preference won>
- **Resolution:** <the concrete decision made, including any compromise or split-token approach>
- **Why:** <one-sentence rationale citing the hierarchy rule>
- **Losing recommendation logged in warnings:** yes/no
- **User surfacing required:** yes/no (rule 6 always surfaces; rules 1-2 surface when the veto requires user override)
```

The structured form makes the decision auditable. A user reading the report can trace every contested decision back to a named rule.

## What this protocol does NOT do

- It does not resolve disagreement between the user and a sub-agent. The user's word wins for their own project (rule 3), except when a veto-holder's blocking issue represents a legal or WCAG-mandated requirement the user cannot waive unilaterally. In that case main-agent surfaces the conflict and waits for explicit user override.
- It does not weight confidence scores numerically. The hierarchy is ordinal, not cardinal. A `high` does not "outweigh" 1.5 `medium`s.
- It does not silence the losing side. Every losing recommendation goes into `warnings` or `decisions arbitrated`. The user always sees both options.
- It does not prevent main-agent from asking the user. Rule 6 explicitly REQUIRES user surfacing. Asking the user is the right move when no rule above 6 resolves the conflict.
- It does not retroactively re-resolve. Once a conflict is resolved and recorded, main-agent does not re-arbitrate the same conflict mid-run unless new information arrives (a sub-agent re-runs with updated input, or the user changes direction).

## Cross-references

- `authority-hierarchy.md` — broad domain → authority table (the source for rule 4).
- `sub-agent-return-contract.md` — confidence field semantics (the source for rule 5).
- `TECH-orchestration-parallel-dispatch.md` — sibling doc on when to dispatch sub-agents in parallel vs sequentially.
- `TECH-orchestration-checkpoint-protocol.md` — sibling doc on when main-agent must pause and check in with the user.
- `TECH-orchestration-recovery-from-veto.md` — sibling doc on how to recover when a veto fires (the downstream of rules 1-2 of this hierarchy).
- `two-mode-workflow.md` — Phase A/B context for when conflicts arise.
- `agents/ai-maestro-webdesign-main-agent.md` §15 Orchestration Doctrine — the binding consumer of this hierarchy.
