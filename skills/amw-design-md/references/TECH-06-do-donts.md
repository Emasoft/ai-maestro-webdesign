---
name: TECH-06-do-donts
category: authoring
source: design.md-main/docs/spec.md L321-L332; design-md-builder/references/9-section-template.md L227-L243
also-in: review-rubric.md, ../ai-slop-avoid.md
status: stable
---

# TECH: Authoring the Do's and Don'ts section

## Table of Contents

- [What it does](#what-it-does)
- [Why this section matters](#why-this-section-matters)
- [Hard rules](#hard-rules)
  - [Variant 1 — Section 8 "Do's and Don'ts"](#variant-1-section-8-dos-and-donts)
  - [Variant 2 — Section 7 "Do's and Don'ts"](#variant-2-section-7-dos-and-donts)
  - [Minimum count](#minimum-count)
  - [Each rule must be specific and actionable](#each-rule-must-be-specific-and-actionable)
  - [Cover the high-leverage failure modes](#cover-the-high-leverage-failure-modes)
- [Recipe for a good Do](#recipe-for-a-good-do)
- [Recipe for a good Don't](#recipe-for-a-good-dont)
- [Brand-specific anti-patterns](#brand-specific-anti-patterns)
- [Worked examples](#worked-examples)
  - [Example A — Editorial minimalist (Variant 1 alternating style)](#example-a-editorial-minimalist-variant-1-alternating-style)
  - [Example B — Developer SaaS (Variant 2 grouped style)](#example-b-developer-saas-variant-2-grouped-style)
- [Common authoring mistakes](#common-authoring-mistakes)
- [Cross-references](#cross-references)


## What it does

Documents how to write the final section of a DESIGN.md (Variant 1: Section 8 "Do's and Don'ts"; Variant 2: Section 7 "Do's and Don'ts"). Covers content guidelines, minimum count, what makes a rule actionable vs vague, and worked examples.

## Why this section matters

The Do's and Don'ts section is a guardrail — concrete rules an AI agent applies as constraints when generating UI. Done well, it eliminates the most common cross-design failure modes (low contrast, mixed corner styles, multi-weight chaos). Done badly, it's marketing flavor text the agent ignores.

This is the only section the design-md-builder rubric checks for **minimum item count** (`T6`: minimum 3 dos and 3 don'ts).

## Hard rules

### Variant 1 — Section 8 "Do's and Don'ts"

Per spec.md L325-L331, written as a single bullet list. Format:

```markdown
## Do's and Don'ts

- Do <concrete action>
- Don't <concrete anti-pattern>
- Do <concrete action>
- Don't <concrete anti-pattern>
- Do <concrete action>
- Do maintain WCAG AA contrast ratios (4.5:1 for normal text)
- Don't use more than two font weights on a single screen
```

The official spec example mixes Do/Don't in one list. Both alternating and grouped (`### Do` then `### Don't`) are accepted; alternating reads better for diverse rules.

### Variant 2 — Section 7 "Do's and Don'ts"

Two `###` subsections:

```markdown
## 7. Do's and Don'ts

### Do
- Do <action>
- Do <action>
- Do <action>

### Don't
- Don't <anti-pattern>
- Don't <anti-pattern>
- Don't <anti-pattern>
```

The grouped style is the convention in V2 corpus; minimum 3 of each (rubric `T6`).

### Minimum count

3 Dos + 3 Don'ts is the floor. Below that, the file fails the rubric. Aim for 5-8 of each.

### Each rule must be specific and actionable

| ✗ Vague | ✓ Specific |
|---|---|
| "Don't be inconsistent." | "Don't mix rounded and sharp corners in the same view." |
| "Do use good judgment." | "Do use the primary color only for the single most important action per screen." |
| "Maintain accessibility." | "Do maintain WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text)." |
| "Don't use too many fonts." | "Don't use more than two font weights on a single screen." |
| "Use appropriate spacing." | "Do respect the 8px grid for every spatial value." |

The test: would a competent designer agree this rule has a clear yes/no application? If "it depends on context," rewrite.

### Cover the high-leverage failure modes

Every DESIGN.md should explicitly address:

1. **Color discipline** — when to use primary, when not to.
2. **Contrast** — minimum WCAG AA target stated.
3. **Spacing grid** — base unit acknowledged.
4. **Font discipline** — weight count, family count.
5. **Token discipline** — never hard-code raw values.
6. **Corner / shape consistency** — radius rules.
7. **One brand-specific rule** — what makes THIS system distinctive.

A list of 7 rules that cover all 7 areas is more valuable than 14 rules that all repeat color discipline.

## Recipe for a good Do

A good "Do" rule answers: *under what condition, do what specific thing?*

```
Do <action> [when <condition>] [for/to <effect>].
```

Examples:
- "Do use the primary color only for the single most important action per screen."
  (action: use; condition: most important action per screen; constraint: only)
- "Do maintain 4.5:1 contrast for body text on any surface."
  (action: maintain; condition: body text + any surface; metric: 4.5:1)
- "Do reference tokens by name in component code; never inline hex."
  (action: reference by name; constraint: never inline)

## Recipe for a good Don't

A good "Don't" rule answers: *what concrete pattern is forbidden, and why is it commonly attempted?*

```
Don't <pattern> [in/on <context>] [— <consequence or reason>].
```

Examples:
- "Don't mix rounded and sharp corners in the same view."
- "Don't introduce new colors outside this palette without updating this file first."
- "Don't use drop shadows on body text or inline buttons."
- "Don't pair Tertiary as the dominant color of any view — it is an accent only."

## Brand-specific anti-patterns

The most valuable Don'ts are brand-specific. They eliminate the AI's tendency to apply generic patterns that contradict the brand:

- For an editorial / minimalist brand: "Don't use gradients on CTAs." / "Don't use illustrative icons; outline-only at 1.5px stroke."
- For a developer-tool brand: "Don't use serif fonts; sans + mono only." / "Don't use organic shapes; geometric only."
- For a luxury brand: "Don't use crowded layouts; whitespace ratio ≥ 50%." / "Don't use sale/discount visual hierarchy."
- For a healthcare brand: "Don't use red on positive outcomes (cultural; reserve red for warnings)." / "Don't show clinical metrics without an interpretation prompt nearby."

These are gold. They tell the agent things it could not infer from tokens alone.

## Worked examples

### Example A — Editorial minimalist (Variant 1 alternating style)

```markdown
## Do's and Don'ts

- Do use the primary color only for the single most important action per screen.
- Don't mix rounded and sharp corners in the same view.
- Do maintain WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text).
- Don't use more than two font weights on a single screen.
- Do reference tokens by name in component code — `var(--primary)` or `bg-primary`, never inline hex.
- Don't introduce new colors outside this palette without updating this file first.
- Do respect the 8px grid for every spatial value.
- Don't use gradients on any CTA or interactive element.
- Don't pair Tertiary as the dominant color of any view — it is an accent only.
```

### Example B — Developer SaaS (Variant 2 grouped style)

```markdown
## 7. Do's and Don'ts

### Do
- Do use sans-serif (Inter) for all UI text and mono (JetBrains Mono) for code.
- Do maintain 4.5:1 contrast for body text. Use the contrast checker before shipping.
- Do show keyboard shortcuts in tooltips for any interactive element a power-user would use repeatedly.
- Do prefer dense data tables (32px row height) over sparse cards for lists of >10 items.
- Do use `--surface-elevated` for hovered/focused rows; never `--primary`.

### Don't
- Don't use serif fonts anywhere — they signal "marketing site" not "tool".
- Don't use illustrative or 3D iconography. Outline-only icons at 1.5px stroke, 16px or 20px size.
- Don't apply drop shadows to body content; reserve elevation for modals and popovers only.
- Don't use the danger color for non-destructive negative states (e.g., low credits is a warning, not a danger).
- Don't introduce gradients. The brand is geometric, not painterly.
```

## Common authoring mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Single rule covers many cases | Rule is vague: "Be consistent." | Split into 3-5 specific rules |
| Rules contradict each other | "Do use primary often" + "Don't overuse primary" | Pick one; specify the threshold |
| All rules are universal best-practices | "Maintain accessibility", "Use a grid" | Add brand-specific Don'ts |
| Less than 3 of each | Rubric `T6` failure | Author until threshold met |
| Rules reference undefined tokens | "Use color X" where X isn't declared | Either declare or remove the rule |

## Cross-references

- [review-rubric](./review-rubric.md) — rubric `T6` (minimum 3 of each)
  > Output schema · Structural checks (must-pass) · Variant 1 (canonical) · Variant 2 (community) · Token-quality checks (must-pass — both variants) · Sync checks (must-pass — when companion files exist) · Content-integrity checks (soft — affects score) · A11y checks (must-pass — both variants) · Scoring · What the rubric does NOT do · How `amw-design-md-author-agent` uses the rubric on its own output · Cross-references
- [ai-slop-avoid](../ai-slop-avoid.md) — anti-patterns S13, S14
  > Token authoring slop · S1. Vibes without hex values · S2. Token name and prose name out of sync · S3. Unresolved token references · S4. Placeholder text never filled in · S5. Color names like "blue" or "red" instead of semantic roles · S6. Typography without a complete row · S7. fontWeight as a string when not a number · Structural slop · S8. Sections out of canonical order · S9. Duplicate section headings · S10. Missing the `## Colors` section · S11. YAML frontmatter not at line 1 · S12. YAML frontmatter that is not actually YAML · Prose slop · S13. Marketing copy where rules belong · S14. Do's and Don'ts that are vague · S15. The `## Overview` section is a wall of adjectives · Variant 2 — community 9-section specific · S16. Section 7 (Do's and Don'ts) with fewer than 3 dos and 3 don'ts · S17. Section 8 (Responsive Behavior) without explicit px breakpoints · S18. Section 9 (Agent Prompt Guide) missing a quick-color-reference · S19. Mermaid component-state diagram absent · Conversion slop · S20. Variant 2 → Variant 1 conversion that loses data · Companion-file slop · S21. tokens.css with hex values that don't match DESIGN.md frontmatter · S22. tokens.json that is not W3C Design Tokens format · Final delivery gate
- [canonical-template](./canonical-template.md) — Variant 1 placeholder
  > Filling guide · Cross-references
- [community-9-section-template](./community-9-section-template.md) — Variant 2 placeholder
  > Optional extension sections · Validation · Cross-references
