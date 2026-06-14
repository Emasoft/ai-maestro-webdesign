---
name: TECH-node-shape-vocabulary
category: svg-shape
source: SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-node-shape-vocabulary

## What it does

Maps each **node type** to a specific SVG shape primitive, producing
consistent visual grammar across diagrams. The shape is a semantic
encoding — readers learn that a diamond is always a decision, a cylinder
is always a database, a circle is always an actor.

## When to use

- **Every node** in a `diagram-svg` output.
- **Whenever consistency** across a family of diagrams matters.
- **When the diagram is a flowchart** — the shape vocabulary is the
  most important part of flowchart readability.

Do not mix shape vocabularies between diagrams in the same document. If
one flowchart uses diamonds for decisions, every other flowchart in the
document must do the same.

## How it works

Canonical mapping:

| Node type | Shape | SVG element | Notes |
|---|---|---|---|
| Process / Service | rect with rounded corners | `<rect rx="20" ry="20">` | The default node |
| Database | cylinder | `<ellipse>` + `<rect>` stacked | Flat-top, curved-bottom |
| User / Actor | circle | `<circle>` | Large radius for primary actor |
| Decision | diamond | `<polygon>` with 4 points | Rhombus — wider than tall |
| Input / Output (I/O) | parallelogram | `<polygon>` with 4 points | Slanted rect — the classic flowchart I/O shape |
| External system | rect with dashed stroke | `<rect stroke-dasharray="10 5">` | Indicates "outside our system" |

**Example snippets**

**Process / Service (rounded rect):**

```xml
<rect x="400" y="400" width="200" height="80" rx="20" ry="20"
      fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>
```

**Database (cylinder = ellipse + rect):**

```xml
<g id="db">
  <ellipse cx="500" cy="420" rx="80" ry="15"
           fill="#334155" stroke="#0f172a" stroke-width="4"/>
  <rect x="420" y="420" width="160" height="80"
        fill="#334155" stroke="#0f172a" stroke-width="4"/>
  <ellipse cx="500" cy="500" rx="80" ry="15"
           fill="#334155" stroke="#0f172a" stroke-width="4"/>
</g>
```

**User / Actor (circle):**

```xml
<circle cx="500" cy="500" r="60"
        fill="#38bdf8" stroke="#0f172a" stroke-width="4"/>
```

**Decision (diamond):**

```xml
<polygon points="500,400 580,480 500,560 420,480"
         fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>
```

**Input / Output (parallelogram):**

```xml
<polygon points="430,440 610,440 570,520 390,520"
         fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>
```

**External system (dashed rect):**

```xml
<rect x="400" y="400" width="200" height="80" rx="20"
      fill="#f1f5f9" stroke="#0f172a" stroke-width="4"
      stroke-dasharray="10 5"/>
```

## Gotchas

- **Diamond points must be equidistant from the center.** The top/bottom
  points and left/right points should form a regular rhombus; a
  lopsided polygon reads as a drawing error.
- **Cylinder needs both ellipses.** Just a rect + top ellipse leaves the
  bottom flat and the shape reads as a wastebasket instead. Top
  ellipse + bottom ellipse + rect for the body.
- **External-system dashes must be proportional to the shape size.**
  `stroke-dasharray="10 5"` works on a 200px-wide rect; shrink the
  dashes on smaller shapes so the pattern is still readable.
- **Circle for actor, not for process.** Using a circle for "Process"
  conflicts with the UML convention where circles mean
  use-cases/actors. Stick with the rect-with-rounded-corners for
  process steps.
- **Colour is orthogonal to shape.** Fill colour encodes category
  (`#f1f5f9` light, `#334155` mid, `#38bdf8` accent); shape encodes
  node type. Don't conflate.

## Cross-references

- [SKILL](../SKILL.md) — node-type table lives in the Usage section
- [TECH-canvas-1000x1000](TECH-canvas-1000x1000.md) — container for these shapes
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-stroke-width-4-palette](TECH-stroke-width-4-palette.md) — the fixed 4px stroke
  > What it does · When to use · How it works · Usage pattern · Minimal example · Gotchas · Cross-references
- [TECH-arrow-marker-def](TECH-arrow-marker-def.md) — the arrowhead convention
  > What it does · When to use · How it works · Attribute breakdown · Minimal example · Gotchas · Cross-references
- [TECH-type-flowchart](../../amw-diagram-editorial/references/TECH-type-flowchart.md) — editorial
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  cousin with different shape conventions (diamond, yes/no labels)
