---
name: amw-design-md-emit-companions
description: "Emit companion files from an existing Variant 1 DESIGN.md — tokens.css (CSS custom properties), tokens.json (W3C Design Tokens), component-inventory.md (per-component variant table), and usage-prompt.md (a copy-paste-ready prompt for downstream agents). Pure-Python, no remote calls."
---

# /amw-design-md-emit-companions

Emit a family of companion files from a canonical DESIGN.md so downstream tooling (CSS pipelines, Figma exports, agent prompts) can consume the design tokens without re-parsing the markdown.

## Arguments

`$ARGUMENTS` may contain:

- `<path-to-DESIGN.md>` — required (default: `./DESIGN.md`)
- `--targets <list>` — comma-separated subset of `css,json,inventory,prompt` (default: all four)
- `--out-dir <dir>` — output directory (default: directory of the input DESIGN.md)
- `--no-lint` — skip the pre-emit lint check (default: lint runs first)

If no path is provided, default to `./DESIGN.md`.

## Action

### 1. Lint gate (default)

Unless `--no-lint` was passed:

```bash
bash bin/amw-design-md-lint.sh "<input>"
```

If lint fails, surface the errors and stop. Companions derived from a broken DESIGN.md propagate the breakage.

### 2. Run the emitter

```bash
python3 bin/amw-design-md-emit-companions.py "<input>" \
  --targets "<list>" \
  --out-dir "<out-dir>"
```

The script emits the requested files:

- **`tokens.css`** — `:root { --primary: #...; --primary-foreground: #...; ... }` block. Pulls every color, typography, rounded, and spacing token from the YAML frontmatter.
- **`tokens.json`** — W3C Design Tokens spec format. Single combined file covering all token categories (colors, typography, rounded, spacing).
- **`component-inventory.md`** — per-component variant table. Reads `components:` frontmatter and emits a markdown table of `Component | Variant | Properties | Notes`.
- **`usage-prompt.md`** — a copy-paste-ready agent prompt: "You are building a UI that uses this design system. The tokens are: ... Always reference tokens by name; never hard-code values." Useful for non-AI-MAESTRO contexts (Cursor, Codex, plain Claude API).

### 3. Surface the result

- List of emitted file paths
- Total token count per category
- Any tokens skipped (e.g., `# TODO:` placeholders in the source — these do not become CSS vars)

## Non-negotiables

- **Lint gate is mandatory** by default. Override with `--no-lint` only when the user has already lint-checked manually.
- **Companions are derived, not authoritative.** The DESIGN.md is the source of truth; regenerate companions whenever the DESIGN.md changes.
- **Idempotent.** Re-running with the same args overwrites the companions without modifying the source DESIGN.md.

## Failure modes

- DESIGN.md fails lint → surface errors and stop. Recommend `/amw-design-md-lint` for a focused fix loop or `/amw-design-md-audit` for deeper diagnosis.
- `--targets` includes an unknown target → surface error listing valid targets and stop.
- Output directory is not writable → surface error and stop.

## Cross-references

- [TECH-12-companion-files](skills/amw-design-md/references/TECH-12-companion-files.md)
- `bin/amw-design-md-emit-companions.py`
- `bin/amw-design-md-lint.sh`
