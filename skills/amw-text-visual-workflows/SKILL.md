---
name: amw-text-visual-workflows
description: ASCII flowcharts and timelines for multi-step workflows (PR lifecycle, launch plan, triage, incident response) — pastes into GitHub PRs, Slack, Notion, terminals. Triggers on "ascii flowchart", "text timeline", "workflow diagram in monospace", "PR-safe flowchart". Does NOT trigger on "design", "diagram", "chart" alone — routes to design-principles / diagram-*. ASCII only; passes amw-validate-ascii.py. Use when producing an ASCII flowchart for a PR. Trigger with "ascii flowchart".
---

# Text-Visual Workflows — ASCII flowcharts and timelines

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Produces ASCII flowcharts and timelines for multi-step workflows — PR lifecycle, launch plan, triage operations, incident response — that paste cleanly into GitHub PRs, issues, Slack, Notion, and terminal output. Three diagram archetypes: branching flowchart, linear timeline with calendar markers, and swimlane parallel-track timeline. Width ceiling: 78 columns terminal, 100 GitHub. Every diagram passes `bin/amw-validate-ascii.py` before delivery. ASCII only — no HTML or SVG output.

## Examples

See [examples](./references/examples.md) for full rendered ASCII of flowchart, timeline, and swimlane.
> [examples.md] Flowchart — branching logic · Timeline — linear sequence with calendar markers · Swimlane timeline — parallel tracks

## Activation

No dedicated slash command. Invoked by the `design-principles` orchestrator during Phase A (low-fi sketch) or Phase B (validated artifact). Skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. Monospaced ASCII pastes unmodified into GitHub PRs, Slack, terminal, Notion. NOT SVG/HTML — route to [ascii-to-svg](../amw-ascii-to-svg/SKILL.md) or [diagram-svg](../amw-diagram-svg/SKILL.md) for pixels.

Scope: **multi-step workflows**. NOT architecture ([arch](../amw-text-visual-arch/SKILL.md)), state machines ([state](../amw-text-visual-state/SKILL.md)), CLI panels ([cheatsheets](../amw-text-visual-cheatsheets/SKILL.md)), or retrospective grids ([retro](../amw-text-visual-retro/SKILL.md)).

## Trigger conditions

- "ASCII flowchart for the release process"
- "text timeline of the launch"
- "monospace workflow I can paste in a PR"
- "chart out the triage flow in ASCII"
- "GitHub-safe flow diagram"
- "terminal-friendly timeline"

Do NOT activate on broad design vocabulary. If the user says "draw a diagram" or "design a flowchart" without the ASCII/text/monospace/PR/terminal framing, that is `design-principles`' job and it may route here or elsewhere.

## Inputs expected

1. **Workflow steps** — the ordered actions, roles involved, and decision points.
2. **Target medium** — GitHub PR, Slack, Notion, terminal log, README. Determines max width (GitHub ≈ 100, Slack ≈ 80, terminal ≈ 78–80).
3. **Metadata to annotate** — owners (`@alice`), tooling (`gh pr checks`), SLA markers (`<24h`), environment tags (`[prod]`).

If any of the three is missing, ask one question to get it. Do not guess — a diagram that fabricates owners or SLAs is a silent trust failure.

## Diagram archetypes

Three shapes — pick one per block. See [examples](./references/examples.md) for full rendered ASCII of each.
> [examples.md] Flowchart — branching logic · Timeline — linear sequence with calendar markers · Swimlane timeline — parallel tracks

1. **Flowchart — branching logic.** Glyphs: `(start)` `(end)`, `[ action ]`, `{ condition? }`, `-->` / `==>` / `~~>`.
2. **Timeline — linear sequence with calendar markers.** `|` anchors dates, `-` fills proportional gap, owner/label below each anchor.
3. **Swimlane — parallel tracks.** One lane per role; `==` fills the active window.

## Glyph and width standards

- **Width ceiling:** 78 columns for terminal output; 100 for GitHub/Notion; never exceed 100.
- **No tab characters.** Use spaces only. Tab rendering varies across Markdown renderers and breaks alignment.
- **Max one blank line between subsections** of the same diagram.
- **No emoji in structural glyphs.** Emoji render at variable width across platforms and will silently misalign the frame on the day the user previews it. For status badges, use `[!]` (warning), `[x]` (done), `[ ]` (todo), `(*)` (current), `*` (highlight).
- **No `▼ ▲ ▶ ◀ ⟶ ⇒`.** These are variable-width in most monospaced fonts. Use `v ^ > <` and `->` / `=>` / `-->` / `==>`.
- **Metadata in parentheses, not inline prose.** `[ Run migrations ] (@db-team, <15min, prod-only)` — not a sentence on the next line.

## Extended connection types

Beyond the core `-->` / `==>` / `~~>`, use the extended vocab when needed. Pick one style per diagram.

| Type | Glyph | Meaning |
|---|---|---|
| sync | `-->` | Sequential step. |
| emphasized | `==>` | Primary path. |
| async | `~~>` | Out-of-band message, fire-and-forget. |
| optional | `..>` | Non-deterministic branch. |
| return | `<--` | Callback / response leg. |
| bidirectional | `<-->` | Handshake. |
| dependency | `---▷` | Build/compile dependency. |
| association | `───` | Plain relation, no direction. |

## Validation gate (MANDATORY)

Every diagram MUST pass `../../bin/amw-validate-ascii.py` before delivery. Flow: draft → `/tmp/amw-tvw-<slug>.txt` → run validator → PASS = present in fenced block; FAIL = apply every `FIX:` hint and re-run until PASS. For strongly-structured flowcharts use `../../bin/amw-ascii-render.py diagram` (alignment guaranteed). See [SKILL](../amw-ascii-validator/SKILL.md) for the JSON schema.

## Instructions

1. Confirm the three inputs (steps, medium, metadata). Ask one question per missing piece, bundled.
2. Pick one archetype — flowchart, timeline, or swimlane. Announce the choice to the user in one sentence ("using a flowchart because your workflow has three decision points").
3. Draft the diagram using the standard glyphs.
4. Run the validation gate. Loop until PASS.
5. Present the diagram inside a fenced code block (no language tag — bare ```), so GitHub renders it in a fixed-width font.
6. Optionally, if the user asked for a canonical stored copy, suggest saving it to `docs/visuals/<name>.txt` in the project repo. Do not write the file unless they approve.

## Technique selection / References

Each TECH file under `./references/` follows the standard TOC: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references.

- [TECH-async-arrow-vocabulary](./references/TECH-async-arrow-vocabulary.md) — `-->` / `==>` / `~~>` / `..>` distinctions
> [TECH-async-arrow-vocabulary.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-flowchart-paren-bracket-glyphs](./references/TECH-flowchart-paren-bracket-glyphs.md) — `(start)` `[action]` `{decision?}`
> [TECH-flowchart-paren-bracket-glyphs.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-metadata-annotation-conventions](./references/TECH-metadata-annotation-conventions.md) — owners, SLAs, tools inline
> [TECH-metadata-annotation-conventions.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-swimlane-parallel-tracks](./references/TECH-swimlane-parallel-tracks.md) — per-role lanes across one timeline
> [TECH-swimlane-parallel-tracks.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-timeline-with-anchors](./references/TECH-timeline-with-anchors.md) — Day/Week markers + labels below
> [TECH-timeline-with-anchors.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [examples](./references/examples.md) — rendered flowchart / timeline / swimlane
> [examples.md] Flowchart — branching logic · Timeline — linear sequence with calendar markers · Swimlane timeline — parallel tracks

<!-- end of references -->

## Completion checklist

Verify all items before reporting complete. FAIL on any triggers a remediation loop.

- Inputs captured verbatim — no silent paraphrasing.
- At least one `TECH-*.md` consulted and cited in the report.
- Output passes Non-negotiables (below).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- Output validated by `bin/amw-validate-ascii.py`.
- Cross-skill hand-offs documented.
- User-facing filename is descriptive English.

## Output

Two outputs per invocation:

1. **Artifact(s)** — monospaced ASCII flowcharts / swimlanes / timelines. Output path is determined by project inference per [project-output-routing](../amw-design-principles/references/project-output-routing.md) (user-supplied path → framework convention → existing `./design/` → `./design/diagrams/` → `/tmp/amw-text-visual-workflows-<slug>/`).
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references

2. **Job-completion report** — `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<slug>_<8-char-hash>.md` containing: Inputs · Method · Artifacts · Checklist · Deviations. Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. **Every artifact MUST be linked from the report.**

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8` (for the validator and ascii-render)
- **python_packages:** none
- **npm_packages:** none
- **mcp_servers:** none
- **scripts:** `../../bin/amw-validate-ascii.py` (mandatory), `../../bin/amw-ascii-render.py` (optional, for JSON-driven flowcharts)

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (Rules 1+2: context + variants).
- [SKILL](../amw-ascii-validator/SKILL.md) — validation contract.
- Siblings: [arch](../amw-text-visual-arch/SKILL.md), [state](../amw-text-visual-state/SKILL.md), [cheatsheets](../amw-text-visual-cheatsheets/SKILL.md), [retro](../amw-text-visual-retro/SKILL.md).
- [SKILL](../amw-ascii-to-svg/SKILL.md) + [SKILL](../amw-diagram-svg/SKILL.md) + `/amw-ascii-to-svg` — for SVG output after ASCII approval.

## How to invoke

No dedicated slash command. Triggered by phrases like "ASCII flowchart of the release workflow". Also `/amw-sketch` (plan phase) and `/amw-ascii-to-svg` (after approval).

## Non-negotiables

- Every diagram passes `../../bin/amw-validate-ascii.py` before delivery. No exceptions.
- 78-column terminal ceiling / 100-column GitHub ceiling. Never exceed 100.
- No tab characters. Ever.
- No variable-width glyphs (`▼ ▲ ▶ ◀ ⟶ ⇒`) or decorative emoji inside structural frames.
- One archetype per diagram. Do not combine flowchart + timeline in a single block — split into two diagrams.
- Every decision branch is labeled. No unlabeled arrows leaving a `{ decision? }` node.
- Every actor / owner / SLA is either present or the user was asked for it. Do not fabricate `@someone` or `<24h`.
- Does NOT emit HTML or SVG. This skill is ASCII only.

## Error Handling

| Failure mode | Recovery |
|---|---|
| Validator reports persistent WIDTH_MISMATCH | The drafting used variable-width glyphs or mixed tabs and spaces. Re-draft with pure ASCII + spaces, re-validate. |
| User wants > 100 columns | Split the workflow into two or three stacked diagrams ("Phase 1", "Phase 2") or collapse micro-steps into super-steps. |
| User wants emoji status badges | Swap to `[!] [x] [ ] (*)` ASCII markers and note the mapping in a caption. |
| Ambiguous intent (workflow vs architecture vs state machine) | Ask one question. Do not guess. Each sibling skill has narrow scope for a reason. |
| Mermaid flowchart requested | Route to `../amw-diagram-architecture/` with a mermaid-passthrough instruction, or to `../amw-ascii-to-svg/` if the user wants a rendered PNG. Not this skill's scope. |
| Diagram too dense to fit within width ceiling | Recommend splitting into a flowchart + a companion timeline, or collapse annotations into footnotes below the block. |
