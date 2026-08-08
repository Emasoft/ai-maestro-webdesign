---
name: TECH-assistant-prefill-json
category: architecture-graph
status: superseded
superseded-by: TECH-structured-outputs-json
source: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/prompts.md
also-in:
---

# TECH-assistant-prefill-json — SUPERSEDED

> **DO NOT USE THIS TECHNIQUE. It returns HTTP 400 on every current Claude model.**
>
> Use **[TECH-structured-outputs-json](TECH-structured-outputs-json.md)** instead.

This file is retained as a redirect so its existing cross-references keep
resolving. The technique it used to document has been removed from the API.

## What changed

Forcing JSON-first output with a trailing assistant turn —

```javascript
{ role: "assistant", content: "{" }   // ← no longer valid
```

— is a **last-assistant-turn prefill**. Prefills were removed from the Claude
API and now return **HTTP 400** on Sonnet 5, Opus 5, Fable 5, and the entire
4.6 / 4.7 / 4.8 family. There is no model still in the catalogue on which this
skill's documented call pattern would have worked.

The replacement is **structured outputs** (`output_config.format` with a
`json_schema`), which constrains the whole object rather than just the first
token, and needs no client-side re-prepending of `"{"`.

## Migrating a caller

1. Delete the trailing `{ role: "assistant", content: "{" }` message.
2. Add `output_config: { format: { type: "json_schema", schema: GRAPH_SCHEMA } }`.
3. **Delete the `"{" +` prepend** before parsing — the response is now the
   complete object, and prepending produces `{{…` which fails to parse.
4. Keep `repairAndParse` as defence-in-depth for truncation.

Full pattern and gotchas: [TECH-structured-outputs-json](TECH-structured-outputs-json.md).

## Cross-references

- [TECH-structured-outputs-json](TECH-structured-outputs-json.md) — **the replacement; read this instead**
- [prompts](prompts.md) — the full API call pattern (already migrated)
  > System Prompt · API Call Pattern · JSON Repair
- [TECH-json-repair-recipe](TECH-json-repair-recipe.md) — downstream repair if parsing still fails
- [TECH-graph-json-schema](TECH-graph-json-schema.md) — the target schema
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
