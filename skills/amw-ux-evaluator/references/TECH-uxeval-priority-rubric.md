---
name: TECH-uxeval-priority-rubric
category: uxeval-prio
source: SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Assignment rule](#assignment-rule)
  - [Output structure](#output-structure)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Priority rubric (P1 / P2 / P3)

## What it does

Every recommendation the evaluator emits carries a P1 / P2 / P3 priority label. The rubric prevents "everything is critical" degradation and gives the recipient a triage order they can act on without reading the full rationale.

## When to use

On every Fail or Warn. The rubric is mandatory; recommendations without priority are rejected by the skill's non-negotiables.

## How it works

Three tiers:

- **P1 — breaks UX.** Ship-blocking. Wrong button order (primary left of secondary on a site where convention is the opposite), inaccessible touch target (< 44 × 44 px on mobile), primary buried (not in the first screenful on a landing page), contrast below AA (< 4.5:1 normal text).
- **P2 — suboptimal but usable.** Should fix before shipping but doesn't block launch. Tight spacing (12 px where 24 px would separate groups), non-standard utility placement (theme toggle mid-nav instead of far right), weak label ("Submit" instead of "Save Changes").
- **P3 — polish only.** Token drift, micro-alignment, aesthetic. Usually batched into a post-launch polish pass.

### Assignment rule

P1 is reserved for issues that would cause users to fail a task, users with disabilities to be blocked, or the product to ship an a11y regression. P2 is for issues that reduce clarity or efficiency. P3 is everything else.

### Output structure

```markdown
### Recommendations

| Priority | Change                                      | Evidence                       | Cited principle                          |
|----------|---------------------------------------------|--------------------------------|------------------------------------------|
| P1       | Move primary CTA to right of secondary      | `.cta-stack` selector          | Balsamiq #4 — primary on right           |
| P2       | Increase spacing from theme-toggle to 32 px | computed margin 24 px          | Nielsen #4 — consistency + proximity     |
| P3       | Adjust button height from 42 to 44 px       | computed height 42 px          | WCAG 2.2 target size (minimum)           |
```

## Minimal example

Pricing-page CTA evaluation:

```markdown
### Recommendations

| Priority | Change                                       | Evidence                             | Cited principle                             |
|----------|----------------------------------------------|--------------------------------------|---------------------------------------------|
| P1       | Raise CTA contrast to 4.8:1 from 3.1:1       | #cta color #2B7A9F on #FFFFFF        | WCAG 2.1 AA normal text                      |
| P2       | Rename "Get Started" to "Start Free Trial"   | button text                          | Microcopy — name the consequence            |
| P3       | Align CTA baseline to 8-pt grid              | computed baseline 172 px             | 8-pt grid consistency                        |
```

*Attributed to the ux-evaluator skill — `SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md`.*

## Gotchas

- Downgrading a P1 to a P2 because the user doesn't want to delay the release is common pressure. The evaluator's non-negotiable: P1 stays P1; the user, not the evaluator, decides whether to ship anyway.
- Upgrading a P3 to a P2 to "make the evaluation look thorough" degrades the rubric. P3 is legitimate — not everything needs to be urgent.
- "All P1" means the rubric has failed. If everything is P1, the evaluator's triage is not being done.
- Priority is assigned per recommendation, not per dimension. A dimension with Fail verdict can produce multiple recommendations at different priorities.

## Cross-references

- [TECH-uxeval-3-dimension-framework](TECH-uxeval-3-dimension-framework.md) — where Fail / Warn come from
  > What it does · When to use · How it works · Verdict rubric per dimension · Evaluation workflow · Minimal example · Gotchas · Cross-references
- [TECH-uxeval-output-format](TECH-uxeval-output-format.md) — full report template
  > What it does · When to use · How it works · Fields · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
