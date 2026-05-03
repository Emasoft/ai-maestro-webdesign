---
name: amw-ascii-diagrams-reference
description: Professional ASCII diagrams for code comments, docs, ADRs, and technical communication using the classic `+--+` / `|` / `-` character set — flowchart conventions, state machines, tree / hierarchy forms, data-structure layouts, network topologies, sequence diagrams, tables, and annotation patterns. Triggers on narrow technical intents only — "ASCII flowchart in a code comment", "state-machine diagram for this protocol", "tree view of this directory", "packet layout diagram", "network topology ASCII", "sequence diagram in ASCII", "before/after ASCII comparison", "annotate these bit fields". Does NOT trigger on broad design vocabulary ("design", "UI", "landing page", "mockup", "wireframe") — those belong to the `design-principles` orchestrator. Use when authoring technical ASCII diagrams for code comments, docs, or ADRs. Trigger with /amw-create-or-modify-ascii-diagram.
version: 0.1.0
---

# ASCII Diagrams Reference

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor. Narrow technical triggers only — the orchestrator routes here when the user wants a text-based diagram for code comments / READMEs / ADRs / design docs, rendered with the classic `+--+ | -` ASCII character set.

## Overview

Reference library of battle-tested ASCII diagram forms for code comments, READMEs, ADRs, and technical documentation — distilled from the CHI'24 paper on ASCII drawings. Routes to the closest pattern file under `references/` and adapts it to the caller's identifiers.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked by the `design-principles` orchestrator during **Phase B** when the user has approved an ASCII-first plan and the deliverable is a technical diagram (code comments, ADRs, READMEs). May also be invoked directly by users who already know they want a classic `+--+` ASCII reference without going through the plan phase.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**OUTPUT.** Reference library of battle-tested ASCII diagram forms distilled from the CHI'24 paper *"Taking ASCII Drawings Seriously"* (2156 diagrams mined from Linux, Chromium, LLVM, TensorFlow). This skill does not invent new forms — it routes the caller to the closest reference file under `references/`, then adapts the pattern to the caller's identifiers.

Use this skill when:

- The diagram will live inside a source-file comment (`//`, `#`, `*`) where UTF-8 glyphs render poorly or inconsistently.
- The diagram will ship in an ADR / README / PR body where classic ASCII survives diffs, blame, and copy-paste across tools.
- The target audience reads via tools that may not render Unicode box-drawing characters (old terminals, email clients, some GitHub rendering paths).

For Unicode rounded-corner box diagrams (terminal-first, modern look) use `../amw-box-diagram/` instead. For wireframe layouts (framed UI mockups) use `../amw-ascii-sketch/`.

## Trigger conditions

- "ASCII flowchart in a code comment"
- "state-machine diagram for this protocol"
- "tree view of this directory / class hierarchy"
- "packet layout diagram", "struct layout ASCII"
- "network topology in ASCII"
- "sequence diagram in ASCII"
- "before/after ASCII comparison"
- "annotate these bit fields"
- "table of HTTP status codes as ASCII"
- "DAG / directed graph as ASCII"

Do **not** activate on broad "design", "UI", "mockup", "wireframe", "landing page", "prototype", "slide", "deck" — those route to `../amw-design-principles/` and its plan-phase executor `../amw-ascii-sketch/`.

## Core principles (inherit from the source paper)

### 1. Alignment is everything
Treat monospace text as a grid. Align every vertical line, keep horizontal spans consistent, and fix misalignment **before** emission. The validator (below) enforces this.

### 2. Prefer plain ASCII that renders everywhere
Basic ASCII characters (`+ - | > < ^ v`) render in any font, terminal, or tool. Use Unicode box-drawing (`─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`) **only** when the target context is a GitHub-rendered README / modern terminal — for code comments, stick to ASCII. When in doubt, route to this skill (ASCII) not `../amw-box-diagram/` (Unicode).

### 3. Keep it minimal
Show the essential structure, not every detail. If the diagram grows beyond ~30 lines, split it or simplify it.

### 4. Connect to the code
Reference real identifiers, constants, and expressions from the surrounding code so the reader can jump between the diagram and the implementation.

### 5. Show what text cannot
Diagram spatial relationships (hierarchies, networks, layouts, branched flows). Do not diagram relationships plain prose or linear code already conveys.

## Character cheat-sheet

| Purpose | Characters | Notes |
|---------|-----------|-------|
| Horizontal lines | `-` `=` | `=` for emphasis / double borders |
| Vertical lines | `\|` | |
| Corners / junctions | `+` | Universal junction character |
| Arrows | `>` `<` `^` `v` | Direction indicators |
| Arrow lines | `-->` `<--` `<-->` | Directional flow (sync request, return, bidirectional) |
| Dotted / optional arrow | `..>` | Optional or conditional transition (state machines) |
| Async event arrow | `- - >` | Fire-and-forget, message-queue publish, async signal |
| Dependency (hollow head) | `----D` | Class / interface dependency — "knows about" not "owns" |
| Plain association | `------` | Link with no directional semantics |
| Boxes | `+--+` with `\|` sides | Standard box drawing |
| Dots / bullets | `*` `.` `o` | For nodes or list items |
| Tree branches | `+--` `\|` `\\` | Hierarchy |
| Elision | `...` `~~~` | "More of the same" |
| Labels | Text inline or beside | Always label clearly |

### Extended connection-type vocabulary

The arrow-line row above gives the three staples every classic-ASCII diagram needs. When the diagram has to distinguish *kinds* of connection (sync vs async, call vs return, dependency vs ownership), use this fuller vocabulary:

| Connection kind | Form | Semantics |
|---|---|---|
| Sync / call | `---->` | Default. Request, synchronous method call, pipeline stage. |
| Return | `<----` | Paired return after a call (sequence diagrams). |
| Bidirectional | `<---->` | Handshake, symmetric coupling. |
| Async event | `- - >` | Dashed horizontal — publish, event emission, fire-and-forget. |
| Dependency | `----D` | Hollow head — "class X depends on class Y" (uses, imports, references). |
| Optional / conditional | `..>` | Dotted arrow — transition fires only if a guard condition is met (state machines). |
| Plain association | `------` | No directional head — composition, containment, loose link. |

Rules for mixing: pick one *primary* connector style per diagram, then reserve a second style for the contrast you are trying to highlight (e.g. everything is `->` except the one async fan-out that uses `- - >`). Three or more styles in one diagram without a legend are noise — document the vocabulary in a small `Legend:` box or omit the distinction.

## Reference library

Every file under `references/` is a short catalogue of proven patterns. Pick the closest reference first, then adapt:

| Category | Reference file | Use for |
|----------|----------------|---------|
| Flowcharts | [[flowcharts](references/flowcharts.md)](references/flowcharts.md) | Decision flows, request pipelines, control flow |
| State machines | [[state-machines](references/state-machines.md)](references/state-machines.md) | Protocol states, lifecycles, transitions |
| Trees | [[trees](references/trees.md)](references/trees.md) | File trees, class hierarchies, org charts |
| Data structures | [[data-structures](references/data-structures.md)](references/data-structures.md) | Memory layouts, packet formats, bit fields, linked lists |
| Network / Architecture | [[network-topology](references/network-topology.md)](references/network-topology.md) | K8s topology, service meshes, observability stacks |
| Sequences / Tables | [[sequences-tables](references/sequences-tables.md)](references/sequences-tables.md) | Request flows, timelines, comparison tables |
> [sequences-tables.md] Sequence Diagrams · Tables
| Graphs / Annotations | [[graphs-annotations](references/graphs-annotations.md)](references/graphs-annotations.md) | DAGs, code annotations, before/after, UI sketches |
> [graphs-annotations.md] Directed Graphs · Code Annotations · Before/After Comparisons · UI Sketches

When responding:

- Pick the closest reference file first.
- Reuse or adapt a pattern from `references/`. Do not re-invent.
- Keep this [SKILL](SKILL.md) as the guidance index, not as the full example catalog.

## Writing diagrams inside code comments

When the diagram lives inside a `//` / `#` / `*` comment block:

- Preserve the host language's comment prefix on every line.
- Keep alignment valid **after** adding the prefix — measure from the first column of actual content, not from the `//` itself.
- Pull the base pattern from the matching file in `references/`.
- Adapt names to real identifiers from the surrounding code.

## Non-negotiables

Every ASCII diagram this skill emits **MUST** pass `../../bin/amw-validate-ascii.py` before presentation to the user. See [SKILL](../amw-ascii-validator/SKILL.md) for the validator contract.

```bash
python3 bin/amw-validate-ascii.py /tmp/ascii-diagram-<slug>.txt
```

Beyond the mechanical validator:

- **Alignment check.** Verify every vertical `|` in the same column, every box corner `+` connects to exactly one horizontal `-` and one vertical `|`, every arrow head points in the intended direction, every label fits inside its box without overflow, widths consistent across comparable boxes.
- **Comment-prefix re-check.** After adding `//` / `#` / `*` prefixes, re-run the validator on the prefixed form — an extra 3 columns at the left can expose latent alignment bugs.
- **Do not assume proportional fonts.** Never trust your own eyeballing — LLMs and humans both misjudge width at a glance.
- **Never emit a diagram that failed validation.** Fix, re-validate, emit.

## Common mistakes to avoid

- **Broken corners**: `+` must connect to exactly one horizontal and one vertical line segment.
- **Floating arrows**: every arrow should clearly connect two elements.
- **Over-detail**: if the diagram has more detail than the code it describes, it is too complex.
- **No labels**: unlabeled boxes and lines are meaningless — always label.
- **Inconsistent spacing**: pick a spacing pattern and stick with it across the whole diagram.
- **Proportional font assumptions**: never assume characters have different widths.

## Instructions

1. Identify the diagram archetype from the user's intent (flowchart, state machine, tree, data structure, network topology, sequence, DAG, or annotation).
2. Select the closest reference file from `references/` using the category table; do not re-invent patterns.
3. Copy the matching pattern and substitute real identifiers from the user's code or brief.
4. Decide context: classic `+--+` ASCII for source-file comments or maximum portability, Unicode box-drawing (`┌─┐`) for GitHub-rendered READMEs.
5. Validate with `bin/amw-validate-ascii.py`; if running inside a comment block, re-validate after adding the language comment prefix.
6. Emit the validated diagram; never present a FAIL output.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `ascii-diagrams-reference` is the user asking about?
  - **classic** (18 techniques)
    - [TECH-classic-annotation-pointer-arrows](./references/TECH-classic-annotation-pointer-arrows.md) — label-to-element connectors
    - [TECH-classic-before-after-comparison](./references/TECH-classic-before-after-comparison.md) — N-scenario side-by-side ASCII
    - [TECH-classic-bit-field-annotation](./references/TECH-classic-bit-field-annotation.md) — bit-width register layout
    - [TECH-classic-compact-table](./references/TECH-classic-compact-table.md) — pipe-separated table with dash underline
    - [TECH-classic-directed-dag](./references/TECH-classic-directed-dag.md) — build-dependency graph with backward edges
    - [TECH-classic-flowchart-diamond](./references/TECH-classic-flowchart-diamond.md) — branching decision with `+--+` diamond
    - (see `## References` for the remaining 12 in this group)

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-classic-annotation-pointer-arrows.md](./references/TECH-classic-annotation-pointer-arrows.md)**
  - Description: label-to-element connectors
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-before-after-comparison.md](./references/TECH-classic-before-after-comparison.md)**
  - Description: N-scenario side-by-side ASCII
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-bit-field-annotation.md](./references/TECH-classic-bit-field-annotation.md)**
  - Description: bit-width register layout
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-compact-table.md](./references/TECH-classic-compact-table.md)**
  - Description: pipe-separated table with dash underline
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-directed-dag.md](./references/TECH-classic-directed-dag.md)**
  - Description: build-dependency graph with backward edges
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-flowchart-diamond.md](./references/TECH-classic-flowchart-diamond.md)**
  - Description: branching decision with `+--+` diamond
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-k8s-topology.md](./references/TECH-classic-k8s-topology.md)**
  - Description: Ingress → Service → Pods fan-out
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-linked-list.md](./references/TECH-classic-linked-list.md)**
  - Description: head → node → node → NULL chain
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-multi-service-architecture.md](./references/TECH-classic-multi-service-architecture.md)**
  - Description: client → gateway → services → DB
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-namespace-nesting.md](./references/TECH-classic-namespace-nesting.md)**
  - Description: Linux netns + overlay/underlay
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-observability-stack.md](./references/TECH-classic-observability-stack.md)**
  - Description: exporters → tsdb → alertmanager → sinks
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-pipeline-fanout.md](./references/TECH-classic-pipeline-fanout.md)**
  - Description: request → parse → split → rejoin
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-sequence-lifelines.md](./references/TECH-classic-sequence-lifelines.md)**
  - Description: Client/Server/DB actor columns
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-state-machine-arrows.md](./references/TECH-classic-state-machine-arrows.md)**
  - Description: TCP-style state diagram
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-struct-byte-offsets.md](./references/TECH-classic-struct-byte-offsets.md)**
  - Description: packet/struct layout with byte scale
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-timeline-events.md](./references/TECH-classic-timeline-events.md)**
  - Description: scaled time axis with event labels
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-tree-file-hierarchy.md](./references/TECH-classic-tree-file-hierarchy.md)**
  - Description: `+--` / `|` file-tree rendering
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-classic-ui-sketch-layout.md](./references/TECH-classic-ui-sketch-layout.md)**
  - Description: `+---+` UI wireframe mockup
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
- At least one `TECH-*.md` file from `skills/amw-ascii-diagrams-reference/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. validated ASCII `.txt` diagrams matching one of the CHI'24 archetypes). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-ascii-diagrams-reference-<slug>/`

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

- **runtime_binaries:** `perl >= 5.10` (pre-installed on macOS and most Linux distros — `/amw-doctor` checks), `python3 >= 3.8`
- **python_packages:** none (pure stdlib)
- **cpan / npm:** none

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Resources

- [SKILL](../amw-ascii-validator/SKILL.md) — MANDATORY validation gate; all emitted ASCII passes `validate-ascii.py`
- `../../bin/amw-validate-ascii.py` — the validator itself (Python, exits non-zero on failure, emits `FIX:` hints)
- [SKILL](../amw-box-diagram/SKILL.md) — Unicode rounded-corner counterpart for terminal / GitHub-README contexts
- [SKILL](../amw-ascii-sketch/SKILL.md) — framed rectangular wireframe layouts (different output medium)
- [SKILL](../amw-ascii-to-svg/SKILL.md) — downstream: convert an approved ASCII diagram to SVG
- [SKILL](../amw-diagram-svg/SKILL.md) — skip ASCII entirely, go direct to SVG
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — misaligned ASCII is a form of AI-slop
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- [[flowcharts](references/flowcharts.md)](references/flowcharts.md) — control-flow / decision trees / pipelines
- [[state-machines](references/state-machines.md)](references/state-machines.md) — protocol states, lifecycles
- [[trees](references/trees.md)](references/trees.md) — hierarchies, file trees, class trees
- [[data-structures](references/data-structures.md)](references/data-structures.md) — packet / struct / bit-field layouts
- [[network-topology](references/network-topology.md)](references/network-topology.md) — service architectures, K8s, observability
- [[sequences-tables](references/sequences-tables.md)](references/sequences-tables.md) — request flows, timelines, tables
  > Sequence Diagrams · Tables
- [[graphs-annotations](references/graphs-annotations.md)](references/graphs-annotations.md) — DAGs, code annotations, before/after
  > Directed Graphs · Code Annotations · Before/After Comparisons · UI Sketches

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| Validator reports `WIDTH_MISMATCH` after adding `//` prefix | Prefix indentation was not accounted for in the grid | Re-grid from column 0 **after** prefixing; every line has the same prefix width |
| Tree branches diverge — the `|` on the parent row is one column off from the `+--` on the child | Parent column offset was counted wrong by one | Recount from the root; last child drops the continuing `|` |
| Fan-in / fan-out arrows do not connect | A `+` corner is missing where branches rejoin | Insert `+` at every intersection; validator flags this as broken-corner |
| Emoji / Unicode glyph in a label reports wide-char | Author slipped a UTF-8 glyph into classic-ASCII output | Replace with ASCII equivalent — this skill is classic ASCII only; Unicode diagrams belong to `../amw-box-diagram/` |
