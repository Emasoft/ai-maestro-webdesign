---
name: TECH-21-style-references-companion
category: companion
source: awesome-design-md community examples; design-system-extractor STYLE-REFERENCES.md pattern
license: MIT
also-in: TECH-12-companion-files.md, TECH-25-brand-archetypes.md, TECH-22-section-10-11-extended.md
status: stable
---

# TECH: STYLE-REFERENCES.md companion file

## Table of Contents

- [What it does](#what-it-does)
- [Why a separate file](#why-a-separate-file)
- [The six mandatory sections](#the-six-mandatory-sections)
  - [1. Design Lineage](#1-design-lineage)
  - [2. Peer References](#2-peer-references)
  - [3. Anti-References](#3-anti-references)
  - [4. Extended Component Gallery](#4-extended-component-gallery)
  - [5. Style Vocabulary](#5-style-vocabulary)
  - [6. Cross-Medium Guide](#6-cross-medium-guide)
- [Emission contract](#emission-contract)
- [How agents consume it](#how-agents-consume-it)
- [Linting STYLE-REFERENCES.md](#linting-style-referencesmd)
- [Synchronization with DESIGN.md](#synchronization-with-designmd)
- [Cross-references](#cross-references)

## What it does

Documents the optional `STYLE-REFERENCES.md` companion that ships alongside `DESIGN.md`. While `DESIGN.md` describes WHAT the design system is (tokens, rules, do/don'ts), `STYLE-REFERENCES.md` describes WHERE the design system came from and how it relates to its peers and rivals. The companion is consumed by `amw-wireframe-builder-agent`, `amw-brand-researcher-agent`, and the design-md-extractor pipeline as a secondary input layer.

## Why a separate file

Three reasons the lineage / references content lives outside `DESIGN.md`:

1. `DESIGN.md` is canonical and small. Adding 60 lines of "we look like X, we differ from Y" prose would dilute the token table and slow the lint gate.
2. `STYLE-REFERENCES.md` is a soft input (it shapes voice and vibe, not strict tokens). Agents read it for orientation, not for validation. Keeping it separate prevents an agent from over-indexing on it.
3. The file is editable by a designer or PM without touching the canonical token spec — and without re-running the linter on every prose tweak.

`STYLE-REFERENCES.md` is OPTIONAL. The DESIGN.md alone is sufficient for HTML rendering. When the companion is present, agents read it for voice and component-pattern hints.

## The six mandatory sections

When `STYLE-REFERENCES.md` is generated, all six sections must appear in this order. Sections may have empty content (annotated as "n/a" or "—") but the headers themselves are mandatory.

### 1. Design Lineage

Documents the historical / aesthetic ancestry of the design system. One paragraph plus a bullet list of 2–5 ancestors.

```markdown
## 1. Design Lineage

Descends from the Swiss editorial tradition (Müller-Brockmann grids) by way of
modern monochrome SaaS (Linear, Vercel). Departs from those ancestors by
adopting a warmer neutral palette (`#F7F5F2` vs Linear's `#FAFAFA`) and a
single-accent restraint inherited from Things 3 / Bear.

Ancestors:
- Swiss editorial grid (Müller-Brockmann, 1961)
- Linear (2020+)
- Things 3 / Bear (single-accent restraint)
```

This section gives the agent a high-level mental model. The agent does NOT clone these ancestors literally — it uses them as a rough anchor for type pairing and rhythm.

### 2. Peer References

Public products the design system explicitly wants to look LIKE. Two columns minimum: name + URL, optional column "what we borrow".

```markdown
## 2. Peer References

| Product | URL | What we borrow |
|---|---|---|
| Linear | linear.app | Monochrome palette, sharp 1px rule lines |
| Things 3 | culturedcode.com/things | Single-accent restraint |
| Vercel | vercel.com | Generous whitespace, large heading scale |
```

Peer references inform the agent's choice of component variants when the DESIGN.md is silent. If the brand says "we look like Linear" and DESIGN.md doesn't specify a primary button shape, the agent picks Linear's compact sharp-corner rectangle.

### 3. Anti-References

Public products the design system explicitly does NOT want to look like. Same two-column format as peers, optional "what we reject" column.

```markdown
## 3. Anti-References

| Product | URL | What we reject |
|---|---|---|
| Stripe | stripe.com | Multi-gradient hero washes |
| Slack | slack.com | Heavy use of brand purple in product chrome |
| HubSpot | hubspot.com | Orange-accent overload, dense feature grids |
```

Anti-references are stronger guardrails than peer references. The agent treats anti-references as taboo: if the DESIGN.md leaves a decision ambiguous, the agent picks WHATEVER the anti-reference would NOT do.

### 4. Extended Component Gallery

URLs to specific component patterns the brand has cited as canonical. Differs from peer references: peers give whole-product vibe; gallery cites specific UI fragments.

```markdown
## 4. Extended Component Gallery

- **Card hover state**: `https://linear.app/features` (subtle 1px border darken,
  no shadow lift)
- **Form input**: `https://vercel.com/contact` (8px rounded, 1px border, 16px
  vertical padding)
- **Empty state**: `https://things3.com` (centered icon + 14px caption only,
  no CTA below the fold)
```

This is the most useful section when the brand says "make the card hover like Linear's". The agent visits the URL, observes the actual pattern, applies it.

### 5. Style Vocabulary

Two parallel lists: words the brand uses to describe ITSELF, and words the brand REFUSES to use. Drives microcopy and UI-text voice.

```markdown
## 5. Style Vocabulary

**We sound like:** considered, restrained, editorial, technical, precise,
matter-of-fact, lowercase.

**We never sound like:** playful, friendly, exclamatory, jargon-heavy,
emoji-heavy, marketing-y, upbeat, "hey there!".
```

The agent's microcopy generation reads this section before writing CTAs, empty states, error messages, and toast text.

### 6. Cross-Medium Guide

Translations of the design system into non-web mediums. Used when the brand needs print collateral, video lower-thirds, email templates, presentation decks, or social tiles.

```markdown
## 6. Cross-Medium Guide

| Medium | Adaptation |
|---|---|
| Email (transactional) | Drop shadows entirely; keep all type at 16px |
| Print (1-pager PDF) | Promote `secondary` to body color; black-on-white only |
| Slide deck (16:9) | 48pt heading minimum; reduce palette to primary + neutral |
| Social tile (1200×630) | Heading-only; no body; brand mark bottom-right |
```

This section is consumed when the orchestrator delegates to `amw-email-designer-agent`, the presentation skill, or any non-web output path.

## Emission contract

The companion is emitted by `bin/amw-design-md-emit-companions.py` when invoked with the `--style-references` flag. When the flag is absent (default), only the four core companions emit (`tokens.css`, `tokens.json`, `component-inventory.md`, `usage-prompt.md`).

When `--style-references` is set:

- The emitter populates whatever it can from the DESIGN.md and the awesome-design-md brand-archetype patterns (see [TECH-25-brand-archetypes](TECH-25-brand-archetypes.md)).
- Sections it cannot populate from the source receive a stub header with the marker `<!-- TODO: populate -->`. This signals the human author to fill those sections.
- All section headers are emitted unconditionally — the structural shape is preserved even when content is empty.

## How agents consume it

`amw-wireframe-builder-agent` reads `STYLE-REFERENCES.md` AFTER reading `DESIGN.md` and treats it as a secondary input layer. Concretely:

1. If a token-level decision is ambiguous (DESIGN.md says "primary button, rounded corner" but doesn't specify `1px` vs `2px` border-width), the agent visits the peer-reference URL and observes which value the peer uses.
2. If the anti-reference uses a specific anti-pattern (e.g. Stripe's multi-gradient hero), the agent refuses to use that pattern even if it would technically pass the lint.
3. Microcopy strings are filtered through the §5 Style Vocabulary lists.
4. When delegating to a non-web sub-agent, the orchestrator passes the relevant §6 Cross-Medium Guide row as additional context.

## Linting STYLE-REFERENCES.md

The companion is plain Markdown; no machine-readable schema. The validator (`bin/amw-design-md-validate.py`) does NOT validate it. Two soft checks the human author should run manually:

1. Every URL in §2 Peer References, §3 Anti-References, and §4 Extended Component Gallery should resolve (HTTP 200). Dead links signal the file is stale.
2. The §5 Style Vocabulary "we never sound like" list should not duplicate the "we sound like" list. Contradiction means the brand voice is unresolved.

## Synchronization with DESIGN.md

When `DESIGN.md` is regenerated (e.g. via re-extraction from a refreshed URL), `STYLE-REFERENCES.md` is NOT regenerated automatically — the lineage and references are stable across token refreshes. The companion is only regenerated when the emitter is invoked with `--style-references --force-regenerate`. Otherwise the existing file is left untouched.

## Cross-references

- [TECH-12-companion-files](../../amw-design-md/references/TECH-12-companion-files.md) — the four core companions
- [TECH-22-section-10-11-extended](TECH-22-section-10-11-extended.md) — optional DESIGN.md sections (Iteration Guide / Known Gaps) that complement this file
- [TECH-25-brand-archetypes](TECH-25-brand-archetypes.md) — pre-fill patterns the emitter uses to populate sections from a known archetype
- [TECH-23-section-9-agent-prompt-guide](TECH-23-section-9-agent-prompt-guide.md) — DESIGN.md §9 Agent Prompt Guide overlaps with the §5 Style Vocabulary
