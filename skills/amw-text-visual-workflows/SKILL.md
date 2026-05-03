---
name: amw-text-visual-workflows
description: Produces ASCII flowcharts and timelines for multi-step workflows — PR lifecycle, launch plan, triage ops, incident response — that paste cleanly into GitHub PRs, issues, Slack, Notion, and terminal output. Triggers on narrow intents — "ascii flowchart", "text timeline", "workflow diagram in monospace", "PR-safe flowchart", "paste-into-GitHub flow diagram", "timeline for a comment". Does NOT trigger on generic "design", "diagram", "chart", "draw a flow" — those belong to design-principles / diagram-* / ascii-to-svg. Output is ASCII only; every diagram passes bin/amw-validate-ascii.py before delivery. Use when producing an ASCII flowchart or timeline for a PR, launch plan, or incident-response workflow. Trigger with "ascii flowchart", "text timeline", or "PR-safe flowchart" phrasing.
version: 0.1.0
---

# Text-Visual Workflows — ASCII flowcharts and timelines

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).

## Overview

Produces ASCII flowcharts and timelines for multi-step workflows — PR lifecycle, launch plan, triage operations, incident response — that paste cleanly into GitHub PRs, issues, Slack, Notion, and terminal output. Three diagram archetypes: branching flowchart, linear timeline with calendar markers, and swimlane parallel-track timeline. Width ceiling: 78 columns terminal, 100 GitHub. Every diagram passes `bin/amw-validate-ascii.py` before delivery. ASCII only — no HTML or SVG output.

## Examples

See the `## Diagram archetypes` section below for minimal skeleton examples of a flowchart, timeline, and swimlane.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during Phase A (as a low-fi ASCII medium for workflow/timeline sketches) or Phase B (when the approved design requires a validated workflow ASCII artifact). The orchestrator may apply any flowchart, timeline, or swimlane technique from this skill without command-layer restriction.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT. This is a text-visualization executor, not a diagram renderer. It produces monospaced ASCII that a user can paste unmodified into a GitHub PR body, a Slack message, a terminal transcript, or a Notion/Markdown doc. It does not emit SVG or HTML — if the user wants pixels, route them to `../amw-ascii-to-svg/` or `../amw-diagram-svg/` instead.

Scope is strictly **multi-step workflows** — a sequence of actions, a timeline of events, or a branching flow with decision points. Architecture diagrams go to `../amw-text-visual-arch/`. State machines go to `../amw-text-visual-state/`. CLI panels go to `../amw-text-visual-cheatsheets/`. Retrospective grids go to `../amw-text-visual-retro/`.

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

This skill supports three shapes. Pick one — do not mix two into a single block.

### 1. Flowchart — branching logic

Use when the workflow has decisions with yes/no or multi-way branches.

Glyphs:

- Start / End: `(start)` `(end)`
- Process step: `[ action ]`
- Decision: `{ condition? }`
- Sync arrow: `-->`
- Emphasized arrow: `==>`
- Async / eventual arrow: `~~>`

Skeleton:

```
(start)
  |
  v
[ Open PR ]
  |
  v
{ Checks pass? }
  |       |
  yes     no
  |       |
  v       v
[ Review] [ Fix + push ]
  |           |
  |           '--> back to checks
  v
[ Merge ]
  |
  v
(end)
```

### 2. Timeline — linear sequence with calendar markers

Use when time ordering and calendar position are the point (launch schedules, onboarding weeks, migration phases).

Skeleton:

```
Day 0     Day 3     Day 7     Day 14
|---------|---------|---------|
Plan      Build     QA        Launch
@alice    @bob      @cara     @dana
```

The vertical bars `|` mark the anchor dates; horizontal dashes `-` fill the gap proportional to the interval, not to character count. Annotate each anchor with owner / phase label underneath.

### 3. Swimlane timeline — parallel tracks

Use when multiple roles / teams are working in parallel and you want to show who owns what over time.

Skeleton:

```
          Day 0     Day 3     Day 7     Day 14
Dev       |==build==|==test==|
QA                  |==plan==|==run====|
Launch                                 |==go=|
```

Each row is one lane; `==` fills the active window for that lane on that date range.

## Glyph and width standards

- **Width ceiling:** 78 columns for terminal output; 100 for GitHub/Notion; never exceed 100.
- **No tab characters.** Use spaces only. Tab rendering varies across Markdown renderers and breaks alignment.
- **Max one blank line between subsections** of the same diagram.
- **No emoji in structural glyphs.** Emoji render at variable width across platforms and will silently misalign the frame on the day the user previews it. For status badges, use `[!]` (warning), `[x]` (done), `[ ]` (todo), `(*)` (current), `*` (highlight).
- **No `▼ ▲ ▶ ◀ ⟶ ⇒`.** These are variable-width in most monospaced fonts. Use `v ^ > <` and `->` / `=>` / `-->` / `==>`.
- **Metadata in parentheses, not inline prose.** `[ Run migrations ] (@db-team, <15min, prod-only)` — not a sentence on the next line.

## Extended connection types

When a flowchart or timeline needs to show response paths, handshakes, non-deterministic transitions, or plain relations alongside the core `-->` / `==>` / `~~>` vocabulary, use this extended set. Pick one style per diagram; do not mix within a single figure. Source: adapted from the diagram-skill-main ASCII-STYLES reference (subsumed into the current skill).

| Type | Glyph | Meaning |
|---|---|---|
| sync | `-->` | Synchronous sequential step. |
| emphasized | `==>` | Primary / high-traffic path; single accented arrow per diagram. |
| async | `~~>` | Async event, out-of-band message, fire-and-forget. |
| optional | `..>` | Dotted conditional transition (used only when the branch is non-deterministic). |
| return | `<--` | Callback / response leg (useful in workflows that double as informal sequence diagrams). |
| bidirectional | `<-->` | Handshake step — both sides exchange data. |
| dependency | `---▷` | Build/compile dependency (hollow triangle head). |
| association | `───` | Plain relation, no direction (workflow phase grouping). |

## Validation gate (MANDATORY)

Every diagram this skill emits MUST pass `../../bin/amw-validate-ascii.py` before being shown to the user.

The flow:

1. Draft the diagram in a scratch buffer.
2. Write it to `/tmp/amw-tvw-<slug>.txt`.
3. Run `perl ../../bin/amw-validate-ascii.py /tmp/amw-tvw-<slug>.txt`.
4. If PASS → present in a fenced code block.
5. If FAIL → apply every `FIX:` hint emitted, re-run. Loop until PASS.
6. Never present an un-validated diagram.

For strongly-structured flowcharts (many branches, nested decisions) prefer `../../bin/amw-ascii-render.py` with the `diagram` mode — the renderer guarantees alignment by construction. See [SKILL](../amw-ascii-validator/SKILL.md) for the JSON schema.

## Instructions

1. Confirm the three inputs (steps, medium, metadata). Ask one question per missing piece, bundled.
2. Pick one archetype — flowchart, timeline, or swimlane. Announce the choice to the user in one sentence ("using a flowchart because your workflow has three decision points").
3. Draft the diagram using the standard glyphs.
4. Run the validation gate. Loop until PASS.
5. Present the diagram inside a fenced code block (no language tag — bare ```), so GitHub renders it in a fixed-width font.
6. Optionally, if the user asked for a canonical stored copy, suggest saving it to `docs/visuals/<name>.txt` in the project repo. Do not write the file unless they approve.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `text-visual-workflows` is the user asking about?
  - **async** (1 techniques)
    - [TECH-async-arrow-vocabulary](./references/TECH-async-arrow-vocabulary.md) — `-->` / `==>` / `~~>` / `..>` distinctions
  - **flowchart** (1 techniques)
    - [TECH-flowchart-paren-bracket-glyphs](./references/TECH-flowchart-paren-bracket-glyphs.md) — `(start)` `[action]` `{decision?}`
  - **metadata** (1 techniques)
    - [TECH-metadata-annotation-conventions](./references/TECH-metadata-annotation-conventions.md) — owners, SLAs, tools inline
  - **swimlane** (1 techniques)
    - [TECH-swimlane-parallel-tracks](./references/TECH-swimlane-parallel-tracks.md) — per-role lanes across one timeline
  - **timeline** (1 techniques)
    - [TECH-timeline-with-anchors](./references/TECH-timeline-with-anchors.md) — Day/Week markers + labels below

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-async-arrow-vocabulary.md](./references/TECH-async-arrow-vocabulary.md)**
  - Description: `-->` / `==>` / `~~>` / `..>` distinctions
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-flowchart-paren-bracket-glyphs.md](./references/TECH-flowchart-paren-bracket-glyphs.md)**
  - Description: `(start)` `[action]` `{decision?}`
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-metadata-annotation-conventions.md](./references/TECH-metadata-annotation-conventions.md)**
  - Description: owners, SLAs, tools inline
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-swimlane-parallel-tracks.md](./references/TECH-swimlane-parallel-tracks.md)**
  - Description: per-role lanes across one timeline
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-timeline-with-anchors.md](./references/TECH-timeline-with-anchors.md)**
  - Description: Day/Week markers + labels below
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
- At least one `TECH-*.md` file from `skills/amw-text-visual-workflows/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. monospaced ASCII flowcharts / swimlanes / timelines for PRs and issue threads). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-text-visual-workflows-<slug>/`

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

- **runtime_binaries:** `perl >= 5.10` (for the validator)
- **python_packages:** none (optional `python3` if using `bin/amw-ascii-render.py`)
- **npm_packages:** none
- **mcp_servers:** none
- **scripts:** `../../bin/amw-validate-ascii.py` (mandatory), `../../bin/amw-ascii-render.py` (optional, for JSON-driven flowcharts)

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator. Rules 1 and 2 (context, variants) apply; for a flowchart, "variants" means offering a flowchart shape vs a timeline shape vs a swimlane if the intent is ambiguous.
- [SKILL](../amw-ascii-validator/SKILL.md) — the validation contract.
- [SKILL](../amw-text-visual-arch/SKILL.md) — sibling skill for architecture diagrams (not workflows).
- [SKILL](../amw-text-visual-state/SKILL.md) — sibling skill for state machines (user journey states, retention loops).
- [SKILL](../amw-text-visual-cheatsheets/SKILL.md) — sibling skill for CLI command panels.
- [SKILL](../amw-text-visual-retro/SKILL.md) — sibling skill for retrospectives and experiment readouts.
- [SKILL](../amw-ascii-to-svg/SKILL.md) — if the user wants the same diagram as an SVG instead of ASCII, route here after they approve the ASCII draft.
- [SKILL](../amw-diagram-svg/SKILL.md) — natural-language → SVG diagram primitives, for when ASCII is not the output format.
- `/amw-ascii-to-svg` — slash command that converts an approved ASCII diagram to SVG. No dedicated slash command for this skill — the orchestrator or `/amw-sketch` routes here when the intent is text-only.

## How to invoke via existing commands

This skill does NOT ship its own slash command. Invoke it via:

- **Direct skill activation** — user phrases like "ASCII flowchart of the release workflow" trigger this skill directly through the orchestrator.
- `/amw-sketch` — when the user is in the ASCII-first plan phase and asks for a workflow visualization (this skill borrows the validation contract and output format).
- `/amw-ascii-to-svg` — after a workflow ASCII is approved, convert it to SVG for publication in a non-monospace surface.

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
