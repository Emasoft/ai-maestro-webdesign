---
name: amw-doctor
description: "Shortcut for users who want a quick dependency status report for the plugin runtime — prints a table of installed/missing tools. An agent in Main-agent mode may also run the same dependency checks inline as part of a broader Phase B pre-flight before spawning sub-agents."
---

# /amw-doctor

Inspect the local environment for every binary and package the plugin needs and print a concise status table. This command **never installs** — it only reports. For installation, the user runs `/amw-init`.

## Action

Run the following checks in parallel where possible, collect the results, and print a single markdown table at the end.

### 1. System-required (user's responsibility)

| Tool | Check | Minimum |
|---|---|---|
| node | `node --version` | v22.0.0 |
| git | `git --version` | any |
| python3 | `python3 --version` | 3.8.0 (also required for `bin/amw-validate-ascii.py` — the Windows-friendly Python port of the Perl validator) |
| perl | `perl --version \| head -2 \| tail -1` | 5.10 (for `bin/amw-validate-ascii.pl`) — optional if `python3` is available and callers use `bin/amw-validate-ascii.py` instead |

### 2. Installed at runtime by `/amw-init`

| Tool | Check | Notes |
|---|---|---|
| bun | `bun --version` | Used by hyperframes-bridge |
| ffmpeg | `ffmpeg -version` | Used by hyperframes-bridge |
| dev-browser CLI | `dev-browser --version` | The plugin's only browser-automation primitive |
| dev-browser Chromium | `dev-browser --help 2>&1 \| grep -q install && echo present \|\| echo unknown` | Installed via `dev-browser install` |
| Playwright | `python3 -c "import playwright; print(playwright.__version__)"` | Used by infographics (`infographics/scripts/export.py`) only — NOT used by hyperframes |
| Playwright Chromium | `python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(); b.close(); p.stop(); print('ok')" 2>&1 \| tail -1` | For infographics only |
| Hyperframes Chrome | `(cd external/hyperframes && npx hyperframes browser ensure) 2>&1 \| tail -3` | Hyperframes uses Puppeteer + `@puppeteer/browsers` (NOT Playwright) to manage its own Chrome binary. Run `(cd external/hyperframes && npx hyperframes browser ensure)` to provision. |
| CairoSVG | `python3 -c "import cairosvg; print(cairosvg.__version__)"` | Used by svg-creator, ascii-to-svg |
| Mermaid wrapper | `bin/amw-mermaid-render.sh --version` | Wrapper script presence only — does NOT validate the npm dep. Actual dependency validated by the `beautiful-mermaid` row below. |
| beautiful-mermaid | `test -d external/mermaid-render/node_modules/beautiful-mermaid && echo installed \|\| echo missing` | Installed by `/amw-init` step 7 or lazy on first render via `bin/amw-mermaid-render.sh` |
| xmllint | `xmllint --version 2>&1 \| head -1` | Used by SVG + HTML diagram validators (`bin/amw-validate-svg-diagram.sh`, `bin/amw-validate-html-diagram.sh`). Usually pre-installed on macOS/Linux via libxml2. |
| tidy (HTML Tidy) | `tidy -version 2>&1 \| head -1` | Used by `bin/amw-validate-html-diagram.sh` alongside xmllint. Optional — wrapper degrades gracefully when absent, but `/amw-init` installs it. |
| mmdc (mermaid-cli) | `mmdc --version` | Used by `bin/amw-mermaid-lint.sh` + `bin/amw-mermaid-render.sh`. Installed globally by `/amw-init` via `npm i -g @mermaid-js/mermaid-cli`. |
| lxml (Python) | `python3 -c "import lxml; print(lxml.__version__)" 2>/dev/null \|\| echo missing` | Optional — used by Phase 1 HTML/SVG parsers. Install via `uv pip install lxml`. |
| beautifulsoup4 (Python) | `python3 -c "import bs4; print(bs4.__version__)" 2>/dev/null \|\| echo missing` | Optional — used by Phase 1 HTML parser. Install via `uv pip install beautifulsoup4`. |

### 3. Optional npm tools + env vars

| Tool / Env | Check | Notes |
|---|---|---|
| designlang | `npx --no-install designlang --version 2>/dev/null \|\| echo missing` | Used by design-extract |
| `ANTHROPIC_API_KEY` | `[ -n "$ANTHROPIC_API_KEY" ] && echo set \|\| echo unset` | Used by `diagram-architecture` when running standalone. NOT required when invoked inside Claude Code (platform supplies it). |
| `GEMINI_API_KEY` | `[ -n "$GEMINI_API_KEY" ] && echo set \|\| echo unset` | Required by `excalidraw-illustrations`. Get one from https://aistudio.google.com/. Every Gemini call is billed to the user's own Google account. Unset is fine if the user does not plan to generate hand-drawn illustrations. |
| Pillow (optional) | `python3 -c "import PIL; print(PIL.__version__)" 2>/dev/null \|\| echo missing` | Optional — only needed by `excalidraw-illustrations` two-phase text-overlay fallback (`scripts/generate.py`). Install via `/amw-init` Section 7. |

### 4. Hyperframes version check

If `external/hyperframes/` is present, read the CLI package version and soft-warn if it is below 0.4.30. This is informational — do not fail the doctor run.

```bash
if [ -f "external/hyperframes/packages/cli/package.json" ]; then
  hf_version=$(node -p "require('./external/hyperframes/packages/cli/package.json').version" 2>/dev/null)
  if [ -z "$hf_version" ]; then
    echo "hyperframes version could not be determined"
  elif [ "$(printf '%s\n' "$hf_version" "0.4.30" | sort -V | head -n1)" = "0.4.30" ]; then
    echo "hyperframes v$hf_version OK"
  else
    echo "WARN: hyperframes v$hf_version < 0.4.30 — inspect, --hdr, data-variable-values require ≥0.4.30"
  fi
fi
```

Include the result in the doctor table as a `Hyperframes version` row under the `Plugin` category. Use `OK` (green) for ≥0.4.30, `WARN` (yellow) for older versions (do not use `MISSING` or `FAIL`).

### 5. Plugin file presence

Check that these paths exist (use `test -e`):

- `.claude-plugin/plugin.json`
- `skills/amw-design-principles/SKILL.md`
- `skills/amw-diagram-formats/SKILL.md` (Phase 0 — shared references meta-skill)
- `skills/amw-diagram-formats/schema.json` (IR JSON schema)
- `bin/amw-svg-render.py`
- `bin/amw-html-export.py`
- `bin/amw-ascii-render.py`
- `bin/amw-validate-ascii.pl` (Perl validator — primary)
- `bin/amw-validate-ascii.py` (Python port — Windows-friendly, group-aware width detection)
- `bin/amw-mermaid-render.sh`
- `bin/amw-diagram-ir.py` (Phase 0 — IR parser / emitter / validator / diff)
- `bin/amw-diagram-detect-format.sh` (Phase 0 — format sniffer)
- `bin/amw-validate-diagram.sh` (Phase 0 — top-level validator dispatcher)
- `bin/amw-validate-html-diagram.sh` (Phase 0 — HTML validator; wraps xmllint + tidy)
- `bin/amw-validate-svg-diagram.sh` (Phase 0 — SVG validator; wraps xmllint + namespace check)
- `bin/amw-mermaid-lint.sh` (Phase 0 — Mermaid grammar linter; wraps mmdc)
- `external/hyperframes/` (mark as "pending" if absent)
- `external/mermaid-render/package.json` (mark as "pending" if absent — fix: run `/amw-init` step 7)

## Output format

Produce a single table:

```
| Category | Tool | Status | Version | Fix |
|---|---|---|---|---|
| System | node | OK | v22.3.0 | — |
| System | python3 | OK | 3.12.4 | — |
| Runtime | bun | MISSING | — | /amw-init |
| Runtime | dev-browser | MISSING | — | /amw-init |
...
```

Finish with a one-line verdict: `✅ all green` or `⚠️ N missing — run /amw-init to install`.

## Exit behavior

This command is idempotent and read-only. It never modifies the filesystem, never writes config, never touches `~/.zshrc` or `~/.bashrc`.
