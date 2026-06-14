---
name: amw-design-md
description: Author, lint, extract, audit, and convert DESIGN.md design-system specifications. Triggers on "create DESIGN.md", "lint DESIGN.md", "extract DESIGN.md from URL/Tailwind/codebase", "audit DESIGN.md", "DESIGN.md companions". Does NOT trigger on generic "design system", "extract design tokens" — those route to amw-design-principles or amw-design-extract. Use when authoring, linting, or converting a DESIGN.md spec. Trigger with /amw-design-md-create.
version: 0.1.0
---

# AMW Design.md

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **This skill was split into five focused children.** It now routes to them and exists for backward compatibility — the `/amw-design-md-*` commands and every existing cross-reference still resolve here. DESIGN.md is one of several optional input/output formats the plugin accepts (peer to ASCII wireframes, mockup images, slideshows, URL "copy this style" briefs, and prose).

## What this skill is now

A router. The DESIGN.md capability (author, lint, extract, audit, convert, emit companions) outgrew a single skill's token budget, so it was split into five domain skills. Pick the child that matches the operation:

| If you want to… | Use |
|---|---|
| Look up the **format** — the two specs, templates, frontmatter schema, the 13 authoring rules, the CLAUDE.md adoption snippet | [amw-design-md-spec](../amw-design-md-spec/SKILL.md) |
| **Author** a new DESIGN.md from a brief / interview / brand archetype / 5-question flow (lint + WCAG-AA contrast gate, extended sections, `{token.ref}` interpolation, STYLE-REFERENCES.md, CJK) | [amw-design-md-author](../amw-design-md-author/SKILL.md) |
| **Extract** a DESIGN.md from a live URL / Tailwind config / codebase / Figma (component + state detection, asset export, fingerprinting) | [amw-design-md-extract](../amw-design-md-extract/SKILL.md) |
| **Lint / validate / audit / score** a DESIGN.md (5-pass audit, quality rubric, validation-failure recovery, ai-slop check, diff) | [amw-design-md-audit](../amw-design-md-audit/SKILL.md) |
| **Convert / apply / export** — Variant 2→1, emit companions (tokens.css/json, inventory, usage-prompt), showcase HTML, DTCG export, token-enforcement, cross-project library, as-input to the wireframe-builder | [amw-design-md-convert](../amw-design-md-convert/SKILL.md) |

## Activation

Any agent landing here should read the table above and dispatch to the matching child SKILL.md, which is **autonomous and self-contained**. The `/amw-design-md-*` commands continue to work; in main-agent mode the orchestrator delegates to one of three sub-agents (`amw-design-md-author-agent`, `amw-design-md-extractor-agent`, `amw-design-md-auditor-agent`), which read the relevant child skill's SKILL.md and references to do their job.

## Position in flow

INPUT or OUTPUT (peer status). DESIGN.md is one of six input formats the plugin accepts (peer to ASCII wireframe, mockup image, slideshow, URL "copy this style", prose). When the user provides a DESIGN.md, the parse/validate path ([audit](../amw-design-md-audit/SKILL.md) + [convert](../amw-design-md-convert/SKILL.md)) normalizes it into canonical tokens for downstream Phase B agents (notably `amw-wireframe-builder-agent`). When the user asks for a DESIGN.md as the deliverable, the [author](../amw-design-md-author/SKILL.md) or [extract](../amw-design-md-extract/SKILL.md) path produces a Variant 1 file (plus optional companions via [convert](../amw-design-md-convert/SKILL.md)).

## What this skill is NOT

- Not a brand database. The pre-paywall snapshot of 58 example DESIGN.md files lives in `docs_dev/extracted/google-labs/awesome-design-md-pre-paywall-main/` and is reference-only.
- Not a UI generator. After extracting tokens or authoring a DESIGN.md, the actual HTML is built by `amw-wireframe-builder-agent` via the `amw-ascii-to-html` skill.
- Not the orchestrator. Generic "design system" requests route to `amw-design-principles`. Only DESIGN.md-specific requests reach the children.

## Hard rules (inherited by every child)

1. Variant 1 (official `<@google/design.md>`) is the canonical output format. Variant 2 is accepted as input via the [convert](../amw-design-md-convert/SKILL.md) converter.
2. Every authored / extracted DESIGN.md MUST pass `bin/amw-design-md-lint.sh` before delivery; lint failure halts delivery. WCAG-AA contrast failures (via `bin/amw-design-md-contrast.py`) go to `warnings`, not silent omission.
3. No paywalled service, no API key beyond what `amw-dev-browser` already requires, no Chrome extension.
4. No child re-emits broad design vocabulary in tool-call text — that would re-trigger the orchestrator. See [skill-invocation-protocol](../amw-design-principles/references/skill-invocation-protocol.md).
> [skill-invocation-protocol.md] The problem · The protocol · Examples · Enforcement

## Reference material not (yet) owned by a child

Earlier design-md reference files that predate the split remain in `references/` here for backward compatibility (per-token TECH docs `TECH-02`…`TECH-13`, `TECH-16`, the brand fingerprint catalog `brand-*.md`, `TECH-86/91/94/96`, `TECH-design-contract.md`, the `TECH-extractor-*` color/dark-mode/pseudo-element/typography-role docs, `design-decision-rules.md`, `writing-voice.md`). They are not on any child's progressive-discovery path; consult them directly when a deep token-extraction or brand-fingerprint detail is needed.

## Resources

- [amw-design-md-spec](../amw-design-md-spec/SKILL.md) — format, specs, templates, frontmatter schema, 13 authoring rules
- [amw-design-md-author](../amw-design-md-author/SKILL.md) — author from brief / interview / archetype; lint + contrast gate
- [amw-design-md-extract](../amw-design-md-extract/SKILL.md) — extract from URL / Tailwind / codebase / Figma
- [amw-design-md-audit](../amw-design-md-audit/SKILL.md) — lint / validate / 5-pass audit / quality score / ai-slop
- [amw-design-md-convert](../amw-design-md-convert/SKILL.md) — V2→V1, companions, showcase, DTCG, token-enforcement, library, as-input
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (this skill is downstream)
- `<plugin-root>/bin/amw-design-md-*.{sh,py,mjs}` — ten bin scripts (lint, validate, contrast, emit-companions, showcase, from-url, from-tailwind, from-codebase, convert-v2-to-v1, diff) shared by the children
