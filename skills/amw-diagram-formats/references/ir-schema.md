## Table of Contents

- [1. Top-level shape](#1-top-level-shape)
- [2. `nodes`](#2-nodes)
- [3. Well-known annotations](#3-well-known-annotations)
- [4. Raw-source fast path (MVP)](#4-raw-source-fast-path-mvp)
- [5. Lossy-conversion matrix](#5-lossy-conversion-matrix)
- [6. Versioning policy](#6-versioning-policy)
- [7. Example IRs](#7-example-irs)
  - [Minimal flowchart (3 nodes, 2 edges)](#minimal-flowchart-3-nodes-2-edges)
  - [Sequence (two actors, one message + note)](#sequence-two-actors-one-message-note)
  - [Architecture (3 layers)](#architecture-3-layers)
  - [Raw-source stub (MVP HTML → IR)](#raw-source-stub-mvp-html-ir)
- [8. Validation](#8-validation)
- [9. Consumers](#9-consumers)


# IR Schema — `diagram-ir/1.0`

**Authoritative spec for the plugin's Intermediate Representation.** Pair this prose with the machine-readable `../schema.json`; they describe the same shape. Changes to either MUST change both together, and MUST be gated by an ADR + explicit version bump (§6 below).

The IR is the pivot format used by `bin/amw-diagram-ir.py`, by every `amw-convert-any-diagram-format` dispatch, by `/amw-compare-diagrams`, and by the 4 `wd-create-or-modify-*-diagram` modify-flows. It is intentionally **lossy** (§5) — the goal is structural preservation, not byte-perfect round-trip.

## 1. Top-level shape

```json
{
  "format": "diagram-ir/1.0",
  "source_format": "ascii|html|svg|mermaid",
  "kind": "flowchart|sequence|state|arch|tree|table|freeform",
  "layout": "layered|grid|freeform|sequence",
  "nodes": [ ... ],
  "edges": [ ... ],
  "metadata": { ... }
}
```

Required fields: `format`, `source_format`, `kind`, `layout`, `nodes`, `edges`. `metadata` is optional.

`format` is the version identifier — it MUST be `diagram-ir/1.0`. Every parser writes this; every emitter / validator refuses anything else until the schema is formally bumped.

`source_format` records the format the IR was parsed **from**. It is consumed by downstream emitters to apply format-specific re-styling on round-trip (e.g. an ASCII → HTML emission uses starter-component chrome; an SVG → HTML emission wraps the existing SVG).

`kind` is a semantic hint — it drives template selection inside each emitter. A `flowchart` IR emits a Mermaid `flowchart TD`, a `sequence` IR emits a Mermaid `sequenceDiagram`, and so on.

`layout` is the visual placement intent. `freeform` means "the source did not dictate a layout"; `layered` / `grid` / `sequence` each map to specific emitter templates.

## 2. `nodes`

Every node has:

| Field | Required | Notes |
|---|---|---|
| `id` | Y | Stable identifier. `^[A-Za-z0-9_\-]+$`. Used as match key for IR-diff. |
| `label` | Y | Human-readable label. Emitted verbatim. For freeform raw-source IR (see §4), `label` carries the entire source text. |
| `bbox` | N | Absolute `{x,y,w,h}`. Lossy through ASCII round-trips. |
| `rank` | N | Layer index for layered diagrams (0 = top / leftmost). |
| `style` | N | `{shape, fill, stroke, corner}`. All free-form strings. |
| `annotations` | N | Free-form tag list (see §3). |

## 3. Well-known annotations

`annotations` is a tag array with a small vocabulary of well-known values. Parsers and emitters MUST preserve unknown tags verbatim (additive is fine; destructive is not).

| Tag | Meaning |
|---|---|
| `entry-point` | Start node of a flow. Rendered with a distinguishing style. |
| `decision` | Diamond-shape decision node. |
| `external` | Out-of-scope system / actor. Rendered dashed or grey. |
| `terminal` | End / terminal node. |
| `raw-source` | The node carries a verbatim copy of the source document in its `label`. Emitters for the matching `source_format` MUST round-trip the label byte-for-byte. Used by the MVP parser for HTML / SVG / Mermaid until Phase 1 format-native parsers land. |

## 4. Raw-source fast path (MVP)

Until Phase 1 ships native parsers for HTML / SVG / Mermaid, the MVP parser emits a stub IR of the form:

```json
{
  "format": "diagram-ir/1.0",
  "source_format": "html",
  "kind": "freeform",
  "layout": "freeform",
  "nodes": [{"id": "raw", "label": "<html>... entire source ...</html>", "annotations": ["raw-source"]}],
  "edges": []
}
```

Emitters inspect `annotations` and — when the target format matches `source_format` — emit `nodes[0].label` verbatim. This keeps conversion pipelines from breaking before structural parsers are written: an HTML → HTML "conversion" round-trips byte-for-byte, and an HTML → ASCII "conversion" falls through to a plain `<pre>`-ish listing that the user can iterate on.

When the native parsers land in Phase 1, these stubs become structured IRs and `annotations: ["raw-source"]` disappears from the emitted documents — the schema does not change.

## 5. Lossy-conversion matrix

Every parse-to-IR is lossy. Downstream emitters cannot reconstruct the lost information from the IR alone. The table below names what each format LOSES on parse.

| Source format | Lost on parse to IR |
|---|---|
| **ASCII** | Exact character positions within cells. Font face (monospace implied). Color (monochrome implied). Any non-structural decoration (legend text, watermarks). |
| **HTML** | Inline CSS classes, keyframes / transitions / hover states. JavaScript-driven mutations. Non-SVG embedded content (video, iframes). Responsive breakpoints. |
| **SVG** | `filter="..."` / `<filter>` chains. Multi-stop gradients beyond the primary palette. Embedded `<font>` / `<font-face>`. `<clipPath>`. `<mask>`. `<pattern>`. Non-semantic `<g>` group boundaries. |
| **Mermaid** | Config directives (`%%{init: ...}%%` block). Theme variables. Interaction `click` / `linkStyle` rules. `classDef` style defs. |
| **PNG** | Not parseable in MVP. `source_format: "png"` is `impossible` by plugin directive. The dispatcher refuses PNG inputs. |

Round-trip guidance:

- **Same-format round-trip** (e.g. SVG → IR → SVG) preserves structure but drops styling / filters / gradients per the table. If a skill needs byte-perfect round-trip, it must take the raw-source fast path (§4) and NOT route through a structured IR.
- **Cross-format round-trip** loses BOTH the source-format styling AND the target format's native idioms. Emission should re-add the target format's chrome (e.g. starter-components for HTML, themes for Mermaid).

## 6. Versioning policy

- `format: "diagram-ir/1.0"` is LOCKED for Phase 0. No silent schema drift.
- Backwards-incompatible changes require:
  1. ADR in the repo documenting the motivation and migration path.
  2. Bump to `diagram-ir/1.1` or `diagram-ir/2.0` per semver (minor = additive, major = breaking).
  3. Update to `../schema.json`, this document, and `bin/amw-diagram-ir.py::IR_VERSION` in the same commit.
  4. Parsers accept old versions for a deprecation window; emitters always emit the latest.
- Additive changes (new optional field, new well-known annotation tag) are still minor-version bumps — consumers that rely on `additionalProperties: false` will break if we don't bump.

## 7. Example IRs

### Minimal flowchart (3 nodes, 2 edges)

```json
{
  "format": "diagram-ir/1.0",
  "source_format": "ascii",
  "kind": "flowchart",
  "layout": "layered",
  "nodes": [
    {"id": "start", "label": "Login",    "annotations": ["entry-point"]},
    {"id": "check", "label": "2FA?",     "annotations": ["decision"]},
    {"id": "home",  "label": "Dashboard"}
  ],
  "edges": [
    {"id": "e1", "from": "start", "to": "check"},
    {"id": "e2", "from": "check", "to": "home", "label": "ok"}
  ]
}
```

### Sequence (two actors, one message + note)

```json
{
  "format": "diagram-ir/1.0",
  "source_format": "mermaid",
  "kind": "sequence",
  "layout": "sequence",
  "nodes": [
    {"id": "user", "label": "User"},
    {"id": "api",  "label": "API"}
  ],
  "edges": [
    {"id": "m1", "from": "user", "to": "api", "label": "POST /login", "style": {"arrow": "solid"}}
  ],
  "metadata": {"title": "Login flow"}
}
```

### Architecture (3 layers)

```json
{
  "format": "diagram-ir/1.0",
  "source_format": "svg",
  "kind": "arch",
  "layout": "layered",
  "nodes": [
    {"id": "ui",  "label": "UI",       "rank": 0},
    {"id": "api", "label": "API",      "rank": 1},
    {"id": "db",  "label": "Postgres", "rank": 2}
  ],
  "edges": [
    {"id": "a",  "from": "ui",  "to": "api"},
    {"id": "b",  "from": "api", "to": "db"}
  ]
}
```

### Raw-source stub (MVP HTML → IR)

```json
{
  "format": "diagram-ir/1.0",
  "source_format": "html",
  "kind": "freeform",
  "layout": "freeform",
  "nodes": [{"id": "raw", "label": "<!DOCTYPE html>...", "annotations": ["raw-source"]}],
  "edges": []
}
```

## 8. Validation

Validation is enforced by `bin/amw-diagram-ir.py validate` and by `../schema.json` (the machine-readable mirror of this document). Both must agree.

Beyond pure schema validation, the validator enforces two semantic invariants:

1. Every `edge.from` and `edge.to` MUST reference an existing `node.id`. Dangling edges are a FAIL.
2. `format` MUST equal `diagram-ir/1.0` exactly. A missing or mismatched version number is a FAIL.

Both checks are present in `bin/amw-diagram-ir.py::validate`.

## 9. Consumers

- `bin/amw-diagram-ir.py` (library + CLI).
- `bin/amw-diagram-ir-diff.py` (Task 3c — future; consumes the `diff` op list specified in [diff-algorithm](./diff-algorithm.md)).
- Every `wd-create-or-modify-*-diagram` command's modify-flow (see [modify-flow](./modify-flow.md)).
- `/amw-convert-any-diagram-format` (see [conversion-matrix](./conversion-matrix.md)).
- `/amw-compare-diagrams` (see [diff-algorithm](./diff-algorithm.md)).

Any change to the IR shape ripples through all of these; bump the version in lockstep.
