---
name: TECH-hyperframes-cli-capture
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/capture.ts
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Flags](#flags)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Out of scope for the bridge](#out-of-scope-for-the-bridge)
- [Cross-references](#cross-references)

# TECH: `hyperframes capture` — capture a website as editable Hyperframes components

## What it does

Captures a live website (by URL) and converts its visual content into editable Hyperframes composition components. The output is a project directory containing HTML composition files, downloaded assets (images, SVGs), and a structured representation of the website's visual layout.

This is the automated CLI path for the website-to-Hyperframes workflow. It complements the manual 7-step pipeline documented in `TECH-hyperframes-capture-step-*.md` but handles much of the capture-and-extract work programmatically.

## When to use

- Starting a new video composition from an existing website (landing page, marketing page, product tour).
- Generating a baseline composition from a client's live URL before customizing it.
- Programmatic / agentic pipelines where a URL is the input and a composition directory is the output.
- `--json` mode is designed specifically for AI agents that need structured output.

## How it works

```bash
# Basic capture — outputs to a directory named after the domain
npx hyperframes capture https://stripe.com

# Capture to a specific output directory
npx hyperframes capture https://linear.app -o linear-video

# JSON output (for AI agents / programmatic use)
npx hyperframes capture https://example.com --json

# Skip downloading assets (faster, but composition will reference remote URLs)
npx hyperframes capture https://example.com --skip-assets
```

### Flags

| Flag | Alias | Type | Default | Description |
|---|---|---|---|---|
| `url` | — | positional | — (required) | Website URL to capture |
| `--output` | `-o` | string | `captures/<hostname>` | Output directory name (prefixed with `captures/` to keep repo root clean; `<hostname>` is the URL hostname with dots replaced by dashes, `www.` prefix stripped) |
| `--skip-assets` | — | boolean | false | Skip downloading images and SVGs |
| `--max-screenshots` | — | string | `"24"` | Maximum screenshots to capture during scrolling |
| `--timeout` | — | string | `"120000"` | Page load timeout in ms (default: 2 minutes) |
| `--json` | — | boolean | false | Output result as JSON (for AI agents / programmatic use) |

## Minimal example

```bash
# Capture a website and inspect what was generated
npx hyperframes capture https://stripe.com -o stripe-video
ls stripe-video/

# Pipe JSON output to an agent pipeline
npx hyperframes capture https://example.com --json | jq '.components'
```

After capture, the output directory contains a partial Hyperframes project. The typical next steps are:
1. Review the generated composition files
2. Run `npx hyperframes lint` to catch any issues
3. Edit the compositions to add timeline attributes and animation
4. Run `npx hyperframes render` to produce the MP4

## Gotchas

- `capture` requires a live network connection to the target URL. Corporate firewalls, paywalls, and bot-detection may block it.
- The default output directory is `captures/<hostname>` (e.g. `captures/stripe-com` for `https://stripe.com`), NOT the bare domain name. The `captures/` prefix keeps the repo root clean. Pass `-o <dir>` to override (e.g. `-o stripe-video` writes directly to `stripe-video/`).
- `--skip-assets` makes the initial capture faster but the final composition will reference remote URLs, which may cause issues if assets are unavailable or rate-limited during render.
- The output is a starting point, not a ready-to-render composition. Manual curation (adding `data-start`, `data-duration`, timeline scripts) is typically needed.
- `@hyperframes/cli` is NOT published to npm. Invoke via `(cd external/hyperframes && npx hyperframes capture <url>)` from outside the monorepo.
- This CLI command automates Step 1 of the 7-step manual pipeline ([TECH-hyperframes-capture-step-1-capture](TECH-hyperframes-capture-step-1-capture.md)). For full context on what each step produces and how to proceed, read the step-by-step TECH files.
  > What it does · When to use · How it works · Gate · Minimal example · Gotchas · Cross-references

## Out of scope for the bridge

The following CLI commands exist in the upstream monorepo but are out of scope for Phase B pipeline use. See the upstream `cli.mdx` and `external/hyperframes/packages/cli/src/cli.ts:26-53` for the complete command registry. Out-of-scope list (no TECH file in this directory): `play`, `benchmark`, `upgrade`, `skills`, `telemetry`, `catalog`, `compositions`, `info`, `docs`, `publish`. The general rule: any CLI command without a corresponding `TECH-hyperframes-cli-<name>.md` file in this directory is out of bridge scope.

## Cross-references

- [TECH-hyperframes-capture-overview](TECH-hyperframes-capture-overview.md) — full 7-step pipeline overview
  > What it does · When to use · How it works · Video type reference · Format presets · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-1-capture](TECH-hyperframes-capture-step-1-capture.md) — manual capture step (what this command automates)
  > What it does · When to use · How it works · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-cli-render](TECH-hyperframes-cli-render.md) — the final render step
  > What it does · When to use · How it works · Flags · Quality guidance · Transparent video · Minimal example · Workers tuning · Gotchas · Cross-references
- [TECH-hyperframes-cli-browser](TECH-hyperframes-cli-browser.md) — Chrome provisioning (required for capture)
  > What it does · When to use · How it works · Sub-commands · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
