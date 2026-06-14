---
name: amw-design-md-spec
description: DESIGN.md format spec, templates, and authoring rules. Triggers on "DESIGN.md spec", "DESIGN.md template/skeleton", "DESIGN.md frontmatter", "DESIGN.md section order / authoring rules", "adopt DESIGN.md in CLAUDE.md". Variant 1 (official @google/design.md) + Variant 2 (community 9-section). Does NOT trigger on generic "design system". Use to look up the canonical format, fill a skeleton, or check the 13 authoring rules.
version: 0.1.0
---

# AMW Design.md — Spec

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Format-identity authority for the DESIGN.md family. Owns the two canonical specs, the templates, the YAML frontmatter schema, and the 13 authoring rules. Sibling skills: [author](../amw-design-md-author/SKILL.md), [extract](../amw-design-md-extract/SKILL.md), [audit](../amw-design-md-audit/SKILL.md), [convert](../amw-design-md-convert/SKILL.md). DESIGN.md is one of several optional input formats accepted by the plugin (peer to ASCII wireframes, mockup images, slideshows, URL "copy this style" briefs, and prose). Triggers are DESIGN.md-specific only.

## Overview

The canonical reference for the DESIGN.md format. Two variants are supported: official **Variant 1** (`<@google/design.md>` — YAML frontmatter + 8 fixed Markdown sections, the default output) and the community **Variant 2** (VoltAgent 9-section, accepted-with-mapping). This skill is where you look up the format itself, fill an empty skeleton, or check a structural authoring rule. It does not author from a brief (see [author](../amw-design-md-author/SKILL.md)), extract from a source (see [extract](../amw-design-md-extract/SKILL.md)), lint/score (see [audit](../amw-design-md-audit/SKILL.md)), or transform (see [convert](../amw-design-md-convert/SKILL.md)).

## Activation

Invoked by the orchestrator (or any agent) when the question is *about the format* — "what sections does a DESIGN.md have", "give me the skeleton", "what's the frontmatter schema", "what are the authoring rules". This skill is **autonomous and self-contained** — any agent can read this SKILL.md and the referenced files and apply the format without re-routing.

## Position in flow

REFERENCE. Not an emitter. The other four design-md skills lean on this one for the format definition. When a DESIGN.md is produced (by [author](../amw-design-md-author/SKILL.md)) it conforms to the Variant 1 spec defined here; when one is consumed downstream (by `amw-wireframe-builder-agent`) it is parsed against this spec.

## What this skill is NOT

- Not a brand database. The pre-paywall snapshot of 58 example DESIGN.md files lives in `docs_dev/extracted/google-labs/awesome-design-md-pre-paywall-main/` and is reference-only.
- Not an authoring engine. Filling a skeleton from a real brief / interview / codebase is the [author](../amw-design-md-author/SKILL.md) skill's job.
- Not the orchestrator. Generic "design system" requests route to `amw-design-principles`. Only DESIGN.md-format-specific requests reach here.

## Trigger conditions

Fires on: "DESIGN.md spec / format"; "DESIGN.md template / skeleton"; "DESIGN.md frontmatter schema"; "DESIGN.md section order / authoring rules"; "what are the 13 DESIGN.md rules"; "adopt DESIGN.md in CLAUDE.md".

Does NOT fire on generic "design a landing page" / "design system" / "extract design tokens" — those route to `amw-design-principles` (orchestrator) or `amw-design-extract`. Authoring-from-brief, extraction, audit, and conversion route to the respective sibling design-md skills.

## The two canonical specs

- **Variant 1 (default, official):** YAML frontmatter + 8 fixed Markdown sections (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts). Source-cited spec in [canonical-spec-google-alpha](references/canonical-spec-google-alpha.md).
  > File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references
- **Variant 2 (accepted-with-mapping, community):** no frontmatter, 9 numbered sections, optional XML boundary tags + Mermaid component-state diagram. Source-cited spec in [community-9-section-spec](references/community-9-section-spec.md).
> [community-9-section-spec.md] Document head (DESIGN_MD_SPEC L13-L17) · Section count and order (DESIGN_MD_SPEC L25-L36) · No YAML frontmatter · Section specifications · Section 1 — Visual Theme & Atmosphere (DESIGN_MD_SPEC L43-L67) · Section 2 — Color Palette & Roles (DESIGN_MD_SPEC L72-L106) · Section 3 — Typography Rules (DESIGN_MD_SPEC L108-L166) · Section 4 — Component Stylings (DESIGN_MD_SPEC L169-L216) · Section 5 — Layout Principles (DESIGN_MD_SPEC L219-L246) · Section 6 — Depth & Elevation · Section 7 — Do's and Don'ts · Section 8 — Responsive Behavior · Section 9 — Agent Prompt Guide · XML boundary tags (Variant 2 enhancement) · Mermaid component-state diagram · Comparison vs Variant 1 · Cross-references
  > Document head (DESIGN_MD_SPEC L13-L17) · Section count and order (DESIGN_MD_SPEC L25-L36) · No YAML frontmatter · Section specifications · XML boundary tags (Variant 2 enhancement) · Mermaid component-state diagram · Comparison vs Variant 1 · Cross-references
- **Optional extension sections 10-14** layer onto either variant — naming convention, page specs, composite components, token mapping, i18n. See [extension-sections-10-14](references/extension-sections-10-14.md).
  > Overview · Section 10 — Naming Convention (Page > Section > Block > Element) · Section 11 — Page Specifications · Section 12 — Composite Components · Section 13 — Token Mapping · Section 14 — i18n References · When to use these extensions · Cross-references

## Templates

- **Variant 1 skeleton** to fill in: [canonical-template](references/canonical-template.md).
  > Filling guide · Cross-references
- **Variant 2 skeleton:** [community-9-section-template](references/community-9-section-template.md).
  > Optional extension sections · Validation · Cross-references
- **CLAUDE.md adoption snippet** for projects that make DESIGN.md their source of truth: [claude-md-snippet](references/claude-md-snippet.md).
  > Snippet — paste into the project's `CLAUDE.md` · Where this goes in CLAUDE.md · What `{{placeholders}}` get filled with · Cross-references

## The frontmatter schema and the authoring rules

- **YAML frontmatter schema** (Variant 1) — required keys, token-block shape, the contrast-pair convention: [TECH-01-yaml-frontmatter](references/TECH-01-yaml-frontmatter.md).
> [TECH-01-yaml-frontmatter.md] What it does · When to use · Hard rules · Delimiters · Top-level fields · Value type rules · Token references · YAML quoting rules · Common gotchas · Worked example — minimal valid frontmatter · Worked example — token reference inside components · Validation · Cross-references
  > What it does · When to use · Hard rules · Common gotchas · Worked example — minimal valid frontmatter · Worked example — token reference inside components · Validation · Cross-references
- **DESIGN_MD_SPEC — the 13 authoring rules** (section order, heading format, backticks, elevation columns, Do's/Don'ts wording, Variant 1 vs Variant 2 deviations): [TECH-24-authoring-rules-spec](references/TECH-24-authoring-rules-spec.md).
  > What it does · Why a spec exists · The 13 rules · How the rules combine · Linter enforcement · Variant 1 vs Variant 2 differences · Cross-references

## Instructions

1. To answer a format question, read the relevant spec ([canonical-spec-google-alpha](references/canonical-spec-google-alpha.md) for Variant 1, [community-9-section-spec](references/community-9-section-spec.md) for Variant 2).
> [community-9-section-spec.md] Document head (DESIGN_MD_SPEC L13-L17) · Section count and order (DESIGN_MD_SPEC L25-L36) · No YAML frontmatter · Section specifications · Section 1 — Visual Theme & Atmosphere (DESIGN_MD_SPEC L43-L67) · Section 2 — Color Palette & Roles (DESIGN_MD_SPEC L72-L106) · Section 3 — Typography Rules (DESIGN_MD_SPEC L108-L166) · Section 4 — Component Stylings (DESIGN_MD_SPEC L169-L216) · Section 5 — Layout Principles (DESIGN_MD_SPEC L219-L246) · Section 6 — Depth & Elevation · Section 7 — Do's and Don'ts · Section 8 — Responsive Behavior · Section 9 — Agent Prompt Guide · XML boundary tags (Variant 2 enhancement) · Mermaid component-state diagram · Comparison vs Variant 1 · Cross-references
> [canonical-spec-google-alpha.md] File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references
2. To fill a skeleton, copy [canonical-template](references/canonical-template.md) (Variant 1) or [community-9-section-template](references/community-9-section-template.md) (Variant 2), then hand off to [author](../amw-design-md-author/SKILL.md) to fill from a real brief and to [audit](../amw-design-md-audit/SKILL.md) for the lint+contrast gate.
> [community-9-section-template.md] Optional extension sections · Validation · Cross-references
> [canonical-template.md] Filling guide · Cross-references
3. To check a structural rule, read [TECH-24-authoring-rules-spec](references/TECH-24-authoring-rules-spec.md) (the 13 rules) and [TECH-01-yaml-frontmatter](references/TECH-01-yaml-frontmatter.md) (frontmatter).
> [TECH-01-yaml-frontmatter.md] What it does · When to use · Hard rules · Delimiters · Top-level fields · Value type rules · Token references · YAML quoting rules · Common gotchas · Worked example — minimal valid frontmatter · Worked example — token reference inside components · Validation · Cross-references
4. To make a project adopt DESIGN.md, paste the [claude-md-snippet](references/claude-md-snippet.md) into its CLAUDE.md.
> [claude-md-snippet.md] Snippet — paste into the project's `CLAUDE.md` · Where this goes in CLAUDE.md · What `{{placeholders}}` get filled with · Cross-references

## Hard rules

1. Variant 1 (official `<@google/design.md>`) is the canonical format. Variant 2 is accepted as input and mapped to Variant 1 via [convert](../amw-design-md-convert/SKILL.md).
2. The skill never re-emits broad design vocabulary in tool-call text — that would re-trigger the orchestrator. See [skill-invocation-protocol](../amw-design-principles/references/skill-invocation-protocol.md).
> [skill-invocation-protocol.md] The problem · The protocol · Examples · Enforcement

## Resources

- [canonical-spec-google-alpha](references/canonical-spec-google-alpha.md) — Variant 1 spec, source-cited
> [canonical-spec-google-alpha.md] File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references
- [community-9-section-spec](references/community-9-section-spec.md) — Variant 2 spec, source-cited
> [community-9-section-spec.md] Document head (DESIGN_MD_SPEC L13-L17) · Section count and order (DESIGN_MD_SPEC L25-L36) · No YAML frontmatter · Section specifications · Section 1 — Visual Theme & Atmosphere (DESIGN_MD_SPEC L43-L67) · Section 2 — Color Palette & Roles (DESIGN_MD_SPEC L72-L106) · Section 3 — Typography Rules (DESIGN_MD_SPEC L108-L166) · Section 4 — Component Stylings (DESIGN_MD_SPEC L169-L216) · Section 5 — Layout Principles (DESIGN_MD_SPEC L219-L246) · Section 6 — Depth & Elevation · Section 7 — Do's and Don'ts · Section 8 — Responsive Behavior · Section 9 — Agent Prompt Guide · XML boundary tags (Variant 2 enhancement) · Mermaid component-state diagram · Comparison vs Variant 1 · Cross-references
- [extension-sections-10-14](references/extension-sections-10-14.md) — optional Naming / Page Specs / Composite Components / Token Mapping / i18n
> [extension-sections-10-14.md] Overview · Section 10 — Naming Convention (Page > Section > Block > Element) · Section 11 — Page Specifications · Section 12 — Composite Components · Section 13 — Token Mapping · Section 14 — i18n References · When to use these extensions · Cross-references
- [canonical-template](references/canonical-template.md) — Variant 1 skeleton
> [canonical-template.md] Filling guide · Cross-references
- [community-9-section-template](references/community-9-section-template.md) — Variant 2 skeleton
> [community-9-section-template.md] Optional extension sections · Validation · Cross-references
- [claude-md-snippet](references/claude-md-snippet.md) — CLAUDE.md addition for projects using DESIGN.md
> [claude-md-snippet.md] Snippet — paste into the project's `CLAUDE.md` · Where this goes in CLAUDE.md · What `{{placeholders}}` get filled with · Cross-references
- [TECH-01-yaml-frontmatter](references/TECH-01-yaml-frontmatter.md) — YAML frontmatter schema
> [TECH-01-yaml-frontmatter.md] What it does · When to use · Hard rules · Delimiters · Top-level fields · Value type rules · Token references · YAML quoting rules · Common gotchas · Worked example — minimal valid frontmatter · Worked example — token reference inside components · Validation · Cross-references
- [TECH-24-authoring-rules-spec](references/TECH-24-authoring-rules-spec.md) — DESIGN_MD_SPEC 13 authoring rules
> [TECH-24-authoring-rules-spec.md] What it does · Why a spec exists · The 13 rules · Rule 1 — 9 sections mandatory, fixed order · Rule 2 — Section heading format · Rule 3 — Every color value in backticks · Rule 4 — Elevation table exactly 3 columns · Rule 5 — Shadow Philosophy required prose in §6 · Rule 6 — Iteration Guide numbered list · Rule 7 — Do's and Don'ts parallel in count · Rule 8 — Spacing scale base unit is 8px · Rule 9 — §9 Agent Prompt Guide last in body · Rule 10 — One sentence per visual rule · Rule 11 — Typography roles must declare 3 properties · Rule 12 — Component definitions must cite tokens, never raw values · Rule 13 — Frontmatter precedes the H1 · How the rules combine · Linter enforcement · Variant 1 vs Variant 2 differences · Cross-references
- [author](../amw-design-md-author/SKILL.md) · [extract](../amw-design-md-extract/SKILL.md) · [audit](../amw-design-md-audit/SKILL.md) · [convert](../amw-design-md-convert/SKILL.md) — sibling DESIGN.md skills
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (this skill is downstream)
