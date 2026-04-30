---
name: amw-dev-browser
description: Browser automation and page-state capture via the `dev-browser` CLI. Triggers on narrow technical intents only — "go to URL", "click on", "fill form", "take screenshot", "scrape", "automate the browser", "test the website", "inspect DOM", "mobile screenshot". Does NOT trigger on design vocabulary ("design a page", "build a landing page", "mockup", "prototype") — those belong to the `design-principles` orchestrator, which routes here when a design workflow needs to capture a real page.
version: 0.1.0
---

# Dev Browser

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> This skill is an executor. Its triggers are technical only — `design-principles` routes design intent here when a workflow needs to capture, inspect, or automate a real web page.

## Activation

Callable directly via the `/amw-preview` command (screenshot + self-check shortcut) or `/amw-extract-style` command (style-token extraction shortcut) for users who want those specific actions immediately. Also invoked by the `design-principles` orchestrator during Phase B in Main-agent mode for scenario testing of every browser-runnable artifact. In Main-agent mode the orchestrator may apply interaction, DOM inspection, and multi-step navigation techniques from this skill beyond what any individual command exposes.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**INPUT.** This is the plugin's **only** browser-automation primitive for input capture — screenshots, DOM dumps, interactive navigation, form filling. It feeds downstream sub-skills that need real-page evidence (notably `../amw-design-extract/` for style-token extraction), and it drives Phase B scenario tests for every browser-runnable artifact.

Rendering pipelines elsewhere in the plugin — `bin/amw-html-export.py`, `../amw-hyperframes-bridge/`, `../amw-infographics/` — use Playwright **internally for OUTPUT emission** (HTML → PNG / PDF / MP4). They are **not substitutes** for this skill. Input capture (read the web) and output rendering (write from HTML) are different axes.

## Trigger conditions

Activate only on explicit browser-automation or page-capture intents:

- "go to <url>", "open <url>", "navigate to"
- "click on", "fill out the form", "submit", "log in"
- "take a screenshot of <url>", "mobile screenshot", "full-page shot"
- "scrape", "extract data from the page", "dump the DOM"
- "automate the browser", "test the website", "inspect the page state"

Do **not** activate on design-intent vocabulary ("design a page", "build a landing page", "mockup", "prototype", "wireframe"). Those are owned by `design-principles`, which will call this skill only when a design workflow needs a real page as input (e.g. `/amw-extract-style <url>`).

## Dependencies

- **runtime_binaries (system):** `node >= 22`
- **runtime_binaries (installed via `/amw-init`):** `dev-browser` CLI — installed with `npm install -g dev-browser` followed by `dev-browser install` (the second command provisions the sandboxed Chromium profile).
- **python_packages:** none
- **npm_packages:** `dev-browser` (global, as above)
- **mcp_servers:** none

## Usage

**Direct CLI** — learn every subcommand by running:

```bash
dev-browser --help
```

**Plugin-standard wrapper** — prefer `../../bin/amw-dev-browser-wrapper.sh` for the idiomatic invocations used across the plugin. The wrapper exposes:

- `shot <url> [outfile]` — full-page desktop screenshot
- `mobile <url> [outfile]` — mobile-viewport screenshot
- `dom <url> [outfile]` — serialized DOM dump
- `open <url>` — open a persistent interactive session (survives across agent turns)
- `pass-through …` — any raw `dev-browser` argument vector

The wrapper is the stable entry point other plugin code depends on; the raw CLI is fine for ad-hoc exploration.

## Cross-references

- `../../bin/amw-dev-browser-wrapper.sh` — plugin-standard wrapper (the canonical invocation path).
- `../amw-design-extract/SKILL.md` — downstream consumer: combines `dev-browser` screenshots + DOM dumps with the `designlang` extractor to produce token sets.
- `../amw-design-principles/SKILL.md` — upstream orchestrator; route design intents through there, not directly to this skill.
- `../amw-design-principles/ai-slop-avoid.md` — apply after extracting any visual reference, before handing it to a design variant.
- Slash commands: `/amw-extract-style <url>` (uses this skill + design-extract), `/amw-preview` (local preview server; orthogonal to this skill but often used together), `/amw-init` (installs the CLI).

## Non-negotiables

- **Do NOT suggest, import, or fall back to** Chrome DevTools MCP, Playwright MCP, `puppeteer`, `selenium`, or any other browser-automation surface. Those are excluded plugin-wide. This skill is the single authorized browser-automation primitive.
- **Do NOT claim design vocabulary.** Routing decisions based on "design a page" / "build a landing page" belong to `design-principles`. This skill only executes when the orchestrator routes here, or when the user's intent is unambiguously technical browser automation.
- **Rendering backends elsewhere are OUTPUT-only.** `html-export.py` and `hyperframes-bridge` use Playwright internally to convert HTML artefacts to PNG / PDF / MP4. They do **not** replace this skill for input capture. Never propose them as substitutes.
- **Do NOT bake secrets or cookies into scripts.** `dev-browser` maintains a persistent, sandboxed profile — use it for session state; never paste credentials into prompt arguments.

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| `dev-browser: command not found` | CLI not installed | Run `/amw-init`, or manually `npm install -g dev-browser && dev-browser install`. |
| `Chromium download failed` / first-run crash | `dev-browser install` was never run | Re-run `dev-browser install` once per machine to fetch the sandboxed browser. |
| Screenshot is blank or truncated | Page uses lazy-load or infinite scroll | Use the wrapper's `pass-through` to supply `dev-browser`'s wait / scroll flags; do **not** swap to Playwright. |
| Node version error | Node < 22 on PATH | Upgrade Node to >= 22. This skill does not support older runtimes. |
| DOM dump missing shadow-root content | Target uses closed shadow DOM | Document the limitation and fall back to screenshot-based extraction; do not introduce a second automation stack.
