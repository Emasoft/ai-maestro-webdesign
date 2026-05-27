---
name: TECH-18-figma-input-path
category: extraction
source: tokens-studio/figma-plugin (MIT), agents/amw-design-md-extractor-agent.md, TECH-16-figma-tokens-bridge.md
also-in: TECH-07-url-extraction.md, TECH-08-codebase-extraction.md, TECH-16-figma-tokens-bridge.md
status: stable
---

# TECH: Figma input path — Tokens Studio JSON → DESIGN.md

## Table of Contents

- [What it does](#what-it-does)
- [Why a dedicated Figma input path](#why-a-dedicated-figma-input-path)
- [Two supported workflows](#two-supported-workflows)
  - [Workflow A — Tokens Studio export from Figma](#workflow-a-tokens-studio-export-from-figma)
  - [Workflow B — Local styles export via Figma plugin](#workflow-b-local-styles-export-via-figma-plugin)
- [Pre-flight checklist for the user](#pre-flight-checklist-for-the-user)
- [Mapping coverage table](#mapping-coverage-table)
- [Lossy surface — what does NOT round-trip](#lossy-surface-what-does-not-round-trip)
- [Failure paths](#failure-paths)
- [Cross-references](#cross-references)

## What it does

Documents the two supported paths for getting a Figma design-system file into the plugin's DESIGN.md format. Both paths are pure-local: no Figma API key, no remote calls, no headless browser. The user runs an open-source Figma plugin once inside Figma Desktop, exports JSON, then passes that JSON to `bin/amw-figma-tokens-import.py` (existing — see [TECH-16-figma-tokens-bridge](TECH-16-figma-tokens-bridge.md)).

This TECH supplies the **user-facing instructions and pre-flight checks**. The actual bin script and its CLI surface are documented in TECH-16.

## Why a dedicated Figma input path

The plugin's six peer input formats (per the user-guidance principle in [TECH-15-design-md-as-input](TECH-15-design-md-as-input.md)) do not include a native "open a `.fig` file" route — Figma's binary format is proprietary, undocumented at the bytecode level, and gated by a paid API for programmatic read access. Importing a Figma source-of-truth therefore requires the user to first **emit a portable artifact** from Figma — that artifact is the open-source Tokens Studio JSON (MIT-licensed plugin) or the equivalent local-styles JSON from any other open-source exporter.

Closes the CLAUDE.md-flagged gap: previously the only ways into DESIGN.md were prose, URL, Tailwind config, codebase scan, or hand-authoring. Figma designs were left out unless the user transcribed by hand.

## Two supported workflows

### Workflow A — Tokens Studio export from Figma

`Tokens Studio for Figma` (https://github.com/tokens-studio/figma-plugin, MIT) is the de-facto community plugin for token authoring in Figma. It maintains a token tree synchronized with Figma styles and variable collections, and exports the tree as JSON.

User-side steps:

1. Install **Tokens Studio for Figma** from the Figma Community page.
2. Open the design file in Figma Desktop.
3. Open the plugin (`Plugins → Tokens Studio for Figma`).
4. Tap *Export*; select either *Single file* (one JSON) or *Multi-file* (one JSON per token set).
5. Save the exported JSON locally — e.g. `~/Downloads/my-system.tokens.json`.
6. Hand the path to the agent: *"Build a DESIGN.md from this Tokens Studio export: `~/Downloads/my-system.tokens.json`"*.

Agent-side steps:

```bash
bin/amw-figma-tokens-import.py ~/Downloads/my-system.tokens.json \
  -o DESIGN.md \
  --name "My System"
```

The importer auto-detects classic vs DTCG shape and single- vs multi-set wrappers. For multi-set files the default merges in `tokenSetOrder` order; pass `--set <name>` to pick exactly one. See [TECH-16-figma-tokens-bridge](TECH-16-figma-tokens-bridge.md) for the full CLI surface, mapping table, and round-trip stability contract.

### Workflow B — Local styles export via Figma plugin

If the user does NOT use Tokens Studio but maintains Figma **local styles** (color styles, text styles, effect styles) and **variable collections** (Figma's native v2 token surface), they can use any open-source exporter that emits compatible JSON. Two MIT-licensed options:

- `figma-tokens-cli` (https://github.com/lukasoppermann/style-dictionary-utils — MIT, ESM) emits Tokens Studio-compatible JSON from a Figma file via the official Figma REST API (requires a personal access token — local to the user, never sent to the plugin).
- A user-written Figma plugin that walks `figma.getLocalPaintStyles()` / `figma.getLocalTextStyles()` / `figma.variables.getLocalVariableCollections()` and posts the result through `figma.ui.postMessage` for download. Boilerplate at https://github.com/figma/plugin-samples (MIT).

User-side steps:

1. Pick an open-source exporter (Tokens Studio is the recommended default — Workflow A above).
2. Configure it to emit Tokens Studio JSON shape (classic `value`/`type` or DTCG `$value`/`$type` — `bin/amw-figma-tokens-import.py` accepts both).
3. Save the exported JSON locally.
4. Hand the path to the agent (same as Workflow A step 6).

Agent-side steps: identical to Workflow A.

## Pre-flight checklist for the user

Before the agent runs `amw-figma-tokens-import.py`, verify with the user:

| Check | Why it matters |
|---|---|
| Did you export from Tokens Studio v1.x or v2.x? | Both work — both shapes are accepted. |
| Did you choose Single-file or Multi-file export? | Single is preferred. Multi means the agent passes `--set` for each leg. |
| Does the JSON contain `boxShadow` tokens? | DESIGN.md has no shadow frontmatter (see TECH-16 lossy table). Document elevation in prose. |
| Does the JSON contain gradient color tokens? | DESIGN.md keeps the first stop's hex. Document the gradient in prose. |
| Does the JSON contain `$themes` matrix (light / dark)? | DESIGN.md has no theme toggle. Pick one theme via `--set <theme>`, or accept later-set-wins merge. |
| Does the JSON contain alias refs `{colors.primary}`? | Resolved eagerly on import — the emitted DESIGN.md has concrete values, not refs. |
| Did the user include the brand name / system name? | Pass via `--name "<title>"`; otherwise derived from the input filename. |

After import, run the standard three-step validation chain (see [TECH-11-validation-and-lint](TECH-11-validation-and-lint.md)):

```bash
bin/amw-design-md-lint.sh DESIGN.md
bin/amw-design-md-validate.py DESIGN.md
bin/amw-design-md-contrast.py DESIGN.md
```

## Mapping coverage table

The full DESIGN.md slot ↔ Tokens Studio group mapping lives in [TECH-16-figma-tokens-bridge](TECH-16-figma-tokens-bridge.md) under "Schema mapping". A condensed view for quick reference:

| DESIGN.md slot | Tokens Studio group | Coverage |
|---|---|---|
| `colors.{primary,secondary,tertiary,neutral,surface,on-surface,error}` | `colors.{slot}` | full |
| `typography.<slot>` | composite `typography` | full (fontFamily, size, weight, lineHeight, letterSpacing) |
| `spacing.<slot>` | `spacing.<slot>` | full (px values) |
| `rounded.<slot>` | `borderRadius.<slot>` | full (px values) |
| `components.<name>.*` | `components.<name>.*` | export-only (importer cannot infer per-component tokens from flat groups) |
| (none) | `boxShadow.*` | DROPPED (no DESIGN.md frontmatter slot) |
| (none) | `gradient stops 2..N` | DROPPED (first stop hex only) |
| (none) | `$themes` matrix | one theme picked via `--set`, or merged later-set-wins |

## Lossy surface — what does NOT round-trip

The Figma → DESIGN.md → Figma round-trip is lossy-but-equivalent for the canonical token surface (see TECH-16's "Round-trip lossiness contract" table). The following Figma constructs do NOT survive a round-trip and MUST be re-authored in DESIGN.md prose:

- **Effect styles** (drop shadows, inner shadows, blurs) — re-author `## Elevation & Depth` in the DESIGN.md body.
- **Gradient fills** — keep the first stop's hex as a token; document the gradient in prose (e.g. *"Buttons use a 135° linear gradient from `--color-primary` to `--color-tertiary`"*).
- **Component variants** (Figma's variant matrix) — represent each variant explicitly in the DESIGN.md `components.<name>.<variant>` block. The importer cannot infer the variant axes from flat token paths.
- **Auto-layout constraints** — DESIGN.md has no Auto Layout schema; document spacing and direction in prose under the relevant component.
- **Component property defs** — same as variants; per-property DESIGN.md component tokens are export-only.

## Failure paths

| Failure | Cause | Recovery |
|---|---|---|
| `amw-figma-tokens-import.py` exits 1 | Tokens Studio JSON is malformed or has an unsupported wrapper | Re-export from Tokens Studio with a clean save; verify the JSON is a top-level object with at least one set. |
| `amw-figma-tokens-import.py` exits 2 | Bad invocation (file not found, unreadable) | Check file path; ensure read permissions. |
| Importer produces a DESIGN.md but `amw-design-md-lint.sh` fails | The JSON had a slot the importer mapped imperfectly (e.g. a `color` token whose value was a CSS function) | Open the emitted DESIGN.md, hand-fix the offending field, re-lint. The importer is best-effort: hand fixup is expected on edge cases. |
| Contrast pre-flight (`amw-design-md-contrast.py`) reports < 4.5:1 pairs | The Figma palette was authored without WCAG-AA discipline | Edit the offending hex in DESIGN.md, document the deviation in `warnings`, or escalate to the user. |
| Multi-set merge produced surprising overrides | `tokenSetOrder` last-set-wins is not what the user expected | Re-run with `--set <name>` for a single set; document the chosen set in `warnings`. |

## License and attribution

The Tokens Studio for Figma plugin is MIT-licensed. The user runs it locally inside their Figma Desktop install; the plugin emits JSON that is the user's own data (their token names, hexes, font picks, etc.). The bridge script `bin/amw-figma-tokens-import.py` consumes that JSON but ships no Tokens Studio code, no Tokens Studio assets, and no copy of the plugin source. License compliance is at the user-tooling layer, not the plugin layer.

If the user employs a different open-source exporter (Workflow B), the same principle applies — their exporter, their license obligations, their data. The plugin's only contract is "accept Tokens Studio JSON shape (classic or DTCG)".

When committing or sharing the resulting DESIGN.md, the user should preserve Figma source attribution in the file's body — e.g. *"Tokens imported from `<design>.fig` via Tokens Studio v1.x on 2026-05-27"*. This is the same provenance convention used by [TECH-07-url-extraction](TECH-07-url-extraction.md) and [TECH-08-codebase-extraction](TECH-08-codebase-extraction.md).

## Cross-references

- [TECH-16-figma-tokens-bridge](./TECH-16-figma-tokens-bridge.md) — bidirectional Tokens Studio ↔ DESIGN.md schema mapping, full CLI surface, round-trip stability table
- [TECH-07-url-extraction](./TECH-07-url-extraction.md) — alternative extraction path (live URL → DESIGN.md)
- [TECH-08-codebase-extraction](./TECH-08-codebase-extraction.md) — alternative extraction path (codebase scan → DESIGN.md)
- [TECH-10-tailwind-conversion](./TECH-10-tailwind-conversion.md) — alternative extraction path (Tailwind config → DESIGN.md)
- [TECH-11-validation-and-lint](./TECH-11-validation-and-lint.md) — the post-import validation chain
- [TECH-15-design-md-as-input](./TECH-15-design-md-as-input.md) — how the imported DESIGN.md is consumed by wireframe-builder
- [TECH-17-dtcg-export](./TECH-17-dtcg-export.md) — round-trip the imported DESIGN.md back out as canonical DTCG JSON
- [TECH-19-design-md-apply](./TECH-19-design-md-apply.md) — token-enforcement during HTML synthesis
- [TECH-20-design-library](./TECH-20-design-library.md) — saving the imported DESIGN.md to the cross-project library
- Tokens Studio for Figma (MIT): <https://github.com/tokens-studio/figma-plugin>
- Figma plugin samples (MIT): <https://github.com/figma/plugin-samples>
