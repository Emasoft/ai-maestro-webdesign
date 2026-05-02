---
name: TECH-guided-creative-mode
category: infographic-builder
source: image-generation/create-infographics/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [The flow](#the-flow)
- [The two-option presentation](#the-two-option-presentation)
- [Example presentation](#example-presentation)
- [User selection handling](#user-selection-handling)
- [Step 5 — one-shot build](#step-5-one-shot-build)
- [Step 6 — Live Editor Block](#step-6-live-editor-block)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# Guided Creative (Mode C) — show two directions before building

## What it does

A premium UX path — before writing any code, show two distinct
composition options. User picks one; Claude builds that one in a
single pass.

## When to use

- "Help me figure out the design" / "I'm not sure what style"
- "Give me options" / "Show me two approaches" / "Show me two directions"
- "What would look best?" / "What do you recommend?"
- User brief is rich in content but visual direction is unclear

## The flow

```
Step 1 — Design Brief
Step 2 — Classify + Layout Intent
Step 3 — Present TWO composition options (no code yet)
Step 4 — User selects
Step 5 — One-shot build (Mode B Steps 2-4)
Step 6 — Export + Live Editor Block
```

## The two-option presentation

Each option gets:
- A short name (2-3 words)
- The composition archetype it uses
- A one-sentence description of the structure + dominant component
- Why it fits this data

**Rules:**
- Two options only — decision fatigue kills momentum
- Options must be genuinely different (different archetypes)
- Each option must have a clear rationale tied to THE data
- Don't start building until the user selects

## Example presentation

```markdown
Here are two directions for this infographic:

**Option A — 'DENSE REFERENCE'** (Stacked Reference)
Top-to-bottom stacked sections, each structurally different —
allocation table, vesting timeline, bullet panel, dense data table.
Every section earns its space with different content format. This
works because the data has 4+ distinct topics that each need their
own visual treatment.

**Option B — 'ECONOMY FLOW'** (Flow Poster)
Central flow diagram showing how tokens move through the system,
with supporting tables above and below. Arrows dominate — fees,
rewards, and burns are shown as directional flows. This works
because the core story is a circular token economy, and the flow IS
the infographic.

Which direction do you want? (Or describe a different approach and
I'll build it.)
```

## User selection handling

| User says | Action |
|-----------|--------|
| "Option A" / "A" / "first one" | Build Option A |
| "Option B" / "B" / "second one" | Build Option B |
| "Neither" / "try X instead" | Propose third option or ask clarifying question |
| No preference / "you pick" | Choose the stronger rationale for THIS data, name the choice, build |

## Step 5 — one-shot build

Use the chosen direction's archetype throughout. Apply it literally
— don't drift toward the other option's patterns. Follow Mode B
Steps 2-4 (classify + layout intent, build, quality check).

## Step 6 — Live Editor Block

After delivery, offer:

```json
{
  "theme": { "primary_color": "current hex", "background_mode": "dark | light" },
  "content": { "title": "current text", "subtitle": "current text" }
}
```

Apply changes when the user pastes updates.

## Gotchas

- Don't show 3+ options — decision fatigue.
- Don't pick two variations of the same archetype — they must feel
  genuinely different.
- Don't write HTML until the user picks — that's the whole point
  of this mode.

## Cross-references

- [TECH-one-shot-mode](TECH-one-shot-mode.md) — the build step after selection.
- [TECH-interactive-builder-mode](TECH-interactive-builder-mode.md) — the component-by-component
  alternative.
- [TECH-stacked-reference-archetype](TECH-stacked-reference-archetype.md) — the default archetype.
- [TECH-flow-poster-archetype](TECH-flow-poster-archetype.md) — for flow-dominant picks.
- [TECH-cheat-sheet-archetype](TECH-cheat-sheet-archetype.md) — for the densest mode.
- [`../SKILL.md`](../SKILL.md) — parent skill

