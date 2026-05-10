---
name: TECH-ux-rule-research
category: ux-rule-research
source: SKILLS-TO-INTEGRATE/web-design/ux-designer/rules/research.md
also-in: SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Interview planning](#interview-planning)
  - [During interviews](#during-interviews)
  - [Synthesis](#synthesis)
  - [Good vs bad questions](#good-vs-bad-questions)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: Rule — User Research (interviews + personas + synthesis)

## What it does

The CRITICAL-priority UX rule covering the Research discipline. Codifies how to plan interviews, ask questions that elicit behavior (not speculation), synthesize findings, and build personas grounded in data.

## When to use

During Phase 1 (Discover & Research) and whenever the user asks for "user research", "interview guide", "persona template", "synthesis workshop", or any phrase naming a research deliverable. Also applies to ad-hoc discovery sessions and stakeholder-alignment workshops.

## How it works

Three clusters:

### Interview planning

- Define clear research objectives before scheduling anyone
- Discussion guide of 8-12 open-ended questions
- Recruit 5-8 participants per qualitative round
- 45-60 min per session (interview + 10-15 min buffer)

### During interviews

- Warm-up questions to build rapport
- Ask about **past behavior**, not hypothetical future behavior
- "Tell me about a time when…" framing
- Follow up with "Why?" and "Can you show me?"
- Stay silent after the question — let the participant fill the space

### Synthesis

1. Debrief within 24 hours (detail decay is 40% by day 7)
2. Extract observations as individual data points (one per sticky note)
3. Cluster with affinity mapping → named themes
4. Identify patterns across 3+ participants (one voice is anecdote, three is signal)
5. Prioritize insights by frequency × impact
6. Actionable recommendations tied to specific quotes

### Good vs bad questions

| ✅ Good | ❌ Bad |
|---|---|
| "Walk me through the last time you [did the task]." | "Don't you think this feature would be useful?" (leading) |
| "What was the hardest part of that experience?" | "Would you use a product that does X?" (hypothetical) |
| "What did you try before finding this solution?" | "Do you like this design?" (opinion, not behavior) |

## Minimal example

Research plan for a new fintech signup flow:

- Objective: understand why 45% of signups drop at workspace-creation step
- Recruit: 4 completed, 4 dropped
- Discussion guide: "Tell me about the last time you signed up for a financial tool at work", "What happened at the workspace-creation screen?", "What did you do next?"
- 6 sessions, 50 min each
- Synthesis within 24 h: drop-off root cause was "I didn't know what a workspace was and I didn't want to guess wrong"

*Attributed to the ux-designer rule file — `SKILLS-TO-INTEGRATE/web-design/ux-designer/rules/research.md`.*

## Gotchas

- "Do you like it?" answers opinion, not behavior, and participants always overestimate how much they like new things (novelty bias).
- Interviewing only power users produces designs that work for power users and fail beginners. Segment participants by experience level.
- Brainstorming personas in a design-team workshop without data is fiction. Personas must come from research.
- Sticker-chart affinity mapping ("12 users said X") without a denominator is misleading — 12 / 12 is everyone, 12 / 200 is a minority.

## Cross-references

- [TECH-ux-persona-template](TECH-ux-persona-template.md) — concrete persona output format
  > What it does · When to use · How it works · Minimal example · Good persona · Bad persona · Gotchas · Cross-references
- [TECH-ux-process-discover](TECH-ux-process-discover.md) — Phase 1 in the process
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-ux-rule-accessibility](TECH-ux-rule-accessibility.md), [TECH-ux-rule-ia](TECH-ux-rule-ia.md), [TECH-ux-rule-interaction](TECH-ux-rule-interaction.md), [TECH-ux-rule-visual](TECH-ux-rule-visual.md)
  > [TECH-ux-rule-ia.md] What it does · When to use · How it works · Navigation structure · Navigation patterns · Mobile specifics · Content organization · Information scent · Search as navigation · Minimal example · Gotchas · Cross-references
  > [TECH-ux-rule-interaction.md] What it does · When to use · How it works · Flow best practices · Multi-step flows · Error recovery · Microcopy · Specific rules · Minimal example · Gotchas · Cross-references
  > [TECH-ux-rule-visual.md] What it does · When to use · How it works · Establishing hierarchy · Typography scale · Color usage · Layout · Design-system essentials · Component documentation · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · WCAG AA (minimum floor) — four POUR pillars · Inclusive design patterns (beyond compliance) · Testing checklist · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
