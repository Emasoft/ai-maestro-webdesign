---
name: TECH-yaml-canonical-schema
category: yaml-versioning
source: diagram-skill-main/REFERENCE.md
also-in: diagram-skill-main/SKILL.md, diagram-skill-main/EXAMPLES.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-yaml-canonical-schema — `meta / nodes / edges / groups / notes`

## What it does

Defines a canonical YAML schema for architecture / sequence / flowchart /
ERD diagrams with five top-level keys: `meta` (name + type + version),
`nodes`, `edges`, `groups` (containment), and `notes` (annotations).
The schema is the single-source-of-truth the renderer parses — all
output formats (ASCII, Mermaid, SVG, PlantUML, D2) derive from one YAML.

## When to use

When iterating on a diagram across sessions or branches — YAML is
human-editable, diff-friendly, and version-control-compatible. Also
when generating multiple output formats from one source; write the
YAML once, render many ways.

## How it works

Top-level keys:

```yaml
meta:
  name: "Authentication Flow"       # required
  type: sequence|flowchart|architecture|erd  # required
  created: 2026-01-14T10:00:00Z
  version: 1
  description: "User login with JWT token generation"
  author: "Emasoft"

nodes:                              # required, list
  - id: user           # kebab-case unique ID
    label: "User"      # visible text
    type: actor        # actor|component|service|database|queue|external|decision|process|entity
    style: primary     # primary|secondary|highlight|dimmed (optional)
    group: frontend    # ID of parent group (optional)

edges:                              # required, list
  - from: user         # source node ID
    to: frontend       # target node ID
    label: "Login"     # optional edge label
    type: sync         # sync|async|return|bidirectional|dependency|association
    order: 1           # for sequence diagrams

groups:                             # optional
  - id: frontend
    label: "Frontend"
    nodes: [user, web-app]
    style: dashed

notes:                              # optional
  - target: auth-service
    text: "Rate limit: 100/min"
    position: bottom
```

## Minimal example

```yaml
# Source: diagram-skill-main/EXAMPLES.md lines 10-90 (Auth flow excerpt)
meta:
  name: "Authentication Flow"
  type: sequence
  version: 1

nodes:
  - id: user
    label: "User"
    type: actor
  - id: frontend
    label: "Frontend"
    type: component
  - id: auth-service
    label: "Auth Service"
    type: service

edges:
  - from: user
    to: frontend
    label: "1. Login"
    type: sync
    order: 1
  - from: frontend
    to: auth-service
    label: "2. Validate"
    type: sync
    order: 2
```

## Gotchas

- Node IDs must be unique and kebab-case — the renderer errors on
  duplicates or spaces.
- Every edge's `from`/`to` must match an existing node ID.
- `meta.type` is required — the renderer dispatches layout by type.

## Cross-references

- [TECH-version-history-yaml](./TECH-version-history-yaml.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-export-mermaid-plantuml-d2](./TECH-export-mermaid-plantuml-d2.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [formats](./formats.md) (existing reference)
  > Format 1: `graph` (default) · Schema · Constraints · Format 2: `mermaid` · Transform Rules · Layer Color Mapping · Mermaid Output Template · Mermaid ID Safety · Format 3: `svg` · Layout Algorithm · SVG Structure · SVG Height Calculation · Format 4: `png`
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

