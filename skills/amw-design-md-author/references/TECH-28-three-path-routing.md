---
name: TECH-28-three-path-routing
category: workflow
source: awesome-design-md three-path routing pattern (MIT)
license: MIT
also-in: TECH-15-design-md-as-input.md, TECH-24-authoring-rules-spec.md, TECH-21-style-references-companion.md, ../../amw-design-principles/SKILL.md
status: stable
---

# TECH: Three-path DESIGN.md routing

## Table of Contents

- [What it does](#what-it-does)
- [The three paths](#the-three-paths)
- [Path A — DESIGN.md exists](#path-a--designmd-exists)
  - [Detection](#detection)
  - [Workflow](#workflow)
  - [Token enforcement](#token-enforcement)
  - [When the existing DESIGN.md is invalid](#when-the-existing-designmd-is-invalid)
- [Path B — No DESIGN.md, project-setup mode](#path-b--no-designmd-project-setup-mode)
  - [Detection](#detection-1)
  - [The 4-item interview](#the-4-item-interview)
  - [Variant generation](#variant-generation)
  - [Writing the DESIGN.md after approval](#writing-the-designmd-after-approval)
- [Path C — No DESIGN.md, one-off task](#path-c--no-designmd-one-off-task)
  - [Detection](#detection-2)
  - [Workflow](#workflow-1)
  - [The one-time DESIGN.md mention](#the-one-time-designmd-mention)
- [Routing decision tree](#routing-decision-tree)
- [Why three paths and not two or four](#why-three-paths-and-not-two-or-four)
- [Cross-references](#cross-references)

## What it does

Documents the three-path routing pattern that determines whether the orchestrator builds against an existing DESIGN.md, conducts a discovery interview to create one, or proceeds without one. The routing is applied at the start of every main-agent session and re-applied whenever the project context changes (new directory, new repo).

This routing is the entry point for the design-md skill family. It precedes any token authoring, extraction, or linting.

## The three paths

- **Path A** — A `DESIGN.md` file exists in the project. Build using its tokens; treat the file as canonical.
- **Path B** — No `DESIGN.md` exists, and the user is in project-setup mode (new project, fresh visual identity, multi-task engagement). Conduct a 4-item interview, generate variants, get approval, then write the DESIGN.md.
- **Path C** — No `DESIGN.md` exists, and the user has a one-off task (single component, single page, single artifact). Do the task without conducting an interview, mention DESIGN.md once at the end, and move on.

The decision is binary at the first split (DESIGN.md exists or not) and based on engagement intent at the second split (setup vs one-off).

## Path A — DESIGN.md exists

### Detection

The orchestrator scans the project root and one level deep for a `DESIGN.md` file:

```bash
find . -maxdepth 2 -name 'DESIGN.md' -type f
```

If exactly one match, Path A. If multiple matches, the orchestrator prompts the user to select one. If zero matches, fall through to Path B/C detection.

### Workflow

1. Read the DESIGN.md.
2. Run `bin/amw-design-md-lint.sh <DESIGN.md>` to confirm the file is structurally valid.
3. Run `bin/amw-design-md-validate.py <DESIGN.md>` for offline pure-Python validation (including dead-reference checks per [TECH-27-token-interpolation](TECH-27-token-interpolation.md)).
4. On lint or validation failure, halt and report — do NOT silently proceed against a broken DESIGN.md.
5. On success, treat the DESIGN.md tokens as canonical for the entire session. Any agent the orchestrator delegates to receives the validated DESIGN.md path as input.
6. If the user requests an artifact (HTML, SVG, infographic, etc.), pass the DESIGN.md path to the appropriate Phase B agent (typically `amw-wireframe-builder-agent`).

### Token enforcement

In Path A, the orchestrator and all sub-agents must:

- Use exclusively the colors declared in the DESIGN.md frontmatter. No introducing a new accent color "to make it pop".
- Use exclusively the typography roles declared. No introducing a new heading size.
- Use exclusively the spacing scale declared. No mixing 12px when the scale is 8px-based.
- Use the elevation treatments per §5. No adding a shadow when the spec says rule lines.

When the user explicitly asks for a deviation ("can we try this with a different accent?"), the orchestrator:
1. Acknowledges the deviation.
2. Generates the variant with the new value.
3. Suggests adding the new value to the DESIGN.md (or splitting into a new DESIGN.md) if the deviation is intended to persist.

### When the existing DESIGN.md is invalid

If lint or validation fails, the orchestrator presents the user with three options:

1. Repair the DESIGN.md (spawn `amw-design-md-author-agent` to fix the lint errors and re-validate).
2. Re-extract the DESIGN.md from source if it was originally extracted (spawn `amw-design-md-extractor-agent`).
3. Proceed in Path C mode (treat the broken DESIGN.md as absent and do the one-off task without it).

The orchestrator does NOT silently auto-repair. Each option requires explicit user choice.

## Path B — No DESIGN.md, project-setup mode

### Detection

Path B is detected when ALL of the following are true:

- No DESIGN.md exists in the project.
- The user's intent involves multiple artifacts (landing page + dashboard + email templates, or "design the whole brand").
- The user has not used a phrase indicating they want a one-off ("just this one page", "quick mockup", "for now").

Phrases that signal Path B intent: "design a brand for", "create a design system", "set up the design language", "we're starting a new project", "let's establish the visual direction".

Detection is heuristic — the orchestrator may ask a clarifying question if the signal is ambiguous: "Are we establishing a design system for the whole project, or is this a one-off task?"

### The 4-item interview

Path B opens with a structured 4-item interview. The user answers each item; the orchestrator does not proceed until all four are filled.

1. **Audience and scenario.** Who is this for, and what are they trying to do?
   - Example user answer: "B2B technical buyers evaluating our analytics product. They land on a marketing page from a Google ad and need to decide whether to book a demo in 90 seconds."

2. **At least 1 visual anchor.** Cite at least one existing brand or product whose visual style you want to anchor against. (May be aspirational — not a literal clone target.)
   - Example user answer: "Linear's website. Specifically the homepage hero and the docs typography."

3. **2-3 tonal positions.** What ADJECTIVES describe the brand voice?
   - Example user answer: "Restrained, technical, lowercase-where-idiomatic."

4. **At least 1 taboo.** What is the brand explicitly NOT?
   - Example user answer: "Not playful. Not exclamatory. Never use bright orange — our biggest competitor owns that color."

The 4-item interview is the minimum. The orchestrator may ask follow-up questions if any item is too vague (e.g. "Linear's website" → "Which Linear page specifically?").

### Variant generation

After the 4-item interview, the orchestrator generates 3 variants:

1. **Baseline.** Conservative interpretation of the user's inputs. Token choices stay close to the anchor brand.
2. **Advanced.** Stronger commitment to the user's tonal positions. May depart further from the anchor.
3. **Experimental.** Pushes one or two design decisions further than the user explicitly requested, to expose the design surface.

All three variants are presented in ASCII or low-fi form per `skills/amw-design-principles/SKILL.md` Phase A — NOT as polished HTML. Token-level differences are described in prose adjacent to the ASCII.

The user picks ONE variant or asks for a fourth that combines elements. The orchestrator iterates until satisfaction tokens are received (`yes`, `ship it`, `that's the one`, `perfect`, `done`, `approved`).

### Writing the DESIGN.md after approval

After approval:

1. The orchestrator spawns `amw-design-md-author-agent` with the approved variant's token bundle.
2. The agent writes a full Variant 1 DESIGN.md per [canonical-spec-google-alpha](../../amw-design-md-spec/references/canonical-spec-google-alpha.md), filling each section from the approved variant.
3. The agent runs `bin/amw-design-md-lint.sh` and `bin/amw-design-md-validate.py` before declaring done.
4. The agent emits companion files via `bin/amw-design-md-emit-companions.py`.
5. The agent optionally emits `STYLE-REFERENCES.md` if the user's visual anchor and taboo answers in the 4-item interview were rich enough to populate sections 1-5 per [TECH-21-style-references-companion](TECH-21-style-references-companion.md).
6. The orchestrator reports the new DESIGN.md path back to the user.

From this point forward, the project is in Path A.

## Path C — No DESIGN.md, one-off task

### Detection

Path C is detected when:

- No DESIGN.md exists in the project.
- The user's intent is a SINGLE artifact (one component, one page, one email, one screenshot).
- The user uses a phrase indicating one-off intent ("just this", "quick", "for now", "single", "one-off", "throwaway").

### Workflow

1. Acknowledge no DESIGN.md exists.
2. Do the task. Apply reasonable defaults from `skills/amw-design-principles/SKILL.md` and the appropriate executor skill.
3. DO NOT conduct the 4-item interview. DO NOT generate 3 variants of the DESIGN.md. Path C is fast.
4. The artifact may go through normal Phase A ASCII iteration (per `amw-design-principles`), but that iteration is about THIS artifact's layout, not about establishing a design system.
5. Deliver the artifact.

### The one-time DESIGN.md mention

At the end of the Path C task (after the artifact is delivered, NOT before), the orchestrator mentions the DESIGN.md opportunity ONCE:

> "Heads up: this project doesn't have a `DESIGN.md`. If you plan to build more visual artifacts, establishing one would lock in token consistency across them. Run `/amw-design-md-create` or ask me to set one up."

This is a SUGGESTION, not a question. The user is free to ignore it. The orchestrator does not repeat the mention in subsequent Path C tasks for the same project — once is enough. Tracking the mention across sessions is best-effort (the orchestrator may forget across session boundaries; that's acceptable).

The mention is calibrated to be a single, non-intrusive sentence. Two-sentence pitches are too long. Three-bullet rationales feel like upselling.

## Routing decision tree

```
START: Receive user request
  |
  v
1. Does DESIGN.md exist in project?
  |--- YES ---> PATH A (Build with existing DESIGN.md)
  |
  |--- NO ---> Continue to step 2
  |
  v
2. Is user in project-setup mode? (multi-artifact intent OR explicit setup phrase)
  |--- YES ---> PATH B (4-item interview → variants → write DESIGN.md)
  |
  |--- NO ---> Continue to step 3
  |
  v
3. Ambiguous? (single intent statement, no setup keyword, no one-off keyword)
  |--- YES ---> Ask clarifying question, then route based on answer
  |
  |--- NO ---> PATH C (Just do it; mention DESIGN.md once)
```

## Why three paths and not two or four

Two paths (DESIGN.md exists vs not) would conflate setup mode with one-off tasks. The 4-item interview is overkill for a one-off task; skipping the interview for setup mode produces a broken design system. The split between B and C is therefore essential.

Four paths might add "DESIGN.md exists but is being intentionally ignored for this artifact" — but that case is handled within Path A as an explicit user override. Adding a separate path bloats the decision tree without adding value.

Three paths is the minimum that:
- Honors existing token systems (A).
- Builds new token systems when intent is established (B).
- Does not over-engineer one-off requests (C).

## Cross-references

- [TECH-15-design-md-as-input](../../amw-design-md-convert/references/TECH-15-design-md-as-input.md) — Path A token-consumption details
- [TECH-21-style-references-companion](TECH-21-style-references-companion.md) — Path B STYLE-REFERENCES.md emission
- [TECH-22-section-10-11-extended](TECH-22-section-10-11-extended.md) — Path B may emit §10/§11 from interview answers
- [TECH-24-authoring-rules-spec](../../amw-design-md-spec/references/TECH-24-authoring-rules-spec.md) — Path A and Path B writing rules
- [TECH-25-brand-archetypes](TECH-25-brand-archetypes.md) — Path B variant generation uses archetype defaults
- [TECH-27-token-interpolation](TECH-27-token-interpolation.md) — Path A token enforcement detail
- [../../amw-design-principles/SKILL.md](../../amw-design-principles/SKILL.md) — orchestrator that applies this routing
- [../../amw-design-principles/references/two-mode-workflow.md](../../amw-design-principles/references/two-mode-workflow.md) — Command-mode vs main-agent-mode (orthogonal to this 3-path routing)
