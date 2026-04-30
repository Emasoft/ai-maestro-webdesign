---
name: amw-design-md-from-tailwind
description: "Convert a Tailwind config + globals.css pair into a Variant 1 DESIGN.md. Pure-local Node port of tailwind-to-design-md (no remote calls). Resolves CSS-var references, walks theme.extend.colors / typography / spacing / borderRadius, and annotates color pairs with WCAG-AA contrast. Spawns amw-design-md-extractor-agent (input_type=tailwind)."
---

# /amw-design-md-from-tailwind

Read a Tailwind v3 or v4 config plus its companion `globals.css` (with `@theme` block or `:root` overrides) and emit a Variant 1 DESIGN.md whose frontmatter mirrors the resolved theme exactly. Pure-local — no API key, no remote calls.

## Arguments

`$ARGUMENTS` should contain at minimum the config path and the css path:

- `<tailwind.config.{ts,js,mjs}> <globals.css> [--out <path>] [--companions <list>] [--no-contrast]`

If both paths are not provided, ask: *"Pass the Tailwind config and globals.css paths."* and stop.

Optional flags:

- `--out <path>` — output DESIGN.md path (default: `./DESIGN.md`)
- `--companions css,json,inventory,prompt` — emit companion files
- `--no-contrast` — skip the WCAG contrast check

## Action

### 1. Prerequisite check

Confirm `node` ≥18 is on PATH. The extractor uses `bin/amw-design-md-from-tailwind.mjs` (Node ESM port).

### 2. Spawn `amw-design-md-extractor-agent`

Pass:

```yaml
input_type: "tailwind"
tailwind_config_path: "<arg-1>"
globals_css_path: "<arg-2>"
output_path: "<--out value or ./DESIGN.md>"
companion_targets: ["<list>"]
contrast_check: true | false
strict_lint: true
```

The agent runs `bin/amw-design-md-from-tailwind.mjs`, then the lint gate and contrast check.

### 3. Surface the result

After the agent returns:

- DESIGN.md path
- Tailwind detection log (v3 vs v4, theme key coverage)
- Lint status
- Contrast warnings, if any
- Companion file paths

If the config uses dynamic features the static evaluator cannot resolve (Zod schemas, dynamic `require()`, env-dependent values), the agent returns `status=partial` with a request for a fully static config — surface and stop.

## Non-negotiables

- **Pure-local evaluation.** No remote API calls; no Tailwind Play CDN.
- **Static evaluation only.** Dynamic configs must be flattened first.
- **CSS-var overrides win** over the corresponding Tailwind theme value when both define the same token (override is what actually renders).
- **Lint gate is mandatory.**

## Failure modes

- Config cannot be statically evaluated → agent returns `status=partial`; surface request for static config.
- `globals.css` references a CSS var the config does not define → emit `# TODO: resolve <var>` in DESIGN.md and add a warning.
- Tailwind config + CSS file disagree on a token → CSS override wins; conflict is logged in `warnings`.

## Cross-references

- `agents/amw-design-md-extractor-agent.md`
- `skills/amw-design-md/references/TECH-10-tailwind-conversion.md`
- `bin/amw-design-md-from-tailwind.mjs` (Node port — the live implementation)
- `bin/amw-design-md-lint.sh`
- `bin/amw-design-md-contrast.py`
