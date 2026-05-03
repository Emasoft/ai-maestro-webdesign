---
name: TECH-json-repair-recipe
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


# TECH-json-repair-recipe

## What it does

Recovers **valid JSON** from an LLM response that `JSON.parse` rejects,
applying a fixed sequence of lightweight repairs — strip markdown
fences, trim to outermost braces, remove trailing commas, normalise
literal newlines inside string values. The goal is "best-effort parse";
if repair fails after the sequence, surface a clear error rather than
silently shipping garbage.

## When to use

- **Always after the LLM call** — even with assistant prefill, the
  repair step is the safety net.
- **Before Stage 1 validation** — validation assumes a parsed object;
  it can't run on a string.
- **Never before** the LLM call — repair is a post-process only.

## How it works

Five-step fallback chain:

```javascript
function repairAndParse(raw) {
  // 1. Strip accidental markdown fences
  let s = raw.replace(/```(?:json)?\s*/gi, "").replace(/```/g, "").trim();

  // 2. Find outermost { … } bounds
  const a = s.indexOf("{"), b = s.lastIndexOf("}");
  if (a !== -1 && b > a) s = s.slice(a, b + 1);

  // 3. First attempt — clean JSON
  try { return JSON.parse(s); } catch (_) {}

  // 4. Remove trailing commas before ] or }
  s = s.replace(/,\s*([}\]])/g, "$1");

  // 5. Normalise literal newlines inside string values
  s = s.replace(/"([^"\\]*)(?:\\.|[^"\\])*"/g,
    m => m.replace(/\n/g, " ").replace(/\r/g, ""));

  // 6. Second attempt
  try { return JSON.parse(s); } catch (e) {
    throw new Error("JSON repair failed: " + e.message);
  }
}
```

## Minimal example

Broken LLM output:

````
Here's your architecture:

```json
{
  "title": "Analytics",
  "subtitle": "Event-driven analytics
with real-time querying",          ← literal newline inside string
  "layers": [
    { "id": "frontend", "order": 0 },
  ],                                ← trailing comma
  "nodes": []
}
```

Hope this helps!
````

After repair:

```json
{
  "title": "Analytics",
  "subtitle": "Event-driven analytics with real-time querying",
  "layers": [
    { "id": "frontend", "order": 0 }
  ],
  "nodes": []
}
```

The sequence handled:

- Markdown prose stripped (`Here's your architecture:` / `Hope this
  helps!`)
- Markdown fences removed (``` ` ``json` / ``` ``` )
- Literal newline inside subtitle → replaced with space
- Trailing comma after the layer → removed

## Gotchas

- **The regex for step 5 is conservative.** It runs only on string
  values (content between double-quotes); it won't mangle newlines
  inside the JSON structure itself (which would be illegal anyway).
- **Don't skip step 2.** The outermost-braces slice is what handles the
  "prose before and after JSON" case. LLMs very occasionally emit the
  JSON in the middle of prose even with prefill.
- **Trailing commas are the #1 repair case.** Models trained on
  JavaScript-flavored JSON emit trailing commas by habit; the regex fix
  is the cheap bailout.
- **If step 6 still fails, surface the error.** Silent fallback to an
  empty graph produces a "0-layer, 0-node, 0-edge architecture" — which
  then fails Stage 1 validation and triggers re-generation, but you've
  wasted an LLM call. Better to raise and let the caller retry with a
  clearer prompt.
- **Do not attempt AST repair.** Parser-level JSON repair libraries
  exist (e.g. `jsonrepair`); this lightweight regex recipe is preferred
  because it fits in the SKILL.md context and the failure mode is
  obvious — if it can't fix it, the response is too broken to trust.

## Cross-references

- [prompts](prompts.md) — the full API pattern this wraps
  > System Prompt · API Call Pattern · JSON Repair
- [TECH-assistant-prefill-json](TECH-assistant-prefill-json.md) — upstream; reduces how often repair
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
  is needed
- [TECH-stage1-graph-validation](TECH-stage1-graph-validation.md) — downstream; consumes parsed object
  > What it does · When to use · How it works · 1 Layer count · 2 Node count · 3 Layer balance · 4 Node label quality · 5 Edge integrity · 6 ID integrity · 7 Layer order sequence · Minimal example · Gotchas · Cross-references
- [TECH-graph-json-schema](TECH-graph-json-schema.md) — the target schema
  > What it does · When to use · How it works · Constraints · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

