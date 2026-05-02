---
name: TECH-classic-state-machine-arrows
category: ascii-classic
source: ascii-diagrams-skill-main/references/state-machines.md
also-in: ascii-diagrams-skill-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-classic-state-machine-arrows — TCP-style state diagram

## What it does

Renders a state machine as ALL-CAPS state names in boxes, connected by
labeled arrows showing the transition trigger on or near the line. Mirrors
the canonical TCP connection state diagram (`CLOSED → OPENING → CONNECTED
→ CLOSED`).

## When to use

- Protocol state documentation (TCP, OAuth, WebSocket handshakes)
- Lifecycle visualizations (lambda container warm/cold, K8s pod state)
- API resource state diagrams (order pending / paid / shipped / delivered)

## How it works

- Each state is a box with its name in CAPS (or mixed case if the audience
  prefers).
- Each arrow is labeled with the transition trigger — the event, timer,
  message, or guard that fires it.
- Initial state has either an unbound incoming arrow or an explicit
  marker (`(start)` / `(*)`).
- Terminal states can use a double border (`+=====+` style) or a
  `((NAME))` marker.

## Minimal example

```
// Source: ascii-diagrams-skill-main/references/state-machines.md lines 6-24
                     +--------+
              +----->| CLOSED |<-----+
              |      +---+----+      |
              |          |           |
              |     open |           | timeout
              |          v           |
              |      +---+----+     |
              |      | OPENING|-----+
              |      +---+----+
              |          |
              |    ready |
              |          v
         close|      +---+-------+
              |      | CONNECTED |
              |      +---+-------+
              |          |
              +----------+
```

## Gotchas

- Every transition needs a label. An unlabeled arrow between two states
  tells the reader nothing about when it fires.
- Keep state names short (≤ 12 chars) so the box widths don't explode the
  horizontal footprint of the whole diagram.
- Bidirectional transitions render as two arrows in opposite directions,
  not as one double-headed arrow.

## Cross-references

- [state-machines](./state-machines.md) (legacy pattern file)
- `../../amw-text-visual-state/references/TECH-state-guards-and-actions.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

