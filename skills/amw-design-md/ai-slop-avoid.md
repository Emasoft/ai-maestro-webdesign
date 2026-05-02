# AI-slop anti-patterns specific to DESIGN.md

A DESIGN.md is a machine-readable specification, not a marketing brochure. Every anti-pattern below makes the file useless to the AI agents that will consume it. Run this checklist before delivering any DESIGN.md.

## Token authoring slop

### S1. Vibes without hex values
Every color in the prose MUST have an exact `#xxxxxx` value either inline or in the YAML frontmatter. Forbidden:
- "a soft, warm cream" with no hex
- "midnight forest green" with no hex anywhere in the file
- "the brand uses a vibrant red" with no hex anywhere

The Google `@google/design.md` linter rejects DESIGN.md files with named-color references that have no token equivalent. The Variant 2 review rubric (`review-rubric.md` check `T1`) does the same.

### S2. Token name and prose name out of sync
If frontmatter has `colors.primary: "#1a1c1e"` and the prose says "**Primary (#0a0a0a)**", they do not match. The reader cannot tell which is canonical. This is a hard validation failure under `bin/amw-design-md-validate.py`.

### S3. Unresolved token references
Frontmatter like `components.button-primary.backgroundColor: "{colors.primary-60}"` when no `colors.primary-60` exists is broken. Token references must resolve. The `npx @google/design.md lint` command catches these.

### S4. Placeholder text never filled in
`{{primary-hex}}`, `TBD`, `???`, `<TODO>`, `[FILL_LATER]` — any of these in a delivered DESIGN.md is slop. Either fill the value or remove the section.

### S5. Color names like "blue" or "red" instead of semantic roles
`primary`, `secondary`, `tertiary`, `surface`, `on-surface`, `error` are semantic. `blue`, `red-500`, `slate-400` are descriptive. Component code should reference semantic tokens, not descriptive ones. A DESIGN.md whose tokens are named `blue / red / green / yellow` invites brand drift.

### S6. Typography without a complete row
Every typography token must include `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`. `letterSpacing` is recommended for display sizes. A row missing any of the four required fields is incomplete and the linter rejects it.

### S7. fontWeight as a string when not a number
`fontWeight: "bold"` is wrong. `fontWeight: 700` is right (or `fontWeight: "700"`). The official spec accepts numbers 100–900, optionally quoted. Named weights (`bold`, `regular`, `light`) are not normative.

## Structural slop

### S8. Sections out of canonical order
Variant 1 fixed order: Overview / Colors / Typography / Layout / Elevation & Depth / Shapes / Components / Do's and Don'ts. A file with `## Components` before `## Typography` is rejected by the linter.

### S9. Duplicate section headings
`## Colors` appearing twice is a hard error. The linter rejects the file.

### S10. Missing the `## Colors` section
At minimum the `primary` color palette must be defined. A DESIGN.md without `## Colors` is invalid.

### S11. YAML frontmatter not at line 1
Frontmatter must start at line 1 with exactly `---`. A blank line, a UTF-8 BOM, or any prose before the opening `---` breaks the parser.

### S12. YAML frontmatter that is not actually YAML
Tabs instead of spaces, unquoted hex strings (`primary: #1a1c1e` without quotes), missing colons. `bin/amw-design-md-validate.py` catches these. So does `npx @google/design.md lint`.

## Prose slop

### S13. Marketing copy where rules belong
"Our brand evokes a sense of timeless elegance combined with modern dynamism" is brochure copy. Replace with concrete rules: "Headings use Public Sans Semibold 600. Body uses Public Sans Regular 400 at 16 px. CTAs use the primary color exclusively — never tertiary or secondary."

### S14. Do's and Don'ts that are vague
- Bad: "Don't be inconsistent" / "Do use good judgment"
- Good: "Don't mix rounded and sharp corners in the same view" / "Do use the primary color only for the single most important action per screen"

### S15. The `## Overview` section is a wall of adjectives
A useful Overview gives a designer an actionable mental model in 3-6 sentences: who the user is, what emotion the UI should evoke, what density it should have, what philosophical choices distinguish it. "Playful, dense, opinionated" is more useful than "bold, vibrant, modern, clean".

## Variant 2 — community 9-section specific

### S16. Section 7 (Do's and Don'ts) with fewer than 3 dos and 3 don'ts
The review rubric (`T6`) requires minimum 3 of each. Fewer indicates the file was not actually completed.

### S17. Section 8 (Responsive Behavior) without explicit px breakpoints
"Mobile first" is not a breakpoint. `sm: 640px / md: 768px / lg: 1024px / xl: 1280px / 2xl: 1536px` (or whatever the brand uses) is. Vague responsive sections are slop.

### S18. Section 9 (Agent Prompt Guide) missing a quick-color-reference
The whole point of Section 9 is to give the AI a TL;DR at the bottom of the file (LLMs attend strongly to recent context). Missing the quick reference defeats the format.

### S19. Mermaid component-state diagram absent
The 9-section template (`references/community-9-section-template.md`) includes a `mermaid stateDiagram-v2` block under Section 4. Reviewers consider its absence a minor failure (rubric `S5/S6`).

## Conversion slop

### S20. Variant 2 → Variant 1 conversion that loses data
The community 9-section format has more granular tokens than the official format (semantic roles, brand-tinted shadow rgba formulas, breakpoint tables). When converting V2 → V1, the converter MUST place V2-specific data in either the prose body or in a custom section flagged as non-normative. Silent data loss is a slop pattern.

## Companion-file slop

### S21. tokens.css with hex values that don't match DESIGN.md frontmatter
If `DESIGN.md` says `primary: #1a1c1e` and `tokens.css` says `--primary: #0a0a0a`, the companion files have drifted. `bin/amw-design-md-emit-companions.py` regenerates them from the source-of-truth DESIGN.md to prevent this.

### S22. tokens.json that is not W3C Design Tokens format
The W3C format requires `$value` and `$type` fields per token. A flat `{"primary": "#1a1c1e"}` is NOT a tokens.json — it is a plain JSON object. Reviewers check for `$value` / `$type`.

## Final delivery gate

Before delivering any authored or converted DESIGN.md:

1. Run `bin/amw-design-md-lint.sh <file>` — must exit 0.
2. Run `bin/amw-design-md-validate.py <file>` — must report no errors.
3. Run `bin/amw-design-md-contrast.py <file>` — color pairs flagged below 4.5:1 must be acknowledged in the file's `## Do's and Don'ts` or escalated as `warnings` in the agent's return contract.
4. Spot-check Section S1 / S5 / S15 / S18 manually.

A file that fails 1, 2, or 3 is not delivered. A file that fails the spot-check is iterated.
