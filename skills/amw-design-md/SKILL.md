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

## Activation

Callable directly via the nine `/amw-design-md-*` commands. Also invoked by the orchestrator when the user provides a DESIGN.md file as input or asks for one as a deliverable. In main-agent mode the orchestrator may delegate to one of three sub-agents (`amw-design-md-author-agent`, `amw-design-md-extractor-agent`, `amw-design-md-auditor-agent`) which read this SKILL.md and its references to do their job.

This skill is **autonomous and self-contained** — any agent can read this SKILL.md and the referenced files and execute the recipes without re-routing through the orchestrator.

## Position in flow

INPUT or OUTPUT (peer status). DESIGN.md is one of six input formats the plugin accepts (peer to ASCII wireframe, mockup image, slideshow, URL "copy this style", prose). When the user provides a DESIGN.md, the parser/validator path here normalizes it into canonical tokens for downstream Phase B agents (notably `amw-wireframe-builder-agent`). When the user asks for a DESIGN.md as the deliverable, the author path here produces a Variant 1 file (plus optional companions).

## What this skill is NOT

- Not a brand database. The pre-paywall snapshot of 58 example DESIGN.md files lives in `docs_dev/extracted/google-labs/awesome-design-md-pre-paywall-main/` and is reference-only.
- Not a UI generator. After extracting tokens or authoring a DESIGN.md, the actual HTML is built by `amw-wireframe-builder-agent` via the `amw-ascii-to-html` skill.
- Not the orchestrator. Generic "design system" requests route to `amw-design-principles`. Only DESIGN.md-specific requests reach here.

## Trigger conditions

Fires on: "create/author/make a DESIGN.md"; "extract DESIGN.md from <url|tailwind config|codebase>"; "lint/validate my DESIGN.md"; "audit/five-pass-audit DESIGN.md"; "convert Variant 2 DESIGN.md to Variant 1"; "emit DESIGN.md companions / tokens.css / tokens.json"; "diff two DESIGN.md files".

Does NOT fire on generic "design a landing page" / "extract design tokens from <url>" / "build a token spec" / "make a UI" — those route to `amw-design-principles` (orchestrator) or `amw-design-extract`.

## How it works

The skill ships:

- **Two canonical specs** — [canonical-spec-google-alpha](references/canonical-spec-google-alpha.md) (Variant 1, official `<@google/design.md>`, primary) and [community-9-section-spec](references/community-9-section-spec.md) (Variant 2, VoltAgent community 9-section, accepted-with-mapping).
- **16 TECH-NN reference files** under `references/TECH-*.md` covering frontmatter, color tokens, typography tokens, component tokens, token references, do/don'ts authoring, URL extraction, codebase extraction, multi-page extraction, Tailwind conversion, validation/lint, companion files, V2→V1 conversion, validation failure recovery, DESIGN.md as input, and CJK localization ([TECH-cjk-localization](references/TECH-cjk-localization.md)).
- **Three templates** under `references/` — Variant 1 skeleton, Variant 2 skeleton, and a CLAUDE.md snippet for projects that adopt DESIGN.md.
- **Two audit/quality docs** — [review-rubric](references/review-rubric.md) (DESIGN.md quality scoring) and [audit-passes](references/audit-passes.md) (5-pass audit: structural / drift / a11y / completeness / consistency).
- **Ten bin scripts** under `<plugin-root>/bin/amw-design-md-*` — pure-local Python and TypeScript ports plus thin shell wrappers around the official `npx @google/design.md` CLI.

## Prerequisites

Standard plugin runtime — no skill-specific prerequisites beyond the global plugin dependencies.

## Instructions

1. Identify the requested operation: author, lint/validate, extract from URL, extract from Tailwind config, extract from codebase, audit, convert Variant 2 → Variant 1, emit companion files, or diff two revisions.
2. For authoring: read [canonical-template](references/canonical-template.md), fill from brief/interview/codebase/URL using the appropriate bin script, then validate with `bin/amw-design-md-lint.sh`.
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

### Generate a visual showcase HTML
Run `bin/amw-design-md-showcase.py <DESIGN.md> -o <out.html>`. Emits a self-contained single-file HTML showcase that renders every color token (swatches + WCAG-AA contrast badges for `X` / `on-X` pairs), every typography role (live specimens at the declared size / weight / line-height), every spacing / rounded / elevation step (visual demos), and every declared component (rendered button / input / card / chip examples with resolved token references). Author-side QA aid used before delivery. Pure stdlib (pyyaml optional). Output is fully offline-safe — no remote fonts, no remote stylesheets, no JS.

### Diff two DESIGN.md revisions
Run `bin/amw-design-md-diff.sh <a.md> <b.md>`. Wrapper around `npx @google/design.md diff`.

## When the result is consumed downstream

When the user provides a DESIGN.md and then proceeds to Phase B (HTML rendering), `amw-wireframe-builder-agent` reads the DESIGN.md, validates it via `bin/amw-design-md-lint.sh`, and treats its tokens as canonical. On lint failure, the wireframe-builder reports and STOPS — the DESIGN.md path is symmetric with brand-researcher's extracted tokens, ascii-sketch's approved variant, and prose. See [TECH-15-design-md-as-input](references/TECH-15-design-md-as-input.md).

## Hard rules

1. The skill produces Variant 1 (official `<@google/design.md>`) as canonical output by default. Variant 2 is accepted as input via the converter.
2. The skill runs no paywalled service, no API key beyond what `amw-dev-browser` already requires, and no Chrome extension. The official CLI is `npx`-installable, no API key, no remote calls.
3. The skill never re-emits broad design vocabulary in tool-call text — that would re-trigger the orchestrator. See [skill-invocation-protocol](../amw-design-principles/references/skill-invocation-protocol.md).
4. Every authored DESIGN.md MUST pass `bin/amw-design-md-lint.sh` before being delivered. Lint failure halts delivery.
5. WCAG-AA contrast checks via `bin/amw-design-md-contrast.py` are run on every authored DESIGN.md. Failures go to `warnings`, not silent omission.

## Output

Produces a single artifact at the path specified in §Operations — a DESIGN.md file (Variant 1) plus optional companion files.

## Error Handling

On failure, the skill emits a non-zero exit code or returns a structured error in the response. See bin/ scripts for tool-specific error semantics.

## Examples

**Author DESIGN.md from a brief (Variant 1):** Input "fintech dashboard, brand `#0F4C81`, secondary `#FFD23F`, Inter body / Manrope headings, WCAG AA." Lint gate runs `amw-design-md-lint.sh`; contrast pre-flight runs `amw-design-md-contrast.py`. Output: `DESIGN.md` (Variant 1) plus companions `tokens.css`, `tokens.json`, `component-inventory.md`, `usage-prompt.md`.

**Extract DESIGN.md from a live URL:** Input `https://stripe.com`. `amw-design-md-from-url.sh` delegates to `amw-dev-browser/` for DOM + computed styles, then transcribes faithfully into Variant 1. Output: `stripe.DESIGN.md` with one-to-one source attribution.

See worked examples in references/.

## Resources

- [ai-slop-avoid](./ai-slop-avoid.md) — DESIGN.md-specific anti-patterns (token authoring, structural, prose, Variant 2-specific, conversion, companion-file slop)
- [canonical-spec-google-alpha](./references/canonical-spec-google-alpha.md) — Variant 1 spec, source-cited
- [community-9-section-spec](./references/community-9-section-spec.md) — Variant 2 spec, source-cited
- [extension-sections-10-14](./references/extension-sections-10-14.md) — optional Naming / Page Specs / Composite Components / Token Mapping / i18n
- [canonical-template](./references/canonical-template.md) — Variant 1 skeleton
- [community-9-section-template](./references/community-9-section-template.md) — Variant 2 skeleton
- [claude-md-snippet](./references/claude-md-snippet.md) — CLAUDE.md addition for projects using DESIGN.md
- [review-rubric](./references/review-rubric.md) — quality-scoring rubric
- [audit-passes](./references/audit-passes.md) — 5-pass audit
- [TECH-01-yaml-frontmatter](./references/TECH-01-yaml-frontmatter.md) through `TECH-15-design-md-as-input.md` — 16 per-technique reference files
- [TECH-cjk-localization](./references/TECH-cjk-localization.md) — CJK localization (JP/KO/ZH)
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (this skill is downstream)
- [SKILL](../amw-dev-browser/SKILL.md) — browser primitive used by URL extraction
- [SKILL](../amw-design-extract/SKILL.md) — sibling URL-extraction skill (looser format; this skill is the strict-format counterpart)
- `<plugin-root>/bin/amw-design-md-showcase.py` — DESIGN.md → self-contained HTML visual-QA showcase (color swatches + WCAG-AA badges, type specimens, spacing / rounded / elevation demos, rendered component examples). Pure stdlib (pyyaml optional). Author-side QA before delivery.
- `<plugin-root>/bin/amw-design-md-*.{sh,py,ts}` — eleven bin scripts (lint, validate, contrast, emit-companions, showcase, from-url, from-tailwind, from-codebase, convert-v2-to-v1, diff, plus the official `@google/design.md` lint wrapper)
