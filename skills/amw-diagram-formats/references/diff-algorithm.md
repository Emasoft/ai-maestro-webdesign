# IR Diff Algorithm — `bin/amw-diagram-ir.py diff` and `bin/diagram-ir-diff.py`

**Authoritative spec for structural diagram comparison.** Consumed by `/amw-compare-diagrams` (via the `diagram-compare/` skill) and by any workflow that needs to answer *"what semantic changes happened between these two versions?"*.

**Why IR-level diff, not text-level diff?** Rendering loses metadata and injects layout noise — two SVGs of the same graph differ in pixel coordinates, and two ASCII wireframes of the same dashboard differ in whitespace. IR diff isolates **semantic** changes (added / removed / renamed nodes, edge rewires, kind / layout changes) from **cosmetic** changes (color, spacing, font).

## 1. Inputs

Two IR JSON documents, both conforming to `../schema.json` (version `diagram-ir/1.0`). Source formats MAY differ — comparing an ASCII diagram against its HTML rendering is explicitly supported, as long as both were parsed to IR via the standard pipeline.

Both inputs MUST be validated before diff:

```bash
bin/amw-diagram-ir.py validate --in a.ir.json
bin/amw-diagram-ir.py validate --in b.ir.json
```

Invalid IRs are rejected before diff — dangling edges, missing required fields, or wrong version all abort.

## 2. Output: ordered list of patch ops

The diff is expressed as a **list of patch ops**, JSON Pointer–flavored but simplified. Each op is a JSON object with an `op` field and per-op auxiliary fields.

```json
[
  {"op": "change-kind",   "from": "flowchart", "to": "tree"},
  {"op": "change-layout", "from": "layered",   "to": "grid"},
  {"op": "add-node",      "node": { ... full node object ... }},
  {"op": "remove-node",   "id": "n3"},
  {"op": "change-node",   "id": "n2", "from": { ... }, "to": { ... }},
  {"op": "add-edge",      "edge": { ... full edge object ... }},
  {"op": "remove-edge",   "id": "e2"},
  {"op": "change-edge",   "id": "e1", "from": { ... }, "to": { ... }}
]
```

| Op | Fields | Meaning |
|---|---|---|
| `change-kind` | `from`, `to` | Top-level `kind` field changed. |
| `change-layout` | `from`, `to` | Top-level `layout` field changed. |
| `add-node` | `node` (full object) | A node in B not in A. |
| `remove-node` | `id` | A node in A not in B. |
| `change-node` | `id`, `from`, `to` | Same id in both, but object contents differ (label, bbox, style, annotations, etc.). |
| `add-edge` | `edge` (full object) | An edge in B not in A. |
| `remove-edge` | `id` | An edge in A not in B. |
| `change-edge` | `id`, `from`, `to` | Same edge id, different contents. |

Ops are emitted in this order: `change-kind`, `change-layout`, then node ops sorted by id, then edge ops sorted by id. This is deterministic — the same two IRs always produce the same patch JSON.

## 3. Node / edge matching

Matching is **strictly by `id`**. Two nodes with the same `id` are "the same node" — any differences in other fields become a `change-node` op. Two nodes with different `id`s are distinct, regardless of label similarity.

Rationale: `id` is declared in `../schema.json` with `pattern: "^[A-Za-z0-9_\\-]+$"` and is the intended stable match key. Callers that want "fuzzy" matching (by label similarity) need to normalize ids first — see §6.

Edges match the same way — by `edge.id`. Two edges with the same endpoints but different ids are treated as `remove + add`, not `change`.

## 4. Deep object equality for `change-*`

When deciding whether a matching node / edge triggers a `change-*` op, we use **JSON-deep-equality** on the whole object. Any difference — a flipped style.fill, an added annotation, a bbox shift of 1 pixel — is a change.

Downstream consumers that want coarser granularity (e.g. ignore bbox changes) should either:

- Strip `bbox` before diff (preprocessing), OR
- Post-filter the patch ops to drop `change-*` ops whose `from` and `to` differ only in `bbox`.

The algorithm does NOT take an "ignore list" parameter in Phase 0 — keep the core deterministic and let callers preprocess.

## 5. Markdown report format

`/amw-compare-diagrams` produces a markdown report on top of the patch ops. The canonical layout:

```markdown
# Diagram comparison

- **A:** `<path-a>` (source_format=ascii, kind=flowchart, layout=layered, 5 nodes, 4 edges)
- **B:** `<path-b>` (source_format=mermaid, kind=flowchart, layout=layered, 6 nodes, 5 edges)

## Summary

- Kind: unchanged (`flowchart`)
- Layout: unchanged (`layered`)
- Nodes: +1 / −0 / ~1 changed
- Edges: +1 / −0 / ~0

## Nodes added

| id | label | annotations |
|---|---|---|
| `logout` | Log out | [] |

## Nodes removed

_(none)_

## Nodes changed

| id | field | from | to |
|---|---|---|---|
| `home` | label | Dashboard | Home |

## Edges added

| id | from → to | label |
|---|---|---|
| `e5` | `home → logout` | _(none)_ |

## Edges removed

_(none)_

## Edges changed

_(none)_
```

When diagrams are identical (empty patch op list), the report is a single line: `No structural differences between A and B.`

## 6. Id normalization (caller preprocessing)

When the two inputs have different id schemes (e.g. one parsed from ASCII uses `n1/n2/...`, one parsed from Mermaid uses user-declared names), the caller may normalize ids BEFORE diff. A typical normalization:

```python
# Rename nodes by label match (greedy; first match wins).
a_by_label = {n["label"]: n["id"] for n in a["nodes"]}
for node in b["nodes"]:
    if node["label"] in a_by_label:
        node["id"] = a_by_label[node["label"]]
```

This is OUT OF SCOPE for the core algorithm — the core is deterministic and id-based. Fuzzy matching lives in the caller.

## 7. Exit codes (CLI)

`bin/amw-diagram-ir.py diff --a a.json --b b.json`:

- Exit `0` — IRs are identical (empty patch list).
- Exit `1` — structural differences present (non-empty patch list).
- Exit `2` — input errors (missing file, invalid JSON, IR validation failure).

`/amw-compare-diagrams` maps those to:

- 0 → "No differences"
- 1 → "Differences present; see report"
- 2 → "Inputs invalid"

## 8. Known limitations

1. **Id renames are recorded as add+remove**, not rename. The algorithm has no heuristic to detect that `{id:"foo", label:"Login"}` in A and `{id:"bar", label:"Login"}` in B are "the same node renamed". Callers can preprocess (§6) or post-process.
2. **Edge waypoints diff at JSON-deep-equality granularity**. A 1-pixel waypoint nudge triggers a `change-edge`. Filter `waypoints` out before diff if you only care about graph structure.
3. **Metadata is not diffed**. The algorithm ignores the `metadata` object entirely — title/author/description changes are invisible. Callers that care should diff metadata separately.
4. **No 3-way diff**. The algorithm is 2-way (A vs B). 3-way merge (e.g. for `diagram-webpage-sync`) composes two 2-way diffs; see `./modify-flow.md` §7.1.
5. **No move-op**. If a node moves between two layers in A vs B, the diff reports `change-node` on its `rank` field; it does not emit a dedicated "move" op.

## 9. Visual mode (optional, future)

`/amw-compare-diagrams --mode visual` is specced as a future option: render both IRs via `bin/amw-mermaid-render.sh` / `bin/amw-svg-render.py`, produce side-by-side PNGs, then run a perceptual-diff tool. Out of scope for Phase 0. Structural mode (this document) is the default and the MVP.

## 10. Related references

- `./ir-schema.md` — shape of the inputs.
- `./modify-flow.md` — the modify pipeline; diff is a "read-only" sibling that shares steps 1+2.
- `./conversion-matrix.md` — when comparing cross-format, both inputs go through this matrix to IR first.
- `../../amw-diagram-compare/SKILL.md` — the thin consumer skill that wraps this algorithm.
