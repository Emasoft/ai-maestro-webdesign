---
name: TECH-uxeval-3-dimension-framework
category: uxeval-dim
source: SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Verdict rubric per dimension](#verdict-rubric-per-dimension)
  - [Evaluation workflow](#evaluation-workflow)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: 3-dimension evaluation framework (Position, Visual Weight, Spacing)

## What it does

The core evaluation framework. For ANY UI component, three dimensions are analyzed — **Position**, **Visual Weight**, **Spacing**. Each gets a verdict: Pass / Warn / Fail. The framework prevents subjective "I don't like it" critiques by grounding every verdict in an observable measurement and a cited convention.

## When to use

On every UX evaluation the skill runs. The framework is mandatory — partial evaluations (only Position, only Spacing) are a failure mode of the skill.

## How it works

Three dimensions, five analysis axes each:

| Dimension | What to analyze | Key questions |
|---|---|---|
| **1. Position** | Location relative to other elements, reading flow, adjacency | Does position follow conventions (primary right, utility far right)? Discoverable? |
| **2. Visual Weight** | Fill vs ghost vs icon-only, color, shadow, size, font weight | Does it compete with the primary action? Is hierarchy legible at a glance? |
| **3. Spacing** | Gaps from adjacent elements, touch target, rhythm | Adequate separation (≥ 8 px intra-group, ≥ 24 px between groups)? Touch targets ≥ 44 × 44 px on mobile? |

### Verdict rubric per dimension

- **Pass** — matches convention, no changes needed
- **Warn** — acceptable but suboptimal; improvement attached
- **Fail** — breaks convention or accessibility floor; recommendation is mandatory

### Evaluation workflow

```
Step 1: GATHER CONTEXT
  ├── What component? (hero, navbar, CTA stack, form, pricing card)
  ├── Why evaluating? (user concern, pre-ship check, cited standard)
  ├── External reference? (article, guideline, competitor pattern)
  └── Component role (primary CTA, secondary action, utility control, nav, form field)

Step 2: ANALYZE CURRENT STATE
  ├── Position — exact location in layout (selector + coordinates)
  ├── Visual Weight — styling description (computed-style evidence)
  ├── Spacing — measured gaps (selector pairs + px distances)
  └── Compare to industry conventions (see references/)

Step 3: PRODUCE VERDICT
  ├── For each dimension: Pass / Warn / Fail
  ├── If Fail or Warn: specific recommendation with rationale
  ├── Reference authoritative source
  └── Prioritize: P1 (breaks UX), P2 (suboptimal), P3 (polish)
```

## Minimal example

Navbar CTA evaluation:

```markdown
### Current State
- **Position:** [.nav .cta] right-aligned, 24 px from theme-toggle
- **Visual Weight:** filled primary color, 14 px padding, subtle shadow
- **Spacing:** 12 px intra-nav-group, 24 px from theme-toggle group

### Analysis

| Dimension      | Verdict | Evidence                       | Rationale                                         |
|---------------|--------|--------------------------------|---------------------------------------------------|
| Position      | Pass   | right-aligned (Stripe/GitHub)  | Primary-right convention                          |
| Visual Weight | Pass   | filled brand color + shadow    | Distinctly dominant vs ghost secondary            |
| Spacing       | Warn   | 24 px to theme-toggle          | Could be 32 px for clearer group separation       |
```

*Attributed to the ux-evaluator skill — `SKILLS-TO-INTEGRATE/web-design/ux-evaluator/SKILL.md`.*

## Gotchas

- "Looks wrong" is not a verdict. Every Fail/Warn cites concrete evidence (selector, computed-style value, measured pixel distance).
- All three dimensions ALWAYS. Scoring only the dimension that looked problematic means missing compound issues.
- Conventions are cited from authoritative sources — Balsamiq, Nielsen, Material, Apple HIG, or observable industry patterns (GitHub, Stripe, Notion). "I prefer" is not a citation.
- Re-score after fixes — applying the recommended change can cascade into a different dimension.

## Cross-references

- [TECH-uxeval-priority-rubric](TECH-uxeval-priority-rubric.md) — P1 / P2 / P3 prioritization
  > What it does · When to use · How it works · Assignment rule · Output structure · Minimal example · Gotchas · Cross-references
- [TECH-uxeval-button-conventions](TECH-uxeval-button-conventions.md), [TECH-uxeval-navigation-conventions](TECH-uxeval-navigation-conventions.md), [TECH-uxeval-form-conventions](TECH-uxeval-form-conventions.md)
  > [TECH-uxeval-navigation-conventions.md] What it does · When to use · How it works · Position (top bar, LTR) · Theme toggle placement (industry cross-check) · Visual weight · Utility control visual weight · Spacing · Mobile patterns · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Position · Visual weight · Spacing · Labels · Minimal example · Gotchas · Cross-references
- [balsamiq-button-principles](balsamiq-button-principles.md) — full reference
  > Core Principles · Use Conventional Labels · Say Exactly What Happens · Primary and Secondary Should Look Different · Primary Action on the Right · Use Adequate Spacing · Make Buttons Look Clickable · Size Appropriately · Use Icons Wisely · Consider Loading States · Error Prevention · Button Hierarchy Summary · Common Mistakes
- [SKILL](../SKILL.md)
