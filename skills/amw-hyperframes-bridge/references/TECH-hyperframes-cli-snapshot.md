---
name: TECH-hyperframes-cli-snapshot
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/snapshot.ts
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Flags](#flags)
  - [Output](#output)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: `hyperframes snapshot` — capture key frames as PNG screenshots

## What it does

Captures PNG screenshots of the composition at selected timeline timestamps, saving them as `snapshots/frame-NN-at-<time>.png` inside the project directory. Useful as a visual pre-render gate (complement to `inspect` and `validate`) or for producing thumbnail/preview images without a full MP4 render.

## When to use

- Quick visual sanity check before committing to a full render: "does the composition look right at t=5s and t=20s?"
- Generating thumbnail images for a composition (e.g. cover frames for a video).
- Debugging specific problem frames identified by `inspect` — snapshot those exact timestamps to see the visual state.
- CI pipelines where full render is too slow but a frame check provides confidence.

## How it works

```bash
# Default: 5 evenly-spaced frames
npx hyperframes snapshot

# Custom number of frames
npx hyperframes snapshot --frames 10

# Explicit timestamps (seconds, comma-separated)
npx hyperframes snapshot --at 0.5,3.0,10.0

# Specific project directory
npx hyperframes snapshot ./my-video
```

### Flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `dir` | positional | `.` (current dir) | Project directory to snapshot |
| `--frames` | string | `"5"` | Number of evenly-spaced frames to capture |
| `--at` | string | — | Comma-separated timestamps in seconds (e.g. `--at 3.0,10.5,18.0`). Overrides `--frames` when set. |
| `--timeout` | string | `"5000"` | Ms to wait for runtime to initialize (default: 5000 ms) |

### Output

Screenshots are saved to `snapshots/` inside the project directory, named `frame-NN-at-<time>.png` (where time is a percentage of composition duration when using `--frames`, or the explicit timestamp when using `--at`).

## Minimal example

```bash
cd /path/to/my-project

# Take 5 evenly-spaced snapshots for quick visual QA
npx hyperframes snapshot

# After inspect flags issues at t=2.0s — snapshot exactly that frame
npx hyperframes snapshot --at 2.0

# View the results
open snapshots/
```

## Gotchas

- `snapshot` requires Chrome (same as `render` and `inspect`). Run `npx hyperframes browser ensure` first if Chrome is not provisioned.
- `snapshot` does NOT replace `inspect` — it produces images for human review; `inspect` performs programmatic layout analysis. Use both in combination.
- PNG files can be large for high-resolution compositions (1080p+ = several MB per frame). The `snapshots/` directory is not automatically cleaned.
- `@hyperframes/cli` is NOT published to npm. Invoke via `(cd external/hyperframes && npx hyperframes snapshot)` from outside the monorepo.

## Cross-references

- [TECH-hyperframes-cli-inspect](TECH-hyperframes-cli-inspect.md) — programmatic layout audit; use both for pre-render QA
  > What it does · When to use · How it works · Flags · Output (JSON mode) · Minimal example · Opt-out attributes · Gotchas · Cross-references
- [TECH-hyperframes-cli-render](TECH-hyperframes-cli-render.md) — the full render step that follows successful QA
  > What it does · When to use · How it works · Flags · Quality guidance · Transparent video · Minimal example · Workers tuning · Gotchas · Cross-references
- [TECH-hyperframes-cli-browser](TECH-hyperframes-cli-browser.md) — Chrome provisioning
  > What it does · When to use · How it works · Sub-commands · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
