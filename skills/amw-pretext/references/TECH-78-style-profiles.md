---
name: TECH-78-style-profiles
category: consult
source: pretext-skills/amw-pretext-frontend-motion-main/core/bundle/references/style-profiles.md
also-in: 
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Style profiles (pick ONE aesthetic per pretext output)

**Category:** consult
**Status:** stable

## What it does

When generating pretext-powered output, pick ONE named style profile from `pretext-frontend-motion-main/references/style-profiles.md`:
- `editorial-paper` — literary / curatorial / paper texture / calmer motion
- `technical-lab-white` — sparse / algorithmic / micro-labels / violet/blue/graphite
- `kinetic-dark-poster` — cinematic / high-contrast / glowing type / motion-forward
- `compact-measured-ui` — tight modules / utility-first / bubbles / messaging surfaces

Avoid defaulting to the "centered SaaS hero with Inter on white" — the explicit anti-pattern.

## When to use

- Any pretext demo or output that needs a visual identity
- To prevent the "everything looks the same" problem

## How it works

Map the brief to a profile:
- "literary / exhibition / essay" → `editorial-paper`
- "algorithm / signal / computational typography" → `technical-lab-white`
- "poster / luminous / cinematic" → `kinetic-dark-poster`
- "card wall / accordion / messaging" → `compact-measured-ui`

```
Source: pretext-frontend-motion-main/references/style-profiles.md
Anti-pattern: centered SaaS hero + generic gradient blob + Inter on white
```

## Minimal example

Not a code snippet — a design-direction decision.

## Gotchas

- Mixing two profiles collapses into one dominant. Commit to one per output.
- The anti-pattern list is specific — flag "Inter on white with no stronger POV" in review.

## Cross-references

- Related: TECH-72-use-pretext-decision-guide, TECH-77-font-strategy
- API reference: N/A — consulting guide
- Plugin skill: [skills/amw-pretext/SKILL.md](../SKILL.md)
