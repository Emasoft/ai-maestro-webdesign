---
name: amw-design-md
description: Author, lint, extract, audit, and convert DESIGN.md design-system specifications. Triggers on narrow DESIGN.md-specific phrasing only - "create DESIGN.md", "author DESIGN.md", "lint DESIGN.md", "extract DESIGN.md from this URL", "extract DESIGN.md from this Tailwind config", "extract DESIGN.md from this codebase", "audit DESIGN.md", "convert DESIGN.md", "design-token spec", "design-system markdown", "DESIGN.md companions", "design.md frontmatter validation". Do NOT trigger on generic vocabulary like "design", "design system", "make a UI", "extract design tokens", "build a token spec" - those route to amw-design-principles or amw-design-extract via the orchestrator.
version: 0.1.0
---

# AMW Design.md

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> This skill owns the DESIGN.md format end-to-end (author, parse, lint, validate, audit, convert, emit companions). It does NOT replace the orchestrator. DESIGN.md is one of several optional input formats accepted by the plugin (peer to ASCII wireframes, mockup images, slideshows, URL "copy this style" briefs, and prose). Triggers are DESIGN.md-specific only.

---

## Activation

Callable directly via the nine `/amw-design-md-*` commands. Also invoked by the orchestrator when the user provides a DESIGN.md file as input or asks for one as a deliverable. In main-agent mode the orchestrator may delegate to one of three sub-agents (`amw-design-md-author-agent`, `amw-design-md-extractor-agent`, `amw-design-md-auditor-agent`) which read this SKILL.md and its references to do their job.

This skill is **autonomous and self-contained** — any agent can read this SKILL.md and the referenced files and execute the recipes without re-routing through the orchestrator.

## Position in flow

INPUT or OUTPUT (peer status). DESIGN.md is one of six input formats the plugin accepts:

1. User provides a DESIGN.md (Variant 1 official `@google/design.md` or Variant 2 community 9-section)
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

- **Two canonical specs** documented in `references/canonical-spec-google-alpha.md` (Variant 1 — official `@google/design.md`, primary) and `references/community-9-section-spec.md` (Variant 2 — VoltAgent community 9-section, accepted-with-mapping).
- **16 TECH-NN reference files** under `references/TECH-*.md` covering frontmatter, color tokens, typography tokens, component tokens, token references, do/don'ts authoring, URL extraction, codebase extraction, multi-page extraction, Tailwind conversion, validation/lint, companion files, V2→V1 conversion, validation failure recovery, DESIGN.md as input, and CJK localization (`references/TECH-cjk-localization.md`).
- **Three templates** under `references/templates/` — Variant 1 skeleton, Variant 2 skeleton, and a CLAUDE.md snippet for projects that adopt DESIGN.md.
- **Two audit/quality docs** — `references/review-rubric.md` (DESIGN.md quality scoring) and `references/audit-passes.md` (5-pass audit: structural / drift / a11y / completeness / consistency).
- **Ten bin scripts** under `<plugin-root>/bin/amw-design-md-*` — pure-local Python and TypeScript ports plus thin shell wrappers around the official `npx @google/design.md` CLI.

## Operations the skill exposes

### Author a DESIGN.md
Read `references/templates/canonical-template.md`. Fill from a brief / interview / codebase scan / URL extraction (delegating to one of the bin scripts as appropriate). Validate via `bin/amw-design-md-lint.sh` before declaring done.

### Lint / validate a DESIGN.md
Run `bin/amw-design-md-lint.sh <path>` for the official linter. Run `bin/amw-design-md-validate.py <path>` for offline pure-Python validation (frontmatter + section order + token-reference resolution).

### Extract a DESIGN.md from a live URL
Invoke `bin/amw-design-md-from-url.sh <url> <output-path>` which delegates DOM and computed-style extraction to the plugin's existing `amw-dev-browser` skill, then emits Variant 1 frontmatter.

### Extract a DESIGN.md from a Tailwind config
Run `node bin/amw-design-md-from-tailwind.mjs --config <tailwind.config.ts> --css <globals.css> --out <DESIGN.md>`. Pure-local Node.js port of the upstream tool. Resolves CSS-var references and annotates color pairs with WCAG-AA contrast.

### Extract a DESIGN.md from a codebase scan
Run `bin/amw-design-md-from-codebase.py <project-root>`. Pure-Python scanner that detects shadcn/Tailwind/Chakra/vanilla-CSS/styled-components and emits a draft DESIGN.md.

### Audit a DESIGN.md
Spawn `amw-design-md-auditor-agent`. The auditor runs the 5-pass audit per `references/audit-passes.md` and writes a `<file>.critique.md` adjacent to the input.

### Convert Variant 2 → Variant 1
Run `bin/amw-design-md-convert-v2-to-v1.py <variant2.md> <variant1.md>`. Maps the 9-section community format to the canonical 8-section + YAML frontmatter format.

### Emit companion files
Run `bin/amw-design-md-emit-companions.py <DESIGN.md> <output-dir>`. Emits `tokens.css` (CSS custom properties), `tokens.json` (W3C Design Tokens), `component-inventory.md`, and `usage-prompt.md`.

### Diff two DESIGN.md revisions
Run `bin/amw-design-md-diff.sh <a.md> <b.md>`. Wrapper around `npx @google/design.md diff`.

## When the result is consumed downstream

When the user provides a DESIGN.md and then proceeds to Phase B (HTML rendering), `amw-wireframe-builder-agent` reads the DESIGN.md, validates it via `bin/amw-design-md-lint.sh`, and treats its tokens as canonical. On lint failure, the wireframe-builder reports and STOPS — the DESIGN.md path is symmetric with brand-researcher's extracted tokens, ascii-sketch's approved variant, and prose. See `references/TECH-15-design-md-as-input.md`.

## Hard rules

1. The skill produces Variant 1 (official `@google/design.md`) as canonical output by default. Variant 2 is accepted as input via the converter.
2. The skill runs no paywalled service, no API key beyond what `amw-dev-browser` already requires, and no Chrome extension. The official CLI is `npx`-installable, no API key, no remote calls.
3. The skill never re-emits broad design vocabulary in tool-call text — that would re-trigger the orchestrator. See `../amw-design-principles/references/skill-invocation-protocol.md`.
4. Every authored DESIGN.md MUST pass `bin/amw-design-md-lint.sh` before being delivered. Lint failure halts delivery.
5. WCAG-AA contrast checks via `bin/amw-design-md-contrast.py` are run on every authored DESIGN.md. Failures go to `warnings`, not silent omission.

## Cross-references

- `./ai-slop-avoid.md` — DESIGN.md-specific anti-patterns
- `./references/canonical-spec-google-alpha.md` — Variant 1 spec, source-cited
- `./references/community-9-section-spec.md` — Variant 2 spec, source-cited
- `./references/extension-sections-10-14.md` — optional Naming / Page Specs / Composite Components / Token Mapping / i18n
- `./references/templates/canonical-template.md` — Variant 1 skeleton
- `./references/templates/community-9-section-template.md` — Variant 2 skeleton
- `./references/templates/claude-md-snippet.md` — CLAUDE.md addition for projects using DESIGN.md
- `./references/review-rubric.md` — quality-scoring rubric
- `./references/audit-passes.md` — 5-pass audit
- `./references/TECH-01-yaml-frontmatter.md` through `TECH-15-design-md-as-input.md`
- `./references/TECH-cjk-localization.md` — CJK localization (JP/KO/ZH)
- `../amw-design-principles/SKILL.md` — orchestrator (this skill is downstream)
- `../amw-dev-browser/SKILL.md` — browser primitive used by URL extraction
- `../amw-design-extract/SKILL.md` — sibling URL-extraction skill (looser format; this skill is the strict-format counterpart)
- `<plugin-root>/bin/amw-design-md-*.{sh,py,ts}` — ten bin scripts
