---
name: TECH-structured-outputs-json
category: architecture-graph
source: replaces TECH-assistant-prefill-json (prefill removed from the Claude API)
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-structured-outputs-json

## What it does

Constrains the model's reply to the graph schema using the Claude API's
**structured outputs** parameter (`output_config.format`), so the response is
valid JSON with no prose preamble, no markdown fences, and no apology text.

This is the supported replacement for the assistant-prefill trick. Prefill was
removed from the API and now returns **HTTP 400** on every current model.

## When to use

- **Every graph-generation call.** The system prompt asks for raw JSON; this
  parameter is the mechanical guarantee rather than a request.
- **Any call whose output must be schema-valid JSON** — config generation,
  schema-validated answers.

## How it works

```javascript
const response = await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "claude-sonnet-5",
    max_tokens: 2000,
    system: SYSTEM_PROMPT,
    output_config: {
      format: {
        type: "json_schema",
        schema: GRAPH_SCHEMA   // see TECH-graph-json-schema.md
      }
    },
    messages: [
      { role: "user", content: description }
    ]
  })
});

const data = await response.json();
if (data.error) throw new Error(data.error.message);

const raw = data.content.find(b => b.type === "text").text;
return repairAndParse(raw);   // defence-in-depth, not the primary mechanism
```

The schema does the work the prefill used to do, and does it better: the
prefill only constrained the *first token*, whereas the schema constrains the
whole object.

## Minimal example

```
User: "analytics SaaS with web + mobile + api + postgres"

Response content[0].text:
{"title": "Analytics SaaS", "subtitle": "...", "layers": [...], ...}
```

`JSON.parse(raw)` works directly — there is nothing to prepend.

## Gotchas

- **Nothing to prepend.** Unlike the prefill technique, the returned text is
  the complete object. Prepending `"{"` here produces `{{...` and fails to
  parse. Delete any such prepend when migrating.
- **The schema must satisfy the API's subset.** Every object needs
  `additionalProperties: false` and a `required` array. Numeric/string
  constraints (`minimum`, `maxLength`) are NOT enforced server-side — keep
  enforcing layer/node budgets in
  [TECH-stage1-graph-validation](TECH-stage1-graph-validation.md).
- **First call with a new schema is slower** (one-time compile), then cached
  ~24h. Do not mistake it for a hang.
- **Incompatible with citations**, and a `stop_reason` of `"refusal"` or
  `"max_tokens"` can still yield output that does not match the schema —
  check `stop_reason` before parsing.
- **Keep `repairAndParse`.** It is cheap and covers the truncation case; it is
  no longer load-bearing for shape.
- **Porting to another provider:** the equivalent is that provider's
  strict/JSON-schema response mode. Re-test the prompt under the new model.

## Cross-references

- [prompts](prompts.md) — the full API call pattern
  > System Prompt · API Call Pattern · JSON Repair
- [TECH-assistant-prefill-json](TECH-assistant-prefill-json.md) — the superseded technique this replaces
- [TECH-json-repair-recipe](TECH-json-repair-recipe.md) — downstream repair if parsing still fails
- [TECH-graph-json-schema](TECH-graph-json-schema.md) — the target schema
- [TECH-stage1-graph-validation](TECH-stage1-graph-validation.md) — structural validation after parse
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
