---
name: TECH-version-history-yaml
category: yaml-versioning
source: diagram-skill-main/REFERENCE.md
also-in: diagram-skill-main/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-version-history-yaml — v1 / v2 / ... + history.yaml + rollback

## What it does

Persists every saved revision of a diagram to a per-diagram folder
(`claude-diagrams/<name>/v1.yaml`, `v2.yaml`, ...) plus a
`history.yaml` log that tracks which version is current and when each
was saved. Lets the caller `/diagram rollback 3` or `/diagram diff 2 4`
without losing prior work.

## When to use

Long sessions where the user iterates on a diagram (adding services,
swapping the data layer, pulling a component out of a group). Also
team workflows where a stable diagram lives under source control and
new revisions need review.

## How it works

Per-diagram storage layout:

```
claude-diagrams/
└── <kebab-name>/
    ├── current.yaml      Canonical active version (copy of latest vN)
    ├── v1.yaml           First saved graph (validated)
    ├── v2.yaml           Second saved graph
    ├── ...
    └── history.yaml      Log of { version, timestamp, message }
```

`history.yaml`:

```yaml
versions:
  - version: 1
    timestamp: 2026-01-14T10:00:00Z
    message: "Initial diagram"
  - version: 2
    timestamp: 2026-01-14T10:15:00Z
    message: "Added cache layer"
  - version: 3
    timestamp: 2026-01-14T10:30:00Z
    message: "Simplified DB connections"
current: 3
```

## Minimal example

```
// Source: diagram-skill-main/SKILL.md lines 116-125 + REFERENCE.md lines 216-234
Session flow:

Usuario: /diagram new auth-flow
Claude: [creates claude-diagrams/auth-flow/v1.yaml + current.yaml + history.yaml]

Usuario: Agrega un cache de Redis entre el frontend y el auth service
Claude: [saves v2.yaml + updates history.yaml + updates current.yaml]
        Agregué Redis Cache. Guardado como v2.

Usuario: /diagram history
Claude: Versiones de auth-flow:
        v1 - 10:00 - Initial diagram
        v2 - 10:15 - Added Redis Cache  ← actual
```

## Gotchas

- `current.yaml` is a copy, not a symlink — easier to diff but requires
  an explicit write after every save.
- Versions are numbered sequentially; deleted/rolled-back versions leave
  gaps (`v1, v3, v5` is valid).
- `history.yaml.current` is the authoritative pointer; `current.yaml`
  the artifact. If they disagree, `history.yaml` wins.

## Cross-references

- [TECH-yaml-canonical-schema](./TECH-yaml-canonical-schema.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-export-mermaid-plantuml-d2](./TECH-export-mermaid-plantuml-d2.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

