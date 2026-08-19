---
name: skill-trigger-collision-ratchet
description: "why is HIGH_BASELINE 1 in test_skill_trigger_collisions / trigger collision test failing / new HIGH skill-trigger collision / two skills claim the same trigger phrase / can I add a diagram type list to a SKILL description / detector says diagram modify diagram collides"
ocd: 2026-08-19
lmd: 2026-08-19
metadata:
  node_type: memory
  type: project
  tier: component
publish-globally: false
---

# skill-trigger-collision-ratchet


^ATOM-7ALV-C1TP [desc: "TRDD-0TBHW83S paid the 37 frozen HIGHs down to 1 justified residual (2026-08-19)", keywords: trigger_collision HIGH_BASELINE ratchet skill_description_overlap diagram_type_list detector_noise test_skill_trigger_collisions_failing, type: project, ocd: 2026-08-19, lmd: 2026-08-19]

TRDD-0TBHW83S (2026-08-19, commit 68fe6a2) adjudicated all 37 frozen HIGH trigger collisions: 17 REAL — amw-html-diagram duplicated amw-diagram-editorial's diagram-type enumeration; the type list is OWNED by amw-diagram-editorial, amw-html-diagram stays format-keyed only. 19 NOISE removed by principled detector corrections in bin/amw-skill-trigger-collision.py: disclaimer/scope sentences ("does not claim…", "use when…", "not when…", "routes to…") stripped before n-gram extraction; agent-vs-agent overlaps demoted to low (sub-agents are name-dispatched, never description-routed); amw-design-md router-vs-child overlap whitelisted via ROUTERS; the delegation heuristic now matches the skill DIRECTORY, not only SKILL.md. Residual HIGH_BASELINE=1: "diagram modify diagram" is a stopword-filter artifact — html/svg, the disambiguating tokens, are stopwords. Full verdicts: reports/trigger-collision-adjudication/. Never re-enumerate diagram types in a second skill description; never raise the baseline without its own TRDD.

## Notes and lessons learned
