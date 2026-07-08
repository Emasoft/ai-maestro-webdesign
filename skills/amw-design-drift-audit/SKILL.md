---
name: amw-design-drift-audit
description: Audit a Tailwind config / CSS custom-properties file / tokens.json for design-token DRIFT — near-duplicate color clusters (CIEDE2000 ΔE<3), off-scale spacing/radius values, single-use magic numbers — and emit a harmonization recommendation report. Audit-only (never modifies the source). Triggers on "audit design tokens for drift", "find duplicate colors", "check spacing scale consistency", "harmonize tokens", "tokens.json drift audit", "tailwind config drift". Does NOT trigger on generic "design" / "style" / "design system" — those route to design-principles or design-extract/design-md.
---

# Design Drift Audit

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is an executor. Triggers are token-drift-audit-specific only.

## Overview

Scans an existing design-token surface (Tailwind config, CSS custom properties, tokens.json, DESIGN.md `tokens:` block) and produces a **drift report** + **harmonization recommendation**. Three failure modes are detected:

1. **Color drift** — near-duplicate colors (CIEDE2000 ΔE<3) that should collapse to one token.
2. **Scale drift** — spacing, radius, font-size values that fall outside the project's declared scale (e.g. a 7px padding in a 4/8/12/16/24 system).
3. **Magic numbers** — values used exactly once across the whole codebase, indicating an ad-hoc decision that should either be promoted to a token or aligned to an existing one.

**Audit-only.** This skill diagnoses; it never rewrites the config. The output is a markdown report a human (or a follow-up agent in main-agent mode) acts on.

## Activation

Callable directly via the `/amw-audit-token-drift` command (when added), or invoked by the orchestrator during a `design-md-auditor` pass or a periodic plugin-maintenance sweep. Also useful before a Tailwind v3→v4 migration to surface tokens that won't survive the upgrade cleanly.

This skill is **autonomous and self-contained** — any agent (main-agent, sub-agent, external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

GOVERNANCE. Sits between `amw-design-extract` (input — extracts tokens from a URL) and `amw-design-md` (canonical — authors / lints a DESIGN.md). The drift audit looks at the CURRENT state of a token surface and reports inconsistencies; it does not author, extract, or convert.

For DESIGN.md-level structural audits (frontmatter validity, section completeness, WCAG-AA contrast), prefer **`amw-design-md`** (`design-md-lint.sh` + `design-md-contrast.py`). This skill is the looser, codebase-wide drift detector that runs across whatever token surface exists (Tailwind / CSS-vars / tokens.json / DESIGN.md tokens).

## Trigger conditions

Fires on these specific phrasings:

- "audit design tokens for drift"
- "find duplicate colors in tokens.json"
- "check spacing scale consistency"
- "harmonize tokens"
- "tokens.json drift audit"
- "tailwind config drift report"
- "find near-duplicate colors in tailwind.config"
- "detect off-scale spacing values"
- "single-use magic numbers in CSS vars"

Do NOT fire on: "design a landing page", "extract design tokens from <url>", "lint my DESIGN.md", "create a design system". Those route to design-principles, design-extract, design-md, or design-system-presets respectively.

## Inputs (required)

The audit needs at least ONE token surface to scan. Acceptable inputs:

- **Tailwind config** — `tailwind.config.js` / `tailwind.config.ts` / `globals.css` with `@theme` block (Tailwind v4).
- **CSS custom properties** — `:root { --color-primary: ... }` blocks in any `.css` file.
- **tokens.json** — W3C Design Tokens Format Module shape (`$value`, `$type`) or shadcn-style flat key-value.
- **DESIGN.md** — the `tokens:` YAML frontmatter block from a `@google/design.md` Variant 1 document.

If multiple surfaces are present, audit each independently AND report any cross-surface conflicts (e.g. Tailwind `primary: #2563eb` vs CSS `--color-primary: #1d4ed8`).

## Audit procedure

See [audit-procedure](references/audit-procedure.md) for the detailed step-by-step. Summary:
> [audit-procedure.md] Phase 0 — Parse the token surface · Phase 1 — Color drift (CIEDE2000 ΔE<3) · Phase 2 — Scale drift (off-step values) · Phase 3 — Magic numbers (single-use tokens) · Phase 4 — Cross-surface conflicts · Phase 5 — Emit report

1. **Parse** the input surface into a normalized list of `(token-name, category, value, source-location)` tuples.
2. **Category-1 (color drift)** — for every pair of colors in the same category (background / text / border / brand), compute CIEDE2000 ΔE. Cluster pairs with ΔE<3.0. A cluster of 2+ tokens with low ΔE is a drift finding.
3. **Category-2 (scale drift)** — infer the project's declared scale (the modal spacing step, e.g. 4px or 0.25rem). Flag any spacing / radius / font-size value that is not an integer multiple of the step AND not on a documented exception list (e.g. `1px` border, `0.5px` hairline).
4. **Category-3 (magic numbers)** — count usage of each token value across the codebase. A token used exactly once is a candidate for either promotion (rename to a meaningful semantic token) or elimination (inline back to a parent scale value).
5. **Emit report** — one markdown table per category + a top-level summary with severity (HIGH = >5 findings per category, MEDIUM = 3–5, LOW = 1–2, CLEAN = 0).

## What this skill MUST NOT do

- Rewrite the Tailwind config, CSS file, or tokens.json. The report describes WHAT to change, not HOW; humans (or a follow-up agent) apply changes.
- Bump versions, commit, or push.
- Suggest specific replacement values that aren't already on the project's declared scale — e.g. don't suggest a new `#3b82f6` token; instead say "values X, Y, Z are near-duplicates of existing `primary-500` — consider collapsing".
- Run on a codebase the user has not pointed at. The skill needs an explicit input path; refuse if none was provided.

## Output contract

A single markdown file at the path the orchestrator specifies (default: `$MAIN_ROOT/reports/design-drift/<timestamp>-drift-audit.md`). Sections:

1. **Summary** — overall verdict (CLEAN / LOW / MEDIUM / HIGH) + count per category.
2. **Color drift** — table: cluster ID | tokens | ΔE | recommendation.
3. **Scale drift** — table: token | value | declared scale | nearest aligned value | recommendation.
4. **Magic numbers** — table: token | value | usage count | promotion-or-eliminate recommendation.
5. **Cross-surface conflicts** (if multiple surfaces) — table: token name | surface-A value | surface-B value.
6. **Next steps** — bullet list of human-actionable items, ordered by impact.

## Examples

CLEAN:
```
amw-design-drift-audit — tailwind.config.ts (47 tokens)
CLEAN: 0 color clusters, 0 off-scale spacing, 0 single-use magic numbers.
Nothing to harmonize.
```

DRIFT:
```
amw-design-drift-audit — globals.css + tailwind.config.ts (89 tokens)
HIGH severity: 7 color clusters, 4 off-scale spacing, 12 single-use magic numbers.

Color drift (top finding):
  cluster-01: --color-primary (#2563eb), --color-brand (#2864ec), brand-blue (#2762ed)
    ΔE max: 1.4 — collapse to one token.

Scale drift (top finding):
  --space-7px: 7px (declared scale: 4/8/12/16/24/32) — align to 8px.

Magic numbers (top finding):
  --shadow-very-specific: 0 2px 11px rgba(15, 23, 42, 0.07) — used once;
  consider eliminating or promoting to elevation-3.
```

## References

- [audit-procedure](references/audit-procedure.md) — detailed step-by-step audit algorithm (color clustering, scale inference, magic-number detection).
> [audit-procedure.md] Phase 0 — Parse the token surface · Phase 1 — Color drift (CIEDE2000 ΔE<3) · Phase 2 — Scale drift (off-step values) · Phase 3 — Magic numbers (single-use tokens) · Phase 4 — Cross-surface conflicts · Phase 5 — Emit report
- [ciede2000-implementation](references/ciede2000-implementation.md) — pure-Python CIEDE2000 ΔE implementation (no external deps) for color-drift detection.
> [ciede2000-implementation.md] Implementation · Validation · Why CIEDE2000 instead of CIE76 / Lab Euclidean

## Provenance

Clean-room implementation. The drift-audit problem is well-known in design-system maintenance literature (Style Dictionary, Theo, Specify, Tokens Studio all touch parts of it); this skill defines the workflow procedurally for an LLM-driven audit pass without copying code from any specific upstream project.
