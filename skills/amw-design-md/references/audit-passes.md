## Table of Contents

- [Pass 1 — Structural](#pass-1-structural)
- [Pass 2 — Drift](#pass-2-drift)
- [Pass 3 — Accessibility](#pass-3-accessibility)
- [Pass 4 — Completeness](#pass-4-completeness)
- [Pass 5 — Consistency](#pass-5-consistency)
- [Output file format](#output-file-format)
- [What the auditor does NOT do](#what-the-auditor-does-not-do)
- [Pre-flight checks](#pre-flight-checks)
- [Cross-references](#cross-references)


# 5-pass DESIGN.md audit

**Adapted from:** `docs_dev/extracted/google-labs/MDDesign-main/MDDesign-main/commands/critique.md` (Apache-2.0). The MDDesign skill defines a 5-pass audit; this file ports the audit dimensions to the plugin's `amw-design-md-auditor-agent` and the `bin/amw-design-md-validate.py` offline validator.

The 5-pass audit is broader than [review-rubric](review-rubric.md). The rubric is a structured pass/fail checklist for a single file; the audit examines a DESIGN.md against the **actual code** of the project that uses it, looking for drift, orphan tokens, contrast failures, and consistency gaps.

The auditor produces `<DESIGN.md>.critique.md` adjacent to the input, listing findings with stable IDs (`F1`, `F2`, ...) and proposed fixes. The auditor never edits DESIGN.md itself.

---

## Pass 1 — Structural

**Goal:** Verify the file is structurally valid against the relevant spec.

**Checks (delegate to `bin/amw-design-md-lint.sh` for Variant 1):**

- Frontmatter starts at line 1 with `---` and ends with `---` (V1 only).
- YAML between delimiters is well-formed.
- Section headings match the canonical order (V1: 8 sections; V2: 9 sections).
- No duplicate section headings.
- Token references `{path.to.token}` resolve to existing paths (V1).
- `colors.*` values are valid hex.
- `Dimension` values use px/em/rem (V1).
- `fontWeight` values are integers 100-900 (V1).

**Tools:**
- Variant 1: `bin/amw-design-md-lint.sh DESIGN.md`
- Variant 2: rule-based parser in `bin/amw-design-md-validate.py --variant 2`

**Findings format:**
```
F<n>: [Pass 1 / structural / P<0|1|2>]
  Finding: <one-line summary>
  Evidence: <line numbers, exact text>
  Fix: <exact corrective action>
  Slash: /amw-design-md-lint
```

---

## Pass 2 — Drift

**Goal:** Detect divergence between DESIGN.md tokens and the actual code in the project that uses them.

**Checks:**

- **Orphan tokens:** Tokens declared in DESIGN.md frontmatter but never used in the project's source code (e.g., `colors.tertiary` declared but no `bg-tertiary`, `text-tertiary`, or `var(--tertiary)` reference anywhere).
- **Leak tokens:** Hex values, named CSS colors, or font families that appear in code but were not declared in DESIGN.md (e.g., `<div style="background: #ff0000">` when `#ff0000` is not in the palette).
- **Near-duplicate tokens:** Color pairs with ΔE < 5 (perceptually similar enough to be unintended duplicates) or radii within ±1px of each other.
- **Stale companion files:** `tokens.css` / `tokens.json` whose values don't match DESIGN.md's frontmatter.

**Tools:**
- `bin/amw-design-md-from-codebase.py <project-root>` — produces a draft DESIGN.md from current code; the auditor diffs the draft against the existing DESIGN.md to find drift.
- Filesystem scan for `*.css`, `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.html` files containing hex/rgb literals.

**Findings format:**
```
F<n>: [Pass 2 / drift / P1]
  Finding: Token `colors.tertiary` (#B8422E) declared but unused in 0/47 source files.
  Evidence: DESIGN.md L8; greppable in src/ — 0 hits for tertiary, B8422E
  Fix: Either remove the token from DESIGN.md frontmatter, or use it in at least one component.
  Slash: /amw-design-md-audit (will not auto-fix)
```

---

## Pass 3 — Accessibility

**Goal:** Verify the design system meets WCAG-AA at minimum on declared color pairs.

**Checks:**

- **Body text contrast:** Every text-on-surface color pair achieves 4.5:1.
- **Large text contrast:** ≥ 18px or ≥ 14px-bold text on surface achieves 3:1.
- **Interactive contrast:** Button background vs button text ≥ 4.5:1; button text vs surface ≥ 3:1.
- **Focus-ring contrast:** Declared focus-ring color vs surface ≥ 3:1.
- **Disabled-state contrast:** Documented or warned (not a hard fail; AA exempts disabled).
- **Reduced-motion fallback:** If animation tokens are present, a `prefers-reduced-motion` rule is documented.
- **Error-state contrast:** Danger color vs surface ≥ 4.5:1 for the typical use case (error message text).

**Tools:**
- `bin/amw-design-md-contrast.py DESIGN.md` — outputs every color-pair contrast ratio.

**Findings format:**
```
F<n>: [Pass 3 / accessibility / P0]
  Finding: text-secondary (#A0A8B0) on surface (#FFFFFF) = 2.98:1, fails WCAG-AA 4.5:1 for normal text.
  Evidence: DESIGN.md frontmatter L4, L7; pair tested by bin/amw-design-md-contrast.py
  Fix: Darken text-secondary to at least #6C7278 to reach 4.66:1, or restrict text-secondary to large text only (3:1 threshold).
  Slash: (no auto-fix; requires design decision)
```

---

## Pass 4 — Completeness

**Goal:** Verify the design system covers the surfaces the project actually uses.

**Checks:**

- **Component states:** For every declared component (`button-primary`, `input-default`), check that `*-hover`, `*-active`, `*-focus`, `*-disabled`, `*-error` variants are declared (or that the prose explains how state changes derive from the base).
- **Dark-mode counterparts:** If the project's source code references a dark-mode toggle (`dark:` Tailwind prefix, `[data-theme="dark"]`, `prefers-color-scheme: dark`), check that DESIGN.md addresses dark mode (either via separate dark-mode tokens or explicit prose).
- **Responsive breakpoints:** Project uses `sm:` / `md:` / `lg:` Tailwind classes — check that DESIGN.md `## Layout` or `## Responsive Behavior` defines them.
- **Empty / loading / error states:** Project has empty-state UI surfaces — check DESIGN.md addresses them (typically in `## Components` or `## Do's and Don'ts`).

**Findings format:**
```
F<n>: [Pass 4 / completeness / P1]
  Finding: button-primary declared but no -hover, -active, -focus, -disabled variants.
  Evidence: DESIGN.md frontmatter L60-65; project src/components/Button.tsx L42-58 sets hover/active/focus styles inline.
  Fix: Add button-primary-hover / -active / -focus / -disabled to components: frontmatter, OR add `## Components` prose explicitly stating "states inherit from base via {opacity, brightness} adjustments".
  Slash: (no auto-fix; the fix is a token-authoring decision)
```

---

## Pass 5 — Consistency

**Goal:** Verify the declared scales are mathematically consistent (geometric or arithmetic progression).

**Checks:**

- **Spacing scale:** Values should follow a consistent multiplier (typically ×2 or ×1.5) — e.g., `4 / 8 / 16 / 32 / 64` (×2) or `4 / 6 / 8 / 12 / 16 / 24 / 32 / 48 / 64` (×1.5). Random values like `4 / 9 / 18 / 35 / 50` are inconsistent.
- **Radius scale:** Same — geometric progression preferred (`4 / 8 / 12 / 16` arithmetic; `2 / 4 / 8 / 16` geometric ×2).
- **Font-size scale:** Should follow a modular scale (typically major-second 1.125, perfect-fourth 1.333, or custom).
- **Line-height progression:** Should typically inversely correlate with font-size (large text gets tighter line-height, small text looser).
- **Color-palette consistency:** If the system uses a tonal scale (`primary-10`, `primary-30`, `primary-60`, etc.), check that lightness values follow a consistent scale.

**Findings format:**
```
F<n>: [Pass 5 / consistency / P2]
  Finding: Spacing scale (4 / 8 / 12 / 24 / 48) skips the 16 step, breaking ×2 progression.
  Evidence: DESIGN.md frontmatter L80-85
  Fix: Insert `md: 16px` between `12px` and `24px` to restore the geometric ×2 ladder.
  Slash: (no auto-fix; user decides whether to add the step)
```

---

## Output file format

The auditor writes `<DESIGN.md>.critique.md` adjacent to the input file. Structure:

```markdown
# DESIGN.md Audit — <YYYY-MM-DD HH:MM:SS ±HHMM>

**File audited:** `./DESIGN.md`
**Variant detected:** 1 (canonical) | 2 (community 9-section)
**Project root:** `<absolute path>` (only if drift / completeness passes ran)
**Total findings:** <n>
**Verdict:** PASS | REVISE
**Score:** <0-100>

## Summary

<2-3 sentence prose summary>

## Findings

### Pass 1 — Structural (<n> findings)

<list of F<n> entries per format above>

### Pass 2 — Drift (<n> findings)

<list>

### Pass 3 — Accessibility (<n> findings)

<list>

### Pass 4 — Completeness (<n> findings)

<list>

### Pass 5 — Consistency (<n> findings)

<list>

## Blocking findings (P0 — must fix before delivery)

<list of P0 findings only>

## Recommended next steps

<numbered actionable list>
```

The auditor also appends a one-line summary to `progress.md` (if present at project root).

---

## What the auditor does NOT do

- **Never edits DESIGN.md.** Read-only on the input file.
- **Never edits source code.** Read-only on the project tree.
- **Never recommends new tokens that aren't clearly required by the codebase.**
- **Never marks PASS with any P0 finding outstanding.**
- **Never invents WCAG numbers** — every contrast ratio comes from `bin/amw-design-md-contrast.py`.

## Pre-flight checks

Before starting Pass 1:

1. Verify `DESIGN.md` exists at the path passed in. If absent, return immediately with `status=failed`, `blocking_issues=["DESIGN.md not found at <path>"]`.
2. Detect variant by inspecting line 1 (V1: `---`; V2: `# Design System Inspired by ...`).
3. For Pass 2 / Pass 4, verify `<project_root>` is provided and contains source files. If not, those passes are skipped with `status=partial`.

## Cross-references

- [review-rubric](./review-rubric.md) — single-file pass/fail checklist
- [canonical-spec-google-alpha](./canonical-spec-google-alpha.md) — Variant 1 spec
- [community-9-section-spec](./community-9-section-spec.md) — Variant 2 spec
- `<plugin-root>/bin/amw-design-md-lint.sh` — official linter
- `<plugin-root>/bin/amw-design-md-validate.py` — pure-Python validator
- `<plugin-root>/bin/amw-design-md-contrast.py` — contrast checker
- `<plugin-root>/bin/amw-design-md-from-codebase.py` — codebase scanner (used in Pass 2)
- `../../../agents/amw-design-md-auditor-agent.md` — the agent that runs the 5 passes
