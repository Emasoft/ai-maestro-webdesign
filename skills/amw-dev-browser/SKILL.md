---
name: amw-dev-browser
description: Browser automation and page-state capture via the `dev-browser` CLI. Triggers on "go to URL", "click on", "fill form", "take screenshot", "scrape", "automate the browser", "test the website", "inspect DOM", "mobile screenshot". Does NOT trigger on design vocabulary — those route to `design-principles`. Use when automating a browser, taking screenshots, filling forms, or scraping. Trigger with /amw-preview.
---

# Dev Browser

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is an executor. Its triggers are technical only — `design-principles` routes design intent here when a workflow needs to capture, inspect, or automate a real web page.

## Overview

Browser automation and page-state capture via the `dev-browser` CLI. The plugin's single authorized browser-automation primitive for input capture — screenshots, DOM dumps, interactive navigation, form filling. Rendering pipelines that use Playwright for output emission (HTML → PNG/PDF/MP4) are separate and are NOT substitutes for this skill.

## Instructions

1. Use `bin/amw-dev-browser-wrapper.sh` as the stable entry point for all plugin-internal automation; avoid calling `dev-browser` raw.
2. For screenshots: call `bin/amw-dev-browser-wrapper.sh shot <url> [outfile]` (desktop) or `mobile <url> [outfile]` (mobile viewport).
3. For DOM capture: call `bin/amw-dev-browser-wrapper.sh dom <url> [outfile]` to get the serialized DOM.
4. For interactive or persistent sessions: use `open <url>` to keep the browser alive across agent turns.
5. For any capability not covered by the wrapper shortcuts, use `pass-through …` to forward a raw `dev-browser` argument vector.
6. This skill is the ONLY browser-automation primitive in the plugin — do not wire live-page inspection through Chrome DevTools MCP, Playwright MCP, or any other browser wrapper.

Full usage details (activation, trigger conditions, wrapper subcommands, non-negotiables, full error-handling table): see [usage-guide](./references/usage-guide.md).
> Position in flow · Activation · Trigger conditions · Prerequisites · Usage details · Non-negotiables · Error handling

## Prerequisites

- **runtime_binaries (system):** `node >= 22`
- **runtime_binaries (installed via `/amw-init`):** `dev-browser` CLI — install with `npm install -g dev-browser` followed by `dev-browser install` (the second command provisions the sandboxed Chromium profile).
- **python_packages:** none
- **npm_packages:** `dev-browser` (global, as above)
- **mcp_servers:** none

## Output

Produces screenshots (PNG), DOM dumps (HTML/text), or interactive session state depending on the invocation. Output path is determined by the caller or the wrapper script's default.

## Examples

**Input:** user says "Take a screenshot of https://stripe.com on mobile."
**Output:** call `bin/amw-dev-browser-wrapper.sh mobile https://stripe.com /tmp/stripe-mobile.png`; deliver the path to the user. Do NOT inline the PNG into chat.

**Input:** user says "Dump the DOM of the current onboarding step."
**Output:** call `bin/amw-dev-browser-wrapper.sh dom <url> /tmp/onboarding.html`; deliver the path; the consumer parses the markup.

See the worked examples documented in the extended usage guide (Resources) and in the `bin/amw-dev-browser-wrapper.sh` help text.

## Error Handling

Common failure modes and remediation are listed in the extended usage guide (see Resources). Summary: `dev-browser: command not found` → run `/amw-init`; first-run Chromium download failed → re-run `dev-browser install`; screenshot blank → use `pass-through` for `dev-browser`'s wait flags (do not swap to Playwright); Node < 22 → upgrade Node.

## Resources

- `../../bin/amw-dev-browser-wrapper.sh` — plugin-standard wrapper (the canonical invocation path).
- [SKILL](../amw-design-extract/SKILL.md) — downstream consumer: combines `dev-browser` screenshots + DOM dumps with the `designlang` extractor to produce token sets.
- [SKILL](../amw-design-principles/SKILL.md) — upstream orchestrator; route design intents through there, not directly to this skill.
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — apply after extracting any visual reference, before handing it to a design variant.
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- [usage-guide](./references/usage-guide.md) — extended usage notes
  > Position in flow · Activation · Trigger conditions · Prerequisites · Usage details · Non-negotiables · Error handling
- Slash commands: `/amw-extract-style <url>` (uses this skill + design-extract), `/amw-preview` (local preview server; orthogonal to this skill but often used together), `/amw-init` (installs the CLI).
