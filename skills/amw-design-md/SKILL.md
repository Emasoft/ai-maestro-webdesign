---
name: amw-design-md
description: Author, lint, extract, audit, and convert DESIGN.md design-system specifications. Triggers on "create DESIGN.md", "lint DESIGN.md", "extract DESIGN.md from URL/Tailwind/codebase", "audit DESIGN.md", "DESIGN.md companions". Does NOT trigger on generic "design system", "extract design tokens" — those route to amw-design-principles or amw-design-extract. Use when authoring, linting, or converting a DESIGN.md spec. Trigger with /amw-design-md-create.
version: 0.1.0
---

# AMW Design.md

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill owns the DESIGN.md format end-to-end (author, parse, lint, validate, audit, convert, emit companions). It does NOT replace the orchestrator. DESIGN.md is one of several optional input formats accepted by the plugin (peer to ASCII wireframes, mockup images, slideshows, URL "copy this style" briefs, and prose). Triggers are DESIGN.md-specific only.

## Overview

Owns the DESIGN.md format end-to-end: author, lint, validate, audit, convert, and emit companion files (tokens.css, tokens.json, component-inventory.md). Supports both the official Variant 1 (`<@google/design.md>`) and the community 9-section Variant 2.

---

## Activation

Callable directly via the nine `/amw-design-md-*` commands. Also invoked by the orchestrator when the user provides a DESIGN.md file as input or asks for one as a deliverable. In main-agent mode the orchestrator may delegate to one of three sub-agents (`amw-design-md-author-agent`, `amw-design-md-extractor-agent`, `amw-design-md-auditor-agent`) which read this SKILL.md and its references to do their job.

This skill is **autonomous and self-contained** — any agent can read this SKILL.md and the referenced files and execute the recipes without re-routing through the orchestrator.

## Position in flow

INPUT or OUTPUT (peer status). DESIGN.md is one of six input formats the plugin accepts:

1. User provides a DESIGN.md (Variant 1 official `<@google/design.md>` or Variant 2 community 9-section)
2. User provides an ASCII wireframe / sketch
3. User provides a mockup image
4. User provides a slideshow
5. User says "copy the style from this URL"
6. User describes the wishes in prose only

These are **peers**, not a hierarchy. DESIGN.md is one option. When the user provides a DESIGN.md, the parser/validator path here normalizes it into canonical tokens that any downstream Phase B agent (notably `amw-wireframe-builder-agent`) can consume. When the user asks for a DESIGN.md as the deliverable, the author path here produces a Variant 1 file (plus optional companions).

## What this skill is NOT

- Not a brand database. The pre-paywall snapshot of 58 example DESIGN.md files lives in `docs_dev/extracted/google-labs/awesome-design-md-pre-paywall-main/` and is reference-only.
- Not a UI generator. After extracting tokens or authoring a DESIGN.md, the actual HTML is built by `amw-wireframe-builder-agent` via the `amw-ascii-to-html` skill.
- Not the orchestrator. Generic "design system" requests route to `amw-design-principles`. Only DESIGN.md-specific requests reach here.

## Trigger conditions

Fires on these specific phrasings:

- "create DESIGN.md" / "author DESIGN.md" / "make a DESIGN.md"
- "extract DESIGN.md from <url>" / "extract DESIGN.md from this Tailwind config" / "extract DESIGN.md from this codebase"
- "lint DESIGN.md" / "validate my DESIGN.md" / "check my DESIGN.md frontmatter"
- "audit DESIGN.md" / "five-pass audit on DESIGN.md" / "review DESIGN.md against the code"
- "convert DESIGN.md" / "convert Variant 2 DESIGN.md to Variant 1" / "convert 9-section DESIGN.md to canonical"
- "emit DESIGN.md companions" / "emit tokens.css from DESIGN.md" / "emit tokens.json from DESIGN.md"
- "diff two DESIGN.md files" / "design.md diff"

Does NOT fire on:

- "design a landing page" → `amw-design-principles` (orchestrator)
- "extract design tokens from <url>" without DESIGN.md keyword → `amw-design-extract`
- "build a token spec" / "set up a design system" → `amw-design-principles`
- "make a UI" / "style this page" → orchestrator

## How it works

The skill ships:

- **Two canonical specs** documented in [canonical-spec-google-alpha](references/canonical-spec-google-alpha.md) (Variant 1 — official `<@google/design.md>`, primary) and [community-9-section-spec](references/community-9-section-spec.md) (Variant 2 — VoltAgent community 9-section, accepted-with-mapping).
  > File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Top-level fields · Type definitions · Component property tokens (spec.md L312-L319) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Section content guidance · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references
- **16 TECH-NN reference files** under `references/TECH-*.md` covering frontmatter, color tokens, typography tokens, component tokens, token references, do/don'ts authoring, URL extraction, codebase extraction, multi-page extraction, Tailwind conversion, validation/lint, companion files, V2→V1 conversion, validation failure recovery, DESIGN.md as input, and CJK localization ([TECH-cjk-localization](references/TECH-cjk-localization.md)).
  > What it does · When to use · How it works · Typography (per language) · Layout · Punctuation + line breaking · Cultural symbolism · Microcopy patterns · Locale machinery · SEO impacts · Performance · Minimal example · Gotchas · Cross-references · Source attribution
- **Three templates** under `references/` — Variant 1 skeleton, Variant 2 skeleton, and a CLAUDE.md snippet for projects that adopt DESIGN.md.
- **Two audit/quality docs** — [review-rubric](references/review-rubric.md) (DESIGN.md quality scoring) and [audit-passes](references/audit-passes.md) (5-pass audit: structural / drift / a11y / completeness / consistency).
  > [review-rubric.md] Output schema · Structural checks (must-pass) · Variant 1 (canonical) · Variant 2 (community) · Token-quality checks (must-pass — both variants) · Sync checks (must-pass — when companion files exist) · Content-integrity checks (soft — affects score) · A11y checks (must-pass — both variants) · Scoring · What the rubric does NOT do · How `amw-design-md-author-agent` uses the rubric on its own output · Cross-references
  > [audit-passes.md] Pass 1 — Structural · Pass 2 — Drift · Pass 3 — Accessibility · Pass 4 — Completeness · Pass 5 — Consistency · Output file format · What the auditor does NOT do · Pre-flight checks · Cross-references
- **Ten bin scripts** under `<plugin-root>/bin/amw-design-md-*` — pure-local Python and TypeScript ports plus thin shell wrappers around the official `npx @google/design.md` CLI.

## Prerequisites

Standard plugin runtime — no skill-specific prerequisites beyond the global plugin dependencies.

## Instructions

1. Identify the requested operation: author, lint/validate, extract from URL, extract from Tailwind config, extract from codebase, audit, convert Variant 2 → Variant 1, emit companion files, or diff two revisions.
2. For authoring: read [canonical-template](references/canonical-template.md), fill from brief/interview/codebase/URL using the appropriate bin script, then validate with `bin/amw-design-md-lint.sh`.
  > Filling guide · Cross-references
3. For extraction: choose `bin/amw-design-md-from-url.sh`, `bin/amw-design-md-from-tailwind.mjs`, or `bin/amw-design-md-from-codebase.py` based on the source type.
4. For auditing: spawn `amw-design-md-auditor-agent`; the auditor runs the 5-pass audit and writes a `<file>.critique.md` adjacent to the input.
5. For companion file generation: run `bin/amw-design-md-emit-companions.py` to produce `tokens.css`, `tokens.json`, `component-inventory.md`, and `usage-prompt.md`.
6. Validate every DESIGN.md output before delivery; fail fast if the linter reports errors.

## Operations the skill exposes

### Author a DESIGN.md
Read [canonical-template](references/canonical-template.md). Fill from a brief / interview / codebase scan / URL extraction (delegating to one of the bin scripts as appropriate). Validate via `bin/amw-design-md-lint.sh` before declaring done.

### Lint / validate a DESIGN.md
Run `bin/amw-design-md-lint.sh <path>` for the official linter. Run `bin/amw-design-md-validate.py <path>` for offline pure-Python validation (frontmatter + section order + token-reference resolution).

### Extract a DESIGN.md from a live URL
Invoke `bin/amw-design-md-from-url.sh <url> <output-path>` which delegates DOM and computed-style extraction to the plugin's existing `amw-dev-browser` skill, then emits Variant 1 frontmatter.

### Extract a DESIGN.md from a Tailwind config
Run `node bin/amw-design-md-from-tailwind.mjs --config <tailwind.config.ts> --css <globals.css> --out <DESIGN.md>`. Pure-local Node.js port of the upstream tool. Resolves CSS-var references and annotates color pairs with WCAG-AA contrast.

### Extract a DESIGN.md from a codebase scan
Run `bin/amw-design-md-from-codebase.py <project-root>`. Pure-Python scanner that detects shadcn/Tailwind/Chakra/vanilla-CSS/styled-components and emits a draft DESIGN.md.

### Audit a DESIGN.md
Spawn `amw-design-md-auditor-agent`. The auditor runs the 5-pass audit per [audit-passes](references/audit-passes.md) and writes a `<file>.critique.md` adjacent to the input.

### Convert Variant 2 → Variant 1
Run `bin/amw-design-md-convert-v2-to-v1.py <variant2.md> <variant1.md>`. Maps the 9-section community format to the canonical 8-section + YAML frontmatter format.

### Emit companion files
Run `bin/amw-design-md-emit-companions.py <DESIGN.md> <output-dir>`. Emits `tokens.css` (CSS custom properties), `tokens.json` (W3C Design Tokens), `component-inventory.md`, and `usage-prompt.md`.

### Diff two DESIGN.md revisions
Run `bin/amw-design-md-diff.sh <a.md> <b.md>`. Wrapper around `npx @google/design.md diff`.

## When the result is consumed downstream

When the user provides a DESIGN.md and then proceeds to Phase B (HTML rendering), `amw-wireframe-builder-agent` reads the DESIGN.md, validates it via `bin/amw-design-md-lint.sh`, and treats its tokens as canonical. On lint failure, the wireframe-builder reports and STOPS — the DESIGN.md path is symmetric with brand-researcher's extracted tokens, ascii-sketch's approved variant, and prose. See [TECH-15-design-md-as-input](references/TECH-15-design-md-as-input.md).
> [TECH-15-design-md-as-input.md] What it does · When this TECH applies · The wireframe-builder's flow when DESIGN.md is the input · Token mapping — DESIGN.md to wireframe-builder's `brand_tokens` shape · Component tokens — direct passthrough · Failure paths · DESIGN.md fails lint · DESIGN.md is Variant 2 · DESIGN.md missing required fields · CLAUDE.md-coupled projects · Companion-file consumption · Symmetry with non-DESIGN.md inputs · Cross-references

## Hard rules

1. The skill produces Variant 1 (official `<@google/design.md>`) as canonical output by default. Variant 2 is accepted as input via the converter.
2. The skill runs no paywalled service, no API key beyond what `amw-dev-browser` already requires, and no Chrome extension. The official CLI is `npx`-installable, no API key, no remote calls.
3. The skill never re-emits broad design vocabulary in tool-call text — that would re-trigger the orchestrator. See [skill-invocation-protocol](../amw-design-principles/references/skill-invocation-protocol.md).
  > The problem · The protocol · DO · DON'T · Examples · Correct: agent produces an HTML mockup from approved ASCII · Incorrect: agent tries to delegate back through commands · Correct: agent needs to produce a diagram in Mermaid format · Incorrect: agent uses Skill tool with a vague English prompt · Enforcement
4. Every authored DESIGN.md MUST pass `bin/amw-design-md-lint.sh` before being delivered. Lint failure halts delivery.
5. WCAG-AA contrast checks via `bin/amw-design-md-contrast.py` are run on every authored DESIGN.md. Failures go to `warnings`, not silent omission.

## Output

Produces a single artifact at the path specified in §Operations — a DESIGN.md file (Variant 1) plus optional companion files.

## Error Handling

On failure, the skill emits a non-zero exit code or returns a structured error in the response. See bin/ scripts for tool-specific error semantics.

## Examples

**Concrete example — author DESIGN.md from a brief (Variant 1):**

- **Input:** "We're building a fintech dashboard. Brand color is `#0F4C81` (deep blue). Secondary `#FFD23F` (sunflower amber). Body type Inter, headings Manrope. WCAG AA-compliant."
- **Operation:** lint gate runs `amw-design-md-lint.sh` (wraps `npx @google/design.md lint`). Contrast pre-flight runs `amw-design-md-contrast.py` on every color pair.
- **Output:** `DESIGN.md` (Variant 1, YAML frontmatter + 8 fixed sections), `tokens.css` (CSS custom properties), `tokens.json` (W3C Design Tokens), `component-inventory.md`, `usage-prompt.md` (companion files emitted by `amw-design-md-emit-companions.py`).

**Concrete example — extract DESIGN.md from a live URL:**

- **Input:** `https://stripe.com` and target Variant 1 schema.
- **Operation:** `amw-design-md-from-url.sh` delegates to `amw-dev-browser/` for DOM + computed styles, then transcribes faithfully into the canonical Variant 1 schema.
- **Output:** `stripe.DESIGN.md` capturing detected tokens (color, type, spacing, radii) with one-to-one source attribution.

See the worked examples in the per-mode sub-sections above and in references/.

## Resources

- [ai-slop-avoid](./ai-slop-avoid.md) — DESIGN.md-specific anti-patterns
  > Token authoring slop · S1. Vibes without hex values · S2. Token name and prose name out of sync · S3. Unresolved token references · S4. Placeholder text never filled in · S5. Color names like "blue" or "red" instead of semantic roles · S6. Typography without a complete row · S7. fontWeight as a string when not a number · Structural slop · S8. Sections out of canonical order · S9. Duplicate section headings · S10. Missing the `## Colors` section · S11. YAML frontmatter not at line 1 · S12. YAML frontmatter that is not actually YAML · Prose slop · S13. Marketing copy where rules belong · S14. Do's and Don'ts that are vague · S15. The `## Overview` section is a wall of adjectives · Variant 2 — community 9-section specific · S16. Section 7 (Do's and Don'ts) with fewer than 3 dos and 3 don'ts · S17. Section 8 (Responsive Behavior) without explicit px breakpoints · S18. Section 9 (Agent Prompt Guide) missing a quick-color-reference · S19. Mermaid component-state diagram absent · Conversion slop · S20. Variant 2 → Variant 1 conversion that loses data · Companion-file slop · S21. tokens.css with hex values that don't match DESIGN.md frontmatter · S22. tokens.json that is not W3C Design Tokens format · Final delivery gate
- [canonical-spec-google-alpha](./references/canonical-spec-google-alpha.md) — Variant 1 spec, source-cited
  > File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Top-level fields · Type definitions · Component property tokens (spec.md L312-L319) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Section content guidance · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references
- [community-9-section-spec](./references/community-9-section-spec.md) — Variant 2 spec, source-cited
  > Document head (DESIGN_MD_SPEC L13-L17) · Section count and order (DESIGN_MD_SPEC L25-L36) · No YAML frontmatter · Section specifications · Section 1 — Visual Theme & Atmosphere (DESIGN_MD_SPEC L43-L67) · Section 2 — Color Palette & Roles (DESIGN_MD_SPEC L72-L106) · Section 3 — Typography Rules (DESIGN_MD_SPEC L108-L166) · Section 4 — Component Stylings (DESIGN_MD_SPEC L169-L216) · Section 5 — Layout Principles (DESIGN_MD_SPEC L219-L246) · Section 6 — Depth & Elevation · Section 7 — Do's and Don'ts · Section 8 — Responsive Behavior · Section 9 — Agent Prompt Guide · XML boundary tags (Variant 2 enhancement) · Mermaid component-state diagram · Comparison vs Variant 1 · Cross-references
- [extension-sections-10-14](./references/extension-sections-10-14.md) — optional Naming / Page Specs / Composite Components / Token Mapping / i18n
  > Section 10 — Naming Convention (Page > Section > Block > Element) · Section 11 — Page Specifications · Section 12 — Composite Components · Section 13 — Token Mapping · Section 14 — i18n References · When to use these extensions · Cross-references · "What to build" (page-level specs, requirements) · Component composition (LoginPage as a unit, not just Button + Input) · Token-to-Tailwind / token-to-CSS-var mapping table · i18n string-resource mapping
- [canonical-template](./references/canonical-template.md) — Variant 1 skeleton
  > Filling guide · Cross-references
- [community-9-section-template](./references/community-9-section-template.md) — Variant 2 skeleton
  > Optional extension sections · Validation · Cross-references
- [claude-md-snippet](./references/claude-md-snippet.md) — CLAUDE.md addition for projects using DESIGN.md
  > Snippet — paste into the project's `CLAUDE.md` · Where this goes in CLAUDE.md · What `{{placeholders}}` get filled with · Cross-references
- [review-rubric](./references/review-rubric.md) — quality-scoring rubric
  > Output schema · Structural checks (must-pass) · Variant 1 (canonical) · Variant 2 (community) · Token-quality checks (must-pass — both variants) · Sync checks (must-pass — when companion files exist) · Content-integrity checks (soft — affects score) · A11y checks (must-pass — both variants) · Scoring · What the rubric does NOT do · How `amw-design-md-author-agent` uses the rubric on its own output · Cross-references
- [audit-passes](./references/audit-passes.md) — 5-pass audit
  > Pass 1 — Structural · Pass 2 — Drift · Pass 3 — Accessibility · Pass 4 — Completeness · Pass 5 — Consistency · Output file format · What the auditor does NOT do · Pre-flight checks · Cross-references
- [TECH-01-yaml-frontmatter](./references/TECH-01-yaml-frontmatter.md) through `TECH-15-design-md-as-input.md`
  > What it does · When to use · Hard rules · Delimiters · Top-level fields · Value type rules · Token references · YAML quoting rules · Common gotchas · Worked example — minimal valid frontmatter · Worked example — token reference inside components · Validation · Cross-references
- [TECH-cjk-localization](./references/TECH-cjk-localization.md) — CJK localization (JP/KO/ZH)
  > What it does · When to use · How it works · Typography (per language) · Layout · Punctuation + line breaking · Cultural symbolism · Microcopy patterns · Locale machinery · SEO impacts · Performance · Minimal example · Gotchas · Cross-references · Source attribution
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (this skill is downstream)
- [SKILL](../amw-dev-browser/SKILL.md) — browser primitive used by URL extraction
- [SKILL](../amw-design-extract/SKILL.md) — sibling URL-extraction skill (looser format; this skill is the strict-format counterpart)
- `<plugin-root>/bin/amw-design-md-*.{sh,py,ts}` — ten bin scripts
