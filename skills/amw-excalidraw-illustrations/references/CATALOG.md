# amw-excalidraw-illustrations — Technique Catalog

## Table of Contents

- [Decision tree (top-down)](#decision-tree-top-down)
- [Per-technique TOC index](#per-technique-toc-index)
- [Cross-references](#cross-references)

This is the full reference index for the `amw-excalidraw-illustrations` skill.
The orchestrator should read only the technique file whose topic matches the
current need; this catalog exists so the SKILL.md itself stays compact.

## Decision tree (top-down)

Walk this tree top-down to pick the right reference. If a branch does not
match the user's intent, skip to the next. Every technique in the catalog
is a leaf of this tree.

- Which aspect of `excalidraw-illustrations` is the user asking about?
  - **aspect** (1 technique) — aspect-ratio choice before any Gemini call
    - [TECH-aspect-ratio-selection](./TECH-aspect-ratio-selection.md)
      > What it does · When to use · How it works · Asking the user · API wiring · Minimal example · Gotchas · Cross-references
  - **framed** (1 technique) — text always inside frames / bubbles / callouts
    - [TECH-framed-text-no-floating](./TECH-framed-text-no-floating.md)
      > What it does · When to use · How it works · Rounded title frame (section headers) · Speech bubble (tag-line commentary) · Labelled callout with filled background · Minimal example · Gotchas · Cross-references
  - **gemini** (1 technique) — Pro vs flash model choice
    - [TECH-gemini-pro-vs-flash-model-choice](./TECH-gemini-pro-vs-flash-model-choice.md)
  - **letter** (1 technique) — letter-by-letter spelling block in the prompt
    - [TECH-letter-by-letter-spelling-block](./TECH-letter-by-letter-spelling-block.md)
  - **prompt** (1 technique) — the canonical prompt-template shape
    - [TECH-prompt-template-structure](./TECH-prompt-template-structure.md)
      > What it does · When to use · How it works · Section order and purpose · Template skeleton · Minimal example · Gotchas · Cross-references
  - **reference** (1 technique) — embedding reference images for style stability
    - [TECH-reference-image-priming](./TECH-reference-image-priming.md)
  - **two** (1 technique) — visual-first then text-overlay fallback
    - [TECH-two-phase-visual-then-overlay](./TECH-two-phase-visual-then-overlay.md)
      > What it does · When to use · How it works · Phase 1 — visual-only generation · Phase 2 — local text overlay via Pillow · Minimal example · Gotchas · Cross-references

## Per-technique TOC index

Every technique in this skill is documented as a single reference file
under `./` (this directory). Read only the file whose TOC matches the
current need.

- **[TECH-aspect-ratio-selection](./TECH-aspect-ratio-selection.md)**
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- **[TECH-framed-text-no-floating](./TECH-framed-text-no-floating.md)**
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- **[TECH-gemini-pro-vs-flash-model-choice](./TECH-gemini-pro-vs-flash-model-choice.md)**
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- **[TECH-letter-by-letter-spelling-block](./TECH-letter-by-letter-spelling-block.md)**
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- **[TECH-prompt-template-structure](./TECH-prompt-template-structure.md)**
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- **[TECH-reference-image-priming](./TECH-reference-image-priming.md)**
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- **[TECH-two-phase-visual-then-overlay](./TECH-two-phase-visual-then-overlay.md)**
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references

## Cross-references

- [SKILL](../SKILL.md) — parent skill (orchestrator for this catalog)
- [SKILL](../../amw-design-principles/SKILL.md) — broader orchestrator
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — item 3 (illustration ban) carves an exception for this skill only
