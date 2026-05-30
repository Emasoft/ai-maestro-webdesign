---
name: amw-text-visual-state
description: ASCII state machines and storyboards for user journeys, retention loops, lifecycles, stateful processes — for PRs, ADRs, growth docs. Triggers on "ASCII state machine", "text state diagram", "user journey in ASCII", "retention loop as text", "issue lifecycle in monospace". Does NOT trigger on "state", "journey", "lifecycle" alone — routes to design-principles / ux-flows / diagram-svg. Use when producing an ASCII state machine or storyboard. Trigger with "ASCII state machine".
version: 0.1.0
---

# Text-Visual State — ASCII state machines

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Produces ASCII state machines and user-journey storyboards that model stateful processes — user lifecycle, issue triage, experiment status, order lifecycle — using `[STATE]` bracket notation with labeled `-->` transition arrows, guard conditions, and optional metric/dashboard links. Every diagram passes a completeness check (all states have in/out edges) and `bin/amw-validate-ascii.py` before delivery. Width ceiling: 78 columns terminal, 100 GitHub ADR.

## Examples

See [examples](./references/examples.md) for skeleton and annotated-with-metrics forms.

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during Phase A (low-fi sketch) or Phase B (validated artifact). Skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. ASCII state-machine storyboards — boxed states + labeled transitions, guard conditions, entry/exit actions, optional metrics dashboards.

This skill is for **stateful processes** (user lifecycle, issue triage, experiment status, order lifecycle). NOT freeform flowcharts ([workflows](../amw-text-visual-workflows/SKILL.md)), architecture diagrams ([arch](../amw-text-visual-arch/SKILL.md)), CLI panels ([cheatsheets](../amw-text-visual-cheatsheets/SKILL.md)), or retrospectives ([retro](../amw-text-visual-retro/SKILL.md)). For SVG/clickable output route to [ux-flows](../amw-ux-flows/SKILL.md) or [ascii-to-svg](../amw-ascii-to-svg/SKILL.md) after ASCII approval.

## Trigger conditions

- "ASCII state machine for the user lifecycle"
- "retention loop in text"
- "text diagram of issue triage states"
- "state transitions as monospace"
- "ASCII storyboard for onboarding"
- "state machine I can paste in a PR"

Do NOT activate on broad design or product vocabulary. "User journey" on its own does not trigger this — `ux-flows` or `ux-designer` may be the right routes for that phrasing.

## Inputs expected

1. **State list** — every state the entity can occupy, with no synonyms collapsed. Example: `New`, `Activated`, `Retained`, `Churn Risk`, `Churned`.
2. **Transition triggers** — what event / metric / timer causes each transition. Example: `signup complete`, `>=3 sessions`, `NPS<30`, `90 days silent`.
3. **Guard conditions and actions** — preconditions that must hold for a transition to fire, and side effects. Example: `guard: has_verified_email`, `action: send_welcome_email`.
4. **Start and end states** — explicitly named. If a state is a terminal sink (no outgoing edges), flag it.

If any is missing, ask one bundled question. Fabricating states or triggers silently is a trust failure; the whole point of a state machine is rigor.

## Diagram format

Standard legend, skeleton, and annotated-with-metrics example all live in [examples](./references/examples.md). Quick legend: `[STATE]` brackets, `(start)` / `(end)` / `((STATE))` (absorbing), `-->` solid + label, `..>` optional, `--[guard: x] trigger/action--> [NEXT]`. The annotated form adds `metric: <name> (link)` below each transition so the state machine stays falsifiable.

## Glyph and width standards

- **Width ceiling:** 78 columns terminal / 100 GitHub-ADR. Never exceed 100.
- **No tabs.** Spaces only.
- **State brackets:** `[STATE]` for normal, `(start)` / `(end)` for terminals, `((STATE))` for double-boxed absorbing.
- **Edge labels are mandatory.** Every arrow has a trigger word. `-->` alone is never acceptable.
- **No `▼ ▲ ▶ ◀ ⟶ ⇒`.** Use `v ^ > <` and `->` / `=>` / `..>` .
- **No decorative emoji.** For optional states use the `..>` dotted arrow, not an emoji.

## Extended connection types

When the standard `-->` / `..>` set isn't expressive enough — reverse transitions (undo/rollback), reciprocal pairs (open/close), submachine dependency — use this vocab. Pick one style per diagram.

| Type | Glyph | Meaning |
|---|---|---|
| sync | `-->` | Standard labeled transition. |
| emphasized | `==>` | Primary / happy-path transition. |
| async | `~~>` | Out-of-band event (timer, external signal). |
| optional | `..>` | Optional / guarded / non-deterministic. |
| return | `<--` | Reverse transition (undo, cancel). Label still required. |
| bidirectional | `<-->` | Paired transitions (label both triggers). |
| dependency | `---▷` | Submachine depends on parent state. |
| association | `───` | Plain relation, no direction. |

`return` arrows handle undo / back-button flows cleanly — e.g. `[CONFIRMED] <-- cancel -- [CART]`.

## Completeness check

After drafting, verify:

- Every state (except the start) has at least one incoming edge.
- Every state (except terminal absorbing states) has at least one outgoing edge.
- Every edge has a label.
- No state is dangling (exists in the legend but has no edges).
- If there is a `Churn Risk` or `Blocked` style recovery state, it has at least one outgoing edge back to a healthy state AND one to the terminal state.

If any of these fail, fix before showing the user — an unreachable state or a missing exit is a real bug in the lifecycle model.

## Validation gate (MANDATORY)

Every diagram MUST pass `../../bin/amw-validate-ascii.py` before delivery. Flow: draft → `/tmp/amw-tvs-<slug>.txt` → run validator → PASS = present in fenced block; FAIL = apply every `FIX:` hint and re-run until PASS. For state machines with >10 states use `../../bin/amw-ascii-render.py diagram` (alignment guaranteed). See [SKILL](../amw-ascii-validator/SKILL.md) for the JSON schema.

## Instructions

1. Confirm the four inputs (states, triggers, guards/actions, start/end). One bundled question.
2. Run the completeness check on the state list before drafting.
3. Draft the diagram using the standard legend.
4. Run the validation gate. Loop until PASS.
5. Run the completeness check again on the drafted diagram.
6. Present inside a fenced code block (no language tag).
7. If the user has metrics / dashboards available, offer the annotated form and ask whether to add the links.
8. Offer to save a canonical copy to `docs/state-machines/<name>.txt` or similar project-local location. Do not write until user approves.

## Technique selection / References

Each TECH file under `./references/` follows the standard TOC: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references.

- [TECH-state-guards-and-actions](./references/TECH-state-guards-and-actions.md) — `[guard]` prefix + `/{action}` suffix
- [TECH-state-machine-legend](./references/TECH-state-machine-legend.md) — `[STATE]` boxes + `-->` / `..>` arrows
- [TECH-every-state-has-ingress-egress](./references/TECH-every-state-has-ingress-egress.md) — verification rule for correctness
- [TECH-metrics-per-transition](./references/TECH-metrics-per-transition.md) — link every edge to a dashboard
- [examples](./references/examples.md) — skeleton + annotated-with-metrics rendered diagrams

<!-- end of references -->

## Completion checklist

Verify all items before reporting complete. FAIL on any triggers a remediation loop.

- Inputs captured verbatim — no silent paraphrasing.
- At least one `TECH-*.md` consulted and cited in the report.
- Output passes Non-negotiables (below).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
- Output validated by `bin/amw-validate-ascii.py`.
- Cross-skill hand-offs documented.
- User-facing filename is descriptive English.

## Output

Two outputs per invocation:

1. **Artifact(s)** — monospaced ASCII state machines + journey storyboards. Output path is determined by project inference per [project-output-routing](../amw-design-principles/references/project-output-routing.md) (user-supplied path → framework convention → existing `./design/` → `./design/diagrams/` → `/tmp/amw-text-visual-state-<slug>/`).

2. **Job-completion report** — `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<slug>_<8-char-hash>.md` containing: Inputs · Method · Artifacts · Checklist · Deviations. Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. **Every artifact MUST be linked from the report.**

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8`
- **python_packages:** none
- **npm_packages:** none
- **mcp_servers:** none
- **scripts:** `../../bin/amw-validate-ascii.py` (mandatory), `../../bin/amw-ascii-render.py diagram` (optional)

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (Rule 1: without a real state list, the diagram is fabrication).
- [SKILL](../amw-ascii-validator/SKILL.md) — validation contract.
- Siblings: [workflows](../amw-text-visual-workflows/SKILL.md), [arch](../amw-text-visual-arch/SKILL.md), [cheatsheets](../amw-text-visual-cheatsheets/SKILL.md), [retro](../amw-text-visual-retro/SKILL.md).
- [SKILL](../amw-ux-flows/SKILL.md) — route here when state machine becomes clickable wireframes.
- [SKILL](../amw-diagram-svg/SKILL.md) + [SKILL](../amw-ascii-to-svg/SKILL.md) + `/amw-ascii-to-svg` — for SVG output.

## How to invoke

No dedicated slash command. Triggered by phrases like "ASCII state machine for the activation funnel". Also `/amw-sketch` for plan-phase state modelling; `/amw-ascii-to-svg` after approval.

## Non-negotiables

- Every diagram passes `../../bin/amw-validate-ascii.py` before delivery. No exceptions.
- 78-column terminal ceiling / 100-column GitHub ceiling.
- No tabs.
- Every arrow has a trigger label. Every state (except terminals) has entry and exit edges. Complete the model before drawing it.
- No variable-width glyphs or decorative emoji in structural positions.
- No fabricated states or triggers. If the user has not specified, ask.
- Does NOT emit HTML or SVG. ASCII only.

## Error Handling

| Failure mode | Recovery |
|---|---|
| State list has synonyms collapsed ("Active" and "Activated" used interchangeably) | Ask the user to deduplicate or disambiguate before drafting — the ambiguity is a product-model issue, not a drawing issue. |
| State machine has >15 states | Collapse related states into a super-state with a footnote, or split into two diagrams (e.g. "happy path" vs "error paths"). |
| Missing terminal / absorbing state | Ask the user. Every real entity eventually leaves the system — `Churned`, `Closed`, `Shipped`, `Archived`. Add it. |
| Missing a recovery edge (e.g. `Churn Risk` has no route back to `Retained`) | Surface to user: "Is there a path back to Retained, or is Churn Risk always a one-way step?" Do not guess. |
| Dense transitions between 3-4 states create arrow tangles | Re-layout states in a triangle or diamond; use numbered references (`(1)`) and an edge list below if arrows still cross. |
| User wants state machine in Mermaid instead | Route to `../amw-diagram-architecture/` in mermaid-passthrough mode. Not this skill's scope. |
| User asks "is this diagram complete?" | Run the completeness check explicitly and report findings. Offer to add missing edges. |
