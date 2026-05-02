---
name: TECH-06-do-donts
category: authoring
source: design.md-main/docs/spec.md L321-L332; design-md-builder/references/9-section-template.md L227-L243
also-in: review-rubric.md, ../ai-slop-avoid.md
status: stable
---

# TECH: Authoring the Do's and Don'ts section

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
- `../ai-slop-avoid.md` — anti-patterns S13, S14
- [canonical-template](./canonical-template.md) — Variant 1 placeholder
- [community-9-section-template](./community-9-section-template.md) — Variant 2 placeholder
