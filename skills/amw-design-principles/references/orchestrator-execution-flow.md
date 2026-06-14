# Orchestrator execution flow + ASCII-first plan phase

The step-by-step recipe the orchestrator walks on every Main-agent-mode
request, plus the ASCII-first plan-phase rules. `SKILL.md` keeps a compact
pointer to this file and the relevant TOC embeds.

## Table of Contents

- [Instructions](#instructions)
- [ASCII-first plan phase (the default workflow)](#ascii-first-plan-phase-the-default-workflow)

## Instructions

1. Read the brief and decide if this skill fires (broad design vocabulary: design, UI, mockup, landing page, wireframe, prototype, slide, deck, poster, website).
2. Gather context: request UI kit, brand assets, or reference examples; use `amw-ui-ux-reasoning` as last resort if none are available.
3. Run the question checklist from [question-templates](../question-templates.md) (ask ≥ 10 questions), then declare the visual system (font + palette + spacing rhythm).
4. Run `/amw-sketch` to iterate ≥ 3 ASCII variants with the user; loop until an explicit satisfaction token is received.
5. Apply the AI-slop-avoid.md gate over the approved direction before conversion.
6. Convert to HTML via `/amw-ascii-to-html`, apply tokens, and deliver via `/amw-preview`.
7. Route specialized requests (diagrams, infographics, video, SEO, forms) to the appropriate executor skill — see [downstream-executors](./downstream-executors.md) for the full routing table.

## ASCII-first plan phase (the default workflow)

**When the user asks for a webpage design, the plan phase runs in ASCII, not HTML.** Iterate on position, size, alignment, and component choice in ASCII until the user is explicitly satisfied; only then convert. The flow is: (1) `design-principles` applies Rules 1/2/3 → (2) `/amw-sketch` loops 3 ASCII variants ↔ feedback → (3) `/amw-ascii-to-html` (terminal) applies tokens, wraps chrome, previews via `/amw-preview`.

The loop is cheap (ASCII costs ~1% of HTML-iteration tokens, so 10+ revisions without context decay). It ends only on the canonical satisfaction tokens (the same approval gate the SKILL.md states); ambiguous acknowledgement (`looks good`, `sure`, `ok`, `fine`) is NOT approval — ask a clarifying question first. Skip the loop only when the user has already committed to a layout (e.g. they pasted a wireframe and said "build this"); otherwise ASCII-first is default.
