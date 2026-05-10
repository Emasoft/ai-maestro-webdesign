---
name: TECH-ux-process-discover
category: ux-process
source: SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: UX process — Discover & Research (Phase 1)

## What it does

The first of five UX-process phases. Phase 1 is CRITICAL-priority: it produces the evidence base every downstream phase depends on. Outputs are user interviews, analytics analysis, competitive audits, empathy maps, and identified pain points.

## When to use

At the start of any non-trivial UX project. Skip only when (a) the feature is a small tweak to an already-researched surface, or (b) the organization has existing research the designer can read instead of running fresh interviews.

## How it works

Four activities, run roughly in parallel:

- **User interviews** — 5-8 participants per round, 45-60 min each, recorded and transcribed. Discussion guide of 8-12 open-ended questions centered on past behavior, not future speculation.
- **Analytics + heatmap analysis** — read GA4 / Mixpanel funnels, Hotjar / FullStory session recordings, conversion drop-offs. Identify what users DO vs what they SAY.
- **Competitive analysis** — audit 3-5 competitor experiences with the same task. Note patterns, anti-patterns, feature gaps.
- **Empathy maps + pain-point extraction** — synthesize interview + analytics findings into one-page empathy map per persona archetype, with themes extracted via affinity mapping.

## Minimal example

Research plan for a SaaS onboarding flow:

1. Recruit 8 participants: 4 who just signed up, 4 who churned in week 1
2. Discussion guide (10 questions): "Walk me through the last time you set up a new tool at work", "What was the hardest part?", "What did you try before finding us?"
3. Pull GA4 funnel: sign-up → workspace-setup → first-action. Note the drop-off step.
4. Audit competitor onboardings: Notion, Linear, Vercel — what do they do differently?
5. Synthesize: 3 pain points ranked by frequency + impact. Top one drives the redesign brief.

*Attributed to the ux-designer skill — `SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md`.*

## Gotchas

- "Don't you think X would be useful?" is a leading question — the participant will almost always say yes. Replace with "Tell me about a time you needed X" (behavior, not hypothesis).
- 5-8 participants is the sweet spot for qualitative — less than 5 misses patterns, more than 8 overweights early-recruit bias.
- Debriefing within 24 hours prevents detail decay. Waiting a week loses 40% of the nuance.
- "Heatmaps are gospel" is wrong — they show clicks, not intent. Pair with session recordings and interview quotes before drawing conclusions.

## Cross-references

- [TECH-ux-rule-research](TECH-ux-rule-research.md) — detailed rule for interview planning, synthesis, and persona creation
  > What it does · When to use · How it works · Interview planning · During interviews · Synthesis · Good vs bad questions · Minimal example · Gotchas · Cross-references
- [TECH-ux-process-define](TECH-ux-process-define.md) — next phase (Define)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
