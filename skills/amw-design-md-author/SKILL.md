---
name: amw-design-md-author
description: Author a DESIGN.md from a brief, interview, archetype, or 5-question flow. Triggers on "create/author/make a DESIGN.md", "DESIGN.md from brief", "brand archetype DESIGN.md", "DESIGN.md agent prompt guide", "DESIGN.md i18n/CJK". Does NOT trigger on extraction-from-source or generic design. Use to write a new DESIGN.md with the lint+contrast gate.
version: 0.1.0
---

# AMW Design.md — Author

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Writes a new DESIGN.md from a brief, interview, brand archetype, or 5-question flow, with a mandatory lint + WCAG-AA contrast gate. For the format itself read [spec](../amw-design-md-spec/SKILL.md); to extract from an existing source use [extract](../amw-design-md-extract/SKILL.md); to lint/score an existing file use [audit](../amw-design-md-audit/SKILL.md). DESIGN.md is one of several optional input/output formats the plugin accepts. Triggers are DESIGN.md-specific only.

## Overview

The authoring engine for DESIGN.md. Takes a brief / interview / brand archetype / 5-question flow and produces a Variant 1 file, gated by `bin/amw-design-md-lint.sh` (official linter) and `bin/amw-design-md-contrast.py` (per-pair WCAG-AA contrast). Ships the brand-archetype pre-fill library, the extended-section guidance (motion/a11y/iteration/known-gaps/agent-prompt-guide), the `{token.ref}` interpolation contract, the three-path routing decision, the STYLE-REFERENCES.md companion, and CJK localization.

## Activation

Callable when the user wants to *create* a DESIGN.md. Also invoked by the orchestrator in main-agent mode, which may delegate to `amw-design-md-author-agent` (it reads this SKILL.md and its references to do the work). This skill is **autonomous and self-contained** — any agent can read this SKILL.md and the referenced files and execute the recipes without re-routing.

## Position in flow

OUTPUT (author path). Produces a Variant 1 DESIGN.md (plus, when asked, the STYLE-REFERENCES.md companion). Conforms to the format owned by [spec](../amw-design-md-spec/SKILL.md). After authoring, the lint+contrast gate runs; on failure the [audit](../amw-design-md-audit/SKILL.md) recovery flow applies. Downstream, the file is consumed by `amw-wireframe-builder-agent` (see [convert](../amw-design-md-convert/SKILL.md) for the as-input contract).

## What this skill is NOT

- Not the format reference — that is [spec](../amw-design-md-spec/SKILL.md).
- Not an extractor — faithfully transcribing a live URL / Tailwind config / codebase into a DESIGN.md is [extract](../amw-design-md-extract/SKILL.md).
- Not the orchestrator. Generic "design system" / "design a page" requests route to `amw-design-principles`.

## Trigger conditions

Fires on: "create/author/make a DESIGN.md"; "DESIGN.md from a brief / interview"; "brand-archetype DESIGN.md"; "DESIGN.md agent prompt guide (§9)"; "DESIGN.md i18n / CJK localization"; "DESIGN.md motion / a11y extended sections"; "STYLE-REFERENCES.md companion".

Does NOT fire on "extract DESIGN.md from <url|tailwind|codebase>" (→ [extract](../amw-design-md-extract/SKILL.md)) or generic "design a landing page" / "design system" (→ `amw-design-principles`).

## The author operation

Read the Variant 1 skeleton from [spec](../amw-design-md-spec/SKILL.md) ([canonical-template](../amw-design-md-spec/references/canonical-template.md)). Fill it from the brief / interview / codebase / URL, then run the gate:

1. **Lint gate (mandatory):** `bin/amw-design-md-lint.sh <path>` (wraps `npx @google/design.md lint`). Lint failure halts delivery.
2. **WCAG-AA contrast pre-flight (mandatory):** `bin/amw-design-md-contrast.py <path>` runs pair-level contrast on every color pair. Failures go to `warnings`, not silent omission.

## Routing, archetypes, and the extended sections

- **Three-path routing** — decide up front whether a DESIGN.md already exists (Path A), the project needs one (Path B, 4-item interview → variants → write), or this is a one-off (Path C): [TECH-28-three-path-routing](references/TECH-28-three-path-routing.md).
  > What it does · The three paths · Path A — DESIGN.md exists · Path B — No DESIGN.md, project-setup mode · Path C — No DESIGN.md, one-off task · Routing decision tree · Why three paths and not two or four · Cross-references
- **Five brand archetypes** for fast pre-fill (Dark Technical / Luxury Automotive / Fintech / Developer Platform / AI ML): [TECH-25-brand-archetypes](references/TECH-25-brand-archetypes.md).
  > What it does · Why archetypes accelerate extraction · The five archetypes · How to detect an archetype · Pre-fill workflow · Cautions · Cross-references
- **Extended §7-8 (Motion + Accessibility)** for motion-heavy / a11y-heavy brands: [TECH-26-extended-sections-7-8](references/TECH-26-extended-sections-7-8.md).
  > What it does · Why these are "extended" · When to include · §7-ext Motion (extended) · §8-ext Accessibility (extended) · Numbering convention · Linting the extended sections · Cross-references
- **Extended §10 Iteration Guide + §11 Known Gaps:** [TECH-22-section-10-11-extended](references/TECH-22-section-10-11-extended.md).
  > What it does · Position in the section order · §10 Iteration Guide · §11 Known Gaps · Linting rules · When to omit · Cross-references
- **§9 Agent Prompt Guide** (CSS snippets / authoring sentence / "do not use" / voice descriptor): [TECH-23-section-9-agent-prompt-guide](references/TECH-23-section-9-agent-prompt-guide.md).
  > What it does · Why §9 exists · The four required subsections · Why copy-paste-ready matters · Worked example · What §9 is NOT · Linting §9 · Cross-references

## Token interpolation, companion, and localization

- **`{token.ref}` interpolation + dead-reference detection** (prose references tokens, never raw values): [TECH-27-token-interpolation](references/TECH-27-token-interpolation.md).
  > What it does · The interpolation contract · Syntax · Why prose references tokens, not raw values · Dead-reference detection · Resolution order · Where interpolation is enforced · Where interpolation is suggested but not enforced · Worked examples · Lint message format · Implementation notes · Cross-references
- **STYLE-REFERENCES.md companion** (6 sections: Design Lineage / Peer / Anti / Component Gallery / Style Vocabulary / Cross-Medium): [TECH-21-style-references-companion](references/TECH-21-style-references-companion.md).
  > What it does · Why a separate file · The six mandatory sections · Emission contract · How agents consume it · Linting STYLE-REFERENCES.md · Synchronization with DESIGN.md · Cross-references
- **CJK localization (JP / KO / ZH):** [TECH-cjk-localization](references/TECH-cjk-localization.md).
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references · Source attribution

## Instructions

1. Run the three-path routing decision ([TECH-28-three-path-routing](references/TECH-28-three-path-routing.md)) to confirm authoring is the right action.
2. If the brand fits an archetype, pre-fill from [TECH-25-brand-archetypes](references/TECH-25-brand-archetypes.md); otherwise fill the [canonical-template](../amw-design-md-spec/references/canonical-template.md) from the brief.
3. Add extended sections only when the brand warrants them (motion/a11y → TECH-26; iteration/gaps → TECH-22; §9 agent guide → TECH-23).
4. Reference tokens in prose via `{token.ref}` per [TECH-27-token-interpolation](references/TECH-27-token-interpolation.md); never inline raw hex/px.
5. Run the lint gate (`bin/amw-design-md-lint.sh`) and the contrast pre-flight (`bin/amw-design-md-contrast.py`). Fail fast on lint errors; route contrast failures to `warnings`.
6. Emit STYLE-REFERENCES.md ([TECH-21](references/TECH-21-style-references-companion.md)) and localize ([TECH-cjk-localization](references/TECH-cjk-localization.md)) when requested.

## Hard rules

1. The author path produces Variant 1 (official `<@google/design.md>`) as canonical output.
2. Every authored DESIGN.md MUST pass `bin/amw-design-md-lint.sh` before being delivered. Lint failure halts delivery.
3. WCAG-AA contrast checks via `bin/amw-design-md-contrast.py` run on every authored DESIGN.md. Failures go to `warnings`, not silent omission.
4. No paywalled service, no API key beyond what `amw-dev-browser` already requires, no Chrome extension. The official CLI is `npx`-installable.
5. The skill never re-emits broad design vocabulary in tool-call text — that would re-trigger the orchestrator. See [skill-invocation-protocol](../amw-design-principles/references/skill-invocation-protocol.md).

## Examples

**Author DESIGN.md from a brief (Variant 1):** Input "fintech dashboard, brand `#0F4C81`, secondary `#FFD23F`, Inter body / Manrope headings, WCAG AA." Lint gate runs `amw-design-md-lint.sh`; contrast pre-flight runs `amw-design-md-contrast.py`. Output: `DESIGN.md` (Variant 1) plus companions via [convert](../amw-design-md-convert/SKILL.md) when requested.

## Resources

- [TECH-25-brand-archetypes](references/TECH-25-brand-archetypes.md) — 5-archetype pre-fill library
- [TECH-26-extended-sections-7-8](references/TECH-26-extended-sections-7-8.md) — optional §7-ext Motion + §8-ext Accessibility
- [TECH-22-section-10-11-extended](references/TECH-22-section-10-11-extended.md) — optional §10 Iteration Guide + §11 Known Gaps
- [TECH-23-section-9-agent-prompt-guide](references/TECH-23-section-9-agent-prompt-guide.md) — optional §9 Agent Prompt Guide
- [TECH-27-token-interpolation](references/TECH-27-token-interpolation.md) — {token.ref} interpolation + dead-reference detection
- [TECH-28-three-path-routing](references/TECH-28-three-path-routing.md) — Path A / B / C routing
- [TECH-21-style-references-companion](references/TECH-21-style-references-companion.md) — STYLE-REFERENCES.md 6-section companion
- [TECH-cjk-localization](references/TECH-cjk-localization.md) — CJK localization (JP/KO/ZH)
- [spec](../amw-design-md-spec/SKILL.md) · [extract](../amw-design-md-extract/SKILL.md) · [audit](../amw-design-md-audit/SKILL.md) · [convert](../amw-design-md-convert/SKILL.md) — sibling DESIGN.md skills
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator (this skill is downstream)
- `<plugin-root>/bin/amw-design-md-lint.sh` · `<plugin-root>/bin/amw-design-md-contrast.py` — the author gate
