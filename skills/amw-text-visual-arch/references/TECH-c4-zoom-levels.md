---
name: TECH-c4-zoom-levels
category: text-visual-arch
source: cc-plugin-text-visualizations-main/skills/tools-visual-ascii-arch/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-c4-zoom-levels — context / container / component framing

## What it does

Picks one C4-style zoom level per diagram: context (users ↔ system),
container (services + DBs + queues inside the system), or component
(modules / classes / contracts inside a container). Mixing zoom levels in
a single diagram is the single most common cause of "this architecture
diagram is confusing".

## When to use

Before drawing any architecture diagram. Decide which level the audience
needs. A VP asking "what is this system?" needs context. A new engineer
asking "which services do I deploy to?" needs container. A module
refactor PR needs component.

## How it works

- **Context**: outer boundary = the system. Everything outside is users or
  external systems. Typical content: 1-3 user types + the system + 2-5
  external dependencies.
- **Container**: inside "the system", break out services, data stores,
  message queues. Typical content: 3-8 containers, no internal module
  detail.
- **Component**: inside one container, show modules / classes /
  contracts. Typical content: 4-10 components with their interactions.

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-ascii-arch/SKILL.md lines 18-22
Context:
+-------+      +--------+
| User  |----->| System |
+-------+      +---+----+
                   |
                   v
               +--------+
               | Stripe |
               +--------+

Container (inside "System"):
+---------+  +---------+  +---------+
| Web API |  | Worker  |  |  DB     |
+---------+  +---------+  +---------+
```

## Gotchas

- Audiences conflate zoom levels; always STATE which level the diagram
  is at in a one-line caption ("Container diagram of the Payments
  service").
- A user asking "draw the architecture" without specifying depth usually
  wants container-level; ask if ambiguous.
- Stacking two zoom levels in one diagram (context + container boxes in
  the same frame) always confuses — split into two diagrams.

## Cross-references

- [TECH-protocol-label-arrows](./TECH-protocol-label-arrows.md)
- `../../amw-diagram-architecture/SKILL.md`
- [TECH-footnote-tags-deployment](./TECH-footnote-tags-deployment.md)
- [`../SKILL.md`](../SKILL.md) — parent skill

