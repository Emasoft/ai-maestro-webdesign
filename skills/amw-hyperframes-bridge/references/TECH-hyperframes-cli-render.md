---
name: TECH-hyperframes-cli-render
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/render.ts
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Flags](#flags)
  - [Quality guidance](#quality-guidance)
  - [Transparent video](#transparent-video)
- [Minimal example](#minimal-example)
  - [Workers tuning](#workers-tuning)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: `hyperframes render` — capture composition to MP4 / WebM

## What it does

Captures the composition to a video file via a headless Chromium + FFmpeg pipeline. Supports MP4 (H.264), MOV (ProRes 4444, with transparency), WebM (VP9, with transparency), multiple FPS targets, quality presets, parallel workers, GPU encoding, Docker-reproducible mode.

## When to use

After `lint`, `validate`, and `inspect` pass. `render` is the final step of the pre-render gate sequence (`lint → validate → inspect → render`).

## How it works

```bash
# Standard MP4
npx hyperframes render

# Named output path
npx hyperframes render --output final.mp4

# Fast iteration (lower quality, smaller file)
npx hyperframes render --quality draft

# Final delivery (60 fps, high quality)
npx hyperframes render --fps 60 --quality high

# Transparent overlay (ProRes 4444 — recommended for video editors)
npx hyperframes render --format mov --output overlay.mov

# Transparent WebM (Chromium browsers only — not for video editors)
npx hyperframes render --format webm

# Reproducible Docker-based render (byte-identical across machines)
npx hyperframes render --docker

# Fine-grained quality: override CRF directly
npx hyperframes render --crf 15 --output pristine.mp4

# Size-constrained delivery: target bitrate
npx hyperframes render --video-bitrate 10M --output controlled.mp4
```

### Flags

| Flag | Options | Default | Notes |
|---|---|---|---|
| `--output` | path | `renders/<name>.mp4` | Output path |
| `--fps` | 24, 30, 60 | 30 | 60 fps doubles render time |
| `--quality` | draft / standard / high | standard | draft = CRF 28 ultrafast; standard = CRF 18 medium; high = CRF 15 slow |
| `--crf` | 0–51 | — | Override CRF directly. Cannot combine with `--video-bitrate` |
| `--video-bitrate` | e.g. `10M`, `5000k` | — | Target bitrate. Cannot combine with `--crf` |
| `--format` | mp4 / mov / webm | mp4 | MOV = ProRes 4444 (transparent, editor-compatible); WebM = VP9 (transparent, browser-only) |
| `--workers` | int or auto | auto (`cpuCount - 2`, capped at 6, also bounded by memory ≥256MB/worker and frame count) | Each worker spawns a separate Chrome process (~256 MB RAM each) |
| `--max-concurrent-renders` | 1-10 | 2 | Max simultaneous renders on the producer server |
| `--docker` | flag | off | Deterministic output — same Chrome + FFmpeg + fonts across platforms |
| `--gpu` | flag | off | GPU-accelerated encoding (NVENC, VideoToolbox, VAAPI). Local mode only. |
| `--quiet` | flag | off | Suppress verbose output |
| `--hdr` | flag | off | Detect HDR sources (BT.2020 PQ/HLG) and emit H.265 10-bit BT.2020 MP4. No-op on SDR-only compositions. MP4 only — `--format mov` / `--format webm` fall back to SDR with a warning. |
| `--strict` | flag | off | Fail on lint errors |
| `--strict-all` | flag | off | Fail on lint errors AND warnings |

### Quality guidance

| Preset | CRF | x264 Preset | Use for |
|---|---|---|---|
| `draft` | 28 | ultrafast | Iteration, quick previews |
| `standard` | 18 | medium | General use — visually lossless at 1080p |
| `high` | 15 | slow | Final delivery, near-lossless |

### Transparent video

MOV (ProRes 4444) is the correct format for video editors (CapCut, Final Cut, Premiere, DaVinci, After Effects). WebM VP9 alpha is only decoded by Chromium browsers — major video editors render its alpha as black. For transparent overlays going into an editor, always use `--format mov`.

When authoring a transparent composition, do NOT set a `background` on `html` or `body` — leave them unset so the transparent background passes through.

## Minimal example

```bash
# Iteration render
npx hyperframes render --quality draft --output out/draft.mp4

# Final delivery
npx hyperframes render --fps 30 --quality high --output out/final.mp4

# Transparent overlay for video editor
npx hyperframes render --format mov --output out/overlay.mov

# CI: fail on any issue
npx hyperframes render --strict-all --quality standard
```

### Workers tuning

Default `--workers auto` uses `cpuCount - 2` workers, also bounded by available memory (≥256 MB per worker) and total frame count (≥minimum frames per worker), with a hard ceiling of 6 workers. On a 4-core machine the default is typically 2 workers; on a 12-core machine it can be up to 6. If RAM-constrained, explicitly set `--workers 1`.

Run `npx hyperframes benchmark` to find the optimal setting for your machine.

*Attributed to the hyperframes-cli skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes-cli/SKILL.md`.*

## Gotchas

- `--docker` produces byte-identical output across machines (same Chrome, fonts, FFmpeg version). Required for Docker mode: Docker installed and running.
- `--gpu` only works on machines with NVIDIA NVENC, Apple VideoToolbox, or VAAPI. CPU fallback is silent. Local mode only — no GPU in Docker.
- MOV (ProRes 4444) files are large by design (intermediate codec). Typical 5-40 MB for short clips — this is expected and correct.
- WebM VP9 alpha is NOT supported by major video editors. Safari does not support it either. Use MOV for editor workflows.
- `--fps 60` doubles render time and bitrate. Reserve for final deliveries with fast motion, or when slow-motion post-processing requires higher source FPS.
- `--hdr` is detection-based, not force. If the composition has no HDR-tagged source (no `<video>` or `<img>` with BT.2020 PQ/HLG color metadata), the flag is a no-op and the output is SDR H.264 as usual. Verify the result with: `ffprobe -v error -show_streams output.mp4 | grep color_transfer` — look for `smpte2084` (PQ) or `arib-std-b67` (HLG).

## Cross-references

- [TECH-hyperframes-cli-lint](TECH-hyperframes-cli-lint.md), [TECH-hyperframes-cli-preview](TECH-hyperframes-cli-preview.md), [TECH-hyperframes-cli-validate](TECH-hyperframes-cli-validate.md), [TECH-hyperframes-cli-inspect](TECH-hyperframes-cli-inspect.md)
  > [TECH-hyperframes-cli-validate.md] What it does · When to use · How it works · Output · When warnings appear · Minimal example · Gotchas · Cross-references
  > [TECH-hyperframes-cli-inspect.md] What it does · When to use · How it works · Flags · Output (JSON mode) · Minimal example · Opt-out attributes · Gotchas · Cross-references
  > What it does · When to use · How it works · Minimal example · CI integration · Gotchas · Cross-references
- [TECH-hyperframes-cli-doctor](TECH-hyperframes-cli-doctor.md) — environment health check if render fails
  > What it does · When to use · How it works · What `doctor` checks · Minimal example · Common failure modes surfaced by `doctor` · Gotchas · Cross-references
- [SKILL](../SKILL.md)
