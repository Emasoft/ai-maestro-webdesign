---
name: TECH-ux-rule-interaction
category: ux-rule-interaction
source: SKILLS-TO-INTEGRATE/web-design/ux-designer/rules/interaction-design.md
also-in: SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md
---

# TECH: Rule — Interaction Design (flows + microcopy)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Flow best practices](#flow-best-practices)
  - [Multi-step flows](#multi-step-flows)
  - [Error recovery](#error-recovery)
  - [Microcopy](#microcopy)
  - [Specific rules](#specific-rules)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

HIGH-priority rule. Covers the two elements that most directly determine whether users complete tasks or abandon them: user flows (step sequences, errors, recovery) and microcopy (button labels, error messages, empty states, confirmations).

## When to use

On any flow design (checkout, signup, onboarding, feature walkthrough), error-message review, button-copy review, empty-state design, or confirmation-dialog audit.

## How it works

### Flow best practices

- Design happy path first, then errors + edge cases
- Minimize steps (every step loses users)
- Progress indicator for 3+ step flows
- Back without losing data
- Auto-save per step
- Confirm destructive actions with specific consequences

### Multi-step flows

- Show total steps + current position ("Step 2 of 4")
- Allow skipping optional steps
- Summarize before final submission
- Confirm via email/notification for important transactions

### Error recovery

- Detect early (inline validation)
- Explain in plain language + how to fix
- Preserve all valid input (never clear on error)
- Offer alternative paths when primary fails

### Microcopy

| Context | ✗ Weak | ✓ Strong |
|---|---|---|
| Save button | Submit | Save Changes |
| Delete confirm | "Are you sure?" / Yes / No | "Delete 'Q4 Report'? This can't be undone." / Delete / Cancel |
| Empty inbox | No messages | You're all caught up! New messages will appear here. |
| Form error | Invalid | Enter a valid email address (e.g., name@example.com) |

### Specific rules

- Verbs on buttons: "Save Draft", "Send Message", "Create Account"
- Avoid generic: "Submit", "OK", "Click Here"
- Destructive buttons name the consequence: "Delete Project", not "Confirm"
- Asymmetric confirmation labels: "Delete Project" / "Keep Project" (not Yes / No)
- Error messages: what happened + how to fix + don't blame the user

## Minimal example

Checkout flow done right:

```
Cart → Shipping → Payment → Review → Confirmation
  ↑        ↑          ↑        ↑
  [Back]   [Back]     [Back]   [Edit each section]
Progress bar visible · Each step validates inline · Review screen before commit
```

Checkout flow done wrong:

```
Cart → "Login required!" → Shipping → "Re-enter email" → Payment → "Surprise $15 shipping!" → Submit
                                                                                ↓
                                                                         [No back button]
```

*Attributed to the ux-designer rule file — `SKILLS-TO-INTEGRATE/web-design/ux-designer/rules/interaction-design.md`.*

## Gotchas

- Forced registration before any value is shown ("sign up to see pricing") loses 60-80% of users.
- Dead-end confirmation screens ("Thanks!" with no next action) waste the momentum the user built.
- "Yes/No" on destructive actions is unsafe — the user who's about to delete their account should type the project name, not click Yes.
- Inconsistent verbs for the same action ("remove", "delete", "trash") in different parts of the product confuses users.

## Cross-references

- [TECH-ux-rule-research](TECH-ux-rule-research.md), [TECH-ux-rule-accessibility](TECH-ux-rule-accessibility.md), [TECH-ux-rule-ia](TECH-ux-rule-ia.md), [TECH-ux-rule-visual](TECH-ux-rule-visual.md)
  > [TECH-ux-rule-accessibility.md] What it does · When to use · How it works · WCAG AA (minimum floor) — four POUR pillars · Inclusive design patterns (beyond compliance) · Testing checklist · Minimal example · Gotchas · Cross-references
  > [TECH-ux-rule-ia.md] What it does · When to use · How it works · Navigation structure · Navigation patterns · Mobile specifics · Content organization · Information scent · Search as navigation · Minimal example · Gotchas · Cross-references
  > [TECH-ux-rule-visual.md] What it does · When to use · How it works · Establishing hierarchy · Typography scale · Color usage · Layout · Design-system essentials · Component documentation · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Interview planning · During interviews · Synthesis · Good vs bad questions · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
