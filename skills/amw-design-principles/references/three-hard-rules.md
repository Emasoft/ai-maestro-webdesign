# The three hard rules — full text

Violating any one of these is a failure. Summary in the orchestrator SKILL.md; full text and last-resort path here.

## Rule 1: Gather design context before designing

There is no "I have a good idea in my head, let me start coding." Before any design work, obtain at least **one** of:

- An existing UI kit or design system file
- Brand tokens (color palette, font stack, spacing rules, radius scale)
- Screenshots of reference sites or products
- Components already in the project's codebase
- An explicit brand manual (e.g. Equation brand guide)

**If none of these are available → ask the user first,** or together pin down a "visual DNA anchor" (e.g. "like Aesop — cream-white + serif + whitespace").

The recommended structured form for a brand-token spec — both as Phase A *output* (when the user asks "give me a design system") and as Phase A *input* (when the user shows up with one already) — is a Variant 1 DESIGN.md (the official `<@google/design.md>` format). The plugin's `amw-design-md` skill owns authoring, extraction, lint, audit, conversion, and companion emission. When this rule fires and the user has neither a UI kit nor a brand manual, offer `/amw-design-md-create` (5-Q interview), `/amw-design-md-from-url <url>` (extract from a reference site), or `/amw-design-md-from-codebase` (scan an existing project). The produced DESIGN.md becomes the canonical token source for Phase B sub-agents (wireframe-builder, component-library-architect, accessibility-auditor).

> Mocking from scratch is a **last resort**. It produces generic AI slop.

### Last-resort path (when context is genuinely unavailable)

When the user has supplied no design system and cannot name a reference:

1. **Invoke the `ui-ux-reasoning` sub-skill** for a library of 50+ visual styles / 21+ palettes / 50+ font combinations as ammunition.
2. **Vocalize assumptions:** state out loud *"I am going with X typeface + Y color temperature + Z layout rhythm"* and wait for the user's nod before going further.
3. If you have to proceed without confirmation, annotate the file header: *"These are temporary visual assumptions. Replace with real brand assets when available."*

**Stance:** mocking from scratch only produces "barely passable" generic output. It never produces premium work.

## Rule 2: Deliver at least three variants, baseline → advanced → experimental

A single answer is never the full answer. Every design task must include:

- **Variant A (Baseline):** strictly follows the existing design system; zero risk.
- **Variant B (Advanced):** builds on the system but shifts one dimension (color, layout, typographic rhythm).
- **Variant C (Experimental):** allowed to break the system — new metaphors, novel layouts, bold typography.

Present them side-by-side (tabs, stacked cards, multi-slide deck) so the user can mix and match.

**The plan-phase medium for variant exploration is ASCII via `/amw-sketch`, not HTML.** See the "ASCII-first plan phase" section in SKILL.md — Rule 2 is almost always easier to satisfy in ASCII than in HTML.

## Rule 3: Reject every AI-slop pattern

Specific patterns are an instant tell for AI generation. The complete list is in [../ai-slop-avoid.md](../ai-slop-avoid.md) (26 patterns + positive-stance section). Highlights:

- Large purple-blue or pink-orange linear gradients
- Rounded-card + 4px left accent bar
- AI-drawn SVG illustrations of people / mascots / scenes
- Inter / Roboto / Arial / Fraunces / system default fonts
- Emoji carpet-bombing (unless the brand explicitly uses emoji)
- Filler data, icons, statistics added just to fill space
- Invented testimonials, placeholder portraits
- "Trust markers" / customer logo walls on every section

Every HTML output runs a final scan against [../ai-slop-avoid.md](../ai-slop-avoid.md) before delivery.
