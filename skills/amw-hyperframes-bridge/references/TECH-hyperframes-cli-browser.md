---
name: TECH-hyperframes-cli-browser
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/browser.ts
also-in: external/hyperframes/packages/cli/src/browser/manager.ts
---

# TECH: `hyperframes browser` — manage Chrome for rendering

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Sub-commands](#sub-commands)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


> This is the **canonical Chrome-provisioning command** for Hyperframes. Hyperframes uses Puppeteer + `@puppeteer/browsers` (NOT Playwright) to manage its own Chrome Headless Shell. Running `npx playwright install chromium` is NOT a fix for browser-missing errors in Hyperframes — use `hyperframes browser ensure` instead.

## What it does

Manages the Chrome Headless Shell binary that Hyperframes uses for all rendering operations (`render`, `inspect`, `validate`, `snapshot`). Three sub-commands: `ensure` (find or download Chrome), `path` (print executable path for scripting), `clear` (remove cached download).

## When to use

- **First time after cloning the monorepo:** run `ensure` once before any render command. Chrome is not bundled in the repo — it must be downloaded on first use.
- **CI / Docker:** run `ensure` at the start of the pipeline to guarantee Chrome is ready before `render` is invoked.
- **After a Chrome version bump:** run `clear` then `ensure` to refresh the cached binary.
- **Scripting:** use `path` to get the executable path for passing to Puppeteer directly (advanced use).
- **Diagnosing browser errors:** if `render` or `inspect` fails with a Puppeteer-related error, run `ensure` to verify Chrome is present.

## How it works

```bash
# Find or download Chrome (safe to run multiple times — idempotent)
npx hyperframes browser ensure

# Print the Chrome executable path (for scripting)
npx hyperframes browser path

# Remove cached Chrome download
npx hyperframes browser clear
```

### Sub-commands

| Sub-command | Description |
|---|---|
| `ensure` | Find an existing Chrome installation (system Chrome or cached download); if not found, download Chrome Headless Shell. Idempotent. |
| `path` | Print the executable path of the Chrome binary Hyperframes will use. Exits 0 even if Chrome is not yet downloaded (triggers a download first). |
| `clear` | Remove the cached Chrome Headless Shell download from `~/.cache/puppeteer/` (or the platform-equivalent `@puppeteer/browsers` cache directory). Does NOT remove system Chrome. |

## Minimal example

```bash
# Standard setup after cloning the monorepo (run once):
cd external/hyperframes && bun install
npx hyperframes browser ensure

# Verify Chrome is ready before rendering:
npx hyperframes browser path && echo "Chrome ready"

# From the plugin's project root (subshell pattern — @hyperframes/cli is not on global npm):
(cd external/hyperframes && npx hyperframes browser ensure)
```

## Gotchas

- `@hyperframes/cli` is NOT published to npm. Invoke via `(cd external/hyperframes && npx hyperframes browser ensure)` or `npx --prefix external/hyperframes hyperframes browser ensure` from the plugin root. Direct `npx hyperframes browser ensure` from outside the monorepo fails.
- Chrome is cached under `~/.cache/puppeteer/` (Linux) or the platform-equivalent `@puppeteer/browsers` cache directory. The `clear` command removes this cache.
- `ensure` is idempotent — if Chrome is already found (system Chrome or cached), it reports the path and exits without downloading.
- Hyperframes resolves Chrome in this priority order: (1) `HYPERFRAMES_CHROME_PATH` env var, (2) `PUPPETEER_EXECUTABLE_PATH` env var, (3) system `google-chrome-stable` / `chromium`, (4) the `@puppeteer/browsers` cache. Only (4) requires running `ensure`.
- Do NOT confuse with Playwright's `npx playwright install chromium` — those are separate binaries in separate cache directories. Playwright's Chromium is invisible to Hyperframes.

## Cross-references

- [TECH-hyperframes-cli-render](TECH-hyperframes-cli-render.md) — render uses Chrome managed by this command
  > What it does · When to use · How it works · Flags · Quality guidance · Transparent video · Minimal example · Workers tuning · Gotchas · Cross-references
- [TECH-hyperframes-cli-inspect](TECH-hyperframes-cli-inspect.md) — inspect also requires Chrome
  > What it does · When to use · How it works · Flags · Output (JSON mode) · Minimal example · Opt-out attributes · Gotchas · Cross-references
- [TECH-hyperframes-cli-snapshot](TECH-hyperframes-cli-snapshot.md) — snapshot also requires Chrome
  > What it does · When to use · How it works · Flags · Output · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md) — bridge invocation pattern (see Failure modes section)
