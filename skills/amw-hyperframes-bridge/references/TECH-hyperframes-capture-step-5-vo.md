---
name: TECH-hyperframes-capture-step-5-vo
category: hyperframes-capture-step
source: external/hyperframes/skills/website-to-hyperframes/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Gate](#gate)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Step 5 — Generate VO + map timing to beats

## What it does

Generates text-to-speech narration audio for SCRIPT.md, transcribes it for word-level timestamps, then maps those timestamps back to STORYBOARD.md beats so the composition step has **real durations** — not guessed ones.

## When to use

After SCRIPT.md (Step 3) and STORYBOARD.md (Step 4) exist, before building compositions (Step 6). Even when narration is optional (music-only brand reel), timing generation runs so beat durations are anchored in actual audio, not estimated.

## How it works

Three sub-steps:

- **Generate TTS** — `npx hyperframes tts <script.txt> --voice af_heart --output narration.wav`. 12 bundled voices in the CLI (Kokoro-82M ships 54 total; the CLI exposes 12 via `BUNDLED_VOICES` in `tts/manager.ts`). Default voice is `af_heart`. Read [TECH-hyperframes-cli-tts](TECH-hyperframes-cli-tts.md) for voice selection rules.
- **Transcribe for word-level timestamps** — `npx hyperframes transcribe narration.wav --model medium.en`. Produces `transcript.json` with per-word start/end times.
- **Map timestamps to beats** — walk STORYBOARD.md beats in order, match each beat's narration text to the transcript, record the actual start/end seconds. Update STORYBOARD.md so every beat has a real duration (not a placeholder).

## Gate

Both `narration.wav` and `transcript.json` exist. STORYBOARD.md beats have real per-beat durations written in (replacing the estimated ones).

## Minimal example

```bash
# 1. Generate
npx hyperframes tts scripts/narration.txt --voice af_heart --output narration.wav

# 2. Transcribe
npx hyperframes transcribe narration.wav --model medium.en --language en

# 3. Read transcript.json → map to beats
# (scripted — the hyperframes repo ships a mapper; or do it manually by
#  scanning the transcript for each beat's first 3-4 words as anchors)
```

Updated STORYBOARD.md beat header:

```markdown
## Beat 1 (hook, 0.0-2.47 s) — "Address verification, in under 120 milliseconds."
  (was: "0-2.5 s" estimated)
```

*Attributed to the website-to-hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/website-to-hyperframes/SKILL.md`.*

## Gotchas

- Skipping this step and guessing durations produces compositions that don't sync with the audio — visual elements land before or after their narration cues.
- TTS voice choice is load-bearing for the brand vibe — technical brands sound wrong with enthusiastic voices. Audition 2-3 voices before committing.
- If the narration is re-written in Step 3 after Step 5 has run, the whole timing map is stale. Re-run the TTS + transcribe cycle.
- Word-level timestamps from Whisper (the default transcriber) are accurate to ~80ms. Don't over-snap visuals to exact word boundaries — it looks mechanical.

## Cross-references

- [TECH-hyperframes-capture-step-3-script](TECH-hyperframes-capture-step-3-script.md), [TECH-hyperframes-capture-step-4-storyboard](TECH-hyperframes-capture-step-4-storyboard.md), [TECH-hyperframes-capture-step-6-build](TECH-hyperframes-capture-step-6-build.md)
- [TECH-hyperframes-cli-tts](TECH-hyperframes-cli-tts.md), [TECH-hyperframes-cli-transcribe](TECH-hyperframes-cli-transcribe.md)
- `../SKILL.md`
