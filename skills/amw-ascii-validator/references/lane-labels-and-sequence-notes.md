# Lane-labeled diagrams and sequence-mode inline notes

## Table of Contents

- [Lane-labeled diagrams (git graphs, CI pipelines)](#lane-labeled-diagrams-git-graphs-ci-pipelines)
- [Sequence-mode inline notes](#sequence-mode-inline-notes)
- [Cross-references](#cross-references)

Companion reference for [SKILL](../SKILL.md). Two advanced renderer features of `bin/amw-ascii-render.py` that the orchestrator should consult only when needed.

## Lane-labeled diagrams (git graphs, CI pipelines)

`diagram` mode accepts an optional top-level `lanes: ["label1", "label2", ...]` array that renders left-margin track labels next to each grid row — same pattern `layers` mode uses, but driven by arbitrary lane names instead of an automatic `"Presentation / API / Services / Data"` style. Use this for git-branch graphs, CI-pipeline swimlanes, or any diagram where each horizontal row represents a distinct named track.

Git-merge example:

```json
{
  "diagram": {
    "lanes": ["main", "feature"],
    "boxes": [
      {"id": "m1", "label": "v1.0"},
      {"id": "m2", "label": "v1.1"},
      {"id": "f1", "label": "auth"},
      {"id": "f2", "label": "tests"}
    ],
    "grid": [
      ["m1", null, "m2"],
      [null, "f1", "f2"]
    ],
    "connectors": [
      {"from": "m1", "to": "m2"},
      {"from": "m1", "to": "f1", "label": "branch"},
      {"from": "f1", "to": "f2"},
      {"from": "f2", "to": "m2", "label": "merge"}
    ]
  }
}
```

Rendered output shows `main` / `feature` labels at the left margin of each row and routes the branch/merge connectors with elbowed L-shapes between lanes. Works the same way for CI pipelines (`["build", "test", "deploy"]`), or any two-or-three-track flow that would be cramped on a single linear row.

## Sequence-mode inline notes

`sequence` mode supports a `notes` array alongside `messages`. Each note is `{"between": [actor1, actor2], "text": "...", "after_message": N}` where `N` is the 0-based index of the message after which to place the note. The renderer draws a boxed text block spanning the two actors, positioned between the outgoing message and the next interaction. Use notes to annotate timeouts, preconditions, side effects, or anything a plain message arrow cannot convey.

Timeout-annotation example:

```json
{
  "sequence": {
    "actors": ["User", "Frontend", "API", "DB"],
    "messages": [
      {"from": "User", "to": "Frontend", "label": "Click checkout", "style": "solid"},
      {"from": "Frontend", "to": "API", "label": "POST /checkout", "style": "solid"},
      {"from": "API", "to": "DB", "label": "INSERT order", "style": "solid"},
      {"from": "DB", "to": "API", "label": "OK", "style": "dashed"},
      {"from": "API", "to": "Frontend", "label": "200 OK", "style": "dashed"}
    ],
    "notes": [
      {"between": ["Frontend", "API"], "text": "Timeout after 30s", "after_message": 1}
    ]
  }
}
```

The note appears as a small boxed block between the Frontend and API lifelines right after message 1 (`POST /checkout`), reading `Timeout after 30s`. Keep note text under ~30 chars per line to respect the 78-col overall width cap; the renderer errors out if a note overflows.

## Cross-references

- [SKILL](../SKILL.md) — the parent validator + renderer skill.
- [SKILL](../../amw-ascii-sketch/SKILL.md) — the most common consumer of the lane-labeled feature (dashboard variants with named regions).
- `../../../bin/amw-ascii-render.py` — renderer (the `render_ascii` docstring at the top of the file has the canonical JSON schema).
