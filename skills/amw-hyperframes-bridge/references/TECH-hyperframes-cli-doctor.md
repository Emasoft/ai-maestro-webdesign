---
name: TECH-hyperframes-cli-doctor
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/doctor.ts
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [What `doctor` checks](#what-doctor-checks)
- [Minimal example](#minimal-example)
  - [Common failure modes surfaced by `doctor`](#common-failure-modes-surfaced-by-doctor)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: `hyperframes doctor` + environment utilities

## What it does

`hyperframes doctor` checks the runtime environment for common render-blockers: Node.js version, FFmpeg availability, Chrome/Chromium installation, memory headroom. Paired with `hyperframes browser`, `hyperframes info`, and `hyperframes upgrade` — the four commands together diagnose "why did my render fail".

## When to use

- First run `doctor` before the first render on any new machine.
- When `render` fails with a non-composition error (FFmpeg missing, Chrome missing, OOM).
- As part of CI pre-flight.

## How it works

```bash
# Health check
npx hyperframes doctor

# Manage bundled Chrome
npx hyperframes browser              # info
npx hyperframes browser ensure       # find or download bundled Chrome
npx hyperframes browser path         # print Chrome executable path

# Environment + version info
npx hyperframes info

# Check for CLI updates
npx hyperframes upgrade
```

### What `doctor` checks

- Version (current vs latest)
- Node.js (version + platform)
- CPU (core count + model)
- Memory (total + free; warns below 2 GB free)
- Disk (free space; warns below 1 GB)
- /dev/shm size (Linux only; warns below 256 MB — Chrome crashes in Docker without it)
- Environment (Docker / WSL / CI / non-TTY detection)
- FFmpeg on PATH
- FFprobe on PATH
- Chrome or Chromium available (bundled or system)
- Docker available
- Docker running

## Minimal example

```bash
$ npx hyperframes doctor
✓ Version         0.4.30 (latest)
✓ Node.js         22.1.0 (darwin arm64)
✓ CPU             10 cores · Apple M2 Pro
✓ Memory          16.0 GB total · 8.2 GB free
✓ Disk            234.1 GB free
✓ Environment     Native terminal
✓ FFmpeg          ffmpeg version 6.1.1
✓ FFprobe         ffprobe version 6.1.1
✓ Chrome          bundled: /Users/you/.cache/hyperframes/chrome/...
✓ Docker          Docker version 24.0.7
✓ Docker running  Running

$ npx hyperframes info
hyperframes CLI 0.4.30
Node.js 22.1.0
Platform: darwin arm64
Bundled Chromium: 126.0.6478
FFmpeg: 6.1.1 /opt/homebrew/bin/ffmpeg
```

### Common failure modes surfaced by `doctor`

- **FFmpeg missing** — install via `brew install ffmpeg` (macOS) or distro package manager (Linux)
- **Chromium missing** — `npx hyperframes browser ensure`
- **Node.js too old** — upgrade to 22+ (hyperframes uses modern ESM + fetch)
- **Low RAM** — reduce `--workers` on `render` to 2 or 1

*Attributed to the hyperframes-cli skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes-cli/SKILL.md`.*

## Gotchas

- `doctor` reports green but `render` still fails = the issue is composition-specific, not environmental. Drop to `lint` + `preview` to diagnose.
- The bundled Chromium is Ubuntu-flavored and may not match system Chrome colors exactly for some fonts or emoji. For strict color-reproduction, use `--docker` on `render`.
- `hyperframes upgrade` performs the actual upgrade interactively (prompts "Upgrade now?") or non-interactively with `--yes`. Use `--check` if you only want to check the available version without prompting. Source: `commands/upgrade.ts` uses `execSync(installCmd, { stdio: "inherit" })` when the user confirms or `--yes` is passed.

## Cross-references

- [TECH-hyperframes-cli-render](TECH-hyperframes-cli-render.md) — the command this diagnoses
- [TECH-hyperframes-cli-lint](TECH-hyperframes-cli-lint.md), [TECH-hyperframes-cli-preview](TECH-hyperframes-cli-preview.md)
- `../SKILL.md`
