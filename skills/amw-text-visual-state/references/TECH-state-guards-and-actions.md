---
name: TECH-state-guards-and-actions
category: text-visual-state
source: cc-plugin-text-visualizations-main/skills/tools-visual-state-machines/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-state-guards-and-actions — `[guard]` prefix + `/{action}` suffix

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Annotates state transitions with guard conditions and side-effect
actions, using `[guard]` as a prefix (`[guard: has_verified_email]`) and
`/{ action }` as a suffix (`/{ send_welcome_email }`). Keeps the
transition label self-documenting without a separate legend panel.

## When to use

- Formal state machines (ACK protocols, order-state workflows)
- User lifecycle diagrams with strict preconditions
- Compliance-sensitive flows where guards are audit-relevant

## How it works

Transition label format:

```
-- [guard_expression] trigger_event / { action } --> [NEXT_STATE]
```

- `[guard_expression]` — precondition that must be true for the
  transition to fire. Typical examples: `[has_email]`, `[age>=18]`,
  `[session_count>=3]`.
- `trigger_event` — what fires the transition. `signup_complete`,
  `timer_expired`, `user_action`.
- `/ { action }` — side effect executed during transition.
  `send_welcome_email`, `debit_account`, `log_event`.

Order in the label: guard → trigger → action → target state.

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-state-machines/SKILL.md lines 32-34 + adapted
[NEW] --[verified_email] activate / { send_welcome }--> [ACTIVATED]

[ACTIVATED] --[sessions>=3] retain--> [RETAINED]

[RETAINED] --90d_silent / { mark_churn_risk }--> [CHURN RISK]
```

## Gotchas

- Guards without an explicit failure path leave the state machine
  ambiguous — what happens if `[sessions>=3]` is false? State there or
  omit the guard.
- Action expressions should be short (`send_welcome`, not `Send a
  welcome email to the user and also log an audit event`) — keep the
  diagram legible.
- Separator style `/{action}` vs `/ action` vs `/{ action }` — pick one
  and stick to it across the project.

## Cross-references

- [TECH-state-machine-legend](./TECH-state-machine-legend.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-metrics-per-transition](./TECH-metrics-per-transition.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

