---
name: TECH-sequence-notes
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


# TECH-sequence-notes — inline boxed annotations between lifelines

## What it does

In `sequence` mode, a `notes` array lets the author place a small boxed text
block spanning between two specific lifelines, immediately after a given
message index. Used for timeouts, preconditions, side-effects, or any
metadata a plain arrow cannot convey.

## When to use

- "Timeout after 30s" between a request and its response lifelines
- "Retry on 429" between an outgoing call and an inner service
- "Side-effect: writes to audit_log" on a DB write
- "Async — fire and forget" on an event-emit message

## How it works

A note is:

```json
{"between": ["actorA", "actorB"], "text": "...", "after_message": N}
```

The renderer draws a boxed block spanning the columns of the two named
actors, positioned between the Nth message (0-indexed) and the (N+1)th. Text
is wrapped if it exceeds the column span width.

## Minimal example

```json
// Source: perfect-ascii-main/server.py docstring
{
  "sequence": {
    "actors": ["User", "Frontend", "API", "DB"],
    "messages": [
      {"from": "User",     "to": "Frontend", "label": "Click checkout",  "style": "solid"},
      {"from": "Frontend", "to": "API",      "label": "POST /checkout",  "style": "solid"},
      {"from": "API",      "to": "DB",       "label": "INSERT order",    "style": "solid"},
      {"from": "DB",       "to": "API",      "label": "OK",              "style": "dashed"},
      {"from": "API",      "to": "Frontend", "label": "200 OK",          "style": "dashed"}
    ],
    "notes": [
      {"between": ["Frontend", "API"], "text": "Timeout after 30s", "after_message": 1}
    ]
  }
}
```

## Gotchas

- Note text must fit in the column span between the two named actors; wider
  notes force a renderer error.
- `between` must name two actors that appear in `actors[]`; spelling must
  match exactly.
- Each note adds a row to the vertical layout — don't stack more than 2-3
  notes in a single sequence or the diagram gets unreadable.

## Cross-references

- [TECH-render-mode-sequence](./TECH-render-mode-sequence.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

