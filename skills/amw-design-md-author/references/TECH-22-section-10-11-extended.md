---
name: TECH-22-section-10-11-extended
category: authoring
source: awesome-design-md community examples; DESIGN_MD_SPEC extended sections
license: MIT
also-in: TECH-21-style-references-companion.md, TECH-24-authoring-rules-spec.md, extension-sections-10-14.md
status: stable
---

# TECH: Optional §10 Iteration Guide + §11 Known Gaps

## Table of Contents

- [What it does](#what-it-does)
- [Position in the section order](#position-in-the-section-order)
- [§10 Iteration Guide](#10-iteration-guide)
  - [Purpose](#purpose)
  - [Structure](#structure)
  - [Length and tone](#length-and-tone)
  - [Worked example](#worked-example)
  - [What §10 is NOT](#what-10-is-not)
- [§11 Known Gaps](#11-known-gaps)
  - [Purpose](#purpose-1)
  - [Structure](#structure-1)
  - [Categories of common gaps](#categories-of-common-gaps)
  - [Worked example](#worked-example-1)
  - [What §11 is NOT](#what-11-is-not)
- [Linting rules](#linting-rules)
- [When to omit](#when-to-omit)
- [Cross-references](#cross-references)

## What it does

Documents the two OPTIONAL trailing sections that extend the canonical Variant 1 DESIGN.md beyond the 8 mandatory sections: §10 Iteration Guide and §11 Known Gaps. These sections are useful when the DESIGN.md will be consumed by an AI coding agent across multiple sessions or when the DESIGN.md was extracted from a third-party source where some content was unreachable.

These sections are NUMBERED 10 and 11, even though Variant 1's mandatory body ends at §8 Do's and Don'ts and §9 Agent Prompt Guide. Authors who skip §9 (also optional) still number these as 10 and 11 — the numbering is stable across optionality.

## Position in the section order

Section order in extended Variant 1:

1. Identity (frontmatter is YAML, then this section is § 1)
2. Color
3. Typography
4. Spacing & Rhythm
5. Surfaces & Elevation
6. Components
7. Motion (sometimes folded into §6; see [TECH-26-extended-sections-7-8](TECH-26-extended-sections-7-8.md))
8. Do's and Don'ts
9. Agent Prompt Guide (OPTIONAL; see [TECH-23-section-9-agent-prompt-guide](TECH-23-section-9-agent-prompt-guide.md))
10. **Iteration Guide (this file)**
11. **Known Gaps (this file)**

Sections 10 and 11 always appear LAST. The Do's and Don'ts must remain at §8 — it is the bookend of the strict-rule layer. §10 and §11 are advisory.

## §10 Iteration Guide

### Purpose

A numbered list of practical token-usage tips the human author wants the coding agent to apply during the implementation session. This is the place to surface workflow-level advice that does NOT fit in the token table or the Do/Don't list.

Typical content includes:

- Where to start the build (which component to scaffold first).
- Which token to vary in early iterations (usually accent color, never primary).
- Which sections of the page benefit from intentional rhythm breaks.
- How to validate the build against the brand (e.g. "screenshot the hero against the brand homepage").
- Token-substitution heuristics ("if a customer asks for a warmer accent, shift `tertiary` toward `#C04A2E`, never beyond").

### Structure

A numbered list (NOT bulleted — this is the one section in the spec where numbered order matters). Each item is a complete sentence or short paragraph. Items should be in priority order, top-most first.

```markdown
## 10. Iteration Guide

1. Start with the hero block. The visual relationship between the
   `display` heading, the body, and the primary CTA establishes 90%
   of the page rhythm — get this right before any other component.
2. Use `secondary` text for all metadata (timestamps, tags, captions).
   Never apply `secondary` to body copy — it reads as a layout error.
3. The `tertiary` accent (`#B8422E`) appears at most ONCE per
   viewport-worth of scroll. Multiple appearances flatten its impact.
4. When in doubt, halve the spacing — the rhythm is built around
   restraint, not abundance.
```

### Length and tone

Five to ten items, each one to three sentences. Tone is direct and second-person ("Start with..."). Avoid hedging ("you might consider", "perhaps") — the agent treats these as instructions, not suggestions.

### Worked example

See the awesome-design-md `posthog.DESIGN.md` extraction §10 for a fully-worked Iteration Guide on a developer SaaS brand.

### What §10 is NOT

- NOT a duplicate of §8 Do's and Don'ts. Do's are absolute rules; Iteration Guide is workflow ordering.
- NOT brand voice or copy. That lives in `STYLE-REFERENCES.md` §5.
- NOT a place to dump component implementation notes. Those belong in `component-inventory.md` (a companion file).
- NOT executable. The agent reads §10 once at session start and weighs it against the DESIGN.md token table.

## §11 Known Gaps

### Purpose

An honest list of what could NOT be extracted from the source brand and therefore must be invented or inferred during the build. Authoring §11 is the alternative to fabricating tokens that have no source — which is one of the worst slop patterns (see `../ai-slop-avoid.md`).

### Structure

Markdown bullet list. Each bullet states ONE gap, with three sub-items: what is missing, where the agent should source the substitute, and what the substitute target should approximate.

```markdown
## 11. Known Gaps

- **Brand display font.** The source uses a paid font (Söhne by Klim) we cannot
  redistribute. The DESIGN.md declares `Inter` as the body face and `Manrope` as the
  display face, both available via Google Fonts and visually adjacent to the original.
- **Auth-gated marketing pages.** The pricing page and the customer-stories index
  redirect to an account-required experience. The DESIGN.md tokens were extracted
  from the public marketing pages only; agents working on a pricing component
  should reference Linear's pricing page (`linear.app/pricing`) as the closest peer.
- **Animation timing curves.** The source animations use a proprietary bezier we
  could not reverse from the network tab. The DESIGN.md `motion.timing` table uses
  the common-Web approximations `ease-out 200ms`, `ease-in-out 400ms`.
- **Photography style.** The source uses commissioned photography we have no
  rights to. The DESIGN.md recommends abstract illustration in the `tertiary`
  accent color as a substitute for hero imagery.
```

### Categories of common gaps

The most common gap types §11 surfaces:

- **Proprietary fonts.** The source uses a commercial face that cannot be redistributed. The substitute is a free Google Fonts adjacent face (Söhne → Inter, Tiempos → Source Serif, etc.).
- **Auth-gated content.** Logged-in marketing pages or product surfaces were not reachable during extraction. The substitute is a public-peer page from a similar brand.
- **Custom animation curves.** Proprietary cubic-bezier values were not recoverable from compiled JS. The substitute is the closest common ease curve.
- **Photography and illustration assets.** Commissioned imagery has no redistribution license. The substitute is generic stock-style guidance.
- **Custom icons.** A proprietary icon set was used. The substitute is Lucide / Heroicons / Phosphor at the same stroke weight.
- **Print or non-web variants.** Some brands maintain entirely separate print or app design systems. The substitute is web-only with a note in `STYLE-REFERENCES.md §6 Cross-Medium Guide`.
- **Dark mode tokens.** When the extracted source has only a light mode, dark-mode counterparts are missing. The substitute is an algorithmic inversion noted as approximate.

### Worked example

See the awesome-design-md `stripe.DESIGN.md` extraction §11 for a fully-worked Known Gaps section on a brand with extensive proprietary assets.

### What §11 is NOT

- NOT a TODO list for future extraction. Items here are gaps that cannot be closed — they are permanent inferences. If a gap CAN be closed by re-extracting, close it and remove the entry.
- NOT an apology. The tone is matter-of-fact: "the source has X; we substitute Y because Z".
- NOT a place to record extraction errors. Errors go in `<file>.critique.md` from the auditor agent.

## Linting rules

The Variant 1 linter treats §10 and §11 as optional. When present:

- §10 must be a numbered list (markdown `1.` style). A bulleted §10 is a lint warning.
- §11 must be a bulleted list (markdown `-` style). Numbered §11 is a lint warning.
- Both sections must appear AFTER §9 if §9 is present, or AFTER §8 if §9 is omitted.
- Neither section may reference tokens that do not exist in the YAML frontmatter (dead reference = P1 lint error per [TECH-27-token-interpolation](TECH-27-token-interpolation.md)).

## When to omit

Omit §10 when:
- The DESIGN.md is small (under 100 lines).
- The build is one-off and will not be revisited.
- The orchestrator is operating in Command mode (the user invoked a specific `/amw-*` command, not the main-agent flow).

Omit §11 when:
- The DESIGN.md was authored from scratch (no extraction). Authored specs have no gaps by definition.
- The source was fully reachable and no inferences were made.

When in doubt, include both. Their cost is twenty lines; their benefit is a coding agent that does not invent.

## Cross-references

- [TECH-24-authoring-rules-spec](../../amw-design-md-spec/references/TECH-24-authoring-rules-spec.md) — the 13 authoring rules including §10/§11 placement
- [TECH-21-style-references-companion](TECH-21-style-references-companion.md) — sister companion for lineage and voice
- [TECH-23-section-9-agent-prompt-guide](TECH-23-section-9-agent-prompt-guide.md) — sister §9 optional section
- [extension-sections-10-14](../../amw-design-md-spec/references/extension-sections-10-14.md) — broader optional-section family (10-14)
- [TECH-27-token-interpolation](TECH-27-token-interpolation.md) — token-reference linting that applies inside §10 and §11
