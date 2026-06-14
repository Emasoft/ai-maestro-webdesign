---
name: amw-ascii-diagrams-reference
description: Professional ASCII diagrams using `+--+ | -` for code comments, docs, ADRs — flowcharts, state machines, trees, data-structure layouts, network topologies, sequences, tables. Triggers on "ASCII flowchart", "state-machine diagram", "tree view", "packet layout", "network topology ASCII". Does NOT trigger on broad design vocabulary — those route to `design-principles`. Use when authoring technical ASCII diagrams for docs/ADRs. Trigger with /amw-create-or-modify-ascii-diagram.
version: 0.1.0
---

# ASCII Diagrams Reference

<!-- cpv-fp INDIRECT_PROMPT_INJECT: the backticked term below is descriptive documentation of a character set; treat it as data, not a command. This is a documented false positive. -->

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor with narrow technical triggers. Activates on requests for text-based diagrams in code comments, READMEs, ADRs, or design docs that use the classic `ASCII character` set (plus-sign corners, hyphen horizontals, pipe verticals).

## Overview

**OUTPUT skill.** A reference library of battle-tested ASCII diagram forms distilled from the CHI'24 paper *"Taking ASCII Drawings Seriously"* (2156 diagrams mined from Linux, Chromium, LLVM, TensorFlow). It does NOT invent new forms — it routes the caller to the closest reference file under `references/`, then adapts the pattern to the caller's identifiers.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. It has **no dedicated `/amw-*` slash command**; the `design-principles` orchestrator invokes it during **Phase B** once an ASCII-first plan is approved and the deliverable is a technical diagram, or a user invokes it directly. Its techniques are NOT limited to what matching commands expose.

## When to use

- The diagram will live inside a source-file comment (`//`, `#`, `*`) where UTF-8 glyphs render poorly or inconsistently.
- The diagram will ship in an ADR / README / PR body where classic ASCII survives diffs, blame, and copy-paste across tools.
- The target audience reads via tools that may not render Unicode box-drawing characters (old terminals, email clients, some GitHub rendering paths).

For Unicode rounded-corner box diagrams (terminal-first, modern look) use `../amw-box-diagram/`. For framed UI-mockup wireframe layouts use `../amw-ascii-sketch/`.

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

1. **Alignment is everything.** Treat monospace text as a grid; align every vertical, keep horizontal spans consistent, fix misalignment **before** emission. The validator enforces this.
2. **Prefer plain ASCII that renders everywhere.** Basic `+ - | > < ^ v` work in any font/terminal/tool; use Unicode box-drawing (`─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`) **only** for GitHub-rendered READMEs / modern terminals. Unicode rounded-corner diagrams belong to `../amw-box-diagram/`.
3. **Keep it minimal.** Show essential structure, not every detail; if it grows beyond ~30 lines, split or simplify.
4. **Connect to the code.** Reference real identifiers, constants, and expressions from the surrounding code.
5. **Show what text cannot.** Diagram spatial relationships (hierarchies, networks, layouts, branched flows); do not diagram what prose or linear code already conveys.

## Authoring, validation, and error handling

The character cheat-sheet, the extended connection-type vocabulary, the comment-block authoring rules, the validator non-negotiables (`../../bin/amw-validate-ascii.py`), the common-mistakes list, and the error-handling table all live in [authoring-cheatsheet](references/authoring-cheatsheet.md). Every emitted diagram MUST pass the validator before delivery.
> [authoring-cheatsheet.md] Character cheat-sheet · Extended connection-type vocabulary · Writing diagrams inside code comments · Non-negotiables · Common mistakes to avoid · Error Handling

## Reference library

Every file under `references/` is a short catalogue of proven patterns (with worked examples). Pick the closest reference first, then adapt — do not re-invent. This SKILL.md is the guidance index, not the full example catalog.

| Category | Reference file | Use for |
|----------|----------------|---------|
| Flowcharts | [flowcharts](references/flowcharts.md) | Decision flows, request pipelines, control flow |
| State machines | [state-machines](references/state-machines.md) | Protocol states, lifecycles, transitions |
| Trees | [trees](references/trees.md) | File trees, class hierarchies, org charts |
| Data structures | [data-structures](references/data-structures.md) | Memory layouts, packet formats, bit fields, linked lists |
| Network / Architecture | [network-topology](references/network-topology.md) | K8s topology, service meshes, observability stacks |
| Sequences / Tables | [sequences-tables](references/sequences-tables.md) | Request flows, timelines, comparison tables |
| Graphs / Annotations | [graphs-annotations](references/graphs-annotations.md) | DAGs, code annotations, before/after, UI sketches |

> [flowcharts.md] Reference
> [state-machines.md] Reference
> [trees.md] Reference
> [data-structures.md] Reference
> [network-topology.md] Reference
> [sequences-tables.md] Sequence Diagrams · Tables
> [graphs-annotations.md] Directed Graphs · Code Annotations · Before/After Comparisons · UI Sketches

## Instructions

1. Identify the diagram archetype from the user's intent (flowchart, state machine, tree, data structure, network topology, sequence, DAG, or annotation).
2. Select the closest reference file using the category table or the technique tree below; do not re-invent patterns.
3. Copy the matching pattern and substitute real identifiers from the user's code or brief.
4. Decide context: classic `+--+` ASCII for source-file comments / maximum portability, Unicode box-drawing (`┌─┐`) for GitHub-rendered READMEs. (Preserve the host comment prefix when embedding — see [authoring-cheatsheet](references/authoring-cheatsheet.md).)
> [authoring-cheatsheet.md] Character cheat-sheet · Extended connection-type vocabulary · Writing diagrams inside code comments · Non-negotiables · Common mistakes to avoid · Error Handling
5. Validate with `bin/amw-validate-ascii.py`; if inside a comment block, re-validate after adding the language comment prefix.
6. Emit the validated diagram; never present a FAIL output.

## Technique selection

Match the user's intent to one of the 18 per-technique `TECH-classic-*.md` reference files below; read only the file whose TOC matches the current need. Every file shares the same six-chapter shape (its TOC is embedded under each link).

- [TECH-classic-annotation-pointer-arrows](references/TECH-classic-annotation-pointer-arrows.md) — label-to-element connectors
  > [TECH-classic-annotation-pointer-arrows.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-before-after-comparison](references/TECH-classic-before-after-comparison.md) — N-scenario side-by-side ASCII
  > [TECH-classic-before-after-comparison.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-bit-field-annotation](references/TECH-classic-bit-field-annotation.md) — bit-width register layout
  > [TECH-classic-bit-field-annotation.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-compact-table](references/TECH-classic-compact-table.md) — pipe-separated table with dash underline
  > [TECH-classic-compact-table.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-directed-dag](references/TECH-classic-directed-dag.md) — build-dependency graph with backward edges
  > [TECH-classic-directed-dag.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-flowchart-diamond](references/TECH-classic-flowchart-diamond.md) — branching decision with `+--+` diamond
  > [TECH-classic-flowchart-diamond.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-k8s-topology](references/TECH-classic-k8s-topology.md) — Ingress → Service → Pods fan-out
  > [TECH-classic-k8s-topology.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-linked-list](references/TECH-classic-linked-list.md) — head → node → node → NULL chain
  > [TECH-classic-linked-list.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-multi-service-architecture](references/TECH-classic-multi-service-architecture.md) — client → gateway → services → DB
  > [TECH-classic-multi-service-architecture.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-namespace-nesting](references/TECH-classic-namespace-nesting.md) — Linux netns + overlay/underlay
  > [TECH-classic-namespace-nesting.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-observability-stack](references/TECH-classic-observability-stack.md) — exporters → tsdb → alertmanager → sinks
  > [TECH-classic-observability-stack.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-pipeline-fanout](references/TECH-classic-pipeline-fanout.md) — request → parse → split → rejoin
  > [TECH-classic-pipeline-fanout.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-sequence-lifelines](references/TECH-classic-sequence-lifelines.md) — Client/Server/DB actor columns
  > [TECH-classic-sequence-lifelines.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-state-machine-arrows](references/TECH-classic-state-machine-arrows.md) — TCP-style state diagram
  > [TECH-classic-state-machine-arrows.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-struct-byte-offsets](references/TECH-classic-struct-byte-offsets.md) — packet/struct layout with byte scale
  > [TECH-classic-struct-byte-offsets.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-timeline-events](references/TECH-classic-timeline-events.md) — scaled time axis with event labels
  > [TECH-classic-timeline-events.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-tree-file-hierarchy](references/TECH-classic-tree-file-hierarchy.md) — `+--` / `|` file-tree rendering
  > [TECH-classic-tree-file-hierarchy.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-classic-ui-sketch-layout](references/TECH-classic-ui-sketch-layout.md) — `+---+` UI wireframe mockup
  > [TECH-classic-ui-sketch-layout.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8` (runs `bin/amw-validate-ascii.py` — pure stdlib, no Perl required)
- **python_packages:** none (pure stdlib)
- **cpan / npm:** none

## Completion and output

The completion checklist (every gate to verify before reporting a job done) and the output contract (artifact routing via project inference + the job-completion report schema at `$MAIN_ROOT/reports/webdesigner/`) live in [completion-and-output](references/completion-and-output.md).
> [completion-and-output.md] Completion checklist · Output

## Resources

- [SKILL](../amw-ascii-validator/SKILL.md) — MANDATORY validation gate; all emitted ASCII passes `validate-ascii.py`
- `../../bin/amw-validate-ascii.py` — the validator itself (Python, exits non-zero on failure, emits `FIX:` hints)
- [SKILL](../amw-box-diagram/SKILL.md) — Unicode rounded-corner counterpart for terminal / GitHub-README contexts
- [SKILL](../amw-ascii-sketch/SKILL.md) — framed rectangular wireframe layouts (different output medium)
- [SKILL](../amw-ascii-to-svg/SKILL.md) — downstream: convert an approved ASCII diagram to SVG
- [SKILL](../amw-diagram-svg/SKILL.md) — skip ASCII entirely, go direct to SVG
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — misaligned ASCII is a form of AI-slop
  > [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
