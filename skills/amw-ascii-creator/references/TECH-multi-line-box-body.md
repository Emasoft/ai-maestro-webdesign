---
name: TECH-multi-line-box-body
category: ascii-render
source: perfect-ascii-main/server.py
also-in: box-diagram-master/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-multi-line-box-body — rich multi-row boxes via `body[]`

## What it does

In `diagram` mode, a box can include a `body` field — a list of strings, one
per body line. The renderer draws a separator rule under the main label, then
each body string on its own line, all padded to the frame width. Used for ER
attribute lists, state-machine entry/exit actions, and richly labeled
pipeline stages.

## When to use

- ER diagrams: label = entity name, body = attribute list (`id: uuid`, `email: string`)
- State machines: label = state name, body = entry/exit actions
- Runbook flows: label = step number + name, body = commands / severity /
  on-call channel (see `box-diagram/examples/incident-response.txt`)

## How it works

Each box object becomes:

```
+----------------+
| label          |
+----------------+
| body[0]        |
| body[1]        |
| ...            |
+----------------+
```

The renderer computes the frame width as `max(len(label), max(len(line) for line in body)) + padding`.

## Minimal example

```json
// Source: perfect-ascii-main/server.py docstring + box-diagram/examples/incident-response.txt
{
  "diagram": {
    "boxes": [
      {
        "id": "alert",
        "label": "ALERT TRIGGERED",
        "body": [
          "PagerDuty -> #incident",
          "Severity: P1",
          "Source: Grafana"
        ]
      }
    ],
    "grid": [["alert"]],
    "connectors": []
  }
}
```

## Gotchas

- Every body line counts toward the 78-col cap.
- The separator rule between label and body is automatic — do not include it
  manually in the body array.
- Blank body lines are allowed and produce a visually empty row; useful for
  pagination in a long list of attributes.

## Cross-references

- [TECH-render-mode-diagram](./TECH-render-mode-diagram.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- `../../amw-box-diagram/examples/incident-response.txt`
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

