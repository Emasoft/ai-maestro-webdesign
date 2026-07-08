---
name: amw-design-md-convert
description: Convert, apply, and export a DESIGN.md and its companions. Triggers on "convert Variant 2 DESIGN.md to Variant 1", "emit DESIGN.md companions / tokens.css / tokens.json", "apply DESIGN.md tokens / enforce tokens", "DESIGN.md DTCG export", "cross-project DESIGN.md library". Use to transform a DESIGN.md into downstream artifacts or enforce its tokens at code-gen.
---

# AMW Design.md — Convert

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Transforms a DESIGN.md into downstream artifacts (companions, DTCG export, showcase) and enforces its tokens at code-gen time. For the format itself read [spec](../amw-design-md-spec/SKILL.md); to author from a brief use [author](../amw-design-md-author/SKILL.md). DESIGN.md is one of several optional input/output formats the plugin accepts. Triggers are DESIGN.md-specific only.

## Overview

The transform-and-apply engine for DESIGN.md. Converts Variant 2 → Variant 1, emits companion files (`tokens.css`, `tokens.json`, `component-inventory.md`, `usage-prompt.md`), generates a visual showcase HTML, exports DTCG / W3C Design Tokens, runs the apply / token-enforcement pipeline at code-gen time, manages a cross-project DESIGN.md library, and documents downstream consumption by `amw-wireframe-builder-agent`.

## Activation

Callable when the user wants to *convert, apply, or export* a DESIGN.md or its companions. Also invoked by the orchestrator and by Phase B agents (notably `amw-wireframe-builder-agent`, which reads the DESIGN.md as input). This skill is **autonomous and self-contained** — any agent can read this SKILL.md and the referenced files and execute the recipes without re-routing.

## Position in flow

TRANSFORM / OUTPUT-adapter. Sits between a finished DESIGN.md (produced by [author](../amw-design-md-author/SKILL.md) or [extract](../amw-design-md-extract/SKILL.md)) and downstream consumers — code-gen, design-system tooling, or `amw-wireframe-builder-agent`. The V2→V1 converter normalizes input into the canonical format owned by [spec](../amw-design-md-spec/SKILL.md).

## What this skill is NOT

- Not the format reference — that is [spec](../amw-design-md-spec/SKILL.md).
- Not a UI generator. After tokens are applied, the actual HTML is built by `amw-wireframe-builder-agent` via the `amw-ascii-to-html` skill.
- Not the orchestrator. Generic "design system" requests route to `amw-design-principles`.

## Trigger conditions

Fires on: "convert Variant 2 DESIGN.md to Variant 1"; "emit DESIGN.md companions / tokens.css / tokens.json"; "apply DESIGN.md tokens / enforce tokens"; "DESIGN.md DTCG / W3C Design Tokens export"; "DESIGN.md visual showcase"; "cross-project DESIGN.md library"; "use this DESIGN.md as input to the wireframe-builder".

Does NOT fire on "create a DESIGN.md" (→ [author](../amw-design-md-author/SKILL.md)), "extract a DESIGN.md" (→ [extract](../amw-design-md-extract/SKILL.md)), or generic "design a page" / "extract design tokens" (→ `amw-design-principles` / `amw-design-extract`).

## The convert / emit / showcase operations

- **Convert Variant 2 → Variant 1:** `bin/amw-design-md-convert-v2-to-v1.py <variant2.md> <variant1.md>` — maps the 9-section community format to the canonical 8-section + YAML frontmatter format.
- **Emit companion files:** `bin/amw-design-md-emit-companions.py <DESIGN.md> --out-dir <output-dir>` — emits `tokens.css` (CSS custom properties), `tokens.json` (W3C Design Tokens), `component-inventory.md`, and `usage-prompt.md`.
- **Generate a visual showcase HTML:** `bin/amw-design-md-showcase.py <DESIGN.md> -o <out.html>` — self-contained single-file HTML that renders every color token (swatches + WCAG-AA contrast badges for `X` / `on-X` pairs), every typography role (live specimens), every spacing / rounded / elevation step, and every declared component (rendered button / input / card / chip examples with resolved token references). Author-side QA aid. Pure stdlib (pyyaml optional); fully offline-safe — no remote fonts, no remote stylesheets, no JS.

## Apply, export, library, and downstream consumption

- **Apply / token-enforcement pipeline** (raw-hex sweep / raw-px sweep / typography sweep / WCAG pair-check / Do's-Don'ts enforcement, run at code-gen time): [TECH-19-design-md-apply](references/TECH-19-design-md-apply.md).
> [TECH-19-design-md-apply.md] What it does · When this TECH applies · The five-pass apply pipeline · Pass 1 — Raw-hex sweep · Pass 2 — Raw-px sweep · Pass 3 — Typography sweep · Pass 4 — WCAG contrast pair-check · Pass 5 — Do's and Don'ts enforcement · Replacement table — DESIGN.md slot → CSS-var name · Token-resolution algorithm · Failure paths · Worked example · Cross-references
  > What it does · When this TECH applies · The five-pass apply pipeline · Replacement table — DESIGN.md slot → CSS-var name · Token-resolution algorithm · Failure paths · Worked example · Cross-references
- **DTCG / W3C Design Tokens export** (schema mapping + source coverage + harmonize mode + round-trip with the companion emitter): [TECH-17-dtcg-export](references/TECH-17-dtcg-export.md).
> [TECH-17-dtcg-export.md] What it does · Why a dedicated DTCG exporter · DTCG schema mapping · Leaf shape · Group shape and `$type` inheritance · Alias syntax · Composite typography tokens · Source coverage · Harmonize mode · Bare-key rewrite · Type inference for unlabelled leaves · Idempotence · Validation contract · Round-trip contract with `amw-design-md-emit-companions.py` · CLI reference · Cross-references
  > What it does · Why a dedicated DTCG exporter · DTCG schema mapping · Source coverage · Harmonize mode · Validation contract · Round-trip contract with `amw-design-md-emit-companions.py` · CLI reference · Cross-references
- **Cross-project DESIGN.md library** at `~/.config/ai-maestro/design-library/` (CLI verbs list / use / show / remove / diff / preview / add): [TECH-20-design-library](references/TECH-20-design-library.md).
> [TECH-20-design-library.md] What it does · Why a cross-project library · Library layout on disk · Proposed CLI surface · `amw-design-library list` · `amw-design-library use <name>` · `amw-design-library show <name>` · `amw-design-library remove <name>` · `amw-design-library diff <name-a> <name-b>` · `amw-design-library preview <name>` · `amw-design-library add <name>` · Naming convention · Workflow — "build this in the Linear style" · Integration with existing skills · Security and privacy · Limitations · Cross-references
  > What it does · Why a cross-project library · Library layout on disk · Proposed CLI surface · Naming convention · Workflow — "build this in the Linear style" · Integration with existing skills · Security and privacy · Limitations · Cross-references
- **DESIGN.md as input to the wireframe-builder** (token mapping to `brand_tokens`, component passthrough, symmetry with non-DESIGN.md inputs): [TECH-15-design-md-as-input](references/TECH-15-design-md-as-input.md).
> [TECH-15-design-md-as-input.md] What it does · When this TECH applies · The wireframe-builder's flow when DESIGN.md is the input · Token mapping — DESIGN.md to wireframe-builder's `brand_tokens` shape · Component tokens — direct passthrough · Failure paths · DESIGN.md fails lint · DESIGN.md is Variant 2 · DESIGN.md missing required fields · CLAUDE.md-coupled projects · Companion-file consumption · Symmetry with non-DESIGN.md inputs · Cross-references
  > What it does · When this TECH applies · The wireframe-builder's flow when DESIGN.md is the input · Token mapping — DESIGN.md to wireframe-builder's `brand_tokens` shape · Component tokens — direct passthrough · Failure paths · CLAUDE.md-coupled projects · Companion-file consumption · Symmetry with non-DESIGN.md inputs · Cross-references

## When the result is consumed downstream

When the user provides a DESIGN.md and then proceeds to Phase B (HTML rendering), `amw-wireframe-builder-agent` reads the DESIGN.md, validates it via `bin/amw-design-md-lint.sh`, and treats its tokens as canonical. On lint failure, the wireframe-builder reports and STOPS — the DESIGN.md path is symmetric with brand-researcher's extracted tokens, ascii-sketch's approved variant, and prose. See [TECH-15-design-md-as-input](references/TECH-15-design-md-as-input.md).
> [TECH-15-design-md-as-input.md] What it does · When this TECH applies · The wireframe-builder's flow when DESIGN.md is the input · Token mapping — DESIGN.md to wireframe-builder's `brand_tokens` shape · Component tokens — direct passthrough · Failure paths · DESIGN.md fails lint · DESIGN.md is Variant 2 · DESIGN.md missing required fields · CLAUDE.md-coupled projects · Companion-file consumption · Symmetry with non-DESIGN.md inputs · Cross-references

## Instructions

1. To normalize Variant 2 input, run `bin/amw-design-md-convert-v2-to-v1.py`. Validate the output against the [spec](../amw-design-md-spec/SKILL.md) (hand off to [audit](../amw-design-md-audit/SKILL.md)).
2. To produce downstream artifacts, run `bin/amw-design-md-emit-companions.py` (tokens.css / tokens.json / inventory / usage-prompt) and/or the DTCG exporter ([TECH-17](references/TECH-17-dtcg-export.md)).
> [TECH-17-dtcg-export.md] What it does · Why a dedicated DTCG exporter · DTCG schema mapping · Leaf shape · Group shape and `$type` inheritance · Alias syntax · Composite typography tokens · Source coverage · Harmonize mode · Bare-key rewrite · Type inference for unlabelled leaves · Idempotence · Validation contract · Round-trip contract with `amw-design-md-emit-companions.py` · CLI reference · Cross-references
3. To QA before delivery, run `bin/amw-design-md-showcase.py`.
4. At code-gen time, run the apply / token-enforcement pipeline per [TECH-19-design-md-apply](references/TECH-19-design-md-apply.md).
> [TECH-19-design-md-apply.md] What it does · When this TECH applies · The five-pass apply pipeline · Pass 1 — Raw-hex sweep · Pass 2 — Raw-px sweep · Pass 3 — Typography sweep · Pass 4 — WCAG contrast pair-check · Pass 5 — Do's and Don'ts enforcement · Replacement table — DESIGN.md slot → CSS-var name · Token-resolution algorithm · Failure paths · Worked example · Cross-references
5. To reuse a style across projects, use the cross-project library per [TECH-20-design-library](references/TECH-20-design-library.md).
> [TECH-20-design-library.md] What it does · Why a cross-project library · Library layout on disk · Proposed CLI surface · `amw-design-library list` · `amw-design-library use <name>` · `amw-design-library show <name>` · `amw-design-library remove <name>` · `amw-design-library diff <name-a> <name-b>` · `amw-design-library preview <name>` · `amw-design-library add <name>` · Naming convention · Workflow — "build this in the Linear style" · Integration with existing skills · Security and privacy · Limitations · Cross-references

## Hard rules

1. Variant 1 (official `<@google/design.md>`) is the canonical format; Variant 2 is accepted as input via the converter.
2. Tokens applied at code-gen time are enforced — raw hex / raw px that bypass the DESIGN.md tokens are swept and flagged per [TECH-19-design-md-apply](references/TECH-19-design-md-apply.md).
> [TECH-19-design-md-apply.md] What it does · When this TECH applies · The five-pass apply pipeline · Pass 1 — Raw-hex sweep · Pass 2 — Raw-px sweep · Pass 3 — Typography sweep · Pass 4 — WCAG contrast pair-check · Pass 5 — Do's and Don'ts enforcement · Replacement table — DESIGN.md slot → CSS-var name · Token-resolution algorithm · Failure paths · Worked example · Cross-references
3. No paywalled service, no API key beyond what `amw-dev-browser` already requires, no Chrome extension. The official CLI is `npx`-installable.
4. The skill never re-emits broad design vocabulary in tool-call text — that would re-trigger the orchestrator. See [skill-invocation-protocol](../amw-design-principles/references/skill-invocation-protocol.md).
> [skill-invocation-protocol.md] The problem · The protocol · Examples · Enforcement

## Resources

- [TECH-19-design-md-apply](references/TECH-19-design-md-apply.md) — apply / token-enforcement pipeline (used at code-gen time)
> [TECH-19-design-md-apply.md] What it does · When this TECH applies · The five-pass apply pipeline · Pass 1 — Raw-hex sweep · Pass 2 — Raw-px sweep · Pass 3 — Typography sweep · Pass 4 — WCAG contrast pair-check · Pass 5 — Do's and Don'ts enforcement · Replacement table — DESIGN.md slot → CSS-var name · Token-resolution algorithm · Failure paths · Worked example · Cross-references
- [TECH-17-dtcg-export](references/TECH-17-dtcg-export.md) — DTCG / W3C Design Tokens export
> [TECH-17-dtcg-export.md] What it does · Why a dedicated DTCG exporter · DTCG schema mapping · Leaf shape · Group shape and `$type` inheritance · Alias syntax · Composite typography tokens · Source coverage · Harmonize mode · Bare-key rewrite · Type inference for unlabelled leaves · Idempotence · Validation contract · Round-trip contract with `amw-design-md-emit-companions.py` · CLI reference · Cross-references
- [TECH-20-design-library](references/TECH-20-design-library.md) — cross-project DESIGN.md library at `~/.config/ai-maestro/design-library/`
> [TECH-20-design-library.md] What it does · Why a cross-project library · Library layout on disk · Proposed CLI surface · `amw-design-library list` · `amw-design-library use <name>` · `amw-design-library show <name>` · `amw-design-library remove <name>` · `amw-design-library diff <name-a> <name-b>` · `amw-design-library preview <name>` · `amw-design-library add <name>` · Naming convention · Workflow — "build this in the Linear style" · Integration with existing skills · Security and privacy · Limitations · Cross-references
- [TECH-15-design-md-as-input](references/TECH-15-design-md-as-input.md) — DESIGN.md as input to `amw-wireframe-builder-agent`
> [TECH-15-design-md-as-input.md] What it does · When this TECH applies · The wireframe-builder's flow when DESIGN.md is the input · Token mapping — DESIGN.md to wireframe-builder's `brand_tokens` shape · Component tokens — direct passthrough · Failure paths · DESIGN.md fails lint · DESIGN.md is Variant 2 · DESIGN.md missing required fields · CLAUDE.md-coupled projects · Companion-file consumption · Symmetry with non-DESIGN.md inputs · Cross-references
- [spec](../amw-design-md-spec/SKILL.md) · [author](../amw-design-md-author/SKILL.md) · [extract](../amw-design-md-extract/SKILL.md) · [audit](../amw-design-md-audit/SKILL.md) — sibling DESIGN.md skills
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (this skill is downstream)
- `<plugin-root>/bin/amw-design-md-convert-v2-to-v1.py` · `amw-design-md-emit-companions.py` · `amw-design-md-showcase.py` — the convert / emit / showcase scripts
