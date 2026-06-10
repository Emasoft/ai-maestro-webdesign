# amw-text-visual-state — Diagram format examples

## Table of Contents

- [Standard legend](#standard-legend)
- [Skeleton](#skeleton)
- [Annotated form with metrics and dashboards](#annotated-form-with-metrics-and-dashboards)

This file holds the skeleton state machine and the annotated form with metrics. The parent `SKILL.md` references this file when concrete examples are needed.

## Standard legend

- States: `[STATE]` uppercase inside square brackets.
- Start state: `(start)` or `(*)`.
- End / terminal state: `(end)` or `((STATE))` for a double-boxed absorbing state.
- Solid transition: `-->` with required edge label describing the trigger.
- Optional transition: `..>` (dotted) with edge label.
- Self-loop: horizontal arrow returning to same state, labeled with the event.
- Edge label format: `-- trigger --> [STATE]` or `--trigger/action--> [STATE]`.
- Guard: prefix the trigger with `[guard] ` — e.g. `--[has_email] signup_complete--> [Activated]`.

## Skeleton

```
(start)
  |
  | signup_complete / send_welcome_email
  v
[NEW]
  |
  | --[guard: verified_email] activate--> [ACTIVATED]
  v
[ACTIVATED] --fails_sla--> [CHURN RISK]
  |                              |
  | >=3 sessions                 | 7 days silent
  v                              v
[RETAINED]                     [CHURNED] ((terminal))
  |
  | 90 days silent
  v
[CHURN RISK]
```

## Annotated form with metrics and dashboards

When the user is modelling a product lifecycle, annotate each transition with the metric or query that powers it:

```
[NEW] --signup_complete--> [ACTIVATED]
        metric: dau_signup (looker://dash/42)

[ACTIVATED] --[guard: sessions>=3] retain--> [RETAINED]
            metric: week1_retention (looker://dash/51)
```

This keeps the state machine falsifiable — a reviewer can follow the link to verify the metric really says what the diagram claims.
