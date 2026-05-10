## Table of Contents

- [Domains and authority](#domains-and-authority)
- [Veto power — what it means](#veto-power-what-it-means)
- [Resolution rules by conflict pattern](#resolution-rules-by-conflict-pattern)
- [How main-agent applies the hierarchy](#how-main-agent-applies-the-hierarchy)
- [What the hierarchy does NOT do](#what-the-hierarchy-does-not-do)
- [Enforcement](#enforcement)

# Authority hierarchy — conflict resolution and veto power

This document specifies who wins when two amw-* sub-agents return recommendations that cannot both be satisfied. Without explicit hierarchy, main-agent silently picks one, which is worse than picking the wrong one — it hides the conflict from the user.

## Domains and authority

| Domain | Authority agent | Veto power? | Arbiter when disputed |
|---|---|---|---|
| Visual / aesthetic direction | `amw-brand-researcher-agent` | no | main-agent presents both options to user |
| IA / content hierarchy / section order | `amw-user-research-analyst-agent` | no | main-agent; SEO-strategist has consulting input on H-tag structure |
| Keyword / meta / structured data | `amw-seo-strategist-agent` | no | main-agent |
| Copy / locale / cultural adaptation | `amw-multilanguage-copywriter-agent` | no | main-agent |
| Legal / compliance mandatory elements | `amw-legal-expert-agent` | **YES** | main-agent; if user overrides, mark user-accepted-risk in job report |
| WCAG AA hard blockers | `amw-accessibility-auditor-agent` | **YES** | main-agent; if user overrides, mark user-accepted-risk in job report |
| Artifact format / rendering technique | production agent (wireframe-builder, diagram-producer, etc.) | no | main-agent |
| Form architecture / validation UX | `amw-form-designer-agent` | no | accessibility-auditor wins on a11y blockers; user-research-analyst wins on flow disputes |
| Motion / animation / scroll behavior | `amw-motion-designer-agent` | no | accessibility-auditor wins on `prefers-reduced-motion` and vestibular-safety blockers |
| Email layout / MJML / table-grid | `amw-email-designer-agent` | no | accessibility-auditor wins on alt-text + plain-text-fallback; legal-expert wins on unsubscribe / sender-ID compliance |
| Design tokens / variant matrix | `amw-component-library-architect-agent` | no | brand-researcher wins on brand-fidelity (token values must round-trip to brand source); accessibility-auditor wins on contrast |

## Veto power — what it means

Two agents in this plugin have veto power: `amw-legal-expert-agent` over regulatory mandatory elements, and `amw-accessibility-auditor-agent` over WCAG AA hard blockers. Veto power means:

1. If the veto-holding agent returns `blocking_issues` in the mandatory-element / WCAG-AA category, main-agent **does not proceed to Phase B completion** until those issues are resolved or explicitly user-overridden.
2. Other agents' contrary recommendations do not override the veto. A brand-researcher recommending "remove the cookie banner for aesthetic minimalism" does not override legal-expert's "GDPR requires cookie banner for EU visitors".
3. The veto can be overridden by the user, not by main-agent and not by peer agents. If the user accepts the risk ("ship without the cookie banner, I'll handle consent externally"), main-agent logs the override in the final job-completion report under a clearly labeled "user-accepted-risk" section.
4. The veto does not block independent work streams. If legal-expert vetoes the cookie banner design but accessibility-auditor signs off on the main page, the cookie-banner issue is raised but the main-page work continues.

Veto power is narrow. Legal-expert does not have veto power over aesthetic choices, copy tone, or technical architecture. Accessibility-auditor does not have veto power over non-AA concerns (AAA nice-to-haves, Section 508 when not contractually required, etc.).

## Resolution rules by conflict pattern

### Pattern 1: Visual vs. functional tension
**Example:** brand-researcher recommends dark-mode luxury aesthetic with 14px body copy; accessibility-auditor flags body copy below 16px as a WCAG reflow concern.
**Resolution:** Accessibility-auditor has veto power. Main-agent adjusts to 16px minimum. If brand-researcher's design system depends on the 14px size, main-agent proposes a responsive size scaling (14px at 1.25rem root → 16px with root adjustment) and re-submits to both agents for sign-off.

### Pattern 2: SEO vs. UX content hierarchy
**Example:** seo-strategist wants H1 = "Luxury Overwater Villas in Bora Bora | [Brand]" for keyword coverage; user-research-analyst wants H1 = "Wake Up Over the Lagoon" for emotional resonance.
**Resolution:** No veto. User-research-analyst has IA authority, seo-strategist has H-tag consulting input. Main-agent presents both to user in a short "H1 decision point" with the trade-off ("keyword-weighted vs. emotion-weighted") and lets user choose. If user doesn't answer, main-agent defaults to the user-research-analyst option and logs seo-strategist's recommendation as a warning in the final report.

### Pattern 3: Copywriter locale vs. legal disclaimer
**Example:** multilanguage-copywriter produces a punchy French headline; legal-expert says "under French consumer law, the headline claim 'guaranteed' requires specific supporting language".
**Resolution:** Legal-expert has veto. Main-agent returns to copywriter with the legal constraint, requests a reworded headline that satisfies the law. If copywriter cannot produce one (tone collapses), main-agent escalates to user: "French law requires X; I can offer a softer tone or a longer headline — which?"

### Pattern 4: Production agent vs. discovery agent
**Example:** wireframe-builder's ASCII-to-HTML output deviates from brand-researcher's extracted spacing tokens because the responsive grid constraints force adjustment.
**Resolution:** No veto. Production agent has format/rendering authority (their domain). They must document the deviation in `warnings`. Main-agent surfaces the warning in the final job-completion report. If the deviation is large enough to violate brand-researcher's assessment ("spacing-unit 8px is mandatory"), main-agent asks user to accept the trade-off or requests a re-design.

### Pattern 5: Two discovery agents with opposite readings of the same data
**Example:** brand-researcher reads the competitor URLs as "market expects minimalism"; user-research-analyst reads the user interviews as "users want dense info-rich design".
**Resolution:** No veto, genuine disagreement. Main-agent presents both readings to user: "Competitors go minimalist but your users want density — pick one or specify a hybrid." If user defers back ("what do you recommend?"), main-agent's default is to weight user-research over competitor analysis (user-research is closer to the end-user behavior), but logs this as a judgment call.

### Pattern 6: Missing data from a domain
**Example:** no user research provided; user-research-analyst returns status=partial with confidence=low and recommendations based on domain heuristics.
**Resolution:** Low-confidence output is treated as "suggestive, not authoritative". Main-agent surfaces this to user: "No user-research data was provided; I'm using hospitality-industry heuristics. Do you want to answer three questions about your audience, or shall I proceed with the heuristic defaults?"

### Pattern 7: Upstream contradiction between user and an agent
**Example:** user says "no cookie banner, I hate those"; legal-expert says "GDPR mandates one for EU visitors".
**Resolution:** Legal-expert's veto applies, but user can override. Main-agent surfaces the conflict in exactly these terms: "GDPR requires a cookie banner for EU visitors. Options: (1) add the banner, (2) geofence EU visitors to a different entry page, (3) accept the legal risk and ship without. Which?" User's choice is logged in the final job-completion report, with option (3) labeled "user-accepted-risk".

## How main-agent applies the hierarchy

When main-agent aggregates sub-agent outputs, it runs through this decision procedure:

1. Read every sub-agent's YAML header. Note `blocking_issues` for veto-holders.
2. If any veto-holder has blocking issues: stop the forward path for the affected work stream. Produce a user-facing conflict summary with options.
3. If two non-veto agents conflict on a shared domain (H-tag, section order, tone, etc.): identify the authority per the table above, apply the authority's recommendation as default, surface the conflict as a warning with the losing recommendation attached.
4. If two agents conflict in orthogonal domains (e.g., SEO vs. legal on meta description length when legal requires a specific disclaimer): escalate to user.
5. Record every arbitration decision in the final job-completion report under a "decisions arbitrated" section. The user can review what was chosen on their behalf.

## What the hierarchy does NOT do

- It does not resolve disagreement between user-stated preferences and an agent's recommendation. The user's word always wins for their own project, except when a veto-holder's blocking issue represents a legal or WCAG-mandated requirement the user cannot waive unilaterally (e.g., ADA compliance for a US public-sector site).
- It does not silence a losing recommendation. Even when an authority agent wins, the losing recommendation goes into `warnings` so the user sees the trade-off.
- It does not override the user in Phase A conversation. Phase A is dialog; the user can change direction any round, and sub-agent recommendations are advisory not binding until the satisfaction-gate token is emitted.

## Enforcement

- Every agent spec with authority in a domain states it in §14 Hard Rules / Veto Power
- Every agent spec with veto power states the veto domain explicitly and describes what "blocking issue" means in its context
- Main-agent's §15 Orchestration Doctrine cites this document and describes the arbitration pseudo-code above
