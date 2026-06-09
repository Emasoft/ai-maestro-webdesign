---
name: TECH-error-handling
category: hyperframes-bridge
source: skills/amw-hyperframes-bridge/SKILL.md
---

# TECH: Error handling — amw-hyperframes-bridge

Common failure modes and their fixes when invoking the Hyperframes bridge.

## Environment

- **`external/hyperframes/` missing** — first-use clone step was skipped. Run `/amw-init` or clone manually (see Prerequisites in SKILL.md).
- **`npx hyperframes render --help` fails** — monorepo cloned but `bun install` not run. `cd external/hyperframes && bun install`.
- **`bun: command not found`** — Bun not installed. `/amw-init` provisions it (on macOS via Homebrew's `bun` formula; otherwise the upstream `bun.sh` installer ritual, which fetches a setup script from `bun.sh` and pipes it to the shell).
- **`ffmpeg: command not found`** — FFmpeg not on PATH. `/amw-init` installs it (macOS: `brew install ffmpeg`; Linux: distro package manager).
- **Chrome not provisioned** — Hyperframes uses Puppeteer + `@puppeteer/browsers` (NOT Playwright) to manage Chrome. Run `(cd external/hyperframes && npx hyperframes browser ensure)` to download Chrome Headless Shell.

## Composition / render

- **HTML attribute parse errors** — composition is missing required `data-composition-id`, `data-start`, or `data-duration`. Re-author the HTML per the schema in `external/hyperframes/packages/core/`.
- **Video encoding failure** — check stderr log from the render shell-out; usually an FFmpeg codec mismatch or missing source asset (video/audio file referenced by the composition does not exist).
- **Stale clone** — if render fails with "method not found" errors that suggest an API change, verify the version: `node -e "console.log(require('./external/hyperframes/packages/cli/package.json').version)"`. If below 0.4.30, pull and re-run `bun install`.
