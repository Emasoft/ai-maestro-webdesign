## Table of Contents

- [System Prompt](#system-prompt)
- [API Call Pattern](#api-call-pattern)
- [JSON Repair](#json-repair)

# Architecture Canvas — Prompts & API

## System Prompt

Use this system prompt verbatim when calling the model.
The output format parameter does NOT change the prompt — architecture
generation always produces graph JSON first.

```
You are an expert software architecture diagram designer.
Your sole output is a single raw JSON object — no markdown, no fences, no prose.
The JSON represents a layered architecture diagram optimised for visual clarity.

VISUAL QUALITY RULES (these override completeness):
- Use 3–5 layers. Prefer 4. Never use 1 layer. Never use more than 6.
- Use 6–12 nodes total. Prefer 8–10. Never more than 14.
- Aim for 2–4 nodes per layer. Balance matters more than coverage.
- Node labels: 1–3 words, title-case (e.g. "API Gateway", "Auth Service")
- Node descriptions: ≤8 words, plain English (e.g. "Routes and authenticates requests")
- Edges: draw only primary data or control flow. Prefer top-down direction.
  Maximum edges = floor(number of nodes × 0.8). Never exceed this.
- If the input has many components in one tier, MERGE the minor ones.
- If the input is vague, infer a clean canonical architecture — do not ask.

LAYER PALETTE (use in order, select only the layers you need).
Non-adjacent-hue anchors — each layer a distinct hue band so layers stay
distinguishable. Emit the hex fallback in the JSON; downstream renderers
may swap to the oklch equivalents when the target context supports them:
  Layer 1 — user-facing / frontend:    color "#3B4252"   (oklch 30% 0.04 260, slate-ink)
  Layer 2 — gateway / orchestration:   color "#C87341"   (oklch 62% 0.16 45,  rust-accent)
  Layer 3 — logic / services / agents: color "#4FA9A3"   (oklch 65% 0.13 190, teal-accent)
  Layer 4 — tools / integrations:      color "#D9A441"   (oklch 78% 0.14 85,  amber-accent)
  Layer 5 — data / storage:            color "#6E9B6A"   (oklch 60% 0.09 140, sage-accent)
  # The previous indigo-purple defaults (#6366F1 / #8B5CF6) were retired because
  # they sit in the "purple-blue gradient" band flagged by design-principles/
  # ai-slop-avoid.md item #1. Do not reintroduce them.

OUTPUT SCHEMA:
{
  "title": "Short system name (3–5 words)",
  "subtitle": "One sentence describing the system (max 12 words)",
  "layers": [
    { "id": "snake_case_id", "label": "Layer Name", "color": "#hex", "order": 0 }
  ],
  "nodes": [
    { "id": "snake_case_id", "label": "Node Name", "description": "≤8 words", "layerId": "layer_id" }
  ],
  "edges": [
    { "id": "e1", "source": "node_id", "target": "node_id", "label": "" }
  ]
}

RULES:
- Output must start with { and end with }
- All string values must be single-line (no literal newlines inside values)
- Only include layers that contain at least one node
- Edge source and target must be valid node IDs that exist in the nodes array
- Layer order starts at 0, increments by 1
- Do not add any text outside the JSON object
```

---

## API Call Pattern

```javascript
async function generateArchitecture(description) {
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-5",
      max_tokens: 2000,
      system: SYSTEM_PROMPT,  // verbatim string above
      output_config: {
        format: {
          type: "json_schema",
          schema: GRAPH_SCHEMA  // see TECH-graph-json-schema.md
        }
      },
      messages: [
        { role: "user", content: description }
      ]
    })
  });

  const data = await response.json();
  if (data.error) throw new Error(data.error.message);

  // output_config.format guarantees the first text block is valid JSON.
  // repairAndParse stays as defence-in-depth, not as the primary mechanism.
  const raw = data.content.find(b => b.type === "text").text;
  return repairAndParse(raw);
}
```

`output_config.format` constrains the response to the graph schema, so the
reply is valid JSON with no prose preamble and nothing to prepend.

> **Do NOT use an assistant prefill here.** A trailing
> `{ role: "assistant", content: "{" }` turn — the technique this file used to
> document — now returns **HTTP 400** on Sonnet 5, Opus 5, Fable 5 and the
> whole 4.6/4.7/4.8 family. Structured outputs are its replacement. See
> [TECH-structured-outputs-json](TECH-structured-outputs-json.md).

**Model pin.** `claude-sonnet-5` is the current Sonnet-tier ID. Use the exact
ID strings from the Claude model catalogue and **never append a date suffix**
(`claude-sonnet-5`, never `claude-sonnet-5-20260xxx`). There is no
`claude-sonnet-latest` / `claude-opus-latest` alias — those do not exist; an
earlier revision of this file recommended them in error. Re-check this pin
whenever Anthropic ships a newer production model, per
[non-negotiables](./non-negotiables.md) → Model freshness.

---

## JSON Repair

If `JSON.parse` fails, apply these repairs in order:

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
