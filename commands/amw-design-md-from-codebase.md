---
name: amw-design-md-from-codebase
description: "Scan a project tree for Tailwind / shadcn / Chakra / vanilla-CSS / styled-components signals and emit a Variant 1 DESIGN.md whose frontmatter reflects the dominant style system. Pure-Python scanner (no remote calls). Spawns amw-design-md-extractor-agent (input_type=codebase)."
---

# /amw-design-md-from-codebase

Walk a codebase, detect its primary style system, and emit a Variant 1 DESIGN.md whose frontmatter mirrors the actual tokens in use. Pure-local Python scanner.

## Arguments

`$ARGUMENTS` may contain:

- A directory path: `./` or `~/projects/foo` (default: current working directory)
- `--out <path>` — output DESIGN.md path (default: `./DESIGN.md`)
- `--companions css,json,inventory,prompt` — emit companion files
- `--no-contrast` — skip the WCAG contrast check
- `--prefer-stack {tailwind,shadcn,chakra,vanilla,styled-components}` — when the scanner sees multiple stacks, force this one as primary

If no path is provided, default to the current working directory.

## Action

### 1. Prerequisite check

Confirm `python3` ≥3.8 is on PATH. The scanner uses `bin/amw-design-md-from-codebase.py`.

### 2. Spawn `amw-design-md-extractor-agent`

Pass:

```yaml
input_type: "codebase"
codebase_path: "<arg-1 or cwd>"
output_path: "<--out value or ./DESIGN.md>"
companion_targets: ["<list>"]
contrast_check: true | false
strict_lint: true
prefer_stack: "<value or null>"
```

The agent runs `bin/amw-design-md-from-codebase.py`, then the lint gate and contrast check.

### 3. Surface the result

After the agent returns:

- DESIGN.md path + sidecar `<DESIGN.md>.extraction-notes.md` (primary-stack detection, class-frequency table, Tailwind config evaluation log)
- Detected primary stack and any secondary stacks ignored
- Lint status
- Contrast warnings, if any
- Companion file paths

If extraction-notes flags multiple competing stacks, recommend re-running with `--prefer-stack` to override the auto-detection.

## Non-negotiables

- **Pure-local scanning.** No remote calls; no upload of the codebase.
- **Faithful transcription.** Tokens absent from the source remain `# TODO:` in the output — they are never invented.
- **Lint gate is mandatory.**

## Failure modes

- No detectable style system → minimal DESIGN.md with all-`# TODO:` frontmatter; `confidence=low`. Recommend running `/amw-design-md-create` interactively instead.
- Multiple competing stacks → primary-stack rule applies; user can override via `--prefer-stack`.
- Codebase too large (>5000 files matching style extensions) → scanner pages internally; no extra action needed.

## Cross-references

- [amw-design-md-extractor-agent](agents/amw-design-md-extractor-agent.md)
- [TECH-08-codebase-extraction](skills/amw-design-md/references/TECH-08-codebase-extraction.md)
- `bin/amw-design-md-from-codebase.py`
- `bin/amw-design-md-lint.sh`
- `bin/amw-design-md-contrast.py`
