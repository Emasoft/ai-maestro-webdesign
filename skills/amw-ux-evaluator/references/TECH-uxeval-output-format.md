---
name: TECH-uxeval-output-format
category: uxeval-dim
source: SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md
also-in:
---

# TECH: Output format — structured evaluation report

## What it does

Every evaluation the skill produces uses a single structured Markdown format. The format enforces: current-state description, 3-dimension analysis table, explicit verdict, prioritized recommendations. It exists to prevent prose-only "looks good / looks bad" outputs, which the skill rejects.

## When to use

On every report the skill emits. The format is mandatory; free-form outputs are a failure mode.

## How it works

The template:

```markdown
## [Component Name] Evaluation

### Current State
- **Position:** [selector + coordinates]
- **Visual Weight:** [selector + computed-style evidence]
- **Spacing:** [measured gaps + selector pairs]

### Analysis

| Dimension      | Verdict          | Evidence                  | Rationale                       |
|---------------|------------------|---------------------------|---------------------------------|
| Position      | Pass/Warn/Fail   | selector + value          | Why + cited convention          |
| Visual Weight | Pass/Warn/Fail   | selector + computed-style | Why + cited convention          |
| Spacing       | Pass/Warn/Fail   | measured gap + selectors  | Why + cited convention          |

### Verdict: PASS / NEEDS CHANGES

### Recommendations
| Priority | Change             | Evidence           | Cited principle                         |
|----------|--------------------|--------------------|-----------------------------------------|
| P1       | [Specific change]  | [selector / value] | [e.g. Balsamiq #4 — primary on right]   |
| P2       | [Specific change]  | [selector / value] | [e.g. Nielsen #4 — consistency]         |
```

### Fields

- **Current State** — describes what is, not what should be. Evidence-first.
- **Analysis table** — three rows (always). One per dimension. Verdict + evidence + rationale.
- **Verdict** — overall. If any dimension is Fail → NEEDS CHANGES. If all Pass → PASS. Warn-only → user decides.
- **Recommendations** — only emitted when there are Fails or Warns. Every row has priority + change + evidence + citation.

## Minimal example

Full evaluation of a pricing-page CTA:

```markdown
## Pricing Page CTA Evaluation

### Current State
- **Position:** `.pricing .cta` centered horizontally, 120 px below feature list
- **Visual Weight:** filled primary color #2B7A9F on #FFFFFF, 14 px padding, no shadow
- **Spacing:** 120 px from feature list above, 80 px to FAQ below

### Analysis

| Dimension      | Verdict | Evidence                                             | Rationale                                                  |
|---------------|--------|------------------------------------------------------|------------------------------------------------------------|
| Position      | Pass   | centered, above-fold on 1280-wide viewport           | Expected pattern for pricing pages; matches Stripe, Linear |
| Visual Weight | Warn   | #2B7A9F on #FFFFFF — contrast 4.2:1                  | Passes AA for large text (3:1) but below 4.5:1 floor      |
| Spacing       | Pass   | 120 px above, 80 px below — 8-pt grid aligned        | Generous isolation, appropriate rhythm                      |

### Verdict: NEEDS CHANGES

### Recommendations
| Priority | Change                                    | Evidence                           | Cited principle                  |
|----------|-------------------------------------------|------------------------------------|----------------------------------|
| P1       | Darken CTA color to #1E5A78 (4.8:1)       | current #2B7A9F computed-color     | WCAG 2.1 AA — normal text 4.5:1 |
| P2       | Add subtle shadow: 0 2px 4px rgba(0,0,0,.1) | current box-shadow: none          | Affordance — buttons look tappable |
```

*Attributed to the ux-evaluator skill — `SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md`.*

## Gotchas

- Prose-only outputs ("the button looks a bit small") are rejected. The table is mandatory.
- Missing columns in the recommendations table (e.g. no citation) is an audit failure. Every recommendation cites a principle.
- "Evidence" must be observable — a selector, a computed-style value, a measured pixel distance. Never "seems too tight".
- Overall Verdict is binary (PASS or NEEDS CHANGES). Three-way ("mostly good") defeats the rubric.

## Cross-references

- `TECH-uxeval-3-dimension-framework.md`
- `TECH-uxeval-priority-rubric.md`
- `../SKILL.md`
