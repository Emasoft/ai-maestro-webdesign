# Versioning — opt-in on-disk diagram versioning

## Table of Contents

- [Opt-in triggers](#opt-in-triggers)
- [Storage layout (per user working directory)](#storage-layout-per-user-working-directory)
- [YAML shape (canonical graph + meta)](#yaml-shape-canonical-graph--meta)
- [Rendering saved versions to ASCII](#rendering-saved-versions-to-ascii)
- [Versioning operations (conversational, not slash-command)](#versioning-operations-conversational-not-slash-command)
- [Conversational edits (mini-DSL for editing saved diagrams)](#conversational-edits-mini-dsl-for-editing-saved-diagrams)
- [When NOT to use versioning](#when-not-to-use-versioning)

For users iterating on an architecture diagram across a long session (adding services, swapping the data layer, pulling a component out of a layer, etc.), this skill supports an **opt-in on-disk versioning layout** so each revision is preserved and can be compared or rolled back. The feature is dormant by default — it activates only when the caller uses one of the versioned-trigger forms below, or explicitly passes an output directory.

## Opt-in triggers

- "save this as v1" / "save the current architecture as a new version"
- "show me v2 of the <name> diagram"
- "rollback <name> to v3"
- "diff v2 and v4 of <name>"
- "list versions of <name>"

## Storage layout (per user working directory)

```
claude-diagrams/
└── <kebab-name>/
    ├── current.yaml     Canonical active version (copy of the latest vN.yaml)
    ├── v1.yaml          First saved graph (validated, post-Stage 1)
    ├── v2.yaml          Second saved graph
    ├── ...
    └── history.yaml     Log of { version, timestamp, description, author }
```

## YAML shape (canonical graph + meta)

The YAML that gets persisted is the validated internal graph (same structure the skill uses in step 2 of the core pipeline — layers, nodes, edges) plus a `meta` block:

```yaml
meta:
  name: "System architecture"
  type: architecture               # architecture | sequence | flowchart | erd
  created: 2026-04-22T10:00:00+02:00
  version: 3
  description: "Added Redis cache between gateway and services"

layers:
  - id: layer-1
    label: Frontend
  # ...

nodes:
  - id: client
    label: "Web Client"
    layer: layer-1
    description: "Browser-based SPA"
  # ...

edges:
  - from: client
    to: gateway
    label: "HTTPS"
  # ...
```

This is a superset of the in-memory graph — the `meta` block adds versioning metadata; `layers`, `nodes`, `edges` are the validated graph unchanged.

## Rendering saved versions to ASCII

When the user asks to view a specific version (`show me v2 of the payment-flow diagram`), the flow is:

1. Load `claude-diagrams/<name>/v2.yaml`.
2. Convert the layered-graph into `bin/amw-ascii-render.py` input (the `layers` JSON mode is the structural match for architecture diagrams; the `diagram` mode is used for flowchart/ERD; `sequence` for sequence diagrams).
3. Pipe to `bin/amw-ascii-render.py` and return the ASCII preview.

ASCII preview is the default viewing format for a saved version because it is token-cheap and fits inline in chat. SVG / PNG are still available by re-running step 3 of the core pipeline on the loaded graph — same output formats, same validations.

## Versioning operations (conversational, not slash-command)

| User says | Skill does |
|---|---|
| "save this as a new version" | Increment version number in `history.yaml`; write `vN.yaml`; update `current.yaml`. |
| "show me v2 of <name>" | Load `vN.yaml`; render via `bin/amw-ascii-render.py` (layers/diagram/sequence mode). |
| "rollback <name> to v2" | Copy `v2.yaml` over `current.yaml`; do NOT delete v3/v4 — rollback is a new version, not a destructive revert. Log a new entry in `history.yaml` noting the rollback source. |
| "diff v2 and v4" | Load both YAMLs; report layer/node/edge additions, removals, and label changes as a structured list (not a textual unified diff — graphs don't diff well as text). |
| "list versions of <name>" | Read `history.yaml`; print a one-line-per-version table (version, timestamp, description). |
| "open <name>" | Load `claude-diagrams/<name>/current.yaml`; render via ASCII as the quick view; prompt for next action. |

The versioning layer is a thin wrapper — it does NOT bypass Stage 1 / Stage 2 validation. Every saved version must pass validation before persistence; a graph that fails validation is never committed to disk.

## Conversational edits (mini-DSL for editing saved diagrams)

When the user has loaded a saved YAML diagram (`open <name>` or `show me v2`), they can mutate it with natural-language edits instead of re-authoring the whole system description. This is a **mini-DSL** — a small fixed vocabulary of NL → graph-operation mappings. After each edit, the skill re-runs Stage 1 validation, bumps the version via the versioning flow above, and renders the new ASCII preview inline. This is the conversational companion to the YAML versioning layout — they share one storage substrate.

Source: ported and translated from the diagram-skill-main source (originally Spanish — "Agrega un servicio de cache", etc.). Translated to English below.

| User says | Skill does |
|---|---|
| "add a cache service" / "add a Redis cache between frontend and auth" | Add one `service`-type node; if a position hint is given ("between X and Y"), insert it on that edge (split the X→Y edge into X→new and new→Y). |
| "remove service X" / "delete the X component" | Remove node X and every edge with `source == X` or `target == X`. |
| "connect X to Y" / "link X with Y" | Create a new edge `{source: X, target: Y}`. If an edge already exists, no-op. |
| "move X before Y" / "move X into the Frontend layer" | Re-assign `node.layerId` for X; re-run Stage 1.3 (layer balance). |
| "group these into Backend" / "wrap X, Y, Z in a new layer called Backend" | Create a new layer with the given label; move the listed nodes into it. |
| "rename X to Z" | Update `node.label` for X (keep `node.id` stable so edges don't break); re-run Stage 1.4 (label quality). |
| "label the edge X→Y as 'HTTPS'" | Set `edge.label` for the matching edge. |
| "disconnect X from Y" | Remove the edge `{source: X, target: Y}` only — leaves nodes in place. |
| "save this" / "commit this version" | Persist via the versioning flow above — increment `vN.yaml`, update `current.yaml`, append to `history.yaml`. |

**Rules for the mini-DSL:**

- **No edit bypasses validation.** After every NL edit, re-run Stage 1 on the mutated graph. If the edit violates a hard constraint (e.g. would empty a layer, or push node count past 14), reject the edit and tell the user which rule was violated — do not silently patch.
- **IDs are stable; labels are free.** A rename updates `node.label`, never `node.id`. This keeps the edges intact across edits.
- **The YAML is the source of truth between edits.** After each confirmed edit, the new graph is persisted via the versioning flow — there is no in-memory-only "dirty" state that can be lost to a crash or a context reset.
- **Ambiguous edits require clarification.** "move X" with no destination, "connect these" with no explicit node pair, "remove the red one" — the skill asks one clarifying question rather than guess.

## When NOT to use versioning

- **Single-shot requests.** "Draw the architecture of X as SVG" — no versioning, no disk writes, just the SVG.
- **Claude.ai sandboxed environments without filesystem write access.** The skill degrades gracefully: version operations become in-memory-only for the session, and the caller is told that versions will not persist.
- **Large teams with shared architecture repos.** The on-disk layout is per-user-working-directory by design; it is not a substitute for a shared ADR / diagrams repo. Tell the user to commit `claude-diagrams/<name>/` to their own repo if they want persistence beyond the session.

(This versioning feature subsumes the scope of the upstream read-only `diagram-skill-main` source, which produced ASCII-previewed versioned architecture / flowchart / sequence / ERD diagrams on disk. That source's slash-command surface — `/diagram new`, `/diagram history`, `/diagram rollback` — is intentionally NOT reimplemented as slash commands in this plugin; the conversational triggers above replace them. The plugin reserves the `/amw-*` namespace for capabilities that cannot be invoked via natural-language intent alone.)
