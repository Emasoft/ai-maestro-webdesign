---
name: amw-text-visual-cheatsheets
description: Produces portable ASCII CLI command panels — tabular cheat sheets summarizing workflows for tools like gh, git, kubectl, deploy scripts — with macOS/Linux and Windows variants side by side. Triggers on narrow intents — "ASCII cheat sheet", "CLI reference panel in monospace", "command grid for pasting in a README", "gh cheat sheet", "terminal command panel". Does NOT trigger on generic "cheat sheet", "guide", "docs" — those are documentation tasks for general skills. Output is ASCII only; every panel passes bin/amw-validate-ascii.py before delivery. Use when creating a portable ASCII CLI cheat-sheet panel for a README or PR description. Trigger with "ASCII cheat sheet" or "CLI reference panel in monospace" phrasing.
version: 0.1.0
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

Do NOT activate on broad "make docs" or "write a guide" requests. A multi-paragraph onboarding doc with embedded commands is a documentation task, not a cheat-sheet panel.

## Inputs expected

1. **Task categories** — grouping of commands (e.g. `setup`, `daily workflow`, `review`, `deploy`, `rollback`).
2. **Command variants per platform** — macOS/Linux bash/zsh *and* Windows PowerShell/CMD, if cross-platform parity matters. Single-platform is fine; just say so upfront.
3. **Notes on flags, prerequisites, env vars** — what must be installed, what shell-specific escaping applies, which flags are destructive.

If the user gives you commands for one platform only, ask whether they want the other — do not invent Windows variants of POSIX commands by guessing escaping rules.

## Panel format

### Standard layout

Table with fixed-width columns, one action per row, one platform per column:

```
+------------------+--------------------------------+---------------------------------------+
| Action           | macOS / Linux                  | Windows (PowerShell)                  |
+------------------+--------------------------------+---------------------------------------+
| Clone            | gh repo clone org/repo ~/code  | gh repo clone org/repo $HOME\code     |
| Create PR        | gh pr create --fill            | gh pr create --fill                   |
| *Force push      | git push --force-with-lease    | git push --force-with-lease           |
| Check CI         | gh pr checks --watch           | gh pr checks --watch                  |
+------------------+--------------------------------+---------------------------------------+
```

### Column alignment

- Left-align every column.
- Column widths: longest cell plus 2 spaces of padding. Never wrap a command mid-cell.
- Headers match column widths with `-` fill in the separator row.

### Highlighting critical / destructive commands

- Prefix the action name with `*` — e.g. `*Force push`, `*Drop database`, `*Reset local branch`.
- Add a footnote line below the table per starred action:

```
* Force push: rewrites remote history. Use `--force-with-lease` to avoid
  clobbering teammates' commits. Never on `main` / `master` / `release/*`.
```

- For non-destructive but non-obvious commands, use a `(note)` suffix and expand in the footer.

### Categorizing into sections

If the command set spans multiple workflows (setup vs daily vs deploy), split into **separate small panels** with a header line per section:

```
### Setup (one-time)

+------------------+---------------------------+---------------------------+
| Install gh       | brew install gh           | winget install gh         |
| Authenticate     | gh auth login             | gh auth login             |
+------------------+---------------------------+---------------------------+

### Daily workflow

+------------------+---------------------------+---------------------------+
| Sync main        | git fetch && git pull     | git fetch; git pull       |
| Create branch    | git checkout -b feat/x    | git checkout -b feat/x    |
+------------------+---------------------------+---------------------------+
```

A single monolithic 20-row panel is nearly unreadable. Two five-row panels with clear headers is always better.

### Placeholders and context

- Explicit placeholder syntax: `<branch>`, `<env>`, `<issue-id>`. Consistent `<...>` brackets.
- Legend below the panel listing every placeholder: `<branch> = the feature branch, e.g. feat/order-refactor`.
- Note env vars inline: `GH_TOKEN=$(op read op://...) gh pr create`.

## Glyph and width standards

- **Width ceiling:** 100 columns for GitHub READMEs; 80 for terminal `--help` embedding. Drop to 80 when in doubt.
- **Box corners:** `+`, verticals `|`, horizontals `-`.
- **No tabs.** Spaces only.
- **No variable-width glyphs.** No emoji. Use `*` for "important" and `(note)` for "has a footnote".
- **Consistent quoting.** Use double quotes in shell commands when a variable expands; escape PowerShell variables as `$env:USERPROFILE` not `%USERPROFILE%` unless the target shell is CMD.

## Extended connection types

Cheat sheets are mostly tabular, but occasionally a panel needs an inline command-flow annotation ("command A pipes to command B", "set-env then run") or a cross-reference arrow (`see also ---▷ ...`). Use this vocabulary when the panel needs to show relationships alongside the command grid. Source: adapted from the diagram-skill-main ASCII-STYLES reference (subsumed into the current skill).

| Type | Glyph | Meaning |
|---|---|---|
| sync | `-->` | Command A chains into command B (sequential). |
| emphasized | `==>` | Primary / most-used command path; single accented arrow per panel. |
| async | `~~>` | Command fires a background job (non-blocking). |
| optional | `..>` | Optional follow-up (only if previous succeeded). |
| return | `<--` | Reverse command (undo / rollback reference). |
| bidirectional | `<-->` | Two-way sync command (e.g. `git pull <--> git push`). |
| dependency | `---▷` | "See also" cross-reference to another panel / command. |
| association | `───` | Plain grouping / shared context indicator. |

Use sparingly — cheat sheets are read by scanning columns, not by tracing arrows. When a command flow has more than 2 arrows in it, promote to `text-visual-workflows` instead.

## Footer metadata

End every panel with:

- A last-tested date: `Last verified: 2026-04-22 on macOS 14 / Windows 11.`
- Link(s) to source docs if applicable: `See: https://cli.github.com/manual/`.
- Owner / reviewer tag if cross-team: `Owner: @platform-team.`

Stale cheat sheets are worse than no cheat sheet. The footer forces accountability.

## Validation gate (MANDATORY)

Every panel this skill emits MUST pass `../../bin/amw-validate-ascii.py` before being shown to the user.

The flow:

1. Draft the panel.
2. Write it to `/tmp/amw-tvc-<slug>.txt`.
3. Run `perl ../../bin/amw-validate-ascii.py /tmp/amw-tvc-<slug>.txt`.
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

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `text-visual-cheatsheets` is the user asking about?
  - **category** (1 techniques)
    - [TECH-category-sections](./references/TECH-category-sections.md) — split by workflow stage with section headers
  - **destructive** (1 techniques)
    - [TECH-destructive-command-marker](./references/TECH-destructive-command-marker.md) — `*` prefix + footnote caveat
  - **legend** (1 techniques)
    - [TECH-legend-and-placeholders](./references/TECH-legend-and-placeholders.md) — `<branch>` convention + legend caption
  - **side** (1 techniques)
    - [TECH-side-by-side-platforms](./references/TECH-side-by-side-platforms.md) — macOS/Linux vs Windows columns

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-category-sections.md](./references/TECH-category-sections.md)**
  - Description: split by workflow stage with section headers
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-destructive-command-marker.md](./references/TECH-destructive-command-marker.md)**
  - Description: `*` prefix + footnote caveat
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-legend-and-placeholders.md](./references/TECH-legend-and-placeholders.md)**
  - Description: `<branch>` convention + legend caption
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-side-by-side-platforms.md](./references/TECH-side-by-side-platforms.md)**
  - Description: macOS/Linux vs Windows columns
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
- At least one `TECH-*.md` file from `skills/amw-text-visual-cheatsheets/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. monospaced ASCII CLI cheat-sheet panels for READMEs and wiki pages). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` or `./docs/` created fresh)
   - Last-resort scratch: `/tmp/amw-text-visual-cheatsheets-<slug>/`

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
