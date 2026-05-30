---
name: TECH-23-section-9-agent-prompt-guide
category: authoring
source: design-extractor agent-prompt patterns (clean-room from GPL design-extractor) + design-swatches §9 template (MIT, direct-port)
license: mixed (clean-room + MIT)
also-in: TECH-22-section-10-11-extended.md, TECH-24-authoring-rules-spec.md, TECH-12-companion-files.md
status: stable
---

# TECH: §9 Agent Prompt Guide

## Table of Contents

- [What it does](#what-it-does)
- [Why §9 exists](#why-9-exists)
- [The four required subsections](#the-four-required-subsections)
  - [1. CSS snippets (3-5)](#1-css-snippets-3-5)
  - [2. Component-authoring instruction sentence](#2-component-authoring-instruction-sentence)
  - [3. "Do not use" clause](#3-do-not-use-clause)
  - [4. Voice descriptor](#4-voice-descriptor)
- [Why copy-paste-ready matters](#why-copy-paste-ready-matters)
- [Worked example](#worked-example)
- [What §9 is NOT](#what-9-is-not)
- [Linting §9](#linting-9)
- [Cross-references](#cross-references)

## What it does

Documents the OPTIONAL Variant 1 §9 "Agent Prompt Guide" — a copy-paste-ready block the human author writes for direct insertion into a coding-agent system prompt. It is NOT a duplicate of `usage-prompt.md` (the auto-emitted companion); it is the human-authored counterpart that lives INSIDE DESIGN.md and reflects judgments the author wants surfaced to every agent that reads the file.

Mixed-license origin: the four-subsection structure is a clean-room re-derivation of the GPL-licensed `design-extractor` agent-prompt convention; the specific subsection content patterns and the voice-descriptor format are direct-ported from the MIT-licensed `design-swatches` §9 template.

## Why §9 exists

The DESIGN.md token table answers WHAT to use. The do/don't list answers what to AVOID. Neither answers HOW to use them when authoring a component from scratch in a session that may only briefly touch the DESIGN.md. §9 is the high-density distillation an agent reads at the start of every session before scanning the full DESIGN.md.

Practical use: when a sub-agent is delegated a small task (e.g. "build a single contact form") and reading the full 200-line DESIGN.md is overkill, the orchestrator may pass only the §9 block as context. The §9 block is small enough to fit in a delegation message and dense enough to constrain the build.

## The four required subsections

When §9 is included, all four subsections must be present in this order.

### 1. CSS snippets (3-5)

Between three and five short, executable CSS snippets the agent pastes verbatim into the component scaffold. These are NOT the full `tokens.css` file (that's the companion) — they are HIGH-LEVERAGE patterns the author has identified as critical.

```markdown
### CSS

```css
/* Primary button (sharp, monochrome) */
.btn-primary {
  background: var(--primary);
  color: var(--on-primary);
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  padding: 12px 24px;
  font: var(--text-sm-medium);
}

/* Card with rule lines, no shadow */
.card {
  background: var(--surface);
  border: 1px solid var(--neutral-200);
  border-radius: var(--radius-md);
  padding: var(--space-4);
}

/* Focus ring (mandatory on every interactive element) */
:focus-visible {
  outline: 2px solid var(--tertiary);
  outline-offset: 2px;
}
```
```

Rules for the CSS snippets:
- Use the CSS-custom-property names declared in the `tokens.css` companion. Do NOT inline raw hex / px values.
- Each snippet is COMPLETE — it compiles on its own; no `@apply`, no Tailwind, no Sass.
- Order from highest-impact to lowest: primary button first, focus ring last.
- Max 15 lines per snippet. Max 5 snippets total.

### 2. Component-authoring instruction sentence

A SINGLE sentence (one period, no semicolons) that tells the agent how to approach component-authoring decisions in this design system. The sentence is voice-neutral but content-loaded.

```markdown
### Authoring instruction

When building a new component, prefer the smaller of two viable type sizes,
use rule lines instead of shadows for elevation, and apply the accent color
exactly once per viewport-worth of vertical scroll.
```

Rules:
- ONE sentence. No bullets, no list, no expansion. The sentence enforces the brand's specific approach to ambiguous decisions.
- Stated as a positive instruction ("prefer X") not a negative ("don't use Y"). The negatives live in subsection 3.
- Names at least 2 concrete decisions the agent will face (size, elevation, accent usage, corner style, etc.).
- Maximum 50 words.

### 3. "Do not use" clause

A bulleted list of patterns the agent must NOT use even if they would otherwise be valid CSS. This subsection is DIFFERENT from §8 Do's and Don'ts — §8 is general brand rules; §9 "do not use" is mechanical anti-patterns specific to code generation.

```markdown
### Do not use

- `box-shadow` for elevation. Use a `1px` rule line with `var(--neutral-200)` instead.
- Gradients of any kind. The brand is monochrome with a single accent.
- Border-radius values outside the declared `--radius-{sm,md,lg}` triplet.
- Tailwind utility classes. The design system is plain CSS / CSS variables only.
- Font-weight values outside `{400, 500, 600}`. No `700`, no `800`, no thin weights.
```

Rules:
- Between 3 and 8 items.
- Each item identifies a CSS PROPERTY, VALUE, or CONSTRUCT — not a brand concept.
- Each item explains WHY in one clause when the reason is non-obvious.

### 4. Voice descriptor

Two parts: one adjective + one sentence. The adjective is the brand's voice in a single word; the sentence is a worked example of that voice applied to a microcopy string.

```markdown
### Voice

Restrained.

The brand sounds like an engineer documenting their own tool — matter-of-fact,
lowercase where idiomatic, never exclamatory.
```

Rules:
- The adjective is exactly ONE word. Not a phrase. Not two words.
- The sentence is the WORKED INTERPRETATION of the adjective, not a definition.
- Common adjectives: editorial, restrained, playful, technical, exuberant, considered, terse, conversational.
- The sentence must imply how a microcopy string changes between voices (lowercase, exclamation marks, hedge words, etc.).

## Why copy-paste-ready matters

Section 9's value depends entirely on its lift-and-drop usability. When a sub-agent is delegated a narrow task, the orchestrator extracts §9 verbatim and prepends it to the delegation message. If §9 contains TODO markers, placeholders, or generic patterns that aren't specific to this brand, the agent operates without effective constraints. The author MUST tune §9 to this brand's specific decisions — never copy a §9 from a different DESIGN.md.

The four-subsection format is enforced because an agent reading a §9 reliably expects: (1) snippets to paste, (2) one instruction to internalize, (3) one veto list to apply, (4) one voice to channel. Reordering or omitting subsections weakens the consume contract.

## Worked example

```markdown
## 9. Agent Prompt Guide

### CSS

```css
.btn-primary {
  background: var(--primary);
  color: var(--on-primary);
  border-radius: var(--radius-sm);
  padding: 12px 24px;
  font: 14px/1.4 'Inter', sans-serif;
  font-weight: 500;
}

.card {
  background: var(--surface);
  border: 1px solid var(--neutral-200);
  border-radius: var(--radius-md);
  padding: 24px;
}

:focus-visible {
  outline: 2px solid var(--tertiary);
  outline-offset: 2px;
}
```

### Authoring instruction

When building a new component, choose the smaller of two viable type sizes, use rule lines instead of shadows for elevation, and place the accent color exactly once per viewport.

### Do not use

- `box-shadow` for elevation — use a 1px border on `--neutral-200`.
- Gradients of any kind.
- Font-weights other than 400, 500, or 600.
- Tailwind utility classes.

### Voice

Restrained.

The brand sounds like an engineer writing release notes — short, specific, all lowercase headings, never exclamatory.
```

## What §9 is NOT

- NOT the `usage-prompt.md` companion. That file is auto-emitted by `bin/amw-design-md-emit-companions.py`. §9 is HAND-AUTHORED and may contain judgments the emitter cannot derive.
- NOT a token table. Tokens live in §2-§6 and the YAML frontmatter.
- NOT a place for examples beyond the four required subsections. Worked examples belong in the body of the DESIGN.md or in `STYLE-REFERENCES.md §4 Extended Component Gallery`.
- NOT a Variant 2 concept. Variant 2 has no agent-prompt section.

## Linting §9

When §9 is present:
- The four subsections must appear in order: CSS, Authoring instruction, Do not use, Voice.
- The CSS block must contain between 3 and 5 standalone snippets.
- The Authoring instruction must be a single sentence (one terminal period).
- The Voice subsection's adjective line must be a single word.
- Token references inside CSS snippets must resolve to declared frontmatter tokens (dead-ref → P1 lint error).

## Cross-references

- [TECH-22-section-10-11-extended](TECH-22-section-10-11-extended.md) — sister optional sections §10 and §11
- [TECH-12-companion-files](TECH-12-companion-files.md) — usage-prompt.md (auto-emitted; complement to §9)
- [TECH-24-authoring-rules-spec](TECH-24-authoring-rules-spec.md) — 13 spec rules including §9 ordering
- [TECH-21-style-references-companion](TECH-21-style-references-companion.md) — `STYLE-REFERENCES.md §5 Style Vocabulary` overlaps with §9 Voice
- [TECH-27-token-interpolation](TECH-27-token-interpolation.md) — token-ref linting inside §9 CSS snippets
