---
name: amw-text-visual-retro
description: ASCII retrospective grids, milestone timelines, heatmaps for team retros, experiment readouts, launch post-mortems — pastes into PRs, GitHub Discussions, Slack. Triggers on "ASCII retro template", "text retrospective grid", "start-stop-continue in ASCII", "post-mortem grid as ASCII". Does NOT trigger on "retro", "post-mortem", "review" alone — those are docs tasks. ASCII only; passes amw-validate-ascii.py. Use when producing an ASCII retro grid or timeline. Trigger with "ASCII retro template".
---

# Text-Visual Retro — ASCII retrospectives and readouts

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Produces ASCII retrospective grids, milestone timelines, and heatmaps for team retros, experiment readouts, and launch post-mortems — designed to paste cleanly into PR descriptions, GitHub Discussions, or Slack. Three template archetypes: grid (categories side-by-side), milestone timeline (temporal story), and heatmap (density/frequency readout). Width ceiling 80 columns. Every artifact passes `bin/amw-validate-ascii.py` before delivery.

## Examples

See [examples](./references/examples.md) for full rendered ASCII of grid, milestone timeline, and heatmap.

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during Phase A (low-fi sketch) or Phase B (validated artifact). Skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. Produces ASCII retrospective artifacts — grids, timelines, heatmaps — for team retros, experiment readouts, and launch post-mortems. Drops cleanly into PR descriptions, GitHub Discussions, Slack.

Scope is strictly **retrospective / readout visualization**. NOT architecture ([arch](../amw-text-visual-arch/SKILL.md)), state machines ([state](../amw-text-visual-state/SKILL.md)), flowcharts ([workflows](../amw-text-visual-workflows/SKILL.md)), or CLI panels ([cheatsheets](../amw-text-visual-cheatsheets/SKILL.md)). For per-page UX evaluation see [ux-evaluator](../amw-ux-evaluator/SKILL.md).

## Trigger conditions

- "ASCII retro template for last sprint"
- "start / stop / continue grid in text"
- "experiment readout in ASCII"
- "launch post-mortem grid as text"
- "went well / needs attention table in monospace"
- "heatmap of this week's incidents in ASCII"

Do NOT activate on broad "write up the retro" — that is a documentation task that may include prose, timelines, and action items that exceed this skill's scope. This skill produces the *visual artefact* (grid / timeline / heatmap), not the surrounding prose.

## Inputs expected

1. **Retro categories** — e.g. `Went Well`, `Needs Attention`, `Risks`, `Next Bets`, `Metrics`. Or a template name (`start/stop/continue`, `4Ls`, `mad/sad/glad`, `KPT`).
2. **Highlights and quantitative results** — short bullets per category, and key metric deltas (e.g. `+12% DAU`, `p99 latency -180ms`, `2 incidents this sprint`).
3. **Owners and follow-up items** — action items per bullet with `@owner` and optional due date.
4. **Distribution target** — PR description, GitHub Discussion, Slack, Notion, canonical project doc. Determines width and format.

If any is missing, ask one bundled question. Retros that invent action items or fabricate owners erode team trust; ask rather than guess.

## Template archetypes

Three shapes — pick one per artifact, do not merge them. See [examples](./references/examples.md) for full rendered ASCII of each.

1. **Grid (categories side-by-side)** — `start/stop/continue`, `went well / needs attention`, `4Ls`, or any 2-4 category split.
2. **Milestone timeline** — launch post-mortems or experiment readouts where the story is temporal (weeks → highlights → actions).
3. **Heatmap** — density / frequency readouts. Intensity markers (low→high): `[ ]`  `[~]`  `[+]`  `[++]`  `[!]`. Use exactly this set — anything else breaks alignment.

## Glyph and width standards

- **Width ceiling:** 80 columns (pastes cleanly in any surface — README, PR, Slack, terminal).
- **Box corners:** `+`, verticals `|`, horizontals `-`.
- **No tabs.** Spaces only.
- **Heatmap markers:** `[ ]`  `[~]`  `[+]`  `[++]`  `[!]` — exactly this set, each rendered as a 3-char token so columns line up. No emoji.
- **No variable-width glyphs** (`▼ ▲ ▶ ◀ ⟶ ⇒`).
- **Metric format:** `+12% DAU`, `-180ms p99`, `2 incidents`. Prefix sign always. No rounding to suspiciously clean numbers.
- **Owner format:** `@name` consistently. If the team is `@platform-team`, not `platform-team`.
- **Due date format:** ISO-8601 short (`2026-04-28`) or kebab-short (`04-28`) — be consistent within a single artifact.

## Extended connection types

When the retro shows causal relationships, use this arrow vocab. Pick one style per doc; keep count ≤ 2-3.

| Type | Glyph | Meaning |
|---|---|---|
| sync | `-->` | Sequential causation. |
| emphasized | `==>` | Primary causal chain. |
| async | `~~>` | Delayed effect (bug introduced week 1 surfaced in week 3). |
| optional | `..>` | Speculative causal link. |
| return | `<--` | Feedback loop. |
| bidirectional | `<-->` | Mutual reinforcement. |
| dependency | `---▷` | Action depends on another action. |
| association | `───` | Co-occurrence, no causal claim. |

## Action-item rigor

Every action item has three required fields, or it is not an action item:

1. **What.** `[ ] Fix incident #42 runbook`.
2. **Who.** `@oncall` or a named person.
3. **When.** `due 04-28` or `due next retro`.

Entries without one of these are noise. If the user hasn't named a date or owner for a bullet, ask — do not default them to `TBD` unless the user explicitly wants a TBD placeholder row.

## Validation gate (MANDATORY)

Every artifact MUST pass `../../bin/amw-validate-ascii.py` before delivery. Flow: draft → write to `/tmp/amw-tvr-<slug>.txt` → run validator → PASS = present in fenced block; FAIL = apply every `FIX:` hint and re-run until PASS. Never present un-validated output. For heatmaps with >5 columns use `../../bin/amw-ascii-render.py table` (alignment guaranteed by construction). See [SKILL](../amw-ascii-validator/SKILL.md) for the JSON schema.

## Instructions

1. Confirm the four inputs (categories, highlights, owners, distribution target). One bundled question for missing pieces.
2. Pick an archetype — grid, timeline, or heatmap — based on the retro shape. Announce choice in one sentence.
3. Draft the artifact using the standard glyphs.
4. Verify every action item has what / who / when. Ask for any missing fields before validating.
5. Run the validation gate. Loop until PASS.
6. Present inside a fenced code block (no language tag).
7. Add a `Next Checkpoint` line below — the date the team will review progress on the action items. Ask if not given.
8. Offer to save a canonical copy (e.g. `<docs/retros/2026-Q2-sprint-04.md>`). Do not write until user approves.

## Technique selection / References

Each TECH file under `./references/` follows the standard TOC: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references.

- [TECH-grid-side-by-side](./references/TECH-grid-side-by-side.md) — `Went Well` / `Needs Attention` 2-column grid
> [TECH-grid-side-by-side.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-heatmap-intensity-markers](./references/TECH-heatmap-intensity-markers.md) — `[++] [+] [~] [!]` density cells
> [TECH-heatmap-intensity-markers.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-metric-delta-inline](./references/TECH-metric-delta-inline.md) — `+12% DAU` / `-180ms p99` signed deltas
> [TECH-metric-delta-inline.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-milestone-timeline](./references/TECH-milestone-timeline.md) — weekly timeline + highlights + actions
> [TECH-milestone-timeline.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-owner-action-items](./references/TECH-owner-action-items.md) — `[ ] <action> (@owner, due YYYY-MM-DD)`
> [TECH-owner-action-items.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [examples](./references/examples.md) — three rendered template archetypes
> [examples.md] Grid (categories side-by-side) · Milestone timeline · Heatmap

<!-- end of references -->

## Completion checklist

Verify all items before reporting complete. FAIL on any triggers a remediation loop.

- Inputs captured verbatim — no silent paraphrasing.
- At least one `TECH-*.md` consulted and cited in the report.
- Output passes Non-negotiables (below).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- Output rendered/validated by `bin/amw-validate-ascii.py`.
- Cross-skill hand-offs documented.
- User-facing filename is descriptive English.

## Output

Two outputs per invocation:

1. **Artifact(s)** — monospaced ASCII retro grids / milestone timelines / heatmaps. Output path is determined by project inference per [project-output-routing](../amw-design-principles/references/project-output-routing.md) (user-supplied path → framework convention → existing `./design/` → `./design/diagrams/` → `/tmp/amw-text-visual-retro-<slug>/`).
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references

2. **Job-completion report** — `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<slug>_<8-char-hash>.md` containing: Inputs · Method · Artifacts · Checklist · Deviations. Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. **Every artifact MUST be linked from the report.**

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8`
- **python_packages:** none
- **npm_packages:** none
- **mcp_servers:** none
- **scripts:** `../../bin/amw-validate-ascii.py` (mandatory), `../../bin/amw-ascii-render.py table` (optional for heatmaps)

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.
- [SKILL](../amw-ascii-validator/SKILL.md) — validation contract.
- Siblings: [workflows](../amw-text-visual-workflows/SKILL.md), [arch](../amw-text-visual-arch/SKILL.md), [state](../amw-text-visual-state/SKILL.md), [cheatsheets](../amw-text-visual-cheatsheets/SKILL.md).
- [SKILL](../amw-ux-evaluator/SKILL.md) + `/amw-eval` — per-page UX scoring (post-launch rubric).
- [SKILL](../amw-seo/SKILL.md) — Core Web Vitals retros.

## How to invoke

No dedicated slash command. Triggered by phrases like "ASCII start/stop/continue grid for last sprint". Also `/amw-eval` when the retro is a UX-scoring post-launch readout.

## Non-negotiables

- Every artifact passes `../../bin/amw-validate-ascii.py` before delivery. No exceptions.
- 80-column width ceiling.
- No tabs.
- No emoji or variable-width glyphs. Heatmap markers are exactly `[ ]  [~]  [+]  [++]  [!]`.
- Every action item has what / who / when. No orphan bullets.
- No fabricated owners, metrics, or dates. Ask the user for anything not supplied.
- Metric format always includes a sign. No rounding-to-clean-numbers fabrication.
- Every artifact ends with a `Next Checkpoint` line.
- Does NOT emit HTML or SVG. ASCII only.

## Error Handling

| Failure mode | Recovery |
|---|---|
| User pastes raw retro notes in prose form | Extract into bullets, classify by category, then ask user to confirm the classification before drafting the grid. |
| Heatmap has >10 columns (e.g. 30 days) | Collapse into weeks or 3-day buckets; add a footnote with the bucket definition. |
| Action items all have the same owner | Flag this — real retros distribute ownership. Ask if the team wants to redistribute before committing. |
| User wants a retro artifact without any action items ("just a readout") | Drop the actions section but keep `Next Checkpoint` — even a pure readout deserves a decision point. |
| Retro spans multiple teams with conflicting tones ("we shipped X" vs "we failed at Y") | Emit two stacked grids — one per team — rather than trying to reconcile into a single table. |
| Sensitive / confidential content (incident root causes, personal performance) | Ask the user explicitly whether this artifact is for a public PR or an internal doc; for internal, prefix every bullet with `[internal]` and include the distribution-target note in the footer. |
| User wants the retro as a styled HTML page | This skill produces the ASCII source of truth. Route to `../amw-ascii-to-html/` after approval. |
