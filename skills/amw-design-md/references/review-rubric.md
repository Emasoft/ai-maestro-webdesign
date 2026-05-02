## Table of Contents

- [Output schema](#output-schema)
- [Structural checks (must-pass)](#structural-checks-must-pass)
  - [Variant 1 (canonical)](#variant-1-canonical)
  - [Variant 2 (community)](#variant-2-community)
- [Token-quality checks (must-pass — both variants)](#token-quality-checks-must-pass-both-variants)
- [Sync checks (must-pass — when companion files exist)](#sync-checks-must-pass-when-companion-files-exist)
- [Content-integrity checks (soft — affects score)](#content-integrity-checks-soft-affects-score)
- [A11y checks (must-pass — both variants)](#a11y-checks-must-pass-both-variants)
- [Scoring](#scoring)
- [What the rubric does NOT do](#what-the-rubric-does-not-do)
- [How `amw-design-md-author-agent` uses the rubric on its own output](#how-amw-design-md-author-agent-uses-the-rubric-on-its-own-output)
- [Cross-references](#cross-references)


# DESIGN.md review rubric

**Adapted from:** `docs_dev/extracted/google-labs/design-md-builder-main/design-md-builder-main/references/review-rubric.md` (Apache-2.0 / MIT, attributed to design-md-builder).

This is a deterministic, structured rubric used by `amw-design-md-auditor-agent` and the `amw-design-md` skill's pre-delivery checklist. The rubric is **pass/fail per check** and produces a single JSON verdict. It applies to BOTH variants — pure-V1 files skip the V2-specific checks (`S2`-`S4` XML boundary, `S5/S6` Mermaid). The auditor agent picks the right subset based on which variant it detects.

## Output schema

The auditor produces this JSON object (no markdown fences in the actual output):

```json
{
  "verdict": "PASS" | "REVISE",
  "score": 0-100,
  "variant_detected": 1 | 2,
  "checks": [
    {"id": "<check id>", "status": "pass" | "fail" | "n/a", "detail": "<why>"}
  ],
  "failures": [
    {"section": "<section>", "issue": "<what's wrong>", "fix": "<exact corrective action>"}
  ],
  "blocking_findings": [
    {"id": "<check id>", "severity": "P0" | "P1", "text": "<what to do>"}
  ]
}
```

`verdict = PASS` only if `score >= 85` AND `failures` is empty AND no `P0` findings.

---

## Structural checks (must-pass)

### Variant 1 (canonical)

| id | check |
|---|---|
| `S1.V1` | YAML frontmatter starts at line 1 with `---` and ends with `---` |
| `S2.V1` | YAML between delimiters is well-formed (parses without error) |
| `S3.V1` | At least one `## Overview` (or `## Brand & Style`) section present |
| `S4.V1` | Sections present follow the canonical 8-section order — none reordered |
| `S5.V1` | No duplicate section heading |
| `S6.V1` | At least the `colors.primary` token defined OR a `## Colors` section present |

### Variant 2 (community)

| id | check |
|---|---|
| `S1.V2` | All 9 numbered section headers present, in canonical order |
| `S2.V2` | XML boundary tags `<context>`, `<design_tokens>`, `<constraints>` each opened and closed exactly once |
| `S3.V2` | `<context>` precedes `<design_tokens>` precedes `<constraints>` |
| `S4.V2` | Section 9 (Agent Prompt Guide) is the final section in the file |
| `S5.V2` | At least one fenced ```mermaid``` code block present |
| `S6.V2` | Mermaid block parses: starts with valid diagram type, has nodes and edges |

---

## Token-quality checks (must-pass — both variants)

| id | check |
|---|---|
| `T1` | Every color value is a valid 3- or 6-digit hex, or rgba()/hsl()/oklab()/lch() — zero named CSS colors, zero placeholders |
| `T2` | Every typography row has: family, size (px/em/rem), weight (100-900), line-height, and (recommended) letter-spacing |
| `T3` | Every shadow formula uses rgba()/hex with explicit px offsets and blur — no soft/medium/heavy adjectives |
| `T4` | Spacing values conform to a single base unit (4px or 8px most common) |
| `T5` | Breakpoints listed as px values in ascending order |
| `T6` | Section 7 / "Do's and Don'ts" has minimum 3 dos and 3 don'ts |
| `T7` | Quick color reference present (V2 §9, V1 may live in `## Colors` prose) — explicit hex values |
| `T8` | `fontWeight` values are integers 100-900, not "bold"/"regular"/"light" strings |

---

## Sync checks (must-pass — when companion files exist)

| id | check |
|---|---|
| `X1` | Every color token name in DESIGN.md appears in `tokens.json` (if present) |
| `X2` | Every color token's value matches between DESIGN.md and `tokens.json` (no drift) |
| `X3` | `tokens.json` follows W3C Design Tokens format: tokens have `$value` and `$type` fields |
| `X4` | `CLAUDE.md` (if present) contains a literal instruction to read DESIGN.md at session start |
| `X5` | `CLAUDE.md` does not contradict DESIGN.md (e.g., different font family stated) |
| `X6` | `tokens.css` CSS variable values match DESIGN.md frontmatter values |

`n/a` if companion files do not exist. Only fails if files exist AND values drifted.

---

## Content-integrity checks (soft — affects score)

| id | check | weight |
|---|---|---|
| `C1` | No placeholder text remaining (`{{...}}`, `TODO`, `FIXME`, `TBD`, `???`, `<TODO>`) | -3 each |
| `C2` | Organization name stated in `<context>` block (V2) or `name:` frontmatter (V1) | -3 |
| `C3` | Do's and Don'ts are specific, not generic | -3 |
| `C4` | Responsive section includes at least one px value per breakpoint | -3 |
| `C5` | No duplicate headings (besides `##` sections) | -3 |
| `C6` | File length: 200-1500 lines (signal, not hard fail) | -3 if outside range |
| `C7` | At least one paragraph of prose under each section heading (no empty `## Foo` followed immediately by next `## Bar`) | -3 |
| `C8` | Section ordering matches canonical (V1: 8 sections; V2: 9 numbered) | -3 |

---

## A11y checks (must-pass — both variants)

| id | check |
|---|---|
| `A1` | Every declared color pair (foreground × background) achieves WCAG-AA contrast: 4.5:1 normal text, 3:1 large text |
| `A2` | If error/danger color is declared, its contrast against surface is documented |
| `A3` | Focus-ring color or formula is declared somewhere |
| `A4` | If animation tokens are present, a reduced-motion fallback is documented |

`A1` runs via `bin/amw-design-md-contrast.py`.

---

## Scoring

Start at 100. For each failure:

- Any must-pass check failing (`S*`, `T*`, `X*`, `A*`): **-15 points** AND adds to `failures[]` AND `blocking_findings[]` if `P0` (S* / A1 / A3).
- Soft check failing (`C*`): **-3 points each**, added to `checks[]` only (not `failures[]`) unless the cumulative drop pushes score below 85.

Floor at 0.

`verdict = PASS` iff (`score >= 85`) AND (`failures == []`) AND (no `P0` findings).

P0 (block delivery) findings:
- `S*` failures (file is structurally invalid)
- `A1` failures involving body text or primary CTAs
- `A3` failure when interactive components are declared

P1 (must fix before final delivery, may pass for draft):
- `T*` failures
- `X*` failures
- `A1` failures on edge components, `A2`, `A4`

P2 (warn only, doesn't block):
- `C*` failures

---

## What the rubric does NOT do

- **Never rewrites the file.** Audit-only.
- **Never invents new tokens.** Suggested fixes can rephrase or restructure but cannot fabricate hex values.
- **Never marks PASS if any P0 or P1 failure remains.** A score of 99 with one `T1` failure is still `REVISE`.
- **Does not score stylistic preferences.** "I'd prefer #3B82F6 over #4F46E5" is not a check.

---

## How `amw-design-md-author-agent` uses the rubric on its own output

After authoring a draft DESIGN.md, the author agent:

1. Runs `bin/amw-design-md-validate.py` (catches `S*`, `T*`).
2. Runs `bin/amw-design-md-contrast.py` (catches `A1`, `A2`).
3. Runs `bin/amw-design-md-lint.sh` if Variant 1 (the official linter).
4. Computes the rubric score on its own output.
5. If `score < 85` or any `P0`/`P1` failure remains: iterate. Cap at 3 self-revision rounds; if still failing, deliver as `status=partial` with the failures in `blocking_issues`.

---

## Cross-references

- [audit-passes](./audit-passes.md) — 5-pass audit (broader than the rubric)
- [canonical-spec-google-alpha](./canonical-spec-google-alpha.md) — Variant 1 spec
- [community-9-section-spec](./community-9-section-spec.md) — Variant 2 spec
- `../../../bin/amw-design-md-validate.py` — runs `S*` / `T*` checks
- `../../../bin/amw-design-md-contrast.py` — runs `A1` / `A2`
- `../../../bin/amw-design-md-lint.sh` — runs the official linter
