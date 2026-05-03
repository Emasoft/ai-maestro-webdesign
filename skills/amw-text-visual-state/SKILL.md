---
name: amw-text-visual-state
description: ASCII state machines and storyboards for user journeys, retention loops, lifecycles, stateful processes — for PRs, ADRs, growth docs. Triggers on "ASCII state machine", "text state diagram", "user journey in ASCII", "retention loop as text", "issue lifecycle in monospace". Does NOT trigger on "state", "journey", "lifecycle" alone — routes to design-principles / ux-flows / diagram-svg. ASCII only; passes amw-validate-ascii.py. Use when producing an ASCII state machine or storyboard. Trigger with "ASCII state machine".
version: 0.1.0
---

# Text-Visual State — ASCII state machines

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Produces ASCII state machines and user-journey storyboards that model stateful processes — user lifecycle, issue triage, experiment status, order lifecycle — using `[STATE]` bracket notation with labeled `-->` transition arrows, guard conditions, and optional metric/dashboard links. Every diagram passes a completeness check (all states have in/out edges) and `bin/amw-validate-ascii.py` before delivery. Width ceiling: 78 columns terminal, 100 GitHub ADR.

## Examples

See the `## Diagram format` section below for a skeleton state machine and an annotated form with metrics.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during Phase A (as a low-fi ASCII medium for state-machine sketches) or Phase B (when the approved design requires a validated ASCII state-machine artifact). The orchestrator may apply any state-transition, guard-condition, or storyboard technique from this skill without command-layer restriction.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. Produces ASCII state-machine storyboards — boxed states connected by labeled transition arrows, with guard conditions, entry/exit actions, and optional links to metrics dashboards.

This skill is for **stateful processes** — user lifecycle (New → Activated → Retained → Churned), issue lifecycle (Open → In Progress → Blocked → Closed), experiment status (Proposed → Running → Analyzed → Shipped → Rolled Back), order lifecycle, etc. It is not for freeform flowcharts (`../amw-text-visual-workflows/`), architecture diagrams (`../amw-text-visual-arch/`), CLI panels (`../amw-text-visual-cheatsheets/`), or retrospectives (`../amw-text-visual-retro/`). If the state machine needs to become clickable wireframes or SVG, hand off to `../amw-ux-flows/` or `../amw-ascii-to-svg/` after the ASCII is approved.

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

### Standard legend

- States: `[STATE]` uppercase inside square brackets.
- Start state: `(start)` or `(*)`.
- End / terminal state: `(end)` or `((STATE))` for a double-boxed absorbing state.
- Solid transition: `-->` with required edge label describing the trigger.
- Optional transition: `..>` (dotted) with edge label.
- Self-loop: horizontal arrow returning to same state, labeled with the event.
- Edge label format: `-- trigger --> [STATE]` or `--trigger/action--> [STATE]`.
- Guard: prefix the trigger with `[guard] ` — e.g. `--[has_email] signup_complete--> [Activated]`.

### Skeleton

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

### Annotated form with metrics and dashboards

When the user is modelling a product lifecycle, annotate each transition with the metric or query that powers it:

```
[NEW] --signup_complete--> [ACTIVATED]
        metric: dau_signup (looker://dash/42)

[ACTIVATED] --[guard: sessions>=3] retain--> [RETAINED]
            metric: week1_retention (looker://dash/51)
```

This keeps the state machine falsifiable — a reviewer can follow the link to verify the metric really says what the diagram claims.

## Glyph and width standards

- **Width ceiling:** 78 columns terminal / 100 GitHub-ADR. Never exceed 100.
- **No tabs.** Spaces only.
- **State brackets:** `[STATE]` for normal, `(start)` / `(end)` for terminals, `((STATE))` for double-boxed absorbing.
- **Edge labels are mandatory.** Every arrow has a trigger word. `-->` alone is never acceptable.
- **No `▼ ▲ ▶ ◀ ⟶ ⇒`.** Use `v ^ > <` and `->` / `=>` / `..>` .
- **No decorative emoji.** For optional states use the `..>` dotted arrow, not an emoji.

## Extended connection types

State machines sometimes need to show reverse transitions (undo/rollback), reciprocal state pairs (open/close handshake), dependency relationships between state machines (submachine depends on parent), or plain state associations. Use this vocabulary when the standard `-->` / `..>` set is not expressive enough. Source: adapted from the diagram-skill-main ASCII-STYLES reference (subsumed into the current skill).

| Type | Glyph | Meaning |
|---|---|---|
| sync | `-->` | Standard labeled transition. |
| emphasized | `==>` | Primary / happy-path transition; single accented arrow per diagram. |
| async | `~~>` | Async transition fired by out-of-band event (timer, external signal). |
| optional | `..>` | Dotted optional / guarded / non-deterministic transition. |
| return | `<--` | Reverse transition (undo, rollback, back-button, cancel). Edge label still required. |
| bidirectional | `<-->` | Paired transitions (e.g. `[OPEN] <-- close/open --> [CLOSED]`). Label MUST list both triggers. |
| dependency | `---▷` | Submachine depends on parent state (hollow triangle). Used only in multi-level hierarchical diagrams. |
| association | `───` | Plain relation between states, no direction (grouping cue, not a transition). |

`return` arrows are how user-journey state machines show undo / back-button flows cleanly without inventing fake events — e.g. `[CONFIRMED] <-- cancel -- [CART]`. The edge label on a return arrow is the action that triggered the reverse transition, same convention as forward transitions.

## Completeness check

After drafting, verify:

- Every state (except the start) has at least one incoming edge.
- Every state (except terminal absorbing states) has at least one outgoing edge.
- Every edge has a label.
- No state is dangling (exists in the legend but has no edges).
- If there is a `Churn Risk` or `Blocked` style recovery state, it has at least one outgoing edge back to a healthy state AND one to the terminal state.

If any of these fail, fix before showing the user — an unreachable state or a missing exit is a real bug in the lifecycle model.

## Validation gate (MANDATORY)

Every diagram this skill emits MUST pass `../../bin/amw-validate-ascii.py` before being shown to the user.

The flow:

1. Draft the diagram.
2. Write it to `/tmp/amw-tvs-<slug>.txt`.
3. Run `perl ../../bin/amw-validate-ascii.py /tmp/amw-tvs-<slug>.txt`.
4. If PASS → present in a fenced code block.
5. If FAIL → apply every `FIX:` hint, re-run. Loop until PASS.
6. Never present an un-validated diagram.

For state machines with many states and transitions (>10), prefer `../../bin/amw-ascii-render.py` in `diagram` mode with explicit boxes and connectors — the renderer guarantees alignment by construction. See [SKILL](../amw-ascii-validator/SKILL.md) for the JSON schema.

## Instructions

1. Confirm the four inputs (states, triggers, guards/actions, start/end). One bundled question.
2. Run the completeness check on the state list before drafting.
3. Draft the diagram using the standard legend.
4. Run the validation gate. Loop until PASS.
5. Run the completeness check again on the drafted diagram.
6. Present inside a fenced code block (no language tag).
7. If the user has metrics / dashboards available, offer the annotated form and ask whether to add the links.
8. Offer to save a canonical copy to `docs/state-machines/<name>.txt` or similar project-local location. Do not write until user approves.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `text-visual-state` is the user asking about?
  - **state** (2 techniques)
    - [TECH-state-guards-and-actions](./references/TECH-state-guards-and-actions.md) — `[guard]` prefix + `/{action}` suffix
    - [TECH-state-machine-legend](./references/TECH-state-machine-legend.md) — `[STATE]` boxes + `-->` / `..>` arrows
  - **every** (1 techniques)
    - [TECH-every-state-has-ingress-egress](./references/TECH-every-state-has-ingress-egress.md) — verification rule for correctness
  - **metrics** (1 techniques)
    - [TECH-metrics-per-transition](./references/TECH-metrics-per-transition.md) — link every edge to a dashboard

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-every-state-has-ingress-egress.md](./references/TECH-every-state-has-ingress-egress.md)**
  - Description: verification rule for correctness
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-metrics-per-transition.md](./references/TECH-metrics-per-transition.md)**
  - Description: link every edge to a dashboard
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-state-guards-and-actions.md](./references/TECH-state-guards-and-actions.md)**
  - Description: `[guard]` prefix + `/{action}` suffix
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-state-machine-legend.md](./references/TECH-state-machine-legend.md)**
  - Description: `[STATE]` boxes + `-->` / `..>` arrows
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-text-visual-state/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. monospaced ASCII state machines + journey storyboards). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-text-visual-state-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## Prerequisites

- **runtime_binaries:** `perl >= 5.10`
- **python_packages:** none (optional `python3` for `bin/amw-ascii-render.py`)
- **npm_packages:** none
- **mcp_servers:** none
- **scripts:** `../../bin/amw-validate-ascii.py` (mandatory), `../../bin/amw-ascii-render.py diagram` (optional)

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator. Rule 1 (context) binds — without a real state list, the diagram is fabrication.
- [SKILL](../amw-ascii-validator/SKILL.md) — validation contract.
- [SKILL](../amw-text-visual-workflows/SKILL.md) — sibling for flowcharts and timelines (not state).
- [SKILL](../amw-text-visual-arch/SKILL.md) — sibling for architecture diagrams.
- [SKILL](../amw-text-visual-cheatsheets/SKILL.md) — sibling for CLI panels.
- [SKILL](../amw-text-visual-retro/SKILL.md) — sibling for retrospectives.
- [SKILL](../amw-ux-flows/SKILL.md) — if the state machine is a user-journey precursor to clickable wireframes, route here after ASCII is approved.
- [SKILL](../amw-diagram-svg/SKILL.md) — natural-language → SVG flow diagrams, when SVG is required.
- [SKILL](../amw-ascii-to-svg/SKILL.md) — convert approved ASCII state machine to SVG.
- `/amw-ascii-to-svg` — slash command for SVG conversion.

## How to invoke via existing commands

No dedicated slash command. Invoke via:

- **Direct skill activation** — phrases like "ASCII state machine for the activation funnel" trigger this skill.
- `/amw-sketch` — when the plan phase involves modelling states before UI.
- `/amw-ascii-to-svg` — after the ASCII state machine is approved.

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
