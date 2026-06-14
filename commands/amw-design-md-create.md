---
name: amw-design-md-create
description: "Author a fresh Variant 1 DESIGN.md from a brief, codebase, URL, or 5-question interactive interview. Spawns amw-design-md-author-agent. The agent assembles YAML frontmatter (colors / typography / rounded / spacing / components) plus the 8 canonical prose sections, runs lint + WCAG contrast checks, and writes the file plus optional companions (tokens.css, tokens.json, component-inventory.md, usage-prompt.md)."
---

# /amw-design-md-create

Create a new Variant 1 DESIGN.md (the canonical `@google/design.md` format) from a brief, an existing codebase, a reference URL, or a structured 5-question interview.

## Arguments

`$ARGUMENTS` may contain any combination of:

- A free-form brief in quotes: `"luxury Bora Bora resort, French + English, sand + ocean palette"`
- A path: `./` (treated as `input_type=codebase`) or `./tailwind.config.ts ./app/globals.css` (treated as `input_type=tailwind`)
- A URL: `https://example.com` (treated as `input_type=url` — but the dedicated `/amw-design-md-from-url` is preferred)
- An explicit `--input-type {brief|codebase|tailwind|url|interview}` flag
- An explicit `--out <path>` flag (default: `./DESIGN.md`)
- Companion targets: `--companions css,json,inventory,prompt`

If no `$ARGUMENTS` is provided, the command runs the **5-question interview** path (Path D).

## Action

### 1. Detect input type

Inspect `$ARGUMENTS`:

- A bare URL → `input_type=url`. Recommend `/amw-design-md-from-url` instead and ask for confirmation.
- A `tailwind.config.{js,ts,mjs}` path + a `.css` path → `input_type=tailwind`. Recommend `/amw-design-md-from-tailwind` instead.
- A directory path → `input_type=codebase`. Recommend `/amw-design-md-from-codebase`.
- A quoted brief → `input_type=brief`.
- Empty → `input_type=interview`.

### 2. Spawn `amw-design-md-author-agent`

Pass the structured input contract per [amw-design-md-author-agent](../agents/amw-design-md-author-agent.md) §5. Wait for the agent's YAML return contract.

### 3. If `input_type=interview`, conduct the 5-question interview

Ask exactly five questions, one per turn:

1. **Brand personality** — "How would you describe the brand voice in 2–3 adjectives? (e.g., bold and modern; warm and crafted; technical and precise)"
2. **Core audience** — "Who is the primary user? (e.g., enterprise developers; first-time home buyers; healthcare professionals)"
3. **Key action** — "What is the single most important thing the user should do? (e.g., sign up for beta; book a consultation; buy this product)"
4. **Palette preference** — "Color direction? (e.g., dark with teal accent; sand + ocean; minimal monochrome with one signal color)"
5. **Competitor reference** — "One reference URL whose visual style is in the right ballpark? (or 'none' if you'd rather not anchor on a competitor)"

Pass the answers as the `interview_answers` block of the input contract.

### 4. Surface the result

After the agent returns, show:

- The file path of the produced DESIGN.md
- Lint status (PASS / PARTIAL with errors)
- Contrast warnings, if any
- Companion file paths, if `--companions` was passed
- Next-step recommendation (typically: pass to `/amw-ascii-to-html` or `/amw-sketch` with the DESIGN.md as the token source)

## Non-negotiables

- **Lint gate is mandatory.** A DESIGN.md that fails P0 lint is delivered as `status=partial` with the failures listed; it is never silently shipped.
- **No invented tokens.** When the input is sparse, missing tokens stay as `# TODO:` placeholders in the YAML rather than being fabricated.
- **WCAG-AA contrast check** runs by default. Failing pairs go to warnings; the user decides whether to override the source's intentional contrast choice.
- **Variant 1 (canonical) is the default output.** Variant 2 (community 9-section) requires an explicit request and currently relies on manual re-formatting from the Variant 1 source.

## Failure modes

- Empty `$ARGUMENTS` and the user declines the interview → stop and ask what they want as input.
- Mis-routed input (e.g., user pastes a Figma link) → the agent returns `status=failed` with `next_action=escalate_to_user`. Surface the message verbatim.
- Lint fails repeatedly → pass through the agent's `blocking_issues` list and stop.

## Cross-references

- [amw-design-md-author-agent](../agents/amw-design-md-author-agent.md)
- [SKILL](../skills/amw-design-md/SKILL.md)
- [canonical-spec-google-alpha](../skills/amw-design-md-spec/references/canonical-spec-google-alpha.md)
> [canonical-spec-google-alpha.md] File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references
- [canonical-template](../skills/amw-design-md-spec/references/canonical-template.md)
> [canonical-template.md] Filling guide · Cross-references
- `bin/amw-design-md-lint.sh` (lint gate)
- `bin/amw-design-md-contrast.py` (WCAG check)
- `bin/amw-design-md-emit-companions.py` (companions)
