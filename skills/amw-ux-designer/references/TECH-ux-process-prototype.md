---
name: TECH-ux-process-prototype
category: ux-process
source: SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md
also-in:
---

# TECH: UX process — Prototype & Test (Phase 4)

## What it does

The fourth of five phases. HIGH priority. Phase 4 builds interactive prototypes for the selected wireframes and runs usability tests to validate them before engineering investment. Outputs are quantitative task-success metrics plus qualitative observations.

## When to use

After Phase 3 (Ideate) produces a selected wireframe per problem. Run before engineering starts — every bug caught in a usability test is 10x cheaper than a bug caught in production.

## How it works

Three activities:

- **Build interactive prototype** — Figma interactive mode, Framer, or coded HTML prototype. Focuses on the 1-3 flows that carry the most risk. Fidelity matches the fidelity of the wireframes.
- **Usability testing** — moderated (researcher + participant, 45-60 min) or unmoderated (Maze, UserTesting). 5-8 participants per flow. Script: realistic task, think-aloud protocol, completion observation.
- **Measure + iterate** — four metrics: task success rate, time on task, error rate, satisfaction (SUS or Single Ease Question). Iterate until task success ≥ 80% or the test reveals the wireframe is fundamentally wrong.

## Minimal example

Prototype for Sarah's "basics rail":

- Figma interactive prototype: home screen → basics rail (6 items) → tap "reorder all" → checkout
- Moderated test, 6 participants matching Sarah persona
- Task: "You realize on your commute you're out of milk and diapers — reorder them"
- Metrics: 5/6 completed in <90 sec. One participant didn't notice the "reorder all" button — relocated from bottom-right to top-right in the next iteration.

*Attributed to the ux-designer skill — `SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md`.*

## Gotchas

- Think-aloud protocol is essential. A participant who completes silently tells you nothing about their decision-making.
- Unmoderated tests scale but miss nuance. Use them for quick signal (large-N comprehension check), not for deep behavior understanding.
- Task success rate alone is misleading — a user who completes the task in 4 minutes via a confusing detour counts as a success, but the experience is broken.
- Leading questions during moderation poison the data. "Was that easy?" → replace with "What did you try to do there?"

## Cross-references

- `TECH-ux-process-ideate.md` — upstream (Phase 3)
- `TECH-ux-process-handoff.md` — downstream (Phase 5)
- `../SKILL.md`
