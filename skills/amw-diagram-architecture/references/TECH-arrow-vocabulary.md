---
name: TECH-arrow-vocabulary
category: arrow-vocab
source: diagram-skill-main/ASCII-STYLES.md
also-in: diagram-skill-main/REFERENCE.md
---

# TECH-arrow-vocabulary — 6-type connection taxonomy

## What it does

Defines a 6-type taxonomy of edge semantics — sync / async / return /
bidirectional / dependency / association — each rendered with a distinct
arrowhead or dash pattern. Used across Mermaid, SVG, and ASCII renderers
so the reader learns one vocabulary and applies it everywhere.

## When to use

Any architecture or sequence diagram where the TYPE of connection
matters — sync REST call vs async Kafka publish vs "uses" dependency
vs data association.

## How it works

| Type | Unicode | Classic ASCII | Compact | Meaning |
|---|---|---|---|---|
| `sync` | `───▶` | `---->` | `→` | Synchronous request, default |
| `async` | `- - ▶` | `- - >` | `⇢` | Fire-and-forget, event emit |
| `return` | `◀───` | `<----` | `←` | Paired return after a call |
| `bidirectional` | `◀──▶` | `<-->` | `↔` | Handshake / symmetric |
| `dependency` | `───▷` | `----D` | `⊳` | Hollow head — depends on / uses |
| `association` | `────` | `------` | `─` | Plain link, no directional semantics |

Conventions:

- Pick one *primary* style per diagram, reserve one alternative for
  contrast (all sync except one async fan-out).
- Three or more styles without a legend = noise.

## Minimal example

```
// Source: diagram-skill-main/ASCII-STYLES.md lines 183-193 + REFERENCE.md lines 127-134
Client ───▶ API (sync REST)
API - - ▶ Kafka (async event publish)
API ◀── DB (return of query result)
API ◀──▶ Cache (bidirectional warm-up)
Worker ───▷ Redis (depends on)
Order ──── Invoice (association)
```

## Gotchas

- The compact forms (`→ ⇢ ← ↔ ⊳ ─`) are the cleanest visually but
  depend on UTF-8 rendering; some viewers fall back to `?`.
- `dependency` with a hollow triangle head is rare in ASCII and sometimes
  drawn as `----D` (a D as the head). The validator flags nothing either
  way.
- Overloading `return` in an architecture diagram is unusual; typically
  it's a sequence-diagram construct.

## Cross-references

- `./TECH-style-presets.md`
- `../../amw-box-diagram/references/TECH-arrow-head-variants.md`
- `../../amw-text-visual-workflows/references/TECH-async-arrow-vocabulary.md`
- [`../SKILL.md`](../SKILL.md) — parent skill

