---
name: TECH-render-mode-sequence
category: ascii-render
source: perfect-ascii-main/server.py
also-in: perfect-ascii-main/README.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH-render-mode-sequence — lifelines + messages + notes

## What it does

Produces sequence diagrams with actors, vertical lifelines (`|`), solid
request arrows (`-->`), dashed response arrows (`- ->`), and optional boxed
notes spanning between two lifelines.

## When to use

Any multi-actor interaction where the order of messages matters: request/
response flows, OAuth handshakes, payment pipelines, pub/sub event walks.

## How it works

Top-level `sequence` key holds:

- `actors`: ordered list of participant names (left to right, 4-5 max to fit
  in 78 cols).
- `messages`: each message is `{from, to, label, style}`. `style: "solid"`
  renders `-->`, `style: "dashed"` renders `- ->`.
- `notes` (optional): `[{between: [actor1, actor2], text, after_message: N}]`
  places a boxed text block spanning the two lifelines immediately after
  the 0-indexed message `N`.

## Minimal example

```json
// Source: perfect-ascii-main/server.py docstring
{
  "sequence": {
    "actors": ["User", "Frontend", "API Server", "Database"],
    "messages": [
      {"from": "User",       "to": "Frontend",   "label": "Click checkout", "style": "solid"},
      {"from": "Frontend",   "to": "API Server", "label": "POST /checkout", "style": "solid"},
      {"from": "API Server", "to": "Database",   "label": "INSERT order",   "style": "solid"},
      {"from": "Database",   "to": "API Server", "label": "OK",             "style": "dashed"},
      {"from": "API Server", "to": "Frontend",   "label": "200 OK",         "style": "dashed"}
    ],
    "notes": [
      {"between": ["Frontend", "API Server"], "text": "Timeout after 30s", "after_message": 1}
    ]
  }
}
```

## Gotchas

- Keep actor names short; their width drives the column spacing.
- Notes must fit between the two named actors; cross-diagram spans aren't
  supported.
- `after_message: N` is 0-based — the note appears after the Nth message.

## Cross-references

- [TECH-json-render-four-modes](./TECH-json-render-four-modes.md)
- [TECH-sequence-notes](./TECH-sequence-notes.md)
- [`../SKILL.md`](../SKILL.md) — parent skill

