---
name: amw-design-md-extract
description: Extract a DESIGN.md from a live URL, Tailwind config, codebase scan, or Figma export. Triggers on "extract DESIGN.md from URL/Tailwind/codebase/Figma", "DESIGN.md fingerprint", "detect components for DESIGN.md". Does NOT trigger on generic "extract design tokens" (that routes to amw-design-extract). Use to faithfully transcribe an existing source into Variant 1.
version: 0.1.0
---

# AMW Design.md — Extract

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Faithfully transcribes an existing source (live URL, Tailwind config, codebase, Figma export) into a Variant 1 DESIGN.md. For the format itself read [spec](../amw-design-md-spec/SKILL.md); to author from a brief use [author](../amw-design-md-author/SKILL.md). DESIGN.md is one of several optional input/output formats the plugin accepts. Triggers are DESIGN.md-specific only.

## Overview

The extraction engine for DESIGN.md. Transcribes an existing source into a Variant 1 file — one-to-one, faithful, no invention. Three primary inputs: a live URL (via `amw-dev-browser`), a Tailwind config, and a codebase scan; plus a Figma input path. Ships component + state detection (codebase patterns + DOM landmarks + ARIA roles), inline-SVG/raster asset export with a `DESIGN.assets.json` manifest, and a deterministic SHA-256 token-block fingerprint.

## Activation

Callable when the user wants to *extract* a DESIGN.md from something that already exists. Also invoked by the orchestrator in main-agent mode, which may delegate to `amw-design-md-extractor-agent` (it reads this SKILL.md and its references). This skill is **autonomous and self-contained** — any agent can read this SKILL.md and the referenced files and execute the recipes without re-routing.

## Position in flow

OUTPUT (extract path) → conforms to the format owned by [spec](../amw-design-md-spec/SKILL.md). Reads an external source and emits a Variant 1 DESIGN.md plus optional `DESIGN.assets.json`. Distinct from the looser sibling `amw-design-extract` (which dumps tokens in many formats); this skill is the strict-DESIGN.md-format counterpart.

## What this skill is NOT

- Not the format reference — that is [spec](../amw-design-md-spec/SKILL.md).
- Not the loose token extractor — generic "extract design tokens from <url>" routes to `amw-design-extract`. Only "extract a *DESIGN.md*" reaches here.
- Not an inventor. Extraction is faithful transcription; if a value is absent in the source it is omitted, not guessed.
- Not the orchestrator. Generic "design system" requests route to `amw-design-principles`.

## Trigger conditions

Fires on: "extract DESIGN.md from <url>"; "extract DESIGN.md from <tailwind config>"; "extract DESIGN.md from <codebase>"; "extract DESIGN.md from Figma / Tokens Studio"; "fingerprint this DESIGN.md token block"; "detect components for DESIGN.md".

Does NOT fire on "extract design tokens from <url>" (→ `amw-design-extract`), "create a DESIGN.md from a brief" (→ [author](../amw-design-md-author/SKILL.md)), or generic "design a page" / "design system" (→ `amw-design-principles`).

## The extract operations

- **From a live URL:** `bin/amw-design-md-from-url.sh <url> -o <output-path>` — delegates DOM + computed-style extraction to the plugin's `amw-dev-browser` skill, then emits Variant 1 frontmatter.
- **From a Tailwind config:** `node bin/amw-design-md-from-tailwind.mjs --config <tailwind.config.ts> --css <globals.css> --out <DESIGN.md>` — pure-local Node.js port; resolves CSS-var references and annotates color pairs with WCAG-AA contrast.
- **From a codebase scan:** `bin/amw-design-md-from-codebase.py <project-root>` — pure-Python scanner; detects shadcn / Tailwind / Chakra / vanilla-CSS / styled-components and emits a draft DESIGN.md.

## Detection, asset export, and fingerprinting

- **Component + state detection** (five codebase patterns in priority order + URL DOM-landmark + ARIA-role table + boolean-prop / pseudo-class / variant-enum state cascade): [TECH-extractor-component-detection](references/TECH-extractor-component-detection.md).
  > When the extractor runs component detection · Codebase detection — five patterns, in priority order · URL detection — DOM landmarks + ARIA roles · State detection (T-094) · shadcn / Radix specific signals · What the extractor skips · Confidence and fallbacks · Output — what lands in DESIGN.md · Validation gate · Cross-references
- **Inline-SVG icon export + raster asset export + `DESIGN.assets.json` manifest** (role assignment + alt-text inference + license/provenance): [TECH-extractor-icon-asset-export](references/TECH-extractor-icon-asset-export.md).
  > When this runs · Phase A — Discovery · Phase B — Role assignment (T-093 + T-095) · Phase C — Alt-text inference (T-095, raster only) · Phase D — Export · License + provenance · Privacy + robots compliance · What the extractor refuses to do · Cross-references
- **Deterministic SHA-256 token-block fingerprint** (canonicalization recipe + interpretation + cross-project library lookup): [TECH-extractor-fingerprinting](references/TECH-extractor-fingerprinting.md).
  > Goal · Algorithm · Concrete recipe (pure-Python, no extra deps) · Interpretation guide · Non-goals (what fingerprinting is NOT) · Versioning the algorithm · Validation gate · Cross-references
- **Figma input path** (Tokens Studio export + pre-flight checklist + mapping-coverage table + lossy surface): [TECH-18-figma-input-path](references/TECH-18-figma-input-path.md).
> [TECH-18-figma-input-path.md] What it does · Why a dedicated Figma input path · Two supported workflows · Workflow A — Tokens Studio export from Figma · Workflow B — Local styles export via Figma plugin · Pre-flight checklist for the user · Mapping coverage table · Lossy surface — what does NOT round-trip · Failure paths · Cross-references
  > What it does · Why a dedicated Figma input path · Two supported workflows · Pre-flight checklist for the user · Mapping coverage table · Lossy surface — what does NOT round-trip · Failure paths · License and attribution · Cross-references

## Instructions

1. Choose the input path: `bin/amw-design-md-from-url.sh`, `bin/amw-design-md-from-tailwind.mjs`, `bin/amw-design-md-from-codebase.py`, or the Figma path ([TECH-18](references/TECH-18-figma-input-path.md)) based on the source type.
> [TECH-18-figma-input-path.md] What it does · Why a dedicated Figma input path · Two supported workflows · Workflow A — Tokens Studio export from Figma · Workflow B — Local styles export via Figma plugin · Pre-flight checklist for the user · Mapping coverage table · Lossy surface — what does NOT round-trip · Failure paths · Cross-references
2. Run component + state detection per [TECH-extractor-component-detection](references/TECH-extractor-component-detection.md); export icons/assets per [TECH-extractor-icon-asset-export](references/TECH-extractor-icon-asset-export.md) when present.
> [TECH-extractor-icon-asset-export.md] When this runs · Phase A — Discovery · Phase B — Role assignment (T-093 + T-095) · Phase C — Alt-text inference (T-095, raster only) · Phase D — Export · License + provenance · Privacy + robots compliance · What the extractor refuses to do · Cross-references
> [TECH-extractor-component-detection.md] When the extractor runs component detection · Codebase detection — five patterns, in priority order · URL detection — DOM landmarks + ARIA roles · State detection (T-094) · shadcn / Radix specific signals · What the extractor skips · Confidence and fallbacks · Output — what lands in DESIGN.md · Validation gate · Cross-references
3. Fingerprint the canonical token block ([TECH-extractor-fingerprinting](references/TECH-extractor-fingerprinting.md)) for cross-project library lookup.
> [TECH-extractor-fingerprinting.md] Goal · Algorithm · Concrete recipe (pure-Python, no extra deps) · Interpretation guide · Non-goals (what fingerprinting is NOT) · Versioning the algorithm · Validation gate · Cross-references
4. Validate the extracted Variant 1 file against the [spec](../amw-design-md-spec/SKILL.md) — hand off to [audit](../amw-design-md-audit/SKILL.md) for the lint gate. Fail fast if the linter reports errors.

## Hard rules

1. Extraction is faithful transcription into Variant 1 (official `<@google/design.md>`). Absent values are omitted, never invented.
2. No paywalled service, no API key beyond what `amw-dev-browser` already requires, no Chrome extension. The official CLI is `npx`-installable, no remote calls.
3. The skill never re-emits broad design vocabulary in tool-call text — that would re-trigger the orchestrator. See [skill-invocation-protocol](../amw-design-principles/references/skill-invocation-protocol.md).
> [skill-invocation-protocol.md] The problem · The protocol · Examples · Enforcement

## Examples

**Extract DESIGN.md from a live URL:** Input `https://stripe.com`. `amw-design-md-from-url.sh` delegates to `amw-dev-browser/` for DOM + computed styles, then transcribes faithfully into Variant 1. Output: `stripe.DESIGN.md` with one-to-one source attribution (plus `DESIGN.assets.json` when inline SVG icons are present).

## Resources

- [TECH-extractor-component-detection](references/TECH-extractor-component-detection.md) — component detection (T-091) + state detection (T-094)
> [TECH-extractor-component-detection.md] When the extractor runs component detection · Codebase detection — five patterns, in priority order · URL detection — DOM landmarks + ARIA roles · State detection (T-094) · shadcn / Radix specific signals · What the extractor skips · Confidence and fallbacks · Output — what lands in DESIGN.md · Validation gate · Cross-references
- [TECH-extractor-icon-asset-export](references/TECH-extractor-icon-asset-export.md) — inline SVG icon export (T-093) + raster asset export (T-095) + `DESIGN.assets.json` manifest
> [TECH-extractor-icon-asset-export.md] When this runs · Phase A — Discovery · Phase B — Role assignment (T-093 + T-095) · Phase C — Alt-text inference (T-095, raster only) · Phase D — Export · License + provenance · Privacy + robots compliance · What the extractor refuses to do · Cross-references
- [TECH-extractor-fingerprinting](references/TECH-extractor-fingerprinting.md) — deterministic SHA-256 token-block fingerprint (T-096)
> [TECH-extractor-fingerprinting.md] Goal · Algorithm · Concrete recipe (pure-Python, no extra deps) · Interpretation guide · Non-goals (what fingerprinting is NOT) · Versioning the algorithm · Validation gate · Cross-references
- [TECH-18-figma-input-path](references/TECH-18-figma-input-path.md) — Figma → DESIGN.md (Tokens Studio export + pre-flight checklist)
> [TECH-18-figma-input-path.md] What it does · Why a dedicated Figma input path · Two supported workflows · Workflow A — Tokens Studio export from Figma · Workflow B — Local styles export via Figma plugin · Pre-flight checklist for the user · Mapping coverage table · Lossy surface — what does NOT round-trip · Failure paths · Cross-references
- [spec](../amw-design-md-spec/SKILL.md) · [author](../amw-design-md-author/SKILL.md) · [audit](../amw-design-md-audit/SKILL.md) · [convert](../amw-design-md-convert/SKILL.md) — sibling DESIGN.md skills
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (this skill is downstream)
- [SKILL](../amw-dev-browser/SKILL.md) — browser primitive used by URL extraction
- [SKILL](../amw-design-extract/SKILL.md) — looser sibling token extractor (this skill is the strict-format counterpart)
- `<plugin-root>/bin/amw-design-md-from-url.sh` · `from-tailwind.mjs` · `from-codebase.py` — the extract scripts
