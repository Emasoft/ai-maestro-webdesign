---
name: amw-text-visual-cheatsheets
description: Portable ASCII CLI command panels — tabular cheat sheets for gh, git, kubectl, deploy scripts — with macOS/Linux + Windows variants side by side. Triggers on "ASCII cheat sheet", "CLI reference panel in monospace", "command grid for a README", "gh cheat sheet". Does NOT trigger on "cheat sheet", "guide", "docs" alone — those are docs tasks. ASCII only; passes amw-validate-ascii.py. Use when creating an ASCII CLI cheat sheet. Trigger with "ASCII cheat sheet".
---

# Text-Visual Cheatsheets — ASCII CLI command panels

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Produces portable ASCII CLI command panels — tabular cheat sheets with rows for actions and columns for platforms (macOS/Linux bash/zsh + Windows PowerShell/CMD). Sections split by workflow stage. Destructive commands starred with footnote caveats. Width ceiling: 100 columns for GitHub READMEs, 80 for terminal `--help`. Every panel passes `bin/amw-validate-ascii.py` before delivery. ASCII only — no HTML or SVG output.

## Examples

See the `## Panel format` section below for a minimal standard-layout panel example.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during Phase A (as a low-fi ASCII medium for CLI reference sketches) or Phase B (when the approved design requires a validated ASCII cheat-sheet artifact). The orchestrator may apply any column layout and platform-variant technique from this skill without command-layer restriction.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. Produces ASCII tables that summarize CLI workflows in a glanceable grid, with rows for actions and columns for platforms (macOS/Linux bash/zsh + Windows PowerShell/CMD). Embeds cleanly in READMEs, PR descriptions, CONTRIBUTING guides, and terminal `--help` output.

Scope is strictly **command reference panels**. Not flowcharts (`../amw-text-visual-workflows/`), architecture (`../amw-text-visual-arch/`), state machines (`../amw-text-visual-state/`), or retrospectives (`../amw-text-visual-retro/`). Not generic prose documentation either — if the user wants a paragraph-style guide, this is not the right skill.

## Trigger conditions

- "ASCII cheat sheet for git"
- "CLI command panel for our deploy script"
- "gh reference grid I can put in the README"
- "terminal command table"
- "bash + powershell cheat sheet"
- "panel of common commands in ASCII"

Do NOT activate on broad "make docs" or "write a guide" requests. A multi-paragraph onboarding doc with inline commands is a documentation job, not a cheat-sheet panel.

## Inputs expected

1. **Task categories** — grouping of commands (e.g. `setup`, `daily workflow`, `review`, `deploy`, `rollback`).
2. **Command variants per platform** — macOS/Linux bash/zsh *and* Windows PowerShell/CMD, if cross-platform parity matters. Single-platform is fine; just say so upfront.
3. **Notes on flags, prerequisites, env vars** — what must be installed, what shell-specific escaping applies, which flags are destructive.

If the user gives you commands for one platform only, ask whether they want the other — do not invent Windows variants of POSIX commands by guessing escaping rules.

## Panel format (summary — full spec in TECH-panel-format)

Tabular layout: one action per row, one platform per column, left-aligned,
fixed-width. Columns sized to longest cell + 2 spaces padding. Box corners
`+`, verticals `|`, horizontals `-`. **No tabs, no emoji, no variable-width
glyphs.** Width ceiling: 100 cols (README) / 80 cols (terminal `--help`).

Destructive commands: prefix action with `*`, add footnote below the table.
Multi-workflow command sets: split into separate small panels with
section headers. Placeholders use `<...>` brackets with a legend below.

Footer every panel with: last-verified date, source-doc link, owner tag.

Extended connection-arrow vocabulary (`-->`, `==>`, `~~>`, `..>`, `<--`,
`<-->`, `---▷`, `───`) — use sparingly; if a flow needs > 2 arrows, route
to `../amw-text-visual-workflows/` instead.

See [TECH-panel-format](references/TECH-panel-format.md) for the full
> [TECH-panel-format.md] What it does · When to use · Standard layout · Column alignment · Highlighting critical / destructive commands · Categorizing into sections · Placeholders and context · Glyph and width standards · Extended connection types · Footer metadata · Cross-references
authoring contract (layout / alignment / markers / placeholders / glyph
standards / arrow vocabulary / footer).

## Validation gate (MANDATORY)

Every panel this skill emits MUST pass `../../bin/amw-validate-ascii.py` before being shown to the user.

The flow:

1. Draft the panel.
2. Write it to `/tmp/amw-tvc-<slug>.txt`.
3. Run `python3 ../../bin/amw-validate-ascii.py /tmp/amw-tvc-<slug>.txt`.
4. If PASS → present in a fenced code block.
5. If FAIL → apply every `FIX:` hint, re-run. Loop until PASS.
6. Never present an un-validated panel.

For tabular panels, `../../bin/amw-ascii-render.py` in `table` mode guarantees column alignment by construction. Strongly recommended when the panel has more than 5 columns or more than 10 rows. See [SKILL](../amw-ascii-validator/SKILL.md) for the JSON schema.

## Instructions

1. Confirm the three inputs (categories, platform variants, notes). One bundled question for missing pieces.
2. Group commands into sections; never emit a single monolithic table for mixed workflows.
3. Draft each panel with aligned columns.
4. Add the footer (last-tested date, source link, owner).
5. Run the validation gate per panel. Loop until PASS.
6. Present each panel in its own fenced code block under a section header.
7. If the user intends to commit this to a repo, suggest a canonical location (e.g. `<docs/cli-cheatsheet.md>`). Do not write until approved.

## Technique selection and references

Every technique is a single `TECH-*.md` file under `./references/`. Each
file has the same TOC: *What it does · When to use · How it works ·
Minimal example · Gotchas · Cross-references*. Read only the one whose
topic matches.

- [TECH-category-sections](./references/TECH-category-sections.md) —
> [TECH-category-sections.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  split by workflow stage with section headers.
- [TECH-destructive-command-marker](./references/TECH-destructive-command-marker.md)
> [TECH-destructive-command-marker.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  — `*` prefix + footnote caveat.
- [TECH-legend-and-placeholders](./references/TECH-legend-and-placeholders.md)
> [TECH-legend-and-placeholders.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  — `<branch>` convention + legend caption.
- [TECH-side-by-side-platforms](./references/TECH-side-by-side-platforms.md)
> [TECH-side-by-side-platforms.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  — macOS/Linux vs Windows columns.

<!-- end of references -->

## Completion checklist

Before reporting complete (FAIL on any item triggers a remediation loop):

- Inputs captured verbatim — no silent paraphrasing.
- At least one `TECH-*.md` consulted and cited.
- Output passes `## Non-negotiables`.
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- Every panel passes `bin/amw-validate-ascii.py`.
- Cross-skill hand-offs documented.
- Filename is descriptive English (`gh-cheatsheet.md`, not `out.txt`).

## Output

TWO outputs (ASCII panels + job-completion report). Full contract in
[skill-completion-and-output-contract](../amw-design-principles/references/skill-completion-and-output-contract.md)
and [project-output-routing](../amw-design-principles/references/project-output-routing.md).
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
Report path: `$MAIN_ROOT/reports/webdesigner/<ts>_<slug>_<hash>.md`.
Every artifact MUST be linked from the report.

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8`
- **python_packages:** none
- **npm_packages:** none
- **mcp_servers:** none
- **scripts:** `../../bin/amw-validate-ascii.py` (mandatory), `../../bin/amw-ascii-render.py table` (strongly recommended for >5 columns or >10 rows)

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.
- [SKILL](../amw-ascii-validator/SKILL.md) — validation contract.
- [SKILL](../amw-text-visual-workflows/SKILL.md) — sibling for workflow diagrams.
- [SKILL](../amw-text-visual-arch/SKILL.md) — sibling for architecture.
- [SKILL](../amw-text-visual-state/SKILL.md) — sibling for state machines.
- [SKILL](../amw-text-visual-retro/SKILL.md) — sibling for retrospectives.
- [SKILL](../amw-shadcn-ui/SKILL.md) / [SKILL](../amw-tailwind-4/SKILL.md) — if the user wants the cheat sheet as a styled HTML page instead of ASCII, these are the reference-doc skills to route to.
- `/amw-ascii-to-svg` — if the user wants the panel as an SVG image (rare — usually the ASCII is the point).

## How to invoke via existing commands

No dedicated slash command. Invoke via:

- **Direct skill activation** — phrases like "ASCII cheat sheet for the deploy script" trigger this skill.
- `/amw-sketch` — when the cheat sheet is part of a broader docs planning effort.

## Non-negotiables

- Every panel passes `../../bin/amw-validate-ascii.py` before delivery. No exceptions.
- Column alignment is exact — no off-by-one pipes, no ragged edges.
- 100-column README ceiling; 80-column terminal `--help` ceiling.
- No tabs.
- No emoji or variable-width glyphs.
- Every panel carries a last-tested date and a source link.
- No fabricated commands. If the user has not supplied a Windows variant, ask rather than invent one from pattern-matching.
- Destructive commands are starred and explained in a footnote.
- Does NOT emit HTML or SVG. ASCII only.

## Error Handling

| Failure mode | Recovery |
|---|---|
| Column widths blow past 100 cols because of one long command | Shorten by using a shell variable at the top of the panel (`REPO=org/repo`) and referencing `$REPO` in each cell. Note the variable in the legend. |
| macOS and PowerShell commands diverge wildly for one row | Split into two rows with clear labels (`Clone (macOS)`, `Clone (Windows)`) — consistency is worth more than a forced single row. |
| User only uses one platform | Drop the Windows column. Footer note: `Tested on macOS 14 only.` |
| Commands stale quickly (e.g. evolving `gh` flags) | Put last-tested date in footer; bold in reviewer-checklist: "verify before merging". |
| Destructive command with no safe alternative | Star it, footnote the danger, and include a dry-run flag if the tool supports one (`--dry-run`, `-n`). |
| Commands with secrets or tokens | Never inline tokens. Use a placeholder (`$GH_TOKEN`) and point to a secret manager in the footer. |
| User wants the cheat sheet as a styled web page | This skill produces the ASCII source of truth. Route to `../amw-shadcn-ui/` / `../amw-tailwind-4/` / `../amw-ascii-to-html/` for a styled HTML rendering. |
