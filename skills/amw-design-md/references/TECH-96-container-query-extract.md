# TECH-96: Container query + intrinsic-breakpoint extraction

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Architecture](#architecture)
- [What dev-browser captures](#what-dev-browser-captures)
- [Container-name catalog](#container-name-catalog)
- [Breakpoint extraction](#breakpoint-extraction)
- [Intrinsic-size detection](#intrinsic-size-detection)
- [Output schema](#output-schema)
- [Interaction with viewport media queries](#interaction-with-viewport-media-queries)
- [Worked example](#worked-example)
- [Failure modes](#failure-modes)
- [Cross-references](#cross-references)

## What it does

Documents how `amw-design-md-extractor-agent` reads `@container` rules and `container-type` / `container-name` declarations from a live URL, derives the **per-container breakpoint contract**, and emits a `containers.{name}` block under `extensions.containers` in the DESIGN.md frontmatter.

Container queries are a recent CSS feature (Baseline 2023). When a site uses them, the design system has TWO breakpoint surfaces:

1. **Viewport breakpoints** — global, captured by [TECH-07-url-extraction](TECH-07-url-extraction.md) under `spacing` / Tailwind config.
2. **Container breakpoints** — local to a component, captured by this TECH.

Mixing them blindly produces an incorrect breakpoint scale. This TECH separates them and documents each.

## When to use

- User says: "extract DESIGN.md from <URL> with the responsive contract"
- User says: "I need to know the breakpoints; the site uses container queries"
- Brand-researcher: extracting from a modern component-library-driven site (post-2023 React / Vue libraries that adopted container queries)

## When NOT to use

- Site uses only viewport-level media queries → [TECH-07-url-extraction](TECH-07-url-extraction.md) captures these; no container-query layer needed
- User explicitly only wants Variant 1 core tokens → skip; do not bloat frontmatter
- Container queries used only for one-off layout (not part of the design system) → record in `warnings`, do not promote to tokens

## Architecture

```
        URL ─────► dev-browser eval ────► JSON snapshot
                                          (matched CSS rules)
                          │
                          ▼
        Scan for `@container` at-rules + `container-type` / `container-name` declarations
                          │
                          ▼
        Group by container-name:
          {name, type (size | inline-size | normal),
           queries: [{condition, properties_changed}],
           intrinsic_size?, owning_selector}
                          │
                          ▼
        Extract breakpoints from each query condition:
          (min-width: 320px) → bp-sm
          (min-width: 640px) → bp-md
          (min-width: 960px) → bp-lg
                          │
                          ▼
        Emit extensions.containers.{name} entries
```

## What dev-browser captures

The extraction extends the standard JSON snapshot with a `containers` array. Container queries require reading stylesheet rules (not just computed styles), so the eval script walks every accessible stylesheet:

```js
function captureContainers() {
  const named = new Map();   // container-name → {type, owning_selectors[]}
  const queries = [];        // every @container at-rule

  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch { continue; }
    if (!rules) continue;
    for (const rule of rules) {
      // 1. Containers declared via container-type / container-name
      if (rule.type === CSSRule.STYLE_RULE) {
        const ct = rule.style.containerType;
        const cn = rule.style.containerName;
        if (ct || cn) {
          const names = (cn || '__anon__').trim().split(/\s+/);
          for (const name of names) {
            if (!named.has(name)) named.set(name, {type: ct || 'normal', selectors: []});
            named.get(name).selectors.push(rule.selectorText);
          }
        }
      }
      // 2. @container at-rules
      if (rule.type === CSSRule.CONTAINER_RULE || rule.cssText?.startsWith('@container')) {
        queries.push({
          name: rule.containerName || '__anon__',
          condition: rule.containerQuery || rule.cssText?.match(/@container[^{]+/)?.[0],
          inner: Array.from(rule.cssRules || []).map(r => r.cssText),
        });
      }
    }
  }
  return { named: Object.fromEntries(named), queries };
}
```

Anonymous containers (no `container-name`) get bucketed under `__anon__` and surfaced separately — they cannot be referenced by `@container <name>` rules, so they form a less-structured layer.

## Container-name catalog

The post-processor groups all captured rules by container-name:

| Container | container-type | Queries observed | Inferred purpose |
|---|---|---|---|
| `card` | `inline-size` | `(min-width: 320px)`, `(min-width: 480px)` | Adaptive card component (header layout, image position) |
| `sidebar` | `inline-size` | `(min-width: 240px)` | Sidebar variant (icons-only vs labeled) |
| `chart` | `size` | `(min-aspect-ratio: 16/9)` | Chart responsive layout |
| `__anon__` | mixed | various | Ad-hoc containers — not part of canonical system |

The classifier suggests "Inferred purpose" by inspecting `owning_selector` patterns (e.g., `.card-container`, `[data-component="card"]`).

## Breakpoint extraction

For each named container, the breakpoints are the set of `min-width` / `max-width` values appearing in its `@container` queries:

```
container: card
  query 1: (min-width: 320px) → render image left-aligned
  query 2: (min-width: 480px) → show metadata row
  query 3: (min-width: 640px) → wide layout
  → breakpoints: [320px, 480px, 640px]
```

The breakpoints become the container's **intrinsic responsive contract**. They are typically NOT the same as the viewport breakpoints (which would be 768/1024/1280 for a Tailwind site).

Duplicates across containers are surfaced as a "shared breakpoint scale" prose note when 2+ containers share the same breakpoint values.

## Intrinsic-size detection

When a container declares both `container-type: size` AND an explicit `width` / `height`, the extractor records the **intrinsic size** alongside the breakpoints:

```yaml
extensions:
  containers:
    chart:
      type: size
      intrinsic_size: "100% × 320px"   # the declared size
      queries:
        - condition: "(min-aspect-ratio: 16/9)"
          purpose: "wide chart layout"
```

This helps consumers of the DESIGN.md understand the design intent — a `size` container with no intrinsic size is unusual and usually a smell.

## Output schema

```yaml
extensions:
  containers:
    card:
      type: inline-size
      breakpoints: ["320px", "480px", "640px"]
      owning_selectors: [".card-container", "[data-component='card']"]
      query-count: 3
      usage: "adaptive card; image position + metadata visibility shift at each breakpoint"
    sidebar:
      type: inline-size
      breakpoints: ["240px"]
      owning_selectors: [".sidebar"]
      query-count: 1
      usage: "icons-only ↔ labeled toggle"
    chart:
      type: size
      breakpoints: ["aspect-ratio 16/9"]
      intrinsic_size: "100% × 320px"
      owning_selectors: [".chart-host"]
      query-count: 1
      usage: "wide ↔ tall chart layout"
  anonymous_containers:
    count: 4
    note: "4 unnamed containers found; not part of canonical system — verify before promotion"
```

## Interaction with viewport media queries

The DESIGN.md should NOT collapse container queries into the viewport breakpoint list. They are different responsive layers:

- `spacing.breakpoints` (existing Variant 1 schema) → viewport breakpoints (320 / 640 / 768 / 1024 / 1280)
- `extensions.containers.{name}.breakpoints` → per-container breakpoints (often 240 / 320 / 480, NOT viewport-aligned)

A component documented in the DESIGN.md as using a container query should reference the container name, not a viewport breakpoint:

```markdown
## Card component

Adaptive across `container: card`. At 320px container width, switches to
horizontal image layout. At 480px, shows the metadata row.
(Independent of viewport width.)
```

## Worked example

Input: a modern documentation site using Radix UI + container queries.

dev-browser captures:
- 3 named containers: `card`, `sidebar`, `code-block`
- 7 `@container` at-rules across them
- 2 anonymous containers (one-off)

Result:
- `card` (3 breakpoints: 320, 480, 640)
- `sidebar` (1 breakpoint: 240)
- `code-block` (2 breakpoints: 480, 800)
- 2 anonymous containers flagged in prose

The extracted DESIGN.md keeps viewport breakpoints from Tailwind config (TECH-10) intact AND adds the `extensions.containers` block — both responsive surfaces are now documented.

## Failure modes

| Failure | Cause | Recovery |
|---|---|---|
| Site uses no container queries | Older site / Tailwind-only | Return empty `extensions.containers: {}` + prose note; do NOT promote viewport breakpoints into this slot |
| CORS blocks stylesheets | Cross-origin CSS | Capture available rules; record skipped sheets in `warnings` |
| Container-name omitted everywhere | Anonymous container-only usage | Bucket under `__anon__`; surface as "containers used but not named" warning; consumers cannot reference them |
| `container-type: normal` (i.e., no containment) | Misconfiguration | Skip; record in `warnings` — containers without a containment context cannot be queried |
| Aspect-ratio queries on `inline-size` container | Invalid CSS combination | Capture as-is; flag invalid combination in `warnings` |
| 50+ unique container names | Container queries used for one-off layout, not the design system | Cluster by selector pattern; surface only the top N (default 10) in the DESIGN.md; rest in `warnings` |

## Cross-references

- [TECH-07-url-extraction](./TECH-07-url-extraction.md) — base URL extraction flow (captures viewport breakpoints separately)
  > What it does · When to use · Architecture · Inputs · What `dev-browser eval` returns · Heuristics for token extraction · Colors · Typography · Spacing · Radius · Components · Output structure · Failure modes and recovery · Validation gate · Cross-references
- [TECH-10-tailwind-conversion](./TECH-10-tailwind-conversion.md) — Tailwind viewport breakpoints (the OTHER responsive layer)
- [TECH-86-multi-page-extract](./TECH-86-multi-page-extract.md) — when container usage differs across pages, multi-page merge applies
- [TECH-94-animation-extract](./TECH-94-animation-extract.md) — modern motion sometimes depends on container size; extract together for layered systems
- [extension-sections-10-14](./extension-sections-10-14.md) — where extension namespaces live in Variant 1 DESIGN.md
- `../../../bin/amw-design-md-from-url.sh` — bin script that hosts this classifier
- `../../../bin/amw-dev-browser-wrapper.sh` — browser primitive used internally
- [amw-design-md-extractor-agent](../../../agents/amw-design-md-extractor-agent.md) — the agent that owns this flow
