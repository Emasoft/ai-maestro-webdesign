---
name: amw-text-visual-retro
description: Produces ASCII retrospective grids, milestone timelines, and heatmaps for team retros, experiment readouts, and launch post-mortems — designed to paste cleanly into PR descriptions, GitHub Discussions, or Slack. Triggers on narrow intents — "ASCII retro template", "text-only retrospective grid", "start-stop-continue in ASCII", "experiment readout in monospace", "launch heatmap in text", "post-mortem grid as ASCII". Does NOT trigger on generic "retro", "post-mortem", "review" — those might be documentation tasks. Output is ASCII only; every diagram passes bin/amw-validate-ascii.py before delivery. Use when producing an ASCII retrospective grid, milestone timeline, or heatmap for a team retro or post-mortem. Trigger with "ASCII retro template" or "start-stop-continue in ASCII" phrasing.
version: 0.1.0
---

# Text-Visual Retro — ASCII retrospectives and readouts

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.

## Overview

Produces ASCII retrospective grids, milestone timelines, and heatmaps for team retros, experiment readouts, and launch post-mortems — designed to paste cleanly into PR descriptions, GitHub Discussions, or Slack. Three template archetypes: grid (categories side-by-side), milestone timeline (temporal story), and heatmap (density/frequency readout). Width ceiling 80 columns. Every artifact passes `bin/amw-validate-ascii.py` before delivery.

## Examples

See the `## Template archetypes` section below for minimal examples of a grid, milestone timeline, and heatmap.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during Phase A (as a low-fi ASCII medium for retro grid sketches) or Phase B (when the approved design requires a validated ASCII retrospective artifact). The orchestrator may apply any grid, heatmap, or timeline technique from this skill without command-layer restriction.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. Produces ASCII retrospective artifacts — grids, timelines, heatmaps — for team retros, experiment readouts, and launch post-mortems. Designed to be digestible without slideware, and to drop cleanly into PR descriptions, GitHub Discussions, issue comments, or Slack posts.

Scope is strictly **retrospective / readout visualization**. Not architecture (`../amw-text-visual-arch/`), not state machines (`../amw-text-visual-state/`), not flowcharts (`../amw-text-visual-workflows/`), not CLI panels (`../amw-text-visual-cheatsheets/`). For UX-level evaluation of a shipped page see `../amw-ux-evaluator/`; this skill is for the team-level retro on the whole initiative.

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

This skill supports three shapes. Pick one per artifact — do not merge them.

### 1. Grid (categories side-by-side)

Use for `start/stop/continue`, `went well / needs attention`, `4Ls` (liked / learned / lacked / longed-for), or any two-to-four-category split.

```
+----------------------------+-----------------------------+
| Went Well                  | Needs Attention             |
+----------------------------+-----------------------------+
| Deploy automation shipped  | Flaky tests blocked 3 PRs   |
| @alice, done               | @bob owns fix (due 04-28)   |
|                            |                             |
| +12% DAU post-launch       | Support ticket backlog +40% |
| metric: dau_daily          | @triage-team to prioritize  |
+----------------------------+-----------------------------+
```

### 2. Milestone timeline

Use for launch post-mortems or experiment readouts where the story is temporal.

```
Week 1      Week 2      Week 3      Week 4
|-----------|-----------|-----------|-----------|
Plan        Build       QA          Launch      Post
@alice      @dev-team   @qa-team    @launch     @all

Highlights:
  Week 2 -- migration framework shipped (PR #123)
  Week 3 -- 2 p0 bugs caught (one leaked to prod, see incident #42)
  Week 4 -- soft launch succeeded, +12% DAU

Actions:
  [ ] Fix incident #42 runbook (@oncall, due 04-28)
  [ ] Remove dead migration code (@db-team, due 05-05)
```

### 3. Heatmap

Use for density / frequency readouts — incident count per day, experiment exposure per segment, error rate per endpoint.

Legend for intensity markers (from low to high): `[ ]`  `[~]`  `[+]`  `[++]`  `[!]`. Use exactly this set — anything else breaks the column alignment.

```
              Mon   Tue   Wed   Thu   Fri   Sat   Sun
incidents    [ ]   [~]   [+]   [!]   [++]  [ ]   [ ]
deploys      [+]   [+]   [+]   [+]   [+]   [ ]   [ ]
on-call      [ ]   [ ]   [ ]   [!]   [!]   [ ]   [ ]

Legend: [ ] 0,  [~] 1,  [+] 2-3,  [++] 4-6,  [!] 7+
```

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

Retro grids, timelines, and heatmaps occasionally need arrows — an action item that feeds the next sprint, a root cause that triggered a secondary incident, a before/after pair that shares a relation. Use this vocabulary when the retro doc needs to show relationships alongside the grid. Source: adapted from the diagram-skill-main ASCII-STYLES reference (subsumed into the current skill).

| Type | Glyph | Meaning |
|---|---|---|
| sync | `-->` | Sequential causation ("A caused B"). |
| emphasized | `==>` | Primary / highest-impact causal chain. |
| async | `~~>` | Delayed effect (e.g. bug introduced week 1 surfaced in week 3). |
| optional | `..>` | Conditional / speculative causal link ("may have contributed"). |
| return | `<--` | Feedback loop (retro action became new problem). |
| bidirectional | `<-->` | Mutual reinforcement ("A and B amplified each other"). |
| dependency | `---▷` | Action item depends on another action (blocking relationship). |
| association | `───` | Co-occurrence with no causal claim. |

Retros often benefit from the `return` and `bidirectional` arrows because they surface feedback loops — a fix that created a new problem, two systems amplifying each other. Keep the arrow count low (2–3 max per doc) so the retro stays scannable.

## Action-item rigor

Every action item has three required fields, or it is not an action item:

1. **What.** `[ ] Fix incident #42 runbook`.
2. **Who.** `@oncall` or a named person.
3. **When.** `due 04-28` or `due next retro`.

Entries without one of these are noise. If the user hasn't named a date or owner for a bullet, ask — do not default them to `TBD` unless the user explicitly wants a TBD placeholder row.

## Validation gate (MANDATORY)

Every retro artifact this skill emits MUST pass `../../bin/amw-validate-ascii.py` before being shown to the user.

The flow:

1. Draft the artifact.
2. Write it to `/tmp/amw-tvr-<slug>.txt`.
3. Run `perl ../../bin/amw-validate-ascii.py /tmp/amw-tvr-<slug>.txt`.
4. If PASS → present in a fenced code block.
5. If FAIL → apply every `FIX:` hint, re-run. Loop until PASS.
6. Never present an un-validated artifact.

For heatmaps, `../../bin/amw-ascii-render.py` in `table` mode guarantees column alignment. Strongly recommended when the heatmap has >5 columns. See `../amw-ascii-validator/SKILL.md` for the JSON schema.

## Instructions

1. Confirm the four inputs (categories, highlights, owners, distribution target). One bundled question for missing pieces.
2. Pick an archetype — grid, timeline, or heatmap — based on the retro shape. Announce choice in one sentence.
3. Draft the artifact using the standard glyphs.
4. Verify every action item has what / who / when. Ask for any missing fields before validating.
5. Run the validation gate. Loop until PASS.
6. Present inside a fenced code block (no language tag).
7. Add a `Next Checkpoint` line below — the date the team will review progress on the action items. Ask if not given.
8. Offer to save a canonical copy (e.g. `docs/retros/2026-Q2-sprint-04.md`). Do not write until user approves.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `text-visual-retro` is the user asking about?
  - **grid** (1 techniques)
    - [TECH-grid-side-by-side](./references/TECH-grid-side-by-side.md) — `Went Well` / `Needs Attention` 2-column grid
  - **heatmap** (1 techniques)
    - [TECH-heatmap-intensity-markers](./references/TECH-heatmap-intensity-markers.md) — `[++] [+] [~] [!]` density cells
  - **metric** (1 techniques)
    - [TECH-metric-delta-inline](./references/TECH-metric-delta-inline.md) — `+12% DAU` / `-180ms p99` signed deltas
  - **milestone** (1 techniques)
    - [TECH-milestone-timeline](./references/TECH-milestone-timeline.md) — weekly timeline + highlights + actions
  - **owner** (1 techniques)
    - [TECH-owner-action-items](./references/TECH-owner-action-items.md) — `[ ] <action> (@owner, due YYYY-MM-DD)`

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-grid-side-by-side.md](./references/TECH-grid-side-by-side.md)**
  - Description: `Went Well` / `Needs Attention` 2-column grid
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-heatmap-intensity-markers.md](./references/TECH-heatmap-intensity-markers.md)**
  - Description: `[++] [+] [~] [!]` density cells
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-metric-delta-inline.md](./references/TECH-metric-delta-inline.md)**
  - Description: `+12% DAU` / `-180ms p99` signed deltas
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-milestone-timeline.md](./references/TECH-milestone-timeline.md)**
  - Description: weekly timeline + highlights + actions
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-owner-action-items.md](./references/TECH-owner-action-items.md)**
  - Description: `[ ] <action> (@owner, due YYYY-MM-DD)`
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
- At least one `TECH-*.md` file from `skills/amw-text-visual-retro/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per `../amw-design-principles/ai-slop-avoid.md` (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. monospaced ASCII retro grids / milestone timelines / heatmaps for post-mortems). The output path is determined by **project inference**, NOT hardcoded. See [`../amw-design-principles/references/project-output-routing.md`](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-text-visual-retro-<slug>/`

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
- **scripts:** `../../bin/amw-validate-ascii.py` (mandatory), `../../bin/amw-ascii-render.py table` (optional for heatmaps)

## Resources

- `../amw-design-principles/SKILL.md` — orchestrator.
- `../amw-ascii-validator/SKILL.md` — validation contract.
- `../amw-text-visual-workflows/SKILL.md` — sibling for workflows and timelines (the forward-looking kind).
- `../amw-text-visual-arch/SKILL.md` — sibling for architecture diagrams.
- `../amw-text-visual-state/SKILL.md` — sibling for state machines.
- `../amw-text-visual-cheatsheets/SKILL.md` — sibling for CLI panels.
- `../amw-ux-evaluator/SKILL.md` — per-page UX scoring, for post-launch evaluations that want a rubric rather than a retro.
- `../amw-seo/SKILL.md` — for performance / Core Web Vitals retros specifically.
- `/amw-eval` — slash command for UX evaluation.

## How to invoke via existing commands

No dedicated slash command. Invoke via:

- **Direct skill activation** — phrases like "ASCII start/stop/continue grid for last sprint" trigger this skill.
- `/amw-eval` when the retro is specifically a UX-scoring post-launch readout.

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
