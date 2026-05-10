---
name: TECH-assistant-prefill-json
category: architecture-graph
source: SKILLS-TO-INTEGRATE/diagrams-skills/architecture-canvas/references/prompts.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-assistant-prefill-json

## What it does

Uses the Claude API's **assistant prefill** feature to force the model's
output to begin inside a JSON object — no prose preamble, no markdown
fences, no apology text. Prepend `"{" ` to the assistant's content, run
the call, then prepend `"{"` back to the response text before parsing.

## When to use

- **Every graph-generation call.** The system prompt tells the model to
  return raw JSON, but LLMs periodically slip in explanatory prose. The
  prefill is the mechanical guard against that.
- **Any other call** where the output must be structured JSON with no
  surrounding text — config generation, tool-call-like responses,
  schema-validated answers.

## How it works

Claude API messages with prefill:

```javascript
const response = await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "claude-sonnet-4-20250514",
    max_tokens: 2000,
    system: SYSTEM_PROMPT,
    messages: [
      { role: "user",      content: description },
      { role: "assistant", content: "{" }            // prefill
    ]
  })
});

const data = await response.json();
if (data.error) throw new Error(data.error.message);

// The model's reply continues from "{" — prepend it back before parsing
const raw = "{" + data.content.find(b => b.type === "text").text;
return repairAndParse(raw);
```

The prefill guarantees:

- The model's response begins inside the JSON object — no prose preamble.
- The first token it emits is constrained to "valid JSON continuation".
- Any apology text or "here's your diagram:" prefix is eliminated.

## Minimal example

User description → assistant reply (with prefill):

```
User: "analytics SaaS with web + mobile + api + postgres"

Assistant (with prefill "{"): continues emitting...
"title": "Analytics SaaS", "subtitle": "...", "layers": [...], ...}
```

After the call, client prepends `"{"` and parses:

```javascript
const raw = "{" + responseText;
// raw = '{"title": "Analytics SaaS", ...}'
JSON.parse(raw);   // works
```

## Gotchas

- **Do not prefill with `{"`** (quote after brace). Prefill `"{"` only —
  the opening brace, nothing else. The model will emit the first key's
  quote, its name, etc.
- **Prepend `"{"` when parsing.** The prefill text itself is NOT echoed
  in `response.content`; it's the STARTING point from which the model
  continued. So the returned text starts with `"title":...`, not
  `{"title":...`.
- **Still run `repairAndParse`.** Even with the prefill, models
  occasionally close a JSON string with a literal newline, forget a
  comma, or include a stray markdown fence. See
  [TECH-json-repair-recipe](TECH-json-repair-recipe.md) for the recovery logic.
- **Set `max_tokens` high enough.** A 10-node graph serialises to ~800
  tokens; cap at 2000 to allow for Stage 1 expansion (descriptions,
  labels). Running out of tokens mid-object produces unparseable
  output that repair can't always recover.
- **Prefill works on Claude, not generic LLMs.** If this skill is ever
  ported to a different provider, the equivalent trick is usually a
  strict `response_format: json_schema` — but even that is imperfect;
  re-test the prompt under the new model before trusting it.

## Cross-references

- [prompts](prompts.md) — the full API call pattern
  > System Prompt · API Call Pattern · JSON Repair
- [TECH-json-repair-recipe](TECH-json-repair-recipe.md) — downstream repair if parsing still
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  fails
- [TECH-stage1-graph-validation](TECH-stage1-graph-validation.md) — structural validation after parse
  > What it does · When to use · How it works · 1 Layer count · 2 Node count · 3 Layer balance · 4 Node label quality · 5 Edge integrity · 6 ID integrity · 7 Layer order sequence · Minimal example · Gotchas · Cross-references
- [TECH-graph-json-schema](TECH-graph-json-schema.md) — the target schema
  > What it does · When to use · How it works · Constraints · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
