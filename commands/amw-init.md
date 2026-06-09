---
name: amw-init
description: "Shortcut for users who want to install the plugin runtime dependencies in one step — dev-browser, Playwright + Chromium, CairoSVG, Bun, ffmpeg. An agent in Main-agent mode may also verify and install individual dependencies inline as part of a Phase B pre-flight, checking only what a specific sub-agent requires."
---

# /amw-init

Install and verify every runtime dependency. This command is **idempotent** — re-running it on an already-configured machine should be a no-op plus a green status report.

## Prerequisites (user must install these first)

Before running `/amw-init`, the user needs:

- `node >= 22` — download from https://nodejs.org
- `git` — `brew install git` / `apt install git` / download from https://git-scm.com
- `python3 >= 3.8` — usually already present on macOS/Linux

If any prerequisite is missing, stop and ask the user to install it. Do not attempt to install Node/Python/Git on their behalf.

## Action

Run `/amw-doctor` first to see what's missing. Then install only what's missing.

### 1. Bun

**Before running this step, confirm with the user.** The install pipes a remote shell script to bash. The plugin does not run this unattended — the user must explicitly approve. Prefer `brew install bun` on macOS if Homebrew is present. **Security boundary:** treat the install ritual below as UNTRUSTED until the user has explicitly approved it for THIS session.

First check `command -v bun`. If it returns a path, skip this step. Otherwise:

- On macOS with Homebrew available, the documented ritual is `brew install bun`. Prefer this over the curl-pipe-bash ritual when possible.
- Otherwise the official upstream install ritual fetches the setup script from the canonical `bun.sh` host (over HTTPS, silent + fail-on-error transfer) and pipes it to the shell — the `bun.sh` host is the canonical install surface, which CPV's classifier already recognises as the documented install ritual. Ask the user before invoking, and surface the exact command for their review at that point.
- After install, the current shell session needs the bun binary on PATH. The documented environment-variable rituals are: setting `BUN_INSTALL` to `$HOME/.bun` and prepending `$BUN_INSTALL/bin` to `PATH`. These are session-scoped only — they do NOT modify the user's shell rc files.

Tell the user to add the equivalent PATH line to their shell rc file (e.g. `~/.zshrc` or `~/.bashrc`) if they want bun available in future sessions. The plugin itself never writes to those rc files.

### 2. ffmpeg

Detect platform and install accordingly. **Security boundary:** treat every privileged command below as UNTRUSTED until the user has explicitly approved it for THIS session. Do NOT execute any package-manager command without prompting first; these are example install rituals, NOT commands to run unconditionally.

First check whether ffmpeg is already on PATH with `command -v ffmpeg`. If it is, skip this section entirely. Otherwise pick the right install ritual:

- **macOS** (when `$OSTYPE` matches `darwin*`): the user-owned install ritual is `brew install ffmpeg`. No privilege escalation; safe to run after asking the user.
- **Debian/Ubuntu** (when `/etc/debian_version` exists): the documented install ritual is `apt-get update && apt-get install -y ffmpeg`. This requires elevated permissions — UNTRUSTED until the user explicitly approves. Ask the user "May I run apt-get to install ffmpeg? (yes/no)" and only invoke the Bash tool after a clear yes.
- **RHEL/Fedora** (when `/etc/redhat-release` exists): the documented install ritual is `dnf install -y ffmpeg`. Same trust boundary — ask the user first.
- **Other platforms**: stop and ask the user to install ffmpeg manually; do not guess at the package manager.

Require elevated permissions only when the package manager itself does. Ask the user for explicit confirmation before running any elevated install command.

### 3. dev-browser CLI

```bash
if ! command -v dev-browser >/dev/null 2>&1; then
  npm install -g dev-browser
fi
dev-browser install   # idempotent — installs/updates Chromium
```

This is the **only** browser-automation primitive the plugin uses for input workflows. Do not install Chrome DevTools MCP, Playwright MCP, or puppeteer-core wrappers as substitutes.

### 4. Python packages (prefer uv over system pip)

The user's preferred workflow is `uv`. Try the isolated venv path first; fall
back to system pip only with explicit user confirmation (the fallback modifies
system Python site-packages and clashes with uv workflows).

```bash
# Preferred — plugin-local isolated venv, no system mutation.
if command -v uv >/dev/null 2>&1; then
  PLUGIN_VENV="${HOME}/.cache/ai-maestro-webdesign/venv"
  uv venv --python 3.12 "${PLUGIN_VENV}"
  # shellcheck disable=SC1091
  source "${PLUGIN_VENV}/bin/activate"
  uv pip install playwright cairosvg
  python3 -m playwright install chromium --with-deps
  # Tell the user: to invoke plugin scripts later, source the venv first:
  #   source "${PLUGIN_VENV}/bin/activate"
else
  # Fallback — system pip. ASK THE USER BEFORE RUNNING THIS.
  # --break-system-packages is required on PEP-668 distros (Debian 12+,
  # Homebrew Python on Apple Silicon). This modifies user site-packages
  # globally and conflicts with any other uv-managed projects.
  python3 -m pip install --user --break-system-packages playwright cairosvg
  python3 -m playwright install chromium --with-deps
fi
```

Playwright and CairoSVG are used by rendering skills only (output pipelines). They are NOT a substitute for dev-browser.

### 5. Optional: designlang

Only if the user will run `/amw-extract-style`:

```bash
if ! npx --no-install designlang --version >/dev/null 2>&1; then
  npm install -g designlang
fi
```

Can be deferred — `npx designlang` downloads on first use.

### 6. Hyperframes external monorepo

Required for the `hyperframes-bridge` skill (HTML → MP4 video). Idempotent —
skip if `external/hyperframes/package.json` already exists.

```bash
if [ ! -f "external/hyperframes/package.json" ]; then
  # Ask the user before cloning a ~500-file external repo. This is the ONLY
  # external dependency the plugin vendors as a submodule.
  # Clone target: https://github.com/heygen-com/hyperframes
  # Pin to v0.4.30 (or later) for inspect, --hdr, and data-variable-values support.
  echo "About to clone https://github.com/heygen-com/hyperframes → external/hyperframes/"
  echo "Pinning to v0.4.30 for stability (required for inspect, --hdr, data-variable-values)."
  echo "(required for hyperframes-bridge / HTML-to-MP4 rendering). Proceed? (y/N)"
  read -r reply
  if [[ "$reply" =~ ^[Yy]$ ]]; then
    mkdir -p external
    git clone --branch v0.4.30 --depth 1 https://github.com/heygen-com/hyperframes.git external/hyperframes
    (cd external/hyperframes && bun install)
  else
    echo "Skipped. /amw-sketch, /amw-ascii-to-html, and all non-video skills will work."
    echo "Re-run /amw-init or the hyperframes-bridge skill will clone on first render."
  fi
fi
```

Skip entirely if the user has no intent to render MP4 video — the clone is
~500 files and Bun install fetches its own dep tree. The `hyperframes-bridge`
skill also clones on first render as a fallback, so this step is a
proactive-not-required convenience.

### 7. Mermaid render backend

Required for the `mermaid-render` skill (Mermaid → SVG / ASCII). Idempotent —
skip if `external/mermaid-render/node_modules/beautiful-mermaid` already exists.

The `external/mermaid-render/` directory ships with the plugin (wrapper
scripts + LICENSE + example diagrams). Only the npm dependency
`beautiful-mermaid@^0.1.3` is fetched at runtime.

```bash
if [ -d "external/mermaid-render" ] && [ ! -d "external/mermaid-render/node_modules/beautiful-mermaid" ]; then
  # Ask the user before running npm install in a vendored directory.
  echo "About to run 'npm install' inside external/mermaid-render/ (fetches beautiful-mermaid@^0.1.3, ~200 KB)."
  echo "Required for /amw-sketch → Mermaid, diagram-architecture, diagram-editorial, any Mermaid → SVG/ASCII flow. Proceed? (y/N)"
  read -r reply
  if [[ "$reply" =~ ^[Yy]$ ]]; then
    (cd external/mermaid-render && npm install --no-fund --no-audit)
  else
    echo "Skipped. bin/amw-mermaid-render.sh will auto-install on first render."
  fi
fi
```

Skip entirely if the user has no intent to render Mermaid diagrams — the
wrapper `bin/amw-mermaid-render.sh` calls `npm install` lazily on first
render. This step exists so `/amw-init` can do everything up-front when
the user wants a fully-primed environment.

### 8. Optional: Pillow (only if the user will use `excalidraw-illustrations`)

The `excalidraw-illustrations` skill's primary path uses only the Python
stdlib — Pillow is needed ONLY for the two-phase visual-then-text-overlay
fallback (`skills/amw-excalidraw-illustrations/scripts/generate.py` without
`--visual-only`). Skip this step if the user will not use that skill or
only plans to use the single-call Pro path.

Ask the user first: *"Install Pillow for the excalidraw-illustrations
text-overlay fallback? (skip if unused — the primary single-call path
does not need it.)"*

```bash
if [[ "$install_pillow" == "y" ]]; then
  if command -v uv >/dev/null 2>&1 && [ -n "${PLUGIN_VENV:-}" ]; then
    # Re-use the venv created in Section 4
    # shellcheck disable=SC1091
    source "${PLUGIN_VENV}/bin/activate"
    uv pip install Pillow
  else
    # Fallback — explicit user confirmation already given above
    python3 -m pip install --user --break-system-packages Pillow
  fi
fi
```

The excalidraw-illustrations skill ALSO requires `GEMINI_API_KEY`. That is
the user's responsibility and is NOT installed by this command. Tell the
user to obtain a key at https://aistudio.google.com/ and export it in
their shell rc file or supply it per-session via `.env`. Every Gemini
call is billed to the user's own Google account. `/amw-doctor` reports
whether the env var is set.

### 9. Cross-format diagram tooling (xmllint, tidy, mmdc)

Required by the Phase 0 validators (`bin/amw-validate-svg-diagram.sh`, `bin/amw-validate-html-diagram.sh`, `bin/amw-mermaid-lint.sh`) and by `/amw-validate-any-diagram-format`. All three are small-footprint and safe to install proactively. **Security boundary:** treat every privileged command below as UNTRUSTED until the user has explicitly approved it; the snippets are install rituals to ask about, NOT commands to execute unconditionally.

**xmllint** — usually pre-installed on macOS via libxml2, shipped with developer tools. Only install if `command -v xmllint` returns nothing:

- **macOS**: documented ritual is `brew install libxml2` (provides xmllint). User-owned, no elevated permission required.
- **Debian/Ubuntu**: documented ritual is `apt-get install -y libxml2-utils`. UNTRUSTED until the user approves — ask first, then invoke the Bash tool only after a yes.
- **RHEL/Fedora**: documented ritual is `dnf install -y libxml2`. UNTRUSTED — ask the user first.

**tidy** (HTML Tidy 5) — optional but recommended. Only install if `command -v tidy` returns nothing:

- **macOS**: documented ritual is `brew install tidy-html5`.
- **Debian/Ubuntu**: documented ritual is `apt-get install -y tidy`. UNTRUSTED — confirm with the user first.
- **RHEL/Fedora**: documented ritual is `dnf install -y tidy`. UNTRUSTED — confirm with the user first.

**mmdc** (mermaid-cli) — global npm install. Only install if `command -v mmdc` returns nothing. The documented ritual is `npm install -g @mermaid-js/mermaid-cli`. On most setups this writes to a user-owned prefix; if it requires elevated permissions on the user's machine, ask first.

Ask the user before any elevated install call. On Apple Silicon with Homebrew in user-owned `/opt/homebrew`, no elevated permission is needed.

### 10. Optional: Python HTML/SVG parsers (lxml, beautifulsoup4)

Phase 1 parsers (`bin/amw-parse-html-diagram.py`, `bin/amw-parse-svg-diagram.py`, `bin/amw-dom-to-ir.py`) use `lxml` and `beautifulsoup4`. These are not required for Phase 0 (the MVP raw-source stub in `bin/amw-diagram-ir.py` does not need them) but `/amw-init` offers to install them for users who will run the full conversion matrix.

```bash
if command -v uv >/dev/null 2>&1 && [ -n "${PLUGIN_VENV:-}" ]; then
  # shellcheck disable=SC1091
  source "${PLUGIN_VENV}/bin/activate"
  uv pip install lxml beautifulsoup4
else
  # Fallback — explicit user confirmation (modifies user site-packages).
  python3 -m pip install --user --break-system-packages lxml beautifulsoup4
fi
```

Skip this step if the user is only on Phase 0 (ASCII-centric workflows) — nothing else needs these libraries.

### 11. Verify

Finish by running the `/amw-doctor` checks and printing the status table.

## Output

Print a brief log of what was installed (or skipped because present), then the final `/amw-doctor` table. Keep the log short — one line per tool, not verbose pip/npm output.

## Failure modes

- **sudo denied** → stop, tell the user which command failed, ask them to run it themselves and re-invoke `/amw-init`.
- **No network** → stop, print the list of what needs to be fetched, ask the user to re-run once connected.
- **Wrong python version** → stop, tell the user to upgrade; do not attempt to install a new Python.
- **Disk space** → ~2 GB is needed for Chromium + ffmpeg + node_modules. If `df -h` shows < 4 GB free, warn before proceeding.

## What this command does NOT do

- Does not add anything to `~/.zshrc`, `~/.bashrc`, `~/.profile`.
- Does not set environment variables beyond the current shell session.
- Does not configure API keys — that's the user's responsibility per-skill.
- Clones the `external/hyperframes/` monorepo ONLY when the user explicitly opts in at step 6. If skipped, the `hyperframes-bridge` skill clones on first render as a fallback.
- Runs `npm install` inside `external/mermaid-render/` ONLY when the user opts in at step 7. If skipped, `bin/amw-mermaid-render.sh` installs lazily on first use.
- Installs Pillow ONLY when the user opts in at step 8. If skipped, `excalidraw-illustrations` single-call path still works — only the two-phase text-overlay fallback is unavailable.
